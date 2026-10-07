---
name: cold-email-playbook
description: >-
  Cold-email reference playbook for the parts the rest of the outbound toolkit does not cover. (1)
  Sending infrastructure from zero: mailbox and domain sizing math, secondary domains, Google
  Workspace and Microsoft 365, MX / SPF / DKIM / DMARC, warm-up timeline, going-live ramp,
  blacklist recovery, troubleshooting. (2) Thirteen named copy frameworks,
  each credited to its creator. (3) Benchmarks and operating rules with sources: reply and bounce
  ranges, sequence length, TAM reuse every quarter, the Golden ICP. (4) Re-engaging ghosted,
  no-show and closed-lost leads. Use when asked about email infrastructure, how many domains or
  mailboxes, DNS setup, warm-up, scaling sending, blacklists, "which copy framework", cold-email
  benchmarks, or reviving old leads; "скільки доменів", "прогрів", "фреймворк листа",
  "реанімувати старі ліди". NOT for writing sequences (sequence-writer, followup-sequence) or
  subject lines (subject-line-generator).
---

# Cold Email Playbook

A reference skill with four modules. It answers infrastructure, framework, benchmark and
re-engagement questions from its own files and hands every copywriting or audit job to the skill
built for it.

## Routing

All paths are relative to this skill's folder. Read only the file the request needs.

| Request | Read |
|---|---|
| Build sending infrastructure; how many domains or mailboxes; Workspace / M365 setup; DNS records; warm-up; going live; monitoring; blacklist or bounce recovery; "it's broken / in spam" | `resources/email-infra.md` |
| A named framework or structure for a cold email (Do the Math, Pattern Interrupt, Josh Braun's problem-first, etc.), first-line types, value-prop styles, the three-email arc | `resources/copy-frameworks.md` |
| "Is this campaign healthy", reply / bounce / positive benchmarks, sequence length, TAM reuse, Golden ICP, seasonal dips | `resources/benchmarks-and-rules.md` |
| Reactivate a ghosted, no-show, closed-lost or old lead | `resources/re-engagement.md` |

```
Request
├─ infrastructure: build / size / set up / broken      → resources/email-infra.md
├─ which framework or structure for the copy           → resources/copy-frameworks.md
├─ benchmarks, health check, TAM reuse, Golden ICP     → resources/benchmarks-and-rules.md
├─ reviving old, ghosted or closed-lost leads          → resources/re-engagement.md
└─ writing a sequence, subject lines, auditing replies → Hand-off below
```

## Quick answers (no file read needed)

- **Sizing**: monthly emails ÷ 20 working days = daily volume; ÷ 20-25 per mailbox = mailboxes; × 1.5
  buffer; ÷ 2 = domains. Mix about 60% Google Workspace and 40% Microsoft 365.
- **Never**: send cold from the main domain; put more than 2 mailboxes on a domain; put several domains
  in one tenant; switch warm-up off while live; raise per-mailbox limits to scale.
- **DNS**: MX, SPF (one record only), DKIM, DMARC on every domain; DMARC moves from `p=none` to
  enforcement once SPF and DKIM pass. Every sending domain points at a live page.
- **Warm-up**: two weeks minimum, three recommended; plan the first campaign at setup day + 3 weeks.
- **Ramp per mailbox per day**: Google 10-15 → 15-20 → 20-25 over about four weeks; Microsoft 5-10 →
  10-12 → 12-15.
- **Health**: bounce under 2% (pause over 5%), spam complaints under 0.1%, opens unreliable.
- **Copy**: about 60-90 words, plain text, one interest-based ask, 2-3 emails, 3-5 days apart, a new
  angle in each.

For DNS values, recovery steps and anything beyond these lines, read the file; do not improvise DNS
records.

## How to answer

1. Pick the module from the routing table and read its file.
2. State the benchmark that applies to the user's scenario, with its source as given in the file.
3. Name the most common mistake for that scenario.
4. If the request is really a hand-off case, say so and point to the right skill instead of
   half-answering here.

Rules for any email text this skill produces (frameworks, re-engagement templates):
- The CTA is interest-based: an interest question, an offer to send something, or a routing question.
  Never a call, meeting or time-slot ask. If installed, `cta-interest-based` (pack
  outbound-engine-skills) has the CTA bank and wins over any template.
- No invented results, client names or figures. Unfilled placeholders stay visible.

## Hand-off

If installed (pack outbound-engine-skills unless noted):

| The ask | Skill |
|---|---|
| Write a first-touch email or a full sequence | `sequence-writer` |
| Follow-ups inside an active sequence | `followup-sequence` |
| Subject lines | `subject-line-generator` |
| P.S. lines and personalisation at scale | `ps-line-generator`, `personalization-pipeline` |
| Choose the angle before writing | `angle-finder` |
| Answer one inbound reply or objection | `reply-objection-handler` |
| Analyse a batch of replies | `reply-audit` |
| Judge whether campaign numbers are good | `outbound-analyst` |
| Audit an existing setup's deliverability (this skill builds; that one audits) | `deliverability-audit` |
| ICP, signals, hypotheses | `icp-builder`, `signal-research`, `hypothesis-builder` |

## Credits

Modules condensed and rewritten from a public cold-outreach playbook collection, including its
email-infrastructure guide and an outbound agency's lessons from 10M+ emails; framework names credited
to their creators. Further figures from a cold-email playsheet built on a sending platform's data
(2025) and Google's email sender guidelines. Router, practitioner rules and re-engagement templates: Victor Shulga
(victorshulga.com).
