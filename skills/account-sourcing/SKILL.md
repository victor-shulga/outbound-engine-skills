---
name: account-sourcing
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

Tiers: first priority ≥ 95 · second priority 75–94 · third priority < 75. In the report write the priority in words; the CSV column may keep A/B/C as a filter value.

**A blank field is not an average.** A company with no founding date silently loses 10 points. That is correct — unknown is not fine — but say which rows were capped, so a thin-data low score is never mistaken for a bad-fit low score.

## Verify the quote before it ships

Regex on `legacy` produces false positives. Real examples from one run: "building a legendary legacy", "access should not be limited by legacy systems" in a marketing preamble. Roughly one in seven quotes is noise.

Extract one sentence around the match, cap it at 260 characters, and put it in a `proof_snippet` column. Someone reads that column with their eyes before the list goes to enrichment. Ten seconds per account.

## Terms and plain-language output

<!-- glossary:start terms=ats,buying-signal,stop-filter,priority-tier,headcount,proof-snippet,enrichment,anti-icp -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| ATS, ATS aggregator, career sites | система найму на сайті компанії | сервіси на кшталт Greenhouse чи Lever, звідки беремо повний текст вакансій |
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
| stop-filter, hard gate, deny-list | стоп-фільтр | одна ознака «ні» прибирає компанію до будь-яких витрат на дослідження |
| score tier A / B / C (≥95 / 75–94 / <75) | пріоритет: перший · другий · третій | група компанії за сумою балів зі 135 можливих |
| headcount, emp_final | кількість працівників | беремо зі сторінки компанії в LinkedIn, бо бази часто помиляються в діапазонах |
| proof_snippet | цитата-доказ з вакансії | одне речення з тексту вакансії, де компанія сама називає свою проблему |
| enrichment, enrich | дозбір даних | Пошук імен, посад і робочих пошт для компаній зі списку з кількох джерел. |
| Anti-ICP, disqualifiers | кому не продаємо | ознаки компаній, з якими не працюємо, щоб не витрачати на них час. |
<!-- glossary:end -->

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
