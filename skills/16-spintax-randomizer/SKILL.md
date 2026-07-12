---
name: spintax-randomizer
description: Use when asked to add spintax to emails, randomize copy for deliverability, or make a sequence more unique at scale
---

# Spintax Randomizer

Add spintax variation to an email sequence to make each send look unique — improving deliverability and reducing pattern detection by spam filters.

## What you need

- Email sequence (all steps, final approved copy)
- Sending volume context (higher volume = more variation needed)

## What spintax is

Spintax uses `{option1|option2|option3}` syntax to randomly swap words or phrases per send. Example:
- `{Hi|Hello|Hey} {first_name}` — sends as "Hi John", "Hello Sarah", "Hey Mike"
- `{Best|Thanks|Cheers}` — randomizes sign-off

Most sending platforms (Instantly, PlusVibe, Smartlead) support this syntax natively.

## Where to apply spintax

Apply variation to these parts of every email — in order of impact:

1. **Greeting**: `{Hi|Hello|Hey} {{first_name}}`
2. **Sign-off**: `{Best|Thanks|Talk soon|Cheers}`
3. **CTA phrasing**: vary how you ask the question — same meaning, different words
4. **Opening phrase**: first 3–5 words before the signal reference
5. **Transition phrases**: "The reason I'm reaching out" → `{The reason I'm reaching out|What made me write|Why I'm sending this}`
6. **Subject line**: if 3 variants were selected, apply spintax across all three

## What NOT to randomize

- The signal reference — this must be specific and consistent
- The company name or role variable — these come from the data
- The core argument — variation in logic confuses the message
- PS lines — they should be consistent to build the pattern

## Process

1. Read each step of the sequence
2. Identify 3–5 spintax points per step (use list above)
3. Write 2–3 variants for each point
4. Wrap in `{variant1|variant2|variant3}` syntax
5. Return the full sequence with spintax applied
6. Flag any variables that will need platform-specific tokens (e.g., `{{first_name}}`)

## Output format

Return the full sequence with spintax inline. For each step, note how many variation points were added.

```
STEP 1 — [n] variation points applied
Subject: {subject A|subject B|subject C}
---
{Hi|Hello|Hey} {{first_name}},

{The reason I'm reaching out|What prompted this email} is...
[rest of body]

{Best|Thanks|Talk soon},
[Sender name]
---

[Repeat for each step]
```

## Notes

- More variation = better for high-volume sends (5,000+/day). For under 500/day, 2 variants per point is enough.
- Test that spintax renders correctly in the platform before launching — send a test to yourself
- Spintax helps with deliverability but does not replace good copy — a bad email with spintax is still a bad email
- After applying, run the sequence through stress-test one final time to confirm quality is preserved
