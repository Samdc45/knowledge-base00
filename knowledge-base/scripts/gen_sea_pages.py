"""
Generate 12 new Southeast Asia regional course pages:
- Singapore, Malaysia, Philippines × 4 courses = 12 pages
"""

import os
from pathlib import Path

BASE = Path('/home/ubuntu/sc-website')
SITE = 'https://southconsultants.biz'

# ─── REGION DEFINITIONS ──────────────────────────────────────────────────────

REGIONS = {
    'singapore': {
        'label': 'Singapore',
        'flag': '🇸🇬',
        'hreflang': 'en-SG',
        'currency': 'SGD',
        'price': '499',
        'compliance': 'Aligned with the Singapore Workplace Safety and Health (WSH) Act and MOM guidelines.',
        'context': 'Singapore has one of the most rigorous construction safety frameworks in Southeast Asia, governed by the Workplace Safety and Health (WSH) Act administered by the Ministry of Manpower (MOM). All construction workers are required to complete the Construction Safety Orientation Course (CSOC). Our courses complement and extend these requirements, providing practical skills for civil construction teams operating on major infrastructure projects including MRT expansions, expressways, and public housing developments.',
        'geo_kw': 'Singapore SG',
        'body_context': 'Suitable for teams working on Singapore civil infrastructure projects including MRT, expressways, HDB and commercial developments.',
        'regions_note': 'Content aligned to Singapore WSH Act and MOM construction safety requirements.',
    },
    'malaysia': {
        'label': 'Malaysia',
        'flag': '🇲🇾',
        'hreflang': 'en-MY',
        'currency': 'MYR',
        'price': '899',
        'compliance': 'Aligned with the Malaysia Occupational Safety and Health Act (OSHA 1994) and CIDB requirements.',
        'context': 'Malaysia\'s construction industry is regulated by the Construction Industry Development Board (CIDB) and the Department of Occupational Safety and Health (DOSH) under the Occupational Safety and Health Act 1994 (OSHA 1994). CIDB Green Card certification is mandatory for all construction workers. Our courses support CIDB compliance and provide practical civil construction skills for teams working on Malaysia\'s major infrastructure programmes including MRT3, Pan Borneo Highway, and the National Water Grid.',
        'geo_kw': 'Malaysia MY',
        'body_context': 'Suitable for teams working on Malaysian civil infrastructure projects including MRT3, Pan Borneo Highway, and federal road programmes.',
        'regions_note': 'Content aligned to Malaysia OSHA 1994 and CIDB construction safety requirements.',
    },
    'philippines': {
        'label': 'Philippines',
        'flag': '🇵🇭',
        'hreflang': 'en-PH',
        'currency': 'PHP',
        'price': '5999',
        'compliance': 'Aligned with the Philippines Occupational Safety and Health Standards (OSHS) and DOLE requirements.',
        'context': 'The Philippines construction industry is governed by the Department of Labor and Employment (DOLE) under the Occupational Safety and Health Standards (OSHS). Construction Safety and Health Officers (CSHO) are required on all major project sites. Our courses support DOLE compliance and provide internationally recognised civil construction skills for Filipino teams working domestically on the Build Better More programme and for OFW construction workers deployed across the Middle East, Singapore, and Australia.',
        'geo_kw': 'Philippines PH',
        'body_context': 'Suitable for Filipino construction teams working domestically and OFW workers deployed across APAC and the Middle East.',
        'regions_note': 'Content aligned to Philippines DOLE OSHS construction safety requirements.',
    },
}

# ─── COURSE DEFINITIONS ──────────────────────────────────────────────────────

COURSES = {
    'communicating-on-site': {
        'name': 'Communicating on Site',
        'slug': 'communicating-on-site',
        'keywords_base': 'site communication training APAC, construction radio training, toolbox talk training, civil construction communication course, site briefing training Southeast Asia',
        'description': 'Master site communication skills for civil construction. Covers two-way radio protocols, toolbox talk delivery, hazard communication, and effective briefing techniques for site supervisors and workers.',
        'learn': [
            'Two-way radio protocols and phonetic alphabet',
            'Toolbox talk planning and delivery',
            'Hazard communication and escalation',
            'Pre-start briefing techniques',
            'Communicating with subcontractors and visitors',
            'Written site communication and documentation',
        ],
        'duration': '1 day',
        'level': 'All levels',
    },
    'compaction-101-aggregates-pavement': {
        'name': 'Compaction 101 — Aggregates for Pavement',
        'slug': 'compaction-101-aggregates-pavement',
        'keywords_base': 'compaction training APAC, aggregates pavement course, road construction training, civil construction compaction Southeast Asia, compaction equipment training',
        'description': 'Compaction theory and practice for civil construction professionals. Covers aggregate selection, compaction equipment operation, quality testing, and pavement construction for road and infrastructure projects.',
        'learn': [
            'Aggregate types, grading and selection',
            'Compaction theory and proctor testing',
            'Roller and compactor operation',
            'In-situ density testing methods',
            'Pavement layer construction and tolerances',
            'Quality control and defect identification',
        ],
        'duration': '1 day',
        'level': 'Intermediate',
    },
    'nzci-flexi-civil-industry-induction': {
        'name': 'Civil Industry Induction',
        'slug': 'nzci-flexi-civil-industry-induction',
        'keywords_base': 'civil industry induction APAC, construction site induction Southeast Asia, civil construction safety training, site induction training online, construction induction course',
        'description': 'Civil industry induction programme for construction teams entering the civil infrastructure sector. Covers site safety, PPE, hazard identification, and civil construction fundamentals aligned to international safety standards.',
        'learn': [
            'Site safety rules and emergency procedures',
            'Personal protective equipment (PPE) requirements',
            'Hazard identification and risk assessment',
            'Working near plant and machinery',
            'Excavation and underground services awareness',
            'Environmental and community obligations',
        ],
        'duration': 'Half day',
        'level': 'Entry level',
    },
    'sling-lift-move-place-us31245': {
        'name': 'Sling Lift Move Place',
        'slug': 'sling-lift-move-place-us31245',
        'keywords_base': 'sling lift training APAC, rigging course Southeast Asia, excavator lifting training, civil construction rigging, load slinging training, lifting operations course',
        'description': 'Sling lift, move and place training for civil construction teams. Covers rigging principles, load calculations, excavator lifting operations, and safe slinging techniques aligned to international lifting standards.',
        'learn': [
            'Rigging principles and terminology',
            'Sling types, ratings and inspection',
            'Load calculation and centre of gravity',
            'Excavator and crane lifting operations',
            'Exclusion zones and communication signals',
            'Pre-lift planning and documentation',
        ],
        'duration': '1 day',
        'level': 'Intermediate',
    },
}

# ─── PAGE TEMPLATE ───────────────────────────────────────────────────────────

def make_page(course, region_slug, region):
    c = course
    r = region
    slug = c['slug']
    url = f"{SITE}/courses/{slug}/{region_slug}/"
    title = f"{c['name']} Training — {r['label']} | South Consultants"
    desc  = (f"{c['description'].split('.')[0]}. "
             f"{r['compliance']} "
             f"Available online and in-person. From {r['currency']} {r['price']}.")[:160]
    kw    = f"{c['keywords_base']}, {c['name'].lower()} {r['geo_kw'].lower()}"
    learn_items = '\n'.join(f'      <li>{item}</li>' for item in c['learn'])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <link rel="icon" type="image/png" href="/favicon.png" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <link rel="alternate" hreflang="{r['hreflang']}" href="{url}" />
  <link rel="alternate" hreflang="x-default" href="{SITE}/courses/{slug}/" />
  <link rel="canonical" href="{url}" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="{SITE}/og-image.png" />
  <meta property="og:site_name" content="South Consultants" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{SITE}/og-image.png" />

  <!-- Structured Data: Course -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Course",
    "name": "{c['name']} \u2014 {r['label']}",
    "description": "{c['description']}",
    "url": "{url}",
    "provider": {{
      "@type": "Organization",
      "name": "South Consultants",
      "url": "https://southconsultants.biz"
    }},
    "offers": {{
      "@type": "Offer",
      "price": "{r['price']}",
      "priceCurrency": "{r['currency']}",
      "availability": "https://schema.org/InStock",
      "url": "https://southconsultants.biz/courses"
    }},
    "courseMode": ["online", "onsite"],
    "educationalLevel": "{c['level']}",
    "timeRequired": "{c['duration']}",
    "inLanguage": "en",
    "hasCourseInstance": {{
      "@type": "CourseInstance",
      "courseMode": "online",
      "courseWorkload": "{c['duration']}"
    }}
  }}
  </script>

  <!-- Keywords -->
  <meta name="keywords" content="{kw}" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/style.css" />
  <style>
    .course-hero {{ background: var(--navy); padding: 120px 0 60px; text-align: center; }}
    .course-hero .eyebrow {{ color: var(--orange); font-size: 0.85rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 1rem; }}
    .course-hero h1 {{ color: #fff; font-size: clamp(2rem, 5vw, 3rem); margin-bottom: 1rem; max-width: 800px; margin-left: auto; margin-right: auto; }}
    .course-hero p {{ color: rgba(255,255,255,0.75); font-size: 1.1rem; max-width: 640px; margin: 0 auto 2rem; }}
    .course-meta {{ display: flex; gap: 2rem; justify-content: center; flex-wrap: wrap; margin-top: 2rem; }}
    .course-meta-item {{ background: rgba(255,255,255,0.1); border-radius: 8px; padding: 0.75rem 1.5rem; color: #fff; font-size: 0.9rem; }}
    .course-meta-item strong {{ display: block; font-size: 1.1rem; color: var(--orange); }}
    .course-body {{ max-width: 860px; margin: 0 auto; padding: 80px 2rem; }}
    .course-body h2 {{ color: var(--navy); font-size: 1.8rem; margin: 2.5rem 0 1rem; }}
    .course-body ul {{ padding-left: 1.5rem; color: #444; line-height: 2; }}
    .course-body ul li::marker {{ color: var(--orange); }}
    .compliance-box {{ background: #f0f7ff; border-left: 4px solid var(--navy); padding: 1.25rem 1.5rem; border-radius: 0 8px 8px 0; margin: 2rem 0; color: #333; font-size: 0.95rem; }}
    .enrol-section {{ background: var(--navy); padding: 80px 2rem; text-align: center; }}
    .enrol-section h2 {{ color: #fff; font-size: 2rem; margin-bottom: 1rem; }}
    .enrol-section p {{ color: rgba(255,255,255,0.75); margin-bottom: 2rem; }}
    .price-display {{ font-size: 3rem; font-weight: 900; color: var(--orange); margin: 1rem 0; }}
    .price-display span {{ font-size: 1rem; font-weight: 400; color: rgba(255,255,255,0.6); }}
    .breadcrumb {{ background: #f8f9fb; padding: 1rem 2rem; font-size: 0.85rem; color: #666; }}
    .breadcrumb a {{ color: var(--navy); text-decoration: none; }}
    .breadcrumb a:hover {{ color: var(--orange); }}
  </style>
</head>
<body>

  <!-- HEADER -->
  <header id="header">
    <div class="header-inner">
      <a href="/" class="logo">
        <img src="https://static.wixstatic.com/media/7b181a_155e82fd215044179419fe3c7d2cb72e~mv2.png" alt="South Consultants Logo" />
        <div class="logo-text">
          <span class="logo-name">South Consultants</span>
          <span class="logo-tagline">Smarter Operations. Safer Sites.</span>
        </div>
      </a>
      <nav id="nav">
        <a href="/#about">About</a>
        <a href="/#products">Products</a>
        <a href="/courses">Courses</a>
        <a href="/#training">Training</a>
        <a href="/#contact" class="nav-cta">Get in Touch</a>
      </nav>
      <button class="hamburger" id="hamburger" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>

  <!-- BREADCRUMB -->
  <div class="breadcrumb">
    <div class="container">
      <a href="/">Home</a> &rsaquo; <a href="/courses">Courses</a> &rsaquo; <a href="/courses/{slug}">{c['name']}</a> &rsaquo; {r['flag']} {r['label']}
    </div>
  </div>

  <!-- HERO -->
  <section class="course-hero">
    <div class="container">
      <p class="eyebrow">{r['flag']} {r['label']} &mdash; Civil Construction Training</p>
      <h1>{c['name']}</h1>
      <p>{c['description']}</p>
      <div class="course-meta">
        <div class="course-meta-item"><strong>{c['duration']}</strong>Duration</div>
        <div class="course-meta-item"><strong>{c['level']}</strong>Level</div>
        <div class="course-meta-item"><strong>{r['currency']} {r['price']}</strong>Price (excl. tax)</div>
        <div class="course-meta-item"><strong>Online &amp; On-site</strong>Delivery</div>
      </div>
    </div>
  </section>

  <!-- COURSE BODY -->
  <section class="course-body">
    <h2>About This Course</h2>
    <p>{c['description']}</p>

    <div class="compliance-box">
      <strong>Compliance &amp; Recognition</strong><br/>
      {r['compliance']}
    </div>

    <h2>What You Will Learn</h2>
    <ul>
{learn_items}
    </ul>

    <h2>Who Is This Course For?</h2>
    <p>This course is designed for civil construction professionals working in {r['label']} at the <strong>{c['level']}</strong> level. Whether you are new to the industry or looking to formalise your existing skills, this course provides the knowledge and practical competencies you need to work safely and effectively on civil construction sites.</p>

    <h2>Delivery Options</h2>
    <p>Available as <strong>online self-paced learning</strong> through the SiteMate platform, or as <strong>on-site group training</strong> delivered to your team anywhere in {r['label']}. Group discounts available for teams of 5 or more.</p>

    <h2>Regional Context — {r['label']}</h2>
    <p>{r['context']}</p>

    <div class="compliance-box">
      {r['regions_note']}
    </div>
  </section>

  <!-- ENROL SECTION -->
  <section class="enrol-section">
    <div class="container">
      <h2>Enrol in {c['name']}</h2>
      <p>{r['flag']} Available for teams in {r['label']}. Instant access on enrolment.</p>
      <div class="price-display">{r['currency']} {r['price']} <span>excl. tax</span></div>
      <a href="https://southconsultants.biz/courses" class="btn btn-primary" style="font-size:1.1rem;padding:1rem 2.5rem;">Enrol Now &rarr;</a>
      <p style="margin-top:1.5rem;font-size:0.9rem;color:rgba(255,255,255,0.5);">Or <a href="/#contact" style="color:var(--orange);">contact us</a> for group pricing and on-site delivery.</p>
    </div>
  </section>

  <!-- FOOTER -->
  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <img src="https://static.wixstatic.com/media/7b181a_155e82fd215044179419fe3c7d2cb72e~mv2.png" alt="South Consultants" style="height:40px;margin-bottom:0.5rem;" />
        <p>Smarter Operations. Safer Sites.</p>
      </div>
      <div class="footer-links">
        <a href="/">Home</a>
        <a href="/courses">Courses</a>
        <a href="/sitemate">SiteMate</a>
        <a href="/#contact">Contact</a>
      </div>
      <p class="footer-copy">&copy; 2026 South Consultants Ltd. Auckland, New Zealand.</p>
    </div>
  </footer>

  <script src="/main.js"></script>
</body>
</html>"""


# ─── GENERATE ALL 12 PAGES ───────────────────────────────────────────────────

count = 0
for region_slug, region in REGIONS.items():
    for course_slug, course in COURSES.items():
        out_dir = BASE / 'courses' / course_slug / region_slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / 'index.html'
        html = make_page(course, region_slug, region)
        out_path.write_text(html)
        print(f"  ✓ courses/{course_slug}/{region_slug}/index.html")
        count += 1

print(f"\n=== {count} pages generated ===")
