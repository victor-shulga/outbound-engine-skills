#!/usr/bin/env python3
"""Pre-launch data check: is this CSV safe to load into the sender today?

Runs on the FINAL file — after enrichment and personalization, right before upload.
Standard library only. Reads one CSV, optionally several suppression files, and prints
a per-layer report with a verdict: GO / GO WITH FIXES / STOP.

    python3 check_list.py leads.csv
    python3 check_list.py leads.csv --suppress crm_export.csv active_campaigns.csv clients.csv \
        --vars first_name,company,first_line --max-signal-age 60 --mailboxes 6 --daily-cap 30

Column names are auto-detected (email, first_name, company, domain, title, linkedin,
email_status, tier, signal_date, signal_source). Override any of them with --col key=header.

Exit code: 0 = GO, 1 = GO WITH FIXES, 2 = STOP. Use --out to write the rows that failed.
"""

import argparse
import csv
import datetime as dt
import re
import sys
from collections import Counter, defaultdict

ALIASES = {
    "email": ["email", "work_email", "email_address", "e-mail", "mail"],
    "first_name": ["first_name", "firstname", "first name", "name_first"],
    "last_name": ["last_name", "lastname", "last name"],
    "company": ["company", "company_name", "organization", "account", "account_name"],
    "domain": ["domain", "company_domain", "website", "company_website", "url"],
    "title": ["title", "job_title", "position", "role", "headline"],
    "linkedin": ["linkedin", "linkedin_url", "person_linkedin_url", "li_url", "profile_url"],
    "email_status": ["email_status", "verification", "verification_status", "status", "email_verification", "risk"],
    "tier": ["tier", "queue", "icp_tier", "segment", "priority"],
    "sender": ["sender", "mailbox", "owner", "assigned_to", "campaign"],
    "signal_date": ["signal_date", "event_date", "signal_at", "trigger_date", "posted_at"],
    "signal_source": ["signal_source", "source_url", "evidence_url", "signal_url", "proof_url"],
}

ROLE_PREFIXES = {"info", "sales", "hello", "contact", "admin", "office", "support", "team",
                 "hr", "jobs", "careers", "marketing", "billing", "noreply", "no-reply", "enquiries"}
FREE_MAIL = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "aol.com",
             "proton.me", "protonmail.com", "gmx.com", "mail.ru", "ukr.net", "yandex.ru", "live.com"}
PLACEHOLDER = re.compile(r"\{\{|\}\}|\[[A-Z _]+\]|^(n/?a|null|none|undefined|-|tbd|#n/a)$", re.I)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I)


def norm(s):
    return (s or "").strip()


def dom_of(url_or_domain):
    d = norm(url_or_domain).lower()
    d = re.sub(r"^https?://", "", d)
    d = d.split("/")[0]
    return d[4:] if d.startswith("www.") else d


def li_key(u):
    u = norm(u).lower().rstrip("/")
    m = re.search(r"linkedin\.com/in/([^/?#]+)", u)
    return m.group(1) if m else ""


def status_bucket(v):
    v = norm(v).lower()
    if not v:
        return "unknown"
    if "catch" in v or "accept_all" in v or "accept-all" in v:
        return "catch-all"
    if v in {"valid", "deliverable", "ok", "verified", "safe", "a", "b"}:
        return "valid"
    if v in {"invalid", "undeliverable", "bounce", "bounced", "f", "e", "spamtrap", "disposable"}:
        return "invalid"
    if v in {"risky", "unknown", "c", "d", "unverifiable"}:
        return "risky"
    return "unknown"


def parse_date(v):
    v = norm(v)
    m = re.match(r"(\d{4})[-/](\d{2})[-/](\d{2})", v)      # 2026-09-14, 2026/09/14, ISO datetime
    if m:
        y, mo, d = map(int, m.groups())
    else:
        m = re.match(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", v)   # 14.09.2026
        if m:
            d, mo, y = map(int, m.groups())
        else:
            m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", v)  # 09/14/2026 (US)
            if not m:
                return None
            mo, d, y = map(int, m.groups())
    try:
        return dt.date(y, mo, d)
    except ValueError:
        return None


def detect(headers, overrides):
    low = {h.lower().strip(): h for h in headers}
    cols = {}
    for key, names in ALIASES.items():
        if key in overrides:
            cols[key] = overrides[key] if overrides[key] in headers else None
            continue
        cols[key] = next((low[n] for n in names if n in low), None)
    return cols


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        r = csv.DictReader(f, dialect=dialect)
        return r.fieldnames or [], list(r)


def suppression_keys(paths, overrides):
    emails, lis, domains = set(), set(), set()
    for p in paths:
        headers, rows = read_csv(p)
        c = detect(headers, overrides)
        for row in rows:
            if c["email"] and norm(row.get(c["email"])):
                emails.add(norm(row[c["email"]]).lower())
            if c["linkedin"] and li_key(row.get(c["linkedin"])):
                lis.add(li_key(row[c["linkedin"]]))
            # a file with domains but no people = company-level suppression (clients, DNC accounts)
            if c["domain"] and not c["email"] and not c["linkedin"] and norm(row.get(c["domain"])):
                domains.add(dom_of(row[c["domain"]]))
    return emails, lis, domains


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--suppress", nargs="*", default=[], help="CSV files whose people/companies must not be contacted")
    ap.add_argument("--vars", default="first_name,company", help="comma list of columns the sequence uses as variables")
    ap.add_argument("--max-signal-age", type=int, default=60, help="days; older signals count as stale")
    ap.add_argument("--max-per-company", type=int, default=3)
    ap.add_argument("--catch-all-max", type=float, default=0.25, help="share of catch-all above which the batch is a fix")
    ap.add_argument("--min-volume", type=int, default=300, help="volume gate per hypothesis (300 event signal, 500 data point)")
    ap.add_argument("--mailboxes", type=int, default=0)
    ap.add_argument("--daily-cap", type=int, default=30, help="new contacts per mailbox per day")
    ap.add_argument("--col", action="append", default=[], help="override a column: key=Header Name")
    ap.add_argument("--out", help="write failing rows with a 'problems' column to this CSV")
    a = ap.parse_args()

    overrides = dict(x.split("=", 1) for x in a.col)
    headers, rows = read_csv(a.csv)
    c = detect(headers, overrides)
    n = len(rows)
    today = dt.date.today()
    problems = defaultdict(list)          # row index -> list of problems
    stops, fixes, notes = [], [], []

    print(f"Pre-launch data check: {a.csv}")
    print(f"Date: {today.isoformat()} | Rows: {n}")
    print("Columns detected: " + ", ".join(f"{k}={v}" for k, v in c.items() if v))
    if n == 0:
        print("\nVERDICT: STOP — the file has no rows.")
        return 2
    if not c["email"] and not c["linkedin"]:
        print("\nVERDICT: STOP — no email or LinkedIn column found. Map it with --col email=<header>.")
        return 2

    # 1 · SOURCE — duplicates and suppression
    print("\n1 · SOURCE — duplicates and suppression")
    seen_e, seen_l = {}, {}
    dup = 0
    for i, r in enumerate(rows):
        e = norm(r.get(c["email"])).lower() if c["email"] else ""
        l = li_key(r.get(c["linkedin"])) if c["linkedin"] else ""
        hit = (e and e in seen_e) or (l and l in seen_l)
        if hit:
            dup += 1
            problems[i].append("duplicate in file")
        if e:
            seen_e.setdefault(e, i)
        if l:
            seen_l.setdefault(l, i)
    print(f"  duplicates inside the file: {dup}")
    if dup:
        fixes.append(f"{dup} duplicate rows — keep one per person")

    if a.suppress:
        se, sl, sd = suppression_keys(a.suppress, overrides)
        sup = 0
        for i, r in enumerate(rows):
            e = norm(r.get(c["email"])).lower() if c["email"] else ""
            l = li_key(r.get(c["linkedin"])) if c["linkedin"] else ""
            d = dom_of(r.get(c["domain"])) if c["domain"] else (e.split("@")[-1] if e else "")
            if (e and e in se) or (l and l in sl) or (d and d in sd):
                sup += 1
                problems[i].append("on a suppression list")
        print(f"  on suppression lists ({len(a.suppress)} files, {len(se)} emails, {len(sl)} profiles, {len(sd)} companies): {sup}")
        if sup:
            stops.append(f"{sup} rows are on a suppression list (CRM / active campaign / client / opt-out) — remove before upload")
    else:
        print("  suppression: NOT CHECKED — no --suppress files given")
        notes.append("suppression not checked: pass the CRM export, active campaigns, current clients and opt-outs")

    per_company = Counter()
    for r in rows:
        key = dom_of(r.get(c["domain"])) if c["domain"] else norm(r.get(c["company"])).lower() if c["company"] else ""
        if key:
            per_company[key] += 1
    heavy = {k: v for k, v in per_company.items() if v > a.max_per_company}
    print(f"  companies: {len(per_company)} | above {a.max_per_company} contacts: {len(heavy)}")
    if heavy:
        fixes.append(f"{len(heavy)} companies carry more than {a.max_per_company} contacts — trim to the 2–3 who own the problem")

    # 2 · VALIDATION — can the address take the email
    print("\n2 · VALIDATION — addresses")
    buckets = Counter()
    role = free = malformed = mismatch = 0
    if c["email"]:
        for i, r in enumerate(rows):
            e = norm(r.get(c["email"])).lower()
            if not e:
                buckets["no email"] += 1
                continue
            if not EMAIL_RE.match(e):
                malformed += 1
                problems[i].append("malformed email")
                continue
            local, edom = e.split("@", 1)
            if local in ROLE_PREFIXES:
                role += 1
                problems[i].append("role address")
            if edom in FREE_MAIL:
                free += 1
                problems[i].append("free-mail address")
            if c["domain"] and norm(r.get(c["domain"])):
                cd = dom_of(r[c["domain"]])
                if cd and edom != cd and not edom.endswith("." + cd) and edom not in FREE_MAIL:
                    mismatch += 1
            b = status_bucket(r.get(c["email_status"])) if c["email_status"] else "unknown"
            buckets[b] += 1
            if b == "invalid":
                problems[i].append("invalid email")
            elif b == "risky":
                problems[i].append("risky email")
    with_email = n - buckets["no email"]
    for k in ("valid", "catch-all", "risky", "invalid", "unknown", "no email"):
        if buckets[k]:
            print(f"  {k}: {buckets[k]} ({buckets[k] / n:.0%})")
    print(f"  malformed: {malformed} | role addresses: {role} | free-mail: {free} | email domain ≠ company domain: {mismatch}")
    if c["email"] and not c["email_status"]:
        stops.append("no verification column — run every address through a validator before upload")
    if buckets["invalid"] or malformed:
        stops.append(f"{buckets['invalid'] + malformed} invalid or malformed addresses — they bounce and burn the domain")
    if buckets["risky"]:
        fixes.append(f"{buckets['risky']} risky addresses — drop them or re-verify; never send risky")
    if c["email_status"] and buckets["unknown"]:
        fixes.append(f"{buckets['unknown']} addresses with no or unrecognised verification status")
    if with_email and buckets["catch-all"] / with_email > a.catch_all_max:
        fixes.append(f"catch-all is {buckets['catch-all'] / with_email:.0%} of the batch (limit {a.catch_all_max:.0%}) — send them as a small separate batch first")
    if role:
        fixes.append(f"{role} role addresses (info@, sales@…) — find the named person or drop")
    if free:
        notes.append(f"{free} free-mail addresses — fine for a solo founder, suspicious for a company contact")
    if mismatch:
        notes.append(f"{mismatch} emails on a different domain than the company — check they still work there")

    # 3 · COMPLETENESS — every variable the sequence uses is filled and rendered
    print("\n3 · COMPLETENESS — sequence variables")
    wanted = [v.strip() for v in a.vars.split(",") if v.strip()]
    for v in wanted:
        col = c.get(v) or (v if v in headers else None)
        if not col:
            print(f"  {v}: column MISSING")
            stops.append(f"sequence variable '{v}' has no column — every email would render it empty")
            continue
        empty = placeholder = 0
        for i, r in enumerate(rows):
            val = norm(r.get(col))
            if not val:
                empty += 1
                problems[i].append(f"empty {v}")
            elif PLACEHOLDER.search(val):
                placeholder += 1
                problems[i].append(f"placeholder in {v}")
        print(f"  {v} ({col}): empty {empty}, placeholder/unrendered {placeholder}")
        if empty or placeholder:
            stops.append(f"'{v}': {empty} empty + {placeholder} unrendered — those emails go out broken")

    # 4 · ROUTING — every row knows its queue and sender
    print("\n4 · ROUTING — tier / queue / sender")
    for key in ("tier", "sender"):
        if c[key]:
            vals = Counter(norm(r.get(c[key])) or "(empty)" for r in rows)
            print(f"  {key} ({c[key]}): " + ", ".join(f"{k} {v}" for k, v in vals.most_common(6)))
            if vals.get("(empty)"):
                fixes.append(f"{vals['(empty)']} rows with no {key} — route them before upload")
        else:
            print(f"  {key}: no column")
    if not c["tier"]:
        fixes.append("no tier/queue column — the A/B/D queues from prospect-scoring are not in the file")

    # 5 · HYGIENE — what the reader sees in the first line
    print("\n5 · HYGIENE — names, titles, companies")
    caps = lower = legal = 0
    if c["first_name"]:
        for i, r in enumerate(rows):
            fn = norm(r.get(c["first_name"]))
            if len(fn) > 1 and fn.isupper():
                caps += 1
                problems[i].append("first name in CAPS")
            elif fn and fn[0].islower():
                lower += 1
                problems[i].append("first name lowercase")
    if c["company"]:
        for r in rows:
            if re.search(r"\b(llc|inc\.?|ltd\.?|gmbh|s\.?r\.?l\.?|sp\. z o\.o\.|limited|corp\.?)$", norm(r.get(c["company"])), re.I):
                legal += 1
    print(f"  first name CAPS: {caps} | lowercase: {lower} | company with legal suffix: {legal}")
    if caps or lower:
        fixes.append(f"{caps + lower} first names need case fixing — 'Hi JOHN' reads as a mail merge")
    if legal:
        fixes.append(f"{legal} company names carry a legal suffix (LLC, Inc, GmbH) — strip it for the copy")
    if c["title"]:
        empty_t = sum(1 for r in rows if not norm(r.get(c["title"])))
        print(f"  empty titles: {empty_t}")
        if empty_t:
            notes.append(f"{empty_t} contacts with no title — cannot confirm they are the persona")

    # 6 · SIGNALS — the reason to write now is still fresh
    print("\n6 · SIGNALS — freshness and proof")
    if c["signal_date"]:
        stale = undated = 0
        for i, r in enumerate(rows):
            raw = norm(r.get(c["signal_date"]))
            if not raw:
                continue
            d = parse_date(raw)
            if not d:
                undated += 1
                continue
            if (today - d).days > a.max_signal_age:
                stale += 1
                problems[i].append(f"signal older than {a.max_signal_age} days")
        print(f"  stale (> {a.max_signal_age} days): {stale} | unparseable dates: {undated}")
        if stale:
            fixes.append(f"{stale} rows open on a signal older than {a.max_signal_age} days — move them to the data-point queue or re-check")
        if c["signal_source"]:
            nosrc = sum(1 for r in rows if norm(r.get(c["signal_date"])) and not norm(r.get(c["signal_source"])))
            print(f"  signal without a source link: {nosrc}")
            if nosrc:
                fixes.append(f"{nosrc} signals have no source link — an opening line you cannot prove")
    else:
        print("  no signal date column — freshness NOT CHECKED")
        notes.append("signal freshness not checked (no signal_date column)")

    # 7 · ACTIVATION — volume and capacity
    print("\n7 · ACTIVATION — volume and sending capacity")
    sendable = n - len([i for i, p in problems.items() if any(x in p for x in (
        "duplicate in file", "on a suppression list", "invalid email", "malformed email", "risky email"))])
    print(f"  sendable after removals: {sendable} (volume gate {a.min_volume})")
    if sendable < a.min_volume:
        fixes.append(f"only {sendable} sendable rows — below the {a.min_volume} volume gate, the test will not read")
    if a.mailboxes:
        per_day = a.mailboxes * a.daily_cap
        days = -(-sendable // per_day) if per_day else 0
        print(f"  capacity: {a.mailboxes} mailboxes × {a.daily_cap}/day = {per_day} new contacts/day → {days} sending days")
    else:
        print("  capacity: not checked (pass --mailboxes)")

    # verdict
    verdict, code = ("STOP", 2) if stops else (("GO WITH FIXES", 1) if fixes else ("GO", 0))
    print(f"\nVERDICT: {verdict}")
    for title, items in (("STOP — fix before upload", stops), ("FIX", fixes), ("NOTE", notes)):
        if items:
            print(f"\n{title}")
            for k, x in enumerate(items, 1):
                print(f"  {k}. {x}")

    if a.out and problems:
        with open(a.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(headers) + ["problems"])
            w.writeheader()
            for i in sorted(problems):
                w.writerow({**rows[i], "problems": "; ".join(problems[i])})
        print(f"\nRows with problems: {len(problems)} → {a.out}")
    return code


if __name__ == "__main__":
    sys.exit(main())
