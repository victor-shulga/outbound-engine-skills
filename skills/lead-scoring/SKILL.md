---
name: lead-scoring
description: >-
  Score a lead AFTER contact — start from the pre-contact profile score and add what only a conversation
  reveals: engagement, confirmed deal size, the real decision path, timeline. Use when asked to rank leads you
  have already spoken to, prioritise a reply queue, decide who gets a call first, or recalibrate scoring bands
  against a real pipeline. Triggers include "score these leads", "prioritise the pipeline", "who do we call
  first", "rank the replies". For scoring a cold base nobody has spoken to, use `prospect-scoring`.
---

# Lead Scoring

Scoring splits in two, because the data splits in two.

- **Pre-contact** — what you can read: profile fit, services fit. That is `prospect-scoring`.
- **Post-contact** — what only a conversation establishes: whether they engaged, what the deal is
  actually worth, who really decides, when they would move.

This skill is the second half, and it **starts from the first**. A lead score that re-derives fit
from scratch throws away the work already done and produces two different fit numbers for the same
account.

## The structure

```
lead score = prospect profile (carried over, capped)  +  post-contact points (0 until contact)
```

A workable default — tune the weights, keep the shape:

| Block | Max | Available |
|---|---:|---|
| Prospect profile (from `prospect-scoring`, normalised) | 30 | before contact |
| Engagement — replied, opened a thread, asked something real, attended | 15 | after contact |
| Confirmed deal potential — a number they said, not one you inferred | 20 | after contact |
| Decision path — you know who signs and how they buy | 15 | after contact |
| Timeline — a date or a window they named | 10 | after contact |
| Access — you are talking to the person who decides, or to a champion who will carry it | 10 | after contact |

**Hard ceiling rule.** A lead with zero post-contact points cannot outrank one that has them,
however good its profile. Cap uncontacted rows below the top band. Otherwise the queue fills with
beautiful strangers and the people who actually replied sit behind them.

## Bands come from your pipeline, not from the rubric

A rubric's thresholds are a guess until a real pipeline calibrates them. If the team's live sheet
treats 60+ as worth a call and the rubric says 75, **the sheet wins** — it is the one that has been
compared against outcomes. Write both numbers down and reconcile them deliberately; do not let a
theoretical threshold quietly override observed behaviour.

Recalibrate after every meaningful cohort, and recalibrate on **accounts, not rows** — a company with
three contacts otherwise counts three times and drags the whole model.

**Only calibrate on a clean cohort.** Accounts with mostly empty fields will show absurd conversion
rates, because they were usually created by hand *after* they converted. Backfilled records
predicting the outcome that created them is the most common way a scoring model gets a flattering,
useless number. In one calibration a base looked like it converted at 9.6%; on the clean cohort it
was 3.2%.

**When the base has no deal values, the model optimises conversations, not revenue** — and will
systematically favour small accounts, because small firms answer more. Say so out loud rather than
presenting the ranking as a revenue ranking. Recalibrate only once deal values exist.

## Hard gates beat points

Some facts should never be outweighed by a good total:

- **Confirmed non-target** → clamp the score below the disqualify line, no matter what else scored.
- **Data doubt on a load-bearing field** → clamp below the top band. The lead stays in the queue and
  gets human eyes, rather than being either promoted on bad data or silently dropped.
- **Explicit opt-out** → out of scoring entirely, out of all campaigns.

A gate that only subtracts points is not a gate. It has to clamp.

## Keep the components visible

Store every block as its own column, never just the total. When a lead scores 78, you have to be able
to see whether that came from a confirmed budget or from three soft engagement points — those two
78s deserve opposite actions. A single total column makes the model unauditable and, in practice,
untrusted by the people meant to work the queue.

Same rule for the inputs behind a block: where a number could come from several sources, keep the
sources in separate columns and note which one was used. Merging them loses the distinction between
a verified figure and an inferred one exactly when you need it.

## Output

One row per lead: `Name · Company · Prospect profile · Engagement · Deal · Decision path · Timeline ·
Access · Total · Band · Action · Data confidence · Gate fired (if any) · What is missing`.

Sorted by band, then by what is missing — because the top of a "needs more information" list is
usually a better use of an hour than the bottom of the qualified one.

## Handoff

Band → action: a call, one qualifying reply, a nurture track, or disqualify. The reply itself is
written by `reply-objection-handler`, which also triages it for intent and speed. Patterns across
many scored leads — a whole band that never converts — belong in `reply-audit` and then back into
`hypothesis-builder`.
