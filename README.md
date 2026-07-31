# outbound-engine

Full outbound execution engine for B2B service companies: 25 skills covering signal sourcing, list building, enrichment, hypotheses, sequence copy, personalization, deliverability, A/B testing, reporting and reply audits.

Part of the GTM-system methodology by [Victor Shulga](https://victorshulga.com) (Fractional CRO).

## Start here

**`signal-outbound`** is the master skill. It runs the full path — service page → signal catalog → scored account list → named contacts with verified emails → sequence → personalization pipeline → launch — routing to the right skill at each step and enforcing the gate between them.

Ask for it in plain words: *"run the outbound process for [company]"*, *"where do I start"*, *"build me a campaign"*. Enter mid-path if you already hold an artifact — it checks that artifact against its own gate and moves forward instead of restarting.

The idea it implements: don't look for companies that resemble your customers. Look for the ones that **already described their own problem in public** — most often in the text of their own job postings — and open with their words.

## Install (Claude Code)

```
/plugin marketplace add victor-shulga/outbound-engine-skills
/plugin install outbound-engine@outbound-engine-skills
```

Restart your Claude Code session after install — skills load at session start.

## Skills included

Skill names carry no number prefixes: the order of the work is defined by `signal-outbound`, not by filenames.

**Master**

- `signal-outbound` — the nine-step path, the gates, and where runs actually fail

**Signal-based sourcing**

- `outbound-signal-catalog` — 50 triggers for one niche, scored, bundled to clear the volume gate
- `outbound-account-sourcing` — ATS job postings → filtered, scored account list (ships with a Python filter/scoring script)
- `outbound-contact-enrichment` — domains → decision-makers with verified work emails
- `outbound-sequence-writer` — 8 touches, interest-only CTAs, separate copy per persona
- `outbound-personalization-pipeline` — two generated fields, a confidence gate, and the push into the sequencer

**Execution**

- `signal-detection`
- `copy-generation`
- `hypothesis-builder`
- `data-research`
- `waterfall-enrichment`
- `lead-scoring`
- `subject-line-generator`
- `spintax-randomizer`
- `linkedin-sequence`
- `followup-sequence`
- `ps-line-generator`
- `campaign-tiering`
- `ab-test-analyzer`
- `campaign-report`
- `multi-channel-orchestrator`
- `campaign-naming`
- `deliverability-audit`
- `reply-audit`
- `weekly-outreach-report`

## The rules the engine enforces

**A state signal does not work alone.** "Your framework is out of support" earns "we know, thanks." Pair it with an event — "you raised in March, that framework lost support in March" — and it becomes a conversation.

**Volume gate: 300 accounts per event-signal hypothesis, 500 per data-point hypothesis.** Under that the test cannot produce a readable result. Bundle related signals under one email theme, or park the hypothesis.

**No meeting ask anywhere in a cold sequence.** The only job of a cold touch is a reply.

**Two generated fields, never a generated letter.** A fully generated email drifts to the mean: correct, smooth, faceless. A fixed skeleton holds the voice.

**Measure per hypothesis, never per campaign.** A campaign mixing two signals reports an average that describes nothing.

## Requirements & integrations

| Integration | Used for | Required? | Auth / setup |
|---|---|---|---|
| Claude Code | running the skills | yes | claude.com/claude-code |
| Apify MCP | job postings from ATS career sites (`outbound-account-sourcing`) | for signal sourcing | Apify API token, connect in Claude settings |
| Freckle CLI | people search and email enrichment (`outbound-contact-enrichment`) | for enrichment | `freckle auth login`, then pin `FRECKLE_ORG_ID` |
| Python 3 | filter and scoring script | for signal sourcing | ships with macOS and Linux |
| Notion MCP | writing reports and audits as Notion pages | optional | connect Notion in Claude settings |
| Outreach platform MCP (Instantly / HeyReach / Grinfi / Aimfox) | live campaign and reply data, sending | optional | connect the platform you use |
| CRM MCP | deals and accounts | optional | connect your CRM |

Skills degrade gracefully: without MCP connections they work from pasted data (CSV, sheets, text).

## License

MIT — see [LICENSE](LICENSE).
