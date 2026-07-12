---
name: data-research
description: Use when asked to build a prospect list, find companies matching an ICP, or run the full data research workflow from scratch
---

# Data Research

Run the full multi-source data research workflow — from TAM identification to a clean, enriched, validated list of contacts ready for sequencing.

## What you need

- ICP definition (reference ICP file or provide inline)
- Target personas and roles
- Buyer signals to apply as filters
- Tools available (Apollo, Sales Navigator, Clay, Blitz API)
- Target list size

## Process

**Phase 1 — List building (multi-source)**
1. Query Apollo via MCP with ICP firmographic filters. Pull all matching companies.
2. Query Clay for the same filters as cross-reference.
3. If Sales Navigator is available, run a third parallel query.
4. Merge all three lists, deduplicate by company domain.

**Phase 2 — ICP validation**
5. For each company, run ICP validation (reference `icp-validation` skill) against their website.
6. Remove companies that fail ICP validation — do not send to them.
7. Flag borderline cases as Tier 2 for separate sequencing.

**Phase 3 — Signal enrichment**
8. Apply buyer signal filters using the `signal-detection` skill.
9. Tag each company with the relevant signal(s) present.
10. Sort companies: Tier 1 (ICP fit + signal) → Tier 2 (ICP fit, no signal) → remove non-fits.

**Phase 4 — Contact finding**
11. For Tier 1 companies: find decision-makers matching target personas via Clay/Apollo.
12. Run email waterfall enrichment (reference `waterfall-enrichment` skill).
13. Validate all emails before adding to list.

**Phase 5 — Output**
14. Produce two tables: company list + contact list with all enrichment data.

## Output format

```
Data research run: [ICP / hypothesis name]
Date: [date]

SUMMARY
Companies sourced: [n] (Apollo: [n] / Clay: [n] / Sales Nav: [n])
After dedup: [n]
After ICP validation: [n] kept / [n] removed
After signal filter: [n] Tier 1 / [n] Tier 2

TIER 1 CONTACTS — ready for sequencing
[Table: Company | Domain | Signal | Contact Name | Role | Email | LinkedIn URL]

TIER 2 CONTACTS — ICP fit, no active signal
[Table: same structure]

Data quality: [% with verified email] | [% with LinkedIn URL]
Next step: [push to campaign-architecture / run more enrichment]
```

## Notes

- Never skip ICP validation — raw Apollo lists are 30–40% off-ICP by default
- Phase 3 signal enrichment is what separates this list from a generic export
- If total Tier 1 is under 50 contacts, check whether signal filters are too narrow
- Do not combine Tier 1 and Tier 2 into the same campaign — they need different copy
