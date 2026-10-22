# Business House Matrix — Marketing Research Engine Protected Rollout

**Date:** 2026-10-22 (IST)  
**Source:** [Approved handover](../handoffs/MARKETING_RESEARCH_ENGINE_EXPANSION_2026-10-22.md)  
**Repository:** `aarondash5-star/business-house-matrix`  
**Implementation branch (unmerged):** `feat/marketing-research-engine-20261022`  
**Change boundary:** Dell isolated owner-scoped development directory and Mac isolated GSC adapter stage. **No live Marketing Brain replacement, no active transport/interface update, no new active timer, no production or staging website writes, no publishing or spending, no root/identity/permission changes.**

## Gate scorecard

| Gate | Implemented | Evidence | Certification |
|---|---|---|---|
| 0 — baseline and protected rollout | Yes | Paired Dell/Mac online; Mac research 1.1 and signed search verified; 17/17 Mac quality tests; Dell user services verified | **PASS (live baseline)** |
| 1 — guarded extraction | Yes on Dell private CLI | HTTPS exact-domain grants, all DNS addresses publicly routable, TCP pinned to checked IPs, TLS hostname validation, per-hop redirect checks, fail-closed robots/crawl-delay, atomic per-host reservations, 512 KB HTML bound, maximum three redirects, no login, public fetches successful on W3C and Moksha, short evidence/canonical/digest/timestamp | **PASS (isolated extraction), NOT ACTIVE in Mac relay** |
| 2 — entity and claim verification | Yes as deterministic guard | Own brand/third-party listing/directory distinct; provider candidates not automatically competitors; typed source-attributed price, currency, unit, timestamp, freshness and explicit conflict rules; independent corroboration + reviewer needed for verified | **PASS (code contract), live verified competitor facts pending** |
| 3 — private research memory | Yes on Dell isolated DB | SQLite + FTS5, versioned tables, source→entity relationships, claim history, review queue, duplicate canonical handling, digest-change classification, 30-day crawl-attempt/180-day history cleanup, no guest data | **PASS (isolated pilot), interdepartment retrieval pending** |
| 4 — monitoring / GSC / Trends | Partially | Owner-reviewed target-only digest monitor, no automatic notification or active schedule. Separate Mac five-dimension GSC importer passed 11 synthetic/offline tests; original query-only adapter untouched. Trends news/CSV separation retained | **PARTIAL; schedule and live dimension data NOT CERTIFIED** |
| 5 — Marketing→Design and final benchmark | Partially | Research packet contract contains market map, first-party identity, unverified leads, UX references, price/GSC/Trends unknowns and explicit human-review gates; 12 representative **offline** query categories tested conservatively | **PARTIAL; 10-query evidence benchmark and reviewed market claims NOT CERTIFIED** |

**Important:** Passing a schema/unit test is not proof of accurate competitor prices, geographic competitor identity, current opening hours, buyer demand, or website conversion.

## Live host baseline and smoke results

- **Dell bridge**: paired/online; all three SSH lanes fresh. Services are `systemctl --user` units **`bhm-searxng`** and **`bhm-research-relay`**, running throughout. A system-level `systemctl` check initially reported them inactive because it addressed the wrong service manager. No remediation was required.
- **Mac bridge**: paired/online; live `unified_research.py` **v1.1.0**, signed encrypted SearXNG relay enabled, paid fallback disabled, 100/day cap. Public search smoke: verified paired relay, **5** results, paid fallback false. Mac GSC state: **99** property-specific query observations in **2** batches, last import 2026-10-22 03:10:46 UTC, no new OAuth; Trends **30 national RSS observations**, **0 genuine historical index points**.
- Dell initial homepage extraction: unavailable `OSError` because an IPv6 address preceded reachable IPv4. Hardened pinning now **prefers validated IPv4 and retries only pre-resolved publicly routable endpoints** (never re-resolves during connect). Re-test on `https://mokshagoa.com/`: succeeded, `first_party_own_brand`, source SHA-256 digest and canonical URL stored privately, no facts auto-verified. W3C `https://www.w3.org/WAI/fundamentals/accessibility-intro/` also successfully extracted, source hash and metadata recorded privately; correctly unverified.
- Data is retained in **Dell owner-scoped** `$HOME/bhm-research-expansion-20261022/private-evidence*.sqlite3`, not GitHub. Source text is not stored in public repo.
- Mac isolated GSC adapter: `$HOME/bhm-gsc-multidim-stage-20261022/`. It expects an *already approved* engagement-core read-only five-dimension report (`query,page,country,device,date`), Pacific-date scoped; it **does not fetch Google data itself, request OAuth, or alter `gsc_metrics.py`**.
- Trafilatura **2.3.1**, Apache-2.0, installed in Dell `.venv`; full observed dependency version lock in [requirements-research-engine.lock.txt](../../marketing/requirements-research-engine.lock.txt). License metadata for transitive dependencies checked locally (Apache-2.0, BSD, MIT, MPL, dual open-source alternatives). No paid package/API.
- Resource baseline: Dell roughly 7.5 GiB RAM / 5.4 GiB available, Mac 7.7 GiB RAM / 6.2 GiB available, moderate Dell thermal readings; no workload/resource cap or root settings were changed.

## Terminal receipts and test results

| Test | Host | Receipt | Exit | Result |
|---|---|---|---:|---|
| Host identity / resource baseline | Mac | `5b7c8195-a887-472f-9b3e-fd9660c55086` | 0 | PASS |
| Host identity / resource baseline | Dell | `f5bbb914-e96f-41cb-8ad3-d819d8b82478` | 0 | PASS |
| Dell user-unit service health | Dell | `373969e2-dd95-4d2a-925e-2d0ecbe2133f` | 0 | PASS |
| Existing research quality suite | Mac | `cb8a70ec-c325-40f6-a0b7-6053bff3ee69` | 0 | **17/17** |
| Signed paired search smoke | Mac | `b79c9b0c-972e-47ff-a151-a1803e7353db` | 0 | 5 public search results, peer=true |
| Open-source package license audit | Dell | `5eba5896-dad5-49c7-819f-cdb80b55f8f7` | 0 | PASS |
| First successful W3C page extraction | Dell | `fca09164-0529-491a-a833-263a97329126` | 0 | PASS |
| Successful Moksha extraction after guarded IP fix | Dell | `8baba9a7-bb58-4073-a53f-e4f85a343a8f` | 0 | PASS |
| Claim/entity regression suite | Dell | `1aa5a5ef-9b61-48b0-b789-f928a10dcc09` | 0 | **20/20** |
| Combined earlier extraction/claims/monitor tests | Dell | `e2344a32-c097-4828-a89f-ce7f03a65873` | 0 | **61/61** |
| Final guarded extraction/entity/monitor suite | Dell | `68915b63-5d9f-48ae-9d9c-5b7276f618ed` | 0 | **63/63** |
| Multi-dimension GSC adapter suite | Mac | `c253ffb2-da76-4b32-884d-6cc9638f8b93` | 0 | **11/11** |
| Empty verified-target monitor dry-run | Dell | `7d81eaec-f9e4-4cd1-90f2-03eaf58a05fc` | 0 | PASS: no fetch, no alerts |

**91 passing latest baseline/regression tests** = Dell 63 + Mac research 17 + Mac GSC 11; prior intermediate test suites are not added again.

**Existing, separate legacy issue:** `test_unified_research.py` on active Mac yielded 11 passes/1 failure because an older fixture expects `observed` for irrelevant results that the newer quality gate correctly classifies `insufficient_evidence`. No production research filter was weakened to satisfy a stale expectation. Repair this fixture in a separate reviewed change, then run all active Mac tests.

## Rollback

1. **No live rollback is necessary:** no Mac active research module, signed relay, service, host root policy, SearchXNG service, site staging, checkout, PMS, tracking or ads state was changed.
2. Isolated Dell code and private evidence: `$HOME/bhm-research-expansion-20261022/`; previous-file rollback copies include `research_engine.py.pre-fts-fix-20261022`, `.pre-ip-fallback-20261022`, `.pre-entity-link-20261022`, `.pre-atomic-rate-20261022`. Protect private DB; do not publish or delete audit history without owner review.
3. Isolated Mac GSC adapter `$HOME/bhm-gsc-multidim-stage-20261022/`. Current production GSC query adapter unchanged.
4. GitHub implementation is **feature-branch only**. Do not merge until remaining live authorization/security/quality gates pass.

## Remaining mandatory release gates / takeover

1. **Signed transport extension:** design and threat-review a typed, signed and encrypted `extract_granted_url` operation for Mac→Dell using the current paired identity and per-request receipts; deny unrestricted URLs and shell to model. Smoke-test relay before enabling; preserve the present `search` operation and rollback. The existing `searxng_research.extract(url)` still intentionally raises.
2. **Provider verification:** build at least two source-supported, owner-reviewed Arambol/Goa competitor identities and compare prices against actual first-party menus, recorded with dates and units. Do not infer competitors from reseller listings. No automatic claim promotion.
3. **Monitoring:** owner-review each explicit competitor URL/domain and robots policy before enabling a respectful timer. Current target manifest is **empty**. Meaningful changes should enter human review; never alert on unverified price or currency/time noise.
4. **GSC dimensional data:** obtain one authorized first-party report with `query,page,country,device,date` via the existing engagement-core read-only route. Validate paging/date windows/Pacific labels, then test actual deltas. No parallel Google OAuth.
5. **Gate 5 live certification:** define before running thresholds: topical precision at least 80% in manually labeled 10-query sample; 100% critical factual claims have dated direct first-party evidence and independent source/reviewer; 100% approved claims cited, 0 fabricated figures, 0 unauthorized network/domain/PII exposure, 0 production writes; capture processing latency, citation completeness, freshness and memory. Re-run Russian separately. Keep Design inputs blocked pending manual review.
6. **No deploy/merge/publish/spend** until these remaining gates have verified evidence. The current research packet is a *conservative development artifact*, not a production marketing recommendation.

## Artifacts

- [Guarded extractor, SQLite and packet CLI](../../marketing/research_engine.py)
- [Entity, claim, conflict, provenance checks](../../marketing/research_entities.py)
- [Approved-target change monitor](../../marketing/research_monitor.py)
- [Read-only five-dimension GSC adapter](../../marketing/gsc_multidim.py)
- [63 Dell regression tests](../../marketing/test_research_engine.py), [entity tests](../../marketing/test_research_entities.py), [monitor tests](../../marketing/test_research_monitor.py)
- [11 Mac GSC tests](../../marketing/test_gsc_multidim.py)
