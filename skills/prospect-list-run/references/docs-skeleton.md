# The four documents of a run

Write them as Notion pages when a Notion connector is available (one parent page, three children).
Without Notion, write four markdown files next to the CSVs in the work directory:
`00-main.md`, `01-icp-personas.md`, `02-signal-catalog.md`, `03-segments-campaigns.md`.
Write them in the language the client reads. Every number comes from the run's console output or the CSVs.

## 00 · Main page (fixed skeleton, 11 sections in this order)

1. Working file as a link **in the first line**, plus how to filter it (band, campaign, text_gate)
2. Navigation to the three child documents
3. Status now: table of campaigns with row counts and how many rows have `text_gate = ok`
4. The main takeaway, plus a before/after table (raw list vs working sample)
5. Where the data came from: source, volume, what each step produced, what it cost
6. Three findings that change how the list should be worked
7. Segments: link to the child page and the short logic
8. How to read the file: block, columns, why each block exists
9. What stayed closed and why (missing data, signals not covered, sources that failed)
10. What to do next: numbered list
11. The one main recommendation

## 01 · ICP and personas

Tiers, firmographics, decision maker and champion per tier, anti-ICP, stop filters (the same reasons
the config uses). Unknowns are written as "to confirm on discovery", never invented.

## 02 · Signal catalog

Signal families, then one row per code: how to detect it, what counts as evidence, shelf life
(window in days), points, first-touch play. A separate block of anti-signals that disqualify.
Codes here and in `signals.points` of the config must match one to one. Codes that need a source
you do not have yet stay in the catalog marked "source needed", so nobody re-invents them later.

## 03 · Segments and campaigns

Queues, personas, message skeleton (observation -> guess -> fixed offer paragraph -> one question),
text rules, spacing between contacts at one company.

## Canonical list: 12 blocks

The order never changes. Blocks 7 and 9 adapt to the client; the rest are identical for every client.

| # | Block | Main columns |
|---|---|---|
| 1 | Company | company_name_raw/clean, domain, country, geo_bucket, city, industry |
| 2 | Stop filters | filter_geo, filter_size, filter_anti_icp, filter_result |
| 3 | Headcount | emp_enriched, emp_final, tier |
| 4 | Fit | fit_icp, fit_services, fit_score (30, gate 20), lead_score, lead_score_100, band, confidence, missing_fields |
| 5 | Signal | signal_type, signal_name, signal_score, signal_route, evidence URL, date, age, window, summary, 2nd/3rd signal |
| 6 | Data point | datapoint_type, datapoint_detail |
| 7 | Proof of current work (client-specific) | capacity_in_house, jobs_open, jobs_role, jobs_source |
| 8 | Source control | match_method, channel_route, exclusion_reason, source_track |
| 9 | Website (client-specific) | site_status, site_cms, site_builders, site_own_stack, site_pages, site_flags |
| 10 | Contact | first/last name, title, LinkedIn, e-mail, email_status, company_linkedin |
| 11 | Text | language, angle, observation, guess, question, opener_style, text_gate, text_gate_reason, hook_source, hook_date |
| 12 | Segmentation | persona_role, campaign, contacts_at_company, persona_gap |
