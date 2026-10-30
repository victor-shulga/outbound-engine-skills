---
name: ab-test-analyzer
description: Use when asked to compare two campaign variants, determine a winner, or analyze the results of a split test
---

# A/B Test Analyzer

Compare two campaign variants, determine statistical significance, declare a winner, and recommend the next test.

## What you need

- Variant A metrics: sends, opens, replies, interested replies
- Variant B metrics: same
- What was different between the variants (the variable being tested)
- Minimum 50 sends per variant for analysis

## Metrics hierarchy

Analyze in this order — each layer tells you something different:

1. **Open rate**: subject line or sender name problem
2. **Reply rate**: copy or targeting problem
3. **Interest rate**: offer or angle problem
4. **Meeting booked rate**: CTA or qualification problem

A test is only conclusive for the layer where the variants diverged. Don't attribute an interest rate difference to the subject line.

## Statistical significance guide

- Under 50 sends per variant: inconclusive — note it, don't act on it
- 50–100 sends per variant: directional — treat as signal, not proof
- 100+ sends per variant: statistically meaningful — act on this

## Process

1. Calculate all four rates for both variants
2. Identify at which layer the variants diverged
3. Determine statistical significance based on send volume
4. Declare winner (or "inconclusive" if under threshold)
5. Recommend what to test next — don't just repeat the same test

## Terms and plain-language output

<!-- glossary:start terms=ab-test,open-rate,reply-rate,positive-reply-rate,meeting-rate,divergence-layer,test-confidence,kill-keep -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| A/B test, test ideas, hypotheses | A/B-тест | показуємо половині відвідувачів один варіант, половині інший і дивимось, який дає більше заявок. |
| open rate, opens | частка відкриттів | Скільки листів відкрили; число неточне, бо поштові сервіси самі відкривають листи, тож це лише підказка. |
| reply rate | частка відповідей | скільки людей з тих, кому написали, відповіли. |
| positive reply rate | частка позитивних відповідей | скільки з тих, кому написали, відповіли з інтересом, а не «відпишіть мене» |
| meeting rate, meeting booked rate | частка зустрічей | скільки зустрічей отримали з усіх, до кого дійшли |
| divergence layer | етап, де варіанти розійшлися | відкриття, відповіді, інтерес чи зустрічі; висновок робимо лише про цей етап |
| Conclusive / Directional / Inconclusive | висновок тесту: доведено · є тенденція · замало даних | залежить від кількості відправок: 100+ на варіант, 50–100, менше 50 |
| kill / keep threshold, N | поріг «лишаємо чи прибираємо» | на 40–60 контактів за 2 тижні: від 10% позитивних відповідей лишаємо, менше 5% прибираємо, між ними міняємо сигнал або посаду |
<!-- glossary:end -->

## Output format

```
A/B test: [what was tested]
Date: [date]

VARIANT A — [description of variant]
Sends: [n] | Opens: [n] ([%]) | Replies: [n] ([%]) | Interested: [n] ([%])

VARIANT B — [description of variant]
Sends: [n] | Opens: [n] ([%]) | Replies: [n] ([%]) | Interested: [n] ([%])

ANALYSIS
Divergence layer: [opens / replies / interest / meetings]
Delta: [A vs B difference at divergence layer]
How much to trust it, in words: [proven (100+ sends per variant) / a trend, not proof (50–100) / too little data (under 50)], [reason]

WINNER: [Variant A / Variant B / Inconclusive]
Why: [one-line explanation]

NEXT TEST
Variable to test next: [what to change]
Hypothesis: [what you expect to happen and why]
```

## Notes

- Only test one variable at a time — if you change subject line AND copy, you can't attribute the result
- Don't declare winners on open rate alone — open rate can be gamed by subject line tricks that don't convert
- If both variants are in Kill territory (under 17% interest rate), the problem is the hypothesis, not the variant
- Document every test result — patterns across tests are more valuable than any single test
