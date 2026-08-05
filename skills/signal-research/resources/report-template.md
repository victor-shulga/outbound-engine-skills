# Coverage report template

The list says who to contact. The report says whether the method is repeatable. Ship both.
Written in the working language of the team; the list stays a CSV.

---

## 1. Header

Client · base name and size · run mode (full / delta) · run date · geo scope · who ran it.
One line linking the enriched files.

## 2. Main takeaway

Three to five sentences. What the base actually looks like now: how many accounts carry a live
signal, which signal type dominates, and the one thing to do first. If the honest answer is "the
base is mostly cold and the geo has no free source", write that.

## 3. Funnel

```
raw rows            N
after dedup         N
after stop-filters  N   (geo −n · size −n · anti-ICP −n)
researched          N
with live signal    N   (x%)
  hot / warm / cool     n / n / n
```

## 4. Signal breakdown

| Signal | Tier | Accounts fired | % of researched | Median age (days) | Verdict |
|---|---|---|---|---|---|

Verdict per signal: `keep` · `keep, cheaper route needed` · `kill — no yield` · `kill — undetectable`.
A planned signal that fired zero times is a finding, and it belongs in this table, not omitted.

## 5. Source yield

| Source | Rung | Accounts covered | Signals produced | Cost | Cost per signal |
|---|---|---|---|---|---|

Rank by cost per signal. This table decides what next run's plan looks like.

## 6. Geo coverage

| Geo bucket | Accounts | Source available | Signals found | Note |
|---|---|---|---|---|

An empty bucket is reported explicitly with the reason (no open source with firm names, paid only,
legal stop) — never left as a blank cell that reads like "nothing happening there".

## 7. Data quality warnings

Everything that makes a number in this report less than solid, stated before anyone acts on it:
fuzzy matches used and spot-check result, approximate dates, datasets with decaying volume, feeds
that turned out dead, rate limits or blocks hit, accounts whose fit could not be verified.

## 8. Top accounts

Hot tier in full, warm tier top N. Per account: company · signal · evidence link · date · age ·
score · one-line why-now. This is the part the sales side reads.

## 9. Actions

| Action | Owner | Date |
|---|---|---|

Include the Hot-tier touch SLA and the `rescan_due` date as concrete actions with owners. A run
that ends without a scheduled re-scan produces a base that will be fiction in two months.

## 10. What stayed open

Signals wanted but undetectable at this budget, geos without a source, accounts left unresearched
because of the batch cap — with the number, so the gap stays visible instead of dissolving.

---

## Delta run — replaces sections 3–4

## 3d. Change table

| Change | Accounts | Note |
|---|---|---|
| new fire | n | never had a signal, now do |
| refired | n | burnt earlier, fresh event |
| burnt | n | past window, demoted to data point |
| unchanged | n | still live inside window |
| still cold | n | researched again, nothing |

## 4d. Burn rate

Signals burnt ÷ signals live at previous run, and the implied re-scan cadence. If more than half
the base burnt in the interval, the interval is too long — state the corrected cadence.
