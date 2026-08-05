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
