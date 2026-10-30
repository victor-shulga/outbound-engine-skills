---
name: campaign-tiering
description: Use when asked to review running campaigns, decide what to scale vs. kill, or sort active hypotheses by performance
---

# Campaign Tiering

Review all running campaigns and sort them into three tiers — scale, optimize, or kill — based on performance data. Do not keep running what isn't working.

## What you need

- Campaign performance data (reply rate, interest rate, open rate)
- List of active campaigns with hypothesis names
- Number of contacts sent per campaign (need minimum 50 sends to tier)

## Performance thresholds

**Tier 1 — Scale**: Interest rate above 30%
→ Add LinkedIn as a second channel. Increase send volume. Expand the contact list.

**Tier 2 — Optimize**: Interest rate 17–30%
→ Tweak copywriting. Adjust CTA. Try a new subject line variant. Don't kill yet.

**Kill — Under 17% interest rate** (or under 1% reply rate)
→ Pause immediately. Do not add more contacts. Document what failed and why.

**Interest rate definition**: % of replies that expressed genuine interest in continuing the conversation (not out of office, not unsubscribe, not "not interested").

## Process

1. Pull campaign metrics via MCP from the sending platform
2. Filter out campaigns with under 50 sends — not enough data to tier
3. Calculate interest rate for each campaign: (interested replies / total replies) × 100
4. Assign tier per thresholds above
5. For Tier 1: suggest specific scale actions
6. For Tier 2: suggest one specific optimization to test
7. For Kill: identify the most likely root cause (targeting, copy, angle, or signal)

## Terms and plain-language output

<!-- glossary:start terms=campaign-tier,interest-rate,reply-rate,open-rate,buying-signal,hypothesis,root-cause -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| Tier 1 Scale / Tier 2 Optimize / Kill | рішення по кампанії: нарощуємо · допрацьовуємо · зупиняємо | Сортування кампаній за часткою зацікавлених відповідей: понад 30% нарощуємо, 17–30% правимо текст, нижче 17% зупиняємо. |
| interest rate, interested | частка зацікавлених відповідей | Яка частка відповідей показує справжнє бажання продовжити розмову; автовідповіді й відмови сюди не входять. |
| reply rate | частка відповідей | скільки людей з тих, кому написали, відповіли. |
| open rate, opens | частка відкриттів | Скільки листів відкрили; число неточне, бо поштові сервіси самі відкривають листи, тож це лише підказка. |
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
| hypothesis | гіпотеза (кому, на яку подію, з якою пропозицією) | Одне припущення, яке перевіряє кампанія; результати рахуємо окремо по кожній гіпотезі. |
| root cause: targeting/data vs message vs pitch | першопричина: не ті люди чи дані · текст · пропозиція | Що саме зламалось; правимо лише це місце. |
<!-- glossary:end -->

## Output format

```
Campaign tiering review: [date]
Campaigns evaluated: [n] | Excluded (under 50 sends): [n]

TIER 1 — SCALE ([n] campaigns)
[Campaign name] | Sends: [n] | Reply rate: [n%] | Interest rate: [n%]
→ Scale action: [add LinkedIn / expand list / increase volume]

TIER 2 — OPTIMIZE ([n] campaigns)
[Campaign name] | Sends: [n] | Reply rate: [n%] | Interest rate: [n%]
→ Optimize: [specific suggestion]

KILL ([n] campaigns)
[Campaign name] | Sends: [n] | Reply rate: [n%] | Interest rate: [n%]
→ Root cause: [targeting / copy / angle / signal quality]

SUMMARY
Campaigns to scale: [n] | To optimize: [n] | To kill: [n]
Recommended next step: [one action]
```

## Notes

- Run tiering weekly — campaigns that looked promising at 20 sends may fail at 100
- Killing campaigns is good news: you freed budget and attention for what's working
- If everything is in Tier 2 or Kill, the problem is usually the signal strategy, not the copy
- Never move a campaign from Kill back to active without changing the hypothesis — same campaign, same result
- Campaigns with high open rate but low reply rate = copy problem. Low open rate = subject line or deliverability problem.
