---
name: icp-validation
description: Use when asked to validate a company against ICP criteria, score fit, or check if a company is worth targeting
---

# ICP Validation

Validate a company against defined ICP criteria and return a scored fit verdict.

## What you need

- Company name or website URL
- ICP definition (provide inline or reference your ICP file)

## Process

1. Pull the company's website and scan for: team size indicators, tech stack signals, product type, industry, and growth stage
2. Check LinkedIn via MCP for: headcount, recent hires, open roles, and leadership profile
3. Score fit against each ICP dimension (1-3 per dimension):
   - **Segment fit**: does the company match the target segment?
   - **Size fit**: does headcount/revenue match the ICP range?
   - **Signal fit**: is there an active reason they'd respond now?
   - **Role fit**: is the target persona present and reachable?
4. Return a one-line verdict + reasoning

## Terms and plain-language output

<!-- glossary:start terms=fit-score,buying-signal,disqualifier-rings,account-tier,sequence -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| ICP fit, services fit, prospect score, prospect profile | оцінка відповідності профілю | Бали за те, чи компанія з вашої ніші і чи їй бракує саме вашої послуги; рахуємо ще до першого контакту. |
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
| negative ICP, anti-ICP, rings 1–4 | фільтри відсіву | Чотири перевірки по черзі: модель бізнесу, конкурент, розмір і країна, вже наш клієнт чи партнер; кожна відсіяна компанія має причину. |
| Tier 1 / Tier 2 / Tier 3, tier | тір: група компаній за розміром і чеком | усередині однієї ніші ділимо компанії за розміром і можливим чеком; від тіру залежить офер і скільки уваги даємо |
| sequences and templates | ланцюжки листів і шаблони | серія з кількох листів чи повідомлень одному проспекту з паузами між ними. |
<!-- glossary:end -->

## Output format

```
Company: [Name]
Fit score: [X/12]
Verdict: [Strong fit / Marginal fit / Not a fit]

Segment: [score] — [one line reason]
Size: [score] — [one line reason]
Signal: [score] — [one line reason]
Role: [score] — [one line reason]
Why a buyer, not a competitor: [one line — what they sell and to whom, and why that makes them a buyer of your offer]

Recommended action: [write first, personal sequence / write later, standard sequence / skip] (in words, no tier numbers)
Skip reason: [business model does not buy this / competitor / size or country outside the range / already a client, partner or vendor] (in words, no ring numbers) — [one line]
```

## Notes

- If ICP isn't defined, ask for it before proceeding
- If LinkedIn data is unavailable via MCP, flag it and use public signals only
- "Marginal fit" means worth a Tier 2 sequence, not skip
