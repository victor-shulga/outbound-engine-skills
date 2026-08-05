---
name: signal-research
description: >
  Runs a signal-research pass over an EXISTING firmographic account base (CSV, Google Sheet,
  Notion DB, CRM export) for a B2B service agency: decides which signals to hunt for this ICP,
  detects them account-by-account from cheapest source upward, records evidence URL + date for
  every hit, scores and heat-tiers the accounts, flags expired signals for re-scan, and returns
  an enriched list plus a coverage report that says which sources actually produced signals.
  Use when the user says: "знайди сигнали по базі", "прогони базу на сигнали", "ресерч сигналів",
  "signal research", "у нас є список компаній — хто зараз гарячий", "перескануй базу, сигнали
  вигоріли", "which accounts have a live trigger right now", "enrich this list with signals",
  or hands over a company list and asks who to contact first. Requires a base — this skill does
  NOT build the list (use list-building / niche-data-finder) and does NOT invent the signal
  library (that lives in `resources/signals-catalog.md`). It also does not write outreach copy.
---

# Signal Research — turn a static account base into a live, dated, evidenced signal list

A firmographic base tells you WHO fits. It does not tell you WHEN to write. This skill closes
that gap: it takes the base you already have and answers, per account, "is a trigger live right
now, what is the proof, and how old is it".

Two run modes:

- **Full run** — base has never been signal-researched.
- **Delta run** — base was researched before; re-scan for burnt signals and new fires. Most bases
  rot in ~45 days, and nobody notices because the status column keeps saying Hot.

## Setup (once per session)

Resolve the install dir dynamically — never hardcode:
1. Glob for `**/signal-research/SKILL.md`
2. That directory is `SKILL_BASE`; resources are `{SKILL_BASE}/resources/...`

Load, in this order:
1. `clients/<client>/icp.md` and `clients/<client>/signals.md` if the workspace has them — the
   client's own signal tiers, detection routes, geo source table and open-data traps ALWAYS win
   over anything generic in this skill.
2. `{SKILL_BASE}/resources/signals-catalog.md` — the signal library: 60 catalogued entries across
   account events and news, hiring, tech changes, person-level activity, project-flow and build-intent,
   plus vertical packs and the data-point series (universal `D`, and per-vertical `DV` / `DA`). Each
   carries a detection route, a freshness window and a pairing note. Use when the client has no
   `signals.md` yet — and extend the catalogue rather than inventing a signal inline.
3. *Optional, if installed:* `agency-signal-sourcer` (in the
   [gtm-skills](https://github.com/victor-shulga/gtm-skills) repo) carries a deeper tool-per-signal
   table with credit costs, decay windows and heat-tier SLAs. Without it, the detection ladder and
   catalogue in this skill's own `resources/` are enough to run.

If none of those exist, stop and say so. Do not invent a signal list here.

## Hard rules

1. **No evidence, no signal.** Every non-empty `signal_type` carries a live URL and a date. A
   signal you cannot link is written as `none` with the reason. Plausible-sounding inference is
   the single fastest way to poison a base.
2. **Date the detection, not the run.** `signal_date` = when the event happened (posting date,
   permit issue date, award date). `signal_age_days` = run date − signal_date. If the source only
   gives "posted 3 weeks ago", record the derived date and set `signal_date_precision = approx`.
3. **Cheapest source first.** Work down the ladder in `resources/detection-ladder.md`. Never spend
   a paid credit on an account a free bulk query already answered.
4. **Stop-filter before research.** Run anti-ICP and geo/size gates first, research only survivors.
   Researching drops is the most common way this job costs 3× what it should.
5. **One row per company for signals, contacts stay separate.** Signal research is account-level.
   Contact expansion (2–3 people per company) happens after, in the list step.
6. **Expired ≠ absent.** A signal past its window is demoted to a data point (it still tells you
   what to say) and the account is queued for re-scan — it is not silently deleted.
7. **Confidentiality.** Never carry one client's account names, evidence or list into another
   client's artifact.

## Phase 0 — Intake and base normalisation

Ask only for what is missing:
- Path/link to the base, and the client it belongs to.
- Run mode: full or delta (if the base has `signal_date` values already → propose delta).
- Geo scope and any batch cap ("just Tier A / NY / first 200").

Then normalise, writing values not formulas:
- `row_id`, `company_name_raw`, `company_name_clean`, `domain`, `country`, `geo_bucket`, `city`,
  `industry` — the canonical company block.
- Dedup by domain; where domain is missing, dedup by cleaned name + city, and flag `match_method`.
- Apply `filter_geo` / `filter_size` / `filter_anti_icp` → `filter_result`, with
  `exclusion_reason` filled for every drop. Report the funnel: raw → deduped → in scope.

Report the surviving count BEFORE starting detection, and get a go if the number implies real cost.

## Phase 1 — Signal plan (the part that decides the cost)

Pick **4–7** signals, no more. For each, write one line in the plan table:

| Signal | Tier | Source / route | Cost per 100 | Window (days) | Expected hit rate |
|---|---|---|---|---|---|

Rules for picking:
- At least two must be **bulk-detectable** — one query covers the whole base (open-data API,
  tender feed, news feed, platform job-posting filter). These carry the run.
- At most two may be **per-account manual** (careers page, site news). These are the expensive tail.
- Drop any signal whose fit score against this ICP is low, even if it is famous. Funding rounds
  fire for almost nobody in contractor/services verticals; hiring fires for everybody.
- A signal with no realistic detection route does not go on the plan. Note it under "wanted but
  undetectable" in the report instead.

Show the plan and the projected cost before running it.

## Phase 2 — Detection, in three passes

Full mechanics, join rules and source-type traps: `{SKILL_BASE}/resources/detection-ladder.md`.

**Pass A — bulk sources (covers the whole base).** One query per source, then join back to the
base by name/domain. Record `match_method` (`domain`, `exact_name`, `fuzzy_name+city`, `manual`).
Fuzzy matches over the base's own names are the main source of false positives — spot-check 10.

**Pass B — per-account web research.** Only for in-scope accounts with no Pass A hit. Batch 10–15
accounts per parallel research agent; each agent returns strictly: company, signal type, one-line
evidence, URL, date, or explicit `none`. Instruct agents that `none` is a correct and expected
answer, otherwise they hallucinate a signal for every row.

**Pass C — platform filters.** Apollo / LinkedIn / Sales Nav / intent tooling for what remains, and
only where the account passed the fit gate. Note person-level tracking is US-only under GDPR —
for EU targets use company-level identification.

After each pass, log yield: accounts scanned, hits, cost. A pass yielding under ~5% on a base this
size is reported as such, not quietly repeated at a larger scale.

## Phase 2b — Data points, harvested in the same pass

A signal fires on 3–5% of a base. A data point is available on almost all of it. Run them together
or the economics never work: Pass B already fetches the account's pages, and a second crawl later
to collect facts is paying twice for the same bytes.

The two are not the same thing and must not share a column:

|  | Signal | Data point |
| :-- | :-- | :-- |
| What it is | a dated event | a standing fact |
| What it decides | **when** to write | **what** to say |
| Coverage | 3–5% of the base | most of the base |
| Expiry | has a window, then burns | does not expire — that is the point |
| Needs | URL **and** date | source page, no date required |

Types worth carrying, roughly in order of how much they change a message: capability the account
runs in-house · equipment or tooling they name · software stack · scale (volumes, sizes, counts) ·
named clients or sectors served. Sector mix is the weakest — it is on every site and adapts almost
nothing.

**Extraction rules that cut the noise.** These were paid for in real runs:

- **A number is only a volume if a working word sits beside it.** Require a domain verb or noun
  within ~70 characters of the figure, otherwise the crawl proudly returns "20 miles west of" as a
  project volume.
- **Take a character window around the match (~150 either side), not a sentence.** Sentence
  splitting drags navigation menus and cookie banners into the quote.
- **Marketing promises are not pain.** A page advertising fast turnaround is a claim about
  themselves, not evidence they struggle with deadlines. Detecting "complaints about timelines"
  this way does not work — drop it rather than record noise.
- **A data point still needs a source URL**, even without a date. Without it the opening line
  cannot be checked before sending, and `hook_source` stays empty, which blocks the row.

Queue D — the accounts with no live signal — stands entirely on this harvest. If the data-point
pass is skipped, queue D has nothing to open with and the campaign silently becomes a mass mailing.

## Phase 3 — Score and heat-tier

Use the client's own formula from `clients/<client>/signals.md`. If absent, default to:

```
score = fit (High 60 / Med 35 / Low 10)
      + signal_tier (T1 40 / T2 25 / T3 10)
      + capability gap (+10 gap present or unknown / −10 they already do it in-house)
```

- **Stacking:** a second independent signal adds +10, a third +5 — never a second full tier.
  Two facts from the same event (a job post and the press release about that job) are ONE signal.
- **Recency multiplier:** ×1.0 inside half the window, ×0.7 in the second half, ×0.3 past it.
- Heat tiers Hot / Warm / Cool / Drop with the client's thresholds, and an SLA per tier (Hot =
  touch within 48h, or the research was wasted).

## Phase 4 — Freshness and the re-scan queue

For every scored account write `signal_expires_on = signal_date + window` and
`rescan_due = min(expires_on, run_date + 30d)`.

Delta run:
1. Reload the previous output, compare `signal_expires_on` to today.
2. Expired → move signal detail into `datapoint_type` / `datapoint_detail`, clear the signal block,
   set `status = burnt`.
3. Re-run Phase 2 for burnt + never-signalled accounts only.
4. Output the change table: new fires, burnt, re-fired, still cold. That table is the actual
   deliverable of a delta run — not the whole file again.

## Phase 5 — Output

Two artifacts, always both.

**1. Enriched list (CSV, flat, one header, values not formulas).** Keeps every input column, adds
the canonical signal block: `signal_type · signal_score · signal_route · signal_evidence_url ·
signal_date · signal_age_days · signal_summary · signal_2_type · signal_2_url · signal_3_type` plus
`datapoint_type · datapoint_detail`, and this skill's own `signal_expires_on · rescan_due ·
signal_date_precision · match_method · detected_by · detected_on`. Full spec and value vocabularies:
`{SKILL_BASE}/resources/output-spec.md`. Ship the full base (drops included, each with a reason)
and the working slice as two files with identical columns.

**2. Coverage report.** Structure and wording: `{SKILL_BASE}/resources/report-template.md`. It must
state the source-yield ranking (which source produced how many signals at what cost), the signals
that produced nothing → keep/kill verdict, what stayed undetectable and why, and the re-scan date.
A run that reports only "found 37 hot accounts" hides whether the method is repeatable.

Where the workspace stores client results in Notion, the list stays a CSV and the report becomes a
readable page — a database dump with a link to a kanban is not a report.

## Handoffs

| Next question | Skill |
|---|---|
| Which signal × ICP × offer should we even test | `hypo-generator` / `06-hypothesis-builder` |
| Which tool detects signal X, what does it cost, when does it decay | `agency-signal-sourcer` |
| Base is too small / where do I find more accounts | `niche-data-finder`, `list-building` |
| Turn scored accounts into a full prospect list with contacts and copy slots | client prospect-list flow |
| Write the sequence off these signals | `sequence-writer` |
| Per-account pre-touch briefing | `prospect-profiler` |

## Detection traps already paid for

- A team member's email signature on a careers page reads as an open vacancy.
- "We don't have any job openings" slips through an empty-page filter and is recorded as a page with
  no result rather than an explicit no.
- An old posting sitting on a live page looks fresh. Date the posting, not the page.
- Aggregators keep copies of closed postings for months. A posting that exists only on an aggregator
  is treated as expired.
- A careers page is not a job list. Most companies route to an external board — follow the link, or
  you will record "no vacancies" for a company with five.
- A `/partners` or `/white-label` page usually means the opposite of a need: they *sell* the service.
  Read the direction of the wording before scoring it. On one run every such page found belonged to a
  competitor, not a lead.
- Anti-signals must sit in their own file and be checked across **all** accounts, including already
  disqualified ones. A run that only reads non-disqualified rows never re-checks a filtered-out
  competitor, the stop-filter melts, and the competitor returns to the base.
- News through general search does not work for firms of 10–500 people: one run of 168 candidates
  returned safety awards, Awards pages, contract registries and social posts, under a third accurate.
  Use dedicated feeds and portals.

## Failure modes seen in real runs

- **Signal on a company that cannot buy.** Fit gate must run before, not after, detection.
- **A whole geo silently uncovered.** Open-data coverage is city-by-city, not national. Report
  coverage per `geo_bucket`; an empty bucket is a finding, not a blank cell.
- **Date fields that lie.** Public datasets ship text dates in mixed formats, placeholder years
  (9999, 3030), and freshness metadata that never updates. Verify the newest row by filtering on a
  literal recent value before trusting any `max()` or descending sort.
- **The base ages and nobody re-scans.** If there is no delta run scheduled, the score column is
  fiction within two months. Set `rescan_due` and say it out loud in the report.
