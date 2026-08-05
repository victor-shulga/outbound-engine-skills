# outbound-engine

Full outbound execution engine for B2B service companies: 24 skills covering signal sourcing, prospect-list research, enrichment, hypotheses, sequence copy, personalization, deliverability, reply handling, A/B testing and reporting.

Part of the GTM-system methodology by [Victor Shulga](https://victorshulga.com) (Fractional CRO).

## Start here

**`signal-outbound`** is the master skill. It runs the full path — service page → signal catalog → scored account list → named contacts with verified emails → sequence → personalization pipeline → launch — routing to the right skill at each step and enforcing the gate between them.

Ask for it in plain words: *"run the outbound process for [company]"*, *"where do I start"*, *"build me a campaign"*. Enter mid-path if you already hold an artifact — it checks that artifact against its own gate and moves forward instead of restarting. It also routes by symptom when a campaign is already running badly, and it will tell you when the problem is the offer rather than the outbound.

The idea it implements: don't look for companies that resemble your customers. Look for the ones that **already described their own problem in public** — most often in the text of their own job postings — and open with their words.

Everything downstream follows from one split: **the event tells you when to write, the data point tells you what to say.** A signal fires on 3–5% of a base; a data point is available on nearly all of it. Skip the second and most of the base has nothing to open with.

## Install (Claude Code)

```
/plugin marketplace add victor-shulga/outbound-engine-skills
/plugin install outbound-engine@outbound-engine-skills
```

Restart your Claude Code session after install — skills load at session start.

## Skills included

Skill names carry no number prefixes: the order of the work is defined by `signal-outbound`, not by filenames.

**Master**

- `signal-outbound` — the nine-step path, the seven gates, symptom routing, and where runs actually fail

**Signal-based sourcing**

- `outbound-signal-catalog` — 50 triggers for one niche, scored, bundled to clear the volume gate
- `outbound-account-sourcing` — ATS job postings → filtered, scored account list (ships with a Python filter/scoring script)
- `outbound-personalization-pipeline` — two generated fields, a confidence gate, and the push into the sequencer

**Research over a base you already have**

- `data-research` — grade a raw base into a scored, evidenced prospect list; owns the pass order and the cost model
- `signal-research` — hunt live signals *and* standing data points over an existing base, each with a source; ships the 60-entry signal catalogue and the re-scan queue
- `waterfall-enrichment` — domains → named people → verified emails, through a priced cascade with a ceiling per contact
- `prospect-scoring` — the pre-contact half: profile fit only, nothing a stop-filter already decided
- `lead-scoring` — the post-contact half: starts from that profile, adds what only a conversation reveals
- `hypothesis-builder` — ICP × signal × offer into a testing matrix
- `campaign-naming` — the convention has to exist before the campaigns do

Scoring is deliberately two skills. Mixing what you can read about a company with what someone told you on a call produces one number that answers neither question — and quietly ranks strangers above people who replied.

**Copy**

- `outbound-sequence-writer` — 8 touches, interest-only CTAs, separate copy per persona
- `subject-line-generator` · `ps-line-generator`
- `linkedin-sequence` — the LinkedIn side of the same hypothesis
- `followup-sequence` — non-responders and re-engagement of a burnt base
- `multi-channel-orchestrator` — the touch grid, set before the copy, because spacing changes what each message can say

**Launch and read**

- `deliverability-audit` — domains, mailboxes, SPF/DKIM/DMARC, warm-up. Runs before anything is sent, not after the numbers go bad.
- `reply-objection-handler` — ONE reply in, one ready-to-send message out: triage for intent and speed, classify the objection, write the response, set the CRM and platform action
- `reply-audit` — the batch view: many replies down to root cause — targeting, message, or pitch
- `ab-test-analyzer` · `campaign-tiering`
- `campaign-report` · `weekly-outreach-report`

The two reply skills are a pair: the handler is the surgeon on one thread, the audit is the epidemiologist over the batch. Audit findings become rules the handler applies; replies the handler writes get tagged so the next audit can aggregate them.

## Requirements & integrations

| Integration | Used for | Required? | Auth / setup |
|---|---|---|---|
| Claude Code | running the skills | yes | claude.com/claude-code |
| Scraping API (Apify or equivalent) | ATS job postings, company profiles, site crawls | for sourcing and signal research | your own API key; costs are per row, see the skills |
| Workflow runner with a people-search node (Freckle over Apollo, or equivalent) | domains → named people | for enrichment from domains | authenticate, then pin the org id |
| Email finders + validator (LeadMagic / Findymail / ZeroBounce or equivalents) | the email cascade | for enrichment | your own accounts |
| Notion MCP | writing reports and audits as pages | optional | connect Notion in Claude settings |
| Outreach platform MCP (Instantly / HeyReach / Grinfi / Aimfox) | pulling live campaign and reply data | optional | connect the platform you use |
| CRM MCP | pulling deals and accounts | optional | connect your CRM |

Skills degrade gracefully: without MCP connections they work from pasted data (CSV, sheets, text).

## Changelog

**0.5.0** — two lines of work merged: the signal-sourcing chain built around job postings, and a rewrite of the research and scoring skills from live client runs.

- **Signal and data-point research is its own step.** `signal-research` takes an existing base and returns live signals with a URL and a date, plus the standing data points that carry every account without one. `data-research` no longer describes detection; it hands off and stays responsible for the pass order and the cost model. The 60-entry signal catalogue now ships with the skill rather than living in another repo.
- **`data-research` rewritten** around grading a base you already have. Adds the evidence rule (no URL and no date, no signal; the source must resolve to the domain, not the company name), the cheapest-cut-first pass order with real per-row costs, the canonical 12-block CSV output and the volume gates.
- **`waterfall-enrichment` rewritten and merged** with the contact-enrichment skill: domains → people via a people-search node, then the email cascade, with per-step credit costs, a ceiling per contact, an input audit before any spend, and cost per *verified* contact as the reported metric.
- **Scoring split in two** — `prospect-scoring` and `lead-scoring`. The old single rubric scored geography and headcount that were already stop-filters: free points, identical for every surviving row, and a threshold that stopped separating anything.
- **`reply-objection-handler` added**, with `meeting-intent-scorer` merged into it as an intent-triage step rather than shipped as a separate skill. The bundle could previously diagnose a batch of replies but not answer a single one.
- **The master skill absorbed the router work**: a locate-the-caller step, all seven gates in one table, symptom routing for live campaigns, and a fixed hand-off format.
- **Removed:** `spintax-randomizer` (token-level randomisation changes nothing a filter reads or a prospect notices — vary by angle instead), `signal-detection` (superseded by `signal-research`), `copy-generation` (superseded by `outbound-sequence-writer`).
- **Cross-repo duplicates removed.** `reply-audit`, `lead-scoring` and `weekly-outreach-report` existed in both this bundle and `gtm-skills` under the same skill name, with the copies drifting apart. They live here only.

**0.1.0** — initial bundle.

## License

MIT — see [LICENSE](LICENSE).
