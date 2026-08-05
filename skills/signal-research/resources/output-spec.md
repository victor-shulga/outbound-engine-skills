# Output spec — signal block columns

Flat CSV. One header row. No grouped headers, no formulas, everything computed and written as a
value. Two files with IDENTICAL columns:

- `<client>_signal_research_full.csv` — the whole base including drops, each with a reason
- `<client>_signal_research_working.csv` — the slice going into outreach

The signal block below slots into the canonical prospect-list column order (company → stop-filters
→ headcount → fit → **signal** → data point → evidence → source control → site → contact → copy →
segmentation). Keep the surrounding blocks the base already has; this skill owns the signal and
data-point blocks plus the freshness columns.

## Columns

| Column | Values | Rule |
|---|---|---|
| `signal_type` | signal id or short slug from the client's signal table (`hiring_bim`, `award_new_project`, `acquisition`, `permit_filed`, `leadership_change`, …) or `none` | Never invent a slug outside the client's table. Extend the table first. |
| `signal_tier` | `T1` · `T2` · `T3` · empty | From the client's tier table, not from how impressive it feels. |
| `signal_score` | integer | Per the scoring formula, after recency multiplier and stacking. |
| `signal_route` | source that found it: `open_data:<dataset>`, `careers_page`, `web_search`, `press:<feed>`, `platform:<tool>` | Needed for the source-yield ranking in the report. |
| `signal_evidence_url` | one live URL | Mandatory whenever `signal_type ≠ none`. No URL → the row is `none`. |
| `signal_date` | `YYYY-MM-DD` | Date of the EVENT, not of the run. |
| `signal_date_precision` | `exact` · `approx` · `unknown` | `approx` when derived from "posted 3 weeks ago". `unknown` blocks T1 treatment. |
| `signal_age_days` | integer | run_date − signal_date. |
| `signal_summary` | ≤ 140 chars, factual | What happened, in the words the copy step can reuse. No adjectives, no inference. |
| `signal_2_type` / `signal_2_url` | as above | Only if independent of signal 1 (different event, different source). |
| `signal_3_type` | as above | Third signal, type only. |
| `signal_expires_on` | `YYYY-MM-DD` | signal_date + window for that tier. |
| `rescan_due` | `YYYY-MM-DD` | min(signal_expires_on, run_date + 30d). |
| `status` | `live` · `burnt` · `never_fired` · `dropped` | `burnt` = detected before, past its window. |
| `datapoint_type` / `datapoint_detail` | static fact slug + detail | Where the message gets its adaptation. Expired signals move here. |
| `match_method` | `domain` · `exact_name` · `fuzzy_name+city` · `manual` | How the source row was joined to the base row. |
| `detected_by` | `bulk` · `agent` · `platform` · `manual` | Which pass produced it. |
| `detected_on` | `YYYY-MM-DD` | Run date. Distinct from `signal_date`. |
| `heat` | `hot` · `warm` · `cool` · `drop` | From score thresholds. |
| `exclusion_reason` | text | Filled for every `filter_result = drop`. Empty for survivors. |

## Value rules

- Empty cell means "not researched". `none` means "researched, nothing found". They are different
  facts and the report needs both.
- One event = one signal. A press release about a hire and the job posting for that hire are one
  signal with two URLs — put the second in `signal_evidence_url` only if it adds proof, not in
  `signal_2_type`.
- `signal_summary` is written so the copy step can lift it into a first line without rewriting:
  concrete object, place, date. "Awarded the 240k sq ft hospital fit-out in Austin, June 2026" —
  not "growing fast in healthcare".
- Never fill a blank observation with a generic filler sentence. Blank is a valid state and it
  routes the row to a different campaign.
- Scores are integers; do not carry decimals from the recency multiplier — round half up.

## Delta-run additions

| Column | Purpose |
|---|---|
| `prev_signal_type` | what it was on the previous run |
| `prev_signal_date` | its date |
| `change` | `new` · `refired` · `burnt` · `unchanged` · `still_cold` |

`change` is what the delta report is built from. Ship the full file, but lead with the rows where
`change ≠ unchanged`.
