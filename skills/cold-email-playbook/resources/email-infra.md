# Email sending infrastructure

How to build cold-email sending capacity from nothing, keep it healthy, and repair it when it
breaks. Platform-neutral: the steps apply to any sequencer that connects Google Workspace or
Microsoft 365 mailboxes. Prices and admin-console paths change; check them at setup time.

Sources: the sizing method, provider split, ramp and recovery steps are condensed from ColdIQ's
public GTM skills (infrastructure module by ColdIQ and Ivan Falco). Lines marked [Practitioner] come
from Victor Shulga's own deliverability work. Google sender rules are from Google's published email
sender guidelines.

---

## 1. Order of work

1. Size the setup (how many mailboxes and domains).
2. Buy secondary domains.
3. Create one workspace or tenant per domain, two mailboxes each.
4. Publish DNS: MX, SPF, DKIM, DMARC. Point the domain at a live page.
5. Connect mailboxes to the sending platform.
6. Warm up.
7. Go live slowly.
8. Monitor on a fixed cadence.

Steps 1-5 take about two hours of work for a small setup. Step 6 is calendar time: plan the first
campaign for setup day plus three weeks [Practitioner].

## 2. Rules that hold everywhere

- The company's main domain never sends cold email. A burned main domain takes invoices, support and
  hiring mail down with it.
- Two mailboxes per domain at most, so one burned domain costs two senders.
- One domain per Google Workspace account or Microsoft 365 tenant. Several domains in one tenant
  share reputation and fail together.
- Buy domains from more than one registrar.
- Warm-up runs before the first campaign and keeps running while campaigns are live.
- Scale by adding mailboxes. Raising the per-mailbox limit is the fastest way to lose a domain.

## 3. Sizing

Work backwards from the monthly goal:

```
daily volume   = monthly new-contact emails ÷ 20 working days
mailboxes      = daily volume ÷ 20 (careful) or ÷ 25 (aggressive)
with buffer    = mailboxes × 1.5   (spares for warm-up, rotation, accounts that break)
domains        = mailboxes with buffer ÷ 2, rounded up
```

Worked examples (careful rate, 20 per mailbox per day):

- 4,000 emails a month: 200 a day, 10 mailboxes, 15 with buffer, 8 domains.
- 10,000 a month: 500 a day, 25 mailboxes, 38 with buffer, 19 domains.
- 20,000 a month: 1,000 a day, 50 mailboxes, 75 with buffer, 38 domains.

Per-mailbox daily limits once fully ramped: Google Workspace about 15-25, Microsoft 365 about
10-15. ColdIQ's guide treats roughly 15 mailboxes as the practical floor for a programme that can
absorb a burned domain without stopping.

Provider mix: about 60% Google Workspace and 40% Microsoft 365. Two providers spread the risk, and
recipients on Outlook tend to receive Microsoft-sent mail more readily (and Gmail users
Google-sent mail).

Count follow-ups in the volume: a three-step sequence to 1,000 new contacts is close to 3,000 emails
if few reply.

## 4. Secondary domains

- Build names from the brand with a clean prefix or suffix: `get`, `try`, `meet`, `hello` + brand, or
  brand + `hq`, `team`, `group`. For a brand `brightpath.com`: `getbrightpath.com`,
  `brightpathhq.com`, `meetbrightpath.com`.
- Avoid typo-style lookalikes of the brand, digits, hyphen chains and salesy words. A crowd of
  near-misspellings of one brand reads as a spammer's fingerprint to filters and to people
  [Practitioner].
- Prefer `.com`; `.org` is a reasonable second. Newer TLDs carry less trust for cold mail.
- Spread purchases over two to four registrars. Turn on auto-renew and WHOIS privacy on every domain.
- Every sending domain must resolve to something real: a 301 redirect to the main site, or a one-page
  site. A sending domain with no working website is one of the strongest negative signals for Google
  and for corporate security gateways [Practitioner].
- Keep a register: domain, registrar, provider, mailboxes, admin login owner, warm-up status, health.

## 5. Workspaces and mailboxes

**Google Workspace** (Business Starter is enough): create a new account per domain, verify the domain
with the TXT record Google gives you, create two users with real first names.

**Microsoft 365** (Business Basic is enough): new tenant per domain, verify with TXT, create two users,
then in the admin center enable **Authenticated SMTP** and **IMAP** for each mailbox. Wait about an
hour after enabling before connecting the mailbox to a sending tool; earlier attempts fail.

Mailbox hygiene:
- Real first names (`anna@`, `mark@`). Role inboxes like `sales@` or `info@` look automated.
- Reuse the same names across domains so replies are easy to route.
- Add a profile photo and a plain signature to every mailbox.

## 6. DNS

All four records on every domain:

| Record | Job | Notes |
|---|---|---|
| MX | where incoming mail goes | set during workspace setup; replies must land somewhere |
| SPF | which servers may send for the domain | exactly one SPF record per domain |
| DKIM | cryptographic signature on each email | generated in the provider's admin console |
| DMARC | what receivers do when SPF or DKIM fail, and where reports go | never added automatically |

SPF values:
- Google: `v=spf1 include:_spf.google.com ~all`
- Microsoft: `v=spf1 include:spf.protection.outlook.com ~all`

Two SPF records on one domain is the most common mistake (some registrars create one by default).
Merge or delete until one remains.

DKIM: in Google Workspace generate the key under Gmail authentication and publish it at
`google._domainkey`; in Microsoft 365 publish the two CNAMEs (`selector1._domainkey`,
`selector2._domainkey`) and switch signing on. Paste values exactly, no added spaces.

DMARC: start with monitoring if you must, then enforce.
- Monitoring start: `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com`
- Target once SPF and DKIM pass: `v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarc@yourdomain.com; adkim=s; aspf=s`, later `p=reject`.
- Corporate security gateways weigh an unenforced `p=none` against the sender, so do not leave it
  there for long [Practitioner]. Google requires a DMARC record for anyone sending more than about
  5,000 messages a day to Gmail addresses, plus SPF and DKIM.

Tracking domain: if you use link or open tracking at all, set up the custom tracking CNAME your
sending platform provides (on Cloudflare, proxy off, grey cloud). Better still, send the first email
with no tracking.

Propagation: usually minutes to a few hours, up to 48 hours. Drop TTL to 300 seconds before changes,
raise it again once records are confirmed.

Test with: the sending platform's domain check, MXToolbox (records and blacklists), Mail-Tester (aim
for 8/10 or better), Google Postmaster Tools and Microsoft SNDS (reputation once volume exists).

## 7. Connecting to the sending platform

- Google: OAuth through the Workspace admin console (allow the platform's app as trusted) is the
  sturdiest connection. App passwords with 2FA are the fallback and allow CSV bulk import.
- Microsoft: usually connected one mailbox at a time, granting consent on behalf of the organization.
  Plan the time.
- Per mailbox after connecting: set the daily limit for its provider, enable the custom tracking
  domain if used, tag by provider and domain, enable slow ramp for new mailboxes only (switching it
  on for a mailbox already sending resets it to a trickle).

## 8. Warm-up

- Minimum two weeks, three recommended (ColdIQ). The ColdIQ and Instantly playsheet goes further:
  5-10 emails a day for 4-6 weeks. Plan on three weeks unless the domains are brand new and the
  stakes are high.
- Typical starting settings for a new mailbox: 10-15 warm-up emails a day with daily increase on,
  warm-up reply rate around 30-40%. Established mailboxes can run 20-30.
- Ready to send when the platform's health score is at least 70% (90%+ preferred) and both sent and
  received warm-up counts are climbing.
- Filter warm-up mail out of the visible inbox with the platform's tag so nobody answers it by hand.
- A warm-up pool status that turns to "disabled" almost always means DNS or bounces. Fix DNS first,
  then request reactivation.

## 9. Going live

Per-mailbox daily ramp (ColdIQ):
- Week 1: Google 10-15, Microsoft 5-10.
- Weeks 2-3: Google 15-20, Microsoft 10-12.
- Week 4 onward: Google 20-25, Microsoft 12-15.

Campaign settings that help placement:
- First email in plain text, no images, no links, open tracking off.
- Match sender provider to recipient provider where the platform supports it.
- Cap emails per company per day (2-3 across the whole workspace).
- Random gaps of several minutes between sends; send in the recipient's business morning, Tuesday to
  Thursday as the B2B default.
- First campaign: 50-100 verified contacts, watch for two or three days, then widen.
- Volume growth at most about 20% a week; launch new domains one per week at most; never change
  volume and copy in the same week, or you cannot tell which one moved the numbers.

## 10. Monitoring cadence

| When | Look at |
|---|---|
| Daily, 5 minutes | bounce, replies, spam complaints, blacklist alerts, disconnected mailboxes |
| Weekly, 15 minutes | Postmaster Tools and SNDS, blacklist check, week-on-week reply and bounce trend |
| Monthly | suppression list, bounce patterns by domain, retire stale contacts, refresh warm-up content |
| Quarterly | full DNS audit across every domain, cost per mailbox, capacity plan for next quarter |

Thresholds that trigger action: bounce over 5%, any spam complaint pattern, Google spam rate over 0.1%
(never let it reach 0.3%).

## 11. Recovery protocols

**Bounce spike (over 5%)**: pause the affected campaigns, find the source (list, a single domain,
DNS), remove every bounced address, then resume at half volume for about three days, three quarters
for the next three, and full volume after that if bounce stays under 2%.

**Blacklisted**: stop sending from that domain at once. Identify the list (Spamhaus matters most for
major mailbox providers; Barracuda for corporate filters). Fix the cause, then follow that list's
delisting procedure. A domain on several lists is cheaper to retire than to repair; replace it and
warm the new one fully.

**Engagement drop with clean infrastructure**: ask what changed and when (list, copy, volume, timing,
CTA), whether all domains dropped or a few, and whether a season explains it (December, July-August,
the sector's main conference week). Roll back to the last working version and change one variable
at a time.

## 12. Troubleshooting table

| Symptom | Check first | Fix |
|---|---|---|
| "DNS record not found" | record saved on the right domain at the right registrar; propagation time | re-save, lower TTL, wait, re-test |
| "Multiple SPF records" | all TXT records starting `v=spf1` | keep one |
| DKIM fails | host name and exact value | regenerate, republish, wait up to 24 hours, restart signing |
| DMARC missing | `_dmarc` TXT record | add it; it is never created for you |
| Tracking domain not verifying | CNAME target; Cloudflare proxy | correct the CNAME, proxy off |
| Microsoft mailbox will not connect | SMTP and IMAP enabled; one hour passed | enable both, wait, retry in a private window |
| Warm-up health under 70% | DNS, domain age, blacklist | fix DNS, lower warm-up volume for a week |
| High bounce on valid-looking addresses, concentrated on some recipient companies | whether those companies sit behind security gateways (Mimecast, Proofpoint, Barracuda show in their MX) | enforce DMARC, put a live site on the sending domain, cut lookalike domains to a few, keep daily send under the warm-up limit [Practitioner] |
| Bounces on typo domains and dead mailboxes that passed verification | the list itself | re-verify, hand-check a sample; verifiers return false positives |
| Zero opens | whether open tracking is on | nothing to fix if tracking is off; judge on replies |
| Reply rate under 1% with clean infrastructure | list and offer | skip seed tests; new list or new angle, then relaunch |

What is usually NOT the cause, once checked: a blacklist when Spamhaus and MXToolbox are clean; DKIM
when it passes; a reverse-DNS mismatch on Google's shared sending servers.
