# -*- coding: utf-8 -*-
"""Step 5. Live signals with evidence and date, checked on the company's OWN domain -> signals.json + anti_signals.json.

Two sources, both tied to the domain by construction:
  1. pages already crawled in site_pages.json (careers / partner URLs),
  2. direct HTTP requests to the paths in signals.detect.paths.
What it detects (codes and regexes come from signals.detect in the config):
  target_role   a vacancy for the role your client replaces or supports (strongest)
  adjacent_role hiring around that role, but not the role itself
  any_hiring    any open vacancy
  partner_seek  the company says it is looking for an outside partner
  partner_offer_anti  the company SELLS the same service itself: an anti-signal (competitor), not a lead
Anti-signals are checked on EVERY account, disqualified ones included, and live in their own file.
No API key, plain HTTP from your own IP.

Usage: python3 scripts/detect_signals_http.py [--config ...] [--workdir ...] [--parallel 12]
"""
import collections
import re
import ssl
import threading
import urllib.request

from common import setup, load_json, dump_json, norm_domain, rx, to_int


def extra(p):
    p.add_argument('--parallel', type=int, default=12)


cfg, WD, args = setup(__doc__, extra)
D = cfg['signals']['detect']
scored = load_json(WD, 'scored.json', required=True)
pages = load_json(WD, 'site_pages.json', default=[])
print('accounts in this pass:', len(scored), flush=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'

TARGET = D.get('target_role', {})
ADJ = D.get('adjacent_role', {})
ANY = D.get('any_hiring', {})
SEEK = D.get('partner_seek', {})
OFFER = D.get('partner_offer_anti', {})
TARGET_RX, ADJ_RX, SEEK_RX, OFFER_RX = rx(TARGET.get('rx')), rx(ADJ.get('rx')), rx(SEEK.get('rx')), rx(OFFER.get('rx'))
ANY_RX = rx(ANY.get('rx') or (
    r"(we(?:'| a)re (?:currently )?(?:hiring|recruiting|looking for)|"
    r"we are (?:currently )?(?:hiring|recruiting|seeking|looking for) an?|"
    r"current vacanc(?:y|ies)|open (?:role|position|vacanc)\w*\s*:|"
    r"apply now|apply for this (?:role|job|position)|offres d'emploi|stellenangebot|wir suchen)"))
NO_VACANCY = re.compile(r"(no (?:current )?(?:job )?(?:vacanc\w+|openings?|opportunities|roles|positions)|"
                        r"(?:do not|don't|dont) (?:currently )?have any (?:job )?(?:openings?|vacanc\w+|roles)|"
                        r"not (?:currently )?(?:hiring|recruiting)|aren'?t (?:currently )?(?:hiring|recruiting)|"
                        r"there are (?:currently )?no)", re.I)
# A vacancy, not a team member's job title: hiring words must sit nearby.
HIRE_CTX = re.compile(r'\b(appl(?:y|ication)|salary|full[- ]time|part[- ]time|permanent|'
                      r'we (?:are )?(?:looking for|seeking|need)|the role|job description|'
                      r'responsibilities|requirements|send (?:us )?your cv|hybrid|remote|'
                      r'competitive|benefits|closing date|contract)\b', re.I)
TESTIMONIAL = re.compile(r'\b(pleasure working with|our account manager|they communicate|'
                         r'highly recommend|great to work with|client testimonial)\b', re.I)
# A staff bio written in the first person, not a vacancy.
BIO = re.compile(r"\b(I've|I have|I enjoy|I hold|my career|I joined|I started|I began|I lead|led me to|I now|I work)\b")
YEAR = re.compile(r'\b(?:19|20)\d{2}\b')
TODAY = cfg['_today']
CUR_YEARS = {str(TODAY.year), str(TODAY.year - 1)}
TAGS = re.compile(r'<script[^>]*>.*?</script>|<style[^>]*>.*?</style>|<[^>]+>', re.S)
HIRING_URL = rx(D.get('hiring_url_rx'))
PARTNER_URL = rx(D.get('partner_url_rx'))
PARTNER_PATH = re.compile(r'partner|white-label|agenc', re.I)


def text_of(html):
    return ' '.join(TAGS.sub(' ', html).split())


def fetch(url, timeout=12):
    r = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html'})
    with urllib.request.urlopen(r, timeout=timeout, context=ctx) as f:
        if f.status >= 400:
            return ''
        return f.read(300000).decode('utf-8', 'ignore')


crawl = collections.defaultdict(list)
for p in pages:
    crawl[norm_domain(p['url'])].append(p)

res = collections.defaultdict(list)
lock, wl = threading.Semaphore(args.parallel), threading.Lock()


def add(dom, code, url, quote):
    if not code:
        return
    with wl:
        if any(s['code'] == code for s in res[dom]):
            return
        res[dom].append({'code': code, 'source': 'company site', 'url': url,
                         'date': TODAY.isoformat(), 'quote': quote[:240]})


def quote_of(t, m):
    return t[max(0, m.start() - 110):m.end() + 110]


def role_hit(t, r):
    """Count a role match only with hiring language nearby, not inside a testimonial or a bio,
    and not on a page whose nearby dates are all older than last year (stale vacancy)."""
    for m in r.finditer(t):
        near = t[max(0, m.start() - 400):min(len(t), m.end() + 400)]
        if TESTIMONIAL.search(near) or BIO.search(near):
            continue
        years = set(YEAR.findall(near))
        if years and not (years & CUR_YEARS):
            continue
        if HIRE_CTX.search(near):
            return m
    return None


def scan_hiring(d, url, t):
    if NO_VACANCY.search(t):
        return
    m = role_hit(t, TARGET_RX)
    if m:
        add(d, TARGET.get('code'), url, quote_of(t, m))
        return
    m = role_hit(t, ADJ_RX)
    if m:
        add(d, ADJ.get('code'), url, quote_of(t, m))
        return
    m = ANY_RX.search(t)
    if m:
        add(d, ANY.get('code'), url, quote_of(t, m))


def scan_partner(d, url, t):
    # Direction matters: a partner page almost always means the company OFFERS the service.
    m = SEEK_RX.search(t)
    if m:
        add(d, SEEK.get('code'), url, quote_of(t, m))
        return
    m = OFFER_RX.search(t)
    if m:
        add(d, OFFER.get('code'), url, quote_of(t, m))


def worker(r):
    with lock:
        d = r['domain']
        for p in crawl.get(d, []):
            if HIRING_URL.search(p['url']):
                scan_hiring(d, p['url'], p['text'])
            if PARTNER_URL.search(p['url']):
                scan_partner(d, p['url'], p['text'])
        for path in D.get('paths', []):
            if any(s['code'] == TARGET.get('code') for s in res[d]):
                break
            url = f'https://{d}{path}'
            try:
                html = fetch(url)
            except Exception:
                continue
            t = text_of(html) if html else ''
            if len(t) < 200:
                continue
            if PARTNER_PATH.search(path):
                scan_partner(d, url, t)
            else:
                scan_hiring(d, url, t)


ths = [threading.Thread(target=worker, args=(r,)) for r in scored]
for t in ths:
    t.start()
for t in ths:
    t.join()

# The adjacent-role signal only counts when in-house capacity is at or below the configured max
# (they hire around the role, and do not have the role itself).
cap_col, cap_max = cfg.get('capacity_column'), ADJ.get('requires_capacity_max')
cap = {r['domain']: to_int(r.get('capacity')) for r in scored}
clean = {}
for d, lst in res.items():
    keep = [s for s in lst if s['code'].startswith('S') and not (
        s['code'] == ADJ.get('code') and cap_col and cap_max is not None and not (0 <= cap.get(d, -1) <= cap_max))]
    if keep:
        clean[d] = keep
anti = {d: [s for s in lst if s['code'].startswith('X')] for d, lst in res.items()}
anti = {d: v for d, v in anti.items() if v}

dump_json(WD, 'signals.json', clean)
dump_json(WD, 'anti_signals.json', anti)
print('anti-signals (stop filter):', len(anti))
print('domains with signals:', len(clean))
print('codes:', collections.Counter(s['code'] for v in clean.values() for s in v).most_common())
print('NEXT: open signals.json and read at least 10 quotes before you trust the run.')
