# Detection ladder — cheapest signal source first

Work top-down. Each rung is roughly an order of magnitude more expensive per account than the one
above it. Never buy what a free bulk query already answered.

| Rung | Source type | Covers | Cost per 100 accounts | Typical hit rate |
|---|---|---|---|---|
| 0 | The base itself (fields already present: employee count, tech, industry) | 100% | 0 | data points only |
| 1 | Bulk open data (permits, awards, licences, tenders, filings) | whole geo at once | 0 | 5–30% where geo is covered |
| 2 | Public feeds (industry press RSS, association news, award announcements) | vertical-wide | 0 | 2–8% |
| 3 | Company-owned pages (careers page, /news, /projects) via scrape | per account | ~0, slow | 10–25% |
| 4 | Web search per account (Serper / Claygent-style) | per account | low credits | 10–20% |
| 5 | Platform filters (job-posting databases, people databases, Sales Nav) | whole base, licensed | subscription | 15–35% |
| 6 | Paid signal / intent vendors | whole base | high subscription | varies, rarely worth it below enterprise budget |

Rungs 1–2 carry a well-designed run. If they carry nothing, the problem is usually the geo or the
signal choice — not the effort spent on rungs 3–5.

---

## Rung 1 — bulk open data

The highest-leverage rung and the one with the most traps.

**Query pattern:** one query per dataset per month-window, filter to commercial/relevant scope,
pull the firm-name field, then join back to the base.

**Before trusting a dataset, verify three things:**
1. **Does it carry a firm NAME?** Many public datasets are fully anonymised (parcel + value, no
   party names). Anonymous = useless for account matching, no matter how rich it looks.
2. **Is it actually current?** Check by filtering on a literal recent value (e.g. a
   `like '07/%/2026'` style filter), not by `max()` or a descending sort. Text date columns with
   two mixed formats make both of those return a date from years ago. Platform "last updated"
   metadata frequently reflects schema touches, not new rows.
3. **What is the real monthly volume?** A dataset with a decaying tail (150k rows in an old year,
   4k this year) is being replaced by a newer system; note the decay in the report.

**Field traps that cost hours:**
- Cost/value columns stored as TEXT → numeric comparison silently returns nothing; cast first.
- Placeholder dates (year 9999, 3030, 2230) in "due"/"end"/"final" columns → sort only on fields
  you have verified.
- Date field named differently from the obvious one (issued vs filed vs entered) — check which one
  moves.
- Residential/commercial or scope flags are often the cheapest built-in anti-ICP filter available.
- Government procurement APIs commonly rate-limit hard without an account role, and some geo-block;
  when an endpoint returns empty 404s on every path while the site loads in a browser, treat it as
  blocked and switch to an alternative rather than debugging the query.

**Legal stop:** if a portal exposes personal data (names, phones, emails of private individuals)
without authentication, do not use it. Record it as a legal stop in the report.

**Geo reality:** open-data coverage is per city/county, not per country. Expect a patchwork: a
couple of metros with a complete free pipeline including names, several with partial coverage, and
whole states where only paid sources work. Map coverage per `geo_bucket` before promising a run.

---

## Rung 2 — public feeds

Association news, industry press, award announcements, procurement bulletins.

- Verify each feed is alive before adding it to the plan; dead feeds keep returning HTTP 200 with
  stale items for years.
- Feeds give a name + a date + a URL — exactly the three fields a signal row needs. Their weakness
  is coverage skew toward large firms.

---

## Rung 3 — company-owned pages

- The careers page is the single most reliable trigger source for service verticals: an open role
  in the discipline you sell IS the buying signal, and it is public, dated and linkable.
- `/news`, `/projects`, `/case-studies` give both signals (new award) and data points (sectors,
  clients, size) in one fetch — capture both while you are there.
- Cache the fetch. Re-fetching the same site in a later pass is pure waste.

---

## Rung 4 — per-account web search

Batch into parallel research agents, 10–15 accounts each. Agent contract:

```
For each company return exactly:
company | signal_type | one-line evidence | URL | date (YYYY-MM-DD or approx) | confidence
If nothing verifiable is found, return signal_type = none. "none" is a correct answer.
Do not infer from the company being large, busy, or well-known.
```

Spot-check ~10% of returned URLs by opening them. Agents that cannot find a signal will invent a
credible one unless explicitly told `none` is acceptable — and the invented ones look best.

---

## Rung 5 — platform filters

Job-posting and people databases turn a per-account job into a whole-base filter. Map every planned
signal to a concrete filter (job title + posted-within, headcount change, title change within N
days) and note which signals have NO platform equivalent and therefore stay on rung 3–4 forever.

GDPR: person-level website de-anonymisation is US-only. For EU targets, company-level
identification only. Never hand an EU-targeting team a US-only person-level tool.

---

## Rung 6 — paid signal vendors

Enterprise intent platforms are priced far above an agency budget and mostly resolve to topic
surges that do not name an account you can call. Default verdict: out of scope; say so plainly
rather than including them in a plan the client will not buy.

---

## Matching back to the base

Signal sources name companies their own way. Join order:

1. `domain` — the only fully reliable key.
2. `exact_name` after normalisation (strip legal suffixes, punctuation, case, doubled spaces).
3. `fuzzy_name + city` — allowed, but flag it: `match_method = fuzzy_name+city`.
4. Manual resolution for high-value accounts only.

Always write `match_method`. When a run later produces a wrong-company outreach, that column is
the only thing that explains why.

Common false-positive sources: shared surnames in family-run firms, multi-entity groups with a
holding and several operating names, and franchise/branch names that differ only by city.
