---
name: signal-detection
description: Use when asked to find hiring signals, growth signals, or buying triggers for a list of companies from Clay or LinkedIn
---

# Signal Detection

Scan a company list for active signals that indicate a buying trigger is present right now.

## What you need

- A list of companies (Clay export, CSV, or pasted list)
- Signal type to look for (hiring, funding, expansion, tool change, leadership change)
- ICP context so signals can be filtered for relevance

## Signal types

**Hiring signals**: open roles matching target persona or team build-out (e.g., "first SDR hire", "Head of RevOps", "VP Sales")

**Growth signals**: recent funding, headcount growth >20% in 6 months, new office, product launch

**Tool change signals**: job descriptions mentioning specific tools, G2 review activity, tech stack changes

**Leadership signals**: new CRO/VP Sales/CMO in last 90 days — new leaders buy new things

## Process

1. For each company in the list, query Clay via MCP for enrichment data
2. Cross-reference LinkedIn via MCP for open roles and recent activity
3. Score signal strength: Strong (active, specific, recent) / Weak (indirect, older) / None
4. Filter out companies with no signal
5. Return scored list sorted by signal strength

## Output format

```
Signal scan: [date] — [N companies scanned]

STRONG SIGNALS ([n])
- [Company] | [Signal type] | [Specific evidence] | Tier 1
- ...

WEAK SIGNALS ([n])
- [Company] | [Signal type] | [Specific evidence] | Tier 2
- ...

NO SIGNAL ([n]) — removed from list

Recommended next step: [run ICP validation on Tier 1 / push Tier 1 to sequence]
```

## Notes

- If Clay MCP is unavailable, flag it and use LinkedIn + public sources only
- Recency matters: signals older than 90 days are weak by default
- Hiring signals for the exact target role = strongest possible signal
