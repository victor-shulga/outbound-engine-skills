# -*- coding: utf-8 -*-
"""Step 3c. Pull a UNIQUE fact about each company for the first line of the message -> hooks.json.

A template with a variable ("your site runs on X, your team is N people") is not personalisation.
This step takes what the company wrote about itself: the page where it sells the relevant service,
its own sentence about it, founding year, city, awards/partner badges, portfolio size, client
sectors and the positioning line from the homepage. Patterns live in the `hooks` block of the config.

Usage: python3 scripts/extract_hooks.py [--config ...] [--workdir ...]
"""
import collections
import re

from common import setup, load_json, dump_json, norm_domain, rx

cfg, WD, args = setup(__doc__)
pages = load_json(WD, 'site_pages.json', default=[])
accounts = load_json(WD, 'accounts.json', required=True)
H = cfg.get('hooks', {})

by = collections.defaultdict(list)
for p in pages:
    by[norm_domain(p['url'])].append(p)

SERVICE_URL = rx(H.get('service_url_rx'))
CLAIM = rx(H.get('claim_rx'))
CITY = re.compile(H['city_rx']) if H.get('city_rx') else None   # case-sensitive: city names are capitalised
SECTORS = rx(H.get('sectors_rx'))
FOUNDED = re.compile(r'\b(?:founded|established|since|started)\s+(?:in\s+)?(19[7-9]\d|20[0-3]\d)\b', re.I)
AWARD = re.compile(r'\b(b corp|b-corp|award[- ]winning|multi-award|iso \d{4,5}|google partner|'
                   r'aws (?:advanced |select )?partner|microsoft partner|shopify partner|hubspot partner|'
                   r'clutch top|living wage employer|carbon neutral|net zero)\b', re.I)
PORTFOLIO_N = re.compile(r'\b(\d{2,4})\s?\+?\s?(?:websites?|projects?|clients?|brands?|apps?|products?)\b', re.I)
JOBS_URL = re.compile(r'career|job|vacanc', re.I)


def clean(t, n=200):
    return ' '.join((t or '').split())[:n]


def first_sentence(t):
    t = ' '.join((t or '').split())
    m = re.search(r'^(.{40,180}?[.!?])\s', t)
    return m.group(1) if m else t[:160]


out = {}
for a in accounts:
    d = a['domain']
    ps = by.get(d, [])
    blob = '\n'.join(p['text'] for p in ps)
    h = {'service_url': '', 'claim': '', 'founded': '', 'city': '', 'awards': [],
         'portfolio_n': 0, 'sectors': [], 'positioning': ''}
    for p in ps:
        if SERVICE_URL.search(p['url']) and not JOBS_URL.search(p['url']):
            h['service_url'] = p['url']
            m = CLAIM.search(p['text'])
            if m:
                h['claim'] = clean(m.group(0), 180)
            break
    if not h['claim']:
        m = CLAIM.search(blob)
        if m:
            h['claim'] = clean(m.group(0), 180)
    m = FOUNDED.search(blob)
    h['founded'] = m.group(1) if m else ''
    if CITY:
        m = CITY.search(blob)
        h['city'] = m.group(1) if m else ''
    h['awards'] = sorted({m.group(0).lower() for m in AWARD.finditer(blob)})[:3]
    nums = [int(x) for x in PORTFOLIO_N.findall(blob)]
    h['portfolio_n'] = max(nums) if nums else 0
    h['sectors'] = sorted({m.group(0).lower() for m in SECTORS.finditer(blob)})[:3]
    home = next((p for p in ps if norm_domain(p['url']) == d and p['url'].rstrip('/').count('/') <= 2), None)
    if home:
        h['positioning'] = first_sentence(home['text'])
    out[d] = h

dump_json(WD, 'hooks.json', out)
print('accounts:', len(out))
for k, label in (('service_url', 'dedicated service page'), ('claim', 'own sentence about the service'),
                 ('founded', 'founding year'), ('city', 'city'), ('awards', 'awards/partner badges'),
                 ('portfolio_n', 'portfolio size'), ('sectors', 'client sectors'), ('positioning', 'homepage positioning')):
    print(f'  {label}:', sum(1 for v in out.values() if v[k]))
print('  UNIQUE claims:', len({v['claim'] for v in out.values() if v['claim']}))
