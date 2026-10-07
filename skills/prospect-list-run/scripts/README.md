# Pipeline scripts

Per client you change **one file**: a copy of `config.example.json`. The scripts stay as they are.
Run everything from the skill folder (or anywhere, with absolute paths to the scripts). Each script
takes `--config <file>` (env `PLR_CONFIG`) and `--workdir <folder>` (env `PLR_WORKDIR`, default `./plr-run`).
All intermediate JSON and the output CSVs go to the work directory, never into the skill folder.

| File | What it does | Network / cost | Reads from config |
|---|---|---|---|
| `common.py` | config loader, rule evaluator, shared helpers | none | everything |
| `run_pipeline.py` | runs all steps in order (`--skip-apify`, `--no-http`, `--no-cms`) | as the steps below | paths only |
| `build_base.py` | raw CSV -> `accounts.json`, dedup by domain, picks the main contact | none | `columns`, `personas`, `source_csv` |
| `run_sites.py` | crawls company sites -> `site_pages.json` | Apify, `APIFY_TOKEN` | `site.glob_paths` |
| `detect_cms.py` | what each company's own site is built on -> `cms.json` (optional) | plain HTTP, free | `site.own_stack_cms` |
| `extract_features.py` | feature flags from page text -> `site_features.json` | none | `site.patterns` |
| `extract_hooks.py` | unique first-line facts -> `hooks.json` | none | `hooks` |
| `run_linkedin.py` | company headcount and industry -> `linkedin_raw.json` (resumable) | Apify, `APIFY_TOKEN` | none |
| `merge_linkedin.py` | LinkedIn records -> `company_size.json` | none | none |
| `score.py` | stop filters, 8 categories, score, score-100, band, tier -> `scored.csv/json` | none | `rubric`, `geo`, `signals.points` |
| `detect_signals_http.py` | live signals with URL and date -> `signals.json`, `anti_signals.json` | plain HTTP, free | `signals.detect` |
| `validate_google_signals.py` | optional domain gate for signals found by name search | none | none |
| `build_canonical_list.py` | two CSVs in the 12-block structure with ready text | none | `text`, `signals`, `capacity_column` |

Order: `build_base -> run_sites -> detect_cms -> extract_features -> extract_hooks -> run_linkedin
-> merge_linkedin -> score -> detect_signals_http -> score -> build_canonical_list`.

## Rule syntax (rubric, stop filters, tiers, guesses)

A rule is a JSON object; every key in it must hold. First matching rule wins.

| Key | Meaning |
|---|---|
| `flags_all` / `flags_any` / `flags_none` | site feature flags (names from `site.patterns`) |
| `has_site` | true when the crawl returned pages for the domain |
| `own_stack` | true when `cms.json` matches `site.own_stack_cms` |
| `own_cms_in` | own-site CMS is in the list |
| `capacity_known`, `capacity_min`, `capacity_max` | the in-house capacity column (`capacity_column`) |
| `volume_min` | portfolio volume found on the site |
| `geo_in` | country is in the list |
| `size_min`, `size_max` | headcount (LinkedIn first, site text as fallback) |
| `points` / `reason` / `tier` / `text` | what the rule returns |
| `gap: true` | marks the category as "no data" (it leaves the score-100 denominator) |

A category with `gap_when` returns "no data" when that condition holds.

## Offline dry run

```bash
python3 scripts/run_pipeline.py --skip-apify --no-http --workdir /tmp/plr-dry
```

Uses `config.example.json` and `examples/source.example.csv` (fictional companies on example domains).
