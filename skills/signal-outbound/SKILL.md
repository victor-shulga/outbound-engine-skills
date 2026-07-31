---
name: signal-outbound
description: Master router for signal-based outbound — runs the full path from a service page to an email addressed to a named person with a verified address, routing to the right skill at each step and enforcing the gate between them. Use when someone asks to build outbound from scratch, says "запусти аутбаунд", "run the outbound process", "де почати", "build me a campaign", "we need pipeline", or is holding one artifact (an ICP, a list, a sequence) and does not know what comes next. Start here rather than guessing which individual skill applies.
---

# Signal Outbound — master

Classic outbound looks for companies that resemble your customers and tells them about a service. This runs the other way: find the companies that **already described their own problem in public**, and open with their words.

The richest source of those words is job postings. A company that writes "our application is a majestic monolith" paid to publish that sentence and will not walk it back. That is not a guess about pain. It is pain confirmed by a hiring budget.

Everything downstream follows from one split: **the event tells you when to write, the data point tells you what to say.**

## The path

Nine steps. Each ends in an artifact, and three of them end in a gate that stops the run.

| # | Step | Route to | Ends with |
|---|---|---|---|
| 1 | ICP and tiers | `03-market-icp-persona` ⧉ | tier matrix + personas + anti-ICP |
| 2 | Offer and entry rung | `offer-factory` ⧉ | 5–6 scored bets, entry rung chosen |
| 3 | Signal catalog | `outbound-signal-catalog` | 50 triggers, scored, bundled |
| 4 | Hypotheses | `hypothesis-builder` | 10 scored, three picked · **GATE: volume** |
| 5 | Account list | `outbound-account-sourcing` | scored CSV · **GATE: 90% ICP spot-check** |
| 6 | People and email | `outbound-contact-enrichment` | contacts with verified addresses |
| 7 | Sequence | `outbound-sequence-writer` | 8 touches, both personas · **GATE: no meeting ask** |
| 8 | Personalization | `outbound-personalization-pipeline` | two generated fields + confidence gate |
| 9 | Launch | `deliverability-audit` | SPF/DKIM/DMARC, warm-up, send caps |

Running later: `weekly-outreach-report` for the weekly read, `reply-audit` when replies accumulate, `ab-test-analyzer` for angle tests.

⧉ = lives in a different plugin. `03-market-icp-persona` is in [gtm-strategy-skills](https://github.com/victor-shulga/gtm-strategy-skills), `offer-factory` in [gtm-skills](https://github.com/victor-shulga/gtm-skills). Without them installed, run steps 1–2 by hand — the path still works, it just loses the scaffolding for those two artifacts.

## The four rules that carry the whole thing

**A state signal does not work alone.** "Your framework is out of support" earns "we know, thanks." Pair it with an event — "you raised in March, that framework lost support in March" — and it becomes a conversation. Step 3 forces this distinction; do not let it collapse.

**Volume gate: 300 accounts per event-signal hypothesis, 500 per data-point hypothesis.** Under that, the test cannot produce a readable result. Bundle related signals under one email theme, or park it. If no bundle clears the gate, the niche was drawn too narrowly — turn the vertical from a targeting filter into a proof selector and widen.

**No meeting ask anywhere.** Not in email one, not in the breakup, not on LinkedIn. The only job of a cold touch is a reply.

**Two generated fields, never a generated letter.** A fully generated email drifts to the mean: correct, smooth, faceless. A fixed skeleton holds the voice while the model does the one thing a template cannot — read someone else's document and form a thought about it.

## Where runs actually fail

**The vertical was used as a filter when it should have been the proof.** A niche with strong case studies but only a few hundred companies is an ABM target, not a campaign. Detect the signal across the wider category and show the case study that matches the reader's vertical. Catch this at step 4, not after the list comes back empty.

**Two thirds of raw sourcing results are noise** — agencies, government contractors, universities. No vendor flag catches them. Budget time for an explicit exclusion pass at step 5, and diff what got dropped: over-filtering quietly removes real accounts.

**The quote was never read by a person.** Roughly one keyword match in seven is a false positive — "building a legendary legacy" is not a modernization signal. Ten seconds per account before enrichment.

**Personalization was attempted inside the sequencer.** It cannot be done there. If step 7 produced a first line that carries a thought, step 8 is mandatory, not optional.

**The list was enriched before it was filtered.** Enrichment is the expensive step. Spend it only on accounts that already passed.

## Reading the results

| State | Condition | Action |
|---|---|---|
| Kill | replies under 1.5% or interest under 17% | change the signal or the angle, not the copy |
| Optimize | interest 17–30% | new angles, tighter filters |
| Scale | interest above 30% | add a channel, raise volume |

Measure **per hypothesis, never per campaign.** A campaign mixing two signals reports an average that describes nothing.

Working ceiling on a signal campaign is around 10% positive replies. Vendor-published figures of 35–40% are marketing.

## Cost, so nobody has to guess

Roughly 2.5 credits per send-ready lead plus pennies per posting scanned. A 300-lead batch lands near 750 credits and a few dollars of scraping. Say this early — teams routinely assume an order of magnitude more and scope down for no reason.

Enterprise intent platforms starting at $30k/year do not pay back at this volume. Name them, price them, move on.

## What never enters the machine

The top 20–30 accounts by score. A person writes those. Automation takes the middle, not the peak.

## When someone arrives mid-path

Ask what artifact they already hold, then enter at the next step. Do not restart at step 1 to be thorough — check the existing artifact against its own gate and move forward. A list with no proof quotes goes back to step 5; a sequence with a calendar link goes back to step 7.
