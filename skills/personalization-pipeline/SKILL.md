---
name: personalization-pipeline
description: Designs the pipeline that computes per-lead personalization before the sequencer — two generated fields, a confidence gate, and a push into the sending tool. Use when the user asks how to send hyper-personalized email at volume, says "як це автоматизувати", "personalization at scale", "конвеєр", "Clay-like pipeline", or has a sequence whose first line cannot be expressed as a template variable.
---

# Personalization Pipeline

The sequencer does not generate anything. It substitutes a string that was computed earlier and stored on the lead.

## Generate two fields, never the letter

```
Hey {{firstName}},

{{observation}}          ← generated, 15–25 words

[fixed offer skeleton, identical across the whole batch]

{{question}}             ← generated, one sentence

{{senderName}}
```

A fully generated email always drifts to the mean: correct, smooth, faceless. The fixed skeleton holds the voice; the model only does the part a template cannot — read someone else's document and form one thought about it.

Roughly 30 of 45 words move. That is enough.

## The pipeline

```
1. signal      ATS aggregator          → posting + raw quote
2. people      domain → person search  → name, title, LinkedIn, email
3. text        model on the quote      → observation + question + confidence
4. gate        branch                  → confidence < 4 → human review queue
5. load        connector               → lead with custom fields
6. send        sequencer               → 20–30 per mailbox per day
```

All six can live in one workbook if the platform has connectors to the sequencer. Check before designing — a missing final connector turns this into CSV export by hand.

## Feed the model facts, not a brief

Input is a fixed record, not "write a personalized email":

| Field | Example |
|---|---|
| quote from the posting | "Our application is a Majestic Monolith built with Rails…" |
| posting title | Senior Software Engineer |
| days open | 8 |
| recipient title | Senior Director of Software Engineering |
| company and size | 142 people |

Output is fixed too: `observation` ≤ 25 words, `question` one sentence, `confidence` 1–5.

**One hard constraint in the prompt: the observation may rest only on the quote.** Not "I saw your LinkedIn", not "as a fast-growing company". No quote means no observation.

## The gate

Without it this is a spam cannon with extra steps.

A lead does not enter the campaign when:

- confidence is below 4
- the line contains template tells: *I noticed · as a · impressive · exciting*
- the observation runs longer than 25 words — the model started summarizing the posting
- the quote is a false positive on the keyword

Everything blocked goes to a human review queue. Expect about one lead in seven. If it is far below that, the gate is not doing anything; if it is far above, the source data is too thin.

## The fallback route matters as much as the main one

A lead with no quote is not discarded and is not given an invented observation. It moves to a **separate campaign** on a weaker signal, using a skeleton with no generated line — only plain variables.

Measure the two campaigns **separately**. Merged, the weak track drags the strong one and you kill a hypothesis that was working.

## What automation does not change

**Send limits stay.** Hyper-personalization does not buy volume. 20–30 per mailbox per day, two to three weeks of domain warm-up, SPF/DKIM/DMARC green, inbox placement tested. The best copy in a spam folder returns zero and a false verdict on the hypothesis.

**The top of the list stays manual.** The 20–30 highest-scoring accounts never enter the pipeline. A human writes those. Automation takes the middle, not the peak.

**Cost is per lead, and it is small.** Roughly 1.5 credits for the person, 1 for the generated line, pennies for the posting. A 300-lead batch lands near 750 credits. Say the number out loud before building — it is usually lower than the team fears, which changes the conversation about scope.

## Terms and plain-language output

<!-- glossary:start terms=first-line,merge-variable,confidence-gate,fallback-route,sequencer,ats,buying-signal,warmup,spf-dkim-dmarc,inbox-placement -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| observation, first line, icebreaker, opener | перший рядок листа | конкретний факт про людину чи компанію, з якого починається лист |
| variable, {{first_line}}, unrendered | змінна в шаблоні листа | поле, яке підставляється в текст; порожнє чи непідставлене видно читачу в першому рядку |
| confidence gate, confidence 1–5, human review queue | поріг упевненості | рядок з оцінкою нижче 4 з 5 іде на ручну перевірку замість розсилки |
| fallback route, fallback campaign | запасний маршрут | компанії без цитати йдуть в окрему кампанію без згенерованого рядка і рахуються окремо |
| sequencer, sending tool | сервіс розсилки | інструмент на кшталт Instantly, який відправляє серії за розкладом |
| ATS, ATS aggregator, career sites | система найму на сайті компанії | сервіси на кшталт Greenhouse чи Lever, звідки беремо повний текст вакансій |
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
| warmup | прогрів поштових скриньок | поступове збільшення кількості листів з нової скриньки, щоб пошта не потрапила в спам. |
| SPF / DKIM / DMARC, MX | SPF, DKIM, DMARC (записи, що підтверджують домен) | Технічні записи в налаштуваннях домену, які доводять поштовим сервісам, що лист справді від вас; без них листи йдуть у спам. |
| inbox placement rate | частка листів у вхідних | Скільки листів потрапляє у вхідні замість спаму; нижче 90% з розсилкою чекаємо. |
<!-- glossary:end -->

## Output

1. Node diagram of the six steps with the actual tool at each one
2. The exact input record and output schema for the generation step
3. Gate conditions as a checklist
4. Fallback route
5. Cost per lead and per batch
6. What stays manual
