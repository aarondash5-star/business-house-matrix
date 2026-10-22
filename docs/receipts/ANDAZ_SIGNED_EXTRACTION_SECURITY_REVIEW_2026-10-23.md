# Business House Matrix — Andaz signed extraction security review and continued QA
**Date:** 2026-10-23 IST. **Branch:** `main` for this receipt; staged research implementation remains in open, unmerged PR #4 (`feat/marketing-research-engine-20261022`).
**Result:** **REVIEWED DESIGN, NOT AUTHORIZED OR LIVE-CERTIFIED.** No signed extraction capability or source scope was activated or expanded.

## Source of truth and scope
- [Andaz main handover](../handoffs/MARKETING_BRAIN_ANDAZ_FINAL_HANDOVER_2026-10-23.md); [previous Andaz QA](ANDAZ_COMPETITOR_PRICING_QA_2026-10-23.md); [staged extractor rollout (PR #4 branch)](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/docs/receipts/MARKETING_RESEARCH_ENGINE_PROTECTED_ROLLOUT_2026-10-22.md).
- Existing Mac/Dell owner-scoped Generic SSH lanes; no root/identity/permission changes, new scheduled jobs, paid services, production modifications, publishing, spend, merge, or authenticated OTA/browser activity.
- Static review of `marketing/research_transport_ops.py`, `research_transport_patch.py`, `research_engine.py`, `research_entities.py` on PR #4, plus live read-only host service, QA and heartbeat receipts. Private reports, source text, secrets, identities and booking/PMS data not committed.

## Deployment and health verified in this continuation
- Mac and Dell authenticated, paired, online, three lanes present at approximately 2026-10-22 19:29 UTC.
- Mac existing `/opt/business-house-matrix/marketing/brain/`: original `bhm-marketing-queue-worker.timer` **active**; queue has **35 completed** tasks, latest prior Andaz job `3d8d43b3-0047-4602-9037-24e1ad25fbc0`. `publish_enabled=false`, `spend_enabled=false`. LangGraph v2 appended marker present once.
- Mac isolated Supervisor regression **7/7 PASS**, exit 0. SSH receipt `800f7f3e-2f77-4fd4-bc49-9ec72da39cb5`.
- Mac isolated GSC adapter regression **11/11 PASS**, exit 0. SSH receipt `3260b4db-944f-4f95-8875-1b83eada4f87`. This certifies adapter tests only, **NOT** property-authorized Andaz GSC or full five-dimensional real data.
- Legacy Mac `test_unified_research`: **11/12 passed**, one known failure in `test_no_gsc_is_explicit_missing_not_zero_demand`. Its test expects `observed`, while the live strict classifier returns `insufficient_evidence`. Caller shell exited 0 because it explicitly captured the test exit; **test suite itself exited 1**. SSH receipt `4b47c01d-e871-47cc-8ba6-22698cee7e9f`. **Do not weaken the evidence classifier**; update the stale fixture in a separately reviewed code change.
- Dell existing user units `bhm-searxng`, `bhm-research-relay`, `bhm-marketing-research-api`, `bhm-autonomy-controller` all **active**; local API `127.0.0.1:18890/health` v1.3.0 `ready`, `bind=loopback`, `manual_review_required=true`, `no_external_publish=true`. SSH receipt `26b36aa9-10dc-42cd-a34d-5fc28c1ca3c9`, exit 0.
- Dell isolated 63-test security regression **was re-queued** as `79f89375-b28c-44a4-bed2-de8649651812`. At review cutoff it was `running/stale_running=true` with no terminal exit. **Outcome unknown; do not replay automatically, do not count as a new pass.** Previous independent dated 22 Oct receipts asserted 63/63, but that is historical, not re-certified here.

## Gate 1: Static security review — existing strengths
1. Exact-page grant code currently permits **only** `https://mokshagoa.com/` and `https://www.w3.org/WAI/fundamentals/accessibility-intro/`; Andaz/OTA pages are not granted.
2. Staged extractor rejects non-HTTPS or non-granted hosts, credentials, IP literals, nonpublic DNS records, unvetted redirect targets and unexpected content types. Connection pins to validated IP, uses TLS hostname verification. Robots failures deny crawling, per-host cooldown is atomic, body limited to 512 KB, redirects bounded, page text marked untrusted and `needs_review` by default.
3. Transport proposal retains existing signed/encrypted device-paired identity and old search operation, proposes distinct versioned `extract_granted_url` operation and exact page check at both ends; only bounded excerpt returned, with no automatic publishing or trusted facts.
4. **Crucial release reality:** transport patch is not deployed. Earlier Mac patch attempt was denied by safety controls; no authorized Mac→Dell signed page-extraction terminal receipt exists. Do not retry via alternative backdoor, broaden page grants or activate the transport during this task.

## Open security and proof gaps — block release
| ID | Finding / requirement | Severity | Decision |
|---|---|---|---|
| SEC-01 | No approved exact Andaz/competitor source grants; staged `PAGES` only Moksha/W3C | BLOCKING | No Andaz extraction |
| SEC-02 | Typed signed Mac→Dell extraction not active or end-to-end certified; prior Mac staging blocked | BLOCKING | No activation, no bypass |
| SEC-03 | `research_entities.certify_claim()` accepts free-form `reviewer` text and caller-supplied corroborating URLs. This alone **does not authenticate a reviewer** or prove the corroborating URLs were independently fetched. | HIGH | Do not connect automated claim promotion; require separate trusted reviewer identity and persisted source receipts before certification |
| SEC-04 | Generic `displayed_price` claim has a 7-day freshness window and lacks booking date, nights, guest/bed count, AC, refund, fees, tax, payment and live inventory fields. Dynamic hotel quotes cannot be certified with that schema. | HIGH | Add explicitly reviewed OTA stay-quote evidence schema in isolated development; require exact-date checkout proof |
| SEC-05 | First-party room descriptions and marketplace snippets may reflect different or duplicate properties (especially Dreamcatcher unrelated to Arambol and multiple 12 Monks identities). | HIGH | Human-reviewed canonical entity/source registry before promotion |
| SEC-06 | No verified person-labeled ten-case benchmark; previous query execution and keyword checks are not human-certified precision. | RELEASE | 10+ independently labeled topics and >=80% precision, plus negative/disambiguation controls |
| SEC-07 | No owner-approved exact competitor monitor targets/robots review; neither Andaz property GSC authorization nor 5D live distribution verified. | RELEASE | Keep monitor disabled and demand unknown |
| SEC-08 | Mac legacy regression known 1/12 fail; Dell new security-suite receipt stale/unknown. | QA | Preserve historical receipts, require fresh terminal exits |

## Competitor evidence: useful leads but no false certification
Public candidate URLs discovered earlier by existing Dell signed search / operator analysis, **NOT extraction allowlist additions**:
- Happy Panda Hostel — `https://www.happypandahostel.com/` (first-party).
- The Peace Hostel Arambol — `https://thepeacehostel.in/` (first-party).
- Dreamcatcher House & Hostel Arambol — `https://www.hostelworld.com/hostels/p/322685/dreamcatcher-house-and-hostel-arambol/` (OTA).
- Travo Tales Goa — `https://www.hostelworld.com/hostels/p/336542/travo-tales-goa/` (OTA).
- 12 Monks Backpacker Resort — `https://www.hostelworld.com/hostels/p/333140/12-monks-backpacker-resort/` (OTA; keep separated from Beachfront).
- Kumbaya Beachside Hostel & Apartments — `https://www.hostelworld.com/hostels/p/333961/kumbaya-beachside-hostel-and-apartments/` (OTA).
The full six are **analyst-level leads**; autonomous Mac Brain still has only two named candidate competitors and **zero independently verified facts**. Andaz own Goibibo alias does not count as a competitor.

## Price normalization gate (NOT passed)
- The next *proposed* comparison fixture is **2026-11-06 to 2026-11-07** (one night). Keep dorm one adult/one bed and private two adults/one room in **separate categories**, with exact AC, inclusions, cancellation, final INR amount, tax/fee split, payment rules, observation timestamp, inventory/checkout proof, cited URL, source identity and conflict.
- No future-date checkout was initiated in this continuation; **0/5** certifiable competitor final-checkout prices, no price-based recommendation or auto-publish.
- Past Hostelworld `From` EUR listings and Andaz own cached Goibibo offers are nonstandardized *displayed leads*, never normalized competitor checkout rates.

## Remaining owner and operational review
- Owner must approve canonical Andaz public identity, room attributes, live base tariff and policy/inclusions, contact/booking links, pool, cafe/kitchen status and owner 1 PM/11 AM vs OTA 2 PM/noon discrepancy. Do not update any listing yet.
- GSC: previously proven real read-only data are linked to **Moksha**, not Andaz; no Andaz property-specific GSC or inquiry-to-booking evidence claimed.
- Cold-boot, soak, 429 handling, signed extraction retry/recovery, reviewer audit identities and 10-case human-labeled benchmark remain outstanding. Do not run disruptive reboots or change timers under this authorization.
- Original PR #4 remains open/draft and Issue #5 open. No merge or issue closure.

## Recommended release sequence (requires separate security authorization, NOT completed)
1. Approve exact, non-sensitive Andaz and competitor URLs, purpose, robots/rate review, with role-separated signed extraction permissions. Confirm repository/host patch fingerprints and rollback.
2. Fix SEC-03 reviewer authentication and SEC-04 dated OTA schema **in isolated code**; add negative and positive tests; pass offline security suite before any live operation.
3. Obtain explicit separate owner/security approval to activate the pre-reviewed typed signed extract on Mac→Dell; run a single bounded end-to-end proof, including denied URL/redirect/replay and no source-to-fact privilege promotion. Do not bypass connector safety denial.
4. Independently verify three named local active competitors, five genuinely comparable INR checkout totals on the same date, ten human-labeled cases >=80%, fresh source citations and contradictions with human sign-off.
5. Then run GSC/seasonality tests with Andaz-authorized data, review release readiness and Design/Dev handoff. Public publishing remains separately denied.

**Final classification:** infrastructure healthy; isolated security *design reviewed*; Mac supervisor/GSC regressions pass; **extraction NOT authorized or activated, autonomous claim/pricing QA NOT certified**. Preserve all working systems and protections.
