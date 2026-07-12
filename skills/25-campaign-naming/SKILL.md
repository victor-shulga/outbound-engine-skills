---
name: campaign-naming
description: Use when asked to name campaigns, generate a naming convention, or organize a hypothesis matrix into readable campaign names
---

# Campaign Naming

Generate consistent, readable campaign names from a hypothesis matrix — so a list of 40 campaigns is scannable in 5 seconds.

## What you need

- Hypothesis matrix (from hypothesis-builder) or list of campaign parameters
- Platform the campaigns will run in (PlusVibe, Instantly, etc.)

## Naming convention

Format: `[Signal]-[Persona]-[Angle]-[Channel]`

Examples:
- `SDRHire-VPSales-Pipeline-Email`
- `NewCRO-Founder-90Days-LinkedIn`
- `FundingRound-HeadOfSales-Scale-Multi`
- `TechStackChange-RevOps-Migration-Email`

Rules:
- No spaces — use CamelCase or hyphens
- No generic labels: "Q2 Campaign", "Test 1", "Outbound April" are all banned
- Maximum 5 components — if you need more, the hypothesis is too complex
- Channel suffix is optional but recommended when running multi-channel
- Date prefix optional for recurring campaigns: `2026Q2-SDRHire-VPSales-Pipeline-Email`

## Why this matters

When you have 40 campaigns running in parallel, you need to read the name and instantly know:
- Who you're targeting (persona)
- Why you're reaching out now (signal)
- What you're arguing (angle)
- Which channel

A campaign named "Outbound Test 3" tells you nothing. `SDRHire-VPSales-Pipeline-Email` tells you everything.

## Process

1. Take the hypothesis matrix or list of campaigns
2. Extract: signal, persona, angle for each
3. Generate name in convention format
4. Check for duplicates — if two campaigns have the same name, the hypotheses are too similar
5. Return full named list

## Output format

```
Campaign names: [ICP / vertical]
Total: [n]

[Original hypothesis description] → [Campaign name]
...

Naming conflicts (same name, different hypothesis): [list — needs resolution]
```

## Notes

- Naming is infrastructure — do it before setting up campaigns, not after
- Rename any existing campaigns that don't follow this convention before the next review
- If your platform has character limits, abbreviate signal and angle but keep persona readable
- Add the campaign name as the first tag in your CRM contact record — it's the fastest way to trace where a lead came from
