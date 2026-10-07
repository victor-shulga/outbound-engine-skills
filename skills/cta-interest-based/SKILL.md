---
name: cta-interest-based
description: >-
  The call-to-action rule for ANY outbound copy: cold sequences use an INTEREST-BASED (soft) CTA
  only and never ask for a call, a meeting or a time slot. Load this skill whenever you write or
  review the CTA line of a cold email, follow-up, LinkedIn message or full sequence, and whenever
  another copy skill (sequence-writer, linkedin-sequence, followup-sequence, cold-email-playbook,
  reply-objection-handler) is producing outreach. Trigger on: "CTA", "call to action", "soft CTA",
  "interest CTA", "fix my CTA", "як закінчити лист", "заклик до дії", "не клич на дзвінок",
  "перепиши CTA". Contains the approved interest-CTA bank, the banned call-based CTA list, red
  flags, a 0-6 scoring method for CTA variants and a reviewer checklist. This rule wins over any
  sample or template that ends a cold message with a meeting ask.
---

# CTA: interest-based only

A cold touch has one job: get a reply. Booking the meeting happens later, inside the reply thread,
after the prospect has shown interest. So every CTA in a cold sequence is an interest (soft) CTA:
it checks interest and does not ask for a call, a meeting or a calendar slot.

Answer in the user's language. The CTA itself is written in the prospect's language.

## The rule

> **Cold sequences use interest-based CTAs only. No call or meeting asks.**

It covers every step: the first email, every follow-up and every LinkedIn message. It overrides any
example, template or other skill's output that ends with "worth a call?", "20 minutes?" or a specific time.

## Why

There are three CTA families:

| CTA type | What it asks | In a cold sequence? |
|---|---|---|
| Specific | A concrete day and time ("Tuesday at 4pm?") | Never |
| Open-ended | A meeting with no fixed time ("time next week to meet?") | Never |
| Interest (soft) | Whether the topic matters to them, no meeting ("interested in how X works?") | Always |

Specific CTAs belong to the deal stage, when a conversation already exists and both sides want the
meeting. In a cold touch they ask for commitment before the prospect has any reason to give it, and
reply rate is the only number that matters until they answer. Keep the two stages apart.

Allowed soft variants:
- Interest question: "Is fixing [pain] on your list this quarter?"
- Lead magnet: "Can I send the 1-pager?"
- Short video: "Can I send you a 2-minute Loom?"

## Approved interest-CTA bank

Swap in the outcome, pain or initiative that the message body set up.

- Want to see what [OUTCOME] could look like for your team?
- Open to hearing how teams like yours get [DESIRED OUTCOME]?
- Which part of this is most relevant for you?
- Does this fit anything on your plan for [YEAR]?
- Could this help your team right now?
- Curious how [PEER 1] and [PEER 2] got to [POSITIVE OUTCOME]?
- Is this on your radar at the moment?
- Worth unpacking how this could help with [PAIN]?
- Interested in exploring this?
- Worth a look?
- Could [SOLUTION] get your team to [OUTCOME] faster?
- Is [POSITIVE OUTCOME] something you are working toward?
- How much is [PAIN] slowing down [BUSINESS OBJECTIVE] today?
- Can I send the doc / 1-pager / short Loom on how [PEER] did it?

Follow-up soft closes (a bump with no meeting ask):
- Any thoughts on my last note?
- Did my last note land, or is it off the mark?
- Is the timing off, or is this just not a fit right now? (breakup)

## Banned CTAs (never ship)

Any CTA that names a call, a meeting, a demo or a time slot. Typical offenders:

- "Are you available Tuesday at 4pm?"
- "Do you have time next week to meet?"
- "Worth a 15/20/30-minute call?"
- "Open to a 20-minute chat about it?"
- "Can we set up a call so I can learn more about your business?"
- "When can we book a call?"
- "I'd love to hop on a call and explain."
- "Let's explore synergies on a quick call."
- "Here is a 30-minute video walkthrough." (too heavy for a cold touch)
- "Do you have time to talk about it?"

If a draft ends with one of these, or any variant of them, rewrite the CTA from the interest bank
before you deliver it.

## Red flags (rewrite on sight)

Beyond the call and meeting ban:
- "Let me know if you're interested": passive, there is no question
- "Would love to connect": vague, asks for nothing
- "Feel free to book a time on my calendar": a meeting ask in disguise
- "I know you're busy, but...": opens with an apology
- two questions in one CTA: keep one
- a sudden switch into sales mode that the body did not lead up to

## Step logic

Every step stays interest-based; only the framing changes.
- Step 1: one yes/no interest question tied to the signal ("Is this something you're actively looking at?")
- Step 2: build on the earlier note and offer the asset ("Can I send the 1-pager on how [PEER] did it?")
- Step 3 / breakup: acknowledge timing, still no meeting ask ("Is the timing off, or is this just not a fit right now?")

LinkedIn CTAs: one sentence, softer than the email version.

## Scoring CTA variants

When asked to improve a CTA, return 3 variants and score each from 0 to 6:
- specificity (0-2): tied to this prospect's pain or signal, not generic
- low friction (0-2): answerable in one word or one line
- fit with the step's goal (0-2): matches step 1, 2 or breakup as described above

Recommend one. A variant that names a call, meeting, demo or time slot scores 0 whatever the rest.

Rule of thumb for diagnosis: a high open rate (roughly 40% or more) with replies under 1% usually points
to the CTA rather than the targeting or the copy. Start the review here.

## Reviewer checklist (run on every sequence)

1. Does any step ask for a call, meeting or time slot? Rewrite it as an interest CTA.
2. Is each CTA a yes/no or other low-friction question? Good.
3. Do the first email, every follow-up and every LinkedIn message each end on a soft CTA phrased as a question? Required.
4. Does the breakup step acknowledge timing without a meeting ask? Good.

## Works with

If installed (pack `outbound-engine-skills`): `sequence-writer`, `linkedin-sequence`, `followup-sequence`,
`cold-email-playbook` and `reply-objection-handler` write the messages; this skill decides how each one ends.
Once a prospect has replied with interest, the meeting ask belongs to `reply-objection-handler`.

## Credits

Method by Victor Shulga (victorshulga.com), from his workshop on trigger-based outreach. The three CTA
families (specific, open-ended, interest) follow a common sales-training classification; the red-flag
list and the 0-6 scoring were adapted from an earlier CTA-review skill in the same collection and
rewritten here.
