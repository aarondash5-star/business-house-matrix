# Business House Matrix — Move Marketing Research Engine to Mac (migration handover)

**Requested:** 2026-10-23 IST, after Stage B deployment remained platform-security-blocked.
**Scope:** Move the local Marketing research core (evidence extraction library, SQLite/FTS5 knowledge, deterministic source/claim review and research packets) to **Mac as primary**; preserve Dell as a tested fallback. Do not conflate the research engine with the entire Business House Matrix.
**Actual status:** **PARTIALLY IMPLEMENTED IN UNMERGED DEVELOPMENT SOURCE ONLY. NOT INSTALLED ON MAC, NOT CUT OVER, NOT STAGE B CERTIFIED.**

## Current runtime (confirmed via previous receipts and latest heartbeat)
- Mac `mac-linux`: paired/online; hosts Marketing Brain Supervisor v2, `unified_research.py` v1.1 and signed encrypted Mac→Dell query/search client; existing Mac GSC read-only adapter.
- Dell `dell-linux`: paired/online; existing `bhm-searxng`, `bhm-research-relay`, `bhm-marketing-research-api`, `bhm-autonomy-controller` services; guarded extraction, `research_engine.py`, entity QA, read-only market packets; private owner-scoped SQLite/FTS5 evidence DB.
- Signed private Supabase relay `bhm-research-relay` already verifies Mac and Dell device public-key identities. Existing Mac-side fixed `linux_probe` was denied upstream by OpenAI safety checks before queuing a task. **Host heartbeat is not host execution clearance**.
- Dell research private DB is **not in GitHub**. Do not fetch it through model-accessible channels or import guest/PMS personal data.

## Prepared migration source (existing draft PR #4 branch)
- [`marketing/research_mac_local.py`](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/marketing/research_mac_local.py) is a **Mac-local, strictly offline/read-only** frontend to existing `research_engine.packet()`. Fixed topics `moksha_arambol` and `andaz_arambol`; fixed private DB path under `~/.local/share/bhm-research/evidence.sqlite3`; SQLite opened read-only/immutable with integrity check; no URL, shell, service mutator, authentication keys, auto-scheduled crawl, publication or spending input. Missing/symlinked snapshot fails closed, not silently initialized.
- [`marketing/test_research_mac_local.py`](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/marketing/test_research_mac_local.py) declares **10 offline tests**: no implicit DB creation, empty/missing/symlinked snapshot rejection, invariant nonpublication, Mac-local FTS packet read, correct Andaz brand constraints, invalid topics, fingerprint integrity, fixed module list and rejected URL input. **Test source committed; no live Mac or fresh terminal CI receipt claimed**.
- Reuse existing `marketing/research_engine.py`, `research_entities.py`, `research_monitor.py`, `andaz_stagea_evidence.py` and provenance tests. The guarded extractor is Python stdlib + pinned OSI-open-source Trafilatura dependency and can be ported in an isolated Mac virtual environment after authorization. Current CLI's default public grant list is **not** authority for Stage B competitor extraction.
- Unchanged `marketing/research_api.py` has Dell-specific `SEARCH=/var/lib/generic-linux-automator-exec/matrix-searxng/local_search.py` and `marketing/research_ddg.py` hardcodes Dell local SearXNG at port 18889, Dell Node binary and isolated Opera path. They must be **reviewed and ported with a Mac-local service first**; do not point Mac to Dell-local absolute paths or silently broaden network access. `marketing/research_market_bridge.py` assumes Dell is packet provider and will need a gated preference/fallback update after Mac tests.
- Production `marketing/marketing_supervisor_langgraph.py`, `marketing/unified_research.v1.1.py`, signed search transport, Supabase gateway and Dell services are not modified by this staging.

## Exact controlled cutover gates
1. **Authorize Mac connector action:** resolve platform safety denial through approved connector/security process. The previously blocked Mac arbitrary shell preflight *and fixed `linux_probe`* must not be retried through alternate Supabase SQL/queue/browser/SSH methods. Security [Issue #14](https://github.com/aarondash5-star/business-house-matrix/issues/14) tracks this.
2. **Mac runtime preflight:** via a newly approved fixed-function collector only, verify nonroot ownership, local Python runtime and interpreter dependencies, local disk/RAM/thermals, current Marketing Brain units, ports, backup permissions, exact file fingerprints and rollback state. No root changes or new unreviewed network services.
3. **Isolated files on Mac:** deploy a pinned Git commit of research engine/entities/monitor and new adapter into a Mac *separate* staging worktree/venv. Verify all source SHA256 hashes. Run unit/negative/SSRF, anti-secret, signature, SQLite/FTS5 and API compatibility tests **on Mac** with receipts and exit codes. No live switch.
4. **Private SQLite transfer:** prepare a consistent owner-scoped SQLite backup from Dell using SQLite backup API (not an unsafe raw `*.sqlite3` copy while WAL may be active), encrypt the snapshot over the already approved authenticated transfer/storage facility, copy only research sources/claims/review queue (no guest/customer/booking data). Validate SHA256, DB `quick_check`, expected schema, FTS search, row counts and owner permissions on Mac. Do not put private DB into GitHub or public storage. Preserve original Dell DB untouched as rollback.
5. **Search backend:** either establish **Mac-local SearXNG** with a reviewed, approved resource-limited deployment and exactly the existing search rules, or keep Dell signed search relay as an explicit **fallback/search backend** during phase 1. No paid providers, CAPTCHA bypass, arbitrary browser scraping or uncontrolled web access. No existing operator session modifications.
6. **Evidence policy:** verify robots/terms for each exact permitted target before Mac extraction; two Stage B candidate homepages remain **NOT CLEARED**. Require human/source signing reviewer identities and exact-source registry. Run public extraction only on independently approved sites with SSRF, IP pinning, TLS, redirects, body-size, cooldown and negative control checks. No authenticated hotel booking.
7. **Mac → Brain integration:** once verified, change supervisor local research routing behind a kill-switch default OFF. Run ≥10 manually scored representative queries, ≥80% topical precision, cross-origin source checks, zero unapproved facts/price claims; compare Mac/Dell outputs and latency. Keep reviewers and publication disabled. Roll back immediately on QA or thermal failure.
8. **Production cutover:** authorized owner approves a versioned enablement and rollback with host SHA receipt, existing services unchanged until sign-off. Mark Mac primary only when matching end-to-end receipts, signatures, approved sources and failback test exist. Keep Dell read-only fallback and original DB for owner-specified retention; do not disable Dell or remove permissions.
9. **Stage B:** does **not** automatically pass simply because Mac becomes primary. The two exact sites' permissions, signed source/reviewer, and live negative security gates must independently pass.

## Suggested future read-only smoke commands (execute ONLY through an approved Mac tool)
- `python -m unittest test_research_mac_local test_research_engine test_research_entities test_research_monitor` from isolated, locked staging directory.
- `python research_mac_local.py status` — emits no secret-bearing content and does not create DB.
- `python research_mac_local.py packet --topic andaz_arambol` — local FTS5 snapshot only, never a verified price report.
- Explicit database snapshot `PRAGMA quick_check`, source digest comparison, and 5-minute thermal/load observation through the approved fixed collector.

## Rollback
- Before activation: no rollback required; staged Git source may remain for review, Mac and Dell unchanged.
- After any approved cutover: disable the new Mac-local flag/service, route signed search back to existing Dell provider, preserve all original Mac Supervisor and Dell services, retain evidence snapshots/audit receipts. Restore only from owner-confirmed signed backup, not overwrite the source DB in place.
- Never change root/sudo/SSH keys, OAuth, pairing, Supabase service-role secrets or global website permissions as part of this migration.

## Measured gate status
| Check | Result |
|---|---|
| Business House Matrix source/host architecture inspected | YES |
| Mac and Dell current heartbeats | ONLINE/PAIRED |
| Mac-local read-only packet adapter | SOURCE STAGED (feature branch only) |
| Mac-local adapter tests | 10 DECLARED; NOT RUN ON MAC |
| Dell guarded extraction/evidence code and prior QA | EXISTS, historic Dell 63/63 |
| Mac-local SearXNG / source extraction | NOT DEPLOYED |
| Dell private evidence DB copied | NOT DONE |
| Owner/platform connector host execution clearance | NOT GRANTED |
| Mac primary switch | NOT DONE |
| Stage B final source and reviewer QA | BLOCKED |
| Production/root/permissions/publishing/spend changes | NONE |

**Outcome:** Migration design and Mac-local adapter are prepared. Production migration and Stage B cannot be truthfully certified under the current explicit Mac security denial. Preserve the working Dell environment and original signed search integrations.
