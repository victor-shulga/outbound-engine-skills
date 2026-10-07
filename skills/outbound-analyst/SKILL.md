---
name: outbound-analyst
description: >-
  Gives a straight verdict on outbound numbers per channel (email, LinkedIn, multichannel): accept
  rate, reply rate, positive reply rate, meeting rate, bounce, spam complaints, with opens treated
  as unreliable. Checks the denominators and the data traps first (fake "replied" fields,
  lifetime-only LinkedIn stats, samples too small to judge), compares each metric with a sourced
  benchmark table, names the root cause and gives 1-2 fixes with the skill that applies them.
  Full-audit mode reviews every campaign and channel with a scale / hold / stop / not tested
  verdict. Use when asked "is my reply rate good", "why no replies", "my accept rate is low", "is
  2% good for cold email", "analyze my campaign stats", "чи нормальний reply rate", "чому нема
  відповідей", "низький accept", "розбери цифри кампанії", "аудит аутбаунду", or before giving any
  opinion on an outreach metric. NOT for reading individual replies (reply-audit), NOT for the
  weekly client report (weekly-outreach-report).
---

# Outbound Analyst

Outreach numbers get two kinds of bad answers: "it depends" and a verdict built on the wrong
denominator. This skill gives a clear verdict, checks the data before judging it, explains the
cause, and points to the one or two moves that fix it. Answer in the user's language.

Benchmarks live in `references/benchmarks.md`. Read it before the first verdict in a session. Every
number there is tagged **[Public]** (published, with its source) or **[Practitioner]** (an operating
rule of thumb). Carry the tag into the answer.

## Modes

| Input | Mode | Output |
|---|---|---|
| one to three numbers, a question like "is X% good" | **Quick verdict** | verdict per metric, cause, 1-2 fixes |
| campaign exports, platform access, a dashboard, several campaigns or channels | **Full audit** | data check, funnel by channel, campaign table with verdicts, red flags, next-week plan |

Ask once, in one message, for what is missing: channel, contacts reached, time window, list source,
the offer, and whether open tracking is on. If the user only wants a fast read, give the verdict with
the assumptions stated.

## Step 1: Get the numbers right before judging them

Use these definitions. If the user's tool defines a metric differently, recompute or say so.

| Metric | Numerator | Denominator |
|---|---|---|
| Email reply rate | unique contacts who replied (excluding auto-replies and out-of-office) | contacts who received at least one email (bounces removed) |
| Positive reply rate | contacts who showed interest (asked for info, agreed to talk, referred internally to the right person) | same as above |
| Meeting rate | meetings booked | contacts reached; also show meetings ÷ positive replies |
| Bounce rate | hard bounces | emails sent |
| LinkedIn accept rate | accepted invites | invites sent at least 14 days ago (fresh invites are still pending) |
| LinkedIn reply rate | contacts who replied | accepted contacts who received a message |
| Multichannel reply rate | contacts who replied on any channel, counted once | contacts enrolled |

Data traps to check every time:

1. **"Replied" fields that lie.** In some multichannel and LinkedIn tools the built-in reply rate stays
   at 0 while real conversations exist, or counts auto-replies, or a CRM stage called "Replied" is
   filled by hand and lags. Count real replies from the conversations or inbox (or from the tool's
   per-flow reply events), not from a summary field or a pipeline stage.
2. **Lifetime-only statistics.** Several LinkedIn tools report campaign numbers since launch only. To
   get a week, take a snapshot of the counters every week at the same time and subtract the previous
   snapshot. A snapshot taken before the week ends understates it, so re-pull and correct last
   week's figure on the next run and say that you corrected it. Per-campaign lifetime counters can
   even go down when leads move between campaigns; if they do, judge the campaign on accept rate and
   remaining pool rather than on the reply delta, and check that the sum across senders equals the
   workspace total.
3. **Opens.** Machine opens (Apple Mail Privacy Protection) inflate them, and with tracking off they
   read 0. Opens never decide a verdict; at most they hint at inbox placement.
4. **Sample size.** Under 300 contacts reached, a hypothesis or segment is **not tested**, whatever its
   rate. Under 100, show counts ("3 of 80"), not percentages. A planned channel with no weekly
   number is **not launched**.
5. **Mixed windows.** Do not divide this week's replies by last month's sends. Replies lag sends by
   days; compare cohorts by send date when possible.

If a trap is present and cannot be fixed with the data at hand, say what it does to the verdict
("reply rate likely understated, real count needed") and continue.

## Step 2: Verdict per metric

For each metric: value with counts (n of N), band from `references/benchmarks.md`, the source tag, and
one sentence on what it means. Opens, if mentioned, go last with the reliability caveat.

```
Reply rate: 2.1% (21 of 1,000 delivered) · In line with plan [Practitioner: plan ~1.5%]
            · below the 3.43% public average [Public: Instantly benchmark report]
Verdict: normal for cold email in 2026; not the bottleneck.
```

## Step 3: Root cause

Walk the funnel top-down and stop at the first stage that breaks. A later stage cannot be judged
while an earlier one is broken.

| Pattern | Most likely cause | Check |
|---|---|---|
| Bounce over 5% | dirty or unverified list | re-verify a sample; look for typo domains and dead mailboxes that passed the verifier |
| Bounces cluster on certain recipient domains | recipients behind email security gateways rejecting the sender | DMARC still at `p=none` (move to `quarantine`, then `reject`), no live website on the sending domain, a crowd of lookalike sending domains, warm-up limit below daily send |
| Reply rate under 1% with healthy bounce | inbox placement or targeting | placement test or seed check; if placement is fine, the list has no reason to reply |
| Replies fine, positives low | offer or ICP mismatch; copy attracts curiosity without need | read the replies (`reply-audit`) |
| Positives fine, meetings low | slow or weak reply handling, a call ask too early, booking friction | time to first answer, the reply sent, the CTA |
| Meetings fine, call → paid under 15% | qualification or sales process, outside outbound | pipeline review |
| LinkedIn accept under 20% | wrong audience, weak profile, a selling note in the invite, exhausted list | remaining pool per campaign, invite note on or off, profile headline |
| Accept fine, reply after accept under 8% | first message too long or a pitch with no question | message length, the ending |
| Multichannel no better than single channel | channels hit the same people with the same message, or one channel is not live | per-channel launch status, cohort comparison |
| Everything dips at once in December, July-August or a conference week | seasonality | compare with the dip ranges in the benchmarks |

When two causes fit, name the one with the most evidence and say what would separate them.

## Step 4: 1-2 fixes

Each fix: what to change, which skill does it (if installed), the metric that will show it worked, and
when to re-check. Change one variable per test so the next read is clean.

## Full-audit mode

Run Steps 1-4 for every channel and campaign, then return:

1. **Data check**: sources pulled, traps found, corrections made, what is missing and why.
2. **Funnel by channel**: contacts → delivered / invites → accepts → replies → positive → meetings,
   each with counts and band.
3. **Campaign table**:

| Campaign | Channel | Contacts | Key rate (n/N) | Remaining pool | Verdict | Why |
|---|---|---|---|---|---|---|

   Verdicts: **scale** (above band, pool left), **hold** (in band, keep running), **stop** (below band
   with enough sample, or pool exhausted), **not tested** (under 300 contacts).
4. **Red flags**: deliverability, data quality, silent senders, channels planned but not launched.
5. **Next week**: the 1-2 fixes, owner, re-check date.

A section with no data stays in the output with "no data" and the reason.

## Hand-off

If installed (pack outbound-engine-skills):
- `reply-audit` reads the replies themselves when positives or meetings are the weak stage.
- `weekly-outreach-report` turns this analysis into the weekly client report.
- `deliverability-audit` checks DNS, warm-up and domains when bounce or placement is the cause.
- `ab-test-analyzer` judges a variant test before anyone declares a winner.
- `sequence-writer` rewrites the sequence when the cause is the angle or the copy.
- `reply-objection-handler` writes the answer to a specific reply that stalled.

## Rules

- Never "it depends" without a verdict. State the assumption and give the verdict.
- Never present a [Practitioner] rule as data, and never strip the source from a [Public] number.
- Never judge a hypothesis under 300 contacts as failed or proven.
- Never invent a benchmark that is not in `references/benchmarks.md`. If none fits, say so.

## Credits

The idea of an instant-verdict outbound analyst comes from lemlist's public `outbound-analyst` skill
(github.com/l3mpire/claude-skills). This version is rewritten from scratch for B2B service companies
and does not use lemlist's dataset; every benchmark number carries its own source in
`references/benchmarks.md`. Author of this version: Victor Shulga (victorshulga.com).
