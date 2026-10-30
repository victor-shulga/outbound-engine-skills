---
name: prospect-scoring
description: Score an account BEFORE any contact — profile fit only, from data you can read without talking to anyone. Use when asked to qualify or rank a cold base, set a fit gate, decide who is worth outreach at all, or sort a list into outreach queues. Triggers include "score this base", "qualify the list", "ICP fit score", "who is worth writing to", "rank these accounts". This is the pre-contact half of scoring — for ranking leads you have already spoken to, use `lead-scoring`.
---

# Prospect Scoring

Answers one question about a cold account: **is this profile ours, before anyone has spoken to them?**

Everything here is readable without a conversation — what they do, who they serve, what they run.
Nothing that only a call can establish belongs in this score. That is `lead-scoring`.

## The rule that fixes most broken rubrics

**Never score a dimension you already use as a stop-filter.**

If geography and headcount are hard gates at the filtering step, they must not also carry points.
Every surviving account passed them by definition, so those points are free, identical for everyone,
and they inflate the total until the threshold stops separating anything. A rubric that spread
100 points across four dimensions where two were already gates had to be replaced for exactly this:
the numbers looked discriminating and were not.

What is left after removing the gates is usually small — and that is correct. A pre-contact score
built on two honest dimensions beats one built on eight where six are noise.

## What the score is made of

Profile only. A workable default, to be tuned per ICP:

| Dimension | Max | Read from |
|---|---:|---|
| ICP fit — are they the kind of company we serve | 15 | their own description of themselves: site, company page, specialties |
| Services fit — do they need the specific thing we sell | 15 | services listed, work shown, capability they clearly lack or clearly run in-house |

Each dimension is scored on four levels, so two people scoring the same account land on the same number:

| Points | ICP fit | Services fit |
|---:|---|---|
| 15 | their own description names your niche and sub-industry | they do not have this service, and the work for it is visibly there |
| 10 | your industry, a neighbouring sub-industry | they run it in-house, but with 1–2 people |
| 5 | the description is vague, the niche has to be guessed | they have their own team; your service would only add to it |
| 0 | no data → `data-gap` flag | no data → `data-gap` flag |

**Gate:** a floor on the total (e.g. 20 of 30). Below it the account does not enter outreach,
whatever else is true about it.

| Example | Total | Decision |
|---|---:|---|
| 15 + 10 | 25 | outreach |
| 10 + 10 | 20 | outreach |
| 15 + 0 | 15 | fill the data gap, then score again |
| 5 + 5 | 10 | no outreach |

Add a dimension only if it is (a) readable cold, (b) not already a gate, and (c) actually varies
across the base. Deal potential qualifies only when the base genuinely carries it — usually it does
not, see normalisation below.

## The signal is a ROUTE, not points

This is the second thing rubrics get wrong. A buying signal does not make an account a better fit —
it makes it a better **time**. Fit and timing are different axes and must not be summed into one
number, or an account with a perfect profile and no trigger looks worse than a poor-fit account that
happens to be hiring.

So the signal sets the queue, not the score:

| Queue | Condition | What the opening line stands on |
|---|---|---|
| **A** | strong live signal | the event, dated, with a link |
| **B** | weaker or older signal | the event, framed softer |
| **D** | no live signal | a data point from their own site |

No signal is not a low score. It is queue D plus a monitoring window — re-check in ~30 days before
concluding there is nothing there.

**An open role that has stayed open 45+ days is a stronger signal than a fresh one** — they cannot
fill it. Do not decay a vacancy while it is still open.

## Missing data

1. **Missing → 0 plus a `data-gap` flag. Never a guess, never a midpoint.** A guessed firmographic
   becomes a forecast somebody relies on.
2. **Normalise when a whole dimension is structurally empty.** If nobody in the base has deal size,
   that dimension is 0 for everyone, the ceiling drops, and no account clears the gate. Keep two
   numbers: the raw sum, and the same sum as a percentage of the dimensions that actually had data.
   Gate on the second — but only at data confidence M or H. At L, fall back to the raw sum, so a row
   with two filled fields cannot look perfect.
3. **A tier is set only on a verified number.** Where headcount is unconfirmed the tier cell reads
   "verify manually" — never blank, never inferred.

## The headcount trap, from both directions

Worth stating because the obvious fix breaks the opposite case.

Company sites systematically overstate the team: a site claiming dozens of engineers can be a firm of
three. The instinct is to take the smaller of the available numbers — and that immediately breaks
large firms, because a big agency does not list its staff by name, so a named count returns a
fraction of the truth.

The construction that survives both: **the company page headcount is the source; a named count on
their site is only a CHECK, never a source.** When the named count is several times smaller and the
page figure is itself small, flag the row and cap it below the top band — it needs human eyes, but it
is not discarded.

Keep the numbers in separate columns. The moment they are merged into one "headcount" field, you can
no longer tell a verified figure from an inferred one.

## Terms and plain-language output

<!-- glossary:start terms=fit-score,fit-gate,data-gap,data-confidence,outreach-queue,buying-signal,data-point,account-tier,enrichment -->
Rules for every document a client or their team will read (review, roast, canvas, offer cards, instruction):

1. **Open with «Словник цього документа»**: only the terms that actually appear in it, at most 10, each as «термін: що це простими словами». Like the definitions section of a contract.
2. **No internal codes or letter scales in the text** (A/B/C, D L T E, BLEND numbers without words, Own/Shared/Generic, Z1.4, GATE 2.5, T1–T6). Write the meaning instead: «є цифра з клієнтом», not «A».
3. **Use the plain form from the table below.** English stays only for tool names and for copy that ships in English (promises, hooks, subject lines). If the document is in another language, translate the plain form, never the internal term.
4. **Do not score what cannot exist yet.** A block that depends on work not done (signal catalog, case studies, a previous step) gets «пропущено: спершу потрібно <що саме>», not a score.
5. **Every section of a review opens with one concrete action** («до наступного дзвінка: …»), then at most five lines of why. No paragraph that only restates the framework.


| Internal term (this skill) | Write for the reader | What it means |
|---|---|---|
| ICP fit, services fit, prospect score, prospect profile | оцінка відповідності профілю | Бали за те, чи компанія з вашої ніші і чи їй бракує саме вашої послуги; рахуємо ще до першого контакту. |
| gate, fit gate, floor, hard gate, clamp | стоп-фільтр (мінімальний поріг) | Межа, нижче якої компанії не пишемо, хоч би що ще про неї було відомо. |
| data-gap flag, missing → 0 | бракує даних | Поле, яке не вдалося знайти, ставимо в нуль з позначкою; середнє значення не вгадуємо. |
| data confidence H / M / L | впевненість у даних: висока · середня · низька | Наскільки заповнені й перевірені поля компанії; від цього залежить, чи можна довіряти оцінці. |
| queue A / B / D, no-signal queue | черга: свіжий сигнал · слабший чи старіший сигнал · без сигналу | Від черги залежить, з чого відкриваємо лист: з події з датою чи з факту з їхнього сайту; відсутність сигналу не знижує оцінку. |
| buying signal | ознака готовності купувати | факт про компанію, після якого розмова про вашу послугу доречна саме зараз. |
| data point, state signal | факт про компанію (дата-поінт) | Факт з їхнього сайту чи вакансії, з якого відкриваємо лист; подія підказує, коли писати, а факт підказує, що сказати. |
| Tier 1 / Tier 2 / Tier 3, tier | тір: група компаній за розміром і чеком | усередині однієї ніші ділимо компанії за розміром і можливим чеком; від тіру залежить офер і скільки уваги даємо |
| enrichment, enrich | дозбір даних | Пошук імен, посад і робочих пошт для компаній зі списку з кількох джерел. |
<!-- glossary:end -->

## Output

One row per account: `Company · Tier · per-dimension points · Raw total · Normalised total ·
Data confidence in words (high / medium / low) · Passes the fit floor (yes / no) · Outreach queue in words (fresh dated signal / weaker or older signal / no signal, opens on a fact from their site) · Missing fields`.

Plus a `data-gap` list: accounts that need enrichment before the score means anything. Rows that fail
the gate stay in the file with the reason — deleting them means re-buying and re-researching them a
quarter later.

## Don't

- Don't score anything a stop-filter already decided.
- Don't sum fit and timing into one number.
- Don't round up on doubt — take the lower band.
- Don't run a real base on weights nobody approved. If they are not confirmed, say so and label the
  run a draft preview.

## Handoff

Gate passed → queue assigned → `waterfall-enrichment` for contacts, then `sequence-writer` per
campaign. After a reply lands, the account moves to `lead-scoring`, which starts from this profile
and adds what only a conversation can establish.
