# -*- coding: utf-8 -*-
"""Step 3a (optional). Direct HTTP check of what each company's OWN site is built on -> cms.json.

A text crawl cannot see this; it needs the raw HTML. Run it when the client's offer depends on
the prospect's stack (set site.own_stack_cms in the config, e.g. "wordpress", "webflow",
"shopify"). Free: plain HTTP from your own IP, no API key.

Usage: python3 scripts/detect_cms.py [--config ...] [--workdir ...] [--parallel 16]
"""
import collections
import re
import ssl
import threading
import urllib.request

from common import setup, load_json, dump_json


def extra(p):
    p.add_argument('--parallel', type=int, default=16)


cfg, WD, args = setup(__doc__, extra)
doms = load_json(WD, 'domains.json', required=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'

WPSIG = re.compile(r'wp-content|wp-includes|wp-json', re.I)
GEN = re.compile(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']{0,120})', re.I)
OTHER = {
    'webflow': re.compile(r'webflow\.(com|io)|data-wf-page', re.I),
    'wix': re.compile(r'wix\.com|wixstatic', re.I),
    'squarespace': re.compile(r'squarespace', re.I),
    'shopify': re.compile(r'cdn\.shopify|shopify\.com', re.I),
    'framer': re.compile(r'framer\.(com|website)|framerusercontent', re.I),
    'hubspot': re.compile(r'hs-scripts|hubspot', re.I),
    'drupal': re.compile(r'/sites/default/files|Drupal\.settings', re.I),
    'craft': re.compile(r'craftcms', re.I),
    'nextjs': re.compile(r'/_next/static|__NEXT_DATA__', re.I),
}
BUILDER = {
    'elementor': re.compile(r'elementor', re.I),
    'divi': re.compile(r'et_pb_|/themes/divi|et-core|elegantthemes', re.I),
    'wpbakery': re.compile(r'js_composer|wpb_', re.I),
    'bricks': re.compile(r'brxe-|bricks/', re.I),
    'beaver': re.compile(r'fl-builder', re.I),
    'oxygen': re.compile(r'oxy-|oxygen-', re.I),
    'gutenberg': re.compile(r'wp-block-', re.I),
    'acf': re.compile(r'acf/|advanced-custom-fields', re.I),
}

res, lock, wlock = {}, threading.Semaphore(args.parallel), threading.Lock()


def fetch(url, timeout=15):
    r = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html'})
    with urllib.request.urlopen(r, timeout=timeout, context=ctx) as f:
        return f.read(400000).decode('utf-8', 'ignore')


def worker(d):
    with lock:
        out = {'ok': False, 'cms': '', 'wp': False, 'generator': '', 'builders': [], 'others': []}
        html = ''
        for u in (f'https://{d}', f'https://www.{d}', f'http://{d}'):
            try:
                html = fetch(u)
                out['ok'] = True
                break
            except Exception:
                continue
        if html:
            out['wp'] = bool(WPSIG.search(html))
            m = GEN.search(html)
            out['generator'] = m.group(1) if m else ''
            out['builders'] = [k for k, r in BUILDER.items() if r.search(html)] if out['wp'] else []
            out['others'] = [k for k, r in OTHER.items() if r.search(html)]
            if out['wp'] or 'wordpress' in out['generator'].lower():
                out['cms'] = 'wordpress'
            elif out['others']:
                out['cms'] = out['others'][0]
        if out['ok'] and not out['cms']:
            try:
                j = fetch(f'https://{d}/wp-json/', timeout=10)
                if '"namespace"' in j or 'wp/v2' in j:
                    out['wp'], out['cms'] = True, 'wordpress'
            except Exception:
                pass
        with wlock:
            res[d] = out


ths = [threading.Thread(target=worker, args=(d,)) for d in doms]
for t in ths:
    t.start()
for t in ths:
    t.join()

dump_json(WD, 'cms.json', res)
print('checked:', len(res), '| responded:', sum(1 for v in res.values() if v['ok']))
print('CMS:', collections.Counter(v['cms'] or '?' for v in res.values()).most_common())
print('page builders:', collections.Counter(b for v in res.values() for b in v['builders']).most_common())
target = cfg['site'].get('own_stack_cms')
if target:
    print(f'own site on {target}:', sum(1 for v in res.values() if v['cms'] == target))
