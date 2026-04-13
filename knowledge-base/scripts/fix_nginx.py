import paramiko
import time

HOST = "204.168.183.104"
USER = "root"
PASSWORD = "FaCbEttkhn9UukpesrUr"

def run(client, cmd, timeout=30):
    print(f"\n>>> {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode()
    err = stderr.read().decode()
    if out:
        print(out.rstrip())
    if err:
        print("STDERR:", err.rstrip()[:500])
    return out

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USER, password=PASSWORD, timeout=15)
print(f"Connected to {HOST}")

# Step 1: Check current state
run(client, "ls -la /opt/southconsultants/marketing/ 2>&1 || echo 'Directory empty or missing'")

# Step 2: Create dir and clone/pull the repo
run(client, """
mkdir -p /opt/southconsultants/marketing
if [ -d /opt/southconsultants/marketing/.git ]; then
    echo 'Repo exists, pulling latest...'
    git -C /opt/southconsultants/marketing pull
else
    echo 'Cloning southconsultants-website repo...'
    git clone https://github.com/Samdc45/southconsultants-website.git /opt/southconsultants/marketing/
fi
""", timeout=60)

# Step 3: Confirm files are there
run(client, "ls /opt/southconsultants/marketing/")

# Step 4: Find the live Nginx config
run(client, "ls /etc/nginx/sites-enabled/ 2>/dev/null; ls /etc/nginx/conf.d/ 2>/dev/null")

# Step 5: Read the live Nginx config
config_out = run(client, """
for f in /etc/nginx/sites-enabled/southconsultants* /etc/nginx/conf.d/southconsultants*; do
    [ -f "$f" ] && echo "=== $f ===" && cat "$f"
done
""")

# Step 6: Fix the root path in the Nginx config
# The config points to /opt/southconsultants/marketing/dist — change to /opt/southconsultants/marketing
run(client, r"""
for f in /etc/nginx/sites-enabled/southconsultants* /etc/nginx/conf.d/southconsultants*; do
    [ -f "$f" ] && sed -i 's|root /opt/southconsultants/marketing/dist;|root /opt/southconsultants/marketing;|g' "$f" && echo "Patched $f"
done
""")

# Step 7: Test Nginx config
run(client, "nginx -t 2>&1")

# Step 8: Reload Nginx
run(client, "systemctl reload nginx && echo 'Nginx reloaded successfully'")

# Step 9: Confirm the root path is now correct
run(client, r"""
for f in /etc/nginx/sites-enabled/southconsultants* /etc/nginx/conf.d/southconsultants*; do
    [ -f "$f" ] && grep 'root' "$f"
done
""")

client.close()
print("\nDone. SSH connection closed.")
