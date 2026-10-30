---
name: signal-catalog
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

`# · signal · type in words (event / standing fact) · detection tool · freshness window`

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

## Terms and plain-language output

<!-- glossary:start terms=buying-signal,data-point,signal-track,signal-score-factors,signal-bundle,volume-gate,freshness-window,intent-data -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
| data point, state signal | факт про компанію (дата-поінт) | Факт з їхнього сайту чи вакансії, з якого відкриваємо лист; подія підказує, коли писати, а факт підказує, що сказати. |
| track С / Д | тип рядка: подія · постійний факт | подія підказує, коли писати; факт підказує, що сказати, і сам не працює |
| score = Scrape, Scaling, Problem, Offer, Trigger | оцінка сигналу за п'ятьма ознаками | наскільки легко знайти, чи вистачить обсягу, чи доводить біль, чи є готовий офер, наскільки сильний привід писати сьогодні |
| bundle | зв'язка сигналів | кілька споріднених сигналів під однією темою листа, щоб набрати обсяг для тесту |
| volume gate, 300 / 500 rule | мінімальний обсяг для тесту | 300 компаній для гіпотези на події, 500 для гіпотези на факті; менше означає «не перевірено» |
| freshness window, expiry window, decay | термін свіжості сигналу | скільки днів сигнал ще дає привід писати; потім він стає просто фактом |
| intent data | дані про намір купувати | сигнали, що компанія зараз шукає таку послугу: пошукові запити, відвідування сторінок, вакансії. |
<!-- glossary:end -->

## Output

1. Catalog table, grouped, with the score column
2. Top-15 ranking
3. Volume reality check against the gate
4. Bundles with real available counts
5. One recommendation: which bundle runs first, and why it is not only about the score

Hand off to a hypothesis step (signal × tier × offer), then to list building.
