---
name: icp-builder
description: Use when asked to build an ICP from scratch, define the ideal customer profile, or structure ICP documentation for use across skills
---

# ICP Builder

Build a structured ICP definition from existing knowledge, call recordings, and win/loss data. Output a reusable ICP file that all other skills can reference.

## What you need

- Any of the following (provide as much as you have):
  - Description of your best current customers
  - Sales call recordings or transcripts
  - Win/loss notes
  - Industry intuition about who benefits most
- What problem you solve and for whom

## Process

1. Ask 8 calibration questions if inputs are thin:
   - Who are your 3 best customers right now — what do they have in common?
   - Who do you lose deals to most often, and why?
   - What does the prospect say in the first call that makes you think "this is perfect"?
   - What's the typical team size/structure that gets value fastest?
   - What signals tell you a company needs you right now vs. in 6 months?
   - What roles are involved in the buying decision?
   - What is the one sentence your best customer would use to describe your value?
   - What type of company is a waste of time, even if they match on paper?
2. Synthesize answers into structured ICP dimensions
3. Add negative ICP criteria (disqualifiers)
4. Output as a reusable markdown ICP file

## Terms and plain-language output

<!-- glossary:start terms=firmographic,persona,buying-signal,disqualifier-rings,decision-maker,day-to-day-owner -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| firmographic / technographic / situational fit | профіль компанії · її інструменти · ситуація, коли ви потрібні зараз | Три частини ICP: галузь і розмір, якими сервісами користуються, і події, після яких купують. |
| persona, persona document | портрет покупця | опис типової людини, що купує: посада, задачі, болі, заперечення, де її шукати; будуємо лише з реальних даних. |
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
| negative ICP, anti-ICP, rings 1–4 | фільтри відсіву | Чотири перевірки по черзі: модель бізнесу, конкурент, розмір і країна, вже наш клієнт чи партнер; кожна відсіяна компанія має причину. |
| decision maker | ОПР (особа, що приймає рішення) | той, хто підписує: власник, операційний директор, керівник напряму |
| day-to-day owner, champion | той, хто працюватиме з вами щодня | керівник проєкту, BIM-менеджер, керівник розробки; йому важливе інше, ніж ОПР |
<!-- glossary:end -->

## Output format

```
# ICP Definition: [Company Name]
Last updated: [date]

## Firmographic fit
- Industry: [list]
- Company size: [headcount range]
- Revenue stage: [e.g., Series A–C / $5M–$50M ARR]
- Geography: [list]
- Business model: [B2B SaaS / Agency / Services / etc.]

## Technographic fit
- Uses: [tools that indicate fit]
- Likely stack: [CRM, outbound tools, etc.]

## Persona fit
- Primary: [role] — [why this person buys]
- Secondary: [role] — [influence/blocker context]

## Situational fit (when they need you NOW)
- [Signal 1]
- [Signal 2]
- [Signal 3]
Signals RANK accounts, they never filter them: an account that passes the rings and has no signal stays on the list with an empty signal set and a lower priority.

## What you sell (context, not a filter)
"[One line: the offer and who buys it]" — used only to judge competitors: a company that sells this, or anything in the same category to the same buyer, is a competitor, not a lead.

## Negative ICP — four rings, checked in this order
1. **Ring 1 · Business model**: [product-only / marketplace / other models that do not buy this]
2. **Ring 2 · Competitors**: [who sells the same thing, or the same category, to the same buyer]
3. **Ring 3 · Size and geo**: [headcount floor, e.g. under 11 people; markets you do not serve]
4. **Ring 4 · Already ours**: existing clients, former clients, partners, your own peers and vendors — pulled from the CRM, never from memory
Every rejected account carries its ring number and a one-line reason. Rejected accounts are not a reserve to revisit later.

## One-sentence value for this ICP
"[What you do] for [who] so they can [outcome]."
```

## Notes

- This file is the input to icp-validation, signal-research, hypothesis-builder, and sequence-writer
- Revisit after every 20 closed deals — ICPs drift
- Negative ICP criteria are as important as positive ones — include them, ring by ring; ring 4 (already ours) is the one every tool without CRM access misses
- If call recordings are available, extract language the prospect used and include it verbatim under situational fit
