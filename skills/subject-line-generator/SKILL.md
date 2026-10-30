---
name: subject-line-generator
description: Use when asked to write subject lines, improve open rates, or generate subject line options for an email sequence
---

# Subject Line Generator

Generate 10+ subject line options for a given email, score each one, and return a ranked shortlist for testing.

## What you need

- Email body (step 1 at minimum)
- ICP and persona context
- Signal the email is built around
- Channel: cold email or LinkedIn InMail

## Principles

- Subject lines under 6 words perform best in cold outbound
- Never use the company name in the subject line — it reads as a template
- Curiosity beats clarity when it comes to cold email subject lines
- Questions outperform statements when the question is specific, not generic
- Personalization tokens work only when they're signal-derived, not just [First Name]

## Subject line patterns to generate

Generate at least 2 from each pattern:

1. **Signal reference**: directly references what just happened at their company ("new SDR team, new pipeline problem")
2. **Problem statement**: names the specific pain without a solution ("pipeline that depends on one channel")
3. **Reframe**: presents an assumption they hold and challenges it ("outbound isn't broken — the playbook is")
4. **Direct question**: asks the exact question the email answers ("is your outbound tied to one channel?")
5. **Unexpected angle**: something they wouldn't expect from a sales email ("your new CRO's first 90 days")
6. **Ultra short**: 1–3 words, creates pattern interrupt ("quick thought", "SDR question")

## Process

1. Generate 2 subject lines from each of the 6 patterns above (12 total)
2. Score each on: curiosity (0–2) + specificity (0–2) + length penalty if over 6 words (−1)
3. Rank by score
4. Flag top 3 for A/B testing

## Terms and plain-language output

<!-- glossary:start terms=open-rate,buying-signal,ab-test,hook mode=copy -->
Rules for every text a reader will see (post, email, message, page copy):

1. **No internal codes or letter scales** (A/B/C, D L T E, scores without words, framework codes). Write the meaning.
2. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English. A term the reader may not know gets explained in the same sentence or replaced.
3. **Any review, audit or report this skill produces for the team or the client** follows the document rules: open it with «Словник цього документа» (terms used, at most 10), do not score what depends on unfinished work, and open each section with one concrete action.

| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| open rate, opens | частка відкриттів | Скільки листів відкрили; число неточне, бо поштові сервіси самі відкривають листи, тож це лише підказка. |
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
| A/B test, test ideas, hypotheses | A/B-тест | показуємо половині відвідувачів один варіант, половині інший і дивимось, який дає більше заявок. |
| hook, cold hook | гачок | перший рядок листа, через який людина читає далі |
<!-- glossary:end -->

## Output format

```
Subject lines: [hypothesis / email step]
Email: [step number and first line]

RANKED OPTIONS
Score | Subject line | Pattern
[n]   | [subject]    | [pattern type]
...

TOP 3 FOR TESTING
A: [subject]
B: [subject]
C: [subject]

Recommended default: [A/B/C] — [one-line reason]
```

## Notes

- Vary the top 3 by ANGLE, not by swapping synonyms — token-level randomisation changes nothing a filter reads and nothing a prospect notices. Different question, different fact, different frame.
- Test subject lines systematically — track open rate by subject line variant, not campaign overall
- If open rate is below 40%, subject line is the first thing to change before touching copy
- Avoid: "quick question", "following up", "[First Name]" as opener — overused and filtered mentally
