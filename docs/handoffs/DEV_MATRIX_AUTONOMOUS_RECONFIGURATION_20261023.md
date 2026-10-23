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
