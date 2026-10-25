# Dev Yard Manager v1 — Dell private installation and verification receipt

**Date:** 2026-10-25  
**Scope:** User accepted the scoped BMad + LangGraph + Spec Kit manager in conversation; exact frozen brief and RTM at `brain/dev-toolyard/multiproject_release/DEV_YARD_MANAGER_STACK_INTAKE_20261025.md`.  
**Project:** `matrix_dev_manager` / `dev_project_build` / `manager_bmad_langgraph_speckit_v1`  
**STATUS:** `PRIVATE_DEV_STACK_INSTALLED / GOVERNED_BUILD_PASS / INDEPENDENT_PRODUCT_QA_PENDING / NOT_RELEASED`

## What is installed on Dell

- Project workspace: `~/.local/share/matrix-code-executor/matrix_dev_manager` (project-scoped, private).
- BMad Method **v6.12.4** installed: core and BMM modules, **29 Claude-code skills** in local project scope. Official pinned Git source `bab9082c3e884e0d72c759bcd1a6d90bcc01be84`; installer npm package `bmad-method@6.12.4`, integrity `sha512-DBVws7H1NxpSOhv2DHvLEHTceQGCv9c+gBx/1cnVF38WhlN70854SnHUUCHkTuLIalu6hq/7LRVtAWCNHmnFEw==`.
- LangGraph **1.2.17**, Python venv at `.integrations/venv`; actual graph invoked and read back.
- GitHub Spec Kit CLI **1.2.3**, `specify version` passed; full project scaffold and bundled workflow under `.integrations/spec-workspace`.
- `uv 0.13.5` installed in project-local venv to satisfy BMad runtime prerequisite.
- `.integrations/pip-freeze.lock` captured 67 resolved distributions. These are project-local package versions, not a fully reproducible hash-locked cross-platform SBOM.

## Approval and SHA pins

- Exact owner decision: **"deploy this i accept"** following the reviewed PR #27 scope.
- Owner brief SHA-256: `f7369155eca6a4782ff33d52b2a3db7355a0c8840554b9d2e3be2346cbe8fc9f`.
- Contract SHA-256: `ccde38af41907568fedfe267d226f4a56500798378af261ee4c2507055f7681d`.
- Admission: `approved_intake` at submit and after concurrent controller update.
- Approved registry entry exists; no release approval entries exist.

## Governed Tool Yard build and regressions

- Controller task: `dd9ec531-0343-4767-84bd-b059813bed03`, `completed`, `project_isolated_executed_qa`.
- Reviewed patch SHA-256: `ab0f7a334bc09cce8095beb9180750a0cefc1c6978554cb27d3e728e5a2268a1`.
- `backend/manager.py` SHA-256 `57bb699407858f3a75ba942c3e661e77c4992e0d7e595cabd832611c4e68d62f`.
- `tests/test_manager.py` SHA-256 `0fff2ef965d1094e8fad441993e7da60be2ad07fda460fd8497eb0e002f10754`.
- Independent isolated test runner: **8/8 tests passed**, including missing critical requirement, silent downgrade, duplicate, cross-project invalid scope, Delulu no-fold rejection, rejected self-signed review, and good-fixture owner-review-only stage.
- Sandbox doctor: project workspace write YES, home/foreign project/private paths hidden, network denied.
- Private runtime readback: `private_runtime_smoke_passed`, 12 critical requirements in graph input, result `ready_for_toolyard` with `dispatch_authorized=false` and `release_authorized=false`.
- BMad project manifest SHA-256: `7a868eb45796aa0810948b5b243b3f169e0d4c3f35f4527ae177c070af83388a`.
- Spec Kit project manifest SHA-256: `b9529a4e026b97cb119467e84b88461c202b57d2d497ed3b47256f1d7b198dc9`.
- Negative release preflight: **DENIED** with `independent_quality_evidence_not_ready`. Good.
- No public site publish, model spend, service auto-start, root or delegated permission changes were carried out for this manager.

## Concurrent controller upgrade reconciliation

During final readback, another project upgraded the Dell Tool Yard controller from `0.2.2-global-intake-governed` (SHA `e7bbc99658ae1978e7c804fa763de993195a126f43558d238ab2b70269e688f9`) to **`0.2.3-shaadi-toolkit-governed`** (SHA `6c1442395ea1377794045c55ed6424b586161a7e48db706a538063b14deb11a8`). The Shaadi Toolkit backup `release-backups/shaadi-game-toolkit-20261025T114833Z/controller.py` matches previous controller SHA. Post-change manager admission, registry check and controller selftest all PASS. No competing release was rolled back or overridden.

## Remaining blockers (NO PRODUCTION CERTIFICATION)

1. Quality gate reports `evidence_missing` for **MGR-R01 through MGR-R12**, requiring real independent artifact-specific evidence and reviewer identities before acceptance.
2. Independent *semantic* QA must inspect actual Delulu known-bad frames/geometry, not merely a synthetic boolean fixture.
3. No governed autonomous dispatch or production release connectors; manager graph currently stops at a **planning handoff**, and does not yet act as a continuously running supervisor or use an LLM to understand new briefs.
4. Dependency provisioning was executed by bounded Dell development-lane commands into private project directories; those package-install operations were not mediated by the reviewed-patch Tool Yard controller. This **governance coverage gap must be closed** before claiming all execution fully mediated.
5. Persistent LangGraph checkpoint/restart behavior and end-to-end integration with the owner decision loop require further development and certification.
6. Full P0 corrective POA, separate owner product acceptance, artifact/target/time-bound promotion approval and external publishing guard coverage remain pending.

## Source of truth / PR

- Issue: https://github.com/aarondash5-star/business-house-matrix/issues/26
- Draft PR: https://github.com/aarondash5-star/business-house-matrix/pull/27
- SHA-matching implementation and tests: `brain/dev-toolyard/manager_v1/backend/manager.py` and `brain/dev-toolyard/manager_v1/tests/test_manager.py` on the feature branch.
- Do not merge or represent this as certified production pending P0 QA and explicit release acceptance.
