# The email track

## Before the first email

The usual picture: the team rewrites the subject line for a third week while the
emails simply do not arrive. Copy does not cure that.

- separate sending domain; the main domain is not touched. 3–5 domains, 2–3 mailboxes each
- a working page or a 301 to the main site on every sending domain
- SPF, DKIM, DMARC. `p=quarantine` minimum, then `p=reject`
- warmup 2–4 weeks: start at 5–10 emails/day, settle at 25–30 per mailbox
- list validated by two services, bounce under 2%
- open tracking off — the pixel and the redirect domain cost more than the metric returns
- physical address and an unsubscribe path in the signature (CAN-SPAM, US)

### Sender rules that changed the math

| When | What changed |
|---|---|
| Feb 2024 | Google and Yahoo: senders above 5,000/day to consumer addresses must have SPF, DKIM, DMARC, one-click unsubscribe; complaints under 0.3%, recommended under 0.1% |
| May 2025 | Microsoft extended the same requirements to outlook.com, hotmail.com, live.com. Non-compliant mail is rejected with `550 5.7.15`, not filed in spam |
| Nov 2025 | Gmail moved to permanent 550 rejections for non-compliant traffic; Postmaster Tools v2 shows a compliant / non-compliant status |
| Jan 2026 | Gemini inside Gmail. A second gate after delivery: the email arrived and may still never be shown |

UK: companies and LLPs are corporate subscribers, legitimate interest applies.
Sole traders and partnerships are treated as individuals. Objections are honoured
immediately, and the suppression list is one list across every domain and client.

### Capacity, computed before the segment is chosen

**mailboxes x 25 emails x 20 working days = monthly sending ceiling.**

Divide by the number of emails in the sequence to get the contacts per month you
can physically carry. Three mailboxes and a five-email sequence is roughly 300
contacts a month. Not 3,000. Every percentage in the plan is computed off that
number.

---

## Anatomy

Subject → anchor → hypothesis → problem → proof → question → P.S.

Identical for all three anchor types. Only the first sentence changes.

### 1. Find the anchor

One observation, used across every email in this persona's sequence. One, not
three. A sequence where each email opens with a new pretext reads as three
different campaigns from three different people.

### 2. Write the first sentence

It decides whether the second one gets read. Two depths:

- Level 1: Saw, Noticed…
- Level 2: Read, Listened to, Watched, Met…

Seeing is cheaper than reading. If you put in the effort, say so — they will not
guess. Working openers:

> Read your LinkedIn post about your new role…
> Listened to the podcast episode you were in with ACME…
> Noticed you've hired 3 new SDRs this quarter…

Most senders spend the first line on garbage — *Hope this reaches you well… I'm
Victor from XYZ…* That is how 90% of cold emails open. Not being in that 90% is
enough to stand out. Strongest move: go straight to the observation, no run-up.

### 3. Link the observation to a hypothesis

This is where most SDRs break. Finding the observation is easy; connecting it to
the problem you solve is not. So study client problems — you already know your
own services.

**"I did… I bet" frame:**

> Read on your company's LinkedIn page that [observation]
> I bet you're thinking about how to [problem that follows that event]

Filled in:

> Saw you closed the $18M round on July 28 and opened five backend roles the same week.
> I bet the roadmap you raised on assumes those five start now.

### 4. Problem

Often skipped. Include it if you want replies. It does three things: makes the
current situation feel bad, shows the status quo is not the best option, and
raises the cost of doing nothing.

The status quo is what your competitors do and promise — to stand out, move away
from their phrasing.

> Most teams that size end up pulling their senior engineers into interviews and lose a sprint a month to it.

### 5. Proof

The most relevant client example from the same sub-vertical. One story, one
logo, one result, and the client is the subject of the sentence, not you.

- Bad: *We helped ABC achieve…*
- Good: *VPs use [solution] to achieve…*

> Product teams use an outside squad to hold the release date while their own hiring catches up.

One strong story beats ten irrelevant mentions. The target thought is "they get
the result I want".

### You-approach — the subject of the sentence is them

The prospect does not know you. Your services and features are not what they are
weighing; whether their problem gets solved is. Every sentence opening with "we"
spends their attention and returns nothing for it, and a 75-word email has no
credit for that.

**The threshold, and it is countable:** one sentence per email may take you or
your company as its subject. One, and it is the proof sentence. Everything else
belongs to them: their event, its consequence, the question put to them. In a
five-sentence email that lands around 4:1. Checking it takes half a minute and
does not depend on anyone's taste.

| Subject "we" | Subject "they" |
|---|---|
| We help IT companies close senior roles faster. | Your three senior Node roles have been open since May. |
| We provide dedicated development teams for product companies. | The second track runs end to end while your own team stays on the core product. |
| I am Victor, founder of X. We specialise in mobile development. | Saw the mobile app hasn't shipped since January while the web side moved twice. |

**Two exceptions, both inside the conversation.** When they ask about you —
how many engineers, how your process works — answer directly and briefly;
deflecting back to their side is out of place there. And the proof sentence
itself describes work you did: a client from the same sub-vertical, a number, a
timeframe. That is the one sentence above. The signature is yours too and does
not count.

The rule does not rescue an email with no anchor. Writing to someone who does not
have your problem, an inverted subject changes nothing. It works the other way
round: it keeps you from ruining an email whose anchor is already there.

### 6. The question

All questions go at the end — that way you never ask more than one. Its meaning:
"was what I wrote above useful enough to answer?"

**No call, no meeting, no calendar slot. Anywhere in the sequence.** Asking for a
call demands a decision the person is not ready to make; you force a "no" before
they understand the subject. The call arrives after they reply.

#### The soft CTA is three different blocks

| Block | What you ask | What it costs you | What "yes" means |
|---|---|---|---|
| 1. Interest | whether the topic is live at all | nothing | they acknowledged the problem, owe you nothing |
| 2. Permission to send value | whether you may send a guide, breakdown, benchmark | one asset, prepared once per sequence | they agreed to read something; you have a reason for email 2 |
| 3. Permission for a personal teardown | whether you may build something for them specifically | 20–40 minutes of your work each | strongest signal: they will look at their own numbers |

**Block 1 — interest.** Cheapest, weakest. Ask about the problem, not yourself:

> Is this a priority right now?
> Is this something you're looking at this quarter, or is it parked?
> Does this sound like the bottleneck on your side, or am I off?
> How is hiring affecting the roadmap right now?

**Block 2 — permission to send value.** Same asset for the whole segment. Ask
permission, do not push the file:

> Can I send the two-page breakdown of how 12 teams split this?
> Want the benchmark of what this costs teams your size?
> Should I send the case study? One page, no pitch.
> Want the 4-point scorecard to check whether the five hires pay back?

The cheapest asset in this block is a scorecard or checklist of four points:
half a page, no design, and the reader checks their own numbers against it
before anyone talks. It is prepared once per sequence like any other asset.

**Block 3 — permission for a teardown.** Built per company, so used only on top
accounts or after a signal:

> Want me to mark up your roadmap and show where teams your size lose the sprint?
> Can I record a 90-second Loom on your current mobile release and where it stalls?
> Should I put together what your integrations track would cost with an outside squad against a hire?

#### Questions that are removed

do you have 15 minutes? · how does Tuesday at 3 look? · worth a quick call? ·
worth a chat? · shall we book a chat? · would you be open to exchange 20
minutes? · let's explore synergies · have a look at this 30-minute video · any
calendar link in a first touch · statements disguised as questions ("curious
whether…", "wondering if…", "let me know if…") — there is nothing to answer.

"Worth a chat?" asks for a call in shorter words; that is why it is on this list.
A video is offered, not demanded, and it is 90 seconds, not 30 minutes.

Also: **never name a start date in a cold email.** "We can start Monday" reads as
pressure and as an empty bench.

---

## Variants per block

The anatomy above is fixed. What varies is the angle each block takes on the
same anchor. A variant is named, written out in full, and chosen by anchor type,
persona and step. Not spintax: a sequencer picking a clause at random inside one
email produces an email nobody wrote, and the reply rate of that email cannot be
read. Two full variants of email 1 and two of email 2 go into the sequencer as
step variants per persona and are A/B'd on the sample size in
`references/benchmarks.md` (500 contacts per variant minimum; 300 reads only as a
direction).

**The anchor never changes inside a sequence.** Only the angle on it: email 1
restates it as a cost, email 2 adds a second consequence or reframes the metric,
email 3 carries the asset, email 4 a peer number. Four emails, one observation.

Every example below uses one anchor: *five SDR openings posted this month*.
Swap it for yours; the shape stays.

### Anchor / first line

| Variant | Use when | Example |
|---|---|---|
| I did… I bet | default for type A and B | Saw the five SDR openings posted on the 3rd. I bet the Q1 pipeline number assumes they start now. |
| Trigger → cost | type A with a salary, sprint or quarter attached | Five new SDRs is five salaries paid out before the first qualified opportunity shows up. |
| Their own words | the posting or post states the problem itself | "Own the outbound motion end to end" — that line in the SDR posting usually means nobody owns it today. |
| Question-first | champion persona, type C | Who runs outbound while the five SDR seats stay empty? |

### Problem / agitate

| Variant | Use when | Example |
|---|---|---|
| Cost of time | decision-maker with a quarter or roadmap date | Ramp takes four months; the quarter you hired them for ends in three. |
| Cost of money | decision-maker who owns the budget, type B | Five ramping SDRs cost about $90k a quarter before the first qualified opportunity. |
| Risk / no guarantee | after a hiring round | Five hires carry no guarantee: the first one to leave takes a quarter of ramp budget with them. |
| Status quo "most teams end up…" | type C, segment insight | Most teams that size end up with the founder writing the sequences at midnight. |

### Proof

| Variant | Use when | Example |
|---|---|---|
| Peer + number + timeframe | default, the client allows the name | A 40-person SaaS team in the same segment booked 11 qualified opportunities in the first 60 days with an outside squad. |
| No-logo "teams your size" | NDA, no logo allowed | Teams your size in this segment see the first qualified opportunity in week three when an outside squad takes the first touch. |
| Single outcome | the number is the whole story | One client cut cost per qualified opportunity from $1,400 to $600 inside a quarter. |

### Email 2 opener (reply in thread)

| Variant | Use when | Example |
|---|---|---|
| One thing I missed about <trigger> | default for email 2 | One thing I missed about the five SDR openings: the ramp period lands on the same quarter as the pipeline target. |
| The real test reframe | decision-maker who watches one dashboard metric | Activity dashboards cannot show whether five new SDRs pay back. The real test is qualified opportunities per rep in month four. |
| Second consequence | type A, the trigger has more than one cost | Five open SDR seats also means the current reps cover five territories until the seats fill. |
| Peer number | the proof in email 1 was no-logo | A peer team in the same segment needed 4.5 months to get five new SDRs to quota. |

The follow-up bridge and the cost-restated opener are from a published annotated
example by Alan Ruchtein.

---

## Subject line

Lowercase · three words or fewer · very concrete · describes their problem, not
your service. Literally the object you discuss in the body.

- Bad: Increase efficiency using AI · Join our next high-efficiency workshops · Sell more with our best-in-class sales tool
- Good: sdr cold emails · Q2 pipeline · billable headcount · react native roles

---

## P.S.

**Personal.** Something they published themselves: a talk, an article, a photo
from a site, a place in an industry ranking.

> PS. Saw your changelog note on moving off the monolith. The staged cutover is the part most teams skip.

Pets, children, hobbies and "saw your holiday photo" are not in this category.
From an unknown vendor in another country that reads as surveillance, not warmth.

**Redirecting.** Points at another channel of yours.

> PS. Sent you a connection request on LinkedIn — I think you'll get value from my posts there.

**Inviting.** Introduces a marketing activity.

> PS. Running a session next month on how product teams split the roadmap between in-house and an outside squad.

---

## Cadence

Belkins, 7.5M cold emails in 2025: **58.6% of replies land on emails 2–6, and the
third email produces 35.6% of all meetings** — more than the first and second
combined. The 2024 deck advice of 8–12 touches is dead: the same deck says the
first four touches carry 80% of replies, and touches 5–12 are bought with
contacts you will now never reach, because the mailbox ceiling is fixed.
**2026 bet: four emails plus a close.**

| Day | Touch | Content | Length |
|---|---|---|---|
| 0 | Email 1 | anchor, hypothesis, problem, proof, question | ≤ 75 words |
| 3 | Email 2, reply in thread | same anchor, another consequence | ≤ 50 |
| 8 | Email 3, reply in thread | asset: "put together two pages on how 12 firms do it, send it?" | ≤ 45 |
| 14 | Email 4, reply in thread | another angle: one number from a client in the same sub-vertical | ≤ 35 |
| 21 | Email 5, new subject | close. No guilt, no "last chance" | ≤ 25 |

Emails 2–4 are replies inside the same thread. Email 5 gets a new subject: if the
first four sat in spam, the thread leads nowhere, and the close is the last
attempt to appear in front of the person. (Nobody has published a controlled
measurement of same-thread vs new-thread; this is a convention with a plausible
explanation.)

### Follow-up openers that are removed

just circling back · bumping this · in case it got lost in your inbox · I know
you're busy / you must get hundreds of emails · could you spare 15 minutes ·
any thoughts?

Each of these tells the reader the email carries nothing new, so the reply rate
of the follow-up drops to that of a nudge. Email 2 opens with a bridge that names
what is new: *One thing I missed about <trigger>:* or the real-test reframe
(see Variants per block). "Worth seeing how they did it?" reads as a demo ask
and becomes "Want me to send how they did it?".

### Compression to the signal window

A 21-day sequence does not work for a signal with a 72-hour shelf life. **Divide
the window by the number of emails:**

| Signal window | Schedule |
|---|---|
| up to 7 days (a post, a fresh award) | 3 emails: days 0, 2, 5. Then stop |
| 7–30 days (open roles, a release) | 4 emails: days 0, 3, 8, 12 |
| 30+ days (new hire, funding round) | the full sequence above |

When the window closes, the sequence stops even if emails remain. Writing into
the void burns a contact you would otherwise return to next quarter with a new
signal.

---

## What happens with a reply

If you are not asking for a call, you must say what happens next — otherwise the
sequence ends exactly where the work begins.

**The asset exists before launch.** Every interest CTA is a promise of a specific
file: a breakdown, a benchmark, two pages of numbers, a 60-second video. One
sequence, one asset. No asset, no CTA.

**"Yes, send it."** Send it immediately. No form, no registration, no "let's have
a short call first to understand the context". The email carrying the asset ends
with one question that opens the next step — about their process, not your service.

**From asset to call.** Ask for the call on the second or third reply, once they
have reacted to the substance. A question that cannot honestly be answered in
writing works best: *"how is the roadmap split between your own team and an
outside one right now?"*

**Replies that look like a refusal.** For outsourcing in the US and UK most first
replies sound like this:

- *"wrong person"* → route to the right one, ask for the name
- *"we only hire in-house"* → you just learned their model, and it breaks on hiring timelines; ask what carries the roadmap while the roles are being filled
- *"we already have a vendor"* → ask what that vendor does not cover, and who runs the tracks they cannot staff
- *"we don't work with anyone we haven't worked with"* → ask about a pilot on one track instead of a team

Only one reply is a real refusal: *"do not write to me"*. Honour it immediately
and permanently, across every domain and campaign.

**Deadline.** A reply is handled the same working day. This model makes the reply
the conversion point, so the sequence needs a person reading the inbox daily. If
there is no such person, the campaign does not launch.
