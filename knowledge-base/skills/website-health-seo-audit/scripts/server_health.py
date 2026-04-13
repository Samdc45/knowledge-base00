#!/usr/bin/env python3
"""
server_health.py — Check HTTP status, SSL, DNS, and redirect chains for a domain.

Usage:
    python server_health.py <domain>

Example:
    python server_health.py southconsultants.biz
"""
import sys
import subprocess
import socket

def run(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        return r.stdout.strip() + r.stderr.strip()
    except Exception as e:
        return str(e)

def check_url(url, label):
    result = run(f"curl -skILm 10 '{url}' 2>&1 | grep -E 'HTTP/|Location:' | head -6")
    print(f"\n[{label}] {url}")
    print(result if result else '  (no response)')

def check_ssl(domain):
    result = run(
        f"echo | timeout 8 openssl s_client -connect {domain}:443 -servername {domain} 2>/dev/null "
        f"| openssl x509 -noout -subject -issuer -dates 2>/dev/null"
    )
    print(f"\n[SSL] {domain}")
    print(result if result else '  (SSL check failed — cert may be missing or expired)')

def check_dns(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"\n[DNS] {domain} → {ip}")
    except Exception as e:
        print(f"\n[DNS] FAILED: {e}")

def main():
    domain = sys.argv[1] if len(sys.argv) > 1 else 'southconsultants.biz'
    print(f"\n{'='*60}")
    print(f"SERVER HEALTH CHECK — {domain}")
    print(f"{'='*60}")

    check_dns(domain)
    check_ssl(domain)
    check_url(f'http://{domain}/', 'HTTP')
    check_url(f'https://{domain}/', 'HTTPS')
    check_url(f'https://www.{domain}/', 'WWW')

    # Check key pages
    for path in ['/', '/courses', '/sitemate', '/sitemap.xml', '/robots.txt']:
        check_url(f'https://{domain}{path}', f'PAGE {path}')

    print(f"\n{'='*60}")
    print("DONE — Review any non-200 responses above")

if __name__ == '__main__':
    main()
