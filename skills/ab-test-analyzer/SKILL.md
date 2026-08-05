---
name: ab-test-analyzer
description: Use when asked to compare two campaign variants, determine a winner, or analyze the results of a split test
---

# A/B Test Analyzer

Compare two campaign variants, determine statistical significance, declare a winner, and recommend the next test.

## What you need

- Variant A metrics: sends, opens, replies, interested replies
- Variant B metrics: same
- What was different between the variants (the variable being tested)
- Minimum 50 sends per variant for analysis

## Metrics hierarchy

Analyze in this order — each layer tells you something different:

1. **Open rate**: subject line or sender name problem
2. **Reply rate**: copy or targeting problem
3. **Interest rate**: offer or angle problem
4. **Meeting booked rate**: CTA or qualification problem

A test is only conclusive for the layer where the variants diverged. Don't attribute an interest rate difference to the subject line.

## Statistical significance guide

- Under 50 sends per variant: inconclusive — note it, don't act on it
- 50–100 sends per variant: directional — treat as signal, not proof
- 100+ sends per variant: statistically meaningful — act on this

## Process

1. Calculate all four rates for both variants
2. Identify at which layer the variants diverged
3. Determine statistical significance based on send volume
4. Declare winner (or "inconclusive" if under threshold)
5. Recommend what to test next — don't just repeat the same test

## Output format

```
A/B test: [what was tested]
Date: [date]

VARIANT A — [description of variant]
Sends: [n] | Opens: [n] ([%]) | Replies: [n] ([%]) | Interested: [n] ([%])

VARIANT B — [description of variant]
Sends: [n] | Opens: [n] ([%]) | Replies: [n] ([%]) | Interested: [n] ([%])

ANALYSIS
Divergence layer: [opens / replies / interest / meetings]
Delta: [A vs B difference at divergence layer]
Statistical significance: [Conclusive / Directional / Inconclusive] — [reason]

WINNER: [Variant A / Variant B / Inconclusive]
Why: [one-line explanation]

NEXT TEST
Variable to test next: [what to change]
Hypothesis: [what you expect to happen and why]
```

## Notes

- Only test one variable at a time — if you change subject line AND copy, you can't attribute the result
- Don't declare winners on open rate alone — open rate can be gamed by subject line tricks that don't convert
- If both variants are in Kill territory (under 17% interest rate), the problem is the hypothesis, not the variant
- Document every test result — patterns across tests are more valuable than any single test
