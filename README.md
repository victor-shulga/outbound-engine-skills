# outbound-engine

Full outbound execution engine for B2B service companies: 19 skills covering deliverability, list building, hypotheses, sequence copy, A/B testing, reporting and reply audits.

Part of the GTM-system methodology by [Victor Shulga](https://victorshulga.com) (Fractional CRO).

## Install (Claude Code)

```
/plugin marketplace add victor-shulga/outbound-engine-skills
/plugin install outbound-engine@outbound-engine-skills
```

Restart your Claude Code session after install — skills load at session start.

## Skills included

- `02-signal-detection`
- `03-copy-generation`
- `06-hypothesis-builder`
- `11-data-research`
- `12-waterfall-enrichment`
- `13-lead-scoring`
- `15-subject-line-generator`
- `16-spintax-randomizer`
- `17-linkedin-sequence`
- `19-followup-sequence`
- `20-ps-line-generator`
- `21-campaign-tiering`
- `22-ab-test-analyzer`
- `23-campaign-report`
- `24-multi-channel-orchestrator`
- `25-campaign-naming`
- `26-deliverability-audit`
- `reply-audit`
- `weekly-outreach-report`

## Requirements & integrations

| Integration | Used for | Required? | Auth / setup |
|---|---|---|---|
| Claude Code | running the skills | yes | claude.com/claude-code |
| Notion MCP | writing reports/audits as Notion pages | optional | connect Notion in Claude settings |
| Outreach platform MCP (Instantly / HeyReach / Grinfi / Aimfox) | pulling live campaign & reply data | optional | connect the platform you use |
| CRM MCP | pulling deals/accounts | optional | connect your CRM |

Skills degrade gracefully: without MCP connections they work from pasted data (CSV, sheets, text).

## License

MIT — see [LICENSE](LICENSE).
