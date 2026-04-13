# SEO Checklist — southconsultants.biz Standard

This checklist covers every SEO signal implemented on the site. Use it to audit new pages or verify existing ones.

## Per-Page Signals (Required on Every Page)

### Head Tags
- [ ] `<title>` — 50–60 chars, keyword-first, unique per page
- [ ] `<meta name="description">` — 140–155 chars, includes primary keyword, unique per page
- [ ] `<link rel="canonical">` — matches the exact URL the server serves (with or without trailing slash — be consistent)
- [ ] `<meta name="robots" content="index, follow">`
- [ ] `<meta name="keywords">` — comma-separated (Google ignores it, but Bing reads it)
- [ ] `<meta name="viewport" content="width=device-width, initial-scale=1.0">`

### Open Graph (Facebook, LinkedIn, WhatsApp)
- [ ] `<meta property="og:title">` — same as `<title>` or slightly longer
- [ ] `<meta property="og:description">` — same as meta description
- [ ] `<meta property="og:image">` — absolute URL, 1200×630px, hosted on own domain
- [ ] `<meta property="og:url">` — canonical URL
- [ ] `<meta property="og:type">` — `website` for core pages, `article` for blog posts
- [ ] `<meta property="og:locale">` — `en_AU` for APAC targeting

### Twitter / X Card
- [ ] `<meta name="twitter:card" content="summary_large_image">`
- [ ] `<meta name="twitter:site" content="@YourHandle">`
- [ ] `<meta name="twitter:title">`
- [ ] `<meta name="twitter:description">`
- [ ] `<meta name="twitter:image">` — same as og:image

### Structured Data (JSON-LD)
- [ ] `BreadcrumbList` — on all pages except homepage
- [ ] `Course` schema — on all course pages (name, description, provider, offers, areaServed)
- [ ] `Organization` schema — homepage only
- [ ] `WebSite` schema with `SearchAction` — homepage only

### Multi-Search Engine Verification
- [ ] `<meta name="msvalidate.01">` — Bing/Yahoo verification code
- [ ] `<meta name="yandex-verification">` — Yandex verification code

### Regional Pages (hreflang)
- [ ] `<link rel="alternate" hreflang="en-NZ">` — NZ pages
- [ ] `<link rel="alternate" hreflang="en-AU">` — AU pages
- [ ] `<link rel="alternate" hreflang="en-SG">` — Singapore pages
- [ ] `<link rel="alternate" hreflang="en-MY">` — Malaysia pages
- [ ] `<link rel="alternate" hreflang="en-PH">` — Philippines pages
- [ ] `<link rel="alternate" hreflang="en-GB">` — UK pages
- [ ] `<link rel="alternate" hreflang="en-CA">` — Canada pages
- [ ] `<link rel="alternate" hreflang="en-AE">` — UAE pages

## Content Quality (Google Indexing Threshold)
- [ ] Minimum **400 words** of unique body text per page
- [ ] At least **2 paragraphs** of region-specific content on regional pages
- [ ] FAQ section (4+ Q&As) on course pages
- [ ] Compliance/regulatory references specific to the region
- [ ] Internal links to 2+ related pages

## Site-Level Files
- [ ] `sitemap.xml` — all URLs with trailing-slash consistency, `<lastmod>`, `<changefreq>`, `<priority>`
- [ ] `robots.txt` — `Sitemap:` directive pointing to full sitemap URL
- [ ] `favicon.ico` — present at root
- [ ] `apple-touch-icon.png` — 180×180px

## APAC Keyword Strategy
Target these clusters in titles, H1s, and meta descriptions:

| Cluster | Primary Keyword | Secondary |
|---|---|---|
| Platform | `civil construction AI platform APAC` | `construction management software` |
| Safety | `site safety app APAC` | `digital induction software Australia` |
| Training | `civil construction training APAC` | `online construction courses Southeast Asia` |
| Mapping | `underground asset mapping APAC` | `utility detection software NZ` |
| Induction | `civil industry induction APAC` | `CIDB induction Malaysia` |

## Google Search Console Actions After Deployment
1. Delete old failed sitemap entry
2. Resubmit `sitemap.xml`
3. Use URL Inspection tool on key pages to request indexing
4. Check "Pages" report after 7 days — "Discovered but not indexed" should drop to 0
