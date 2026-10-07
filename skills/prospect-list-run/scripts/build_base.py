# -*- coding: utf-8 -*-
"""Step 1. Raw prospect CSV -> accounts.json: one company per row, contacts grouped, main contact picked.

Usage: python3 scripts/build_base.py [--config my-client.json] [--workdir ./plr-run] [--source raw.csv]
"""
import collections
import csv
import os
import re

from common import setup, dump_json, norm_domain, rx


def extra(p):
    p.add_argument('--source', help='raw CSV (default: source_csv from the config, relative to the config file)')


cfg, WD, args = setup(__doc__, extra)
src = args.source or os.path.join(cfg['_dir'], cfg['source_csv'])
if not os.path.exists(src):
    raise SystemExit(f'source CSV not found: {src}')

COL = cfg['columns']
P = cfg['personas']
DM_RX, CHAMP_RX, ASSIST = rx(P['dm_rx']), rx(P['champion_rx']), rx(P.get('out_of_matrix_rx'))
# Order matters: check the champion FIRST, because titles such as "Director of Operations"
# match both the decision-maker pattern ("director") and the champion pattern.
RANKS = [(CHAMP_RX, 2), (DM_RX, 1)]


def rank(title):
    t = (title or '').strip()
    if not t:
        return 9
    if ASSIST.search(t):
        return 8
    for r, n in RANKS:
        if r.search(t):
            return n
    return 5


def col(row, key):
    name = COL.get(key)
    return (row.get(name) or '').strip() if name else ''


with open(src, encoding='utf-8-sig') as fh:
    rows = list(csv.DictReader(fh))

acc = collections.OrderedDict()
for r in rows:
    dom = norm_domain(col(r, 'website'))
    if not dom:
        continue
    a = acc.setdefault(dom, {
        'domain': dom,
        'company': col(r, 'company'),
        'country': col(r, 'country'),
        'linkedin_company': col(r, 'company_linkedin'),
        **{k: (r.get(v) or '').strip() for k, v in COL.get('extra', {}).items()},
        'contacts': [],
    })
    title = col(r, 'title')
    a['contacts'].append({
        'name': col(r, 'contact_name') or ' '.join(x for x in (col(r, 'first_name'), col(r, 'last_name')) if x),
        'first': col(r, 'first_name'),
        'last': col(r, 'last_name'),
        'title': title,
        'linkedin': col(r, 'person_linkedin'),
        'email': col(r, 'email'),
        'rank': rank(title),
    })

for a in acc.values():
    a['contacts'].sort(key=lambda c: (c['rank'], 0 if c['email'] else 1))
    a['contacts_n'] = len(a['contacts'])
    top = a['contacts'][0]
    a.update({'dm_name': top['name'], 'dm_title': top['title'], 'dm_linkedin': top['linkedin'],
              'dm_email': top['email'], 'dm_rank': top['rank'],
              'emails_n': sum(1 for c in a['contacts'] if c['email'])})

out = list(acc.values())
dump_json(WD, 'accounts.json', out)
dump_json(WD, 'domains.json', sorted({a['domain'] for a in out}))

print('contacts in the list:', len(rows))
print('unique companies:', len(out))
print('companies with e-mail:', sum(1 for a in out if a['emails_n']))
print('main-contact rank (1 DM, 2 champion, 5 other, 8 assistant, 9 no title):',
      collections.Counter(a['dm_rank'] for a in out).most_common())
print('geo:', collections.Counter(a['country'] for a in out).most_common())
for k in COL.get('extra', {}):
    print(f'{k}:', collections.Counter(a.get(k, '') for a in out).most_common(8))
print('->', os.path.join(WD, 'accounts.json'))
