"""
Multi-platform SEO signals — inject missing tags across all pages.

Adds to every page:
  - twitter:site handle (@SouthConsultants)
  - og:locale (en_AU for course pages, en_AU for core)
  - Bing/Yahoo msvalidate.01 meta tag (placeholder — needs real code from Bing Webmaster)
  - Yandex verification meta tag (placeholder)
  - BreadcrumbList schema.org structured data
  - Apple touch icon link tag

Also adds to index.html only:
  - Organization schema with sameAs social profiles
  - WebSite schema with SearchAction (Sitelinks searchbox)
"""

import re, os, json
from pathlib import Path

BASE = Path('/home/ubuntu/sc-website')
SITE = 'https://southconsultants.biz'

# ─── BING / YAHOO / YANDEX VERIFICATION ──────────────────────────────────────
# These are placeholder values — real codes come from Bing Webmaster Tools and Yandex.Webmaster
# We add the tags now so the structure is ready; Sam just needs to replace the values
BING_CODE    = 'BING_VERIFY_CODE_REPLACE_ME'
YANDEX_CODE  = 'YANDEX_VERIFY_CODE_REPLACE_ME'
TWITTER_HANDLE = '@SouthConsultants'

# ─── COMMON HEAD ADDITIONS ───────────────────────────────────────────────────

COMMON_TAGS = f"""  <!-- Bing / Yahoo Webmaster Verification -->
  <meta name="msvalidate.01" content="{BING_CODE}">
  <!-- Yandex Webmaster Verification -->
  <meta name="yandex-verification" content="{YANDEX_CODE}">
  <!-- X (Twitter) site handle -->
  <meta name="twitter:site" content="{TWITTER_HANDLE}">
  <meta name="twitter:creator" content="{TWITTER_HANDLE}">
  <!-- Apple Touch Icon -->
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">"""


def get_breadcrumb_schema(page_path):
    """Generate BreadcrumbList JSON-LD for a given page path."""
    parts = page_path.replace(str(BASE) + '/', '').replace('/index.html', '').split('/')
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    pos = 2

    if parts[0] == 'courses.html' or parts[0] == 'courses':
        items.append({"@type": "ListItem", "position": 2, "name": "Courses", "item": SITE + "/courses"})
        pos = 3
    elif parts[0] == 'sitemate.html':
        items.append({"@type": "ListItem", "position": 2, "name": "SiteMate", "item": SITE + "/sitemate"})
        return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}, indent=2)

    if len(parts) >= 2 and parts[0] == 'courses':
        course_slug = parts[1]
        course_name = course_slug.replace('-', ' ').title()
        course_url  = f"{SITE}/courses/{course_slug}/"
        items.append({"@type": "ListItem", "position": pos, "name": course_name, "item": course_url})
        pos += 1

        if len(parts) >= 3:
            region_slug = parts[2]
            region_name = region_slug.replace('-', ' ').title()
            region_url  = f"{SITE}/courses/{course_slug}/{region_slug}/"
            items.append({"@type": "ListItem", "position": pos, "name": region_name, "item": region_url})

    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}, indent=2)


ORGANIZATION_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "South Consultants",
    "url": SITE,
    "logo": f"{SITE}/logo.png",
    "description": "Civil construction AI platforms and training for the APAC region — SiteMate, SiteGuard, TruPeg.",
    "areaServed": ["AU", "NZ", "SG", "MY", "PH", "AE", "GB", "CA"],
    "sameAs": [
        "https://www.linkedin.com/company/south-consultants",
        "https://twitter.com/SouthConsultants",
        "https://www.facebook.com/southconsultants"
    ],
    "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer service",
        "email": "sam@southconsultants.biz",
        "areaServed": "APAC"
    }
}, indent=2)

WEBSITE_SCHEMA = json.dumps({
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "South Consultants",
    "url": SITE,
    "potentialAction": {
        "@type": "SearchAction",
        "target": {
            "@type": "EntryPoint",
            "urlTemplate": f"{SITE}/courses?q={{search_term_string}}"
        },
        "query-input": "required name=search_term_string"
    }
}, indent=2)


def inject_tags(html, extra_head, breadcrumb_schema, is_homepage=False):
    """Inject all missing tags into <head>."""

    # 1. Add common tags before </head>
    if BING_CODE not in html:
        html = html.replace('</head>', extra_head + '\n</head>', 1)

    # 2. Add og:locale if missing on course pages
    if 'og:locale' not in html:
        html = html.replace(
            'property="og:site_name"',
            'property="og:site_name"',
        )
        # Insert og:locale after og:site_name
        html = re.sub(
            r'(<meta property="og:site_name"[^>]+>)',
            r'\1\n  <meta property="og:locale" content="en_AU">',
            html, count=1
        )

    # 3. Add BreadcrumbList schema if not already present
    if 'BreadcrumbList' not in html:
        breadcrumb_block = f'\n<script type="application/ld+json">\n{breadcrumb_schema}\n</script>'
        html = html.replace('</head>', breadcrumb_block + '\n</head>', 1)

    # 4. Add Organization + WebSite schema to homepage only
    if is_homepage:
        if '"WebSite"' not in html:
            org_block = f'\n<script type="application/ld+json">\n{ORGANIZATION_SCHEMA}\n</script>'
            web_block = f'\n<script type="application/ld+json">\n{WEBSITE_SCHEMA}\n</script>'
            html = html.replace('</head>', org_block + web_block + '\n</head>', 1)

    return html


count = 0
errors = []

# Process all HTML files
all_files = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        if f.endswith('.html'):
            all_files.append(Path(root) / f)

for path in all_files:
    try:
        html = path.read_text()
        is_hp = (path == BASE / 'index.html')
        breadcrumb = get_breadcrumb_schema(str(path))
        new_html = inject_tags(html, COMMON_TAGS, breadcrumb, is_homepage=is_hp)
        if new_html != html:
            path.write_text(new_html)
            print(f"  ✓ {path.relative_to(BASE)}")
            count += 1
        else:
            print(f"  - {path.relative_to(BASE)} (no changes needed)")
    except Exception as e:
        errors.append((str(path), str(e)))
        print(f"  ✗ ERROR {path}: {e}")

print(f"\n=== {count} files updated ===")
if errors:
    print(f"ERRORS: {errors}")
