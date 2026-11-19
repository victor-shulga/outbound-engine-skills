---
name: cold-email-formats
description: >-
  Library of 24 named cold-email formats (first touch), like the infographic catalogue but for
  email. Takes an ICP hypothesis (signal / data-point / no anchor, persona, pain, proof, asset)
  plus the sender's tone of voice (6 axes), filters the catalogue by what data the list really
  has and what tone the sender can carry, and proposes 3 formats from different families, each
  as a ready draft with subject, body and optional P.S. Keeps a per-client log so the next
  campaign does not repeat the same shape. Use when the user says "шаблони листів", "варіанти
  холодного листа", "який формат листа під цю гіпотезу", "бібліотека емейлів", "запропонуй
  листи під ICP", "cold email formats", "email templates for this hypothesis", or pastes a
  hypothesis / ICP / cold email and asks for options. Talks to the user in their language, the email in the
  prospect's language. NOT for full sequences and follow-up timing (sequence-writer),
  infrastructure (cold-email-playbook), or replies to replies (reply-objection-handler).
---

# Cold email formats

Pick before you write. The catalogue lives in `references/email-formats.md`: read it FIRST,
every time. It has the selection table, the recipe per format and the tone dial.

## Step 1 · Collect the inputs

From the hypothesis (hypo-generator matrix, a hypothesis card, or the user's words):

| input | values | if missing |
|---|---|---|
| anchor | A signal (with date) / B data-point (with comparison) / C none | ask; never guess |
| data per account | list of real columns in the list (e.g. `round_date`, `open_roles`) | assume none → only C formats |
| persona + level | C-level / VP-Head / manager | take from the hypothesis |
| pain | one sentence | "уточнити", do not invent |
| proof | case with a number, same segment? | no proof → drop formats whose skeleton needs it (1, 3–7, 11, 13–15, 18, 21) or keep the line out |
| asset | exists before send? | no → drop 19 |
| tier | top accounts (teardown capacity)? | no → drop 20 |
| tone | F D E N H K, 1–5 each, from the sender's tone of voice card | ask; a plain peer-to-peer default is F2 D2 E2 N4 H1 K4 |
| language | prospect's language | English |

## Step 2 · Filter, then pick three

1. **Eligibility by anchor + data.** Drop every format whose "needs per account" column the
   list cannot fill for ≥ 80% of rows.
2. **Tone fit.** Drop formats whose tone range excludes the sender's card.
3. **Anti-monotony.** Read `state/log.md`. Drop formats used for this client in the last two
   campaigns, unless the log marks them as the winner (reply rate) and the user wants a re-run.
4. **Pick 3 from different families or mechanisms**: e.g. one A, one B, one C; or, if only C is
   eligible, three different C mechanisms (segment / proof / gift). Never three of the same.

Show the user a short table first, in their language: format · why it fits · what the list
must have · risk. Then the three drafts.

## Step 3 · Draft each one

Follow the recipe skeleton exactly; change wording only along the tone dial. For each:
subject (2 options), body ≤ 90 words, optional P.S. Placeholders as `{{column}}` that exist in
the list; one filled example for a real or neutral account (stripe.com, linear.app), with
every number traceable. No source for a number → the sentence goes.

## Step 4 · Check, mechanically

- If the `anticopywriting-ai` skill is installed (`npx skills add victor-shulga/gtm-skills/anticopywriting-ai`):
  `python3 "<installed anticopywriting-ai folder>/scripts/detect.py" --lang en --mode email <file>` → `verdict`
  must not be `fail`. Not installed → check the bans below by hand.
- Last line is a direct question. No call / slot / calendar ask.
- One "we/I" sentence, and it is the proof.
- No "Saw / Noticed / I came across", no spintax, no dashes, no "not X but Y".
- Body ≤ 90 words (`wc -w`).

## Step 5 · Log

Append one line to `state/log.md`:
`YYYY-MM-DD · client · hypothesis · formats proposed (#n, #n, #n) · chosen: ?`
When the user reports results later, add the reply rate next to the chosen format. That is how
the catalogue learns which format wins per segment.

## Hard rules

- Every number in a sent email comes from the account's data or a named source.
- Client names never go into this skill's files; examples stay segment-generic.
- The email is a draft in chat. Nothing is sent or loaded into a sending tool from here.
