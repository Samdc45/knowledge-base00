"""
APAC SEO Repositioning — southconsultants.biz
Shifts all keyword signals from NZ-centric to APAC-first.

Strategy:
- Primary market: Australia + New Zealand (highest English-language civil construction spend in APAC)
- Secondary: Southeast Asia (Singapore, Malaysia, Philippines — growing infrastructure spend)
- Tertiary: UAE, Canada, UK (already have regional pages)
- Brand positioning: "APAC's civil construction AI platform" not "NZ training provider"
- Core differentiator: AI-powered, not just training — SiteMate, SiteGuard, TruPeg
"""

import re, os
from pathlib import Path

BASE = Path('/home/ubuntu/sc-website')
SITE = 'https://southconsultants.biz'
OG_IMAGE = 'https://southconsultants.biz/og-image.png'

def set_head(content, title, desc, canonical, keywords, og_title=None, og_desc=None):
    og_title = og_title or title
    og_desc  = og_desc  or desc

    content = re.sub(r'<title>[^<]+</title>', f'<title>{title}</title>', content)
    content = re.sub(r'(<meta\s+name="description"\s+content=")[^"]*(")', rf'\g<1>{desc}\g<2>', content)
    content = re.sub(r'(<link\s+rel="canonical"\s+href=")[^"]*(")', rf'\g<1>{canonical}\g<2>', content)
    content = re.sub(r'(<meta\s+property="og:title"\s+content=")[^"]*(")', rf'\g<1>{og_title}\g<2>', content)
    content = re.sub(r'(<meta\s+property="og:description"\s+content=")[^"]*(")', rf'\g<1>{og_desc}\g<2>', content)
    content = re.sub(r'(<meta\s+property="og:url"\s+content=")[^"]*(")', rf'\g<1>{canonical}\g<2>', content)
    content = re.sub(r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")', rf'\g<1>{og_title}\g<2>', content)
    content = re.sub(r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")', rf'\g<1>{og_desc}\g<2>', content)

    # Upsert keywords meta
    kw_tag = f'<meta name="keywords" content="{keywords}" />'
    if 'name="keywords"' in content:
        content = re.sub(r'<meta\s+name="keywords"\s+content="[^"]*"\s*/>', kw_tag, content)
    else:
        content = content.replace('<meta name="robots"', f'{kw_tag}\n  <meta name="robots"')

    return content


# ─── CORE PAGES ──────────────────────────────────────────────────────────────

print("=== Core Pages ===")

# index.html — APAC platform brand
content = (BASE / 'index.html').read_text()
content = set_head(
    content,
    title='South Consultants | Civil Construction AI Platforms — APAC',
    desc='South Consultants builds AI-powered SaaS platforms and accredited training for civil construction teams across APAC — Australia, NZ, Southeast Asia, UAE and beyond.',
    canonical=f'{SITE}/',
    keywords='civil construction AI platform APAC, site safety software Australia, construction management app NZ, SiteMate, SiteGuard, TruPeg, underground asset mapping APAC, civil construction technology',
    og_title='South Consultants — AI Platforms for Civil Construction Across APAC',
    og_desc='Stop incidents before they cost you. AI-powered site safety, underground asset mapping and accredited training for civil construction teams across Australia, NZ and Southeast Asia.',
)
(BASE / 'index.html').write_text(content)
print("  ✓ index.html")

# courses.html — APAC training hub
content = (BASE / 'courses.html').read_text()
content = set_head(
    content,
    title='Civil Construction Training Courses | APAC | South Consultants',
    desc='Accredited civil construction training for teams across Australia, NZ, Southeast Asia, UAE and Canada. Online and in-person. Compaction, induction, rigging, site communication. From $399.',
    canonical=f'{SITE}/courses.html',
    keywords='civil construction training APAC, online construction courses Australia NZ, construction safety training Southeast Asia, accredited civil training, compaction course, rigging course, site induction training',
    og_title='Civil Construction Training Courses — APAC | South Consultants',
    og_desc='Accredited civil construction training across Australia, NZ, Southeast Asia and beyond. Online and in-person. From $399.',
)
(BASE / 'courses.html').write_text(content)
print("  ✓ courses.html")

# sitemate.html — APAC SaaS positioning
content = (BASE / 'sitemate.html').read_text()
content = set_head(
    content,
    title='SiteMate — AI Site Safety App for Civil Construction | APAC',
    desc='SiteMate is an AI-powered site management platform for civil construction teams across APAC. Digital inductions, hazard reporting, machine registers, toolbox talks and training. From $19/month.',
    canonical=f'{SITE}/sitemate',
    keywords='site safety app APAC, digital induction software Australia, construction hazard reporting NZ, toolbox talk app, civil construction compliance software, site management app Southeast Asia, construction AI platform',
    og_title='SiteMate — AI Site Safety & Management App for APAC Civil Construction',
    og_desc='AI-powered site management for civil construction across APAC. Digital inductions, hazard reporting, machine registers, toolbox talks and accredited training. From $19/month.',
)
(BASE / 'sitemate.html').write_text(content)
print("  ✓ sitemate.html")

# ─── COURSE DEFINITIONS — APAC-FIRST ─────────────────────────────────────────

COURSES = {
    'communicating-on-site': {
        'name': 'Communicating on Site',
        'title_base': 'Communicating on Site Training Course | APAC | South Consultants',
        'desc_base': 'Site communication training for civil construction teams across APAC. Covers two-way radio protocols, toolbox talk delivery, hazard communication and effective briefing techniques. Available in Australia, NZ, Southeast Asia, UAE and Canada.',
        'keywords': 'site communication training APAC, construction radio training Australia, toolbox talk training NZ, civil construction communication course, site briefing training Southeast Asia',
    },
    'compaction-101-aggregates-pavement': {
        'name': 'Compaction 101 — Aggregates for Pavement',
        'title_base': 'Compaction 101 Training Course | APAC | South Consultants',
        'desc_base': 'Compaction and aggregates training for civil construction teams across APAC. Covers pavement design, compaction equipment, material testing and quality control. Available in Australia, NZ, Southeast Asia, UAE and Canada.',
        'keywords': 'compaction training APAC, aggregates pavement course Australia, road construction training NZ, civil construction compaction Southeast Asia, compaction equipment training',
    },
    'nzci-flexi-civil-industry-induction': {
        'name': 'NZCI Flexi — Civil Industry Induction',
        'title_base': 'Civil Industry Induction Training Course | APAC | South Consultants',
        'desc_base': 'Civil industry induction training for construction teams across APAC. Covers site safety, PPE, hazard identification and civil construction fundamentals. Meets NZ, Australian and international safety standards.',
        'keywords': 'civil industry induction APAC, construction site induction Australia, NZCI induction online, civil construction safety training NZ, site induction training Southeast Asia',
    },
    'sling-lift-move-place-us31245': {
        'name': 'Sling Lift Move Place — US31245',
        'title_base': 'Sling Lift Move Place Training Course | APAC | South Consultants',
        'desc_base': 'Sling lift, move and place training for civil construction teams across APAC. Covers rigging, load calculations, excavator lifting operations and safe slinging techniques. Aligned to NZ Unit Standard 31245.',
        'keywords': 'sling lift training APAC, rigging course Australia, excavator lifting training NZ, civil construction rigging Southeast Asia, US31245 sling lift course, load slinging training',
    },
}

REGIONS = {
    'new-zealand': {
        'label': 'New Zealand', 'currency': 'NZD',
        'compliance': 'Meets NZ Health and Safety at Work Act 2015 requirements.',
        'geo_kw': 'New Zealand NZ',
    },
    'australia': {
        'label': 'Australia', 'currency': 'AUD',
        'compliance': 'Aligned with Safe Work Australia guidelines and state WHS legislation.',
        'geo_kw': 'Australia AU',
    },
    'united-kingdom': {
        'label': 'United Kingdom', 'currency': 'GBP',
        'compliance': 'Aligned with UK Health and Safety Executive (HSE) standards.',
        'geo_kw': 'United Kingdom UK',
    },
    'canada': {
        'label': 'Canada', 'currency': 'CAD',
        'compliance': 'Aligned with Canadian Centre for Occupational Health and Safety guidelines.',
        'geo_kw': 'Canada',
    },
    'uae': {
        'label': 'UAE', 'currency': 'AED',
        'compliance': 'Aligned with UAE Ministry of Human Resources and Emiratisation safety standards.',
        'geo_kw': 'UAE Middle East',
    },
}

print("\n=== Course Index Pages ===")
for slug, course in COURSES.items():
    path = BASE / 'courses' / slug / 'index.html'
    if not path.exists():
        continue
    content = path.read_text()
    content = set_head(
        content,
        title=course['title_base'],
        desc=course['desc_base'],
        canonical=f'{SITE}/courses/{slug}/',
        keywords=course['keywords'],
        og_title=f"{course['name']} Training — APAC | South Consultants",
        og_desc=course['desc_base'][:160],
    )
    path.write_text(content)
    print(f"  ✓ courses/{slug}/index.html")

print("\n=== Regional Course Pages ===")
for slug, course in COURSES.items():
    for region, reg in REGIONS.items():
        path = BASE / 'courses' / slug / region / 'index.html'
        if not path.exists():
            continue
        content = path.read_text()

        title = f"{course['name']} Training — {reg['label']} | South Consultants"
        desc  = (f"{course['desc_base'].split('.')[0]}. "
                 f"{reg['compliance']} "
                 f"Available online and in-person. From $399 {reg['currency']}.")
        desc = desc[:160]
        canonical = f"{SITE}/courses/{slug}/{region}/"
        kw = f"{course['keywords']}, {course['name'].lower()} {reg['geo_kw'].lower()}"

        content = set_head(
            content,
            title=title,
            desc=desc,
            canonical=canonical,
            keywords=kw,
            og_title=f"{course['name']} Training — {reg['label']} | South Consultants",
            og_desc=desc,
        )
        path.write_text(content)
        print(f"  ✓ courses/{slug}/{region}/index.html")

print("\n=== APAC SEO repositioning complete ===")
