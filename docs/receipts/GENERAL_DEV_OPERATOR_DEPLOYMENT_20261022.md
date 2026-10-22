# General Dev Operator — staged runtime + controlled live deployment

**Date:** 22 Oct 2026 (Asia/Kolkata)  
**Environment:** Business House Matrix, independent from Moksha Master  
**Repository:** `aarondash5-star/business-house-matrix`  
**Source branch:** `feat/dev-autonomy-runtime-20261022`

## Executive status

The Dev Matrix has a newly implemented, **bounded repository-enrolled autonomous coding route** using its existing Dell controller, local Granite model, an independent rootless Bubblewrap workcell and an unpublished local Git review. General-purpose arbitrary repository access, unconstrained Pi tool calling, broad multi-language CI, private Pine, GitHub auto-push/merge, production release and spend are **not certified**. Do not present this gated model-to-code route as unrestricted full autonomy.

## Source of truth

- Design and gates: `docs/architecture/GENERAL_DEV_OPERATOR_RELEASE_20261022.md`.
- Enrolment/policy: `brain/dev-operator/protocol.py`.
- Sandbox worker and launcher: `brain/dev-operator/workcell_worker.py`, `workcell_runner.py`.
- Model→QA→repair→review loop: `brain/dev-operator/agent_loop.py`.
- Enrolments: `brain/dev-operator/enrollments/` (currently synthetic public Matrix UI work only).
- Controller release candidate: `brain/mvp-controller/controller-general-dev-v2-candidate-20261022.py`.
- Controller action: `dev_general_build`, mode `manifest_enrolled_sandbox_review_only`, only `matrix_dev / matrix-dev-dashboard-v2`.
- Original older action `dev_scoped_build` preserved; `dev_proposal` remains proposal-only.

## Independent validation

- Dell and Mac Python 3.12: **21/21 policy + workcell tests each PASS** (postfix) on new source.
- Dell and Mac controller candidate self-test PASS (persistent SQLite/idempotency/blocked routes/privacy/recovery), source commit `0fa6475c900485063186c5ba41394508b3b5ed7b` and final release commit `ba9949bdc7990b74460b2e3262273a829771ad5a`.
- Workcell negative probes: cross-file traversal rejected, hidden files rejected, mutation of test files rejected, unsupported Node test profile fails closed, invalid manifest and cross-repository/permission fields denied.
- First independent autonomous model run: `matrix-dev-taskboard-v1` stage; receipt status `verified_local_review`; **one model attempt**, HTML semantic QA PASS, unpublished local commit **`71accb97d05cc1d00c95152c9b19f941e7eed2d2`**. No live backend/MCP product access.
- Dell/Mac Generic SSH heartbeat observed online; all earlier six lanes passed.
- Underlying Bwrap remains `--unshare-all` and worker is invoked without model-selected shell commands. Ollama model runs offline/no-tool on Dell outside the workcell; generated source is applied and checked *inside* workcell.

## Live deployment facts

- Exact controller predecessor SHA256 `0e0060cfafae64a27cbdca34e0e63d03150ca84e54bde8ca5294ccc4cd6c6367`; stage baseline file matched this hash.
- Previous controller copied unchanged to `~/matrix-controller/controller.py.bak-20261022-generaldev-v2`.
- New live `~/matrix-controller/controller.py` SHA256 **`d99f9ec6b70a2e0acea49604856084df8d208eee37c18e93a4e72172e3e0c656`**.
- The user-level `bhm-autonomy-controller.service` restarted and returned ACTIVE; live controller selftest PASS; existing services and task history retained, with 0 in-flight tasks before promotion.
- Fixed release files installed to `~/matrix-controller/general-dev-release-v2/` and compared byte-for-byte with reviewed repository source; no root/SSH/auth/network changes.
- Controller-enqueued exact task ID **`3ff6f0a9-8358-44de-9735-119884d130c9`**, action `dev_general_build`, manifest `matrix-dev-dashboard-v2`, idempotency key `dev-general-controller-v2-20261022`. Queued then delegated to `matrix-general-dev-dispatch-v2-20261022.service`.

### Independent terminal controller release result

**Pending fresh terminal receipt** at initial documentation commit. Before certifying this final stage, read `~/matrix-controller/release-stage-general-dev-20261022/runs/matrix-dev-dashboard-v2/receipt.json`, verify source scope, unit exit, QA, local review Git SHA and live controller's terminal task state. Never infer success from service launch; retain a failed/uncertain result without replay.

## Security and remaining roadmap

The underlying trusted controller explicitly allows only the above public enrolled manifest; arbitrary projects do not self-register. The model cannot select repository paths, test mode, tools, credentials, runtime commands, production actions or external providers. The job has bounded 3-attempt repair and a one-time run path.

**Still pending to claim full general-purpose autonomy:** independent trusted repository enrollment for any permitted project; protected review-only GitHub PR creation by autonomous worker with per-repository identities; approved language/runtime adapters (Node currently un-certified); source-context retrieval with immutable baseline; multi-task dependencies/prioritization/cancellation and crash recovery under concurrent stress; browser/a11y/security QA for generated outputs; hardened capability-specific MCP write connectors; repeatable cross-project isolated E2E tests; interactive work acceptance.

## Rollback

Stop only after tasks are drained and any delegated outcome has a terminal receipt. Restore `~/matrix-controller/controller.py.bak-20261022-generaldev-v2` over `controller.py`, restart `bhm-autonomy-controller.service`, verify active and original SHA; leave historical receipts for audit. Do not modify root, Generic SSH bridge, or unrelated machines.

**Release gate:** No auto-merge, no prod publish, no spend, no Pine private account, no TradingView writes. All project permissions remain restricted until specifically enrolled and QA-certified.
