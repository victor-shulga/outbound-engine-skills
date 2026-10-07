# Cold-email benchmarks and operating rules

Every number below names where it came from. Four source groups are used:

- **ColdIQ playbook**: ColdIQ's cold email playbook, built on 250K+ emails sent and 73 prospect calls,
  published in ColdIQ's public GTM skills.
- **GEX lessons**: 25 lessons from Growth Engine X, an agency sending 1.5-2M emails a month for 40-50
  clients (10M+ emails in total), as collected in ColdIQ's public GTM skills.
- **Playsheet**: "The 1% Cold Email Playsheet" by ColdIQ (Michel Lieben) with Instantly.
- **[Practitioner]**: Victor Shulga's operating rules for B2B service companies. Rules of thumb, not
  data.

Agency figures describe well-run programmes with tight lists. For a first campaign, plan on the
conservative numbers and treat the agency figures as a ceiling.

---

## 1. Benchmarks

| Metric | Figure | Source |
|---|---|---|
| Average cold-email reply rate | 3.43% | Playsheet (Instantly sending data) |
| Top senders' reply rate | 10%+ | Playsheet |
| Planning reply rate for 2026 | about 1.5% | [Practitioner] |
| Positive replies as share of all replies | at most about 20% | [Practitioner] |
| Positive reply rate, tight lists | 5-8% | ColdIQ playbook (target, denominator not stated) |
| Meeting book rate | 2-4% | ColdIQ playbook (target) |
| Open rate, when tracked | 40-60% is healthy; under 30% points to placement | GEX lessons |
| Reply rate, generic cold vs signal-based vs several signals | 6-8% vs 18-22% vs 35-40% | GEX lessons (their programmes) |
| Share of replies that come from follow-ups | about 42% | Playsheet |
| Gap between best and worst copy variant | up to 13x | ColdIQ playbook |
| Bounce rate | under 2% healthy, over 5% pause | Playsheet; ColdIQ infrastructure module |
| Spam complaint rate | under 0.1%, never 0.3% | Google email sender guidelines |
| Call → paid client | at least 15% | [Practitioner] |

Volume check [Practitioner]: at 1.5% replies and 20% of those positive, about 0.3% of contacts turn
positive, so 20 positive conversations need roughly 6,700 contacts. The expensive part of a cold test
is the domains and warm-up, the proof assets and the person handling replies; sending itself is cheap.

A segment or hypothesis that reached fewer than 300 contacts is **not tested** [Practitioner].

## 2. Writing rules (ColdIQ playbook unless marked)

- Write for the 97% who will not reply: short, easy to skim, nothing to decode.
- About 60-90 words for the first email; the playbook found 70-90 the sweet spot.
- Plain text, one ask, no images, no tracked links in the first email.
- Subject and preview read as one thought; the subject can sound like it came from a peer or a
  potential customer. Keep subjects short (seven words or more is too long).
- Segment-level personalisation beats one-by-one personalisation at scale on effort per reply.
- Soft, interest-based asks beat time asks.
- Common misses: one copy for every persona; the email is about the sender; "helping {{company}}
  grow"; "quick call?"; capitals and promo words.
- Before using a signal, run the "so what" test: is it recent, does it connect to the offer, would
  they care?

## 3. Sequence rules (GEX lessons unless marked)

- Two or three emails. The first email does most of the work; each extra step adds less and raises
  complaint risk. The ColdIQ playbook also found two-step sequences strongest.
- Three to five days between emails; one day is too short.
- Change the value angle between emails (cost, revenue, time) instead of repeating the first email.
- The last email lowers the ask or asks for the right person; no guilt-trip breakups.
- When AI writes part of the email, show where a fact came from ("according to <public source>"), so a
  wrong figure is the source's error. Let AI write one variable part; keep the rest fixed so tests
  stay readable.
- Small markets (under about 20,000 people): cover the whole list on one channel at a time (email,
  then phone, then LinkedIn, then mail for the rest) instead of tightly threaded multi-channel
  timing.
- Recent triggers: a job change still works but is widely used; social signals (the prospect posting or
  engaging on a topic) outperformed the "logical" triggers in GEX's tests.

## 4. TAM reuse

People forget an email within minutes, and their priorities shift within a quarter. GEX's rule: plan to
work through the whole addressable list every three months and then start again with new copy.

```
new contacts per working day = contacts in TAM ÷ ~60 working days
```

Example: 6,000 contacts in the TAM means about 100 new contacts a day to complete a cycle each quarter.
Check that against sending capacity (see `email-infra.md`, sizing). If capacity is lower, the cycle
gets longer; if the TAM is far smaller than capacity, the list is the bottleneck, so widen the ICP or
go deeper per account (2-3 contacts per company).

Before re-mailing, remove anyone who replied, bounced, opted out or became a customer.

## 5. Golden ICP

Broad filters ("20-500 employees, marketing director") group together companies that buy for different
reasons. A Golden ICP is the narrow slice where several signals are true at once.

How to build it:
1. List the 3-5 signals that most predict a need for the offer.
2. Order them by importance and by cost to check. Run the most important signal first and stop
   enriching an account as soon as a required signal fails (a waterfall), so no budget goes to dead
   rows.
3. Count how many signals are true per account and change the message by count: three signals justify
   a specific, confident first line; one signal gets a lighter, question-led one.

Example for a B2B service company selling engineering capacity: (1) hiring for the role the service
replaces, (2) won new work recently (tender award, permit, new client announcement), (3) team growth in
the last six months. Accounts with all three go first.

GEX built this with a spreadsheet-style enrichment tool; any tool that supports conditional steps
works.

## 6. Seasonal dips (ColdIQ infrastructure module)

| Period | Typical drop |
|---|---|
| December holidays | 20-30%, back by mid-January |
| July-August | 10-20% |
| Last weeks of a quarter | lower response while buyers close their own deals |
| The sector's main conference week | 15-25% |

Investigate only when a drop is larger than this or does not recover on schedule.
