# Marketing Superbrain Open-Source Upgrade — Staged Release and Recovery

**Date:** 2026-10-22, approximately 21:45 IST | **Project:** Business House Matrix (not Moksha Master)  
**Release state:** **SOURCE STAGED AND SYNTAX CHECKED, NOT DEPLOYED/CERTIFIED ON MAC**  
**Live blocker:** Mac's generic SSH Linux worker stopped heartbeats during the isolated dependency-install attempt. Dell remains online. **Do not claim the new supervisor is running.**

## Objective and existing-system reuse

Promote the existing **Mac Marketing Brain** from a single-task dispatcher to a bounded, self-managing, owner-supervised department coordinator, starting with public research. Keep one Mac Brain queue and scheduler, the exact existing signed Dell research worker, local evidence storage, source review and no-publish/no-spend gates. Reuse the current Mac `research_report` task registered October 22; no new cron, account connector, external service, remote shell, port or root scope.

## Open-source library selection (license and reuse)

- **LangGraph 1.2.16 — MIT.** Stateful directed cycles for plan → signed research → evidence QA → bounded replan → draft → review → private receipt. Code: https://github.com/langchain-ai/langgraph ; package: https://pypi.org/project/langgraph/1.2.16/
- **Pydantic 2.14.1 — MIT.** Strict output contract and query/QA validation. https://pypi.org/project/pydantic/2.14.1/
- **Trafilatura 2.3.1 — Apache-2.0:** reuse the **existing Dell guarded extraction** module already tested and staged. New supervisor does not yet route arbitrary new extraction sources. No duplicate extraction daemon. https://github.com/adbar/trafilatura
- **SearXNG, SQLite, signed encrypted device-paired relay and the existing zero-paid provider router:** reuse the working infrastructure.
- **AutoGen** not selected; upstream publicly documents maintenance mode. **Haystack** (Apache-2.0) considered but not installed because it would duplicate the lightweight existing search pipeline; the requested libraries should fit existing Mac resource safeguards.
- Existing **Opera** public-only browser fallback remains an owner-requested proprietary exception; not part of the new supervisor dependency installation.

**Security:** OSI license metadata for the full transitive LangGraph/Pydantic dependency set must be audited from the actual isolated environment before live activation. Neither hosted LLM usage nor data processing may silently enable payment/publishing.

## Code delivered on GitHub main

1. `marketing/marketing_supervisor_langgraph.py` — real LangGraph `StateGraph`: a fixed business registry for Andaz/Moksha, optional reviewed-provider model-generated public search query, encrypted signed SearXNG queries, source diversity critic, exactly **one** bounded automatic replan, source-attributed private report, optional no-paid model ideation *flagged as unverified*, independent Pydantic QA and private Markdown/JSON receipt. Never promotes snippets/prices to facts.
2. `marketing/test_marketing_supervisor_langgraph.py` — six offline regression tests: strict planner, malformed model fallback, accepted bounded plan, signed-source report QA, bounded retry when transport fails, rejection of unregistered business. **Written but not executed yet**, because LangGraph has not been confirmed installed and Mac went offline.
3. `marketing/marketing_supervisor_bridge_patch.py` — reversible exact-hunk `marketing_report_orchestrator.run` integration into existing Brain task. Calls the isolated venv Python through a fixed no-shell subprocess with a 135-second bound; verifies receipt schema, guarded status, QA, publish/spend false, exact owner-private report path. Existing v1 implementation retained and can be restored.
4. The older `marketing/brain_report_task_patch.py` already registered `research_report` on the live Mac; this new upgrade **does not** re-register it or create a second queue.

## What was actually tested

- Existing Mac Marketing Brain **previously** confirmed live, including 29 completed jobs, timer and real Andaz private report. This applies to **v1**, not the new LangGraph v2.
- Pre-install resource baseline on Mac: Python 3.12.3, ~6 GiB available RAM, 53 GiB free disk, standard-library venv available. LangGraph/Pydantic were **not yet installed**.
- Sent a command to create an isolated Mac `.venv-supervisor` and install pinned `langgraph==1.2.16` and `pydantic==2.14.1`. SSH task UUID `076f5b7f-5ba5-49ba-97cc-f25d9847fb24`. **NO VERIFIED TERMINAL RECEIPT**; the command became stale-running after the Mac bridge stopped heartbeats. **Do not replay the install until the partial venv and running processes are audited.**
- Mac heartbeat last seen around **2026-10-22 16:09:25 UTC**; last check at **16:17:33 UTC** reported offline for ~488 s. Cause unproven; no claim that pip caused outage. Mac root privileges or Wi-Fi must not be changed blindly.
- Dell remained online: central controller, SearXNG, signed research relay and Research API were active in earlier probes.
- Dell isolated syntax preflight: `python3 -m py_compile` **PASS** for all **three** new Python modules; Dell SSH terminal receipt `5be2abbf-77b1-47e5-8490-418a4608f7f9`, exit 0.
- Runtime LangGraph graph execution, 6 new tests, full Mac venv license metadata audit and live Andaz v2 task **NOT PASSED/NOT ATTEMPTED**. There is no valid report `*-supervisor-report.md` yet.

## When Mac is available — exact next safe steps

1. Verify `linux_host_status(mac-linux)`, three lanes, owner-context, Mac RAM/sensor temperatures, systemd timer and live `brain.py status`. Never infer heartbeat success from queued task receipt.
2. Inspect existing `/opt/business-house-matrix/marketing/brain/.venv-supervisor`, pip/venv processes and previously queued SSH receipt `076f5b7f-5ba5-49ba-97cc-f25d9847fb24` **before doing anything**. If installs are incomplete, reconcile contents; avoid reinstalling blindly.
3. Verify installed LangGraph/Pydantic pinned versions and inspect **all** installed dependency licenses; do not promote unknown/non-OSI components.
4. Fetch `marketing_supervisor_langgraph.py`, `test_marketing_supervisor_langgraph.py`, `marketing_supervisor_bridge_patch.py` from the reviewed main-branch commit into existing Mac Brain directory (owner-only). Run `python -m py_compile` under the isolated venv and `.venv-supervisor/bin/python -m unittest test_marketing_supervisor_langgraph -v`. Fix tests; do not mask errors.
5. Run `python3 marketing_supervisor_bridge_patch.py` **preflight-only**. Apply only after tests pass; it makes a dated backup and leaves existing `research_report` registry untouched. Do not stop or replace `bhm-marketing-queue-worker.timer`.
6. Enqueue `brain.py enqueue research_report --payload '{"business":"andaz_arambol"}' --key bhm-andaz-langgraph-supervisor-live-v2-20261022`. **Do not manually work-once**. Poll the Mac Brain's genuine autonomous worker receipt to terminal success. Check private `reports/private/andaz_arambol-supervisor-report.{md,json}`, number of queries, critic verdict, provenance and QA. Force a controlled mock failed-search / insufficient-evidence regression before any release declaration.
7. Repeat `research_report` for Moksha using its own business slug; ensure strict tenant partition, no guest records, no unsupported verified facts, and no cross-business source/metrics mixing.
8. Update this receipt with actual Mac test IDs, terminal exit codes, dependency license list, report sample QA, and rollback results. Only then mark the v2 research supervisor **ACTIVE**.

**Rollback:** `python3 marketing_supervisor_bridge_patch.py --rollback` restores original report module from `marketing_report_orchestrator.py.pre-langgraph-supervisor-20261022` (only after any in-flight v2 job completes). The v1 Brain task and queue persist. Do not disable the systemd queue worker, Dell research service, private relay, plugins or Marketing Brain to roll back this unactivated upgrade.

## Remaining long-term Superbrain capabilities after v2 research gate

- Evidence corroboration via guarded Dell official-provider page fetch, official/OTA conflict resolution and scoring; not inferred from snippets.
- Adaptive planning based on sampled test results and brand objectives, with strict compute/query budgets and quality-based stopping.
- Full marketing artifacts: credible long-form report, channel/SEO strategy, copy variants and a measurable campaign plan, with citations and owner review.
- Creative research → approved footage → reel editing → independent visual/brand QA and thermal-safe rendering; no social auto-posting.
- Adaptive EVOLUTION: measure engagement and review corrections; evaluate outcomes with tests; propose improvements into gated Dev sandbox; never self-grant production permissions.
- Audit tool licensing, model availability, quotas, service recovery, Wi-Fi loss, Mac cold reboot and integrated QA before claiming a self-sufficient marketing department.

**Primary lesson:** the self-sufficient Marketing Brain must *own* the workflow and its safety/quality contracts; workers execute narrowly governed tools. Code files and a GitHub commit alone are **not** a deployed Brain.
