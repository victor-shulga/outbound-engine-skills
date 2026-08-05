---
name: deliverability-audit
description: Use when asked to check email deliverability, audit sending infrastructure, investigate spam issues, or set up domains and mailboxes correctly
---

# Deliverability Audit

Audit the sending infrastructure and return a pass/fail verdict on every deliverability dimension — with specific fixes for anything that fails.

## What you need

- Sending domain(s) and mailbox addresses
- Sending platform being used
- Current send volume per mailbox per day
- How long the domains/mailboxes have been active

## Audit checklist

**Domain setup**
- [ ] SPF record configured correctly
- [ ] DKIM record configured and active
- [ ] DMARC policy set (minimum `p=none` with monitoring; `p=quarantine` recommended)
- [ ] MX records pointing to the correct mail server
- [ ] Domain is not on any major blacklists (MXToolbox check)

**Mailbox setup**
- [ ] Mailbox has a real name (not "info@" or "sales@")
- [ ] Profile photo set (where platform allows)
- [ ] Email signature includes real name, role, and website
- [ ] Mailbox is at least 14 days old before first campaign send
- [ ] Warm-up is active (if platform supports it)

**Sending behavior**
- [ ] Max sends per mailbox: 30–40/day for new mailboxes, up to 50/day for established
- [ ] Send window: business hours in recipient timezone (8am–6pm)
- [ ] Sending days: Monday–Thursday only for cold outbound
- [ ] Minimum delay between sends: 3–5 minutes
- [ ] Unsubscribe link present in every email

**Warm-up status**
- [ ] Warm-up tool active (Instantly, Mailreach, or equivalent)
- [ ] Minimum 14-day warm-up before sending cold campaigns
- [ ] Warm-up volume: at least 30–50 warm-up emails per day per mailbox
- [ ] Inbox placement rate above 90% on warm-up reports

## Process

1. Request domain and mailbox details
2. Check DNS records via MXToolbox or equivalent
3. Check blacklist status for all sending domains
4. Review sending platform settings against checklist
5. Assign pass/fail to each dimension
6. Return remediation list for any failures, ordered by severity

## Output format

```
Deliverability audit: [domain(s)]
Date: [date]

DOMAIN SETUP
SPF: [PASS / FAIL] — [detail]
DKIM: [PASS / FAIL] — [detail]
DMARC: [PASS / FAIL] — [detail]
Blacklist status: [CLEAN / LISTED] — [which lists if any]

MAILBOX SETUP
[mailbox@domain] — [pass count]/[total checks] — [list of failures]

SENDING BEHAVIOR
Daily volume: [SAFE / HIGH / CRITICAL]
Send window: [PASS / FAIL]
Warm-up: [ACTIVE / INACTIVE / NOT CONFIGURED]

VERDICT
Infrastructure ready to send: [YES / NO / WITH FIXES]

REMEDIATION (ordered by severity)
1. [Critical fix — do immediately]
2. [Important fix — do this week]
3. [Nice to have — do when time permits]
```

## Notes

- Do not start cold sending until SPF, DKIM, and DMARC all pass — deliverability problems compound fast
- Blacklisted domain = stop all sending immediately and investigate the cause before delisting
- 30 emails/day per mailbox is conservative and safe; 50 is the ceiling — never go higher on cold outbound
- Warm-up should never be turned off during active campaigns — even pausing for a few days can drop inbox rate
- Use separate domains for cold outbound — never send cold email from your main company domain
