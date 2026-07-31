---
name: outbound-personalization-pipeline
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

## Output

1. Node diagram of the six steps with the actual tool at each one
2. The exact input record and output schema for the generation step
3. Gate conditions as a checklist
4. Fallback route
5. Cost per lead and per batch
6. What stays manual
