---
name: data-research
description: Use when asked to turn a raw company list into a scored, evidenced prospect list — grade a base the client already has, enrich it from public sources, attach dated buying signals with proof, and output a ready-to-send file. Triggers include "run the list", "score these companies", "build the prospect list", "who do we write to first", "enrich this base".
---

# Data Research

Turns a raw base into a canonical prospect list. Answers three questions per row:
**is this account ours**, **why write now**, and **what goes in the first line**.

Most of the time this is not list building. A client hands over a CRM export, a scraped
sheet or an old campaign file, and the job is to grade what already exists. If there is no
base at all, source one first (Apollo, Sales Navigator, a directory scrape), then run this.

## The split everything rests on

- **Signal** = a dated event. True for ~3–5% of a cold base at any moment. Tells you **WHEN** to write.
- **Data point** = a permanent fact — stack, sector, headcount, whether they run the capability in-house. Tells you **WHAT** to say.

One signal as the reason plus one data point to shape the message. No signal → the message reads
as a mass mailing, because that is what it is.

Expecting a signal on most of the base is the most common planning error. 3–5% is the market,
not a tuning problem.

## Hard rules

1. **No URL and no date, no signal.** Write nothing rather than a guess. An unprovable signal is
   worse than an empty cell: it looks like work was done, and someone writes a letter off it.
2. **The signal source must resolve to the company's DOMAIN, not its name.** Measured on a real run:
   the company's own site produced 21 signals, all valid; Google-by-company-name produced 187 at
   ~40% accuracy (it kept returning different firms with similar names); Reddit and Upwork produced
   906 records and zero matches against the base. Name-matching and open forums find *new* leads —
   they do not verify a list you already have.
3. **`signal_date` is the date of the EVENT.** The date you ran the check is a separate column.
4. **Never invent headcount, deal size, stack or job title.** Missing → 0 points plus an enrichment
   flag. A guessed number becomes a forecast someone relies on.
5. **Rows that fail are not deleted.** They stay in the file with the reason. A deleted row gets
   re-bought and re-researched three months later.
6. **Dedupe by person, not by company.** 2–3 contacts per company is normal and wanted.
7. **Take the highest single signal, never sum them.** Multiple signals move an account up the queue
   inside its band, not up in points.
8. **Anti-signals live in a separate file and are checked across ALL accounts**, including
   disqualified ones. Otherwise the run only reads non-disqualified rows, a filtered-out competitor
   is never re-checked, the stop-filter melts, and the competitor returns to the base.

## Pass order — cheapest cut first

The order is not cosmetic. Each pass is priced per row, so anything that removes rows must run
before anything that costs money per row.

**Pass 0 — audit what you were given.** Before spending a cent. On a real base, of 131 emails in
the client's column only 27 carried their own company domain, 76 carried a foreign domain, and 19
were not emails at all. Also check for rows written off as "no size in CRM" — that is a data hole,
not a rejection, and they belong back in the base.

**Pass 1 — stop-filters.** Anti-ICP and hard gates. One "no" is a stop; completeness is checked
only after. Never spend detection time on a row that fails here.

**Pass 2 — profile.** Cuts the most, costs the least. One SERP query per company (name + country,
one page) returns a service description, domain and social page. On a 596-company run this cost
~$1.5 total and grew the workable segment 1.7×, because half the base could not be classified from
name and job title alone. Cheaper than the manual web verification a client usually does by hand.

**Pass 3 — headcount, only for rows that passed the profile gate.** The company's own social page
is the primary source; enrichment refines inside the range. Roughly $0.004–0.006 per company.
Set the tier **only on a verified number** — on one base of 188 companies half the source's size
buckets were wrong, with 83 companies below the stated lower bound.

**Passes 4 and 5 — signals and data points. Handed to `signal-research`.**

This is a step of its own, not a stage of list building, and it runs on its own economics: a signal
fires on 3–5% of a base while a data point is available on nearly all of it, so both are harvested in
one crawl or the arithmetic never works. `signal-research` owns the signal library, the detection
ladder (cheapest bulk source first, per-account research second, paid platforms last), the evidence
rule, the freshness windows and the re-scan queue.

Run it here, between headcount and email, and take back two things: the signal block
(`signal_type · signal_evidence_url · signal_date · signal_route` …) and the data-point block
(`datapoint_type · datapoint_detail`). Everything downstream — the queue an account lands in, what
its opening line stands on — comes from those two blocks.

Do not re-implement detection inside this skill. The one rule worth repeating here because it decides
the cost of the whole run: **the source must resolve to the company's domain, not its name.**


**Pass 6 — email.** Only for rows that survived. See the `waterfall-enrichment` skill.

**Pass 7 — second contact per account** (champion alongside the decision maker).

After every pass, record: rows covered, results produced, money and time spent. A pass yielding
under 5% is reported as such, not repeated at a bigger scale.

## Cost model — carry real numbers, not "credits"

| Pass | Typical unit cost | Notes |
|---|---|---|
| Profile via SERP | ~$0.0025 / company | one query, one page |
| Company page scrape | $0.004–0.006 / company | headcount, description, specialties |
| Site content crawl | batch-priced | depth 1, globbed URLs, batches of ~35 |
| Job postings | ~$0.005 / posting | filtered by slug + title |
| Email waterfall | ~1.4 credits / person | see `waterfall-enrichment` |

Quote a run before starting it. A base of 2,000 companies through all passes is a known number,
not a surprise.

## Scoring notes

Use `prospect-scoring` for the rubric itself — this stage is pre-contact, so nothing that only a
conversation reveals belongs in the number (that is `lead-scoring`, which starts from this profile).
Three things it insists on at this stage:

- **Tier only on a verified number.** Where headcount is unconfirmed, the tier cell reads
  "verify manually" — never blank, never guessed.
- **Normalise when whole categories are empty.** Raw bases almost never carry deal size. If a
  15-point category is structurally 0 for everyone, the ceiling drops and nobody ever reaches the
  top band. Keep two numbers: the plain sum, and the percentage of categories that actually had
  data. Band on the second — but only when data confidence is medium or better, otherwise a row
  with two filled fields looks perfect.
- **Safety catch.** An account does not enter a top band unless the load-bearing categories
  (stack fit, geo, access to the decision maker) each clear their floor. Otherwise it drops a band.

An open role that has been live for 45+ days is a **stronger** signal than a fresh one — they cannot
fill it. Do not decay a vacancy while it is still open.

## Segmentation

`campaign` = **queue × persona × tier**. One campaign is one text and its own statistics.

- **Queue A** — a dated event. Lives as long as the event lives. Goes first.
- **Queue B** — a weaker signal.
- **Queue D** — no signal; the opening line stands on a data point from their site.

Mixing A and D into one campaign hides both the strong and the weak segment behind an average.
Decision maker and champion are separate campaigns — different pains, different questions. Titles
outside the persona matrix get their own campaign flagged for review.

## Output

Flat CSV, one header row, values not formulas, no grouped rows above the columns. **Two files with
identical columns**: the full base including everything filtered out with its reason, and the
working selection.

Column blocks, in a fixed order:

1. **Company** — row_id · company_name_raw · company_name_clean · domain · country · geo_bucket · city · industry
2. **Stop-filters** — filter_geo · filter_size · filter_anti_icp · filter_result
3. **Headcount** — emp_enriched · emp_final · tier
4. **Fit** — fit_icp · fit_services · fit_score · fit_gate
5. **Signal** — signal_type · signal_score · signal_route · signal_evidence_url · signal_date · signal_age_days · signal_summary · signal_2_type · signal_2_url
6. **Data point** — datapoint_type · datapoint_detail
7. **Evidence of current work** — client-specific (permits, tenders, vacancies)
8. **Source control** — match_method · channel_route · exclusion_reason · source_track
9. **Site** — site_status · site_sectors · then client specifics (equipment, software, volumes, in-house team)
10. **Contact** — person_first_name · person_last_name · person_title · person_linkedin · person_email · email_status
11. **Text** — angle · observation · guess · question · opener_style · text_gate · text_gate_reason · hook_source · hook_date
12. **Segmentation** — persona_role · campaign · contacts_at_company · persona_gap

Blocks 7 and 9 change per client. The rest holds.

`signal_summary` is written so it can be lifted into a first line unchanged: concrete object, place,
date. "Five open coordinator roles across two metros, live on 5 Aug" — not "growing fast".

`text_gate = ok` only when real evidence sits under the first line; otherwise `review` plus a reason.
`hook_source` is mandatory — without it the row does not get sent.

## Volume gates

- A signal-led campaign needs **300+ rows** to produce readable statistics.
- A data-point-led campaign needs **500+**.

Below that, report it. A base that cannot fill a campaign is a finding about the base, not something
to hide behind a nicely formatted file.

## Traps already paid for

Detection traps (careers pages, aggregators, stale postings, `/partners` pages that mean the
opposite) live with `signal-research`, which does that work. What bites in *this* skill is the data
handling:

- Text date columns in two formats make `max()` and descending sorts return a date from years ago.
  Filter on a literal recent value instead.
- Cost columns stored as text — cast before comparing, or the query silently returns nothing.
- Placeholder dates (9999, 3030) sit in "due" / "end" / "final" columns.
- Parallel threads against a scraping API produce DNS errors; retry with backoff, and pick up
  already-running jobs by run id instead of restarting them.
- A crawler with no per-site page cap will spend the whole budget on one large site — batch the
  domains instead of capping nothing.
- Two sources for the same figure (a page count vs a stated range) must stay in two columns. Merged,
  you can no longer tell a verified number from an inferred one.

## What this skill does not do

Write sequences · send anything · score people (it works at the account level) · invent a signal
because an account looks important · delete rows that failed.
