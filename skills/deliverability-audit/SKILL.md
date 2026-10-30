---
name: deliverability-audit
description: Use when asked to check email deliverability, audit sending infrastructure, investigate spam issues, or set up domains and mailboxes correctly
---

# Deliverability Audit

Audit the sending infrastructure and return a pass/fail verdict on every deliverability dimension — with specific fixes for anything that fails.

## What you need

- Sending domain(s) and mailbox addresses
- Sending platform being used
- Current send volume per mailbox per day
- How long the domains/mailboxes have been active

## Audit checklist

**Domain setup**
- [ ] SPF record configured correctly
- [ ] DKIM record configured and active
- [ ] DMARC policy set (minimum `p=none` with monitoring; `p=quarantine` recommended)
- [ ] MX records pointing to the correct mail server
- [ ] Domain is not on any major blacklists (MXToolbox check)

**Mailbox setup**
- [ ] Mailbox has a real name (not "info@" or "sales@")
- [ ] Profile photo set (where platform allows)
- [ ] Email signature includes real name, role, and website
- [ ] Mailbox is at least 14 days old before first campaign send
- [ ] Warm-up is active (if platform supports it)

**Sending behavior**
- [ ] Max sends per mailbox: 30–40/day for new mailboxes, up to 50/day for established
- [ ] Send window: business hours in recipient timezone (8am–6pm)
- [ ] Sending days: Monday–Thursday only for cold outbound
- [ ] Minimum delay between sends: 3–5 minutes
- [ ] Unsubscribe link present in every email

**Warm-up status**
- [ ] Warm-up tool active (Instantly, Mailreach, or equivalent)
- [ ] Minimum 14-day warm-up before sending cold campaigns
- [ ] Warm-up volume: at least 30–50 warm-up emails per day per mailbox
- [ ] Inbox placement rate above 90% on warm-up reports

## Process

1. Request domain and mailbox details
2. Check DNS records via MXToolbox or equivalent
3. Check blacklist status for all sending domains
4. Review sending platform settings against checklist
5. Assign pass/fail to each dimension
6. Return remediation list for any failures, ordered by severity

## Terms and plain-language output

<!-- glossary:start terms=spf-dkim-dmarc,warmup,blacklist,inbox-placement,send-caps,secondary-domain,bounce-rate -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| SPF / DKIM / DMARC, MX | SPF, DKIM, DMARC (записи, що підтверджують домен) | Технічні записи в налаштуваннях домену, які доводять поштовим сервісам, що лист справді від вас; без них листи йдуть у спам. |
| warmup | прогрів поштових скриньок | поступове збільшення кількості листів з нової скриньки, щоб пошта не потрапила в спам. |
| blacklist, listed | чорний список поштових сервісів | Перелік доменів, яким сервіси не довіряють; потрапили туди, тож розсилку зупиняємо і шукаємо причину. |
| inbox placement rate | частка листів у вхідних | Скільки листів потрапляє у вхідні замість спаму; нижче 90% з розсилкою чекаємо. |
| send caps, daily volume per mailbox, ramp | денний ліміт на скриньку | Скільки листів одна скринька надсилає за день; ліміт піднімаємо поступово і масштабуємось кількістю скриньок. |
| secondary domain, sending domain | окремий домен для розсилки | Домен, схожий на основний, лише для холодних листів, щоб проблеми з доставкою не зачепили основну пошту. |
| bounce | відмови доставки | частка листів, які не дійшли, бо адреса неправильна чи мертва. |
<!-- glossary:end -->

## Output format

```
Deliverability audit: [domain(s)]
Date: [date]

DOMAIN SETUP
SPF: [PASS / FAIL] — [detail]
DKIM: [PASS / FAIL] — [detail]
DMARC: [PASS / FAIL] — [detail]
Blacklist status: [CLEAN / LISTED] — [which lists if any]

MAILBOX SETUP
[mailbox@domain] — [pass count]/[total checks] — [list of failures]

SENDING BEHAVIOR
Daily volume: [SAFE / HIGH / CRITICAL]
Send window: [PASS / FAIL]
Warm-up: [ACTIVE / INACTIVE / NOT CONFIGURED]

VERDICT
Infrastructure ready to send: [YES / NO / WITH FIXES]

REMEDIATION (ordered by severity)
1. [Critical fix — do immediately]
2. [Important fix — do this week]
3. [Nice to have — do when time permits]
```

## Notes

- Do not start cold sending until SPF, DKIM, and DMARC all pass — deliverability problems compound fast
- Blacklisted domain = stop all sending immediately and investigate the cause before delisting
- 30 emails/day per mailbox is conservative and safe; 50 is the ceiling — never go higher on cold outbound
- Warm-up should never be turned off during active campaigns — even pausing for a few days can drop inbox rate
- Use separate domains for cold outbound — never send cold email from your main company domain
