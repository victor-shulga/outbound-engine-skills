---
name: lead-scoring
description: Use when asked to score leads, prioritize a contact list, or rank prospects by likelihood to convert
---

# Lead Scoring

Score individual leads by combining ICP fit, signal strength, and persona authority — return a prioritized list for sequencing.

## What you need

- Contact list with company and role data
- ICP definition
- Signals detected (or run signal-detection first)
- Scoring weights (use defaults below or customize)

## Scoring model (default weights, adjust per ICP)

**ICP fit (max 40 points)**
- Industry match: 0 / 10 / 20 (no / partial / full)
- Size match: 0 / 10 / 20 (no / partial / full)

**Signal strength (max 40 points)**
- No signal: 0
- Weak/indirect signal: 10
- Clear signal, 60–90 days old: 20
- Strong signal, under 60 days: 30
- Multiple signals present: 40

**Persona authority (max 20 points)**
- Influencer only (e.g., manager): 5
- Strong influencer (e.g., Director): 10
- Decision-maker (e.g., VP, Head of): 15
- Economic buyer (e.g., CRO, CFO, CEO): 20

## Missing-data rule (never let a blank field score as average)

When a dimension has no/empty/unverified data, **cap it at 50% of its max** — do not default to the
midpoint. Blank = unknown, not "fine".
- no signal detected → signal strength capped at 20/40
- unknown industry or size → ICP fit capped at 20/40
- unknown role/seniority → persona authority capped at 10/20

State in the lead's line which dimensions were capped, so a low score from thin data is never confused
with a low score from a real bad fit (the former = enrich more; the latter = discard).

## Process

1. For each contact, score across three dimensions above
2. Calculate total score (max 100)
3. Assign tier:
   - **Tier 1**: 70–100 → priority sequence, send within 48 hours
   - **Tier 2**: 40–69 → standard sequence, send within 1 week
   - **Tier 3**: under 40 → hold or discard
4. Return scored list sorted by score descending

## Output format

```
Lead scoring: [hypothesis / list name]
Date: [date]
Contacts scored: [n]

TIER 1 — Send now ([n] contacts)
[Name] | [Company] | [Role] | Score: [n] | ICP: [n] | Signal: [n] | Persona: [n] | Signal detail: [what]

TIER 2 — Queue ([n] contacts)
[same format]

TIER 3 — Hold/discard ([n] contacts)
[summary count only — no need to list individually]

Average score: [n]
Top signal driving Tier 1: [signal name]
```

## Notes

- Scores are relative — if everything is 40–50, either the list is weak or weights need calibration
- A perfect ICP-fit company with zero signal is still only Tier 2 — signal is what makes it timely
- Re-score the same list after 60 days — signals expire and scores change
- If a contact is a clear economic buyer at a perfect ICP fit company, move them to Tier 1 regardless of signal — they're too valuable to wait
