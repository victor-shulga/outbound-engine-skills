# -*- coding: utf-8 -*-
"""Step 2. Crawl company websites through Apify (website-content-crawler) -> site_pages.json.

Only pages whose URL matches site.glob_paths in the config are kept (services, work, team,
careers, pricing...). Needs APIFY_TOKEN in the environment. Check your Apify limits first:
an exhausted monthly limit returns 403 on every actor and looks like a broken script.

Usage: python3 scripts/run_sites.py [--config ...] [--workdir ...] [--batch 32] [--parallel 4]
"""
import json
import threading
import time
import urllib.request

from common import setup, load_json, dump_json, apify_token


def extra(p):
    p.add_argument('--batch', type=int, default=32, help='domains per actor run')
    p.add_argument('--parallel', type=int, default=4, help='actor runs at the same time')


cfg, WD, args = setup(__doc__, extra)
TOKEN = apify_token()
ACT = 'apify~website-content-crawler'


def api(method, path, payload=None):
    url = f'https://api.apify.com/v2/{path}'
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'})
    return json.load(urllib.request.urlopen(req, timeout=300))


items = load_json(WD, 'domains.json', required=True)
print('sites:', len(items), flush=True)
GLOBS = [f'**/{p}*' for p in cfg['site']['glob_paths']]
batches = [items[i:i + args.batch] for i in range(0, len(items), args.batch)]
res, lock = {}, threading.Semaphore(args.parallel)


def worker(i, doms):
    with lock:
        payload = {
            'startUrls': [{'url': f'https://{d}'} for d in doms],
            'crawlerType': 'cheerio', 'maxCrawlDepth': 1, 'maxCrawlPages': len(doms) * 8,
            'includeUrlGlobs': [{'glob': g} for g in GLOBS],
            'saveMarkdown': False, 'saveHtml': False,
            'proxyConfiguration': {'useApifyProxy': True}, 'requestTimeoutSecs': 30,
        }
        try:
            run = api('POST', f'acts/{ACT}/runs?memory=4096', payload)['data']
        except Exception as e:
            print(f'batch {i}: start failed: {e}', flush=True)
            return
        rid, ds = run['id'], run['defaultDatasetId']
        t0 = time.time()
        while True:
            time.sleep(20)
            try:
                st = api('GET', f'actor-runs/{rid}')['data']['status']
            except Exception:
                continue
            if st in ('SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT'):
                print(f'batch {i}: {st} in {int(time.time() - t0)}s', flush=True)
                break
            if time.time() - t0 > 1800:
                print(f'batch {i}: timeout', flush=True)
                break
        out, off = [], 0
        while True:
            try:
                ch = api('GET', f'datasets/{ds}/items?offset={off}&limit=100&clean=true&fields=url,text')
            except Exception:
                break
            if not ch:
                break
            out.extend({'url': x.get('url', ''), 'text': (x.get('text') or '')[:9000]} for x in ch)
            off += len(ch)
            if len(ch) < 100:
                break
        res[i] = out
        print(f'batch {i}: {len(out)} pages', flush=True)


ths = [threading.Thread(target=worker, args=(i, b)) for i, b in enumerate(batches)]
for t in ths:
    t.start()
for t in ths:
    t.join()

pages = [p for i in sorted(res) for p in res[i]]
dump_json(WD, 'site_pages.json', pages)
print('pages total:', len(pages))
