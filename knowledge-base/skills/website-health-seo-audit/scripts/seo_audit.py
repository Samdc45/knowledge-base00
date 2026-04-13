#!/usr/bin/env python3
"""
seo_audit.py — Audit all HTML pages in a local repo for SEO quality signals.

Usage:
    python seo_audit.py <repo_dir>

Outputs a table of: file, title length, description length, word count,
canonical URL, robots meta, og:image, twitter:card.
"""
import sys
import os
from pathlib import Path
from bs4 import BeautifulSoup

def get_text_word_count(soup):
    for tag in soup(['script', 'style', 'nav', 'footer', 'head']):
        tag.decompose()
    return len(soup.get_text(separator=' ').split())

def audit_file(path):
    soup = BeautifulSoup(path.read_text(errors='ignore'), 'html.parser')
    title = soup.find('title')
    desc  = soup.find('meta', attrs={'name': 'description'})
    if desc and (not hasattr(desc, 'attrs') or desc.attrs is None): desc = None
    canon = soup.find('link', rel='canonical')
    robots = soup.find('meta', attrs={'name': 'robots'})
    og_img = soup.find('meta', property='og:image')
    tw_card = soup.find('meta', attrs={'name': 'twitter:card'})
    schema = bool(soup.find('script', type='application/ld+json'))
    wc = get_text_word_count(soup)

    def attr(tag, key):
        if not tag: return ''
        a = getattr(tag, 'attrs', None)
        return (a or {}).get(key, '') or ''

    t_len = len(title.string.strip()) if title and title.string else 0
    d_len = len(attr(desc, 'content').strip())
    c_url = attr(canon, 'href') or 'MISSING'
    r_val = attr(robots, 'content') or 'MISSING'
    og    = 'OK' if og_img else 'MISSING'
    tw    = 'OK' if tw_card else 'MISSING'
    sc    = 'OK' if schema else 'MISSING'

    issues = []
    if t_len == 0:       issues.append('NO_TITLE')
    elif t_len > 60:     issues.append(f'TITLE_LONG({t_len})')
    if d_len == 0:       issues.append('NO_DESC')
    elif d_len > 160:    issues.append(f'DESC_LONG({d_len})')
    elif d_len < 100:    issues.append(f'DESC_SHORT({d_len})')
    if wc < 400:         issues.append(f'THIN({wc}w)')
    if c_url == 'MISSING': issues.append('NO_CANONICAL')
    if r_val == 'MISSING': issues.append('NO_ROBOTS')
    if og == 'MISSING':  issues.append('NO_OG_IMAGE')
    if sc == 'MISSING':  issues.append('NO_SCHEMA')

    return {
        'file': str(path),
        'title_len': t_len,
        'desc_len': d_len,
        'words': wc,
        'canonical': c_url,
        'robots': r_val,
        'og_image': og,
        'twitter': tw,
        'schema': sc,
        'issues': ', '.join(issues) if issues else 'OK'
    }

def main():
    repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    pages = sorted(repo.rglob('*.html'))
    if not pages:
        print(f'No HTML files found in {repo}')
        return

    results = [audit_file(p) for p in pages]
    issues_only = [r for r in results if r['issues'] != 'OK']

    print(f"\n{'='*80}")
    print(f"SEO AUDIT — {repo} — {len(pages)} pages, {len(issues_only)} with issues")
    print(f"{'='*80}")
    print(f"{'FILE':<55} {'T':>3} {'D':>3} {'W':>5}  ISSUES")
    print('-'*80)
    for r in results:
        short = r['file'].replace(str(repo)+'/', '')
        print(f"{short:<55} {r['title_len']:>3} {r['desc_len']:>3} {r['words']:>5}  {r['issues']}")

    print(f"\n{'='*80}")
    print(f"SUMMARY: {len(issues_only)}/{len(pages)} pages have issues")
    thin = [r for r in results if 'THIN' in r['issues']]
    if thin:
        print(f"  Thin content (<400w): {len(thin)} pages")
    no_canon = [r for r in results if 'NO_CANONICAL' in r['issues']]
    if no_canon:
        print(f"  Missing canonical: {len(no_canon)} pages")

if __name__ == '__main__':
    main()
