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


---

## Final postflight update — 22 October 2026

**Final decision: PARTIAL DEPLOYMENT ONLY. Full general-purpose Dev Matrix autonomy is NOT enabled or certified.**

The previously operational `bhm-autonomy-controller.service` is **active**, live SHA256 **`ce09dabcc4037a401eb8df3617c375dad0ffddc3cd32e81df056e26317db29bd`**. The saved pre-v3 backup is `controller.py.bak-20261022-generaldev-v3`, SHA256 **`d99f9ec6b70a2e0acea49604856084df8d208eee37c18e93a4e72172e3e0c656`**. Dell and Mac remained online at postflight.

### Successful evidence

- Initial separately staged **Granite4** task `matrix-dev-taskboard-v1`: model generated a complete scoped HTML file on attempt 1; sandbox QA PASS; unpublished local Git review SHA **`71accb97d05cc1d00c95152c9b19f941e7eed2d2`**. This proves the bounded standalone loop for one fixed public synthetic task.
- New protocol, parser, workcell and controller v4 candidate: independent Dell **28/28** and Mac **28/28** tests passed, plus controller selftests on both.
- Direct no-tool Granite raw-HTML diagnostic returned a valid enrolled-path proposal: **262 HTML characters in 33.1 seconds**; SSH receipt `8dab1a0d-115e-412f-bb76-9656483a70e5`. The model is OSI-compatible, with the installed model declaring Apache License Version 2.0.
- Source-controlled candidate `brain/mvp-controller/controller-general-dev-v4-candidate-20261022.py`, commit `2f997241e7665865c40c42177c9fb246c1874953`, is available in the feature branch but **NOT deployed**.
- Draft review PR [#8](https://github.com/aarondash5-star/business-house-matrix/pull/8) created. No PR was merged and no source published automatically by Dell.

### Failed / blocked evidence

- Controller-dispatched v2 `dev_general_build` task **`3ff6f0a9-8358-44de-9735-119884d130c9`**: model emitted malformed JSON in all three guarded attempts. Terminal receipt `blocked`; controller status `needs_review`. No generated files applied or review commit created.
- Controller-dispatched v3 task **`9cc059c2-f547-4363-aa25-c9b3cccf091d`**: Qwen local model timed out on all three guarded attempts. Terminal receipt `blocked`; controller status `needs_review`. No generated files applied or review commit created.
- v4 remedial release: platform safety checks blocked the deployment operation **before** copying release files or changing the controller. The action was **not retried by an alternative route**. Final read-only verification: `~/matrix-controller/general-dev-release-v4` **does not exist**; live controller SHA unchanged.
- Current durable queue: **9 completed, 11 needs_review**, including the two newly failed general Dev tests. Existing historical tasks and failures remain intact; no uncertain task was blindly replayed.
- General-purpose model tool calling, arbitrary repository enrollment, Node/runtime QA, autonomous GitHub PR/push from Dell, cross-project MCP write permissions and production delivery remain unimplemented or uncertified.

### Recovery and next release gate

The enabled `dev_general_build` route is **manifest-enrolled, synthetic-only and not certified for routine use** following its two failed live E2E receipts. Preserve the current working controller, the historical receipts and the source-review branch. A subsequently **authorized** deployment route must first promote a new source-pinned candidate with verified independent test results and rollback. Require at least two successful controller-dispatched end-to-end jobs with different enrolled workloads, plus fault-injection and cross-tenant tests, before promoting general Dev autonomy. Do not bypass platform security checks to accomplish that.

**Do not represent the v4 candidate as deployed. Do not classify a started systemd unit as a successful autonomous development release.**
