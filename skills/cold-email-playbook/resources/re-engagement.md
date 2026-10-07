# Re-engaging ghosted and closed-lost leads

For contacts whose last real exchange was weeks or months ago: a positive reply that went quiet, a
booked call they missed, a proposal that was declined or never answered, or a contact from an old
sequence. Follow-ups inside a running sequence are a different job (if installed, use
`followup-sequence`).

## Before writing: four questions

1. **What happened last?** Date, channel, what was discussed, who said what. Read the thread.
2. **Why did it stop?** Their stated reason if there was one (budget, timing, chose another vendor,
   internal priority), otherwise "unknown".
3. **What is different now?** On their side (new role, new funding, hiring, a project win, a new
   quarter) or on yours (a new capability, a new relevant case you can name, a price or packaging
   change). Without a real change, wait.
4. **Who should get it?** The same person, or someone else if they left or the reply pointed elsewhere.

## Rules

- Say openly that you spoke before. Pretending it is a first touch reads as automation.
- Lead with what changed, then connect it to what they told you last time.
- Quote their own reason when they gave one ("you mentioned the timing was wrong until Q3").
- One message, short, plain text, no attachments.
- The ask is an interest question or an easy-to-refuse question. No call or time-slot ask.
- No guilt, no "just checking in", no "did you see my last email".
- Every claim of a new result or case must be real and checkable.
- Respect an explicit no: anyone who asked not to be contacted stays off the list.

## Timing that works

| Situation | When to reach out |
|---|---|
| They named a time ("talk after Q3") | a week before that time |
| Closed-lost on price or priority | next budget cycle or quarter start, or about 90 days |
| Lost to a competitor | after the new vendor's likely first milestone (often 3-6 months) |
| Positive reply that went silent | 2-3 weeks after the last message, then once more a month later |
| No-show to a booked call | same day or next day, then stop if no answer |
| Old cold-sequence contact | when a new trigger appears, or at the next TAM cycle (about every 3 months) |

## The easy-to-refuse question

Chris Voss (Never Split the Difference) popularised "no-oriented" questions: questions where "no" is
the comfortable answer, such as asking whether it would be a bad idea to pick the topic up again.
People reply more readily when declining costs nothing, and a "no, not a bad idea" is still a yes.
Use one per message at most.

## Templates

Fill every `{{...}}` with real facts. If a field cannot be filled honestly, cut the sentence.

**1. Positive reply that went quiet**

```
Subject: {{topic}}, picking this back up

{{first_name}}, we last spoke on {{date}} about {{their_goal}}, and then it went quiet,
which usually means priorities moved.

Since then {{verifiable_change}}.

Would it be a bad idea to pick this up again, or is it off the table for now?
```

**2. No-show**

```
Subject: today's call

{{first_name}}, we missed each other today. Things come up.

If {{their_goal}} is still on your list, I can send the two or three points I had prepared
so you can see whether a call is worth it.

Want me to send them?
```

**3. Closed-lost, with their reason**

```
Subject: since {{month}}

{{first_name}}, when we talked in {{month}} the blocker was {{their_reason}}.

{{what_changed_that_addresses_it}}.

Is this worth another look, or has the need gone away?
```

**4. Old contact, new trigger**

```
Subject: {{trigger_topic}}

{{first_name}}, I wrote to you a while back about {{old_topic}}. This is a different reason:
{{new_trigger_observed}}.

Teams in that position usually run into {{likely_problem}}.

Is that on your radar, or does someone else on the team own it?
```

## After sending

- A reply of any kind: answer within the same working day. For objections, if installed, use
  `reply-objection-handler`.
- No reply: one more touch at most, then park the contact until the next real change.
- Track re-engagement separately from new outbound; its reply rate is not comparable with cold.
