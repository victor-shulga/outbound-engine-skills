---
name: hypothesis-builder
description: Use when asked to generate campaign hypotheses, build a testing matrix, or create a list of ideas to run from an ICP and signal set
---

# Hypothesis Builder

Take an ICP, a set of buyer personas, and a list of signals — generate a full testing matrix of campaign hypotheses to run.

## What you need

- ICP definition (industry, company size, geography)
- Target personas (2–5 roles you want to reach)
- Buyer signals available (hiring, funding, tool change, leadership change, etc.)
- Angles available (problem-based, time-based, social proof, competitive, etc.)

## Process

1. Map every combination of: persona × signal × angle
2. Remove combinations that are logically incoherent (e.g., "new CRO" signal sent to an SDR)
3. Group into clusters by similarity — don't list near-duplicates as separate hypotheses
4. Assign a priority score to each hypothesis (1–3) based on: signal specificity, persona authority, angle strength
5. Return the full matrix sorted by priority, with a one-line description of each

## Output format

```
Hypothesis matrix: [ICP name]
Generated: [date]
Total hypotheses: [n]

PRIORITY 1 — Highest expected performance
H01 | [Persona] | [Signal] | [Angle] | [One-line description]
H02 | ...

PRIORITY 2 — Worth testing
H03 | ...

PRIORITY 3 — Low conviction, test last
H08 | ...

Recommended starting set: [H01, H02, H04] — run these first
```

## Notes

- Aim for 20–50 hypotheses for a single ICP/vertical — too few means under-testing, too many means you lack focus
- Priority 1 hypotheses should have a specific, recent signal + a senior decision-maker persona
- If signals list is vague, ask for specific examples before generating
- The matrix is not a campaign list — it's a backlog. Only run what you can actually resource
