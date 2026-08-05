---
name: sequence-writer
description: Writes an eight-touch email and LinkedIn sequence built on one signal, with interest-only CTAs and separate copy for the decision-maker and the champion. Use when the user says "напиши сіквенс", "write the sequence", "cold email", "потрібні листи під цю гіпотезу", or has a signal and an offer and needs the messages. Enforces the no-meeting-ask rule on every touch.
---

# Sequence Writer

One hypothesis in, eight touches out. The only job of a cold touch is to earn a reply.

## Non-negotiable rules

**No meeting ask. Anywhere.** Not in email one, not in the breakup, not in a LinkedIn message. No call, no demo, no calendar slot, no "20 minutes". Every touch ends on an interest question instead. The meeting gets booked later, inside the reply thread, once they raised a hand.

Approved closes: *Is this on your radar right now? · Worth exploring? · Want me to send it? · Is that something your team is feeling? · Did you have any feedback on my note? · Is the timing off, or just not a fit?*

**Under 50 words per email.** Excluding the signature. It has to fit a phone screen with whitespace between paragraphs.

**Subject: one or two words, lowercase, boring.** `platform hire`, `on-call`, `majestic monolith`. It should read like it came from someone inside the company. No emoji, no marketing verbs, no four-word headlines.

**The first line names a specific fact.** The number of days a role has been open, a sentence from their own posting, a version they run. Never "I noticed you're growing" or "as a VP of Engineering you must be".

**The decision-maker and the champion get different emails.** The buyer feels an unfilled req. The champion feels the on-call rotation. One text for both lands on neither.

**Signature: name and title.** No links, no banner, no logo.

## Structure

| Day | Channel | Touch |
|---|---|---|
| 0 | LinkedIn | warm-up — visit profile, follow, like a post |
| 1 | LinkedIn | connection request with a note, under 300 characters |
| 1 | Email | cold email |
| 3 | LinkedIn | message after the connect |
| 6 | Email | something useful — an asset, offered as a question |
| 9 | Email | short bump |
| 12 | LinkedIn | different angle or a redirect to the right person |
| 15 | Email | breakup |

First four touches produce ~80% of replies. The rest catches people who were away.

## Email one, the shape

```
{one or two word subject}

Hey {First},

{observation — the specific fact, and what it implies}

{the offer in one sentence, plus what de-risks it}

{interest question}

{Sender}
```

Nothing else. No "we are a company that", no service list, no link.

## Banned phrases

Openers: *I hope this finds you well · I know you're busy · I'm writing to let you know · As a {title} you must be*

Bumps: *Just checking in · Thoughts? · Did you see my previous email? · Just following up to see if you saw*

Pitches: *Here are the services we provide · Please don't think of this as a sales pitch · I really think we can help · CLICK HERE*

## Variables versus generated fields

Only these are safe as plain template variables, because they are facts:

`{First}` `{Company}` `{role}` `{days}`

Anything that carries a *thought* — an observation about their situation, a tailored question — is not a variable. It is a field computed before the send. That is a separate step; see the personalization pipeline skill. Do not try to express an insight as spintax or a nested template. It reads exactly as what it is.

## Before shipping, check

- [ ] no call, meeting, demo or time slot in any of the eight touches
- [ ] every email under 50 words
- [ ] every email ends in a question
- [ ] subject is one or two lowercase words
- [ ] first line is a specific fact, not a category statement
- [ ] any quoted line from the prospect has been read with human eyes
- [ ] buyer and champion versions differ in the pain, not just the title
- [ ] signature carries no links

## Output

Header with the hypothesis, the persona pair, and the signal. Then the timeline, then every touch in full, then two or three ready examples written on real named accounts from the list — that is what proves the sequence works on this data rather than in the abstract.

Close with what to A/B: subject lines, and the two candidate first-line angles.
