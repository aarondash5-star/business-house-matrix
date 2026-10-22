# Business House Matrix — Marketing Superbrain LangGraph Live Deployment & Certification

**Date:** 2026-10-22 (22:10–22:40 IST approx).  
**Live status:** **DEPLOYED** on Mac; bounded Brain supervisor and private report generation **PASS**. Research facts **NOT CERTIFIED**.  
**Project boundary:** Business House Matrix independent from Moksha Master.

## Verified hardware / services

- Mac `mac-linux`: paired online and three SSH lanes responding after the prior bridge outage. At deployment check, ~6.2 GB available memory; Mac temperatures observed **46°C** before dependency installation, **65°C** at QA and **50°C** after Andaz job. These are spot readings, not full thermal soak certification.
- Existing `bhm-marketing-queue-worker.timer` enabled + **active** at end. The timer was briefly stopped for diagnosis and restarted after crypto repair; no cron duplication or new permanent worker was installed.
- Dell `dell-linux`: online; `bhm-searxng`, `bhm-research-relay`, `bhm-marketing-research-api` all **active**; Dell API `GET /health` version 1.3 returned `ready`. Signed SearXNG adapter in the new venv returned 5 search results and verified `device_peer_verified=true`.
- Existing Mac Brain remains the task registry and SQLite queue; `marketing_report_orchestrator.run` now has an opt-in reversible v2 wrapper using the isolated venv. Original v1 report worker saved at `marketing_report_orchestrator.py.pre-langgraph-supervisor-20261022`.

## Libraries and installation correction

The first two attempts to install exact `langgraph==1.2.16` and `pydantic==2.14.1` from `files.pythonhosted.org` timed out on the 5.5 MB `zstandard` wheel. This was a package transfer failure, not a broken Python dependency. The Mac heartbeat had already recovered before retries.

- Verified alternate public package index `https://mirrors.aliyun.com/pypi/simple`; its `zstandard==0.25.0` wheel downloaded successfully to local private install cache, then the remainder of the pinned dependencies installed into dedicated `/opt/business-house-matrix/marketing/brain/.venv-supervisor`.
- `pip check`: **No broken requirements found**.
- **Complete actual runtime freeze:** [requirements-marketing-supervisor.lock.txt](../../marketing/requirements-marketing-supervisor.lock.txt); Python 3.12.3. Runtime license metadata checked for every installed non-pip dependency: MIT, BSD-2/3, Apache-2.0, MPL-2.0, MIT-0 and PSF-2.0 identifiers. Installed LangGraph is MIT; Pydantic MIT.
- The initial live job then exposed the **missing PyNaCl** module: `ModuleNotFoundError: No module named 'nacl'`, because the fresh venv was isolated from the existing system-level signed relay dependency. Installed `PyNaCl==1.5.0` (Apache-2.0), `cffi==2.1.1` (MIT-0) and `pycparser==3.11` (BSD-3-Clause) in the venv via the alternate index. Follow-up imports of `SigningKey`, `VerifyKey`, `PrivateKey` and `SealedBox` **PASS**. This dependency is pinned in the new lock to prevent recurrence.
- No altered SSH keys, Supabase relay secrets, browser session, root permissions, public endpoint or paid API signup.

## Actual regression tests and signed smoke

- **6/6 offline LangGraph/Pydantic regression tests passed**, including static vs validated dynamic query planning, malicious query rejection, correctly verified signed response, one bounded replan after invalid relay, independent QA/report creation and unknown-business rejection.
- `pip check` pass; source compile pass on Dell and Mac; exact-match reversible bridge patch preflight pass.
- **Real signed Mac→Dell SearXNG search** in the new venv returned **5** results with authenticated peer verification; Mac terminal receipt `3e4b83fc-97f5-497a-95bf-90422092627e`, exit 0.
- `systemctl --user is-active bhm-marketing-queue-worker.timer`: **active**; `is-enabled`: **enabled**.
- Existing Brain validates exact `{"business":"andaz_arambol"}` or `{"business":"moksha_arambol"}`; no arbitrary URLs, providers, payments or command execution.

## Real unattended Andaz live run

Idempotency `bhm-andaz-langgraph-supervisor-live-v2-20261022`. Existing Brain queued `research_report` job **`d12ad35f-adb5-4d4b-b417-aea13e31c1bd`**. The **existing systemd timer consumed it autonomously**, with no operator `work-once` call.

- Attempt **1** failed due missing `nacl` from the new virtual environment.
- Attempt **2** was consumed before the timer pause fully took effect; same missing dependency.
- After installing the pinned crypto dependency and passing the real signed search smoke, the remaining attempt **3 completed**, `error=null`, **27.532 seconds**.
- Final Mac queue: **30 completed**, and `bhm-marketing-queue-worker.service` returned `Result=success`/exit code 0.
- Generated owner-private files:
  - `/opt/business-house-matrix/marketing/brain/reports/private/andaz_arambol-supervisor-report.md` (**4,233 bytes**).
  - Adjacent `andaz_arambol-supervisor-report.json` (**11,255 bytes**, mode 0600).
- Supervisor behavior: **model-assisted public query planning used**; **3** public research queries across **2** rounds with bounded critique/replan; **5** unique non-own-property source leads across **5** domains; hosted model ideation was present and labeled as unverified hypotheses.
- **QA `PASS` as a safe private output**, **NOT as an authoritative business report**. Only **1/3** public discovery queries produced usable results in this run. Critic finding `low_source_diversity_or_missing_evidence`; final state **`INSUFFICIENT_EVIDENCE`**, `approved_for_customer_facing_use=false`, `independent_claims_verified=0`, `publish_allowed=false`, `spend_allowed=false`. No competitor price, ratings or demand numbers certified or invented.
- Existing previous 15-source Andaz `research_report` from v1 remains in its separate private file. V2 has not yet merged v1 evidence memory or restored coverage after upstream search failure; this is the leading **quality** blocker.

## Engineering ownership / topology

```
Existing Marketing Brain (Mac) + one durable SQLite queue / systemd timer
  └─ research_report (approved business)
       └─ isolated LangGraph supervisor v2 (same Mac)
             ├─ plan (fixed fallback + optional policy-approved free OSS-model plan)
             ├─ research (existing signed encrypted Dell SearXNG adapter)
             ├─ critic (Pydantic typed source-diversity QA)
             ├─ bounded replan (one additional round; hard query limit 3)
             ├─ compose (evidence-aware private report + unverified ideation)
             ├─ QA (human-review and no-publish/no-spend enforcement)
             └─ private Markdown/JSON receipts
```

There is **no second permanent marketing service**, no unrestricted browser or login capability, no gateway widening, no ad spend and no production content publication.

## Remaining release gates / next actions

1. **Evidence completeness:** SearXNG query reliability, graceful fallback to bounded authorized fresh/stored sources, source freshness/confidence, independently verified true competitor businesses, conflicting price/service detail, historical vs current data. The current Andaz report is review-required.
2. **Production-grade model critique:** Real evidence-aware planning/rewrites without treating source webpages as instructions; full report with current corroborated source-cited claims and internal human review.
3. **Automated QA→follow-up** should track multiple agent rounds and source budgets with durable partial receipts across crashes; present graph creates one report per job with one bounded replan and existing outer queue retries.
4. **Creative marketing:** Design, source-approved media/reels, accessible private site staging, conversion analytics and EVOLUTION feedback loop are not implemented by this specific supervisor deployment.
5. **Ops:** Cold Mac restart, network loss and multi-hour failover/recovery not yet certified; at this checkpoint the isolated package download mirror problem was solved without modifying system network settings.
6. **OSI-only rule:** Keep open-source dependencies validated. The existing owner-requested Opera public DDG fallback is still an explicitly documented proprietary exception; the new LangGraph supervisor does not control saved-login Opera sessions.

## Rollback and diagnostic commands

```bash
cd /opt/business-house-matrix/marketing/brain
python3 brain.py status --verbose
systemctl --user is-enabled bhm-marketing-queue-worker.timer
systemctl --user is-active bhm-marketing-queue-worker.timer
.venv-supervisor/bin/python -m pip check
.venv-supervisor/bin/python -m unittest test_marketing_supervisor_langgraph -v
python3 marketing_supervisor_bridge_patch.py --rollback  # ONLY if v2 jobs terminal
```

Rollback of v2 routes `research_report` to its existing safe v1; **do not disable the Brain timer, change keys or remove Dell services**. No production publishing enabled.

**Authoritative code and tests on main:** `marketing/marketing_supervisor_langgraph.py`, `marketing/test_marketing_supervisor_langgraph.py`, `marketing/marketing_supervisor_bridge_patch.py`, `marketing/requirements-marketing-supervisor.lock.txt`. Earlier [staging report](MARKETING_SUPERBRAIN_OSS_STAGED_2026-10-22.md) is historical and superseded by this live certification.
