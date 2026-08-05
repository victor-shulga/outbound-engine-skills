---
name: outbound-signal-catalog
description: Builds a 50-trigger signal catalog for one niche, scores every signal on a 5-factor weighted model, and bundles the signals that cannot reach test volume alone. Use when the user says "каталог сигналів", "signal catalog", "які сигнали брати", "по чому таргетити", "build triggers for [niche]", or is choosing what to detect before building a prospect list. Produces the raw material for hypotheses — not the hypotheses themselves.
---

# Signal Catalog

A signal catalog is the raw material of signal-based outbound. Fifty triggers, grouped by source, each with a detection tool, a freshness window, and a score.

## The one distinction that matters

Every row is one of two tracks. Get this wrong and the whole catalog is decoration.

| | Track `С` — event | Track `Д` — data point |
|---|---|---|
| Example | funding round, new exec, job posted | outdated framework, no DevOps on staff, product age |
| Fires for | ~3–5% of the base | ~100% of the base |
| Decays | yes, on a calendar | no |
| Tells you | **when** to write | **what** to say |
| Works alone | yes | **no** |

A data point on its own reads as an accusation: "your framework is out of support" earns "we know, thanks." Pair it with an event — "you raised in March and that framework lost support in March too" — and it becomes a conversation.

## Process

### 1. Frame the buying trigger

Before listing anything, write one sentence: what has to become true inside a company for them to need this service *now*. Everything in the catalog is either proof that sentence is true, or the moment it became urgent.

Examples of the frame, not the signals:
- capacity outgrows internal throughput
- obligations outgrow what the architecture can carry
- a deadline exists that the team cannot meet with current staff

### 2. List 50 triggers in source groups

Typical groups. Adapt to the niche — a construction niche has permits and tenders, a software niche has app stores and repos.

- Public records / tenders / permits
- Events and exhibitor lists
- Hiring
- Technology and stack
- Money and growth
- People and content
- Firmographic data points
- Intent and digital

**Where to look for group ideas the niche gives you for free:** any public database the buyer's own industry is forced to publish into.

### 3. Fill four columns per row

`# · signal · track (С/Д) · detection tool · freshness window`

Detection tool must be a specific named tool, not "research." Freshness must be a number of days or the word `стан` for a data point.

### 4. Score every signal

```
score = 0.15·Scrape + 0.15·Scaling + 0.25·Problem + 0.20·Offer + 0.25·Trigger
```
Each factor 1–5.

| Factor | Question |
|---|---|
| Scrape | how cheap and reliable is detection |
| Scaling | does it reach test volume in this base |
| Problem | does it prove acute pain, or just record a fact |
| Offer | is there a ready offer with proof behind it |
| Trigger | how strong is the reason to write today |

Report the maximum alongside every score. A number without a denominator is not a score.

### 5. Bundle what cannot stand alone

Volume gate: **300 accounts for an event-signal hypothesis, 500 for a data-point hypothesis.** Under that, do not run it.

Most single signals fail this. Bundle related signals under one email theme — the reader never sees the bundle, they see one coherent message. Report the available volume per bundle honestly.

If no bundle reaches the gate, the niche is too narrow. Say so, and offer the widening move: turn the vertical from a targeting filter into a proof selector. Detect the signal across the wider category; show the case study matching the reader's vertical.

## Hard rules

1. **Never invent a detection tool.** If you do not know what finds a signal, write `уточнити` and move on.
2. **Job posts live at account level only.** Never duplicate them as a persona trigger.
3. **Benchmarks are directional.** Vendor-published reply rates (18–22% single signal, 35–40% stacked) are marketing. The working ceiling is ~10% positive replies on a signal campaign.
4. **Enterprise intent platforms are out of scope** for teams under enterprise budget. Name them, price them, move on.
5. State which rows are new to the catalog and worth keeping for the next niche.

## Output

1. Catalog table, grouped, with the score column
2. Top-15 ranking
3. Volume reality check against the gate
4. Bundles with real available counts
5. One recommendation: which bundle runs first, and why it is not only about the score

Hand off to a hypothesis step (signal × tier × offer), then to list building.
