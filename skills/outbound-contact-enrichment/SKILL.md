---
name: outbound-contact-enrichment
description: Turns a list of company domains into named decision-makers with verified work emails and LinkedIn URLs, using a Freckle workflow over Apollo with a fallback cascade for misses. Use when the user says "заенрич", "знайди персон", "find contacts", "потрібні пошти", "who do we write to at these companies", or has an account list that needs people on it. Requires the Freckle CLI.
---

# Contact Enrichment

Domains in, people out: name, title, LinkedIn URL, work email, and the verification status of that email.

## Why one node beats a scraper

A LinkedIn employee scraper crawls dozens of pages per company, needs a session cookie, breaks often, and still hands back profiles without emails. A people-search node keyed on domain returns the same people with contact data attached, in about a minute for ten domains. Reach for the scraper only when the provider has no coverage.

## The workflow

One node: `apolloFindPeople`. Draft it once, save it, invoke it per domain.

`assets/find-people.yaml` in this skill is the draft. Create it with:

```bash
export FRECKLE_ORG_ID=<your-org-id>
freckle workflow draft validate --file assets/find-people.yaml
freckle workflow saved create --file assets/find-people.yaml \
  --label "Find engineering leaders by domain"
```

Then invoke per domain:

```bash
freckle workflow saved invoke <workflow-id> --json '{
  "request": {
    "include_similar_titles": true,
    "numResults": 2,
    "q_organization_domains_list": ["example.com"],
    "person_titles": ["CTO","VP of Engineering","Head of Platform","Director of Engineering"],
    "person_seniorities": ["c_suite","vp","director","head"],
    "person_locations": ["United States"]
  }
}'
```

**One domain per invocation.** A single call with ten domains and `numResults: 20` does not guarantee two people per company — it returns twenty people distributed however the provider likes. Loop instead.

## Who to ask for

Two people per account, not five. The pair you want is the one your ICP already describes:

- **economic buyer** — CTO, VP Engineering, or the founder in companies under ~80 people
- **technical approver** — Head of Platform, Director of Engineering, Lead Backend

When both come back for the same company, that is a live check on the persona work: the roles you invented on paper exist in the real target base. When they consistently do not, the persona section is wrong — fix it before writing copy.

## Handling misses

Expect roughly one company in ten to return nothing, and the occasional person to return `email_status: unavailable`. That is coverage, not a broken query. Confirm by relaxing once: drop the location filter, widen titles, add the `manager` seniority. If it is still empty, the provider has no data.

Route misses to a second cascade keyed on the LinkedIn URL:

```
profile lookup (provider A) → fallback (provider B)
      ↓
email finder (provider C) → fallback (provider D)
      ↓
validation
```

Budget it at roughly 1.4 credits per person. Both fallbacks earn their place — in practice the first provider misses often enough that removing either one loses people.

## Do not

- **Do not guess email patterns.** `first.last@domain` looks free and poisons a domain's reputation on every bounce. Unverified is worse than missing.
- **Do not fill a blank with a plausible name.** A missing contact is a data gap; an invented one is a wrong send.
- **Do not enrich the whole list before the account filter runs.** Enrichment is the expensive step; spend it on accounts that already passed.

## Output

CSV: `domain · company · name · title · seniority · email · email_status · linkedin`

Report: people found, share with an email, share verified, companies with zero coverage, and total credits spent.

## Requirements

| Integration | Used for | Required? | Setup |
|---|---|---|---|
| Freckle CLI | workflow authoring and invocation | yes | `freckle auth login`, then pin `FRECKLE_ORG_ID` |
| Apollo (via Freckle) | domain → people with email | yes | connected inside Freckle |
| Email-finder cascade | misses and unavailable statuses | no | second workflow |
