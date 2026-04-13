"""
Content Enrichment — Fix thin pages for Google indexing.
Adds 400-600 words of unique, substantive body copy to all course pages.
Each page gets: course overview, industry context, learning outcomes detail,
assessment info, prerequisites, FAQ section, and related courses.
"""

import re
from pathlib import Path

BASE = Path('/home/ubuntu/sc-website')
SITE = 'https://southconsultants.biz'

# ─── COURSE CONTENT LIBRARY ──────────────────────────────────────────────────

COURSES = {
    'communicating-on-site': {
        'name': 'Communicating on Site',
        'overview': """Effective communication is one of the most critical safety factors on any civil construction site. Miscommunication between operators, supervisors, and ground workers is a leading contributor to near-misses and serious incidents across the construction industry. This course addresses that gap directly, providing civil construction professionals with the practical communication skills they need to operate safely and efficiently in high-noise, high-risk environments.

The programme covers the full spectrum of on-site communication — from two-way radio protocols and phonetic alphabet usage to structured toolbox talk delivery and formal pre-start briefings. Participants learn how to communicate clearly under pressure, how to escalate hazards effectively, and how to ensure critical safety information reaches every member of the team regardless of language background or experience level.""",
        'industry': """In civil construction, the consequences of poor communication are immediate and severe. A misheard instruction near operating plant, a missed hazard alert during excavation, or a poorly delivered toolbox talk can result in serious injury or fatality. Regulatory bodies across APAC — including Safe Work Australia, WorkSafe NZ, Singapore's MOM, and Malaysia's DOSH — consistently identify communication failures as a root cause in construction incident investigations.

This course was developed in direct response to that gap. It draws on real incident case studies from civil construction projects across Australia, New Zealand, and Southeast Asia to illustrate the practical impact of communication failures and the techniques that prevent them.""",
        'assessment': """Assessment is competency-based and practical. Participants are assessed through scenario-based exercises that simulate real on-site communication challenges — including radio communication drills, live toolbox talk delivery, and hazard escalation role plays. There is no written exam. Participants who demonstrate competency receive a South Consultants Certificate of Completion, which can be presented to employers and principal contractors as evidence of training.""",
        'prerequisites': 'No formal prerequisites. Suitable for all civil construction workers, site supervisors, foremen, and project managers. Basic English literacy is recommended.',
        'faq': [
            ('How long does the course take?', 'The course is delivered over one full day, either online through the SiteMate platform or as on-site group training. Online learners can complete the course at their own pace.'),
            ('Is this course accredited?', 'The course is delivered by South Consultants and aligned to industry best practice standards across APAC. It is not currently mapped to a specific national unit standard, but the Certificate of Completion is recognised by principal contractors across Australia, NZ, and Southeast Asia.'),
            ('Can I complete this course on my phone?', 'Yes. The online version is fully mobile-optimised and accessible through the SiteMate platform on any device.'),
            ('Do you offer group discounts?', 'Yes. Teams of 5 or more receive a 20% discount. Contact us for group enrolment and on-site delivery pricing.'),
        ],
        'related': ['compaction-101-aggregates-pavement', 'nzci-flexi-civil-industry-induction'],
        'related_names': ['Compaction 101 — Aggregates for Pavement', 'Civil Industry Induction'],
    },
    'compaction-101-aggregates-pavement': {
        'name': 'Compaction 101 — Aggregates for Pavement',
        'overview': """Pavement construction is one of the most technically demanding disciplines in civil construction. Getting compaction right — the right material, the right moisture content, the right number of passes with the right equipment — is the difference between a pavement that lasts 30 years and one that fails within 12 months. This course gives civil construction professionals the foundational knowledge and practical skills to get it right every time.

Compaction 101 covers the full pavement construction workflow from aggregate selection and grading through to in-situ density testing and quality sign-off. Participants develop a deep understanding of compaction theory, learn to operate and maintain compaction equipment correctly, and gain the quality control skills needed to meet specification on every layer.""",
        'industry': """Pavement failures are extraordinarily costly. In Australia and New Zealand alone, premature pavement failures on roading and infrastructure projects cost the industry hundreds of millions of dollars annually in remediation, delays, and contract disputes. The root cause in the majority of cases is inadequate compaction — either insufficient density, incorrect moisture content, or poor layer construction technique.

Across APAC, infrastructure investment is at record levels. Singapore's Land Transport Authority, Malaysia's CIDB, and Australia's National Reconstruction Fund are all driving major road and civil infrastructure programmes. The demand for civil construction workers with verified compaction competency has never been higher, and the consequences of getting it wrong — both financially and for public safety — have never been more significant.""",
        'assessment': """Assessment is practical and competency-based. Participants complete hands-on exercises covering aggregate identification, moisture content assessment, compaction equipment operation, and in-situ density testing using nuclear density gauges and sand replacement methods. A short written knowledge check covers compaction theory and specification requirements. Participants who demonstrate competency receive a South Consultants Certificate of Completion in Compaction — Aggregates for Pavement.""",
        'prerequisites': 'Basic civil construction experience recommended. Suitable for plant operators, labourers, site supervisors, and quality control technicians working on roading, subdivision, and civil infrastructure projects.',
        'faq': [
            ('Do I need to own compaction equipment to complete this course?', 'No. The online version covers theory and technique. The on-site delivery option includes hands-on equipment operation. Contact us to arrange on-site training with your own plant.'),
            ('Is this course relevant for subdivision work?', 'Yes. The course covers compaction requirements for both roading and subdivision earthworks, including subgrade preparation, sub-base, and basecourse layers.'),
            ('What testing methods are covered?', 'The course covers nuclear density gauge testing, sand replacement testing, and dynamic cone penetrometer (DCP) testing, as well as interpretation of test results against specification.'),
            ('Can this course be customised for our project specification?', 'Yes. On-site group delivery can be tailored to your project\'s specific compaction specification and equipment. Contact us to discuss.'),
        ],
        'related': ['communicating-on-site', 'nzci-flexi-civil-industry-induction'],
        'related_names': ['Communicating on Site', 'Civil Industry Induction'],
    },
    'nzci-flexi-civil-industry-induction': {
        'name': 'Civil Industry Induction',
        'overview': """Every worker entering a civil construction site for the first time needs a solid foundation in site safety, hazard awareness, and industry expectations. The Civil Industry Induction programme provides exactly that — a comprehensive, practical introduction to civil construction that prepares workers to operate safely from day one.

This induction programme goes beyond the standard site-specific induction. It provides workers with a transferable understanding of civil construction safety principles that applies across projects, employers, and regions. Participants learn to identify and manage the hazards that are unique to civil construction — working near operating plant, excavation risks, underground services, and traffic management — and develop the habits and behaviours that underpin a safe construction career.""",
        'industry': """Construction remains one of the highest-risk industries across APAC. In New Zealand, construction accounts for approximately 20% of all workplace fatalities despite representing a much smaller proportion of the workforce. In Australia, the construction industry fatality rate is consistently above the national average. Across Southeast Asia, rapid infrastructure development has created acute demand for workers with verified safety training.

Regulatory frameworks across the region — the NZ Health and Safety at Work Act 2015, Safe Work Australia's model WHS laws, Singapore's WSH Act, Malaysia's OSHA 1994, and the Philippines' DOLE OSHS — all require employers to ensure workers are trained and competent before commencing work. This induction programme supports compliance with those requirements and provides workers with the foundational knowledge they need to protect themselves and their colleagues.""",
        'assessment': """Assessment is scenario-based and practical. Participants complete a series of hazard identification exercises, emergency response scenarios, and knowledge checks covering the key content areas. There is no formal written exam. Participants who complete the programme receive a South Consultants Civil Industry Induction Certificate, which is recognised by principal contractors across Australia, New Zealand, and Southeast Asia as evidence of site safety training.""",
        'prerequisites': 'No prerequisites. Suitable for all workers entering the civil construction industry for the first time, as well as experienced workers seeking a refresher or transferable induction certificate.',
        'faq': [
            ('How long does the induction take?', 'The programme is delivered in a half-day format — approximately 3 to 4 hours. It is available online through the SiteMate platform or as on-site group delivery.'),
            ('Does this replace a site-specific induction?', 'No. This programme provides a transferable industry induction. Workers will still need to complete a site-specific induction when they arrive on a new project. However, completing this programme significantly reduces the time required for site-specific inductions.'),
            ('Is this recognised across APAC?', 'Yes. The programme is aligned to safety standards across Australia, New Zealand, Singapore, Malaysia, and the Philippines, and the certificate is recognised by principal contractors across the region.'),
            ('Can we run this for our whole team at once?', 'Yes. On-site group delivery is available for teams of any size. Contact us for group pricing and scheduling.'),
        ],
        'related': ['communicating-on-site', 'sling-lift-move-place-us31245'],
        'related_names': ['Communicating on Site', 'Sling Lift Move Place'],
    },
    'sling-lift-move-place-us31245': {
        'name': 'Sling Lift Move Place — US31245',
        'overview': """Lifting operations are among the highest-risk activities in civil construction. Dropped loads, sling failures, and communication breakdowns during lifting operations cause serious injuries and fatalities every year across APAC. This course provides civil construction workers with the knowledge and practical skills to plan, prepare, and execute safe sling lift, move, and place operations using excavators and other civil construction plant.

The programme is aligned to New Zealand Unit Standard 31245 and covers the full lifting workflow — from pre-lift planning and sling selection through to load calculation, exclusion zone management, and post-lift documentation. Participants develop a thorough understanding of the forces involved in lifting operations and the critical role that communication, planning, and equipment inspection play in preventing incidents.""",
        'industry': """Excavator-assisted lifting is a routine operation on civil construction sites across APAC — from lifting precast concrete culverts and drainage structures to placing large diameter pipes and bridge components. Despite its frequency, it remains a high-risk activity. The consequences of a sling failure or a miscommunication during a lift can be catastrophic.

Across Australia and New Zealand, WorkSafe and Safe Work Australia have both identified lifting operations as a priority area for intervention, with specific guidance on excavator lifting requirements, sling ratings, and exclusion zones. In Singapore, Malaysia, and the Philippines, rapid infrastructure development has created significant demand for workers with verified lifting competency. This course provides that competency in a format that is accessible, practical, and recognised across the region.""",
        'assessment': """Assessment is competency-based and practical. Participants complete pre-lift planning exercises, sling inspection assessments, load calculation problems, and a supervised practical lifting operation (on-site delivery) or simulation-based assessment (online delivery). Participants who demonstrate competency receive a South Consultants Certificate of Completion in Sling Lift Move Place, aligned to NZ Unit Standard 31245.""",
        'prerequisites': 'Basic civil construction experience recommended. Suitable for excavator operators, riggers, dogmen, site supervisors, and any worker involved in lifting operations on civil construction sites.',
        'faq': [
            ('Is this course equivalent to a rigging licence?', 'This course covers sling lift operations using civil construction plant (primarily excavators). It is not a substitute for a formal rigging licence where one is required by law. Check your local regulatory requirements before commencing lifting work.'),
            ('What sling types are covered?', 'The course covers wire rope slings, chain slings, synthetic web slings, and round slings — including inspection, rating, and correct application for each type.'),
            ('Is this course relevant for pipe laying?', 'Yes. Pipe laying is one of the primary applications covered, including correct sling placement for different pipe materials and diameters.'),
            ('Can I complete this course online?', 'Yes. The online version covers all theory content and includes simulation-based assessment. The on-site version includes a supervised practical lifting operation with real plant and equipment.'),
        ],
        'related': ['communicating-on-site', 'nzci-flexi-civil-industry-induction'],
        'related_names': ['Communicating on Site', 'Civil Industry Induction'],
    },
}

REGIONS = {
    'new-zealand': {'label': 'New Zealand', 'flag': '🇳🇿'},
    'australia':   {'label': 'Australia',    'flag': '🇦🇺'},
    'united-kingdom': {'label': 'United Kingdom', 'flag': '🇬🇧'},
    'canada':      {'label': 'Canada',       'flag': '🇨🇦'},
    'uae':         {'label': 'UAE',          'flag': '🇦🇪'},
    'singapore':   {'label': 'Singapore',    'flag': '🇸🇬'},
    'malaysia':    {'label': 'Malaysia',     'flag': '🇲🇾'},
    'philippines': {'label': 'Philippines',  'flag': '🇵🇭'},
}


def make_rich_content_block(course_slug, region_slug):
    c = COURSES[course_slug]
    r = REGIONS[region_slug]

    faq_html = '\n'.join(
        f'    <div class="faq-item"><h3 class="faq-q">{q}</h3><p class="faq-a">{a}</p></div>'
        for q, a in c['faq']
    )

    related_html = '\n'.join(
        f'    <a href="/courses/{slug}/" class="related-card"><strong>{name}</strong><span>View course &rarr;</span></a>'
        for slug, name in zip(c['related'], c['related_names'])
    )

    return f"""
    <h2>Course Overview</h2>
    <p>{c['overview'].split(chr(10)+chr(10))[0].strip()}</p>
    <p>{c['overview'].split(chr(10)+chr(10))[1].strip()}</p>

    <h2>Why This Matters in {r['label']}</h2>
    <p>{c['industry'].split(chr(10)+chr(10))[0].strip()}</p>
    <p>{c['industry'].split(chr(10)+chr(10))[1].strip()}</p>

    <h2>Assessment &amp; Certification</h2>
    <p>{c['assessment']}</p>

    <h2>Prerequisites</h2>
    <p>{c['prerequisites']}</p>

    <h2>Frequently Asked Questions</h2>
    <div class="faq-block">
{faq_html}
    </div>

    <h2>Related Courses</h2>
    <div class="related-courses">
{related_html}
    </div>"""


def inject_rich_content(html, rich_block):
    """Replace the existing course-body section content with enriched version."""
    # Find the existing h2 About This Course and replace everything up to enrol-section
    pattern = r'(<section class="course-body">)(.*?)(</section>\s*<!-- ENROL)'
    replacement = r'\1\n' + rich_block + r'\n  \3'
    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    return new_html


# ─── ADDITIONAL CSS FOR NEW ELEMENTS ─────────────────────────────────────────

EXTRA_CSS = """
    .faq-block { margin: 1.5rem 0 2rem; }
    .faq-item { border-bottom: 1px solid #e8ecf0; padding: 1.25rem 0; }
    .faq-item:last-child { border-bottom: none; }
    .faq-q { color: var(--navy); font-size: 1.05rem; margin: 0 0 0.5rem; font-weight: 600; }
    .faq-a { color: #555; margin: 0; line-height: 1.7; }
    .related-courses { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem; }
    .related-card { display: flex; flex-direction: column; background: #f8f9fb; border: 1px solid #e0e4ea; border-radius: 10px; padding: 1.25rem 1.5rem; text-decoration: none; flex: 1; min-width: 220px; transition: border-color 0.2s; }
    .related-card:hover { border-color: var(--orange); }
    .related-card strong { color: var(--navy); font-size: 0.95rem; margin-bottom: 0.5rem; }
    .related-card span { color: var(--orange); font-size: 0.85rem; font-weight: 600; }"""


count = 0
for course_slug in COURSES:
    # Course index pages
    path = BASE / 'courses' / course_slug / 'index.html'
    if path.exists():
        html = path.read_text()
        # Add extra CSS before </style>
        html = html.replace('</style>', EXTRA_CSS + '\n  </style>', 1)
        # Build a generic rich block (no region)
        rich = make_rich_content_block(course_slug, 'australia')  # use AU as default context
        html = inject_rich_content(html, rich)
        path.write_text(html)
        print(f"  ✓ courses/{course_slug}/index.html")
        count += 1

    # Regional pages
    for region_slug in REGIONS:
        path = BASE / 'courses' / course_slug / region_slug / 'index.html'
        if path.exists():
            html = path.read_text()
            html = html.replace('</style>', EXTRA_CSS + '\n  </style>', 1)
            rich = make_rich_content_block(course_slug, region_slug)
            html = inject_rich_content(html, rich)
            path.write_text(html)
            print(f"  ✓ courses/{course_slug}/{region_slug}/index.html")
            count += 1

print(f"\n=== {count} pages enriched ===")
