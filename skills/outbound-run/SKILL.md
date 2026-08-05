---
name: outbound-run
description: The router for the outbound engine. Works out which stage of an outbound build you are actually at, checks the gate that stage depends on, and sends you to the one skill that does the next piece of work. Use when you do not know where to start, when you have just installed this bundle, when a campaign is underperforming and you need to find where it broke, or when you ask "what do I do next", "where do I start", "which skill do I use", "our outbound isn't working", "з чого почати", "який скіл запускати", "що робити далі". Routes and enforces gates — it does not do the work itself.
---

# Outbound Run — the router

Twenty skills is a toolbox, not an order of operations. This skill supplies the order.

It does three things and stops: works out where you are, checks whether the gate for that stage is
actually met, and hands you to one skill. It never does the downstream work itself — if it starts
writing copy or scoring a base, it has failed.

## Step 1 — Locate the caller

Ask at most three questions. Stop as soon as the answer is determined.

1. **What do you have in hand right now?** Nothing / a list of companies / a scored list / a written
   sequence / a campaign that is running / replies coming in / numbers that look wrong.
2. **Has anything been sent from these domains before?** Never / warmed but not sent / sending now.
3. **What is the actual complaint?** Only when something is running: no opens, no replies, replies
   that go nowhere, or good replies that die later.

Do not ask for an ICP document, a strategy deck or a budget. If they had those they would not be
asking where to start.

## Step 2 — Check the gate before routing

Each stage depends on one condition. Route past a failed gate and the work downstream is wasted, so
name the gate out loud and say why it exists.

| Gate | Condition | If it fails |
|---|---|---|
| **G1 — infrastructure** | domains authenticated, mailboxes warmed, sending caps set | → `deliverability-audit`. Nothing else matters yet: with broken sending you cannot tell weak copy from a blocked domain, so every later measurement is unreadable. |
| **G2 — a hypothesis exists** | you can say who, on what trigger, with what offer | → `hypothesis-builder`. A campaign without a stated hypothesis cannot be judged later, only argued about. |
| **G3 — a base exists and is graded** | rows have a fit score and passed the stop-filters | → `data-research`, then `prospect-scoring`. |
| **G4 — a reason to write now** | rows carry a dated signal or a data point with a source | → `signal-research`. Without this, queue D has nothing to open with and the campaign is a mass mailing wearing a first name. |
| **G5 — volume** | 300+ rows for a signal-led campaign, 500+ for a data-point-led one | report the shortfall. A base that cannot fill a campaign is a finding about the base, not something to paper over. |
| **G6 — contactable** | verified addresses, or the LinkedIn route confirmed | → `waterfall-enrichment`. |
| **G7 — one campaign, one text** | copy written per queue × persona × tier, not per base | → `copy-generation`. Mixing segments hides both the strong and the weak one behind an average. |

A gate that fails is not a reason to refuse. Name it, route to the fix, and say what it costs to
skip — the caller decides.

## Step 3 — Route

| Where they are | Next skill |
|---|---|
| Nothing yet, never sent | `deliverability-audit` → `hypothesis-builder` |
| Has an idea, no target list | `hypothesis-builder` |
| Has a raw list from a client, a CRM or a scrape | `data-research` |
| Has a graded list, does not know who is worth writing to now | `signal-research` |
| Has signals, needs to rank and gate | `prospect-scoring` |
| Ready to write, one channel | `copy-generation` (+ `subject-line-generator`, `ps-line-generator`) |
| Ready to write, two channels | `multi-channel-orchestrator` first, then the copy skills |
| LinkedIn specifically | `linkedin-sequence` |
| Campaign live, wants naming and structure straight | `campaign-naming`, `campaign-tiering` |
| Testing two variants | `ab-test-analyzer` |
| One reply in hand | `reply-objection-handler` |
| A batch of replies, wants the pattern | `reply-audit` |
| Silence after a few touches | `followup-sequence` |
| Owes a client or a boss an update | `weekly-outreach-report` or `campaign-report` |
| Leads they have already spoken to, needs a queue | `lead-scoring` |

## Step 4 — When something is running badly, route by symptom

The complaint points at a stage. Do not start from the top.

| Symptom | Most likely stage | Route |
|---|---|---|
| Almost nothing opens | infrastructure, not copy | `deliverability-audit` |
| Opens fine, no replies | the opener has no reason to exist | `signal-research`, then rewrite queue D on data points |
| Replies, but all "not now" | targeting is right, timing is not | `reply-audit`, then revisit signals in `hypothesis-builder` |
| Replies, but all "tell me more" that die | the copy is vague — they are curious about you, not about their problem | `reply-objection-handler` (read the tier mix), then `copy-generation` |
| Good replies that go nowhere later | the handoff after the reply | `lead-scoring`, then `reply-objection-handler` |
| Numbers look fine, nothing closes | the offer, not the outbound | say so plainly and stop routing — this bundle cannot fix an offer |

The last row matters. A router that always finds an outbound answer is useless, because sometimes the
honest answer is that outbound is not the broken part.

## Step 5 — Hand off properly

End every run with three lines, no more:

```
Where you are: [stage]
Gate: [met / failed — which one, and what skipping it costs]
Next: run `[skill]` — [one line on what it will produce]
```

Then stop. Do not pre-empt the skill's own questions or summarise what it will say.

## The loop

Outbound is not a line, it closes. A reply audit that lands on "wrong targeting" goes back to
`hypothesis-builder`. One that lands on "the signal burnt out" goes back to `signal-research` in
delta mode — most bases rot in about 45 days while the status column keeps saying Hot.

When a caller returns with the same complaint twice, do not route them to the same skill twice.
Say which assumption is probably wrong instead.

## What this skill does not do

Build lists · write copy · score anything · send anything · invent a strategy. It routes, enforces
gates, and gets out of the way.
