---
name: prospect-scoring
description: Score an account BEFORE any contact — profile fit only, from data you can read without talking to anyone. Use when asked to qualify or rank a cold base, set a fit gate, decide who is worth outreach at all, or sort a list into outreach queues. Triggers include "score this base", "qualify the list", "ICP fit score", "who is worth writing to", "rank these accounts". This is the pre-contact half of scoring — for ranking leads you have already spoken to, use `lead-scoring`.
---

# Prospect Scoring

Answers one question about a cold account: **is this profile ours, before anyone has spoken to them?**

Everything here is readable without a conversation — what they do, who they serve, what they run.
Nothing that only a call can establish belongs in this score. That is `lead-scoring`.

## The rule that fixes most broken rubrics

**Never score a dimension you already use as a stop-filter.**

If geography and headcount are hard gates at the filtering step, they must not also carry points.
Every surviving account passed them by definition, so those points are free, identical for everyone,
and they inflate the total until the threshold stops separating anything. A rubric that spread
100 points across four dimensions where two were already gates had to be replaced for exactly this:
the numbers looked discriminating and were not.

What is left after removing the gates is usually small — and that is correct. A pre-contact score
built on two honest dimensions beats one built on eight where six are noise.

## What the score is made of

Profile only. A workable default, to be tuned per ICP:

| Dimension | Max | Read from |
|---|---:|---|
| ICP fit — are they the kind of company we serve | 15 | their own description of themselves: site, company page, specialties |
| Services fit — do they need the specific thing we sell | 15 | services listed, work shown, capability they clearly lack or clearly run in-house |

**Gate:** a floor on the total (e.g. 20 of 30). Below it the account does not enter outreach,
whatever else is true about it.

Add a dimension only if it is (a) readable cold, (b) not already a gate, and (c) actually varies
across the base. Deal potential qualifies only when the base genuinely carries it — usually it does
not, see normalisation below.

## The signal is a ROUTE, not points

This is the second thing rubrics get wrong. A buying signal does not make an account a better fit —
it makes it a better **time**. Fit and timing are different axes and must not be summed into one
number, or an account with a perfect profile and no trigger looks worse than a poor-fit account that
happens to be hiring.

So the signal sets the queue, not the score:

| Queue | Condition | What the opening line stands on |
|---|---|---|
| **A** | strong live signal | the event, dated, with a link |
| **B** | weaker or older signal | the event, framed softer |
| **D** | no live signal | a data point from their own site |

No signal is not a low score. It is queue D plus a monitoring window — re-check in ~30 days before
concluding there is nothing there.

**An open role that has stayed open 45+ days is a stronger signal than a fresh one** — they cannot
fill it. Do not decay a vacancy while it is still open.

## Missing data

1. **Missing → 0 plus a `data-gap` flag. Never a guess, never a midpoint.** A guessed firmographic
   becomes a forecast somebody relies on.
2. **Normalise when a whole dimension is structurally empty.** If nobody in the base has deal size,
   that dimension is 0 for everyone, the ceiling drops, and no account clears the gate. Keep two
   numbers: the raw sum, and the same sum as a percentage of the dimensions that actually had data.
   Gate on the second — but only at data confidence M or H. At L, fall back to the raw sum, so a row
   with two filled fields cannot look perfect.
3. **A tier is set only on a verified number.** Where headcount is unconfirmed the tier cell reads
   "verify manually" — never blank, never inferred.

## The headcount trap, from both directions

Worth stating because the obvious fix breaks the opposite case.

Company sites systematically overstate the team: a site claiming dozens of engineers can be a firm of
three. The instinct is to take the smaller of the available numbers — and that immediately breaks
large firms, because a big agency does not list its staff by name, so a named count returns a
fraction of the truth.

The construction that survives both: **the company page headcount is the source; a named count on
their site is only a CHECK, never a source.** When the named count is several times smaller and the
page figure is itself small, flag the row and cap it below the top band — it needs human eyes, but it
is not discarded.

Keep the numbers in separate columns. The moment they are merged into one "headcount" field, you can
no longer tell a verified figure from an inferred one.

## Output

One row per account: `Company · Tier · per-dimension points · Raw total · Normalised total ·
Data confidence (H/M/L) · Gate (pass/fail) · Queue (A/B/D) · Missing fields`.

Plus a `data-gap` list: accounts that need enrichment before the score means anything. Rows that fail
the gate stay in the file with the reason — deleting them means re-buying and re-researching them a
quarter later.

## Don't

- Don't score anything a stop-filter already decided.
- Don't sum fit and timing into one number.
- Don't round up on doubt — take the lower band.
- Don't run a real base on weights nobody approved. If they are not confirmed, say so and label the
  run a draft preview.

## Handoff

Gate passed → queue assigned → `waterfall-enrichment` for contacts, then `outbound-sequence-writer` per
campaign. After a reply lands, the account moves to `lead-scoring`, which starts from this profile
and adds what only a conversation can establish.
