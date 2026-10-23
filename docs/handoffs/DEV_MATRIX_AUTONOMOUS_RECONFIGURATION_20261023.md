# Detailed Autonomous Dev Matrix — staged architecture profile

**Date:** 2026-10-23
**Branch:** `feat/dev-supervisor-gate-s-20261023`
**Owner intent:** Enable a detailed AI-driven autonomous software-development team rather than a fixed five-step task dispatcher. Preserve the certified v6 execution controller, provider quotas, security gates, worker identity, rollback and previous Gate E NO-GO status.

## Operating model (three distinct planes)

1. **Cognition — unrestricted planning depth within finite resource budgets.** A local streaming Ollama Qwen worker, `brain/supervisor/gate_s_local_streaming_v3.py`, reads verified Andaz context, decomposes research, UX, implementation, QA/security and critique into five reasoning passes. Context is richer; streaming responses save partial drafts to disk; `keep_alive=20m` between passes avoids repeated cold starts; the last pass unloads. Five passes are organizational aids, **not a fixed five-task response**. Each phase chooses its own detailed work packages, produces acceptance criteria, evidence requirements and risks. This may be replaced with a stronger hosted planning model through existing approved $0 API routes once proven.
2. **Coordination — staged durable task DAG.** `brain/supervisor/autonomous_dev_matrix_v1.py` validates up to 30 independent work packages in the current structured contract (future hierarchical subtasks can exceed this across work orders), exact specialist role allowlist, critical-path dependencies and safe parallel batches (max 3 candidate slots). Persists immutable plan hash, individual task proposals, worker mapping and failure receipts in isolated SQLite. Explains blocked downstream work and leaves final status `owner_review_required`.
3. **Authority — certified v6 only.** AI-generated plans, proposed commands, deadlines, sources and permissions are untrusted data. No model-generated shell or arbitrary MCP tool is executable from the candidate. Approval, identity, idempotency, sandbox, private staging, security and independent QA remain enforced outside any LLM. This stage uses **simulation-only worker receipts** and does not attach to the live v6 executor or GitHub merge/publish tools.

## Six Dev specialties and their specific responsibilities
| Role | Outputs | Evidence needed before downstream handoff |
| --- | --- | --- |
| Research | source-verified current-state audit, architecture inventory, requirements/unknowns | referenced source/inspection receipts, no invented claims |
| Design | mobile-first sitemap, design tokens, wireframes, real-photo/content truth map | owner-approved materials, responsive QA criteria |
| Development | reviewable source modules, private staging plan, safe PMS integrations | exact approved paths, build/test receipts, production unchanged |
| QA | independent immutable tests, mobile browser and booking negative-path evidence | test artifacts, error reproduction, critical issues blocked |
| Security | privacy/permissions analysis, threat model and rollback evidence | independent secure signoff; no unapproved credentials |
| Review | owner-facing evidence and release decision package | explicit owner decision separate from model / synthetic QA |

**Concurrency rule:** autonomous reasoning/decomposition can propose parallel research, design, and preparation work, but dependency and identity constraints determine actual scheduling. QA/security/review are not silently grouped with the work they approve. Failure escalation is not automatically retried. An external worker receipt cannot claim success without evidence.

## Actual state of integrations
- `matrix/graph.py` remains a **simulation**, not a wired production LangGraph supervisor.
- Dev Matrix v6 is a **certified allowlisted task dispatcher**, not a full cognitive supervisor; it is unchanged.
- Gate E coding autonomy remained **NO-GO**, including previous failed Python coding benchmarks.
- Connected Dell worker used for staging; Mac independent peer may be offline and must be reverified before certification.
- Existing OpenRouter/Groq/Local Ollama model router remains free-only, with external prompt/token limits preserved. Do not change these to increase planning depth: use stage decomposition, streaming and independent QA.
- This staged design does **not** assert functional website code was written, autonomously deployed or live workers invoked.

## Staged acceptance gates
- **A — Plan intelligence:** five full Andaz planning passes produce a complete artifact with real tasks, evidence, deliverables, dependencies, acceptance and risk critique. Manual review of correctness beyond keyword presence; no unsupported PMS/price or kitchen claims.
- **B — DAG and policy:** full regression tests on reference 16-task work order: role allowlist, dependency graph, simulated parallel batches, persisted receipts, no real executor, failures blocking downstream tasks, final owner approval required.
- **C — Real specialist onboarding:** independently certify fixed-function worker adapters for read-only source audits, isolated code/build/QA, scoped identity and expiring permissions. Inject failed tests and verify no unapproved retry, scope growth, spending or publishing.
- **D — Cross-host and repair:** Mac/Dell independent evaluation, calibrated model comparisons, QA review of real work, bounded self-repair, rollback drill and canary. All prior v6 protections stay.
- **E — Promotion decision:** only with signed evidence, existing Gate E independent Python/external-project autonomy passing, and owner approval; separately reviewed guarded adapter to v6. No automatic cutover.

## Developer commands (isolated, never production)
- Unit tests: `python3 -B -m unittest discover -s tests -p 'test_autonomous_dev_matrix_v1.py' -v`
- Simulated 16-task handoff: `python3 -B brain/supervisor/autonomous_dev_matrix_v1.py --plan benchmarks/gate_s/andaz_gpt6_reference_plan_20261023.json --database <new-isolated-file.sqlite3> --simulate`
- Stream local Andaz cognition: `python3 -B brain/supervisor/gate_s_local_streaming_v3.py --out <existing-empty-staging-dir>` (launch via bounded owner-scoped unit, test only)

## Non-negotiable security invariant
`model output ≠ owner authorization ≠ approved tool capability ≠ verified QA ≠ permission to deploy`.

## Current rollout decision
**RECONFIGURED AS A CANDIDATE, NOT A PRODUCTION SWITCH.** Detailed planning has been enabled in isolated model runner; durable autonomous dispatch **simulation** is separate and auditable. v6, Gate E, production and all protected controls remain untouched. This document intentionally discloses the remaining gap to genuinely autonomous project execution.

## Dell implementation and evaluation receipts, 23 October 2026

- **Streaming planner source:** `brain/supervisor/gate_s_local_streaming_v3.py`, multi-phase local Qwen `qwen3:4b-instruct` with controlled streaming, isolated evidence files, 20-minute keep-alive between phases, and explicit budget/terminal-state tracking. Initial cognitive policy suite **8/8 PASS**, original terminal receipt `b116a5ba-5ba5-4403-be4d-33026699e4e1`; corrected revision **8/8 PASS**, terminal receipt `f15b25d1-2163-424e-84de-6dc60a3c89e9`.
- **First real Andaz multi-pass run:** `bhm-gate-s-andaz-local-v3-20261023.service`, terminal state `incomplete`; phase 1 produced 3,291 characters / 720 tokens in **201.4s** and `done_reason=length`. The final plan was **not produced**; the partial was preserved. It also proposed accepting only **90% inventory/price consistency**, an unsafe unsupported quality target. Do not classify as PASS.
- **Correction:** improved output instructions, increased phase `num_predict` from 720 to 1,400, expanded total elapsed budget and per-stage timeout while keeping streaming and finite runtime. Corrected model-only candidate file on GitHub; no model install/uninstall or v6 changes. **Second evaluation** `bhm-gate-s-andaz-local-v3b-20261023.service`, isolated folder `~/matrix-gate-s-andaz-local-v3b-20261023`, launched receipt `0e8ad154-59e0-4902-aa89-85ae7f3edb76`; running at the latest verified state. **No completed second-run plan is claimed**.
- **Independent rule-based content QA** `benchmarks/gate_s/review_local_plan_v3.py` rejects incomplete/truncated phases and unjustified sub-100% booking consistency; unit suite **5/5 PASS**, terminal `3d56a668-22f3-4228-82ef-2cc11e752eb9`. This does **not** replace actual expert review, live site verification or QA of factual content.
- **Autonomous task-DAG candidate** `brain/supervisor/autonomous_dev_matrix_v1.py`, 13/13 tests PASS, terminal `2452b6f1-de55-406c-9da8-2108cab692eb`. Simulated 16-task Andaz reference DAG PASS, with multiple independent batches, persisted isolated SQLite receipts, and final `owner_review_required`; no actual worker invoked. Terminal `c94b95c0-7d66-42e2-be3c-fe1e6c1f6c66`. Recorded no permission changes, no code/site execution and no automatic replay.
- **Certified v6 unaffected:** `bhm-autonomy-controller.service` remained **active**; SHA-256 `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e` reverified at terminal `89c06616-d12e-4daa-bd1a-b83edfb3e849`. No GitHub merge or production deployment.
- **Overall verdict:** staged cognitive and orchestration architecture implemented and unit/integration-simulation tested; real live autonomous Dev execution Gate E remains NO-GO. Need complete coherent model plan, semantic QA, approved worker adapters, Mac peer QA and canary/rollback before release. No background completion claim or automatic promotion.
