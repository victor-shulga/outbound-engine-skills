# Cold email formats

Reference for Step 2 of `SKILL.md` (pick formats). Twenty-four first-touch formats, what
anchor each one needs, what data must exist per account, which tone it tolerates, and the
way each one usually gets ruined.

The point of a named catalogue is a deliberate pick per hypothesis, so three campaigns in a row
do not come out as the same "observation → pitch → call?" email.

Follow-ups, sequence timing and channel mix are NOT here: that is `sequence-writer`.
This file is the first touch only.

## Rules that hold across all twenty-four

- **Subject of the email is them.** One sentence per email has "we/I" as the subject, and it
  is the proof sentence. Roughly 4:1 them-to-us on a five-sentence email.
- **≤ 90 words body, ≤ 6 words subject, lowercase-ish subject that reads like a colleague's.**
- **Ends with a real question.** "Curious whether…", "Let me know if…" are statements. Rewrite
  them as a direct question.
- **No call, slot or calendar ask in a first touch.** The CTA is one of three: interest
  ("is X a priority this quarter?"), permission to give value ("can I send the breakdown?"),
  permission for a personal teardown ("want me to mark up your pricing page?" — top accounts
  only, 20–40 min of work each).
- **Every number comes from data about this account or a named public source.** A format that
  needs a number the list does not have is not eligible. Never invent "73% of agencies".
- **No "Saw / Noticed / I came across" opener, no spintax, no dashes, no "not X but Y".**
- **One idea per email.** If the draft carries two pains, it is two formats; split it.
- **Placeholders `{{var}}` must map to a real column.** Before drafting, list the columns the
  format needs and check the list has them for ≥ 80% of rows.

## Anchor families

The anchor is what makes the email about THIS account. It decides eligibility first.

- **A · Signal** — an event with an expiry date (round, new exec, job post, launch,
  migration, a post they wrote). Short emails; the event does the work. Expires: send within
  the signal's window or drop it.
- **B · Data-point** — a fact about the account that only matters next to a comparison
  (their numbers vs peers, vs their own other number, vs a cost). No comparison, no email.
- **C · No anchor** — nothing account-specific. Relevance comes from a narrow segment, an
  open hypothesis, proof from a look-alike client, or a gift.

## Tone axes (from the tone of voice card, 1–5 each)

F formality · D distance · E emotionality · N fact density · H humour · K categoricity.
Each format lists the range it survives in. Outside the range it reads fake: a joke from a
sender at H=1, a hard challenge from a sender at K=1.

## Selection table

| # | format | family | needs per account | persona | tone fit | how it gets ruined |
|---|---|---|---|---|---|---|
| 1 | **Short Trigger** | A | event + date | any | any | the "so what" line missing; the email just reports their news back to them |
| 2 | **First 90 Days** | A | new exec, start date ≤ 90 d | the new exec | F 2–5 | congratulations as the whole first line |
| 3 | **Round → Hiring Math** | A | round size + date, open roles | CEO, CTO, COO | N ≥ 3 | math on numbers you guessed |
| 4 | **Job Post Mirror** | A | live vacancy title + days open | hiring manager, CTO | any | pitching against the hire ("don't hire, use us") to the person hiring |
| 5 | **Stack Shift** | A | migration / new tool / deprecation with date | CTO, VP Eng, Head of Ops | N ≥ 3 | naming the tool without the consequence for their team |
| 6 | **Launch Follow-through** | A | release / launch with date | founder, product lead | E 2–5 | praise of the launch with no next problem attached |
| 7 | **Post Reply** | A | their post or comment, ≤ 14 d | the author | any | quoting the post at length; one phrase is enough |
| 8 | **Audience Mirror** | B | their own engagement / traffic / review numbers, split two ways | founder who posts, marketing lead | N ≥ 4 | a split you cannot defend if they ask "how did you count?" |
| 9 | **Do the Math** | B | 2–3 inputs that multiply to a cost | CFO, COO, founder | N ≥ 4, K ≥ 3 | assumptions hidden; show each input in the email |
| 10 | **Peer Benchmark** | B | their metric + same metric for 3 named-type peers | VP, Head of | N ≥ 3, D ≥ 2 | peers that are not peers (10× their size) |
| 11 | **Gap Spotted** | B | one checked observation on their site / funnel / profile | founder, marketing, sales lead | K ≥ 2 | an "observation" that is a template line; must be something they can verify in 5 s |
| 12 | **Competitor Move** | B | named competitor action + date | founder, sales lead | K ≥ 3 | fear-mongering; state the move, ask how they read it |
| 13 | **Voice of Their Customer** | B | review / G2 / Clutch / Glassdoor quote about them | founder, delivery lead | E ≤ 4 | using a negative review to shame them |
| 14 | **Spend Signal** | B | ads running, ad count or traffic trend | marketing lead, founder | N ≥ 3 | reading intent into one ad |
| 15 | **Narrow Segment** | C | segment membership only (e.g. "20–50 people, UK, fintech clients") | any | any | the segment is wide; if it fits 10 000 companies it is not narrow |
| 16 | **Neutral Insight** | C | none; a pattern you saw across N similar companies | VP, Head of | N ≥ 3, K ≤ 4 | the pattern is a platitude ("sales cycles are getting longer") |
| 17 | **Open Hypothesis** | C | none | any, best for managers | K ≤ 3 | three questions; it must be one |
| 18 | **Look-alike Case** | C | a client result with a number, same segment | any | N ≥ 3 | the case is from another segment; it reads as "we did a thing once" |
| 19 | **Gift First** | C | an asset that exists before send | any | any | the gift is a brochure; it must be useful without ever replying |
| 20 | **Teardown Offer** | C (top tier) | account worth 20–40 min of work | founder, VP | any | offering the teardown to 500 accounts; it stops being personal |
| 21 | **Role Burden** | C | persona only | VP, Head of, C-level | F ≥ 2 | listing all their duties; name the one that hurts this quarter |
| 22 | **Why Are You Paying** | C | known category of spend (tool, vendor, headcount) | CFO, COO, founder | K ≥ 4 | sounding like a vendor attack; ask, do not accuse |
| 23 | **Right Person** | C | company only, persona unclear | manager, ops | F ≤ 4 | asking for a referral before saying what it is about |
| 24 | **One Picture** | B / C | a screenshot, chart or mock of THEIR thing | founder, marketing | E ≥ 2 | a generic image; if it could go to anyone it is a banner |

## Recipes

Each recipe: skeleton → sample (sample numbers in `[brackets]` are illustrations, never ship
them) → subject options → P.S. option. Samples use a dev agency selling to SaaS companies
because that is the most common client case; swap the segment, keep the skeleton.

### 1 · Short Trigger

```
{{event}} on {{date}}.
That usually means {{consequence for their team}} within {{time}}.
{{one line of proof: who we did it for, the number}}.
{{interest question tied to the consequence}}?
```
Sample: "Series A closed on [12 Oct]. That usually means the roadmap doubles before the
engineering team does. We covered that gap for [two SaaS teams] in [6 weeks]. Is the
roadmap ahead of the hiring plan right now?"
Subject: `after the series a` · `{{company}} roadmap`
P.S.: none; the email is short enough.

### 2 · First 90 Days

```
{{name}}, {{role}} at {{company}} since {{month}}.
Most {{role}}s in the first quarter get asked to {{the usual mandate}}.
{{the one thing that usually blocks it}}.
{{interest question: is that the mandate?}}
```
Sample: "Most new VPs of Engineering get asked for a delivery plan in the first 60 days. The
plan usually stalls on the two roles nobody can hire fast. Is the delivery plan the first
ask from your CEO?"
Subject: `first 90 days` · `your q1 plan`

### 3 · Round → Hiring Math

```
{{round}} on {{date}}, {{n}} engineering roles open on your careers page.
At {{days}} days to fill each, that is {{n × days}} days of roadmap waiting.
{{proof line}}.
{{question}}?
```
Show every input. Days-to-fill comes from their own job posts (date posted) or a named
source, never a guess.

### 4 · Job Post Mirror

```
Your {{vacancy}} role has been open {{days}} days.
Teams in that spot usually {{what they do meanwhile}}.
{{offer framed as covering the gap until the hire, never instead of the hire}}.
{{question}}?
```
Sample: "Your Senior React role has been open [41] days. Teams in that spot usually push the
frontend work to the backend people, and both slow down. We put a senior on the gap until
your hire lands. Would that help before Q1 starts?"

### 5 · Stack Shift

```
{{company}} moved from {{old}} to {{new}} in {{month}}.
The part that usually drags is {{specific migration pain}}.
{{proof}}.
{{question}}?
```

### 6 · Launch Follow-through

```
{{launch}} went live on {{date}}.
The next 60 days after a launch are usually {{the follow-on problem}}.
{{proof}}.
{{question}}?
```

### 7 · Post Reply

```
Your post on {{topic}} ({{date}}): "{{one phrase}}".
{{one line that adds to their point, with a number}}.
{{how we deal with it, one line}}.
{{question that continues their post}}?
```
Works best when the person asked something publicly. Pairs with a LinkedIn comment a day
before the email.

### 8 · Audience Mirror

The reference email this catalogue started from (a tool that reads who reacts to a creator's
posts). The prospect's own numbers ARE the subject line.

```
Subject: {{big number}}, {{segment number}} {{segment}}
{{segment number}} {{segment}} {{did what}} since {{date}}.
Your {{content type A}} pull {{x}} per {{unit}}, your {{content type B}} pull {{y}}.
I {{what you do}} for {{who}}, so they can {{outcome}}.
Want {{the list / the split}} with {{detail}}?
P.S. {{kills the main fear: access, cost, effort}}.
```
Sample: "Since [1 Sep], [214] CTOs and VPs of Engineering reacted to your posts. Your
case-study posts pull [31] of them per post, your hiring posts [10]. I track this for dev
agencies, so founders see which buyers already know them. Want the list with names and what
each one reacted to? P.S. Public data only, no access to your LinkedIn."
Eligibility: only accounts that post enough to produce a split. Filter the list first.
After "yes": deliver part of the list, keep the rest for a 15-minute walkthrough.

### 9 · Do the Math

```
{{input 1}} × {{input 2}} = {{cost}} a {{period}}.
{{what that cost is made of, in their words}}.
{{proof: we cut it to X for Y}}.
{{question about whether the number matches theirs}}?
```
Asking "does that match your number?" is the best CTA here: people reply to correct you.

### 10 · Peer Benchmark

```
{{metric}} at {{company}}: {{their value}}.
{{peer type}} of your size sit at {{peer value}} ({{source}}).
{{the usual reason for the gap}}.
{{question}}?
```

### 11 · Gap Spotted

```
{{observation they can verify in 5 seconds}}.
{{why it costs them, one line, number if you have it}}.
{{proof}}.
{{permission question: want me to send what we'd change?}}
```
Sample: "Your services page lists fintech, but the three case studies are all e-commerce.
Fintech buyers read that as no fintech work. We rewrote that page for [an agency your size]
and fintech demos went from [2] to [7] a quarter. Want the two changes I'd make first?"

### 12 · Competitor Move

```
{{competitor}} {{did what}} in {{month}}.
{{what it changes for buyers in their segment}}.
{{question asking how they read it}}?
```
No pitch in the first email at all. The reply opens the pitch.

### 13 · Voice of Their Customer

```
A client of yours on {{platform}}: "{{short quote}}".
{{what that quote says about what buyers value / fear}}.
{{proof}}.
{{question}}?
```
Prefer positive quotes ("they shipped on time") and build on them.

### 14 · Spend Signal

```
{{company}} has run {{n}} {{ad type}} ads since {{date}}, all pointing to {{page}}.
{{what usually happens after the click on that kind of page}}.
{{proof}}.
{{question}}?
```

### 15 · Narrow Segment

```
{{segment described so precisely they feel picked}}.
{{the problem specific to that segment}}.
{{proof inside the segment}}.
{{question}}?
```
Sample: "UK dev agencies of 20 to 50 people with fintech clients have one recurring problem:
compliance reviews stretch every release by two to three weeks. ..." Test: could this first
line go to 10 000 companies? Then it is not narrow.

### 16 · Neutral Insight

```
Across {{n}} {{segment}} we {{looked at / worked with}}, {{pattern}}.
{{the counter-intuitive part}}.
{{question whether it matches what they see}}?
```
No pitch. Positions the sender as someone who has seen the data.

### 17 · Open Hypothesis

```
{{one-sentence hypothesis about their situation}}.
{{why you think so: segment, size, stage}}.
{{direct question: is that true for {{company}}?}}
```
One question only. Avoid the hedge "or am I way off": it lost in tests (≈21% vs 30%).

### 18 · Look-alike Case

```
{{client type like them}} had {{problem}}.
{{what changed, with the number and the time}}.
{{why it might apply to them: shared trait}}.
{{permission question: want the two-page breakdown?}}
```
The case must share at least two traits (size, segment, geo, stack). Otherwise use 16.

### 19 · Gift First

```
{{asset name}}: {{what it gives in one line}}.
Made it for {{segment}} after {{n}} {{projects/audits}}.
{{permission question: want it?}}
```
The asset exists before the first send. Useful without a reply.

### 20 · Teardown Offer

```
{{one specific thing on their site / funnel / product}}.
I'd {{record a 90-second Loom / mark up the page}} on what I'd change first.
{{permission question}}?
```
Top tier only. 20–40 minutes of work per "yes"; plan capacity before sending.

### 21 · Role Burden

```
{{role}}s at {{company stage}} usually own {{one outcome}} this quarter.
{{the part of it that eats the most time}}.
{{proof}}.
{{question}}?
```

### 22 · Why Are You Paying

```
Most {{segment}} pay for {{spend category}} {{how}}.
{{what they get vs what they pay, numbers}}.
{{question: is that how it works at {{company}}?}}
```
High categoricity senders only. Ask, never accuse.

### 23 · Right Person

```
{{what it is about, one line, with the outcome}}.
Is that you, or {{the role you think it is}}?
```
Two sentences. Good for unclear org charts and as a fallback lane in any campaign.

### 24 · One Picture

```
{{image of THEIR thing: chart from their data, marked-up page, mock}}
{{one line on what the picture shows}}.
{{question}}?
```
Plain-text emails deliver better; send the image as a link to a hosted page, or keep this
format for warm accounts and LinkedIn.

## P.S. patterns (optional, max one)

- **Fear killer**: removes the main objection to replying ("No login needed", "No call needed").
- **Second proof**: one more number from a different client.
- **Soft exit**: "If it is not you, who owns {{area}}?" (only when the main CTA is not 23).

## Tone dial: how a sentence moves along each axis

| axis | low (1–2) | high (4–5) |
|---|---|---|
| F formality | "Quick one on your React hire." | "A short note regarding the open Senior React position." |
| D distance | "I'd do X first." | "Teams in your position typically start with X." |
| E emotionality | "The hire is taking 41 days." | "41 days is a long time to carry a frontend gap." |
| N fact density | one number in the whole email | a number in every sentence but the CTA |
| H humour | none | one light aside, never in the subject |
| K categoricity | "might be worth a look?" | "this costs you two releases a quarter." |

Change wording along the axes; never change the skeleton. The skeleton is what was tested.

## Sources

Formats 1, 9, 12, 16, 17, 19, 21, 22 adapt patterns from the `cold-email-playbook` skill in
this pack (its `resources/copy-frameworks.md`), credited there.
Format 8 adapts a cold email shared on LinkedIn by a sales coach in Nov 2026 (product that
maps post reactions to buyers). The A/B/C anchors and the three CTA tiers come from the author's
multichannel sequence method (see `sequence-writer`).
