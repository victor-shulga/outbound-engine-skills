---
name: hypothesis-builder
description: Use when asked to generate campaign hypotheses, build a testing matrix, or create a list of ideas to run from an ICP and signal set
---

# Hypothesis Builder

Take an ICP, a set of buyer personas, and a list of signals — generate a full testing matrix of campaign hypotheses to run.

## What you need

- ICP definition (industry, company size, geography)
- Target personas (2–5 roles you want to reach)
- Buyer signals available (hiring, funding, tool change, leadership change, etc.)
- Angles available (problem-based, time-based, social proof, competitive, etc.)

## Process

1. Map every combination of: persona × signal × angle
2. Remove combinations that are logically incoherent (e.g., "new CRO" signal sent to an SDR)
3. Group into clusters by similarity — don't list near-duplicates as separate hypotheses
4. Assign a priority score to each hypothesis (1–3) based on: signal specificity, persona authority, angle strength
5. Return the full matrix sorted by priority, with a one-line description of each

## Terms and plain-language output

<!-- glossary:start terms=hypothesis-matrix,buying-signal,angle,decision-maker -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| hypothesis matrix | таблиця гіпотез | список варіантів «кому · з чим · через який канал» для перевірки в розсилках. |
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
| angle, differentiation angle | кут подачі | одна думка, з якою ви заходите до покупця: його біль, ваш доказ і фраза, яку він повторить. |
| decision maker | ОПР (особа, що приймає рішення) | той, хто підписує: власник, операційний директор, керівник напряму |
<!-- glossary:end -->

## Output format

```
Hypothesis matrix: [ICP name]
Generated: [date]
Total hypotheses: [n]

PRIORITY 1 — Highest expected performance
H01 | [Persona] | [Signal] | [Angle] | [One-line description]
H02 | ...

PRIORITY 2 — Worth testing
H03 | ...

PRIORITY 3 — Low conviction, test last
H08 | ...

Recommended starting set: [H01, H02, H04] — run these first
```

## Notes

- Aim for 20–50 hypotheses for a single ICP/vertical — too few means under-testing, too many means you lack focus
- Priority 1 hypotheses should have a specific, recent signal + a senior decision-maker persona
- If signals list is vague, ask for specific examples before generating
- The matrix is not a campaign list — it's a backlog. Only run what you can actually resource
