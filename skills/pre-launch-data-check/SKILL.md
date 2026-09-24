---
name: pre-launch-data-check
description: The last stop-filter before a list goes into the sender. Checks the final file (after enrichment and personalization) across seven layers (source and suppression, address validation, variable completeness, routing, hygiene, signal freshness, activation and capacity) and returns GO, GO WITH FIXES or STOP with the exact rows to fix. Ships a standard-library Python script so the verdict is counted, not guessed. Use when asked to check a list before launch, "is this base ready to send", "перевір базу перед запуском", "можна заливати в Instantly", "pre-launch check", "data integrity scan", "clean the list before upload", or right after waterfall-enrichment and personalization-pipeline and before the first send. Not a fit score (that is prospect-scoring) and not the mailbox check (that is deliverability-audit). This one is about the rows themselves.
---

# Pre-launch Data Check

Answers one question: **can this exact file go into the sender today without hurting the domain,
the brand or the test?**

It runs on the FINAL file, after `waterfall-enrichment` and `personalization-pipeline`, right
before upload. Earlier gates decided whether the companies fit (`prospect-scoring`) and whether the
mailboxes can send (`deliverability-audit`). This one looks at the rows as they will be sent. A
fit list with a broken `{{first_line}}`, a current client in row 212 and 30% catch-all still burns
the campaign.

## Where it sits

| Before | This check | After |
|---|---|---|
| `waterfall-enrichment` → `personalization-pipeline` | **pre-launch-data-check**: GO / GO WITH FIXES / STOP | `deliverability-audit` (mailboxes) → upload |

Run it every round, not once per client. Every new batch has its own duplicates, its own stale
signals and its own empty fields.

## What you need

- The final CSV as it will be uploaded (every column the sequence uses)
- Suppression files, each as a CSV: CRM export of everyone already in a conversation, contacts
  in active campaigns, current clients (domains are enough), opt-outs and do-not-contact
- The list of variables the sequence uses (`first_name`, `company`, `first_line`…)
- Optional: number of mailboxes and the daily new-contact cap per mailbox

No suppression files = the check still runs, but reports suppression as NOT CHECKED. Say that
out loud; the most expensive mistake in outbound is a cold email to a current client.

## The seven layers

Each layer is a stop-filter or a fix. Go top to bottom; a STOP in any layer means the file does
not go out today.

| # | Layer | What is checked | STOP when | FIX when |
|---|---|---|---|---|
| 1 | **Source** | duplicates inside the file; overlap with CRM, active campaigns, clients, opt-outs; contacts per company | anyone on a suppression list | duplicates; more than 3 contacts in one company |
| 2 | **Validation** | verification status per address; malformed; role addresses; free-mail; email domain vs company domain | no verification column at all; any invalid or malformed | any risky; catch-all above 25% of the batch; role addresses |
| 3 | **Completeness** | every sequence variable present, filled, and rendered (no `{{…}}`, `N/A`, `null`, `[NAME]`) | a variable column missing, or empty/unrendered in any row | n/a |
| 4 | **Routing** | every row has a tier/queue (A/B/D from `prospect-scoring`) and a sender if you split by sender | n/a | rows with no tier or sender |
| 5 | **Hygiene** | first-name case, legal suffixes in company names, empty titles | n/a | `JOHN`, `maria`, `Stripe Inc.`: the reader sees these in line one |
| 6 | **Signals** | signal age against the freshness window; signal without a source link | n/a | signal older than the window (default 60 days); no proof link |
| 7 | **Activation** | sendable rows after removals vs the volume gate; days of sending at current capacity | n/a | sendable below the volume gate (300 per event-signal hypothesis, 500 per data-point one) |

Invalid addresses and suppression hits are STOP, not FIX, for a reason: one bounces the domain,
the other emails someone who is already talking to you or paying you. Both cost more than a day's
delay.

## Run it

```bash
python3 scripts/check_list.py final.csv \
  --suppress crm_export.csv active_campaigns.csv clients.csv optouts.csv \
  --vars first_name,company,first_line \
  --mailboxes 6 --daily-cap 30 \
  --out rows_to_fix.csv
```

- Columns are auto-detected (`email`, `first_name`, `company`, `domain`, `title`, `linkedin_url`,
  `email_status`, `tier`, `signal_date`, `signal_source`). Map anything else with
  `--col email="Work Email"`.
- A suppression file with only a `domain` column suppresses the whole company (clients, DNC accounts).
- Tune per client: `--max-signal-age`, `--catch-all-max`, `--max-per-company`, `--min-volume`.
- Exit code 0 = GO, 1 = GO WITH FIXES, 2 = STOP, so it can sit in a pipeline.
- `--out` writes only the rows with problems, with a `problems` column. Hand that file back to
  whoever owns the fix.

If the person has no CSV yet (the list lives only in the sending tool), export it first. Do not
run the check on a sample; the problems live in the tail.

## Process

1. Ask for the final file and the suppression files. If any suppression source is missing, name it.
2. Ask which variables the sequence uses. Read them from the sequence if it is at hand.
3. Run `scripts/check_list.py`. Read the output; do not re-derive the counts by hand.
4. For every STOP, say what it costs if ignored and who fixes it.
5. For FIX items, sort by what the reader would notice first: broken variables and names, then
   stale signals, then routing.
6. Give the verdict and one next step. On GO, hand off to `deliverability-audit` if the mailboxes
   were not checked this week, otherwise to upload.

## Output format

```
Pre-launch data check: [file], [rows] rows, [date]
Suppression checked against: [files, or NOT CHECKED]

1 Source        [ok / n duplicates / n suppressed]
2 Validation    valid [n%] · catch-all [n%] · risky [n] · invalid [n]
3 Completeness  [each variable: ok / n empty / n unrendered]
4 Routing       [tier split / n unrouted]
5 Hygiene       [n names to fix / n legal suffixes]
6 Signals       [n stale / n without proof / not checked]
7 Activation    sendable [n] vs gate [n] · [n] sending days

VERDICT: [GO / GO WITH FIXES / STOP]
STOP: [numbered, each with the cost of ignoring it]
FIX:  [numbered, most visible first]
Rows to fix: [file]
Next: [one step]
```

## What this check does not do

- It does not decide fit. A clean row of the wrong company is still the wrong company. That is
  `prospect-scoring` and the 90% spot-check in `signal-outbound`.
- It does not verify addresses. It reads the verification status your validator wrote; if there is
  no status, it stops you and sends you back to `waterfall-enrichment`.
- It does not test the mailboxes. That is `deliverability-audit`, and both must be green before
  the first send.

The idea of checking a base in layers, from source to activation, is adapted from public
data-integrity frameworks for revenue teams; the thresholds here are the ones this methodology uses.
