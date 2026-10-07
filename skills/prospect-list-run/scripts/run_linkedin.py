# -*- coding: utf-8 -*-
"""Step 3d. Company headcount, industry and founding year from LinkedIn company pages -> linkedin_raw.json.

Uses the Apify actor harvestapi/linkedin-company (paid per company; check the actor's current
price on Apify before a large run). Needs APIFY_TOKEN. Resumable: companies already present in
linkedin_raw.json are skipped, so re-run the script if the first pass returned only part of the list.

Usage: python3 scripts/run_linkedin.py [--config ...] [--workdir ...] [--batch 40] [--parallel 3]
"""
import json
import re
import threading
import time
import urllib.request

from common import setup, load_json, dump_json, apify_token


def extra(p):
    p.add_argument('--batch', type=int, default=40)
    p.add_argument('--parallel', type=int, default=3)


cfg, WD, args = setup(__doc__, extra)
TOKEN = apify_token()
ACT = 'harvestapi~linkedin-company'


def api(method, path, payload=None):
    url = f'https://api.apify.com/v2/{path}'
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'})
    return json.load(urllib.request.urlopen(req, timeout=300))


def key(u):
    return re.sub(r'/+$', '', (u or '').lower().replace('http://', 'https://').replace('www.', ''))


accounts = load_json(WD, 'accounts.json', required=True)
have = load_json(WD, 'linkedin_raw.json', default=[])
done = {key(x.get('originalQuery', {}).get('search', '') or x.get('linkedinUrl', '')) for x in have}
todo = [a['linkedin_company'] for a in accounts
        if a['linkedin_company'].startswith('http') and key(a['linkedin_company']) not in done]
print('already fetched:', len(have), '| to fetch:', len(todo), flush=True)

batches = [todo[i:i + args.batch] for i in range(0, len(todo), args.batch)]
out, lock, wl = [], threading.Semaphore(args.parallel), threading.Lock()


def worker(i, chunk):
    with lock:
        try:
            run = api('POST', f'acts/{ACT}/runs?memory=1024', {'companies': chunk})['data']
        except Exception as e:
            print(f'batch {i}: start failed: {e}', flush=True)
            return
        rid, ds, st, t0 = run['id'], run['defaultDatasetId'], '', time.time()
        while True:
            time.sleep(15)
            try:
                st = api('GET', f'actor-runs/{rid}')['data']['status']
            except Exception:
                continue
            if st in ('SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT') or time.time() - t0 > 900:
                break
        items, off = [], 0
        while True:
            try:
                ch = api('GET', f'datasets/{ds}/items?offset={off}&limit=100&clean=true')
            except Exception:
                break
            if not ch:
                break
            items.extend(ch)
            off += len(ch)
            if len(ch) < 100:
                break
        with wl:
            out.extend(items)
        print(f'batch {i}: {st}, {len(items)} records of {len(chunk)}', flush=True)


ths = [threading.Thread(target=worker, args=(i, b)) for i, b in enumerate(batches)]
for t in ths:
    t.start()
for t in ths:
    t.join()

dump_json(WD, 'linkedin_raw.json', have + out)
print('records total:', len(have) + len(out))
