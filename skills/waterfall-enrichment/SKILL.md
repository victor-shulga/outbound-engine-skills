---
name: waterfall-enrichment
description: Turns company domains into named decision-makers with verified work emails, or finds emails for contacts you already have — a people-search node keyed on domain, then a multi-source email cascade with a known cost per contact. Use when asked to enrich a list, find contacts or emails, work from LinkedIn URLs, or raise find rate without guessing patterns. Triggers include "заенрич", "знайди персон", "потрібні пошти", "find contacts", "who do we write to at these companies".
---

# Waterfall Enrichment

Find verified emails by running sources in sequence and stopping at the first verified result.
The point of a waterfall is not coverage alone — it is **coverage at a known cost per contact**.
A cascade without prices is a list of vendor names.

## Two entry points, two different cascades

Which one you are in decides everything downstream.

**Entry A — you have name + company domain.** The normal case. Email finders take exactly this.

**Entry A2 — you have domains and no people yet.** Find the people first, then run the email cascade
on whatever comes back without a verified address. See the next section.

**Entry B — you have a LinkedIn profile URL and nothing else.** Common after list building, and the
one most cascades get wrong: email finders take a name and a domain, not a URL. This needs **two
stages** — resolve the profile to name + company + domain first, then run the email cascade. A
single-stage waterfall on a URL input returns near-zero and looks like a coverage problem when it
is a plumbing problem.

## Finding the people (Entry A2)

**One people-search node keyed on domain beats a profile scraper.** A scraper crawls dozens of pages
per company, needs a session cookie, breaks often, and still returns profiles without emails. A
people-search node returns the same people with contact data attached, in about a minute for ten
domains. Reach for a scraper only where the provider has no coverage.

**One domain per invocation.** A single call with ten domains and a result cap of twenty does not
give you two people per company — it returns twenty people distributed however the provider likes.
Loop over domains instead.

**Ask for two people per account, not five.** The pair you want is the one the ICP already names:
the economic buyer (in smaller companies, often the founder) and the technical or functional
approver who will be asked "is this real?". When both come back for the same company, that is a live
check on the persona work — the roles invented on paper exist in the target base. When they
consistently do not, the persona section is wrong, and it is cheaper to fix it now than after the
copy is written.

**Expect roughly one company in ten to return nothing**, and the occasional person to come back with
an unavailable address. That is coverage, not a broken query. Confirm it by relaxing the query once —
drop the location filter, widen the titles, add one seniority level. Still empty means the provider
has no data, and the account goes to the LinkedIn-URL cascade or to a manual queue.

A worked implementation over a workflow runner sits in `assets/find-people.yaml`, with the invocation
and role filters documented alongside it.

## Pass 0 — audit the input before spending anything

Whatever the client handed over, check it first. On a real base, of 131 addresses in the client's
email column only 27 carried their own company domain, 76 carried a foreign domain (personal
addresses, a partner's, an agency's), and 19 were not addresses at all — one read "write in April".

Check for:
- addresses whose domain does not match the account's domain
- free-mail addresses where a work address was assumed
- non-address text in the address column
- rows already carrying a verified address — do not re-buy them

A base that arrives broken gets rebuilt, not enriched on top of.

## The cascade

Stage 1 — **profile resolution** (Entry B only):

| Order | Source | Typical cost | Notes |
|---|---|---|---|
| 1 | Cheap profile resolver | ~0.09 credits | fails often; it is cheap enough to try first |
| 2 | Full-price person enrichment | ~0.37 credits | fallback, high hit rate |

Stage 2 — **email finding**:

| Order | Source | Typical cost | Strength |
|---|---|---|---|
| 1 | Primary finder (LeadMagic or equivalent) | ~0.37–0.4 credits | broad coverage, cheapest of the finders |
| 2 | Secondary finder (Findymail or equivalent) | ~0.45–0.6 credits | picks up what the first misses |
| 3 | Contact card already in your own tooling (Apollo export, CRM) | 0 | free — check it before paying |
| 4 | Domain pattern + validation | 0 | only where the pattern is known and confirmed on 2+ known addresses |

Stage 3 — **validation**:

| Source | Typical cost | Rule |
|---|---|---|
| Validator (ZeroBounce or equivalent) | ~0.09–0.3 credits | run on **every** result, including free ones |

**Budget ceiling:** roughly **1.4 credits per person** for the full two-stage path. Quote the run
before starting it.

## Rules

1. **Stop at the first verified result.** Move to the next source only on a miss or on
   "risky / unknown".
2. **Do not drop the fallbacks because the first source usually wins.** On the first live run of the
   two-stage cascade: the cheap resolver missed and the paid one hit; then the primary finder missed
   and the secondary hit. Both fallbacks earned their slot in a single run of one contact.
3. **Check free sources before paid ones.** An existing contact card or CRM record costs nothing and
   is often already there.
4. **Do not put a research or web-browsing agent in a contact cascade.** They do not reliably pull
   emails and phone numbers off the open web, and they cost more per attempt than a finder.
5. **Accept "valid" only.** Reject risky, unknown. Catch-all is a separate bucket, not a rejection.
6. **Catch-all domains:** sendable at lower confidence. Flag them, send in a small batch first, and
   watch that domain's bounce rate before scaling.
7. **Never send to unvalidated addresses.** A 5% invalid rate is enough to damage sender reputation,
   and the damage outlives the campaign.
8. **Spend on the top tier first.** Enrichment budget follows the queue — do not fund addresses for
   rows that will never be written to.

## Expectations

- 50–70% verified on a clean base with correct domains is a normal outcome. Above that, check whether
  the validator is being run at all.
- Below 50%, the input is usually the problem, not the sources: malformed names, wrong domains,
  holding-company domains instead of operating ones, or contacts who genuinely have no work address.
- The second finder typically adds 10–20 points over the first alone. That is what pays for it.

## Output format

```
Waterfall enrichment: [list name]
Date: [date]
Contacts processed: [n]
Entry point: [name+domain / LinkedIn URL]

INPUT AUDIT
Rows arriving with an address: [n] — own domain [n] / foreign domain [n] / not an address [n]
Rows already verified (skipped): [n]

RESULTS
Verified: [n] ([%])
Catch-all (sendable, lower confidence): [n] ([%])
Not found: [n] ([%])

SOURCE BREAKDOWN
[source]: [n] found — [credits spent]
...
Free sources (CRM / existing cards): [n] found — 0

VALIDATION
Valid: [n] | Risky/invalid removed: [n]

COST
Total credits: [n] | Per verified contact: [n]

Final clean list: [n] contacts ready for sequencing
```

Cost per **verified** contact is the number that matters. Total spend divided by rows processed
flatters a bad run.

## Notes

- Attribute every address to the source that found it. When deliverability turns bad later, source
  attribution is how you find out which vendor to drop.
- Re-running a waterfall over rows that already failed all sources rarely produces anything. Re-run
  after the input is fixed, not on a schedule.
- Role addresses (info@, hello@, sales@) are not contacts. They belong in a separate column, never in
  a personal-address campaign.

## Requirements

| Integration | Used for | Required? | Setup |
|---|---|---|---|
| A workflow runner with a people-search node (Freckle over Apollo, or equivalent) | domain → people with contact data | for Entry A2 | authenticate, then pin the org id |
| Email finders (LeadMagic, Findymail, or equivalents) | the email cascade | yes | your own accounts |
| Validator (ZeroBounce or equivalent) | every result, including free ones | yes | your own account |
| Profile resolver | the LinkedIn-URL entry point | for Entry B | part of the same runner |
