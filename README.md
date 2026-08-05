# outbound-engine

Full outbound execution engine for B2B service companies: 21 skills covering prospect-list research, enrichment, hypotheses, sequence copy, deliverability, A/B testing, reporting and reply audits.

Part of the GTM-system methodology by [Victor Shulga](https://victorshulga.com) (Fractional CRO).

## Install (Claude Code)

```
/plugin marketplace add victor-shulga/outbound-engine-skills
/plugin install outbound-engine@outbound-engine-skills
```

Restart your Claude Code session after install — skills load at session start.

## Skills included

Listed in the order they run. If you do not know where to start, run `outbound-run` — it works out
which stage you are at, checks the gate that stage depends on, and sends you to one skill.

**0 · The router**

- `outbound-run` — where am I, what gate am I failing, what is the single next step. Also routes by symptom when a live campaign is underperforming, including the case where the honest answer is that outbound is not the broken part.

**1 · Infrastructure — before anything is sent**

- `deliverability-audit` — domains, mailboxes, SPF/DKIM/DMARC, warm-up. Runs first, not after the numbers go bad.

**2 · Targeting — what to test and who to write to**

- `hypothesis-builder` — ICP × signal × offer into a testing matrix
- `campaign-naming` — the convention has to exist before campaigns do, or the statistics never reassemble
- `data-research` — grade a raw base into a scored, evidenced prospect list; owns the pass order and the cost model
- `signal-research` — **its own step**: hunt live signals AND standing data points over an existing base, each with a source, and ships the 60-entry signal catalogue
- `waterfall-enrichment` — verified emails through a priced multi-source cascade
- `prospect-scoring` — the pre-contact half: profile fit only, nothing a stop-filter already decided
- `lead-scoring` — the post-contact half: starts from the profile, adds what only a conversation reveals

Scoring is deliberately two skills. Mixing what you can read about a company with what someone told
you on a call produces one number that answers neither question — and quietly ranks strangers above
people who replied.

**3 · Copy — one campaign, one text**

- `multi-channel-orchestrator` — the touch grid, set before the copy, because spacing changes what each message can say
- `copy-generation` — the sequence body
- `subject-line-generator`
- `ps-line-generator`
- `linkedin-sequence`
- `followup-sequence` — non-responders and re-engagement of a burnt base

**4 · Reading the result**

- `reply-objection-handler` — ONE reply in, one ready-to-send message out: triage for intent and speed, classify the objection, write the response, set the CRM and platform action
- `reply-audit` — the batch view: forensic classification of many replies down to root cause: targeting, message, or pitch
- `ab-test-analyzer` — variant against variant
- `campaign-tiering` — what to scale, what to kill, across all campaigns
- `campaign-report` · `weekly-outreach-report` — the client-facing write-up

The two reply skills are a pair: the handler is the surgeon on one thread, the audit is the
epidemiologist over the batch. Audit findings become rules the handler applies; replies the handler
writes get tagged so the next audit can aggregate them.

The loop closes back on step 2: a reply audit that lands on "wrong targeting" produces a new hypothesis; one that lands on "the signal burnt out" triggers a re-scan.

## Requirements & integrations

| Integration | Used for | Required? | Auth / setup |
|---|---|---|---|
| Claude Code | running the skills | yes | claude.com/claude-code |
| Scraping API (Apify or equivalent) | company profiles, site crawls, job postings in `data-research` | optional | your own API key; costs are per row, see the skill |
| Email finders + validator (LeadMagic / Findymail / ZeroBounce or equivalents) | the cascade in `waterfall-enrichment` | optional | your own accounts |
| Notion MCP | writing reports/audits as Notion pages | optional | connect Notion in Claude settings |
| Outreach platform MCP (Instantly / HeyReach / Grinfi / Aimfox) | pulling live campaign & reply data | optional | connect the platform you use |
| CRM MCP | pulling deals/accounts | optional | connect your CRM |

Skills degrade gracefully: without MCP connections they work from pasted data (CSV, sheets, text).

## Changelog

**0.5.0**

- `outbound-run` added — a router. Twenty skills is a toolbox, not an order of operations; this supplies the order. It locates the caller in three questions, checks the gate that stage depends on (infrastructure before anything is sent, a stated hypothesis before a base, a reason-to-write before copy, volume before statistics), and hands off to exactly one skill. It also routes by symptom for campaigns already running — and will tell you when the problem is the offer rather than the outbound, because a router that always finds an outbound answer is useless.

**0.4.0**

- **Signal and data-point research is now its own step.** `signal-research` moved in — it takes an existing base and returns live signals with a URL and a date, plus the standing data points that carry every account without one. `data-research` no longer describes detection; it hands off, takes back the two blocks and stays responsible for the pass order and the cost model. The weak `signal-detection` skill it replaces is gone.
- **The 60-entry signal catalogue now ships with the skill** (`signal-research/resources/signals-catalog.md`): account events and news, hiring, tech change, person-level activity, project-flow, build-intent, vertical packs, and the data-point series — each with a detection route, a freshness window and a pairing note. Previously the skill referenced a catalogue that lived in another repo, so installing the bundle alone gave you a broken pointer.
- **Data points promoted to a first-class output.** They were treated as where expired signals go to retire. They are what queue D — most of any base — actually opens with, so they are now harvested in the same pass, with the extraction rules that keep the noise out.
- **Scoring split in two.** `prospect-scoring` (pre-contact, profile only) and `lead-scoring` (post-contact, starts from that profile). The old single rubric scored geography and headcount that were already stop-filters — free points, identical for every surviving row, and a threshold that stopped separating anything. It also summed fit and timing into one number; a signal now sets the queue, not the score.

**0.3.0**

- `reply-objection-handler` added — moved in from the `gtm-skills` repo, where it sat apart from the rest of the outbound flow. It is the most-used reply skill in daily work, and the pack could previously diagnose a batch of replies but not answer a single one.
- `meeting-intent-scorer` merged into it rather than added separately. Scoring a reply for meeting intent is the first step of answering that reply, not a standalone job: same input (one reply), same output (a drafted response and a next action). Its three parts that were genuinely missing — the intent tiers with a response clock, the CRM plus sending-platform action, and the read of the tier mix as a diagnosis of the campaign — are now sections of the handler. The standalone skill is gone from the `sales-engine` bundle.
- **Cross-repo duplicates removed.** `reply-audit`, `lead-scoring` and `weekly-outreach-report` previously existed in both this bundle and `gtm-skills` under the same skill `name:`, with the copies drifting apart — installing both gave two different skills answering to one name. The newer copies now live here only. `lead-scoring` in particular was two different skills sharing a name; the deterministic 100-point rubric won, and gained the normalisation and safety-catch rules that `data-research` relies on.

**0.2.0**

- `11-data-research` rewritten from live client runs. Reframed around grading a base you already have (the actual job) rather than sourcing one from scratch. Adds the signal / data-point split, the evidence rule (no URL and no date, no signal; the source must resolve to the domain, not the company name), the cheapest-cut-first pass order with real per-row costs, the canonical 12-block CSV output, campaign volume gates, and the traps that cost real hours.
- `12-waterfall-enrichment` rewritten. Adds the LinkedIn-URL entry point (a two-stage cascade — profile resolution, then email finding), real per-step credit costs and a budget ceiling per contact, an input audit before any spend, and cost per *verified* contact as the reporting metric.
- `16-spintax-randomizer` removed. Token-level randomisation does not change what a filter reads or what a prospect notices. Vary by angle instead — different question, different fact, different frame. `subject-line-generator` updated to match.
- Numeric prefixes dropped from every skill folder. They were positions in a larger internal catalogue, so in a subset they only advertised the gaps. Folder names now match the `name:` in each skill's frontmatter, which was already unnumbered — nothing changes in how a skill is invoked.

**0.1.0** — initial bundle.

## License

MIT — see [LICENSE](LICENSE).
