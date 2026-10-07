# -*- coding: utf-8 -*-
"""Shared helpers for the prospect-list-run pipeline.

Every step script calls `setup(description)` which:
  * parses --config and --workdir (env fallbacks PLR_CONFIG / PLR_WORKDIR),
  * loads the JSON config (default: config.example.json next to SKILL.md),
  * returns (cfg, workdir, args).

Nothing here reads files outside the skill folder, the config you pass and the work directory.
Secrets come from environment variables only (APIFY_TOKEN).
"""
import argparse
import datetime
import json
import os
import re
import sys

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPTS_DIR)
DEFAULT_CONFIG = os.path.join(SKILL_DIR, 'config.example.json')


def setup(description, extra_args=None):
    p = argparse.ArgumentParser(description=description)
    p.add_argument('--config', default=os.environ.get('PLR_CONFIG', DEFAULT_CONFIG),
                   help='path to the client config JSON (env PLR_CONFIG; default: config.example.json in the skill folder)')
    p.add_argument('--workdir', default=os.environ.get('PLR_WORKDIR', os.path.join(os.getcwd(), 'plr-run')),
                   help='folder for intermediate JSON and output CSVs (env PLR_WORKDIR; default: ./plr-run)')
    if extra_args:
        extra_args(p)
    args = p.parse_args()
    cfg = load_config(args.config)
    os.makedirs(args.workdir, exist_ok=True)
    return cfg, args.workdir, args


def load_config(path):
    if not os.path.exists(path):
        sys.exit(f'config not found: {path}')
    with open(path, encoding='utf-8') as fh:
        cfg = json.load(fh)
    cfg['_path'] = os.path.abspath(path)
    cfg['_dir'] = os.path.dirname(os.path.abspath(path))
    cfg.setdefault('client', 'client')
    cfg['_slug'] = re.sub(r'[^A-Za-z0-9]+', '_', cfg['client']).strip('_') or 'client'
    rd = cfg.get('run_date') or datetime.date.today().isoformat()
    cfg['_today'] = datetime.date.fromisoformat(rd)
    return cfg


def rx(pattern):
    """Compile a config regex (case-insensitive). Empty or missing pattern matches nothing."""
    if not pattern:
        return re.compile(r'(?!x)x')
    return re.compile(pattern, re.I)


def wpath(workdir, name):
    return os.path.join(workdir, name)


def load_json(workdir, name, default=None, required=False):
    path = wpath(workdir, name)
    if not os.path.exists(path):
        if required:
            sys.exit(f'missing {path}: run the earlier pipeline step first')
        return default
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def dump_json(workdir, name, obj):
    with open(wpath(workdir, name), 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)


def norm_domain(w):
    w = (w or '').strip().lower()
    w = re.sub(r'^https?://', '', w)
    if w.startswith('www.'):
        w = w[4:]
    return w.strip('/ ').split('/')[0]


def apify_token():
    tok = os.environ.get('APIFY_TOKEN', '').strip()
    if not tok:
        sys.exit('APIFY_TOKEN is not set. Export your Apify API token first: export APIFY_TOKEN=...')
    return tok


def to_int(v, default=-1):
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return default


def cond_ok(cond, ctx):
    """Evaluate one rule condition from the config against an account context.

    ctx keys: flags (set of true site-feature flags), has_site (bool), own_stack (bool),
    own_cms (str), capacity (int, -1 = unknown), volume (int), country (str), size (int, 0 = unknown).
    Every key present in `cond` must hold. Unknown keys are ignored.
    """
    flags = ctx['flags']
    if 'flags_all' in cond and not all(f in flags for f in cond['flags_all']):
        return False
    if 'flags_any' in cond and not any(f in flags for f in cond['flags_any']):
        return False
    if 'flags_none' in cond and any(f in flags for f in cond['flags_none']):
        return False
    if 'has_site' in cond and bool(cond['has_site']) != ctx['has_site']:
        return False
    if 'own_stack' in cond and bool(cond['own_stack']) != ctx['own_stack']:
        return False
    if 'own_cms_in' in cond and ctx['own_cms'] not in cond['own_cms_in']:
        return False
    cap = ctx['capacity']
    if 'capacity_known' in cond and bool(cond['capacity_known']) != (cap >= 0):
        return False
    if 'capacity_min' in cond and not (cap >= 0 and cap >= cond['capacity_min']):
        return False
    if 'capacity_max' in cond and not (cap >= 0 and cap <= cond['capacity_max']):
        return False
    if 'volume_min' in cond and not ctx['volume'] >= cond['volume_min']:
        return False
    if 'geo_in' in cond and ctx['country'] not in cond['geo_in']:
        return False
    size = ctx['size']
    if 'size_min' in cond and not (size and size >= cond['size_min']):
        return False
    if 'size_max' in cond and not (size and size <= cond['size_max']):
        return False
    return True


def first_rule(rules, ctx):
    for r in rules or []:
        if cond_ok(r, ctx):
            return r
    return None
