---
name: niche-data-finder
description: >-
  Finds 3-5 complementary, non-generic public data sources where the target ACCOUNTS of one niche
  can be listed together with a buying signal: association and member directories, licence and
  certification registries, public tenders and procurement portals, event exhibitor lists,
  marketplaces and review directories, job boards and ATS feeds, permit and planning databases
  (AEC), tech-stack lookups. Every source is scored on freshness, coverage, signal strength and
  extraction effort, checked live, and handed over with an extraction plan. Use when asked "where do I find companies that...",
  "data sources for [niche]", "how do I build a list of [segment]", "alternatives to LinkedIn /
  Apollo for this ICP", "де взяти базу під цю нішу", "звідки брати компанії з сигналом",
  "джерела даних для сегмента". NOT for contact-level data or email finding, and NOT for
  building the list itself (data-research, account-sourcing).
---

# Niche Data Finder

Generic B2B databases list everyone and tell you nothing about timing. The accounts worth a first
message usually sit in a narrower place: a registry they had to join, a tender they bid on, a
booth they paid for, a job they posted, a permit they filed. This skill finds those places for one
niche and proves they are usable before anyone spends a day scraping them.

The output is a short, scored shortlist of 3-5 sources that cover each other's blind spots, with a
concrete way to pull each one. Answer in the user's language.

## Where it sits

```
signal-catalog / signal-research   →   niche-data-finder   →   data-research / account-sourcing
(which signals matter for the ICP)     (where accounts +        (pull, filter, score the list)
                                        signals can be listed)
```

Also used by the gtm-strategy pack: `03-market-icp-persona` (where the ICP is visible),
`04-market-sizing` (which sources give a countable universe) and `11-channels-plan` (which channels
the data supports).

## Inputs (ask once, in one message, only what is missing)

1. **Offer**: what the user sells, in one sentence, and the outcome it delivers.
2. **Account definition**: industry or sub-niche, geography, size band, any must-have trait
   (certified, licensed, uses a given tool, works on public projects).
3. **The buying signal**: what an account does or shows right before it needs the offer. If the user
   has a signal catalog (`signal-catalog`), take the top 3-5 signals from it.
4. **Constraints**: budget for paid data, tools available (scraper, Firecrawl, Apify, Clay, a
   spreadsheet only), and how many accounts per month the outreach can actually absorb.

If no signal is known, propose 2-3 likely ones for the niche, mark them as assumptions and continue.

## Step 1: Translate the ICP into "listable" facts

A source is only useful if the fact you need is written down somewhere public. Rewrite the ICP as
facts a third party would record:

| ICP wording | Listable fact | Who records it |
|---|---|---|
| "established engineering firm" | holds a professional licence or ISO certificate | licensing board, certification body |
| "sells to the public sector" | won or bid on a public contract | procurement portal |
| "growing delivery team" | has open roles for the relevant function | job board, company ATS page |
| "active in this market" | exhibits or speaks at the sector's main event | event exhibitor / sponsor list |
| "about to start a building project" | filed a permit or planning application | city / county permit data, planning portal |
| "runs on tool X" | site or store shows tool X | tech-stack lookup, partner directory |

Facts that nobody records (internal pains, budget) are signals for the copy, not for sourcing.

## Step 2: Long list of 10-15 candidates

Pull candidates from at least five of the source families in `references/source-families.md`.
For each candidate write one line: name, URL, what it lists, which signal it carries. Prefer
sources that are specific to the niche over horizontal databases; a horizontal database may stay
on the long list only as a coverage baseline.

Search tactics that work for obscure niches:
- `"member directory" <niche> <country>`, `"find a member" <association>`, `"certified" <standard> "search"`
- the sector's two biggest annual events, then their exhibitor and sponsor pages
- the national procurement portal plus one regional one, searched by CPV / NAICS / UNSPSC code
- marketplaces where the buyers themselves post work (for a service company: where its clients hire)

## Step 3: Score every candidate on four axes (1-5 each)

| Axis | 5 | 3 | 1 |
|---|---|---|---|
| **Freshness** | updated daily or weekly, records carry dates | monthly or quarterly | yearly, undated, or last update over 12 months ago |
| **Coverage** | most ICP accounts in the geo appear, and over half of listed entries fit the ICP | a meaningful slice, or a broad list with 20-50% fit | a handful of accounts, or under 20% fit |
| **Signal strength** | the entry itself is a timing event (tender published, permit filed, role opened) | a fit trait that changes slowly (certified, member, exhibitor this year) | static presence only, no timing |
| **Extraction effort / cost** (5 = easiest) | public, structured, export or API, free | public HTML, paginated, scrapeable with a standard tool | login, captcha, paid seat, PDF-only, or terms that forbid scraping |

Total out of 20. Rules on top of the total:
- Freshness 1 = drop, unless the source is used only as a static base layer and something else on
  the shortlist carries the timing.
- Extraction 1 = keep only if signal strength is 5 and nothing else carries that signal; at most one
  such source on the shortlist.
- Respect the source's terms of use and robots rules. If extraction needs a login you do not have,
  say so; never suggest bypassing access controls.

## Step 4: Verify before recommending

Scores from memory are guesses. For every source that makes the shortlist:
1. Open the live URL. Confirm it loads and lists companies (not people only).
2. Find the newest record and its date. If the page shows no dates, check two or three entries for
   recent activity and say the freshness is inferred.
3. Sample 15-20 entries and count how many fit the ICP. That is the qualification rate.
4. Note the access method that actually worked (export button, API, plain HTML, JS-rendered).

Mark each source **verified** (all four checks done) or **not checked** (with the reason). An
unchecked score is an estimate, and the output labels it that way.

## Step 5: Choose 3-5 that complement each other

- At least one **base** source (high coverage, fit trait) and at least one **timing** source (signal
  strength 4-5).
- No two sources from the same family unless they carry different signals.
- At least two sources with extraction score 4-5, so the first list can be built this week.
- Overlap is useful: an account that appears in two sources (licensed AND hiring) is a stronger lead
  than either alone. Name the join key (normally the company domain).

## Step 6: Extraction plan per source

For each shortlisted source give:
- **Access**: URL, login or not, cost.
- **Method**: CSV export, API, scraper (Firecrawl, Apify actor, a short script), or manual copy for
  tiny lists. If a public Apify actor or API exists, name it as an option and say it is unverified
  until run.
- **Fields to capture**: company name, website / domain, country / region, the signal, signal date,
  evidence URL. Domain is the dedupe key; when the source has no domain, plan a domain lookup step.
- **Filters**: which fields cut the non-ICP rows before enrichment.
- **Refresh cadence**: how often to re-pull so the signal stays alive (weekly for tenders and jobs,
  monthly for permits, quarterly for directories).
- **Expected yield**: accounts per pull, labelled as an estimate with the sample it came from.

## Output format

```
# Data sources for <niche>, <geo>

Signal(s) targeted: ...
Assumptions: ...

## 1. <Source name> (<family>), score XX/20, verified | not checked
What it lists: ...
Signal it carries: ...
Freshness / coverage / signal / effort: x / x / x / x (one line of evidence each)
Qualification rate: ~N of 20 sampled fit the ICP
Extraction: access · method · fields · filters · refresh · expected yield

## 2. ...

## How they work together
Base layer: ... Timing layer: ... Overlap rule: accounts in both A and C go first.

## Start order
1. <source> this week, because ...
2. <source> next, because ...
3. <source> once the first list is through outreach.

## Rejected candidates
<name>: reason (stale / low fit / blocked / duplicate signal)
```

Keep the rejected list short; it shows the user what was considered and saves them a second search.

## Quality bar

- 3-5 sources, each from a different angle, at least one carrying timing.
- Every score has one line of evidence; every shortlisted source is verified or marked "not checked".
- No contact-level sources (email finders, people databases) on the shortlist.
- No source that requires breaking its terms of use.
- Yields and qualification rates come from a sample, never invented.

## Hand-off

- If installed, `data-research` (pack outbound-engine-skills) turns the pulled rows into a scored,
  evidenced list; `account-sourcing` handles the job-posting source end to end.
- `signal-research` re-scans the resulting base when signals expire; `waterfall-enrichment` adds
  contacts once accounts are chosen.
- `04-market-sizing` (pack gtm-strategy-skills) can use the base-layer counts as a bottom-up
  universe estimate.

## Credits

Idea adapted from a public outbound-skills collection; rewritten for B2B
service companies. Author of this version: Victor Shulga (victorshulga.com).
