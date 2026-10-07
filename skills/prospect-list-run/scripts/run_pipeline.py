# -*- coding: utf-8 -*-
"""Run the whole prospect-list-run pipeline in order.

Steps: build_base -> run_sites* -> detect_cms -> extract_features -> extract_hooks -> run_linkedin*
-> merge_linkedin* -> score -> detect_signals_http -> score -> build_canonical_list.
Steps marked * call Apify and need APIFY_TOKEN; --skip-apify leaves them out (a dry run then
works on the client list alone, plus the free HTTP checks unless you also pass --no-http).

Usage:
  python3 scripts/run_pipeline.py --config my-client.json --workdir ./runs/my-client
  python3 scripts/run_pipeline.py --skip-apify --no-http          # offline dry run on the example
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
p.add_argument('--config', default=os.environ.get('PLR_CONFIG', os.path.join(os.path.dirname(HERE), 'config.example.json')))
p.add_argument('--workdir', default=os.environ.get('PLR_WORKDIR', os.path.join(os.getcwd(), 'plr-run')))
p.add_argument('--skip-apify', action='store_true', help='skip the site crawl and the LinkedIn steps')
p.add_argument('--no-http', action='store_true', help='skip the direct HTTP checks (CMS and signals)')
p.add_argument('--no-cms', action='store_true', help='skip detect_cms (when the offer does not depend on the stack)')
a = p.parse_args()

steps = ['build_base']
if not a.skip_apify:
    steps.append('run_sites')
if not a.no_http and not a.no_cms:
    steps.append('detect_cms')
steps += ['extract_features', 'extract_hooks']
if not a.skip_apify:
    steps += ['run_linkedin', 'merge_linkedin']
steps.append('score')
if not a.no_http:
    steps += ['detect_signals_http', 'score']
steps.append('build_canonical_list')

for s in steps:
    print(f'\n=== {s} ===', flush=True)
    rc = subprocess.call([sys.executable, os.path.join(HERE, f'{s}.py'), '--config', a.config, '--workdir', a.workdir])
    if rc != 0:
        sys.exit(f'step {s} failed with exit code {rc}')
print('\ndone. Next: read 10 quotes in signals.json before anyone uses the list.')
