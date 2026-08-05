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
