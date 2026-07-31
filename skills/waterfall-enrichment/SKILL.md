---
name: waterfall-enrichment
description: Use when asked to find emails for a contact list, run email enrichment, or maximize email find rate through multiple sources
---

# Waterfall Enrichment

Find verified emails for a contact list by running multiple data sources in sequence — stopping when a verified email is found. Maximizes find rate while keeping quality high.

## What you need

- Contact list with: name, company domain, role (LinkedIn URL helps)
- Access to enrichment tools (Clay waterfall, Apollo, GetProspect, Hunter, or equivalent)

## Waterfall sequence (in order)

Run each source and stop for that contact when a verified result is returned:

1. **Clay waterfall** (if Clay MCP is available) — covers 75+ sources simultaneously, best coverage
2. **Apollo** — strong for US tech companies
3. **GetProspect** — strong for LinkedIn-based finding
4. **Hunter.io** — strong for pattern-based guessing on company domains
5. **Manual LinkedIn pattern** — if domain email pattern is known (e.g., firstname@company.com), apply pattern and validate

## Process

1. For each contact without a verified email, start at source 1
2. Move to next source only if previous returned no result or returned "risky/unknown"
3. Accept emails marked as "valid" — reject "risky", "catch-all", or "unknown"
4. For catch-all domains: flag them separately — they can be sent to but with lower confidence
5. Run ZeroBounce validation on all results before finalizing
6. Return enriched list with source attribution and confidence level

## Output format

```
Waterfall enrichment: [list name]
Date: [date]
Contacts processed: [n]

RESULTS
Verified emails found: [n] ([%])
Catch-all (sendable, lower confidence): [n] ([%])
Not found: [n] ([%])

SOURCE BREAKDOWN
Clay: [n] found
Apollo: [n] found
GetProspect: [n] found
Hunter: [n] found
Pattern: [n] found

VALIDATION
ZeroBounce valid: [n]
ZeroBounce risky/invalid: [n] — removed

Final clean list: [n] contacts ready for sequencing
```

## Notes

- Never send to unvalidated emails — even 5% invalid rate can damage sender reputation
- Catch-all emails: send in small batches first to test deliverability on that domain
- If find rate is below 50%, check if contact names or domains are malformed in the input list
- Prioritize finding emails for Tier 1 contacts first — don't spend enrichment budget on Tier 3
