---
name: multi-channel-orchestrator
description: Use when asked to build a multi-channel sequence, coordinate email and LinkedIn touchpoints, or plan a combined outreach flow for a hypothesis
---

# Multi-Channel Orchestrator

Design a coordinated email + LinkedIn outreach sequence — with correct timing, channel order, and message coordination across both channels.

## What you need

- Hypothesis name and ICP
- Email sequence (already written or reference `sequence-writer`)
- LinkedIn sequence (already written or reference linkedin-sequence)
- Sending tools available (Instantly/PlusVibe for email, Heyreach/Expandi for LinkedIn)

## Multi-channel principles

- Email and LinkedIn are not duplicates — they support each other
- Email is for the argument. LinkedIn is for the relationship.
- Never send the same message on both channels on the same day
- Use LinkedIn to warm up before email at scale — connection before sequence
- After a positive email reply, switch to LinkedIn DM for the conversation — it's warmer
- After a LinkedIn connection, reference it in the email sequence — "I saw we connected on LinkedIn"

## Default sequence architecture (14-day flow)

```
Day 0:  LinkedIn — send connection request (reference skill: linkedin-sequence)
Day 2:  Email — Step 1 (if LinkedIn not accepted yet, lead with signal only)
Day 3:  LinkedIn — if accepted, send follow-up message 1
Day 5:  Email — Step 2
Day 7:  LinkedIn — follow-up message 2 (if no email reply yet)
Day 10: Email — Step 3 (final email)
Day 14: LinkedIn — soft close or resource share (if no response on either channel)
```

Adjust timing based on persona: founders respond faster on LinkedIn; VPs of Sales respond faster to email.

## Process

1. Confirm email sequence and LinkedIn sequence are both written and stress-tested
2. Map each touchpoint to a day and channel
3. Add coordination notes: what changes in the email if LinkedIn was accepted; what changes if email got a reply
4. Identify decision points: at what point do you go single-channel if one channel isn't working?
5. Return the full orchestration map with conditional logic

## Terms and plain-language output

<!-- glossary:start terms=sequence,connection-request,follow-up,hypothesis,campaign-tier,buying-signal -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| sequences and templates | ланцюжки листів і шаблони | серія з кількох листів чи повідомлень одному проспекту з паузами між ними. |
| connection request, CR, connection note | запит на контакт у LinkedIn | Запрошення з запискою до 300 символів; у ньому нічого не продаємо, мета лише щоб прийняли. |
| follow-up, FU1 / FU2 | наступне повідомлення | Повідомлення після запиту на контакт чи першого листа; кожне додає нову думку замість «просто нагадую». |
| hypothesis | гіпотеза (кому, на яку подію, з якою пропозицією) | Одне припущення, яке перевіряє кампанія; результати рахуємо окремо по кожній гіпотезі. |
| Tier 1 Scale / Tier 2 Optimize / Kill | рішення по кампанії: нарощуємо · допрацьовуємо · зупиняємо | Сортування кампаній за часткою зацікавлених відповідей: понад 30% нарощуємо, 17–30% правимо текст, нижче 17% зупиняємо. |
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
<!-- glossary:end -->

## Output format

```
Multi-channel sequence: [hypothesis name]
ICP: [role] @ [company type]
Total duration: [n] days | [n] touchpoints

SEQUENCE MAP
Day | Channel  | Step | Message summary | Condition
0   | LinkedIn | CR   | Connection note  | Always
2   | Email    | 1    | Signal opener    | If LinkedIn not accepted
3   | LinkedIn | FU1  | First follow-up  | If connection accepted
5   | Email    | 2    | Problem expand   | If no email reply
7   | LinkedIn | FU2  | New angle        | If no reply either channel
10  | Email    | 3    | Direct close     | If no reply
14  | LinkedIn | FU3  | Resource / close | If no reply either channel

CONDITIONAL LOGIC
If email reply received → pause LinkedIn sequence
If LinkedIn reply received → pause email sequence, switch to LinkedIn DM
If connection not accepted by Day 5 → proceed email-only

Platforms: Email via [platform] | LinkedIn via [platform]
```

## Notes

- Multi-channel is for Tier 1 hypotheses only — don't add LinkedIn to campaigns that haven't proven themselves on email first
- The goal of LinkedIn in the sequence is to increase surface area, not to duplicate the pitch
- Keep LinkedIn messages shorter and warmer than email — tone shift matters
- Coordination across platforms requires manual attention or automation via trigger.dev — flag if neither is set up
