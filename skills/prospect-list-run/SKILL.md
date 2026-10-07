---
name: prospect-list-run
description: >-
  End-to-end pipeline that turns a client's raw prospect list (CSV or Google Sheet) into a
  ready-to-send prospect list plus four working documents. Builds an account base, enriches it
  (site crawl, own-site stack, LinkedIn headcount), scores each account on an 8-category rubric,
  finds live signals with evidence URL and date on the company's own domain, splits rows into
  campaigns (queue x persona x tier), writes first-line text into columns and publishes the docs
  (main, ICP, signal catalog, segments) to Notion or markdown. One JSON config per client. Use when the user says "here is our prospect
  list", "score this base and find signals", "run the flow on this list", "ось список проспектів",
  "прожени базу", "зроби проспект-лист", "проскор базу і знайди сигнали", "запусти флоу по базі",
  or shares a Google Sheet of companies. NOT for building a new list from scratch (data-research,
  account-sourcing, niche-data-finder) and NOT for writing sequences (sequence-writer).
---

# Prospect List Run: from a raw list to a list you can write from

A client hands over a list: names, domains, sometimes contacts. Three things are missing, and outreach
does not work without them: is this company a fit, why write now, and what goes in the first
line. This pipeline answers all three and returns a flat CSV that a sender can work from without
improvising.

The list format and the documents are the same for every client. Per client you change one file:
a copy of `config.example.json`.

Talk to the user in their language. Message text in the CSV is written in the prospect's language
(`language` in the config).

## Requirements & integrations

| Integration | Used for | Required? | Auth / setup |
|---|---|---|---|
| Python 3.9+ (standard library only) | all scripts | yes | none |
| Apify (`apify/website-content-crawler`, `harvestapi/linkedin-company`) | site crawl, LinkedIn headcount | optional (`--skip-apify` runs without it, scores drop to lower confidence) | `export APIFY_TOKEN=...` from Apify console, Settings, API & Integrations |
| Plain HTTP from your machine | own-site CMS check, careers/partner pages for signals | optional (`--no-http`) | none |
| Notion connector | publishing the four documents | optional | the client's Notion workspace; without it the docs are written as markdown files |
| Google Sheets | reading the client's list | optional | easiest path is File, Download, CSV of the right tab |

No other keys, services or files outside this folder are used.

## Output

1. `<Client>_prospect_list_full.csv`: the whole base, ~73 columns in 12 blocks, removed rows keep their reason
2. `<Client>_outreach_campaign.csv`: the working sample (passed filters, Hot + Warm, fit gate passed), same columns
3. Four documents: main page + ICP and personas + signal catalog + segments and campaigns
   (Notion if connected, otherwise markdown files; skeleton in `references/docs-skeleton.md`)

## Steps

### Step 0. Questions to answer before you start

- Which file or tab exactly (client spreadsheets often have dozens of tabs).
- Is the scoring rubric approved by the client? If not, label the whole run as preliminary, not as a
  working priority. Running a base on unapproved weights spreads a false priority across every row.
- Is there a signal catalog for this client? If not, build it first (step 5).

### Step 1. Get the data

A Google Sheet shared by link is often unreadable for connectors (access gets cut). The reliable path:
ask the user for `File -> Download -> CSV` of the right tab. Faster than fighting permissions.

### Step 2. Configure the client

Copy `config.example.json` to a file named after the client, kept wherever the user keeps client work
(not inside the skill folder). Walk the blocks top to bottom; each is labelled:

- `columns`: map the raw CSV headers; `extra` carries client-specific columns into the list as they are
- `capacity_column` + `capacity_unit`: the in-house headcount for the role your client replaces or
  supports (for example "in-house QA engineers"); drives stop filters, guesses and the adjacent-role signal
- `personas`: decision maker, champion and out-of-matrix title regexes
- `geo`: points per country and focus buckets
- `site`: which pages to crawl, feature flags (one regex each), optional `own_stack_cms`
- `hooks`: the service page URL pattern, the "own words" sentence pattern, cities, client sectors
- `signals`: codes, points, windows, queues, detection regexes (see step 4 for the source rule)
- `rubric`: 8 category caps, bands, gate, rules per category, stop filters, tiers (rule syntax in `scripts/README.md`)
- `text`: angle per queue, observation templates, guesses, questions

Point `source_csv` at the raw file (relative to the config) or pass `--source` to `build_base.py`.

### Step 3. Run

```bash
python3 scripts/run_pipeline.py --config path/to/client.json --workdir path/to/run-folder
```

or step by step (same flags on every script):

```bash
python3 scripts/build_base.py           # CSV -> accounts.json (dedup by domain, main contact by title rank)
python3 scripts/run_sites.py            # site crawl via Apify -> site_pages.json (about 5-8 min per 250 domains)
python3 scripts/detect_cms.py           # optional: what their own site runs on (the text crawl cannot see it)
python3 scripts/extract_features.py     # feature flags from page text
python3 scripts/extract_hooks.py        # unique first-line facts
python3 scripts/run_linkedin.py         # headcount and industry; re-run to resume if it stops early
python3 scripts/merge_linkedin.py
python3 scripts/score.py                # points -> scored.csv
python3 scripts/detect_signals_http.py  # live signals with evidence and date -> signals.json
python3 scripts/score.py                # re-score with signals
python3 scripts/build_canonical_list.py # the two CSVs
```

Dry run without keys or network: `python3 scripts/run_pipeline.py --skip-apify --no-http` (uses the
example config and `examples/source.example.csv`).

Check the Apify limit BEFORE the run (`GET https://api.apify.com/v2/users/me/limits`). An exhausted
monthly limit returns 403 on every actor and looks exactly like a broken script. When it happens, the
HTTP steps still work and signals can be taken from the company sites directly.

### Step 4. Check the signals by hand

**Mandatory.** Open `signals.json` and read at least 10 quotes. Automatic detection always produces
false positives, and each one becomes a message that looks foolish.

#### The source rule

**A signal counts only when its source is tied to the company's DOMAIN, not to its name.**

From one production run on about 250 agency accounts:

| Source | Raw hits | Survived manual review |
|---|---|---|
| The company's own site (`/careers`, `/partners`) | 21 | all 21: the domain matches by construction |
| Google search by company name | 187 | 0 usable: precision around 40%, it catches other firms with similar names |
| Reddit and Upwork posts | 906 | 0: no real match with the base |

Name search returns a different company whenever the name is short or generic (a one-word brand matches
dozens of unrelated firms). `validate_google_signals.py` drops results that do not contain the domain,
which removes a large share of the noise but also cuts valid vacancies posted on third-party job boards,
so precision stays low.

Reddit, Upwork, Facebook groups and Slack communities fail for another reason: direction. You cannot
ask "did company X post on Reddit". You can only find posts and see who wrote them. That is a search for
NEW leads, a separate exercise, and it does not verify an existing list.

So `signals.points` holds only codes that are read from the company's own domain. Keep the rest in the
catalog marked "source needed".

#### Four traps that already cost a run

- a team member's job title on the careers page ("Full-Stack Developer") reads as a vacancy
- "we do not have any job openings" slips past an empty-page filter
- a vacancy from years ago sits on a live page and looks fresh (the script skips quotes whose nearby
  dates are all older than last year, but check anyway)
- a `/partners` or `/white-label` page almost always means the opposite: the company sells the same
  service itself. That is your client's competitor, not a lead. Signals are split by direction.

#### Anti-signals live separately

They go to `anti_signals.json`, not `signals.json`, and are checked on every account, including ones
already disqualified. Otherwise you get a loop: the signal pass only covers accounts that passed, a
disqualified competitor is never re-checked, the stop filter quietly lapses and the competitor comes back.

### Step 5. Signal catalog

If the client does not have one, build it once: signal families, then per code how to detect it, what
counts as evidence, shelf life, points and the first-touch play. Plus a separate block of anti-signals
that disqualify. Codes in the catalog and in `signals.points` must match one to one. If installed,
`signal-research` (pack `outbound-engine-skills`) helps build the catalog.

### Step 6. Documents

Four documents, skeleton in `references/docs-skeleton.md`. With a Notion connector: one parent page and
three children in the client's workspace. Without it: four markdown files in the work directory.
Nothing is sent to prospects: drafts only, the client sends.

## The list: 12 blocks

The order is fixed. Blocks 7 and 9 adapt to the client, the rest never change:
1 Company · 2 Stop filters · 3 Headcount · 4 Fit · 5 Signal · 6 Data point · 7 Proof of current work
(client-specific) · 8 Source control · 9 Website (client-specific) · 10 Contact · 11 Text · 12 Segmentation.
Column list in `references/docs-skeleton.md`.

## Segmentation

`campaign` = queue x persona x tier. One campaign has one text and its own statistics.

- event queue: a dated event (for example the target vacancy). Lives as long as the event does, goes first, has its own pace
- weak-signal queue: a weaker or older signal
- datapoint queue: no signal; the first paragraph stands on a fact from their own site

Mix event and datapoint rows in one campaign and the average hides both the strong and the weak segment.

Decision maker and champion are separate campaigns: different pains, different questions. Titles outside
the matrix go to their own campaign with `text_gate = review`, so one filter switches them off.

Two or three contacts per company is normal. Leave at least three days between people at the same firm
and use a different angle for the decision maker and the champion.

## Text

The sender writes nothing. They drop values into a fixed skeleton: `observation` (a fact about them) ->
`guess` (a hypothesis about the bottleneck) -> fixed offer paragraph chosen by `angle` -> `question`
(exactly one question).

- `text_gate = ok` only when real evidence sits under the first line. Otherwise `review` with the reason in `text_gate_reason`
- `hook_source` is mandatory: a row without it is not sent
- no filler values in place of an empty observation
- every message ends with a question and never asks for a call. If installed, `cta-interest-based` (pack `outbound-engine-skills`) has the CTA rules

## Score normalisation

Raw lists almost never carry deal value or company size, which is a quarter of the points. Without a
correction the ceiling sits near 75 and nobody reaches Hot, not even a perfect lead.

So there are two numbers: `lead_score` is the plain sum; `lead_score_100` is the share of the points
available in categories that actually have data. The band uses the second one only at confidence H or M.
At L it uses the raw score, so an empty lead cannot look perfect thanks to two filled fields. A Hot lead
at confidence L is lowered to Warm, and Hot or Warm leads that miss the gate (service fit, geo, decision
maker) drop one band.

## Cost of a run (about 250 companies)

| Step | Cost |
|---|---|
| Site crawl (Apify website-content-crawler) | Apify compute units, usually within a monthly plan |
| Own-site stack check (HTTP) | free, from your own IP |
| LinkedIn company data (`harvestapi/linkedin-company`) | per-company actor price, about 1 USD for 250 companies at the time of writing; check the actor page |
| Careers and partner pages (HTTP) | free |

## What the pipeline does not do

- does not build new lists: it works with what the client gave
- does not write sequences, only the three fill-in lines
- sends nothing: drafts only, the client sends
- does not invent deal value, size, stack or titles: no data means 0 and "enrich"
- does not add signals together: it takes the largest one

## Related skills

If installed:
- `signal-research` (pack `outbound-engine-skills`): a signal pass over a base without scoring or the list format
- `lead-scoring` (pack `outbound-engine-skills`): the scoring rubric on its own
- `data-research`, `account-sourcing`, `niche-data-finder` (pack `outbound-engine-skills`): building a NEW list
- `sequence-writer` (pack `outbound-engine-skills`): full sequences on top of this list

## Credits

Method, list format and scripts by Victor Shulga (victorshulga.com). The pipeline calls two public Apify
actors (`apify/website-content-crawler`, `harvestapi/linkedin-company`); their output formats belong to
their authors.
