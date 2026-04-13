# Nginx Redirect Loop — Diagnosis and Fix Reference

## Common Root Causes

| Cause | Symptom | Fix |
|---|---|---|
| Certbot overwrote server block with `return 301 https://domain$request_uri` | HTTPS → 301 → HTTPS (infinite loop) | Rewrite server block with correct `root` and `try_files` |
| Web root directory is empty or missing | Nginx finds no content, falls through to redirect | Clone/deploy site files to the `root` path |
| Conflicting Nginx config files (e.g. default + custom) | Unpredictable routing | Remove or disable the conflicting config |
| `www` and non-`www` both redirecting to each other | www ↔ non-www loop | Ensure only one redirects to the other |

## Diagnosis Steps

```bash
# 1. Check what the server returns (follow redirects, show each hop)
curl -sILm 10 https://yourdomain.com/ | grep -E 'HTTP/|Location:'

# 2. Check SSL cert is valid and covers the domain
echo | timeout 8 openssl s_client -connect yourdomain.com:443 -servername yourdomain.com 2>/dev/null \
  | openssl x509 -noout -subject -dates

# 3. Read the live Nginx config on the server
ssh root@SERVER_IP "cat /etc/nginx/sites-enabled/*"

# 4. Check what files exist at the web root
ssh root@SERVER_IP "ls -la /opt/yoursite/marketing/"
```

## Correct Nginx Server Block Template

```nginx
# HTTP → HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://yourdomain.com$request_uri;
}

# HTTPS — serve static site
server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    root /opt/yoursite/marketing;
    index index.html;

    # Clean URLs — serve .html files without extension
    location / {
        try_files $uri $uri/ $uri.html =404;
    }

    # Serve /courses as courses.html (no .html in URL)
    location = /courses {
        try_files /courses.html =404;
    }
    location = /courses/ {
        return 301 /courses;
    }
}
```

## Deploy Fix via SSH

```bash
# Write corrected config
ssh -i ~/.ssh/sc_server root@SERVER_IP "cat > /etc/nginx/sites-available/yourdomain.com << 'NGINX'
<paste config above>
NGINX"

# Enable and test
ssh -i ~/.ssh/sc_server root@SERVER_IP "
  ln -sf /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/
  nginx -t && systemctl reload nginx
"
```

## Hetzner Server Access

- **Server IP:** 204.168.183.104
- **SSH key:** `~/.ssh/sc_server` (installed in Manus sandbox)
- **Password reset:** Use Hetzner API — `POST /servers/{id}/actions/reset_password`
- **API token env var:** `HETZNER_TOKEN`
