# Marketing Research API and DuckDuckGo/Opera Integration — Live Release Receipt

**Date:** 2026-10-22 (IST)  
**Repository:** `aarondash5-star/business-house-matrix`  
**Implementation branch:** `feat/marketing-research-engine-20261022`  
**PR:** [#4](https://github.com/aarondash5-star/business-house-matrix/pull/4) — branch remains in DRAFT pending all evidence/release criteria  
**Blocking issue:** [#5](https://github.com/aarondash5-star/business-house-matrix/issues/5)

## Executive result

**Working live and tested:** Dell loopback Research API v1.3, Mac Marketing Brain `research_market` queued task, signed Ed25519/sealed-box paired relay v2 for that task, existing relay v1 search backward compatibility, SearXNG DuckDuckGo public search, optional isolated-Opera fallback, explicit source identity, SQLite FTS5 memory, normalized reader-visible content fingerprint, conservative source-attributed research packet.

**Not approved:** unreviewed competitor facts/prices; full five-dimensional GSC import; scheduled third-party competitor monitoring; autonomous publishing, advertising spend or checkout changes. No unrestricted browser operator capability granted.

## Live endpoints and access

- Dell new **user systemd service**: `bhm-marketing-research-api.service` active, enabled, `127.0.0.1:18890` loopback **only**, no public or LAN listener. `GET /health`, `GET /v1/packet/moksha_arambol`, `POST /v1/run` with exact approved topic and explicit source selector `searxng|duckduckgo`, no arbitrary URL or shell action.
- Mac Brain queue: `python3 /opt/business-house-matrix/marketing/brain/brain.py enqueue research_market --payload '{"topic":"moksha_arambol","source_engine":"duckduckgo"}'`, run with existing worker. `brain.py` remains `publish_enabled=false`, `spend_enabled=false`.
- Existing paired relay: Dell owner-scoped `matrix-research-transport/transport.py` extended with sealed `v=2,op=research_market,topic=moksha_arambol,source_engine=duckduckgo|searxng,limit=5`; signed receipts required, fixed Dell-local API target; legacy v1 signed search preserved. Mac transport itself **not modified**; standalone `research_market_bridge.py` reuses its existing keys/crypto.
- Opera: existing Dell Opera CDP browser at local port 9231 reused only by a fresh **ephemeral isolated context**. Existing credentialed operator tabs/profiles are untouched. Browser queries use ordinary public DuckDuckGo and reject cross-site navigation. No CAPTCHA solving, evasion, credentials, uploads, purchasing or authenticated session access. User requested Opera specifically; **Opera is proprietary and an explicit user-directed exception to the Matrix's otherwise OSI-only software requirement**. The core SearXNG, Trafilatura, SQLite, Playwright adapter remain OSS.
- Automatic decision: prefer DDG through SearXNG; when its results explicitly indicate a CAPTCHA, try the isolated Opera public browser once. If challenge remains, mark unavailable and do not bypass. No paid search fallback. Operational limits intentionally remain despite request for unrestricted browser access.

## Real-use smoke receipts

| Receipt | Host | Outcome |
|---|---|---|
| `838252f4-dfce-4b3b-a9d3-9d3ea6d25c0c` | Dell | Guarded real Hidden Oak pricing extraction + evidence record |
| `633c3871-9bff-4a3d-8ad7-d2b555cbff8f` | Dell | Guarded real GoAsian pricing extraction |
| `406cc901-a842-4f77-9de6-b898546d1cd7` | Dell | Guarded real Satori booking-page extraction |
| `9d79271c-667d-439e-b0fa-765b64b4e8cf` | Dell | Existing Opera isolated browser: 5 DDG public result URLs, no CAPTCHA, existing sessions untouched |
| `035465c5-f1dd-455c-8622-ae95e75dbc6a` | Dell | Simulated SearXNG CAPTCHA to exercise **real Opera fallback**, 5 public DDG results, fallback=true (simulation only for upstream trigger) |
| `ace6de3c-5ae0-4e72-ae35-32e9ac880fe1` | Dell | New DDG+API 15/15 tests |
| `7e5f82d0-6ba0-49a7-8e6a-1e0c5c830e75` | Dell | Full updated local 83/83 regressions PASS |
| `4922c433-aecf-47c4-af01-edf61bc33da6` | Dell | Live API source refresh 5/5 success, 3 unverified provider leads |
| `30ec07c7-e35e-4212-bb32-7bf2ec50452d` | Dell | Signed v2 exact-match patch with backup; all three research services active |
| `a983ead9-30e6-4afa-bb54-7bcc85746ab8` | Mac | Signed encrypted v2 request successfully returned 5 evidence sources, 3 candidate providers |
| `5297022f-6f2b-4676-8d5e-bd23a58e655f` | Mac | Brain task registry patch and unsafe-payload rejection PASS |
| `27a61b6d-caa3-4f38-bb6d-a1a8d6299a24` | Mac | **Normal Brain queue**: `research_market` completed on first attempt (15.568 s), job `d0d30d26-dc6c-430b-a5bf-62d21928c3f4`, signed source report |
| `a95505d0-1c22-4fc0-b7f1-f1f7f6ad0987` | Mac | Legacy signed v1 SearXNG search backward compatible: 5 results, peer verified |
| `9521a5e0-9f27-4289-8658-d68d72988a14` | Dell | Restart-ready health probe HTTP 200, all three research user services active |
| `e098fa24-47b0-4321-b01-edf61bc33da6` | Dell | **Two** real five-page refresh rounds after normalized-content fingerprint switch: first migrates digests; second returns **5/5 unchanged**, preventing spurious dynamic-HTML change alerts |

### Observed bugs and fixes

1. Initial systemd active state preceded bound HTTP socket: adopted bounded readiness polling, live second probe returned HTTP 200; process memory approx 11 MB at idle.
2. DuckDuckGo SearXNG sometimes CAPTCHA-blocked or returned unavailable. Added a **separate uncredentialed Opera context**; direct browser and simulated challenge-to-real-Opera tests PASS. Browser neither solves CAPTCHAs nor accesses existing login sessions. Actual operator exposure is not widened.
3. SearXNG named-provider and broad searches sometimes rank first-party Moksha marketing/reseller posts over other providers. Exact first-party evidence registry compensates for discovery gaps, but do **not** count it as a passed ten-query public SERP relevance benchmark.
4. Facebook/Instagram promotional posts were incorrectly tagged provider candidates. Updated entity classifier: social and own-brand promotional listings are **never** automatically verified competitors. Three additional regression tests passed.
5. Raw HTML digests produced false changes from volatile script markup. New normalized reader-visible text digest, two specific regressions and live second-pass 5/5 unchanged. First post-migration digest run is expected to classify content_changed_unverified once.
6. The linked Google Search Console's read-only bridge allows at most **3 dimensions**, not five; 12 authentic query/page/date records previously ingested privately, 99 prior query rows retained. Country and device remain UNKNOWN, not fabricated. Do not pay or request broader OAuth without approval.

### Release gates and restrictions

- Gate 0 baseline **PASS**. Gate 1 Dell page extraction **PASS**, and **signed Mac→Dell market API v2 route PASS**; arbitrary Mac extraction URLs remain unavailable by design.
- Gate 2 entity/claim code **PASS**, current competitor facts **manual review**. Gate 3 SQLite/FTS5 local research memory **PASS** (read-only packet available through signed route).
- Gate 4 no autonomous competitor monitoring schedule without individually owner-reviewed approved targets; GSC 5D unavailable via present no-cost read-only connector; Trends RSS not historical index.
- Gate 5 Mac normal queue/real research packet generation **PASS**. **Editorial fact verification / broad live 10-query precision benchmark NOT certified**. The packet intentionally says `verified_competitors=[]`, `price_claims_approved=false`, `ready_for_design_copy=false`.
- No production website publishing, social posting, purchases, campaign spending, booking/PMS modification, root/identity change or credential export.

### Verified rollback

1. **Disable new API only:** `systemctl --user disable --now bhm-marketing-research-api.service` on Dell.
2. **Restore signed worker v1:** Dell `python3 $HOME/bhm-research-expansion-20261022/research_worker_v2_patch.py --rollback`, then `systemctl --user restart bhm-research-relay.service`. Preserve existing `bhm-searxng`.
3. **Restore original Mac Brain:** `python3 /opt/business-house-matrix/marketing/brain/brain_market_task_patch.py --rollback`; the separate standalone Mac market client can remain inert.
4. Optional Dell data-module rollback copies in the working directory: `research_engine.py.pre-visible-fingerprint-20261022` and `research_entities.py.pre-social-classifier-20261022`. Never drop private SQLite source evidence without independent explicit approval.
5. After rollback, verify old Mac `searxng_research.search` signed v1 and Dell user-service health.

## Still open to full production quality certification

- Resolve direct provider-price conflicts with independent sources and a human reviewer (Hidden Oak with/without ice, Satori operating status).
- Approve individual monitoring URLs and rate policies before enabling unattended watches/alerts.
- Find authorized no-cost five-dimensional GSC source, or retain the honest 3D capability limitation.
- Score at least ten live **human-labeled** research queries for topical precision and source coverage; reject generic/social/off-topic competitors.
- Independently sign off reviewed market facts before handing them to private Design staging. No automatic publication.
