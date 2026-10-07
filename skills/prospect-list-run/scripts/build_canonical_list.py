# -*- coding: utf-8 -*-
"""Step 6. Canonical prospect list: one row per contact, 12 fixed blocks, segmentation and ready text.

Writes two CSVs into the work directory:
  <Client>_prospect_list_full.csv     the whole base; disqualified rows keep their reason
  <Client>_outreach_campaign.csv      working sample: passed filters, Hot + Warm, fit gate passed
Blocks 7 (proof of current work) and 9 (website) are the client-specific ones; their content is
driven by capacity_column, site.patterns and site.own_stack_cms in the config.
Message text is assembled from the `text` block of the config: observation -> guess -> fixed offer
paragraph chosen by `angle` -> one question. text_gate = ok only when real evidence sits under
the first line.

Usage: python3 scripts/build_canonical_list.py [--config ...] [--workdir ...]
"""
import collections
import csv
import datetime
import re

from common import setup, load_json, rx, to_int, cond_ok, wpath


class Safe(dict):
    def __missing__(self, k):
        return ''


cfg, WD, args = setup(__doc__)
accounts = {a['domain']: a for a in load_json(WD, 'accounts.json', required=True)}
scored = load_json(WD, 'scored.json', required=True)
signals = load_json(WD, 'signals.json', default={})
sizes = load_json(WD, 'company_size.json', default={})
feat = load_json(WD, 'site_features.json', default={})
cms = load_json(WD, 'cms.json', default={})
hooks = load_json(WD, 'hooks.json', default={})

TODAY = cfg['_today']
S, T, H = cfg['signals'], cfg['text'], cfg.get('hooks', {})
CAP_COL = cfg.get('capacity_column')
UNIT = cfg.get('capacity_unit', ['person', 'people'])
OWN_STACK = cfg['site'].get('own_stack_cms')
FLAG_KEYS = list(cfg['site']['patterns'].keys())
GEO_B = cfg['geo'].get('buckets', {})
P = cfg['personas']
DM, CHAMP, ASSIST = rx(P['dm_rx']), rx(P['champion_rx']), rx(P.get('out_of_matrix_rx'))
PRIORITY = {c: i for i, c in enumerate(S.get('priority', []))}
TARGET_CODE = S['detect'].get('target_role', {}).get('code')
HIRING_CODES = {S['detect'].get(k, {}).get('code') for k in ('target_role', 'adjacent_role', 'any_hiring')} - {None}
ROLE_RX = re.compile(r'\b((?:junior |senior |mid[- ]?level |lead |principal )?'
                     r'(?:qa|quality assurance|test(?: automation)?|software|web|front[- ]?end|back[- ]?end|'
                     r'full[- ]?stack|mobile|ios|android|php|python|java|devops|data|digital|product|project|'
                     r'delivery|account|marketing|sales|ux|ui)[- ]?'
                     r'(?:developer|engineer|tester|analyst|designer|manager|executive|director|specialist|lead))\b', re.I)
NAV_JUNK = re.compile(r'\b(home|menu|skip to content|about us|contact us|our work|services|'
                      r'portfolio|blog|news|careers|privacy|cookie)\b', re.I)


def persona(title):
    t = ' '.join((title or '').split())
    if not t:
        return 'no-title'
    if ASSIST.search(t):
        return 'out-of-matrix'
    if CHAMP.search(t):
        return 'champion'
    if DM.search(t):
        return 'DM'
    return 'out-of-matrix'


def geo_bucket(country):
    for name, lst in GEO_B.items():
        if country in lst:
            return name
    return 'out of focus'


def trim_words(t, n):
    t = ' '.join((t or '').split())
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '...'


def art(word):
    return 'an' if word[:1].lower() in 'aeiou' else 'a'


def plural(n):
    n = max(n, 0)
    return f'{n} {UNIT[0]}' if n == 1 else f'{n} {UNIT[1]}'


def usable_positioning(t):
    """The first line must never stand on a scraped menu. Keep only text that reads as a sentence."""
    t = ' '.join((t or '').split())
    if len(t) < 30 or t.count('/') > 1 or len(NAV_JUNK.findall(t)) >= 2:
        return ''
    m = re.match(r'^(.{40,150}?[.!?])(\s|$)', t)
    if m:
        return m.group(1)
    cut = t[:130].rsplit(' ', 1)[0]
    return cut if len(cut) >= 40 else ''


def own_stack(cm):
    return bool(OWN_STACK) and cm.get('cms') == OWN_STACK


def datapoint(cm, f, hk):
    """A standing fact about them. Priority: what they wrote themselves, then what we observed."""
    if hk.get('service_url'):
        return 'service page', hk['service_url']
    if hk.get('sectors'):
        return 'client sectors', ', '.join(hk['sectors'])
    builders = [b for b in cm.get('builders', []) if b != 'gutenberg']
    if own_stack(cm):
        return 'site stack', f"own site on {cm['cms']}" + (f", built with {', '.join(builders[:2])}" if builders else '')
    if hk.get('claim'):
        return 'own words', hk['claim']
    if f.get('maintenance'):
        return 'maintenance', 'ongoing support sold as a service'
    return '', ''


def fill(template, **kw):
    return (template or '').format_map(Safe(kw)).strip()


def observation(queue, sg, hk, sz, cm, capacity):
    """First line of the message, in the prospect's language. The most specific fact wins."""
    O = T['observation']
    n = sz.get('employees')
    team = f'a team of {n}' if n else 'the team'
    cap_phrase = plural(capacity) if capacity >= 0 else f'your {UNIT[1]}'
    base = dict(team=team, capacity_phrase=cap_phrase, service=H.get('service_name', 'this service'))
    if queue in ('event', 'weak-signal') and sg:
        s0 = sg[0]
        m = ROLE_RX.search(s0.get('quote') or '')
        role = m.group(1).strip() if m else ''
        code = s0['code']
        if role and O.get(code):
            return fill(O[code], role=role, a_role=f'{art(role)} {role}', **base)
        if O.get(f'{code}_norole'):
            return fill(O[f'{code}_norole'], **base)
        if O.get(code) and '{role}' not in O[code] and '{a_role}' not in O[code]:
            return fill(O[code], **base)
        return fill(O.get('default_signal'), signal=S['human'].get(code, code), **base)
    if hk.get('service_url'):
        key = 'service_page_zero_capacity' if capacity == 0 else 'service_page'
        return fill(O.get(key), url=hk['service_url'], **base)
    if hk.get('claim'):
        return fill(O.get('claim'), claim=hk['claim'], **base)
    pos = usable_positioning(hk.get('positioning')).rstrip('.')
    sectors = ', '.join(hk.get('sectors') or [])
    if pos and sectors:
        return fill(O.get('positioning_sectors'), positioning=pos, sectors=sectors, **base)
    if pos:
        return fill(O.get('positioning'), positioning=pos, **base)
    if sectors:
        return fill(O.get('sectors'), sectors=sectors, **base)
    if own_stack(cm):
        builders = [b for b in cm.get('builders', []) if b != 'gutenberg']
        return fill(O.get('own_stack'), cms=cm['cms'], builder_phrase=(f', built with {builders[0]}' if builders else ''), **base)
    return ''


def guess(capacity, hk):
    vol = f" across {hk['portfolio_n']}+ projects" if hk.get('portfolio_n') else ''
    ctx = {'flags': set(), 'has_site': False, 'own_stack': False, 'own_cms': '', 'capacity': capacity,
           'volume': 0, 'country': '', 'size': 0}
    for g in T.get('guess', []):
        rule = {k: v for k, v in g.items() if k != 'text'}
        if cond_ok(rule, ctx):
            return fill(g['text'], volume_phrase=vol, capacity_phrase=plural(capacity) if capacity >= 0 else f'your {UNIT[1]}')
    return ''


def question(p_role, queue):
    Q = T['question']
    if queue == 'event' and Q.get('event'):
        return Q['event']
    return Q.get(p_role) or Q.get('DM', '')


rows = []
for r in scored:
    d = r['domain']
    a = accounts[d]
    pts = {int(k): v for k, v in r['_pts'].items()}
    sz, f, cm, hk = sizes.get(d, {}), feat.get(d, {}), cms.get(d, {}), hooks.get(d, {})
    capacity = to_int(a.get(CAP_COL)) if CAP_COL else -1
    sg = sorted([s for s in signals.get(d, []) if str(s.get('code', '')).startswith('S')],
                key=lambda s: PRIORITY.get(s['code'], 99))
    top = sg[0] if sg else None
    queue = S['queue'].get(top['code'], 'weak-signal') if top else 'datapoint'
    dp_type, dp_detail = datapoint(cm, f, hk)
    sig_date = top['date'] if top else ''
    sig_age = (TODAY - datetime.date.fromisoformat(sig_date)).days if sig_date else ''
    window = S.get('window_days', {}).get(top['code']) if top else None
    fit = pts[1] + pts[5]
    disq = r['band'] == 'Disqualify'

    for c in a['contacts']:
        p_role = persona(c['title'])
        obs = observation(queue, sg, hk, sz, cm, capacity)
        hook_url = top['url'] if top else (f'https://{d}' if dp_detail else '')
        hook_date = sig_date if top else (TODAY.isoformat() if dp_detail else '')
        gate, reason = 'ok', ''
        if not obs or not hook_url:
            gate, reason = 'review', 'no evidence under the first line'
        elif p_role in ('out-of-matrix', 'no-title'):
            gate, reason = 'review', 'title outside the persona matrix'
        elif disq:
            gate, reason = 'review', 'row removed by a stop filter'
        elif window and sig_age != '' and sig_age > window:
            gate, reason = 'review', f'signal older than its {window}-day window'
        tier_c = {'A': 'A', 'A-': 'A', 'B': 'B', 'C': 'C', '?': 'enrich'}.get(r['tier'], r['tier'])
        camp = 'do not launch' if disq else ('out of matrix' if p_role in ('out-of-matrix', 'no-title')
                                             else f'{queue} · {p_role} · {tier_c}')
        flags = [k for k in FLAG_KEYS if f.get(k)]
        rows.append({
            # 1. Company
            'row_id': 0, 'company_name_raw': a['company'], 'company_name_clean': a['company'].strip(),
            'domain': d, 'country': r['country'], 'geo_bucket': geo_bucket(r['country']),
            'city': hk.get('city', ''), 'industry': ', '.join(sz.get('industries', [])[:2]),
            # 2. Stop filters
            'filter_geo': 'yes' if pts[3] >= cfg['rubric']['gate']['geo_min'] else 'no',
            'filter_size': 'yes' if pts[2] > 0 else 'enrich',
            'filter_anti_icp': 'no' if disq else 'yes',
            'filter_result': 'removed' if disq else 'passed',
            # 3. Headcount
            'emp_enriched': sz.get('employees', ''), 'emp_final': sz.get('employees', '') or f.get('team_size_num', '') or '',
            'tier': r['tier'],
            # 4. Fit (company type + service fit, 30 points, gate 20) and the 100-point lead score
            'fit_icp': pts[1], 'fit_services': pts[5], 'fit_score': fit, 'fit_gate': 'YES' if fit >= 20 else 'NO',
            'lead_score': r['score'], 'lead_score_100': r['score_100'], 'band': r['band'],
            'confidence': r['confidence'], 'missing_fields': r['missing'],
            # 5. Signal
            'signal_type': top['code'] if top else '', 'signal_name': S['human'].get(top['code'], '') if top else '',
            'signal_score': pts[7], 'signal_route': queue,
            'signal_evidence_url': top['url'] if top else '', 'signal_date': sig_date, 'signal_age_days': sig_age,
            'signal_window_days': window or '',
            'signal_summary': trim_words(top.get('quote'), 200) if top else '',
            'signal_2_type': sg[1]['code'] if len(sg) > 1 else '', 'signal_2_url': sg[1]['url'] if len(sg) > 1 else '',
            'signal_3_type': sg[2]['code'] if len(sg) > 2 else '',
            # 6. Data point
            'datapoint_type': dp_type, 'datapoint_detail': dp_detail,
            # 7. Proof of current work (client-specific)
            'capacity_in_house': a.get(CAP_COL, '') if CAP_COL else '',
            'jobs_open': 'yes' if top and top['code'] in HIRING_CODES else 'no',
            'jobs_role': S['human'].get(top['code'], '') if top and top['code'] in HIRING_CODES else '',
            'jobs_source': top['url'] if top and top['code'] in HIRING_CODES else '',
            # 8. Source control
            'match_method': 'client list + site' + (' + LinkedIn' if sz else ''),
            'channel_route': 'e-mail + LinkedIn' if c['email'] else 'LinkedIn',
            'exclusion_reason': r['action'] if disq else '',
            'source_track': cfg.get('source_track', ''),
            # 9. Website (client-specific)
            'site_status': 'responded' if cm.get('ok') or f.get('pages_n') else ('not checked' if not cm else 'no response'),
            'site_cms': cm.get('cms', ''), 'site_builders': ', '.join(cm.get('builders', [])),
            'site_own_stack': ('yes' if own_stack(cm) else 'no') if OWN_STACK else '',
            'site_pages': f.get('pages_n', 0), 'site_flags': ', '.join(flags),
            # 10. Contact
            'person_first_name': c['first'], 'person_last_name': c['last'],
            'person_title': ' '.join((c['title'] or '').split()), 'person_linkedin': c['linkedin'],
            'person_email': c['email'], 'email_status': 'present' if c['email'] else 'missing',
            'company_linkedin': a['linkedin_company'],
            # 11. Text
            'language': cfg.get('language', 'English'), 'angle': T['angle'].get(queue, ''),
            'observation': obs, 'guess': guess(capacity, hk), 'question': question(p_role, queue),
            'opener_style': T.get('opener', {}).get(queue, ''),
            'text_gate': gate, 'text_gate_reason': reason, 'hook_source': hook_url, 'hook_date': hook_date,
            # 12. Segmentation
            'persona_role': p_role, 'campaign': camp, 'contacts_at_company': a['contacts_n'],
            'persona_gap': '' if any(persona(x['title']) == 'champion' for x in a['contacts']) else 'no champion',
        })

BAND = {'Hot': 3, 'Warm': 2, 'Nurture': 1, 'Disqualify': 0}
QORD = {'event': 0, 'weak-signal': 1, 'datapoint': 2}
rows.sort(key=lambda x: (-BAND[x['band']], QORD.get(x['signal_route'], 9), -x['lead_score_100'],
                         x['company_name_clean'], 0 if x['persona_role'] == 'DM' else 1))
for i, x in enumerate(rows, 1):
    x['row_id'] = i

if not rows:
    raise SystemExit('no rows: check accounts.json and scored.json')
cols = list(rows[0].keys())
full = wpath(WD, f"{cfg['_slug']}_prospect_list_full.csv")
work = [x for x in rows if x['filter_result'] == 'passed' and x['band'] in ('Hot', 'Warm') and x['fit_gate'] == 'YES']
camp_path = wpath(WD, f"{cfg['_slug']}_outreach_campaign.csv")
for path, data in ((full, rows), (camp_path, work)):
    with open(path, 'w', newline='', encoding='utf-8-sig') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(data)

print('columns:', len(cols))
print('full base:', len(rows), 'rows |', len({x['domain'] for x in rows}), 'companies')
print('working sample:', len(work), 'rows |', len({x['domain'] for x in work}), 'companies')
print('campaigns (working sample):')
for k, v in collections.Counter(x['campaign'] for x in work).most_common():
    ok = sum(1 for x in work if x['campaign'] == k and x['text_gate'] == 'ok')
    print(f'  {k:<32} {v:>3} rows | text ok: {ok}')
print('queues:', collections.Counter(x['signal_route'] for x in work).most_common())
print('personas:', collections.Counter(x['persona_role'] for x in work).most_common())
print('text_gate (all rows):', collections.Counter(x['text_gate'] for x in rows).most_common())
print('->', full)
print('->', camp_path)
