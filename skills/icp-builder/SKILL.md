---
name: icp-builder
description: Use when asked to build an ICP from scratch, define the ideal customer profile, or structure ICP documentation for use across skills
---

# ICP Builder

Build a structured ICP definition from existing knowledge, call recordings, and win/loss data. Output a reusable ICP file that all other skills can reference.

## What you need

- Any of the following (provide as much as you have):
  - Description of your best current customers
  - Sales call recordings or transcripts
  - Win/loss notes
  - Industry intuition about who benefits most
- What problem you solve and for whom

## Process

1. Ask 8 calibration questions if inputs are thin:
   - Who are your 3 best customers right now — what do they have in common?
   - Who do you lose deals to most often, and why?
   - What does the prospect say in the first call that makes you think "this is perfect"?
   - What's the typical team size/structure that gets value fastest?
   - What signals tell you a company needs you right now vs. in 6 months?
   - What roles are involved in the buying decision?
   - What is the one sentence your best customer would use to describe your value?
   - What type of company is a waste of time, even if they match on paper?
2. Synthesize answers into structured ICP dimensions
3. Add negative ICP criteria (disqualifiers)
4. Output as a reusable markdown ICP file

## Output format

```
# ICP Definition: [Company Name]
Last updated: [date]

## Firmographic fit
- Industry: [list]
- Company size: [headcount range]
- Revenue stage: [e.g., Series A–C / $5M–$50M ARR]
- Geography: [list]
- Business model: [B2B SaaS / Agency / Services / etc.]

## Technographic fit
- Uses: [tools that indicate fit]
- Likely stack: [CRM, outbound tools, etc.]

## Persona fit
- Primary: [role] — [why this person buys]
- Secondary: [role] — [influence/blocker context]

## Situational fit (when they need you NOW)
- [Signal 1]
- [Signal 2]
- [Signal 3]
Signals RANK accounts, they never filter them: an account that passes the rings and has no signal stays on the list with an empty signal set and a lower priority.

## What you sell (context, not a filter)
"[One line: the offer and who buys it]" — used only to judge competitors: a company that sells this, or anything in the same category to the same buyer, is a competitor, not a lead.

## Negative ICP — four rings, checked in this order
1. **Ring 1 · Business model**: [product-only / marketplace / other models that do not buy this]
2. **Ring 2 · Competitors**: [who sells the same thing, or the same category, to the same buyer]
3. **Ring 3 · Size and geo**: [headcount floor, e.g. under 11 people; markets you do not serve]
4. **Ring 4 · Already ours**: existing clients, former clients, partners, your own peers and vendors — pulled from the CRM, never from memory
Every rejected account carries its ring number and a one-line reason. Rejected accounts are not a reserve to revisit later.

## One-sentence value for this ICP
"[What you do] for [who] so they can [outcome]."
```

## Notes

- This file is the input to icp-validation, signal-research, hypothesis-builder, and sequence-writer
- Revisit after every 20 closed deals — ICPs drift
- Negative ICP criteria are as important as positive ones — include them, ring by ring; ring 4 (already ours) is the one every tool without CRM access misses
- If call recordings are available, extract language the prospect used and include it verbatim under situational fit
