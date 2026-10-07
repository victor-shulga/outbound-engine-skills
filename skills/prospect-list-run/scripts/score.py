# -*- coding: utf-8 -*-
"""Step 4. Score every account: stop filters -> 8 categories -> score, score-100, band, tier -> scored.csv/json.

Run it twice: once after enrichment, once more after detect_signals_http.py so category 7
(signal) is filled. Every rule comes from the `rubric` block of the config.

Categories: 1 company type, 2 size, 3 geo, 4 deal value (ACV), 5 service/stack fit, 6 rhythm,
7 signal (largest single verified signal, never a sum), 8 decision maker reachable.

Usage: python3 scripts/score.py [--config ...] [--workdir ...]
"""
import collections
import csv
import os

from common import setup, load_json, dump_json, first_rule, cond_ok, to_int, wpath

cfg, WD, args = setup(__doc__)
R = cfg['rubric']
MAXES = {int(k): v for k, v in R['category_max'].items()}
accounts = load_json(WD, 'accounts.json', required=True)
feat = load_json(WD, 'site_features.json', default={})
cms = load_json(WD, 'cms.json', default={})
sizes = load_json(WD, 'company_size.json', default={})
signals = load_json(WD, 'signals.json', default={})
anti = load_json(WD, 'anti_signals.json', default={})
SIG_POINTS = cfg['signals']['points']
GEO = cfg['geo']
FLAG_KEYS = list(cfg['site']['patterns'].keys())
OWN_STACK = cfg['site'].get('own_stack_cms')
CAP_COL = cfg.get('capacity_column')
ACV = R.get('acv') or {}


def context(a, f, c, sz):
    flags = {k for k in FLAG_KEYS if f.get(k)}
    return {
        'flags': flags,
        'has_site': bool(f.get('pages_n')),
        'own_cms': c.get('cms', ''),
        'own_stack': bool(OWN_STACK) and c.get('cms') == OWN_STACK,
        'capacity': to_int(a.get(CAP_COL)) if CAP_COL else -1,
        'volume': f.get('volume_num', 0) or 0,
        'country': a.get('country', ''),
        'size': sz.get('employees') or f.get('team_size_num') or 0,
    }


def ruled(spec, ctx):
    """Category driven by config rules. Returns (points, is_gap)."""
    if spec.get('gap_when') and cond_ok(spec['gap_when'], ctx):
        return 0, True
    r = first_rule(spec.get('rules'), ctx)
    if not r:
        return 0, False
    return r.get('points', 0), bool(r.get('gap'))


def cat_size(ctx):
    n = ctx['size']
    if not n:
        return 0, True
    for lo, hi, pts in R['size_bands']:
        if lo <= n <= hi:
            return pts, False
    return R.get('size_default', 0), False


def cat_acv(a):
    colkey = ACV.get('column')
    v = to_int(a.get(colkey)) if colkey else -1
    if v < 0:
        return 0, True
    for lo, hi, pts in ACV.get('bands', []):
        if lo <= v <= hi:
            return pts, False
    return 0, False


def cat_signal(dom):
    """Largest single verified signal from signals.json (each one carries a URL and a date).
    Unverified hints from site text never score; they stay in reference columns."""
    best, code, ev, url = 0, '', '', ''
    for s in signals.get(dom, []):
        p = SIG_POINTS.get(s.get('code'), 0)
        if p > best:
            best, code, url = p, s.get('code'), s.get('url', '')
            ev = f"{s.get('source', '')} · {s.get('date', '')}".strip(' ·')
    return best, code, ev, url


def cat_dm(a):
    r = a['dm_rank']
    if r in (1, 2):
        return (10 if (a['dm_email'] or a['dm_linkedin']) else 6), False
    if r == 5:
        return 3, False
    return 0, True


def stop_filter(a, ctx, sg):
    x = next((s for s in sg if str(s.get('code', '')).startswith('X')), None)
    if x:
        return f"anti-signal {x['code']}: {x.get('url', '')}"
    for rule in R.get('stop_filters', []):
        if cond_ok(rule, ctx):
            return rule['reason']
    if a['dm_rank'] >= 8:
        return 'only assistants or contacts without a title in the list'
    return None


def tier(ctx):
    if not ctx['size']:
        return '?'
    r = first_rule(R.get('tiers'), ctx)
    return r['tier'] if r else R.get('tier_default', 'C')


ACTION = {'Hot': 'personal outreach from the founder or senior seller',
          'Warm': 'signal-based sequence, interest CTA',
          'Nurture': 'nurture, one touch every 6-8 weeks',
          'Disqualify': 'do not contact'}

rows = []
for a in accounts:
    d = a['domain']
    f = feat.get(d, {'pages_n': 0, 'team_size_num': 0, 'volume_num': 0})
    c, sz = cms.get(d, {}), sizes.get(d, {})
    sg = signals.get(d, [])
    ctx = context(a, f, c, sz)
    stop = stop_filter(a, ctx, sg + anti.get(d, []))

    pts, gap = {}, {}
    pts[1], gap[1] = ruled(R['company_type'], ctx)
    pts[2], gap[2] = cat_size(ctx)
    pts[3], gap[3] = GEO['points'].get(a['country'], GEO.get('default_points', 0)), False
    pts[4], gap[4] = cat_acv(a)
    pts[5], gap[5] = ruled(R['service_fit'], ctx)
    pts[6], gap[6] = ruled(R['rhythm'], ctx)
    pts[7], s_code, s_ev, s_url = cat_signal(d)
    gap[7] = False
    pts[8], gap[8] = cat_dm(a)

    score = sum(pts.values())
    avail = max(sum(MAXES[k] for k in MAXES if not gap[k]), 1)
    score100 = round(score / avail * 100)
    n_gaps = sum(1 for k in gap if gap[k])
    conf = 'H' if n_gaps == 0 else ('M' if n_gaps <= 2 else 'L')
    # Band uses score-100 only when confidence is H or M; at L it uses the raw score,
    # so a lead with two filled fields cannot look perfect.
    base = score100 if conf in ('H', 'M') else score

    if stop:
        band, action = 'Disqualify', stop
    else:
        B, G = R['bands'], R['gate']
        band = 'Hot' if base >= B['Hot'] else 'Warm' if base >= B['Warm'] else 'Nurture' if base >= B['Nurture'] else 'Disqualify'
        gate_ok = pts[5] >= G['stack_min'] and pts[3] >= G['geo_min'] and pts[8] >= G['dm_min']
        if band in ('Hot', 'Warm') and not gate_ok:
            band = {'Hot': 'Warm', 'Warm': 'Nurture'}[band]
        if band == 'Hot' and conf == 'L':
            band = 'Warm'
        action = ACTION[band]

    names = R.get('category_names', {})
    row = {'company': a['company'], 'domain': d, 'country': a['country'], 'tier': tier(ctx),
           'capacity': a.get(CAP_COL, '') if CAP_COL else ''}
    for k in range(1, 9):
        row[f'c{k} {names.get(str(k), "")}'.strip()] = pts[k]
    row.update({
        'score': score, 'score_100': score100, 'band': band, 'action': action, 'confidence': conf,
        'missing': ', '.join(names.get(str(k), str(k)) for k in gap if gap[k]),
        'signal_code': s_code, 'signal_evidence': s_ev, 'signal_url': s_url,
        'signals_total': len([x for x in sg if str(x.get('code', '')).startswith('S')]),
        'dm_name': a['dm_name'], 'dm_title': a['dm_title'], 'dm_email': a['dm_email'],
        'dm_linkedin': a['dm_linkedin'], 'company_linkedin': a['linkedin_company'], 'contacts': a['contacts_n'],
        'site_pages': f.get('pages_n', 0), 'site_flags': ', '.join(sorted(ctx['flags'])),
        'own_site_cms': c.get('cms', ''), 'builders': ', '.join(c.get('builders', [])),
        'site_team_size': f.get('team_size_num', 0),
        'li_employees': sz.get('employees', ''), 'li_industry': ', '.join(sz.get('industries', [])[:2]),
        'li_founded': sz.get('founded', ''), 'li_followers': sz.get('followers', ''),
        '_pts': pts,
    })
    rows.append(row)

ORDER = {'Hot': 3, 'Warm': 2, 'Nurture': 1, 'Disqualify': 0}
rows.sort(key=lambda r: (-ORDER[r['band']], -r['score_100'], -r['score']))
dump_json(WD, 'scored.json', rows)
cols = [k for k in rows[0] if not k.startswith('_')] if rows else []
with open(wpath(WD, 'scored.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore')
    w.writeheader()
    w.writerows(rows)

print('accounts:', len(rows))
print('bands:', collections.Counter(r['band'] for r in rows).most_common())
print('confidence:', collections.Counter(r['confidence'] for r in rows).most_common())
print('tiers:', collections.Counter(r['tier'] for r in rows).most_common())
print('disqualified, reasons:', collections.Counter(r['action'] for r in rows if r['band'] == 'Disqualify').most_common(10))
print('->', wpath(WD, 'scored.csv'))
