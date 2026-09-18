---
name: icp-validation
description: Use when asked to validate a company against ICP criteria, score fit, or check if a company is worth targeting
---

# ICP Validation

Validate a company against defined ICP criteria and return a scored fit verdict.

## What you need

- Company name or website URL
- ICP definition (provide inline or reference your ICP file)

## Process

1. Pull the company's website and scan for: team size indicators, tech stack signals, product type, industry, and growth stage
2. Check LinkedIn via MCP for: headcount, recent hires, open roles, and leadership profile
3. Score fit against each ICP dimension (1-3 per dimension):
   - **Segment fit**: does the company match the target segment?
   - **Size fit**: does headcount/revenue match the ICP range?
   - **Signal fit**: is there an active reason they'd respond now?
   - **Role fit**: is the target persona present and reachable?
4. Return a one-line verdict + reasoning

## Output format

```
Company: [Name]
Fit score: [X/12]
Verdict: [Strong fit / Marginal fit / Not a fit]

Segment: [score] — [one line reason]
Size: [score] — [one line reason]
Signal: [score] — [one line reason]
Role: [score] — [one line reason]

Recommended action: [Tier 1 / Tier 2 / Skip]
```

## Notes

- If ICP isn't defined, ask for it before proceeding
- If LinkedIn data is unavailable via MCP, flag it and use public signals only
- "Marginal fit" means worth a Tier 2 sequence, not skip
