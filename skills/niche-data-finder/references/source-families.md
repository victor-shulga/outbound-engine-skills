# Source families

Ten families of account-level sources. For each: what it lists, the signal it usually carries,
where to look, how it is typically extracted, and the trap that wastes the most time. Named sources
are examples to check, not endorsements; verify access and terms before using any of them.

---

## 1. Associations and member directories

- **Lists**: firms that pay to belong to a trade or professional body.
- **Signal**: fit and seriousness (they pay dues, often meet entry criteria). Timing only if the
  directory shows "new members" or join dates.
- **Where**: `"member directory"` / `"find a member"` / `"find a firm"` on the sector's national and
  regional associations. Examples: engineering-firm associations (e.g. ACEC member firms in the US),
  chartered-practice directories for architects (e.g. RIBA in the UK), chambers of commerce sector
  lists, agency networks.
- **Extraction**: paginated HTML or a map widget backed by a JSON endpoint (check the browser's
  network tab); sometimes a members-only PDF.
- **Trap**: directories of individuals, not firms. Check that entries are companies with websites.

## 2. Licence and certification registries

- **Lists**: firms holding a licence, permit to practise, or certificate.
- **Signal**: fit (mandatory for the work) plus timing when issue or renewal dates are public. A newly
  issued firm licence in a new state often means geographic expansion.
- **Where**: state or national licensing boards (engineering firm licences, contractor licences),
  certification search tools (ISO certificate databases such as IAF CertSearch, sector schemes),
  supplier pre-qualification schemes, public trust pages for security standards.
- **Extraction**: search forms with one query per region or letter; some boards publish full CSV
  downloads.
- **Trap**: registries that list every holder since 1990. Filter on status = active and on issue date.

## 3. Public tenders and procurement portals

- **Lists**: buyers publishing work and, in award notices, the suppliers who won it.
- **Signal**: strong timing. A firm that just **won** a contract has new work and a capacity gap,
  which suits outsourcing and subcontracting offers. A buyer that just **published** a tender is
  buying now.
- **Where**: TED (EU), Find a Tender and Contracts Finder (UK), SAM.gov contract opportunities and
  award data (US), Prozorro (Ukraine), regional and municipal portals. Search by CPV, NAICS or
  UNSPSC codes plus keywords.
- **Extraction**: most national portals have an API or bulk export; regional portals are HTML.
- **Trap**: award notices name the legal entity, not the website. Budget a domain-matching step.

## 4. Event exhibitor, sponsor and speaker lists

- **Lists**: companies that paid for a booth or sponsorship, or sent a speaker, at the sector's
  main events.
- **Signal**: budget this year and focus on that market; good for a pre-event or post-event angle.
- **Where**: "exhibitor list" / "floor plan" / "sponsors" pages of the two or three biggest annual
  events in the niche; past editions are often still online.
- **Extraction**: HTML lists, event apps with JSON endpoints, downloadable PDF floor plans.
- **Trap**: lists vanish after the event. Capture them when found and record the event date.

## 5. Marketplaces and review directories

- **Lists**: providers listed by service line, or buyers posting work.
- **Signal**: for providers, review dates and new service lines show activity; for buyer-side
  marketplaces, a posted project means a company is looking for outside help right now.
- **Where**: agency and services directories (e.g. Clutch, with service focus and dated reviews),
  freelance marketplaces where clients post projects (e.g. Upwork), software review sites for
  product categories, partner directories of platforms (CRM, e-commerce, website builders, cloud
  providers) that list certified agencies.
- **Extraction**: HTML with filters; partner directories often have hidden JSON APIs.
- **Trap**: anti-bot protection and terms that forbid scraping on some marketplaces. If extraction
  is blocked, use them for manual research on a short list only.

## 6. Job boards and ATS feeds

- **Lists**: companies with open roles.
- **Signal**: strong and dated. Hiring for the function the offer covers (or a role that creates the
  need) is one of the most reliable public timing signals.
- **Where**: public ATS job boards (Greenhouse, Lever, Ashby, Workable and similar expose per-company
  boards and often JSON), aggregators, niche job boards of the sector, company careers pages.
- **Extraction**: ATS JSON endpoints, scrapers or Apify actors for aggregators. The
  `account-sourcing` skill (if installed) runs this family end to end.
- **Trap**: a large share of results are recruiters, agencies, universities and public bodies. Filter
  them out before scoring.

## 7. Permits and planning databases (AEC and anything tied to physical projects)

- **Lists**: building permits and planning applications, with applicant, owner, architect, engineer
  or contractor names, project value and dates.
- **Signal**: the strongest timing signal in AEC. A filed permit or approved application means design
  and construction work is about to start; the named firms are the accounts.
- **Where**: city and county open-data portals (many US cities publish permits as open datasets),
  local planning authority portals (UK), national statistics for volumes, paid aggregators for full
  coverage (e.g. Dodge Construction Network in the US, Barbour ABI or Glenigan in the UK).
- **Extraction**: open-data APIs (often Socrata or ArcGIS) for cities that publish; HTML search per
  authority otherwise.
- **Trap**: coverage is city by city, never national, and date fields are messy (text dates,
  placeholder years). Check the newest real record before trusting a sort.

## 8. Tech-stack lookups

- **Lists**: websites or stores using a given technology.
- **Signal**: fit (they run the platform you serve) and timing when first-seen / last-seen dates are
  available (adoption or migration).
- **Where**: BuiltWith, Wappalyzer, store-specific lookups for e-commerce platforms, integration
  marketplaces, public "customers" pages of the tool vendor.
- **Extraction**: paid exports or APIs; free tiers allow lookups one domain at a time.
- **Trap**: detection works on front-end technology only. Back-office tools (ERP, BIM software,
  internal CRMs) rarely show up; use job posts that mention the tool instead.

## 9. Company registries and filings

- **Lists**: legally registered companies with industry codes, addresses, officers, filing dates.
- **Signal**: new incorporations, new subsidiaries in a country (expansion), officer changes, filed
  accounts that show growth.
- **Where**: national company registries (e.g. Companies House in the UK with SIC codes and a free
  API, EU business registers, US state registries), securities filings for public companies.
- **Extraction**: APIs or bulk downloads in several countries.
- **Trap**: industry codes are self-declared and broad. Use them as a base layer combined with a
  sharper source.

## 10. Funding, awards and growth lists

- **Lists**: companies that raised money, won grants, or ranked on growth lists.
- **Signal**: budget and pressure to scale; time-bound (a round is fresh for a few months).
- **Where**: funding databases and news feeds, public grant registers (national innovation agencies,
  EU research funding portals), annual fast-growth rankings by country or sector.
- **Extraction**: news feeds and RSS, grant registers with exports, ranking pages in HTML.
- **Trap**: rankings are annual and quickly stale; grants are listed under the legal name. Freshness
  usually scores 2-3 here.

---

## Quick map: where to start by target market

| Target accounts | Try first | Timing layer |
|---|---|---|
| Agencies (marketing, web, dev) | platform partner directories, services directories | job boards, buyer-side marketplaces |
| AEC firms (architects, engineers, contractors) | licence boards, associations | permits and planning data, tender award notices |
| SaaS and software companies | tech-stack lookups, review sites by category | ATS job boards, funding news |
| Manufacturers and industrial | registries by industry code, certification databases | trade-show exhibitor lists, tenders |
| Public-sector suppliers | supplier registries, pre-qualification schemes | tender publications and award notices |

The map is a starting point. Always run Step 2 of the skill for the specific niche; the best source
for a narrow segment is often a single directory nobody else uses.
