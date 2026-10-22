# Marketing Brain Research Quality Gate — Certification 2026-10-22

## Scope and verdict

**PASS** for read-only, relevance-filtered research discovery and site-scoped GSC/Trends evidence separation. **NOT YET VERIFIED** for factual competitor claims, prices, review quality, or conversion-performance conclusions. Owner approval remains required for business copy or site changes.

- Project: independent Business House Matrix / Mac Marketing Brain
- User: requested to fix research first, before the Moksha website redesign
- Hosts: `mac-linux` (Marketing) and paired `dell-linux` SearXNG transport, unchanged
- Production impact: **none**. No spend, publishing, advertising, customer information or WordPress writes.

## Root-cause audit

1. The previous `unified_research.collect` submitted one huge mixed query combining geography, wellness service terms, pricing, UX, SEO, mobile design and the year. It accepted the first search results verbatim.
2. A verified October 21 failed-quality receipt `7951f864-ba06-41ce-9260-7d15579b5257` included an unrelated 1939 Billboard PDF, skin-lightening article, GitHub dictionary script and broad keyword pages.
3. The first receipt `49b32b3c-3c57-4ca1-b35e-686df61ec7f4` incorrectly treated the **year 2026** in a Suzlon Energy headline as a Google Trends topic match.
4. Search Console matching also allowed general words such as `and` or `goa` alone; results are site-specific query rows, **not** site totals or global search volume.
5. The first post-fix live smoke test uncovered the GSC adapter's pre-existing maximum `limit=10` contract; corrected from `limit=25`. No GSC adapter limits or credentials were changed.
6. The first successful filtered receipt `0e4efd8d-6e23-4ede-98e3-39efbfa72d25` was too strict on SearXNG engine names, rejecting otherwise relevant results; engine names are now kept as *untrusted attribution metadata* rather than a fixed allowlist.

## New code, rollback and reuse

- [Research evidence-quality rules](../../marketing/research_quality.py) — project-aware focused query planner; category-specific evidence filter; normalized HTTPS links, deduplication, untrusted-engine metadata, own-brand classification, UX inspiration distinction, filtered GSC query matches, Trends query without meaningless years.
- [Unified research aggregator](../../marketing/unified_research.v1.1.py) — applies the quality gate to results from the **existing** signed encrypted Mac↔Dell relay, records all attempted queries and rejection reasons, separates Trends and GSC evidence, refuses unsupported promotional claims, and fails closed when no evidence.
- [Regression suite](../../marketing/test_research_quality.py) — **17/17 offline tests passed** on live Mac. Tests cover previously irrelevant sources, own-brand vs unverified market leads, malformed/unsafe URLs, GSC row-bound integration, broad-year trend pollution, source duplicates, forged signed-transport metadata, unapproved private input and UX/inspiration metadata.
- Live Mac paths: `/opt/business-house-matrix/marketing/brain/research_quality.py`, `unified_research.py`, staged test copies in `research-quality-stage-20261022/`.
- Rollback backups: `unified_research.py.pre-quality-gate-20261022`, `unified_research.py.pre-bounded-gsc-20261022`, `research_quality.py.pre-engine-fix-20261022`.
- **No change** to underlying `searxng_research.py`, secure private transport, trends CSV store, GSC permissions, public query quotas (100/day, 3/min), model settings, machine service or Mac resource/thermal guards.

## Final autonomous worker QA

- **Live job** `c34d92af-16cd-430b-9a64-0af4da1185b8`, idempotency `moksha-research-v11-allengines-cert-20261022`
- **State** `completed` / **attempt** 1 / **error** none / evidence-version `1.1.0`
- 3 bounded queries: `Arambol Goa sauna ice bath wellness services`, `Goa sauna ice bath mud bath wellness booking prices`, `spa wellness mobile booking website user experience`.
- **15 candidate hits**, **11 relevant unique sources**, **4 rejected** (duplicates, off-target location, off-topic UX).
- Category splits: **5 local service leads**, **2 local pricing leads**, **4 general UX references**; each hit carries `evidence_class`, `verified_facts=false` and URL.
- Representative leads: official Moksha site (own brand), Burraa own-brand listing, TripAdvisor local wellness index, Agoda-area spa benchmark (outside Arambol scope), general spa UX design references. **None are verified competitor identities or independently verified prices.**
- Correct Google Trends outcome: `no_relevant_observation` for cached IN national news; no spurious 2026 headline match.
- GSC: `observed`, Moksha property only, settled `2026-09-21`–`2026-10-19` date-window, top-limited query rows. Never sum these rows to site-level totals or infer booking conversions.
- Mac Brain remains `publish_enabled=false`, `spend_enabled=false`.

## Limitations and next research gate

Research results are **discovery leads**, not verified fact sheets. Before incorporating names, competitive prices or claims into final website content, validate individual provider identity, actual geographic relevance (Arambol/North Goa versus South Goa), current service menus and live pricing on primary sources. Missing evidence must remain **unknown**, not modeled or invented. There is no automatic full-page extraction because arbitrary URL extraction remains intentionally disabled. Existing Marketing Brain `hosted_draft` previously produced a truncated 433-character creative output; **creative output and research-to-staging synthesis remain separate blockers** and were not represented as resolved in this gate.

References for the search behavior: https://docs.searxng.org/dev/search_api.html (search query and category parameters); https://developers.google.com/webmaster-tools/v1/searchanalytics/query (dimension-aggregated top-limited results).
