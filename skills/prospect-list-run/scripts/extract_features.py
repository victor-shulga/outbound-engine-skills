# -*- coding: utf-8 -*-
"""Step 3b. Turn crawled page text into the feature flags the rubric uses -> site_features.json.

Flags come from site.patterns in the config (one regex per flag). On top of them the script pulls
a price hint, a team-size hint and a portfolio-volume number from the text.

Usage: python3 scripts/extract_features.py [--config ...] [--workdir ...]
"""
import collections
import re

from common import setup, load_json, dump_json, norm_domain, rx

cfg, WD, args = setup(__doc__)
pages = load_json(WD, 'site_pages.json', default=[])
accounts = load_json(WD, 'accounts.json', required=True)
if not pages:
    print('no site_pages.json (or it is empty): every account gets has_site = false')

by_dom = collections.defaultdict(list)
for p in pages:
    by_dom[norm_domain(p['url'])].append(p)

PAT = {k: rx(v) for k, v in cfg['site']['patterns'].items()}
PRICE = re.compile(r'(from\s?[£$€]\s?[\d,]{3,7}|[£$€]\s?[\d,]{3,7}\s?(\+|per project|per month|/month|pm\b))', re.I)
TEAMSIZE = re.compile(r'\b(team of (\d{1,3})|(\d{1,3}) (\+ )?(strong )?(person|people|specialists?|experts?|'
                      r'engineers?|developers?)|we are a team of (\d{1,3}))\b', re.I)
CASECOUNT = re.compile(r'\b(\d{2,4})\s?\+?\s?(websites?|projects?|clients?|brands?|apps?|products?)\s?'
                       r'(built|delivered|launched|created|designed|served|helped)?', re.I)


def snippet(t, m, w=120):
    lo, hi = max(0, m.start() - w), min(len(t), m.end() + w)
    return ' '.join(t[lo:hi].split())


out = {}
for a in accounts:
    d = a['domain']
    ps = by_dom.get(d, [])
    blob = '\n'.join(p['text'] for p in ps)
    f = {'pages_n': len(ps), 'chars': len(blob)}
    for k, r in PAT.items():
        f[k] = bool(r.search(blob))
    m = PRICE.search(blob)
    f['price_hint'] = snippet(blob, m) if m else ''
    m = TEAMSIZE.search(blob)
    f['team_size_hint'] = snippet(blob, m) if m else ''
    nums = [int(x) for x in re.findall(r'\d{1,3}', m.group(0))] if m else []
    f['team_size_num'] = max(nums) if nums else 0
    m = CASECOUNT.search(blob)
    f['volume_hint'] = snippet(blob, m) if m else ''
    try:
        f['volume_num'] = int(m.group(1).replace(',', '')) if m else 0
    except ValueError:
        f['volume_num'] = 0
    out[d] = f

dump_json(WD, 'site_features.json', out)
got = sum(1 for v in out.values() if v['pages_n'])
print('accounts:', len(out), '| with pages:', got, '| without:', len(out) - got)
for k in PAT:
    print(f'  {k}: {sum(1 for v in out.values() if v[k])}')
print('  price found:', sum(1 for v in out.values() if v['price_hint']))
print('  team size found:', sum(1 for v in out.values() if v['team_size_num']))
