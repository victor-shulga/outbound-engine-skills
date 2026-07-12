---
name: weekly-outreach-report
description: >
  Builds the user's canonical WEEKLY outreach report for a client as a standalone
  narrative Notion page — the exact 7(+2)-section format he otherwise assembles by
  hand every week. Pulls live data from the client's outreach platform (Client B =
  Grinfi MCP; Client A = Aimfox + Instantly MCP; Client E = HeyReach MCP),
  applies the known platform gotchas, classifies every reply with root cause, and
  ends with gold leads + ready-to-send drafts. Trigger when the user says: "тижневий
  звіт по [клієнт]", "weekly report", "звіт по аутрічу", "проаналізуй результати
  за тиждень", "підключись до grinfi/instantly і зроби звіт", or asks for outreach
  results "по нашому шаблону". NOT for batch reply forensics alone (reply-audit)
  and NOT for benchmarking a single metric (outbound-analyst).
---

# Weekly Outreach Report

Canonical 7(+2)-section format is described below.
if available. This skill is the executable version.

## Hard rules

- The report is a **standalone readable narrative Notion page**. NEVER dump rows
  into a matrix DB and point at a kanban. Matrix DB = data store; report = its own
  artifact.
- Report language: Ukrainian. Lead drafts: the prospect's language (usually English).
- Every draft message ends with a question (soft CTA).
- Data-quality warnings come BEFORE the numbers, not in a footnote.
- Numbers must be genuine per-(flow × sender × week). If a platform can't give a
  weekly cut, say so explicitly and show the method used.

## Step 1 — Route to the client's platform

| Client | Source | Gotchas you MUST apply |
|---|---|---|
| Client B | Grinfi MCP  | `response_rate.replied`=0 is fake. Real replies = `trigger_message_replied` tasks per flow, NOT the CRM "Replied" stage. |
| Client A | Aimfox + Instantly (`instantly`) | Aimfox stats are LIFETIME-only → weekly delta = snapshot minus last week's snapshot (store/ask for the previous snapshot). Instantly email data may be dark — report that as a data-quality item. |
| Client E | HeyReach MCP | Stats are workspace-level/day. |

If the platform MCP is not connected, say which one is missing and build the
report from whatever export the user provides (CSV/Sheet/paste) instead of stopping.

## Step 2 — Assemble the page in this exact order

1. **Header** — client, week (Mon–Sun dates), platforms, senders.
2. **Головна думка** — one paragraph: the single most important takeaway of the week.
3. **⚠️ Якість даних** — FIRST, before any table: what's missing, fake-zero
   fields, lifetime-only metrics, dark channels, snapshot method used.
4. **Загальна лійка** — table: sent → connected → replied → positive → calls
   booked, with week-over-week delta where possible.
5. **По флоу/кампаніях** — table per flow: volume, connect %, reply %, positive
   replies; one line of interpretation per flow (not just numbers).
6. **По сендерах** — same cut per sender; flag connect-heavy/message-starved
   funnels (lots of accepts, few messages sent — a recurring Client B pattern).
7. **Дії** — numbered actions, each with owner + date.
8. **Reply Analysis (форензика)** — classify EVERY reply of the week:
   positive / objection / referral / not-now / negative / auto-reply. For each
   non-positive class, root cause: **targeting/data problem vs message problem vs
   pitch problem**. Watch known false positives: event smalltalk inflating reply
   counts; warm replies sitting unstaged in the CRM.
9. **Gold leads** — for each warm/positive lead: full thread quoted, context, and
   a ready-to-send draft in the prospect's language (route drafting through
   `reply-objection-handler` taxonomy if the reply is an objection).

## Step 3 — Ship

- Create the page in the client's Notion reporting area (ask once if unknown,
  then remember). Use `notion-create-pages`. Never regenerate an existing report
  page (kills chart views) — new week = new page.
- Notion table cells must not contain literal `|` — use `·`.
- Post a 5-line TL;DR back in chat: headline metric, biggest problem, top action.