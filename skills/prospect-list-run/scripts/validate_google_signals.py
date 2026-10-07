# -*- coding: utf-8 -*-
"""Optional gate for signals found by searching the company NAME (Google or any search API).

Name search returns other firms with similar names. A result is kept only when the company's
domain appears in its URL or text, or when the exact company name (2+ words or 8+ characters)
appears as a phrase. Entries whose source is not "Google" pass through untouched.
Rewrites signals.json in place and prints what was dropped.

Usage: python3 scripts/validate_google_signals.py [--config ...] [--workdir ...]
"""
import collections
import re

from common import setup, load_json, dump_json

cfg, WD, args = setup(__doc__)
signals = load_json(WD, 'signals.json', required=True)
accounts = {a['domain']: a['company'] for a in load_json(WD, 'accounts.json', required=True)}

kept, dropped, examples = {}, collections.Counter(), []
for dom, lst in signals.items():
    keep = []
    for s in lst:
        if s.get('source') != 'Google':
            keep.append(s)
            continue
        blob = f"{s.get('url', '')} {s.get('title', '')} {s.get('quote', '')}".lower()
        name = (accounts.get(dom) or '').strip().lower()
        ok = dom in blob
        if not ok and name and (' ' in name or len(name) >= 8):
            ok = re.search(r'\b' + re.escape(name) + r'\b', blob) is not None
        if ok:
            keep.append(s)
        else:
            dropped[s['code']] += 1
            if len(examples) < 8:
                examples.append((dom, s['code'], s.get('title', '')[:70]))
    if keep:
        kept[dom] = keep

dump_json(WD, 'signals.json', kept)
before = sum(len(v) for v in signals.values())
after = sum(len(v) for v in kept.values())
print(f'signals before: {before} | kept: {after} | dropped: {before - after}')
print('dropped by code:', dropped.most_common())
print('examples of dropped (matched another company):')
for d, c, t in examples:
    print(f'  {d} [{c}] {t}')
