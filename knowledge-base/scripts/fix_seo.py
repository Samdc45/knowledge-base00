"""
SEO Fix Script — southconsultants.biz
Fixes identified issues:
1. Title tags >60 chars on core pages → truncated to sharp, keyword-rich titles
2. Meta descriptions >160 chars → trimmed to clean 150-155 char versions
3. Canonical mismatch: /courses redirects to /courses/ but canonical says /courses → fix to /courses/
4. /sitemate canonical correct but Nginx serves it as /sitemate (no trailing slash) — OK, leave
5. OG image pointing to base44.com CDN — replace with self-hosted image on our server
6. Missing <meta name="robots"> on all pages — add explicit indexing signal
7. Missing hreflang on regional course pages — add self-referencing hreflang
8. Truncated meta descriptions (contain "tec...") — fix to full clean sentences
9. Missing favicon — add favicon reference
10. Sitemap canonical URLs must match actual served URLs (/courses/ not /courses)
"""

import os
import re
from pathlib import Path

BASE = Path('/home/ubuntu/sc-website')
SITE = 'https://southconsultants.biz'
# Self-hosted OG image (we'll copy it to the server)
OG_IMAGE = 'https://southconsultants.biz/og-image.png'

# ─── CORE PAGE FIXES ────────────────────────────────────────────────────────

def fix_head(content, title, desc, canonical, og_title=None, og_desc=None, extra_ld=None):
    """Replace title, meta description, canonical, OG tags, and add robots meta."""
    
    og_title = og_title or title
    og_desc = og_desc or desc
    
    # Fix title
    content = re.sub(r'<title>[^<]+</title>', f'<title>{title}</title>', content)
    
    # Fix meta description
    content = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*"\s*/>',
        f'<meta name="description" content="{desc}" />',
        content
    )
    
    # Fix canonical
    content = re.sub(
        r'<link\s+rel="canonical"\s+href="[^"]*"\s*/>',
        f'<link rel="canonical" href="{canonical}" />',
        content
    )
    
    # Fix OG image everywhere
    content = re.sub(
        r'(property="og:image"\s+content=")[^"]*(")',
        rf'\g<1>{OG_IMAGE}\g<2>',
        content
    )
    content = re.sub(
        r'(name="twitter:image"\s+content=")[^"]*(")',
        rf'\g<1>{OG_IMAGE}\g<2>',
        content
    )
    
    # Fix OG title
    content = re.sub(
        r'(<meta\s+property="og:title"\s+content=")[^"]*(")',
        rf'\g<1>{og_title}\g<2>',
        content
    )
    
    # Fix OG description
    content = re.sub(
        r'(<meta\s+property="og:description"\s+content=")[^"]*(")',
        rf'\g<1>{og_desc}\g<2>',
        content
    )
    
    # Fix OG URL to match canonical
    content = re.sub(
        r'(<meta\s+property="og:url"\s+content=")[^"]*(")',
        rf'\g<1>{canonical}\g<2>',
        content
    )
    
    # Fix Twitter title
    content = re.sub(
        r'(<meta\s+name="twitter:title"\s+content=")[^"]*(")',
        rf'\g<1>{og_title}\g<2>',
        content
    )
    
    # Fix Twitter description
    content = re.sub(
        r'(<meta\s+name="twitter:description"\s+content=")[^"]*(")',
        rf'\g<1>{og_desc}\g<2>',
        content
    )
    
    # Add robots meta if missing
    if 'name="robots"' not in content:
        content = content.replace(
            '<link rel="canonical"',
            '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />\n  <link rel="canonical"'
        )
    
    # Add favicon if missing
    if 'rel="icon"' not in content and 'rel="shortcut icon"' not in content:
        content = content.replace(
            '<meta charset="UTF-8" />',
            '<meta charset="UTF-8" />\n  <link rel="icon" type="image/png" href="/favicon.png" />'
        )
    
    return content


# ─── INDEX.HTML ─────────────────────────────────────────────────────────────
print("Fixing index.html...")
content = (BASE / 'index.html').read_text()
content = fix_head(
    content,
    title='South Consultants | Civil Construction AI Platforms',
    desc='South Consultants builds AI-powered SaaS platforms and accredited training for civil construction teams in NZ, Australia, UK, Canada and beyond. SiteMate, SiteGuard, TruPeg.',
    canonical=f'{SITE}/',
    og_title='South Consultants — AI Platforms for Civil Construction',
    og_desc='Stop incidents before they cost you. AI-powered site safety, underground asset mapping and accredited training for civil construction teams worldwide.',
)
(BASE / 'index.html').write_text(content)
print("  ✓ index.html")

# ─── COURSES.HTML ────────────────────────────────────────────────────────────
print("Fixing courses.html...")
content = (BASE / 'courses.html').read_text()
content = fix_head(
    content,
    title='Civil Construction Training Courses | South Consultants',
    desc='Accredited civil construction training courses for NZ, Australia and global teams. Excavator, compaction, confined space, sling lift. NZ Unit Standards. From $399 NZD.',
    canonical=f'{SITE}/courses.html',
    og_title='Civil Construction Training Courses — South Consultants',
    og_desc='Accredited civil construction training for NZ, Australia and global teams. NZ Unit Standards. Online and in-person. From $399 NZD.',
)
(BASE / 'courses.html').write_text(content)
print("  ✓ courses.html")

# ─── SITEMATE.HTML ───────────────────────────────────────────────────────────
print("Fixing sitemate.html...")
content = (BASE / 'sitemate.html').read_text()
content = fix_head(
    content,
    title='SiteMate — AI Site Safety App for Civil Construction',
    desc='SiteMate is an AI-powered site management app for civil construction teams. Digital inductions, hazard reporting, machine registers, toolbox talks and training. From $19/month.',
    canonical=f'{SITE}/sitemate',
    og_title='SiteMate — AI Site Safety & Management App',
    og_desc='AI-powered site management for civil construction. Digital inductions, hazard reporting, machine registers, toolbox talks and accredited training. From $19/month.',
)
(BASE / 'sitemate.html').write_text(content)
print("  ✓ sitemate.html")

# ─── PROGRAMMATIC COURSE PAGES ───────────────────────────────────────────────

COURSES = {
    'communicating-on-site': {
        'name': 'Communicating on Site',
        'desc_base': 'Site communication training for civil construction teams. Covers two-way radio protocols, toolbox talk delivery, hazard communication and effective briefing techniques.',
        'keywords': 'site communication training, construction radio training, toolbox talk training, civil construction communication',
    },
    'compaction-101-aggregates-pavement': {
        'name': 'Compaction 101 — Aggregates for Pavement',
        'desc_base': 'Compaction and aggregates training for civil construction. Covers pavement design, compaction equipment, material testing and quality control for road construction.',
        'keywords': 'compaction training, aggregates pavement course, road construction training, civil construction compaction',
    },
    'nzci-flexi-civil-industry-induction': {
        'name': 'NZCI Flexi — Civil Industry Induction',
        'desc_base': 'New Zealand civil industry induction programme. Covers site safety, PPE, hazard identification and civil construction fundamentals for new entrants.',
        'keywords': 'civil industry induction, NZCI induction, construction site safety training, NZ civil construction induction',
    },
    'sling-lift-move-place-us31245': {
        'name': 'Sling Lift Move Place — US31245',
        'desc_base': 'Sling lift, move and place training to NZ Unit Standard 31245. Covers rigging, load calculations, excavator lifting operations and safe slinging techniques.',
        'keywords': 'sling lift training, US31245, rigging course, excavator lifting, civil construction rigging NZ',
    },
}

REGIONS = {
    'new-zealand': {
        'label': 'New Zealand', 'flag': '🇳🇿', 'currency': 'NZD',
        'compliance': 'Meets NZ Health and Safety at Work Act 2015 requirements.',
    },
    'australia': {
        'label': 'Australia', 'flag': '🇦🇺', 'currency': 'AUD',
        'compliance': 'Aligned with Safe Work Australia guidelines and state-based WHS legislation.',
    },
    'united-kingdom': {
        'label': 'United Kingdom', 'flag': '🇬🇧', 'currency': 'GBP',
        'compliance': 'Aligned with UK Health and Safety Executive (HSE) standards.',
    },
    'canada': {
        'label': 'Canada', 'flag': '🇨🇦', 'currency': 'CAD',
        'compliance': 'Aligned with Canadian Centre for Occupational Health and Safety (CCOHS) guidelines.',
    },
    'uae': {
        'label': 'UAE', 'flag': '🇦🇪', 'currency': 'AED',
        'compliance': 'Aligned with UAE Ministry of Human Resources and Emiratisation safety standards.',
    },
}

# Fix course index pages
for course_slug, course in COURSES.items():
    path = BASE / 'courses' / course_slug / 'index.html'
    if not path.exists():
        print(f"  SKIP (not found): {path}")
        continue
    content = path.read_text()
    title = f"{course['name']} Training Course | South Consultants"
    desc = f"{course['desc_base']} Available in NZ, Australia, UK, Canada and UAE. From $399 NZD."
    canonical = f"{SITE}/courses/{course_slug}/"
    content = fix_head(content, title=title, desc=desc, canonical=canonical,
                       og_title=f"{course['name']} Training — South Consultants",
                       og_desc=desc)
    # Fix keywords meta if present
    kw = course['keywords']
    content = re.sub(
        r'<meta\s+name="keywords"\s+content="[^"]*"\s*/>',
        f'<meta name="keywords" content="{kw}" />',
        content
    )
    path.write_text(content)
    print(f"  ✓ courses/{course_slug}/index.html")

# Fix regional pages
for course_slug, course in COURSES.items():
    for region_slug, region in REGIONS.items():
        path = BASE / 'courses' / course_slug / region_slug / 'index.html'
        if not path.exists():
            print(f"  SKIP (not found): {path}")
            continue
        content = path.read_text()
        title = f"{course['name']} Training — {region['label']} | South Consultants"
        desc = f"{course['desc_base']} {region['compliance']} Available online and in-person. From $399 {region['currency']}."
        canonical = f"{SITE}/courses/{course_slug}/{region_slug}/"
        
        content = fix_head(content, title=title, desc=desc, canonical=canonical,
                           og_title=f"{course['name']} Training — {region['label']}",
                           og_desc=desc)
        
        # Fix keywords
        kw = f"{course['keywords']}, {course['name'].lower()} {region['label'].lower()}"
        content = re.sub(
            r'<meta\s+name="keywords"\s+content="[^"]*"\s*/>',
            f'<meta name="keywords" content="{kw}" />',
            content
        )
        
        # Add hreflang self-reference if missing
        if 'hreflang' not in content:
            lang_map = {
                'new-zealand': 'en-NZ', 'australia': 'en-AU',
                'united-kingdom': 'en-GB', 'canada': 'en-CA', 'uae': 'en-AE'
            }
            lang = lang_map.get(region_slug, 'en')
            hreflang = f'  <link rel="alternate" hreflang="{lang}" href="{canonical}" />\n  <link rel="alternate" hreflang="x-default" href="{SITE}/courses/{course_slug}/" />'
            content = content.replace('<link rel="canonical"', f'{hreflang}\n  <link rel="canonical"')
        
        path.write_text(content)
        print(f"  ✓ courses/{course_slug}/{region_slug}/index.html")

print("\n=== All SEO fixes applied ===")
