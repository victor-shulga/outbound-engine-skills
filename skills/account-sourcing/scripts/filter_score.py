#!/usr/bin/env python3
"""
Filter, dedupe and score accounts pulled from an ATS job aggregator.

Input : one or more JSON files, each {"items": [ ...job rows... ]}
Output: CSV, one row per company, scored and tiered.

Expected fields on a job row (Apify fantastic-jobs shape):
  organization, title, date_posted, domain_derived, description_text,
  org_linkedin_headcount, org_linkedin_industry,
  org_linkedin_founded_date, org_linkedin_headquarters

Edit EXCLUDE_INDUSTRY / EXCLUDE_ORG / FOREIGN_HQ for your niche.
These lists are the part that ages — review them after every run.
"""

import argparse, csv, json, re, sys
from datetime import datetime, date

# --- niche-specific exclusions -------------------------------------------
# Industries with no own product, or buying cycles we do not serve.
EXCLUDE_INDUSTRY = [
    "IT Services", "Information Technology & Services", "Business Consulting",
    "Defense", "Higher Education", "Education Administration", "Non-profit",
    "Law Practice", "Professional Services", "Engineering Services",
    "Government", "Medical Practices", "Staffing", "Accounting",
]

# Named companies that keep surfacing and never convert.
# Start empty, grow it from real runs.
EXCLUDE_ORG = []

FOREIGN_HQ = ["England", "Singapore", "Toronto", "Vancouver", "Sweden",
              "Israel", "India", "Northern Ireland"]

CLEARANCE = re.compile(r"clearance|ts/sci|polygraph|\bdod\b", re.I)
PROBLEM_LANGUAGE = re.compile(
    r"\b(legacy|monolith\w*|technical debt|tech debt|re-?architect\w*|modernization)\b",
    re.I)

CORE_HEADCOUNT = (80, 450)
MAX_SCORE = 135
# -------------------------------------------------------------------------


def excluded(row):
    org = (row.get("organization") or "").lower()
    ind = row.get("org_linkedin_industry") or ""
    hq = row.get("org_linkedin_headquarters") or ""
    title = row.get("title") or ""
    founded = str(row.get("org_linkedin_founded_date") or "")

    if any(b.lower() in org for b in EXCLUDE_ORG):
        return "deny-list"
    if any(b in ind for b in EXCLUDE_INDUSTRY):
        return "industry"
    if CLEARANCE.search(title):
        return "clearance"
    if any(f in hq for f in FOREIGN_HQ):
        return "geo"
    if founded.isdigit() and int(founded) >= date.today().year - 2:
        return "too young"
    return None


def snippet(text):
    if not text:
        return ""
    m = PROBLEM_LANGUAGE.search(text)
    if not m:
        return ""
    around = re.search(r"[^.\n]*" + re.escape(m.group(0)) + r"[^.\n]*\.", text)
    if not around:
        return ""
    s = re.sub(r"\s+", " ", around.group(0)).strip()
    return s if 45 < len(s) < 260 else ""


def score(acc):
    s = 40
    capped = []
    if acc["snippet"]:
        s += 25
    s += min(30, 15 * (len(acc["roles"]) - 1))
    if acc["days"] >= 60:
        s += 20
    elif acc["days"] >= 30:
        s += 10
    hc = acc["headcount"] or 0
    if CORE_HEADCOUNT[0] <= hc <= CORE_HEADCOUNT[1]:
        s += 10
    elif not hc:
        capped.append("headcount")
    f = str(acc["founded"] or "")
    if f.isdigit() and int(f) <= date.today().year - 3:
        s += 10
    elif not f.isdigit():
        capped.append("founded")
    acc["capped"] = ",".join(capped)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+", help="JSON files with an items[] array")
    ap.add_argument("-o", "--out", default="accounts.csv")
    ap.add_argument("--today", default=date.today().isoformat())
    args = ap.parse_args()
    today = datetime.strptime(args.today, "%Y-%m-%d")

    accounts, dropped = {}, {}
    total = 0
    for path in args.inputs:
        for row in json.load(open(path, encoding="utf-8"))["items"]:
            total += 1
            why = excluded(row)
            if why:
                dropped[why] = dropped.get(why, 0) + 1
                continue
            key = (row.get("domain_derived") or row.get("organization") or "").lower()
            if not key:
                continue
            acc = accounts.setdefault(key, {
                "company": (row.get("organization") or "").strip(),
                "domain": row.get("domain_derived") or "",
                "headcount": row.get("org_linkedin_headcount"),
                "industry": row.get("org_linkedin_industry") or "",
                "founded": row.get("org_linkedin_founded_date") or "",
                "hq": row.get("org_linkedin_headquarters") or "",
                "roles": [], "snippet": "", "oldest": None, "capped": "",
            })
            t = (row.get("title") or "").strip()
            if t and t not in acc["roles"]:
                acc["roles"].append(t)
            d = (row.get("date_posted") or "")[:10]
            if d and (acc["oldest"] is None or d < acc["oldest"]):
                acc["oldest"] = d
            if not acc["snippet"]:
                acc["snippet"] = snippet(row.get("description_text"))

    rows = []
    for a in accounts.values():
        a["days"] = (today - datetime.strptime(a["oldest"], "%Y-%m-%d")).days if a["oldest"] else 0
        a["score"] = score(a)
        rows.append(a)
    rows.sort(key=lambda x: -x["score"])

    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "score", "max", "tier", "company", "domain", "headcount",
                    "industry", "founded", "hq", "open_roles", "days_open",
                    "target_role", "capped_fields", "proof_snippet"])
        for i, a in enumerate(rows, 1):
            tier = "A" if a["score"] >= 95 else ("B" if a["score"] >= 75 else "C")
            w.writerow([i, a["score"], MAX_SCORE, tier, a["company"], a["domain"],
                        a["headcount"], a["industry"], a["founded"], a["hq"],
                        len(a["roles"]), a["days"],
                        a["roles"][0][:60] if a["roles"] else "",
                        a["capped"], a["snippet"]])

    tiers = {"A": 0, "B": 0, "C": 0}
    for a in rows:
        tiers["A" if a["score"] >= 95 else ("B" if a["score"] >= 75 else "C")] += 1
    print(f"raw rows      : {total}")
    print(f"dropped       : {sum(dropped.values())}  {dropped}")
    print(f"accounts kept : {len(rows)}   tiers {tiers}")
    print(f"with quote    : {sum(1 for a in rows if a['snippet'])}")
    print(f"open 60+ days : {sum(1 for a in rows if a['days'] >= 60)}")
    print(f"written       : {args.out}")
    print("\nRead the proof_snippet column with your eyes before enrichment —"
          "\nroughly one quote in seven is a false positive.")


if __name__ == "__main__":
    sys.exit(main())
