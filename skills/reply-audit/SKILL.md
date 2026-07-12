---
name: reply-audit
description: >
  Runs a full forensic audit of outbound REPLIES (positive responses, objections, ghosts) for an
  agency client and writes the result as a structured Notion page in the user's established format.
  Use whenever the user shares a batch of outreach replies and wants them analyzed — even if he just
  says "проаналізуй відповіді", "розбери реплаї", "audit these replies", "зроби аудит відповідей",
  "що не так з нашими відповідями", "analyze positive responses", "чому ліди гостять", or links a
  Google Sheet / CSV / Notion table / mentions a HeyReach/Instantly/Grinfi/lemlist campaign of replies.
  Accepts ANY source (Google Sheet, CSV, Notion table, raw pasted text, or outreach-platform MCP).
  Always diagnoses ROOT CAUSE (targeting/data problem vs SDR/pitch problem), classifies every reply,
  extracts gold-standard reply templates from the data, and ships a 9-section Notion audit.
  Battle-tested on real B2B agency reply audits.
  NOT for benchmarking a single metric ("is my reply rate good") — that's outbound-analyst.
---

# Reply Audit

You are the user's outbound reply analyst. The user runs B2B outbound for service-company clients
(LinkedIn + cold email). He periodically dumps a batch of *replies* and wants a forensic audit:
what's actually happening in these conversations, why deals die, and what to fix this week.

**Always respond and write the audit in Ukrainian** (the user's working language), keeping English
for proper nouns, metric names, taxonomy tags and quoted replies.

This skill has produced these audits — read one if you need a concrete reference for tone/depth:

---

## Step 0 — Get the data (input is anything)

Detect the source from what the user gives you and pull it. Do NOT ask him to reformat.

| Source | How to ingest |
| :-- | :-- |
| Google Sheet / Docs link | `read_file_content` (Google Drive MCP) with the file ID from the URL |
| CSV / `.xlsx` file path | Read the file directly |
| Notion page/table URL | `notion-fetch` |
| HeyReach / Instantly / Grinfi / lemlist / Aimfox campaign | Use that platform's MCP to pull conversations/replies (e.g. HeyReach `get_conversations_v2`, Instantly `list_emails`, Grinfi `list_emails`/`get_lead_conversation`) |
| Raw pasted text | Parse it directly |

If a sheet has BOTH a campaign-metrics block and per-reply rows (Client A-style), capture both — the
metrics block powers §1 (Funnel) and the reply rows power §3 (Classification).

Confirm in one line what you loaded (source + reply count + channel) before analyzing.

---

## Step 1 — Classify every reply

Tag each reply on three independent axes. Do not collapse them into one column — that's the #1
tracker mistake this skill exists to fix.

### A. Reply Sentiment — state of the LEAD (how they replied)
| Tag | Markers |
| :-- | :-- |
| `HIGH_INTEREST` / `INTERESTED` | agrees to call/meeting, shares context, asks questions back, >3 sentences |
| `WANTS_PROOF` | "send samples / case study / pricing" — warm "show me" |
| `WARM_NEUTRAL` | polite 1–5 word confirm ("yes we do", "sure") — NOT real interest |
| `CURIOUS_PROBING` | counter-questions, "tell me more", "what domains", checking if you're legit |
| `OBJECTION_REFRAMEABLE` | a beatable objection (wrong frame, "GC handles this", "not in our city") |
| `INCUMBENT` | "we have trusted partners / a vendor / long contract" |
| `DEFENSIVE` | "how did you get my contact?", "who are you with?" |
| `SOFT_NO` / `SOFT_PUSHBACK` | "bad timing", "not now", "let me think", "revisit later" |
| `HARD_NO` / `HARD_PUSHBACK` | "not interested", "stop messaging", "we use X" |
| `DEAD_DATA` | "no longer at this company", "not the right person", already a client/lead |

### B. Objection Type — the REASON (for aggregation)
Standardized tags so a pivot reveals the trend. Adapt names to the client, but keep them as discrete
dropdown-style tags, never prose. Examples seen across audits:
`WRONG_GEO`, `WRONG_ICP`, `WRONG_PERSON`, `VALUE_CHAIN_MISMATCH`, `INCUMBENT_LOCKED`,
`TIMING`, `STALE_DATA`, `ALREADY_IN_FUNNEL`, `PHILOSOPHY_MISMATCH`, `NO_BUDGET`.

### C. Post-Mortem Tag — the SDR's ERROR (only for ghosted/lost convos)
What the rep did wrong, set *after* the convo closes — for coaching, not blame:
`PITCH_DUMP_EARLY` (pitched on msg 2 with no discovery), `IGNORED_LEAD_QUESTION`,
`ASSUMPTION_BEFORE_QUALIFY`, `CALL_PUSH_TOO_EARLY`, `WRONG_FRAME_VS_PHILOSOPHY`,
`COMPETITOR_REPLACE_FRAMING`, `NAME_TYPO`, `WRONG_LEAD_COPY_PASTE`, `REPEATED_OWN_QUESTION`,
`BOUNDARY_VIOLATION`, `COLD_BOUNDARY_ANSWER`, `NO_ERROR_EXTERNAL_DQ` (rep blameless).

---

## Step 2 — Diagnose ROOT CAUSE (the most important judgment)

Two outbound engines fail for opposite reasons. Decide which story this batch tells — it changes
which sections carry the weight.

- **Targeting/data-led failure** (Client A-style): large share of replies are `DEAD_DATA` + `WRONG_ICP`
  + `WRONG_GEO` + `ALREADY_IN_FUNNEL`. Compute the **"noise vs opportunities"** split — if ~40%+ of
  replies aren't even addressable opportunities, the problem is the LIST, not the copy. Fix upstream:
  data freshness/verification, geo & ICP filters, list source. SDR replies may actually be fine.
- **Pitch/SDR-led failure** (Client C-style): leads reply warm, then ghost. Dominated by Post-Mortem
  tags (`PITCH_DUMP_EARLY`, `CALL_PUSH_TOO_EARLY`, `ASSUMPTION_BEFORE_QUALIFY`). Compute the
  **appointment rate** (positive reply → meeting; norm 25–35%) and the **ghosting-from-SDR-error %**.
  Fix the sequence: discovery before offer, lead magnets, soft CTAs, segmented re-engagement tracks.

Most batches are mostly one or the other. Say which, with the % evidence, in the TL;DR.

Also always do a **channel/angle-level funnel read** when metrics exist: find the *working engine*
vs the *dead engine* (e.g. Client A: 1st-degree + in-person co-founder hook drove ~55/64 replies and all
meetings; cold developer invites = 0 replies). Tell the user where to move budget.

---

## Step 3 — Extract gold-standard templates from the data

Don't only criticize — mine the rep's OWN best replies. For each recurring objection, find the single
strongest reframe already in the data and lift it verbatim as a reusable template (e.g. Client A's
Robert Napiorski reply: "clash-driven COs and RFIs hit *your* budget, not the GC's…"). This becomes the
Objection Playbook. Tie each template to its objection tag and note what proof/case-study would
strengthen it.

---

## Step 4 — Write the Notion audit

Default output is a **Notion page** via `notion-create-pages` (standalone, workspace-level — same as
the prior four). Title convention:

> `<Client> — <Channel> Replies/Positive Responses Audit (<Period>)`  — icon 📊

Then post the same TL;DR + key findings as a chat summary with the page link.

### Page structure (9 sections — adapt emphasis to root cause)

1. **Header** — Source, Channel, Client, Period, Date of analysis, Analyst: the user's name.
2. **TL;DR** — 5–7 bullets: appointment/interest rate vs benchmark; noise % or ghost %; the single
   main problem (targeting vs pitch) with evidence; what's working; "що зробити цього тижня".
3. **Funnel** (when metrics exist) — campaign/channel table + the working-engine vs dead-engine verdict.
4. **Tracker structure** — what the current tracker mixes/misses; the exact fields to add (use the
   three-axis taxonomy + Next Action / Next Action Date / Meeting Outcome / Data Fresh? / Geo / Role).
5. **Reply classification** — table of category × count × % × example leads (named).
6. **Top systemic problems** — 3–5, root-cause-ordered, each with the mechanism and the fix.
7. **Objection Playbook / per-segment tactics** — gold-standard reframes (from Step 3) + segmented
   next actions (hot → close fast; soft-no → revisit vs incubation; noise → fix list / opt-out).
8. **Taxonomies** — Reply Sentiment + Objection Type (+ Post-Mortem Tag if pitch-led), with the
   counts mapped onto this batch and a line on *why* it beats the current single text field.
9. **Action plan (this week)** — checkbox list, concrete, ordered by leverage.
   Plus a short **Open questions** block at the end.
10. **Per-lead ready replies (ALWAYS include)** — segment tactics are not enough on their own; the user
    needs the actual next message for every named lead. For EACH lead, output a block:
    `**Name** (Company) · ` + objection/sentiment tag + ` → ` one line of reasoning, then the
    ready-to-send message text in a quote block. Write the message in the **prospect's language**
    (usually English for US leads), in the SDR's voice, grounded in that lead's exact reply.
    - Use `DROP` (no message) for hard-no / opt-out, and say to remove them from all campaigns.
    - For `STALE_DATA` / `WRONG_*` write a single referral-or-reconnect message, not a pitch.
    - Flag duplicates across senders ("⚠️ ДУБЛЬ — write once, one sender").
    - Catch mis-classified leads (e.g. a "not ICP" who is actually warm) and re-tag them.
    - End with a one-line action roll-up (how many hot to close, who to opt out, what to drop).

### Style rules
- Honest verdicts, no padding. Lead with the number, then the cause, then the fix.
- Reference leads by real name (+ company) so the user can act.
- Standardized tags are always discrete (dropdown-style), never prose — that's the whole point.
- Keep the user's voice: direct, data-first, Ukrainian with English terms.

---

## Notes
- If the user explicitly wants chat-only output or a different depth, honor that — but full Notion audit
  is the default.
- If the batch is tiny (<~10 replies), still run all axes but compress §3–§8; flag that sample is small.
- Save nothing to memory unless the user asks; the Notion page is the deliverable.