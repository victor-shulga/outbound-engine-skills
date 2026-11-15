---
name: outreach-text-gate
description: >-
  Checks the three personalised fields of a prospect list (observation, guess, question) against the
  nine stop-filter conditions before a cold campaign launches, and marks every row ok, review or
  general. A script handles the seven mechanical conditions; Claude reads the source text for the two
  that need judgment (source is only an internal code, observation and guess describe different
  objects) and spot-checks five random ok rows. Use when someone says "стоп-фільтр тексту", "перевір
  три поля", "перевір observation guess question", "text gate", "перевір проспект-лист перед
  запуском", "чи можна запускати тексти", or uploads a prospect list CSV with
  observation/guess/question columns before a launch. NOT the data check of emails and bounces
  (pre-launch-data-check), NOT writing the fields (prospect-profiler), NOT humanizing the fixed parts
  of the letter (anticopywriting-ai).
---

# Outreach text gate

Source of the rules: instruction «Персоналізований аутріч із трьох полів», section 6 (stop-filter) and section 11 (pre-launch check). Output language for the person: Ukrainian by default, or the language the person writes in.

## Input

A CSV export of the prospect list, one row per person. Columns are matched by name, case-insensitive:

| Field | Accepted column names |
|---|---|
| observation | `observation` |
| guess | `guess` |
| question | `question` |
| model confidence 1–5 | `confidence`, `впевненість` |
| raw source text | `hook_source`, `basis`, `source_text`, `source`, `джерело зачіпки` |
| source date | `source_date`, `дата джерела`, `date` |

If the list lives in Google Sheets, export the tab as CSV first. Ask for the file if none was given. Never invent missing columns.

## Steps

1. Run the script:
   ```bash
   python3 scripts/check.py prospects.csv
   ```
   It writes `prospects.checked.csv` with `text_gate` (ok / review / general), `gate_reason` and `needs_human`, and prints the counts.
2. For every row with `needs_human`, open its source text and decide yourself:
   - condition 6: the source names nothing real (only a permit number, job code, internal id) → review;
   - condition 8: observation and guess are about different objects (different permit, different role, different product) → review;
   - empty question → review.
   The script only flags these by heuristics (no shared content words); a shared object phrased differently ("that seat" vs "the role") is fine, keep ok.
3. Pick five random rows still marked ok and compare observation with the raw source text word by word. If any one is wrong, say so and widen the check to the whole list.
4. Report in that language: counts (ok / review / general), the top reasons with counts, the rows you moved to review in steps 2–3 and why. Update the CSV with your decisions.
5. Rows in review: offer a rewrite only from the same source, or ask for a fresher source of the same company (last 6 months). Mark any rewrite as a draft for the person to approve. Do not overwrite the original fields.

## The nine conditions (any one = review)

1. model confidence below 4
2. observation shorter than 10 or longer than 25 words
3. guess is empty
4. first word is Saw, I saw, I noticed or Hope
5. banned anywhere: as a, impressive, exciting, reach out, hope this finds you, leverage, solutions, partner with, thrilled, passionate
6. the source is only an internal job number or code
7. question asks for a call, meeting or time
8. observation and guess describe different objects
9. the source is older than 6 months and guess says now (a missing source date is also review)

A row with an empty observation is `general`: it goes to the generic segment, not to review.

## Hard rules

- Never fill an empty field with a fallback ("your recent work"). Empty stays empty.
- Never mark a row ok to raise the count. If unsure, review.
- Only rows with `text_gate = ok` and a verified email go into the campaign.
