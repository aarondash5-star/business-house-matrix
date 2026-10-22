# Andaz Marketing Brain — competitor, pricing and autonomy QA
**Run date:** 2026-10-23 IST (host receipts dated 2026-10-22 UTC)
**Repository:** aarondash5-star/business-house-matrix (main)
**Disposition:** FAIL-CLOSED / PARTIALLY COMPLETE — worker operational, public competitor candidates independently discoverable, **Brain fact certification and five comparable live prices NOT ACHIEVED**.

## Source of truth, scope, provenance
- [23 Oct full handover](../handoffs/MARKETING_BRAIN_ANDAZ_FINAL_HANDOVER_2026-10-23.md), [22 Oct reliability QA](MARKETING_ANDAZ_RESEARCH_RELIABILITY_QA_2026-10-22.md), [Andaz owner/Goibibo reference](ANDAZ_OWNER_GOIBIBO_MARKETING_BRAIN_2026-10-22.md), and [public market baseline](../reports/ANDAZ_ARAMBOL_PUBLIC_MARKET_EVIDENCE_2026-10-22.md).
- **Two evidence channels kept separate:** (A) actual Mac LangGraph autonomous job through existing signed Mac–Dell search; (B) analyst/operator-assisted read-only public page checks and a Dell direct SearXNG diagnostic. Channel B **must not be represented as independently source/claim-verified by the Brain**.
- No guest/PMS data, private raw reports, API secrets, authenticated OTA session data, or owner tariff inventory exported. No new services, tokens, permissions, root, publication, spend, merge or production modifications.

## Verified deployed health / regressions
- Both existing authenticated worker heartbeats ONLINE, PAIRED, all three lanes present at 2026-10-22 18:42 UTC.
- Mac live v2 orchestrator marker `# BHM_LANGGRAPH_SUPERVISOR_V2_20261022` count **1**. Isolated `.venv-supervisor/bin/python -m unittest test_marketing_supervisor_langgraph -q`: **7 passed / 7, exit 0**, SSH development receipt `5f8a6191-4c3d-43ca-aced-ebb005e76e9f`.
- Mac original `bhm-marketing-queue-worker.timer` ACTIVE. `brain.py status --verbose`: completed count **34 before**, **35 after** this run; `publish_enabled=false`, `spend_enabled=false`. Read-only terminal receipts `742d903e-ef38-402b-afd4-e87a3b6fbee5`, `652123e2-1ce3-4e5f-b02e-50bc82965daa` (exit 0).
- Dell `bhm-searxng`, `bhm-research-relay`, `bhm-marketing-research-api`, `bhm-autonomy-controller` each ACTIVE (both control and operations lanes, exit 0); loopback API `http://127.0.0.1:18890/health` returned `{"version":"1.3.0","status":"ready","bind":"loopback","no_external_publish":true,"manual_review_required":true}`. Terminal receipts `59f97963-ca46-4d8f-aacb-a173264bd781`, `6292cf9c-137e-404a-a0a6-be734a6ac6d6`.

## Actual new autonomous Brain task
- Enqueued **once** through original queue, no direct model invocation: `python3 brain.py enqueue research_report --payload '{"business":"andaz_arambol"}' --key andaz-competitor-price-qa-20261023-v1`.
- Task UUID `3d8d43b3-0047-4602-9037-24e1ad25fbc0`; queue and terminal receipt verified `4faa8f2a-c58c-4ca4-ba26-0fbf6d0415b5` (exit 0).
- **Completed**, first attempt, **58.965 seconds**, 2026-10-22 18:46:56 UTC; exact `mode=brain_owned_langgraph_supervisor_v2`; 2 rounds, 3 queries, 13 URL/source leads, 10 domains, 3 live observed queries; fixed OSS planner with model ideation enabled.
- Protected Mac private report remains at `/opt/business-house-matrix/marketing/brain/reports/private/andaz_arambol-supervisor-report.{md,json}` (do NOT commit raw private artifact).
- Safe machine-checked private JSON fields: `qa_passed=true` (schema/safety), `quality_gate.source_lead_sufficiency_pass=false`, `quality_gate.distinct_competitor_names_observed=2` (Dreamcatcher House & Hostel; Travo Tales Goa), `quality_gate.sources_verified=0`, `quality_gate.independent_claims_verified=0`, `quality_gate.contains_verified_prices=false`, `pricing_analysis.prices=[]`, `approved_for_customer_facing_use=false`, `publish_allowed=false`, `spend_allowed=false`; `state=INSUFFICIENT_EVIDENCE`. **Do not call this an autonomous market-fact or pricing PASS.**

## Dell 10-case bounded topical/source discovery diagnostic (NOT human-scored)
- Tested the existing Dell local SearXNG `127.0.0.1:18889/search`; fixed 10 authored public-search topics, 3 top results inspected per request, serial pacing, no configuration or quota changes. Receipt `159446b6-b592-44a5-a051-5f16bded25d7` (exit 0).
- At an intentionally short **8-second per-query** deadline: **5/10 nonempty responses**, **5/10 timeout** (queries 4,5,6,7,9). An immediate transport exception under this test deadline is **not proof of an engine outage**.
- Bounded **one retry only** for those 5 topics at 18-second deadline and 1.8-second pacing, receipt `960eea31-8bf2-4a1a-9dc8-507ff6aded24` (exit 0): **5/5 yielded search results**; overall 10/10 topics eventually returned results in these two passes. Initial latency/timeouts remain a performance QA issue.
- Top-1 result of the Golden, BC Dreamcatcher disambiguation query was unrelated 12 Monks; its *second* result matched Golden. This negative control establishes at least one top-rank topical failure even after successful transport. A qualitative assistant review suggests 9/10 top-1 matches the authored subjects; **this is not the mandated 10-case independent human-labeled precision certification**. The 80% human score gate remains open.
- Exact useful public lead URLs from Dell: [Happy Panda first party](https://www.happypandahostel.com/), [Dreamcatcher Arambol](https://www.hostelworld.com/hostels/p/322685/dreamcatcher-house-and-hostel-arambol/), [Travo Tales](https://www.hostelworld.com/hostels/p/336542/travo-tales-goa/), [12 Monks Backpacker Resort](https://www.hostelworld.com/hostels/p/333140/12-monks-backpacker-resort/), [Kumbaya Beachside](https://www.hostelworld.com/hostels/p/333961/kumbaya-beachside-hostel-and-apartments/), [The Peace first party](https://thepeacehostel.in/).
- Never merge `12 Monks Backpacker Resort`, `12 Monks Beachfront Hostel` and `12 Monks Hostel Arambol Goa` without separate identity matching. [dreamcatcherhostel.com](https://dreamcatcherhostel.com/) concerns Golden, BC, **not** Arambol. Andaz aliases all resolve to owner property and **cannot be counted as competitors**.

## Operator-assisted public identity/amenity cross-check (outside Brain certification)
These pages were directly checked as independently identifiable Arambol accommodation leads, **not** final available inventory nor on-site physical inspection:
| Distinct Arambol business | Current checked evidence | Attribute evident on source | Remaining caveat |
|---|---|---|---|
| Happy Panda Hostel | [First-party home](https://www.happypandahostel.com/) | Arambol hostel; community proposition; Wi-Fi, bar, lockers | No date-specific checkout or physical check |
| Dreamcatcher House & Hostel | [Hostelworld property](https://www.hostelworld.com/hostels/p/322685/dreamcatcher-house-and-hostel-arambol/) | Arambol rooms/dorms; cafe/work area, rooftop bar, events | OTA-hosted descriptions; taxes listed separately |
| Travo Tales Goa | [Hostelworld property](https://www.hostelworld.com/hostels/p/336542/travo-tales-goa/) | Arambol dorms, rooms, food/bar/pool table | OTA description; no live rate |
| 12 Monks Backpacker Resort | [Hostelworld property](https://www.hostelworld.com/hostels/p/333140/12-monks-backpacker-resort/) | Arambol dorms/private apartment offerings, pool | Distinguish similar 12 Monks properties |
| Kumbaya Beachside Hostel & Apartments | [Hostelworld property](https://www.hostelworld.com/hostels/p/333961/kumbaya-beachside-hostel-and-apartments/) | Beachside dorms/private/studio products | OTA source; price not normalized |
| The Peace Hostel Arambol | [First-party home](https://thepeacehostel.in/) | Arambol backpacker hostel, Wi-Fi, food/bar listed | No date-specific checkout; claims first-party |

This improves the **analyst-side competitor discovery shortlist (6 distinct leads)** but does **not** change autonomous Brain `distinct_competitor_names_observed=2` or `independent_claims_verified=0`.

## Pricing test and fail-closed result
- Prior [public market baseline](../reports/ANDAZ_ARAMBOL_PUBLIC_MARKET_EVIDENCE_2026-10-22.md) has **five Hostelworld EUR 'From' leads**. A later snapshot of the same category showed changed advertised figures; [Hostelworld Arambol](https://www.hostelworld.com/hostels/asia/india/arambol/). These are unnormalized promotional displays, not INR payable quotes or same-date confirmed availability.
- Separate [Andaz Goibibo](https://www.goibibo.com/hotels/andaz-arambol-artist-party-hostel-hotel-in-goa-3479076370619624886/) shows **Andaz's own** dynamic promotions, **not independent competitor rates**; labels and owner check-in/out conflict require reconciliation. No private tariff feed extracted.
- **0 / >=5 valid equivalent competitor final-checkout prices**: no single fixed *future* check-in/out across all suppliers with one bed vs room occupancy, AC, taxes, fees, cancellation/payment terms, effective currency, live inventory, timestamp, source corroboration. Suggested comparison fixture for a later explicitly authorized run: **2026-11-06 check-in / 2026-11-07 check-out**, dorm *one adult/one bed* separately from private *two adults/one room*. Fixture is **not** a verified reservation result.
- Existing signed SEARCH authority **does not authorize** activating dormant signed third-party page extraction, authenticated booking or browser navigation, paid APIs, rate-limit bypass, or new permissions. This was respected. An evidence failure cannot be converted into a PASS through URL counts or price snippets.

## Certification gate summary
- [x] Connected Mac + Dell live, active existing services/queue, no publication/spend flags.
- [x] Mac v2 bridge checked; 7/7 isolated tests passed.
- [x] Fresh idempotent unattended Brain report reached terminal receipt; safety QA passed; evidence threshold enforced.
- [x] Ten Dell public queries executed with five latency retries, all eventual transport results; no settings changed.
- [x] At least three independent Arambol **operator-side candidate identities** cross-referenced to direct public URLs.
- [ ] **Brain autonomous 3+ competitor source-to-claim certification** (still 2 lead names, zero verified claims).
- [ ] **Five comparable actual bookable competitor prices** (0/5).
- [ ] **Independent human-labeled ten-case accuracy benchmark** and 80% threshold (not certified).
- [ ] Security-reviewed **narrow signed extraction authorization**, with no permission increase in this run.
- [ ] Owner review of Andaz policies, amenities, inventory/rates, property-specific GSC + conversion facts; resilient 429/cold-boot/soak; editorial review.

## Handover and unchanged release gates
- [Draft PR #4](https://github.com/aarondash5-star/business-house-matrix/pull/4) verified **OPEN / DRAFT**, unmerged.
- [Issue #5](https://github.com/aarondash5-star/business-house-matrix/issues/5) verified **OPEN**, not closed.
- Preserve Mac v2 appended bridge; Dell loopback signed transport, quota/security gates and prior rollback copies.
- **Next:** obtain narrow security-approved public source-to-claim extraction route (NOT approved or activated here); run single-date five-property checkout verification through authorized supplier flows, record exact receipt/provenance and reviewer sign-off, rerun Brain job and separate labelled QA. No publication/spend/permission changes performed.

**Final verdict:** Research infrastructure LIVE and regression-stable; public shortlist useful; **full autonomous verified competitor/pricing report remains blocked for evidence/scope reasons.**
