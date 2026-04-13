---
name: website-health-seo-audit
description: "Full website health check, SEO audit, and fix workflow for southconsultants.biz and its Hetzner-hosted static sites. Use for: checking if the site is live and returning correct HTTP status codes, diagnosing and fixing Nginx redirect loops, auditing all pages for SEO signals (meta tags, canonicals, word count, structured data), fixing thin content, expanding regional pages (APAC), implementing multi-platform signals (Bing, Yandex, Twitter/X, Open Graph), analysing Google Search Console crawl stats CSV exports, and deploying all changes to the Hetzner server via SSH and pushing to GitHub."
---

# Website Health & SEO Audit Skill

## Infrastructure Context

The southconsultants.biz marketing site is a **static HTML site** hosted on a Hetzner Cloud VPS. There is no build step — files are served directly by Nginx from `/opt/southconsultants/marketing/`.

| Component | Detail |
|---|---|
| Domain | `southconsultants.biz` |
| Server IP | `204.168.183.104` |
| SSH key | `~/.ssh/sc_server` (installed in Manus sandbox) |
| Web root | `/opt/southconsultants/marketing/` |
| GitHub repo | `Samdc45/southconsultants-website` |
| Nginx config | `/etc/nginx/sites-available/southconsultants.biz` |
| Hetzner API token env | `HETZNER_TOKEN` |

If the SSH key is missing, reset the root password via the Hetzner API and re-run the SSH setup script:
```bash
bash /home/ubuntu/skills/hetzner-server-deploy/scripts/setup_ssh.sh
```

---

## Workflow: Website Health Check

**Step 1 — Run the server health script:**
```bash
python /home/ubuntu/skills/website-health-seo-audit/scripts/server_health.py southconsultants.biz
```
This checks DNS, SSL validity, HTTP→HTTPS redirect, and all key page status codes.

**Step 2 — Interpret results.** Any non-200 response on a key page is a problem. Common issues:
- `301` loop on HTTPS → read `references/nginx-redirect-loop-fix.md`
- `403` on `/courses/` → Nginx is missing a `try_files` directive for that path
- `404` → page file is missing from the web root or Nginx config has wrong path

**Step 3 — Check SSL.** Cert must cover `southconsultants.biz` and `www.southconsultants.biz`. Expiry is in the server_health output. Let's Encrypt certs expire every 90 days — Certbot auto-renews if the cron is active.

---

## Workflow: SEO Audit

**Step 1 — Clone the repo locally:**
```bash
gh repo clone Samdc45/southconsultants-website ~/sc-website
```

**Step 2 — Run the SEO audit script:**
```bash
python /home/ubuntu/skills/website-health-seo-audit/scripts/seo_audit.py ~/sc-website
```
This outputs a table of every HTML file with title length, description length, word count, canonical URL, and a list of issues.

**Step 3 — Interpret results.** Key thresholds:

| Signal | Threshold | Google Impact |
|---|---|---|
| Title length | 50–60 chars | Over 60 = Google rewrites it |
| Description length | 140–155 chars | Under 100 = truncated in results |
| Word count | 400+ words | Under 400 = "Discovered but not indexed" |
| Canonical URL | Must match served URL exactly | Mismatch = duplicate content |
| Robots meta | Must be present | Absence = no explicit indexing signal |

**Step 4 — Fix issues.** Use `references/seo-checklist.md` as the standard. Write a Python fix script to batch-update all pages rather than editing files one by one.

---

## Workflow: Analysing Google Search Console Crawl Stats

When the user exports crawl stats CSVs from GSC (Settings → Crawl Stats → Export), run:
```bash
python /home/ubuntu/skills/website-health-seo-audit/scripts/crawl_stats_analysis.py \
  /path/to/csv/dir /path/to/output/dir
```

Expected CSV filenames: `Summarycrawlstatschart.csv`, `Responsetable.csv`, `Filetypetable.csv`, `Purposetable.csv`, `Googlebottypetable.csv`, `Hoststable.csv`.

Key signals to look for:

| Signal | Meaning |
|---|---|
| 301 rate > 5% | Redirect loop or canonical mismatch still present |
| 404 rate > 0% | Broken URLs — check Nginx access logs for exact paths |
| Download size = 0 KB | Google only checked headers (normal for new sites) |
| Smartphone bot absent | Mobile indexing not active — check viewport meta tag |

---

## Workflow: Deploy Changes to Server

After making changes locally in `~/sc-website`:

```bash
# Commit and push to GitHub
cd ~/sc-website
git add -A
git commit -m "SEO: describe what changed"
git push origin main

# Deploy to Hetzner via git pull
ssh -i ~/.ssh/sc_server -o StrictHostKeyChecking=no root@204.168.183.104 \
  "cd /opt/southconsultants/marketing && git pull origin main"
```

If git pull fails (e.g. diverged history), use rsync as a fallback:
```bash
rsync -avz --delete -e "ssh -i ~/.ssh/sc_server -o StrictHostKeyChecking=no" \
  ~/sc-website/ root@204.168.183.104:/opt/southconsultants/marketing/
```

---

## Workflow: Adding New Regional Pages

The site uses a pattern of `/courses/{course-slug}/{region}/index.html`. To add new regions:

1. Read an existing regional page (e.g. `courses/communicating-on-site/australia/index.html`) as the template.
2. Write a Python generator script that creates all `N_courses × N_regions` pages, substituting region name, hreflang code, pricing in local currency, compliance/regulatory body references, and infrastructure context.
3. Update `sitemap.xml` with the new URLs.
4. Deploy and push.

**Existing regions:** NZ, AU, UK, Canada, UAE, Singapore, Malaysia, Philippines

**Priority next regions:** Indonesia, Vietnam, Thailand

---

## Sitemap Resubmission (After Any Deployment)

After deploying changes that affect page URLs or content:
1. Go to [Google Search Console](https://search.google.com/search-console) → Sitemaps
2. Delete the old entry if it shows "Couldn't fetch"
3. Submit `sitemap.xml` (just the filename, not the full URL)
4. Use URL Inspection on key pages to request immediate indexing

---

## Reference Files

| File | When to Read |
|---|---|
| `references/nginx-redirect-loop-fix.md` | When `server_health.py` shows a 301 loop or 403 on HTTPS |
| `references/seo-checklist.md` | When auditing or building new pages — use as the complete standard |
