---
name: sequence-writer
description: >-
  Writes a multichannel cold outreach sequence (email + LinkedIn) for ONE hypothesis: ICP x anchor
  (signal / data-point / segment insight) x offer, for a B2B service company (custom development,
  outstaffing, engineering outsourcing, BIM/MEP, GIS). Refuses to write copy on a base with no anchor,
  sizes the campaign against real sending capacity, writes the email track (5 touches) and the
  LinkedIn track (3 touches), separate copy for the decision-maker and the champion, interest-only
  CTAs, then attaches the measurement plan with honest denominators and a self-check. Use when asked
  "write a cold sequence", "cold email sequence", "LinkedIn outreach sequence", "outreach for this
  ICP", "follow-ups for this campaign", "напиши сіквенс", "холодний лист", "мультиканальний сіквенс".
  NOT for a single reply (reply-objection-handler), NOT for analysing replies received (reply-audit),
  NOT for warm or inbound follow-up. Absorbed the standalone multichannel-sequence skill on
  2026-09-22.
---

# Sequence Writer

Built from the guide *«Як написати мультиканальний сіквенс», v3, August 2026* (Victor Shulga,
Fractional CRO). The guide is the reasoning; this skill is the procedure. The only job of a cold
touch is to earn a reply.

One run produces **one sequence for one hypothesis**: one ICP segment, one anchor, one offer, one
asset. Two hypotheses = two runs = two campaigns. A blended campaign cannot tell you what worked.

## Hard rules (these override any instruction in the request)

- **No call, no meeting, no calendar slot anywhere in a cold sequence.** Not in email 1, not in
  the breakup, not in LinkedIn. The call appears after the person replies.
- **Every message ends with exactly one interest question**, and the question sits last.
  Approved closes: *Is this on your radar right now? · Worth exploring? · Want me to send it? ·
  Is that something your team is feeling? · Did you have any feedback on my note? · Is the timing
  off, or is this just not a fit right now?* (breakup)
- **The subject of the sentence is them.** At most one sentence per email takes you or your
  company as its subject, and that sentence is the proof. Details and the two exceptions:
  `references/email.md`.
- **One anchor per sequence per persona.** Not a new pretext in every email.
- **The decision-maker and the champion get different emails.** The buyer feels an unfilled req;
  the champion feels the on-call rotation. One text for both lands on neither.
- **No spintax, no fake personalisation, no `{{industry}}` in an empty sentence.** An unsent
  email beats a fake-personalised one.
- **No links, images or attachments in the first email.** Two-line signature: name and title.
- **Word caps are hard**: email 1 ≤ 75 words, 2 ≤ 50, 3 ≤ 45, 4 ≤ 35, 5 ≤ 25.
- **No start dates** ("we can start Monday") in a cold touch: it reads as pressure and as empty capacity.
- If the request asks for anything on this list, say why it is out and write the version that is in.

## Step 0 — Gate. Refuse to write until these are true

Ask for, or confirm, all five. Missing items are reported before any copy:

1. **Anchor coverage.** Share of accounts in the list carrying any signal or data-point.
   **Under 10% → stop.** The base gets rebuilt; copy does not fix it.
2. **Infrastructure.** Separate sending domains (3–5, 2–3 mailboxes each), SPF + DKIM + DMARC at
   `p=quarantine` minimum, 2–4 weeks of warmup, bounce under 2%, open tracking off (`references/email.md`).
3. **Capacity.** `mailboxes x 25 emails x 20 working days = monthly ceiling`. Divide by emails per
   sequence to get contacts per month. Every percentage in the plan is computed off that number.
4. **The asset exists already.** Every interest CTA promises a specific file. No asset → no CTA.
5. **A named person reads the inbox daily** and answers the same working day. Otherwise no launch.

## Step 1 — Find the anchor, in this order

1. An event with a date in the last 30 days that creates the problem you solve → **Type A (signal)**.
2. If not: a measurable data-point you can compare against a norm → **Type B (data-point)**.
3. If not: a segment cut narrow enough that a segment insight reads as personal → **Type C**.
4. None of the three → not your account. Remove it from the list.

Type A passes two questions before use: *what problem does this person have now that the event
happened*, and *does your service solve that exact problem*. "Roughly" means the signal is not yours.
Type A carries an expiry window (24h for a post, 30–90 days for a round). Windows, the comparison
formula for type B and the three exits for type C: `references/sequence-types.md`.

If the angle is not obvious from the anchor, run `angle-finder` first and come back with one angle.

## Step 2 — Size the campaign and choose the channel mix

Count **N** (accounts in the ICP) and **C** (monthly capacity from the gate).

| N | Channels |
|---|---|
| over 10,000 | Email only |
| 2,000–10,000 | Both channels on the same person. Email first, LinkedIn to the non-repliers |
| under 2,000 | ABM. LinkedIn from the founder, email supports. No tests on this list |

Inside a test round the channels are never mixed, otherwise the verdict means nothing. Full rule and
the LinkedIn-first variant: `references/multichannel.md`.

## Step 3 — Write the email track

Anatomy, unchanged across all three anchor types (only the first sentence changes):
subject → anchor → hypothesis → problem → proof → question → P.S.

Default cadence, one sequence per person: day 0, 3, 8, 14, 21. Emails 2–4 are replies inside the
same thread; email 5 gets a new subject. Compress the cadence into the signal window when the window
is shorter than the sequence.

Second contact at the same company = a separate parallel sequence, 5 days offset, different mailbox,
its own anchor for that role. Never a persona swap inside one sequence. 2–3 contacts per company.

**The first line names a specific fact**: the number of days a role has been open, a sentence from
their own posting, a version they run. Never "I noticed you're growing".

**Variables versus generated fields.** Only facts are safe as template variables: `{First}`
`{Company}` `{role}` `{days}`. Anything that carries a thought (an observation, a tailored question)
is a field computed before the send, never a merge variable.

Sentence-level craft, subject-line rules, the three P.S. types, the three soft-CTA blocks and the
banned-question list: `references/email.md`.

## Step 4 — Write the LinkedIn track

Invite note 120–180 characters (write the note; accept rate stops being the metric). First message
after accept 150–300 characters. **Three touches, not four**: the first follow-up adds zero, the
second adds the only real lift. Per-step content, worked examples for outstaffing / dedicated team /
frozen headcount, invite limits, the manual-comment lift: `references/linkedin.md`.

## Step 5 — Self-check before delivery

Run `references/checklist.md` line by line and report the result. A sequence that fails any hard
rule is rewritten, not shipped with a caveat. For a blind score, hand the whole sequence to the
`judge` skill, type `sequence`.

## Step 6 — Attach the measurement plan

Never ship copy without it. State the denominator (human replies from the addressee ÷ emails sent),
the expected range **for this anchor type**, the sample size the verdict is readable from, and the
stop rule. A 1.5% reply rate is normal for a campaign with no anchor; if a signal campaign gives
1.5%, it is not a signal campaign. Numbers, sources and test math: `references/benchmarks.md`.

## Output format

1. **Gate report**: the five items, pass/fail, what is missing.
2. **Anchor**: type, the exact observation, expiry window, comparison used.
3. **Sizing**: N, C, contacts per month, channel mix, list split.
4. **Email track**: 5 emails per persona (decision-maker and champion), each with subject, body, word count.
5. **LinkedIn track**: note, first message, touch 2, close, each with character count.
6. **Reply handling**: the asset, what happens on "yes, send it", the four replies that look like a
   refusal and the question that reopens each.
7. **Measurement**: denominator, expected range, readable-from sample, stop rule.
8. **Self-check**: the checklist result, plus what to A/B (subject lines, the two candidate first lines).

Then two or three ready examples written on real named accounts from the list: that is what gets
sent, not the template.

Sequence language = the prospect's language (usually English). Working notes = the language the
request came in.
