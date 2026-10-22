# Marketing Brain — Andaz research reliability and QA receipt (22 October 2026)

**Project:** Independent Business House Matrix (Andaz used only as a public-research pilot)
**Scope:** Existing Mac LangGraph supervisor + original queue timer + Dell authenticated signed research relay, no publishing, spend, credential/root changes or expanded permissions.
**Disposition:** Research reliability improved; **complete autonomously fact-verified competitor and comparable-price report NOT CERTIFIED**. Public source-checked human-assisted market baseline exists separately. No claims or live prices should be automatically published.

## Source of truth
- Starting [LIVE handover](../handoffs/MARKETING_SUPERBRAIN_LIVE_HANDOVER_2026-10-22.md).
- Public operator-assisted cited [Andaz Market Evidence & Strategy](../reports/ANDAZ_ARAMBOL_PUBLIC_MARKET_EVIDENCE_2026-10-22.md). This must NOT be passed off as the Brain's independently fact-verified output.
- Existing internal Mac private report at `/opt/business-house-matrix/marketing/brain/reports/private/andaz_arambol-supervisor-report.md` and adjacent JSON. Do not upload private raw artifact.
- Issue [#5](https://github.com/aarondash5-star/business-house-matrix/issues/5) remains OPEN; research expansion PR [#4](https://github.com/aarondash5-star/business-house-matrix/pull/4) remains OPEN/DRAFT, not merged.

## Verified Mac and Dell state
- Both authenticated SSH workers ONLINE and fresh in control, operations and development lanes at entry.
- Dell units: `bhm-searxng`, `bhm-research-relay`, `bhm-marketing-research-api`, `bhm-autonomy-controller` all `active`, terminal service check exit 0.
- Dell local Research API loopback `http://127.0.0.1:18890/health`: `{"version":"1.3.0","status":"ready","bind":"loopback","no_external_publish":true,"manual_review_required":true}`.
- SearXNG is Podman-bound at **127.0.0.1:18889**, not 8888; first 8888 diagnostic connection failure was a wrong-port probe, not evidence of failed SearXNG service. A direct true-port query returned 24 results. DuckDuckGo/Brave worked; SearXNG listed `google cse: Suspended: too many requests` on one request. No engine configuration was changed.
- Live Mac authenticated signed-and-encrypted Dell public research query for Happy Panda returned 5 results in **13.6 s**, mode `self_hosted_encrypted_paired_relay`, `device_peer_verified=true`.
- Mac Brain queue timer `bhm-marketing-queue-worker.timer` enabled/active, single max concurrent job; publishing and spending gates FALSE, no changes. Mac completed job count increased from 30 to 33 through this session.

## Research reliability investigation and live tests
- Mac search adapter existing `MAX_DAY=100`, `MAX_MINUTE=3`. Prior historical 21 usage attempts with recent two successful + one failed and several reserved rows; precise cause of older three job attempts not conclusively isolated. Existing retry was vulnerable to quota burst.
- Bounded **at-most-one quota-aware retry** added to supervisor after recognizing existing Mac quota; no quota expansion, remote permission change, anti-bot circumvention or new gateway. Model planner query specificity guard added; previous 6/6 regression passed after correcting one too-strict planner fixture.
- Dell 10 public search probes (local existing SearXNG interface) for generic Arambol market, Happy Panda, Dreamcatcher, Travo Tales, 12 Monks backpacker/beachfront, Kumbaya, Hosteller Mandrem, Andaz, generic amenities: **8/10 nonempty** and **8/10 title-keyword topical match**. This is an automated proxy, **NOT a human-labeled precision test**. Andaz and generic amenities returned 0. No captcha bypass.
- First post-reliability v2 LangGraph unattended Andaz job `207686c3-07d7-43c0-abe0-b882a8ac457e` completed in 29.507s on attempt one, two live queries, 10 unique URL leads, 8 domains, formal schema QA PASS, `REVIEW_REQUIRED`; 0 verified claims, 0 prices. Exposed that domain/URL count could represent the same single hostel repeatedly.
- Tightened critic to count **named competitor identities**, not directories or duplicate citations. For Andaz at least 3 named competitors must appear on independent leads alongside two working queries and the old source-diversity floor. Added structured `distinct_competitors` and `competitor_names` with explicit disclaimer these are **not fact verification**; seven offline supervisor regressions, including duplicate directory failure, **7/7 PASS** in actual isolated Mac runtime.
- Targeted default public queries for Dreamcatcher House and Travo Tales / Kumbaya / 12 Monks. Note: poor real results can still pass as URL evidence; they must not pass verified identity/price gates.

## Regression and repair trace
- Initial stricter planner (seven words) failed an existing planner fixture, automatically rolled back, adjusted to six and passed.
- Duplicate-business offline test initially used `.example` test URLs rejected by the URL cleaner; safely rolled back, corrected fixture to well-formed HTTPS domains and passed 7/7.
- Source sync of `marketing_report_orchestrator.py` inadvertently overwrote the live appended LangGraph v2 entrypoint with legacy v1. Live job `d292d00a-65ce-4bcf-8dd9-35a724094039` completed on v1 with 15 leads / 3 queries but **does not prove v2**. Detected via result `mission` vs exact v2 `mode` contract. Restored exact legacy-v2 bridge using pre-entity local reversible backup and applied targeted public-query changes. Live 7/7 tests PASS.
- Synced exact live restored Mac module back to GitHub `main`; preserve `# BHM_LANGGRAPH_SUPERVISOR_V2_20261022` marker and bridge on all future deployments. A simple raw GitHub orchestrator update must NEVER overwrite the live appended bridge.
- Relevant GitHub commits: supervisor `c26dc371669e18d01a2508e548dea2c4a7e60ea4`; test `361a1b353e4fde3e881e87aacba9826631f80a95`; restored live v2 orchestrator `86cf496cded9ee81928c78989293746af1928be4`. Mac rollback copies named `.pre-reliability-20261022` and `.pre-entity-qa-20261022` preserved.
- Final **verified v2.2** unattended job `3dafa1fd-50a6-485c-bcf5-456acb454522`: completed **18:00:19 UTC / 23:30:19 IST**, attempt 1, elapsed 48.964 s, exact mode `brain_owned_langgraph_supervisor_v2`, 2 rounds, 3 queries, 2 live queries, 10 distinct URL leads, 9 domains, **2 named candidate competitor identities** (`Dreamcatcher House & Hostel`, `Travo Tales Goa`). Supervisor critic `passed=false` → **`INSUFFICIENT_EVIDENCE`**; `qa_passed=true` (safety/schema QA ONLY); `sources_verified=0`, `independent_claims_verified=0`, `contains_verified_prices=false`, `approved_for_customer_facing_use=false`, `publish_allowed=false`, `spend_allowed=false`. This is correct fail-closed outcome, NOT completed trusted price research.

## Separate cited market baseline
The user-requested Andaz market strategy has been captured as a **public, internally reviewable operator-assisted evidence report** at [Andaz Market Evidence & Strategy](../reports/ANDAZ_ARAMBOL_PUBLIC_MARKET_EVIDENCE_2026-10-22.md). Named alternatives, listing discrepancies, market position, segments, SEO/booking channel hypotheses, priorities, and a QA table appear there with links. Advertised hostel dorm/private `from` rates are captured with explicit **date/occupancy/tax/cancellation verification failure** (single changing marketplace; not uniform future-date checkout, not independently corroborated). Do not equate those advertisements with verified payable rates. Distinguish report compiler from autonomous Brain worker.

## Release gates / remaining blockers
- [x] Mac and Dell authenticated live; Dell API/service health passes.
- [x] Existing signed research path real public query succeeds; timer runs unattended.
- [x] Bounded Mac quota-aware search handling implemented; no quota increase.
- [x] 10 real Dell topical probes executed; 8/10 automated signal (NOT human-labeled proof).
- [x] Duplicate citation vs named-business QA regression added; 7/7 offline unit tests pass.
- [x] V2 bridge regression caught, restored live, and synced to main.
- [x] Final first-attempt unattended v2.2 job produces fail-closed source-integrity verdict.
- [x] Public operator-assisted sourced market report and QA limitations committed.
- [ ] **Autonomous claim-to-source verification:** Security-reviewed allowlisted official-provider + relevant OTA source content extraction via existing signed Dell transport, structured claim/date/inclusion/provenance, fact conflicts, trusted independence and reviewer controls. Exact-topic v2 research API currently grants only Moksha; cannot assume Andaz extraction privileges or silently bypass the scope.
- [ ] **Competitor sufficiency:** At least 3 truly separate verified active Andaz-local comparable brands in actual Brain evidence, verify category/identity/amenities and not merely a name in an OTA snippet; 2 currently only named, 0 claims fact-verified.
- [ ] **Pricing:** For >=5 competitors capture equivalent *future dates*, occupancy/room class, AC, cancellation, fees and taxes, currency, timestamped final checkout prices from permitted sources. Independent corroboration / discrepancy log. No standardized bookable rates achieved.
- [ ] **Human-labeled relevance test:** >=10 labeled cases and >=80% topic relevance with authoritative named sources; current 8/10 keyword proxy does not satisfy.
- [ ] **Andaz owner confirmation:** Canonical listing, pool/amenities, room class, true Andaz booking URLs, official rate book and genuine imagery. Aggregated Google Hotels information conflicted; avoid public edits without approval.
- [ ] **Demand/measurement:** Actual Andaz GSC authorization and dimensions, local seasonality/booking conversion measured; current data insufficient. Marketing→Design→Dev→QA/EVOLUTION and creative production gates unchanged.
- [ ] **Resilience:** Full cold-boot/soak/rate-429 retry cert, separate security review for source retrieval and monitoring; keep draft PR #4 and issue #5 open.

## Next safe autonomous assignment
Through the **existing Mac Brain queue**, continue only with current allowlisted public-search capabilities. Replan to named official/OTA business sources with authored labels and evidence-classification failure handling; escalate missing URL extraction permission rather than granting yourself new capabilities. When a security-reviewed signed retrieval path is explicitly granted, run dated claim attribution and normalized pricing, then independent QA and human editorial approval. Do not merge PR #4, publish, spend, increase permissions, pull private guest data, or weaken evidence thresholds to force a PASS.
