---
name: campaign-tiering
description: Use when asked to review running campaigns, decide what to scale vs. kill, or sort active hypotheses by performance
---

# Campaign Tiering

Review all running campaigns and sort them into three tiers — scale, optimize, or kill — based on performance data. Do not keep running what isn't working.

## What you need

- Campaign performance data (reply rate, interest rate, open rate)
- List of active campaigns with hypothesis names
- Number of contacts sent per campaign (need minimum 50 sends to tier)

## Performance thresholds

**Tier 1 — Scale**: Interest rate above 30%
→ Add LinkedIn as a second channel. Increase send volume. Expand the contact list.

**Tier 2 — Optimize**: Interest rate 17–30%
→ Tweak copywriting. Adjust CTA. Try a new subject line variant. Don't kill yet.

**Kill — Under 17% interest rate** (or under 1% reply rate)
→ Pause immediately. Do not add more contacts. Document what failed and why.

**Interest rate definition**: % of replies that expressed genuine interest in continuing the conversation (not out of office, not unsubscribe, not "not interested").

## Process

1. Pull campaign metrics via MCP from the sending platform
2. Filter out campaigns with under 50 sends — not enough data to tier
3. Calculate interest rate for each campaign: (interested replies / total replies) × 100
4. Assign tier per thresholds above
5. For Tier 1: suggest specific scale actions
6. For Tier 2: suggest one specific optimization to test
7. For Kill: identify the most likely root cause (targeting, copy, angle, or signal)

## Output format

```
Campaign tiering review: [date]
Campaigns evaluated: [n] | Excluded (under 50 sends): [n]

TIER 1 — SCALE ([n] campaigns)
[Campaign name] | Sends: [n] | Reply rate: [n%] | Interest rate: [n%]
→ Scale action: [add LinkedIn / expand list / increase volume]

TIER 2 — OPTIMIZE ([n] campaigns)
[Campaign name] | Sends: [n] | Reply rate: [n%] | Interest rate: [n%]
→ Optimize: [specific suggestion]

KILL ([n] campaigns)
[Campaign name] | Sends: [n] | Reply rate: [n%] | Interest rate: [n%]
→ Root cause: [targeting / copy / angle / signal quality]

SUMMARY
Campaigns to scale: [n] | To optimize: [n] | To kill: [n]
Recommended next step: [one action]
```

## Notes

- Run tiering weekly — campaigns that looked promising at 20 sends may fail at 100
- Killing campaigns is good news: you freed budget and attention for what's working
- If everything is in Tier 2 or Kill, the problem is usually the signal strategy, not the copy
- Never move a campaign from Kill back to active without changing the hypothesis — same campaign, same result
- Campaigns with high open rate but low reply rate = copy problem. Low open rate = subject line or deliverability problem.
