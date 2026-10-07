# -*- coding: utf-8 -*-
"""Step 3e. Map LinkedIn company records back to domains -> company_size.json.

Usage: python3 scripts/merge_linkedin.py [--config ...] [--workdir ...]
"""
import collections
import re

from common import setup, load_json, dump_json

cfg, WD, args = setup(__doc__)
accounts = load_json(WD, 'accounts.json', required=True)
raw = load_json(WD, 'linkedin_raw.json', required=True)


def key(u):
    return re.sub(r'/+$', '', (u or '').lower().replace('http://', 'https://').replace('www.', ''))


def names(lst):
    return [i.get('name', '') if isinstance(i, dict) else str(i) for i in (lst or [])]


by_li = {}
for x in raw:
    k = key(x.get('originalQuery', {}).get('search', '') or x.get('linkedinUrl', ''))
    if k and x.get('name'):
        by_li[k] = x

out = {}
for a in accounts:
    x = by_li.get(key(a['linkedin_company']))
    if not x:
        continue
    rng = x.get('employeeCountRange') or {}
    fo = x.get('foundedOn')
    out[a['domain']] = {
        'li_name': x.get('name', ''),
        'employees': x.get('employeeCount') or 0,
        'range_start': rng.get('start') or 0,
        'range_end': rng.get('end') or 0,
        'followers': x.get('followerCount') or 0,
        'founded': fo.get('year') if isinstance(fo, dict) else fo,
        'industries': names(x.get('industries')),
        'specialities': names(x.get('specialities'))[:12],
        'tagline': (x.get('tagline') or '')[:200],
        'jobs_url': x.get('jobSearchUrl', ''),
    }

dump_json(WD, 'company_size.json', out)
sizes = [v['employees'] for v in out.values() if v['employees']]
bands = collections.Counter('1-10' if n <= 10 else '11-50' if n <= 50 else '51-200' if n <= 200 else '200+' for n in sizes)
print('accounts with LinkedIn data:', len(out), 'of', len(accounts))
print('size known:', len(sizes), '| bands:', bands.most_common())
print('industries:', collections.Counter(i for v in out.values() for i in v['industries']).most_common(8))
