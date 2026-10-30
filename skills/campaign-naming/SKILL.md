---
name: campaign-naming
description: Use when asked to name campaigns, generate a naming convention, or organize a hypothesis matrix into readable campaign names
---

# Campaign Naming

Generate consistent, readable campaign names from a hypothesis matrix — so a list of 40 campaigns is scannable in 5 seconds.

## What you need

- Hypothesis matrix (from hypothesis-builder) or list of campaign parameters
- Platform the campaigns will run in (PlusVibe, Instantly, etc.)

## Naming convention

Format: `[Signal]-[Persona]-[Angle]-[Channel]`

Examples:
- `SDRHire-VPSales-Pipeline-Email`
- `NewCRO-Founder-90Days-LinkedIn`
- `FundingRound-HeadOfSales-Scale-Multi`
- `TechStackChange-RevOps-Migration-Email`

Rules:
- No spaces — use CamelCase or hyphens
- No generic labels: "Q2 Campaign", "Test 1", "Outbound April" are all banned
- Maximum 5 components — if you need more, the hypothesis is too complex
- Channel suffix is optional but recommended when running multi-channel
- Date prefix optional for recurring campaigns: `2026Q2-SDRHire-VPSales-Pipeline-Email`

## Why this matters

When you have 40 campaigns running in parallel, you need to read the name and instantly know:
- Who you're targeting (persona)
- Why you're reaching out now (signal)
- What you're arguing (angle)
- Which channel

A campaign named "Outbound Test 3" tells you nothing. `SDRHire-VPSales-Pipeline-Email` tells you everything.

## Process

1. Take the hypothesis matrix or list of campaigns
2. Extract: signal, persona, angle for each
3. Generate name in convention format
4. Check for duplicates — if two campaigns have the same name, the hypotheses are too similar
5. Return full named list

## Terms and plain-language output

<!-- glossary:start terms=naming-convention,buying-signal,angle,hypothesis,persona -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| naming convention [Signal]-[Persona]-[Angle]-[Channel] | правило назв кампаній: подія · посада · аргумент · канал | Назва кампанії одразу каже, кому, чому зараз і через який канал пишемо. |
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
| angle, differentiation angle | кут подачі | одна думка, з якою ви заходите до покупця: його біль, ваш доказ і фраза, яку він повторить. |
| hypothesis | гіпотеза (кому, на яку подію, з якою пропозицією) | Одне припущення, яке перевіряє кампанія; результати рахуємо окремо по кожній гіпотезі. |
| persona, persona document | портрет покупця | опис типової людини, що купує: посада, задачі, болі, заперечення, де її шукати; будуємо лише з реальних даних. |
<!-- glossary:end -->

## Output format

```
Campaign names: [ICP / vertical]
Total: [n]

[Original hypothesis description] → [Campaign name]
...

Naming conflicts (same name, different hypothesis): [list — needs resolution]
```

## Notes

- Naming is infrastructure — do it before setting up campaigns, not after
- Rename any existing campaigns that don't follow this convention before the next review
- If your platform has character limits, abbreviate signal and angle but keep persona readable
- Add the campaign name as the first tag in your CRM contact record — it's the fastest way to trace where a lead came from
