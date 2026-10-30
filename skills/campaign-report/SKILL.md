---
name: campaign-report
description: Use when asked to generate a weekly or monthly campaign performance report, summarize outbound results, or brief a client or stakeholder on campaign status
---

# Campaign Report

Pull metrics across all active campaigns, generate a structured performance report, and surface the one most important action to take this week.

## What you need

- Access to sending platform via MCP (PlusVibe, Instantly, or equivalent)
- Reporting period (default: last 7 days)
- Whether this is an internal report or client-facing

## Report sections

**Executive summary** — 3 bullets max. What happened this week in plain language.

**Campaign performance table** — every active campaign with key metrics.

**Tier movements** — which campaigns moved up or down in tier since last week.

**Top performer this week** — the single campaign with the best interest rate, with a short explanation of why it worked.

**Key insight** — one pattern observed across all campaigns that informs the next action.

**Recommended action** — one specific thing to do this week based on the data.

## Process

1. Pull campaign metrics for the reporting period via MCP
2. Calculate open rate, reply rate, and interest rate per campaign
3. Run campaign-tiering logic to assign tiers
4. Compare to last week's tiers (if data available) to find movements
5. Identify the top performer and extract what made it work
6. Synthesize one key insight from patterns across all campaigns
7. Recommend one specific action

## Terms and plain-language output

<!-- glossary:start terms=open-rate,reply-rate,interest-rate,campaign-tier,buying-signal,angle,persona -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| open rate, opens | частка відкриттів | Скільки листів відкрили; число неточне, бо поштові сервіси самі відкривають листи, тож це лише підказка. |
| reply rate | частка відповідей | скільки людей з тих, кому написали, відповіли. |
| interest rate, interested | частка зацікавлених відповідей | Яка частка відповідей показує справжнє бажання продовжити розмову; автовідповіді й відмови сюди не входять. |
| Tier 1 Scale / Tier 2 Optimize / Kill | рішення по кампанії: нарощуємо · допрацьовуємо · зупиняємо | Сортування кампаній за часткою зацікавлених відповідей: понад 30% нарощуємо, 17–30% правимо текст, нижче 17% зупиняємо. |
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
| angle, differentiation angle | кут подачі | одна думка, з якою ви заходите до покупця: його біль, ваш доказ і фраза, яку він повторить. |
| persona, persona document | портрет покупця | опис типової людини, що купує: посада, задачі, болі, заперечення, де її шукати; будуємо лише з реальних даних. |
<!-- glossary:end -->

## Output format

```
Outbound Report: [week / date range]
Generated: [date]
Prepared by: Claude Code

EXECUTIVE SUMMARY
• [Key result 1]
• [Key result 2]
• [Key result 3]

CAMPAIGN PERFORMANCE
Campaign | Sends | Opens | Replies | Interested | Tier
[name]   | [n]   | [n%]  | [n%]    | [n%]       | [scale / improve / stop]
...

Total pipeline: [n] interested leads this period

TIER MOVEMENTS
Moved to Tier 1: [campaigns]
Moved to Tier 2: [campaigns]
Killed: [campaigns]

TOP PERFORMER
Campaign: [name]
Interest rate: [n%]
Why it worked: [signal + persona + angle that drove results]

KEY INSIGHT
[One pattern observed across campaigns — e.g., "SDR-hiring signal is outperforming new-CRO signal 2:1 this week"]

RECOMMENDED ACTION THIS WEEK
[Specific action — campaign to scale, test to run, copy to change, signal to add]
```

## Notes

- Client-facing reports: remove internal tier labels and replace with plain-language descriptions
- If interest rate is declining week-over-week, flag it prominently — this is the leading indicator of list exhaustion
- The "key insight" is the most valuable part of the report — don't skip it
- Schedule this report to run automatically every Monday morning via trigger.dev or equivalent automation
