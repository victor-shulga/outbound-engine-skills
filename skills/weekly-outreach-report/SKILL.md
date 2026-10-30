---
name: weekly-outreach-report
description: >
  Builds a canonical WEEKLY outreach report for a client as a standalone narrative
  page — the exact 7(+2)-section format instead of a dashboard dump. Pulls live data
  from the client's outreach platform (LinkedIn automation and/or email sending tools),
  applies the known platform gotchas, classifies every reply with root cause, and ends
  with gold leads + ready-to-send drafts. Trigger with: "weekly report", "outreach
  report", "analyse this week's results", "build the report from our template". NOT for
  batch reply forensics alone (use reply-audit) and NOT for benchmarking a single metric
  (use outbound-analyst).
---

# Weekly Outreach Report

The report is a **standalone readable narrative page**, not a row-dump into a matrix DB.
The data store and the report are two separate artifacts.

## Hard rules

- NEVER dump rows into a matrix DB and point at a kanban. Matrix DB = data store;
  the report = its own readable artifact.
- Report language: match the client's working language. Lead drafts: the prospect's
  language (usually English).
- Every draft message ends with a question (soft CTA).
- Data-quality warnings come BEFORE the numbers, not in a footnote.
- Numbers must be genuine per-(flow × sender × week). If a platform can't give a weekly
  cut, say so explicitly and show the method used.

## Step 1 — Route to the client's platform (apply the gotchas)

Every outreach platform lies in its own way. Know the trap before you trust the number:

| Platform type | Gotcha you MUST apply |
|---|---|
| LinkedIn automation (lifetime-stats tools) | Stats are often LIFETIME-only → the weekly delta = this week's snapshot minus last week's snapshot. Store/ask for the previous snapshot; never present lifetime totals as "this week". |
| LinkedIn automation (per-flow CRM) | A platform "Replied" CRM stage can read 0 even when replies exist. Count real replies from the reply/trigger events per flow, NOT the CRM stage. |
| Email sending tools | Reply/open data may be dark or partial. Report the dark channel as a data-quality item rather than implying zero. |
| Workspace/day-level tools | Stats may only be available workspace-level per day, not per campaign per week. Note the granularity limit. |

If the platform data source is not connected, say which one is missing and build the
report from whatever export the client provides (CSV / Sheet / paste) instead of stopping.

## Step 2 — Assemble the page in this exact order

1. **Header** — client, week (Mon–Sun dates), platforms, senders.
2. **Main takeaway** — one paragraph: the single most important thing about the week.
3. **⚠️ Data quality** — FIRST, before any table: what's missing, fake-zero fields,
   lifetime-only metrics, dark channels, snapshot method used.
4. **Overall funnel** — table: sent → connected → replied → positive → calls booked,
   with week-over-week delta where possible.
5. **By flow / campaign** — table per flow: volume, connect %, reply %, positive replies;
   one line of interpretation per flow (not just numbers).
6. **By sender** — same cut per sender; flag connect-heavy/message-starved funnels
   (lots of accepts, few messages sent — a common failure pattern).
7. **Actions** — numbered actions, each with owner + date.
8. **Reply analysis (forensics)** — classify EVERY reply of the week: positive /
   objection / referral / not-now / negative / auto-reply. For each non-positive class,
   root cause: **targeting/data problem vs message problem vs pitch problem**. Watch known
   false positives: event smalltalk inflating reply counts; warm replies sitting unstaged
   in the CRM.
9. **Gold leads** — for each warm/positive lead: full thread quoted, context, and a
   ready-to-send draft in the prospect's language (route objection drafts through the
   reply-objection-handler taxonomy).

## Step 3 — Ship

- Create the page in the client's reporting area (ask once if unknown, then remember).
  New week = new page — never regenerate an existing report page (it kills saved chart
  views).
- If your tool renders tables from pipe-delimited text, don't put a literal `|` inside a
  cell — use `·`.
- Post a 5-line TL;DR back in chat: headline metric, biggest problem, top action.

## Terms and plain-language output

<!-- glossary:start terms=data-quality,accept-rate,reply-rate,positive-reply-rate,sender,root-cause,reply-taxonomy,gold-leads,cta -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| data quality, fake-zero, lifetime-only, dark channel, snapshot | застереження щодо даних | Що в цифрах неповне чи хибне: нуль, який насправді не нуль, показники за весь час замість тижня, канал без даних. |
| accepted connection rate | частка прийнятих запитів у LinkedIn | скільки людей із тих, кому надіслали запит у контакти, його прийняли. |
| reply rate | частка відповідей | скільки людей з тих, кому написали, відповіли. |
| positive reply rate | частка позитивних відповідей | скільки з тих, кому написали, відповіли з інтересом, а не «відпишіть мене» |
| sender, SDR | відправник | Людина чи акаунт, від імені якого йдуть повідомлення; цифри дивимось по кожному окремо. |
| root cause: targeting/data vs message vs pitch | першопричина: не ті люди чи дані · текст · пропозиція | Що саме зламалось; правимо лише це місце. |
| reply type tags (HOT, SOFT_NO, HARD_NO, CURIOUS_PROBING, WANTS_PROOF...) | тип відповіді | Мітка про стан ліда і причину його відповіді; у тексті для людей пишемо словами, коди лишаються лише в мітках CRM. |
| gold leads | найтепліші ліди | Ліди з позитивною відповіддю; для кожного повна переписка і готова чернетка відповіді. |
| CTA | прохання в кінці листа | конкретний маленький наступний крок: відповісти, подивитися, погодитися на дзвінок |
<!-- glossary:end -->
