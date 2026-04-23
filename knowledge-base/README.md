# South Consultants — Knowledge Base

This is the master knowledge base for South Consultants. It contains all strategic documents, operational playbooks, scripts, and reusable skills built by Manus AI. Every Manus session should start by reading this folder and end by committing new documents here.

**Last updated:** April 2026

---

## Folder Structure

| Folder | Contents |
|---|---|
| `infrastructure/` | Server architecture, deployment plans, budgeted roadmaps |
| `funding/` | Grant and investment playbooks by region |
| `seo-and-website/` | SEO audit findings, keyword strategy, page inventory |
| `skills/` | Reusable Manus skills — read SKILL.md in each subfolder |
| `scripts/` | Python scripts for SEO fixes, content generation, server health |

---

## Infrastructure

### `South Consultants Infrastructure Delivery.md`
The master infrastructure document. Covers the full stack: Hetzner server (IP: 204.168.183.104), Docker/Nginx/Portainer setup, GitHub repos, Supabase database, and the 12-month migration roadmap from Base44/Wix to fully independent infrastructure.

**Key credentials (also in `sc-infrastructure` private repo):**
- Server IP: `204.168.183.104`
- SSH Key: `~/.ssh/sc_server` (in Manus sandbox)
- Web root: `/opt/southconsultants/marketing/`
- Nginx config: `/etc/nginx/sites-available/southconsultants.conf`

### `South_Consultants_Budgeted_Plan.md`
Step-by-step delivery plan with effort estimates (~157 hours total) and monthly running costs (~$75–150 NZD).

---

## Funding

### `NZ_Funding_Playbook_2026.md`
Detailed NZ funding guide post-Callaghan disestablishment. Covers MBIE New to R&D Grant ($400k), RDTI 15% tax credit, WNT Ventures ($35k pre-incubation + $750k loan), NZGCP Scout/Aspire funds, and RBPN vouchers.

**Immediate action:** Register at https://web.regionalbusinesspartners.co.nz/business/

### `Global_Funding_Options_TruPeg_CivilApp.md`
APAC and Europe funding overview covering Singapore Startup SG Tech, South Korea TIPS ($40B 2026 initiative), EIC Accelerator (€2.5M non-dilutive + €10M equity), and Eurostars.

---

## SEO & Website

**Current site:** https://southconsultants.biz
**GitHub repo:** https://github.com/Samdc45/southconsultants-website
**Total pages:** 39 (3 core + 4 course index + 32 regional)

**SEO status as of April 2026:**
- Redirect loop: Fixed (Nginx rewritten)
- Canonical conflicts: Fixed
- Thin content: Fixed (all pages 485–623 words)
- APAC repositioning: Complete
- SEA pages (SG, MY, PH): Live — 12 new pages
- Multi-platform signals (Bing, X, Yandex, OG): Live
- Sitemap: 39 URLs at /sitemap.xml — needs resubmission in Search Console

---

## Skills

### `skills/website-health-seo-audit/`
Full workflow for checking site health, auditing SEO, fixing Nginx, deploying to Hetzner, and analysing Google Search Console crawl stats. Read `SKILL.md` for instructions.

---

## Scripts

| Script | Purpose |
|---|---|
| `fix_nginx.py` | Paramiko SSH script to fix Nginx redirect loop on Hetzner |
| `fix_seo.py` | Rewrites meta tags, canonicals, robots across all HTML pages |
| `apac_seo.py` | Repositions keyword strategy from NZ-only to APAC |
| `enrich_content.py` | Adds 400–600 words of unique body copy to thin course pages |
| `multiplatform_seo.py` | Injects Twitter/X, Bing, Yandex, OG, breadcrumb schema signals |
| `gen_sea_pages.py` | Generates regional pages for Singapore, Malaysia, Philippines |
| `crawl_analysis.py` | Reads Google Search Console CSV exports and generates charts |

---

## SiteMate Pro Development Review

### `skills/sitemate-pro-development-review.md`
Knowledge package extracted from the Manus session reviewing the SiteMate codebase and PITCH_DECK_PROFESSIONAL.md. Covers the full tech stack (React/Vite/Tailwind/Base44 SDK), LMS development phases 1-6, AI-powered EDPP course generator architecture, branding decisions (blue + orange), and Base44 publishing status.

**Key URLs from that session:**
- Dev build: `https://sitematepro-arbd2w84.manus.space`
- Production target: `https://sitemate.base44.app`
- Source repo: `Samdc45/sitesafe`
