# Marketing Superbrain — Complete Takeover Handover
**Date:** 22 October 2026 | **Timezone:** Asia/Kolkata  
**Repo:** https://github.com/aarondash5-star/business-house-matrix  
**Project:** Business House AI Matrix — independent from Moksha Master.  
**Live checkpoint:** Mac and Dell owner-scoped Generic SSH workers responsive; autonomous Mac Marketing Brain **v2 LangGraph research supervisor deployed**, but true end-to-end fully self-sufficient marketing and independently verified business reports **NOT YET CERTIFIED**.

> **This file is the primary next-chat handover.** Read this document before any deployment. Follow references for the complete source, historical chronology, tests, file paths, observed failures and rollback. Reuse working infrastructure; no rebuilding or duplicate queue workers.

## 1. Latest independently verified status

| Layer | Live observed result | Do not overclaim |
|---|---|---|
| Mac SSH worker | **Online**, all three lanes fresh at final 2026-10-22 17:10 UTC identity check | Reboot/long outage recovery not yet injected and certified |
| Dell SSH worker | **Online** during deployment, owner-scoped bridge available | Mac↔Dell direct LAN is **not** assumed routable |
| Mac Marketing Brain | Python `brain.py` 0.1.0, durable SQLite queue, **30 completed**, no queued jobs reported in final status | The number is job completion, not 30 quality-approved deliverables |
| Queue scheduling | `bhm-marketing-queue-worker.timer` **enabled+active**, original bounded single-instance `worker.sh`; systemd service last successful | No full host cold boot or multi-hour fault-injection soak |
| Supervisor v2 | `marketing_supervisor_langgraph.py`, LangGraph 1.2.16 and Pydantic 2.14.1, active via `research_report` registry and reversible bridge | First independent-report example yielded `INSUFFICIENT_EVIDENCE`; no verified market facts |
| Signed Mac→Dell SearXNG | Real signed research search **PASS**, five results, `device_peer_verified=true`, `mode=self_hosted_encrypted_paired_relay` | Upstream public search can fail or CAPTCHA; no bypass |
| Dell research services | `bhm-searxng`, `bhm-research-relay`, `bhm-marketing-research-api` **active**, Dell API health `ready` v1.3 | API/relay remain loopback/identity restricted; not arbitrary web/shell access |
| Isolated OSS package install | Mac `.venv-supervisor` installed, pinned, **`pip check` clean**, transitive package licenses audited | PyPI upstream initially timed out; mirror/lock recorded |
| Superbrain regression QA | **6/6** new offline tests passed plus successful real signed research smoke | Does not test every physical service outage or factual research quality |
| Social publication / spending | Mac `publish_enabled=false`, `spend_enabled=false` | No public write/post/spend permission granted |
| Andaz v2 | Real auto-executed `research_report`, private Markdown/JSON report, 3 queries / 2 rounds, 5 unique source leads | **Only 1/3 searches succeeded; 0 verified claims; not a customer-ready report** |
| Mac thermals | Observed 46°C before install, 65°C during checks, 50°C after Andaz run | Local creative inference and high-load autonomous video must remain thermally gated |
| Google Trends | Existing bounded official RSS + scheduled refresh, 40 prior observations | Historical/local search interest index unavailable; zero genuine historical points |
| Google Search Console | Read-only bounded data source; 99 existing Mac query observations, prior 12 actual 3D query/page/date rows via authorized route | `country`, `device` joint dimensions absent; no fabricated SEO metrics |
| Moksha website staging | Dell controller built 9 static private pages; prior Firefox mobile and desktop screenshot smoke | Real photography, full UX/brand/accessibility QA and private owner preview pending |
| Reel Studio | Preflight/review pipeline and thermal safeguard exist | Full genuine Mac finished autonomous video preview not certified |
| Central Matrix | Existing Dell autonomous controller and Dev sandbox routes; separate departmental implementations | Nine-department integrated superbrain/Open WebUI pilot and full EVOLUTION not certified |
| Research release PR | [Draft PR #4](https://github.com/aarondash5-star/business-house-matrix/pull/4) and [blockers Issue #5](https://github.com/aarondash5-star/business-house-matrix/issues/5) | Do not merge based solely on source passing tests |

## 2. Architecture — who owns what

```text
Business House AI Matrix (separate from Moksha Master)
    Marketing Brain on Mac
      Python brain.py + single existing SQLite queue + systemd user timer
      research_report business slug (andaz_arambol / moksha_arambol)
          → reversible marketing_report_orchestrator.py bridge
          → isolated Python 3.12 venv (.venv-supervisor)
          → LangGraph supervisor StateGraph
              PLAN      fixed business query + optional eligible hosted OSS LLM planning
              RESEARCH  original signed encrypted Mac↔Dell SearXNG relay
              CRITIC    Pydantic QA (diversity, source count, freshness caveats)
              REPLAN    at most one extra bounded research round
              COMPOSE   private source-cited draft + explicitly unverified hypotheses
              QA        required sections, source status, publish/spend=false
              STORE     owner-private 0600 JSON and Markdown report
    Dell workers
      SearXNG rootless service, research API v1.3, encrypted relay
      guarded Trafilatura public-page extraction, private SQLite/FTS5 memory
      controlled browser fallback, dedicated Dell Dev Brain, limited QA and staging
```

The supervisor owns bounded research workflow, not unrestricted system administration, service installation, ad purchases, new credential connections, third-party publication or automatic approval of weak evidence. **No second marketing queue/cron/daemon was created.**

## 3. Exact latest live Andaz mission receipt

- **Task:** `research_report` with `{"business":"andaz_arambol"}`
- **Idempotency:** `bhm-andaz-langgraph-supervisor-live-v2-20261022`
- **Job UUID:** `d12ad35f-adb5-4d4b-b417-aea13e31c1bd`
- **Final:** `completed`, attempt **3**, `error=null`, **27.532 seconds** on successful attempt, consumed automatically by Mac systemd queue timer.
- **Two previous failures:** missing `nacl` module inside new isolated venv; fixed with pinned PyNaCl/cffi; attempts happened before the timer was fully paused. Resume-safe retry succeeded without creating another independent queue or human `work-once` call.
- **Report JSON:** `/opt/business-house-matrix/marketing/brain/reports/private/andaz_arambol-supervisor-report.json`, **11,255 bytes**, **mode 0600**.
- **Report Markdown:** adjacent `andaz_arambol-supervisor-report.md`, **4,233 bytes**; private, not uploaded or disclosed in public GitHub.
- **Observed behavior:** model-assisted plan accepted through Pydantic schema; 3 bounded research queries / 2 rounds; 5 unique leads from 5 domains; only 1 research query yielded results; model-generated unverified brainstorming included.
- **QA:** graph stages, signed evidence contract, fail-closed no-publish/spend all passed; critic `low_source_diversity_or_missing_evidence`; final **`INSUFFICIENT_EVIDENCE`**, `independent_claims_verified=0`, `approved_for_customer_facing_use=false`.
- The previous v1 Andaz run `def570d8-8fef-40c5-acff-689ac797f779` returned 15 source leads and a private review draft. Do **not** discard or replace those leads; unifying fresh v2 research with prior deduplicated evidence is a next-step quality improvement, not a reason to rebuild SearXNG.

## 4. What was implemented, chronological (21–22 October)

1. Mac Marketing Brain: hosted OSS model router (prior Groq GPT-OSS/Qwen pilot), durable SQLite jobs, receipt storage, idempotency, rate limits and policy gates. Local heavy inference disabled after Mac thermal incident.
2. Dell research: rootless SearXNG, reusable search skill/contract, Tavily deprecated; Google Trends bounded official RSS and read-only GSC integration. Preserve false-demand and cross-property protections.
3. Encrypted signed Mac↔Dell private relay replacing failed overlapping-Wi-Fi direct LAN plan; v1 legacy public search certified, then narrowly scoped v2 market packets. No unsafe direct LAN gateway.
4. Dell guarded Trafilatura extraction, typed source identity/claim model, private source history + FTS5, reader-visible page fingerprints preventing dynamic HTML false alerts, 83/83 prior Dell regressions. Limited free/no-spend tools.
5. Explicit DuckDuckGo via SearXNG and isolated Opera public-search fallback only when allowed and not challenged. **Opera is proprietary and a user-requested narrow exception** to the independent Matrix OSI-only rule.
6. Dell private static Moksha site stage: 9 pages, 7/7 specific staging tests, mobile/desktop headless Firefox smoke, no production writes or owner-accessible remote preview yet.
7. Mac task quality: `unified_research.py` v1.1, 17/17 earlier quality tests, no price/social claim promotion. Old `research_brief` Andaz task `58b10808-367a-4899-aecc-6e5f76204480` **completed but delivered only 5 OTA/review snippets**, not a report.
8. Worker permanence: migrated only the Marketing Brain cron worker to **systemd user timer** (40 s after prior completion), preserved flock/retry/recovery, initial autonomous Moksha research test, restart/dedup checks. Other Trends cron preserved. Complete rollback in permanent-queue receipt.
9. `research_report` v1 Mac Brain-owned task introduced with exact business registry, signed Dell searches and private cited Markdown/JSON. Andaz task `def570d8-8fef-40c5-acff-689ac797f779` auto-completed, 15 source leads, review required.
10. LangGraph/Pydantic supervisor source, offline test suite and reversible bridge committed to main. Mac briefly became unreachable during *first* pip installation attempt; worker connectivity later returned without altering Wi-Fi/root.
11. Restored Mac heartbeat; installed OSS venv with **Alibaba PyPI mirror** after PyPI CDN timeouts downloading `zstandard`. All pinned dependencies and audited license identifiers are in `marketing/requirements-marketing-supervisor.lock.txt`.
12. Fixed missing crypto import `nacl` by installing `PyNaCl==1.5.0`, `cffi==2.1.1`, `pycparser==3.11` into isolated venv. Six offline graph tests, clean `pip check` and real signed relay search PASSED. No credentials replaced.
13. Activated reversible v2 bridge into existing Mac Brain and allowed existing timer to consume real Andaz task autonomously. Third attempt completed with safe report and honest `INSUFFICIENT_EVIDENCE`.
14. Last audit: Mac host online, 30 completed jobs, timer **enabled+active**, publish/spend false, isolated environment dependency integrity clean, private Andaz report exists. Dell had been online, services active; final resume should recheck health as usual.

## 5. Repository source and documentation (all key artifacts)

**Main branch working code:**
- `marketing/marketing_supervisor_langgraph.py` — supervisor v2 LangGraph nodes.
- `marketing/test_marketing_supervisor_langgraph.py` — 6 no-network graph tests.
- `marketing/marketing_supervisor_bridge_patch.py` — reversible in-place bridge with exact receipt/tenant checks.
- `marketing/requirements-marketing-supervisor.lock.txt` — actual freeze including PyNaCl.
- `marketing/marketing_report_orchestrator.py` — original v1 Brain-owned research report composer.
- `marketing/brain_report_task_patch.py` — earlier exact-match registration of `research_report`.
- `marketing/systemd/bhm-marketing-queue-worker.{service,timer}` — original durable Mac scheduling.
- `docs/receipts/MARKETING_SUPERBRAIN_LANGGRAPH_LIVE_2026-10-22.md` — **most recent live rollout, test, package and rollback receipt**.
- `docs/receipts/MARKETING_SUPERBRAIN_OSS_STAGED_2026-10-22.md` — historical staging blocker; **superseded** by live receipt.
- `docs/receipts/MARKETING_BRAIN_RESEARCH_OWNERSHIP_2026-10-22.md` — initial v1 Brain-owned report.
- `docs/receipts/MARKETING_AUTONOMOUS_QUEUE_PERMANENT_FIX_2026-10-22.md` — timer migration, receipts/rollback.
- `docs/handoffs/MARKETING_MATRIX_STATUS_HANDOVER_2026-10-22.md` — complete earlier checklist, historical source index.
- `docs/dev/PRIVATE_SITE_STAGING_2026-10-22.md` and `tasks/moksha-website-overhaul/STATUS_2026-10-22.md` — private website staging and QA limitations.
- [Draft research expansion PR #4](https://github.com/aarondash5-star/business-house-matrix/pull/4); [open blockers Issue #5](https://github.com/aarondash5-star/business-house-matrix/issues/5).
- The detailed live Dell Research API receipt remains in the draft PR branch at `docs/receipts/MARKETING_RESEARCH_API_LIVE_RELEASE_2026-10-22.md`. Do not assume everything in draft branch has been merged.

**Private runtime paths (never commit raw secrets/receipts/guest data to public repo):**
- Mac Brain: `/opt/business-house-matrix/marketing/brain/brain.py`
- Mac isolated supervisor: `/opt/business-house-matrix/marketing/brain/.venv-supervisor`
- Mac integration module: `/opt/business-house-matrix/marketing/brain/marketing_report_orchestrator.py`
- Mac report: `/opt/business-house-matrix/marketing/brain/reports/private/andaz_arambol-supervisor-report.{md,json}`
- Mac sqlite queue: `/opt/business-house-matrix/marketing/brain/data/queue.sqlite3`
- Mac user-service timer: `systemctl --user status bhm-marketing-queue-worker.timer`
- Dell research API: `127.0.0.1:18890/health` **from Dell only**, service `bhm-marketing-research-api`.
- Dell SearXNG: `127.0.0.1:18889` **Dell only**. Existing paired signed transport route is the correct Mac research path.

## 6. Strict remaining capabilities — prioritized checklist

### P0: From autonomous research *execution* to verified market intelligence
- [ ] Reuse v1 existing Andaz source leads and Dell SQLite memory in LangGraph to improve diversity without repeatedly hitting DDG.
- [ ] Make the Brain's critic track independent **actual competing properties**, not merely unique OTA pages/domains (several URLs may represent one business).
- [ ] Wire narrow authorized Dell guarded extraction/claim verification into source evidence with freshness, units, geolocation, and conflicting-price handling. Independent corroboration + human review before marking facts verified.
- [ ] Improve adaptive query planning and fallback under SearXNG upstream rate limits; avoid CAPTCHA evasion, unrestricted Opera logins, paid fallback and hallucinated results.
- [ ] Produce a genuinely substantial source-cited Andaz market report with current provider comparisons, position/pricing evidence, segments, SEO, distribution, opportunities and limitations; pass an evidence benchmark of at least 10 human-labeled queries.
- [ ] Repeat with Moksha under tenant isolation and approved source registry. No cross-property data, false GSC linkage or fabricated local Trends volume.
- [ ] Reconcile and review research expansion draft PR #4 and Issue #5 after source/CI/security quality gates; do **not** merge automatically.

### P1: Full Marketing Brain creative capability
- [ ] Connect reports → strategy → SEO/copy → Design → independent brand/fact/rights QA → controlled approved staging in one durable mission. Preserve stage receipts across crashes.
- [ ] Deliver a usable owner-authenticated private Moksha website preview with *actual approved photos*, mobile-first visual and accessibility QA; no production WordPress writes.
- [ ] Finish thermally safe, rights-verified automated Reel Studio preview with real assets, independent FFprobe/caption/brand review and no automatic publishing.
- [ ] Add campaign/performance feedback and measured EVOLUTION suggestions, not model-self-certified quality.

### P2: Resilience, governance, future integration
- [ ] Full Mac cold reboot and SSH/network/429/provider interruption recovery, nonduplicating retries, multi-hour soak and queue receipt reconciliations.
- [ ] Approved-source monitoring schedule and meaningful-change alert quality.
- [ ] Real GSC country/device breakdown only via authorized read-only connection; honest unknowns otherwise. Historical Trends index requires independently supplied authentic data, not national RSS.
- [ ] Integrate with wider Matrix Brain and future Open WebUI interface only after UI license/security/central coordination certification. Keep dev, sales, accounts and other departments bounded.
- [ ] Maintain exact OSI-approved licensing and no paid dependencies. Opera owner exception remains narrow to public research.

## 7. Safe verification and rollback for next operator

```bash
# Run on Mac through connected owner-scoped Generic Linux SSH; poll task UUID to terminal.
cd /opt/business-house-matrix/marketing/brain
python3 brain.py status --verbose
systemctl --user is-enabled bhm-marketing-queue-worker.timer
systemctl --user is-active bhm-marketing-queue-worker.timer
.venv-supervisor/bin/python -m pip check
.venv-supervisor/bin/python -m unittest test_marketing_supervisor_langgraph -v
python3 brain.py receipt d12ad35f-adb5-4d4b-b417-aea13e31c1bd
test -f reports/private/andaz_arambol-supervisor-report.md
# To roll back only v2, when no v2 jobs in-flight:
python3 marketing_supervisor_bridge_patch.py --rollback
```

- Preserve dated backup `marketing_report_orchestrator.py.pre-langgraph-supervisor-20261022`.
- Do not reset Mac queue, delete owner-private sources, remove identity keys, change root/Wi-Fi/SSH, disable unrelated user services or recreate the worker.
- Research-only license review passed by metadata. Confirm account/model quota availability per task. Stop on unresolved facts, payments, new credentials, public publishing or sensitive-data transfer.

## 8. Minimal next-chat prompt

> **Continue Business House Matrix Marketing Superbrain.** Read `docs/handoffs/MARKETING_SUPERBRAIN_TAKEOVER_2026-10-22.md` on GitHub main, verify Mac/Dell live receipts, reuse the deployed LangGraph Marketing Brain and signed Dell workers. Fix Andaz evidence quality, extend verified research → full report → QA autonomy; preserve OSI-only, private data, no publishing/spend, and document results. Do not rebuild existing infrastructure.
