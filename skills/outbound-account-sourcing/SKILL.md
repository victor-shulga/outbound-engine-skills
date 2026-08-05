---
name: outbound-account-sourcing
description: Builds a filtered, scored account list from job-posting signals — pulls postings from ATS career sites via Apify, strips the two thirds of results that are agencies, government and universities, and scores every surviving company. Use when the user says "збери список", "прospect list", "build the account list", "знайди компанії за сигналом", "who is hiring for X", or needs accounts before enrichment. Requires an Apify connection.
---

# Account Sourcing From Job Signals

Job postings are the cheapest honest signal in B2B. A company that publishes "our application is a majestic monolith" has spent money saying it and will not walk it back.

## Why ATS aggregators, not LinkedIn

LinkedIn job scraping gives titles. What matters is the **body of the description** — that is where a company names its own problem. Use an aggregator that indexes career sites across ATS platforms (Greenhouse, Ashby, Lever, Workday and friends) and exposes:

- full-text search inside the description
- a company headcount filter
- an agency exclusion flag

On Apify the working actor is `fantastic-jobs/career-site-job-listing-api` (~$0.012 per posting). Equivalents outside Apify: TheirStack, PredictLeads.

## Query design

Two queries, not one.

**Query A — role signal.** Titles only: platform, infrastructure, SRE, DevOps. Wide net, tells you who is staffing the gap.

**Query B — language signal.** Broad engineering titles **plus** `descriptionSearch` on `legacy`, `monolith`, `technical debt`, `modernization`, `re-architect`. Narrow, and every row is a company describing its own problem.

Query B is worth more. Run both, merge, dedupe by domain.

Always set: country, headcount range, full-time, remove agencies, include company details.

### The trap that costs half the signal

"All active postings" mode returns **newest first** and truncates at your limit. Ask for 300 and you get the last week — and you will never see the role that has been open 139 days, which is the strongest capacity signal in the set.

**Fix: narrow the query until the total result count is below your limit.** Then the full active backlog comes back, stale postings included. A tight title list plus a description filter usually does it.

## Filtering — expect to drop two thirds

The agency flag does not catch what actually pollutes the results. Build an explicit exclusion pass:

- **By industry** — IT services and consulting, defense, government, higher education, staffing, professional services, non-profit
- **By name** — a maintained deny-list of contractors and holdcos you keep hitting
- **By title** — anything containing clearance, TS/SCI, polygraph
- **By geography** — headquarters outside the target market
- **By age** — founded within the last 3 years has nothing to modernize

`scripts/filter_score.py` in this skill implements the pass. Edit the lists; they are niche-specific and they are the part that ages.

**Review the deny-list after every run.** It is easy to over-filter and lose real product companies that happen to sit in a mislabeled industry. Diff the dropped rows once.

## Scoring

Additive, maximum 135. Always report the denominator.

```
40  base — cleared every filter
+25 problem language quoted in the posting body
+15 second engineering opening   |  +30 third and beyond
+20 posting open 60+ days        |  +10 open 30–59 days
+10 headcount inside the core band
+10 product in market 3+ years
```

Tiers: A ≥ 95 · B 75–94 · C < 75.

**A blank field is not an average.** A company with no founding date silently loses 10 points. That is correct — unknown is not fine — but say which rows were capped, so a thin-data low score is never mistaken for a bad-fit low score.

## Verify the quote before it ships

Regex on `legacy` produces false positives. Real examples from one run: "building a legendary legacy", "access should not be limited by legacy systems" in a marketing preamble. Roughly one in seven quotes is noise.

Extract one sentence around the match, cap it at 260 characters, and put it in a `proof_snippet` column. Someone reads that column with their eyes before the list goes to enrichment. Ten seconds per account.

## Output

CSV, one row per company:

`rank · score · tier · company · domain · headcount · industry · founded · hq · open_roles · days_open · target_role · proof_snippet`

Report alongside it: raw rows pulled, rows dropped and why, median headcount, median founding year, how many carry a verified quote, and the total spend.

## Requirements

| Integration | Used for | Required? |
|---|---|---|
| Apify MCP | job postings from ATS career sites | yes |
| Python 3 | filter and scoring script | yes |
| BuiltWith / Wappalyzer | stack signals, optional second pass | no |
