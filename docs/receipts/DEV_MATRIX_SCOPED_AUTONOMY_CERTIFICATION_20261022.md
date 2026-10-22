# Dev Matrix — restricted autonomous coding release certification

**Date:** 22 October 2026 (IST)  
**Scope:** Independent Business House Matrix / Dell, exact public synthetic project `pine_mcp_chat`.  
**Live decision:** **CERTIFIED for a manifest-enrolled, one-shot offline model→validated source→isolated QA→local review commit workflow.**  
**Not certified:** unrestricted coding or shell tools; automatic remote Git push/PR/merge; arbitrary projects; private Pine; public deployment or spending.

## Verified source and deployment

- Original live Dell controller SHA256: `448a587b6c11bfbbd4618afc65b6f90a5f56bf54b075642817720c85228aa884`.
- Exact unchanged original version committed for review at `brain/mvp-controller/controller-live-snapshot-20261022.py` (commit `db87285a3e632f8ab6d2ab2e162ba4919df3fbb9`); private hard-coded credentials scan: no literal credential assignments identified. This is source versioning, not a comprehensive secret scanner.
- Reviewed additive candidate `brain/mvp-controller/controller-scoped-autonomy-candidate-20261022.py`, commit `f50ee346f858d34645cd89e922ae17d9a0f29722`. Additive diff reviewed and limited to exact synthetic build manifest/paths, pinned script, bounded runtime/memory, and QA receipt contract. All existing Marketing, Moksha, research, external MCP and other actions preserved.
- Live controller deployed at `~/matrix-controller/controller.py`: SHA256 **`0e0060cfafae64a27cbdca34e0e63d03150ca84e54bde8ca5294ccc4cd6c6367`**. Live service `bhm-autonomy-controller.service` restarted and confirmed active. Controller selftest PASS after restart.
- Immutable rollback copy retained at `~/matrix-controller/controller.py.bak-20261022-dev-autonomy-v4`, SHA256 `448a587b6c11bfbbd4618afc65b6f90a5f56bf54b075642817720c85228aa884`. No SSH/root/system networking/other service permission changes.

## A1 source-governed coding integration and safety

- Reused existing MIT Pi v1.3.0 offline/no-tool wrapper, Ollama `granite4:3b`, rootless Bubblewrap reviewed-patch runner, Python unit tests, local Git and existing durable SQLite controller. The installed Granite model reported **Apache License Version 2.0** from `ollama show granite4:3b --license`; MIT from Pi package metadata. All software licensing remains OSI-compatible within current reused components; no paid API enabled.
- The generic A1 source governor now has **two fixed manifest-specific allowlists**. Exact project/repo/work ID and allowed files are frozen in code; model cannot select paths, commands, credentials, tools, repositories, tests, shell or providers. Unknown fields, cross-tenant requests, stale SHA/overwrites, escapes/symlinks, unsafe source and network patterns fail closed. A single bounded deterministic correction repairs a missing HTML `main` landmark without granting arbitrary edits.
- New sources: `brain/secure-coding/source_governor.py`; `strict_content_agent_v3.py`; `dev_autonomy_task_v4.py`; independent regression tests. Existing `scoped_dev_pilot.py` and `reviewed_patch_runner.py` retained.
- Two independent Dell + Mac suites each passed **13 governor tests + 7 agent tests = 20/20**, exit code 0, pinned source HEAD `c1fa0e6fffda30d1a4ec874dbc5434be2531d39c` at that checkpoint. Five existing rootless Bubblewrap security tests also passed on Dell, with host private files/foreign project hidden, network blocked and isolated workspace write permitted.
- Existing `dev_proposal` remains proposal-only; `dev_scoped_build` is `synthetic_model_sandbox_review_only`. Offline model works only within the enrolled workload. No unrestricted Pi shell is enabled.

## First complete staged autonomous run (V3)

- Stage worker on Dell `matrix-dev-autonomy-cert-v3-20261022.service` exited with validated receipt `verified_local_review`.
- Enrolled work ID `pine_chat_b1_synthetic_review_v1`; model proposal accepted first attempt; generated two fixed synthetic paths; Bubblewrap isolated QA **4/4 PASS**; local Git review commit **`6764836943bde1bd89636e34e0f44791ce8da850`**, unpublished.
- Immutable receipt located at `~/matrix-controller/release-stage-pine-mcp-sandbox-20261022/autonomous-code-state/pine_chat_b1_synthetic_review_v1/receipt.json`. No open-ended agent or root access involved.

## Independent live controller end-to-end run (V4)

- Controller task UUID **`2ce7c08b-e1f2-450e-a61b-5f234416daaa`**, project `pine_mcp_chat`, action `dev_scoped_build`, manifest `dev_matrix_synthetic_release_v1`, idempotency key `dev-matrix-autonomy-release-v4-20261022`.
- Durable queue submitted **once** and automatically delegated to `matrix-dev-autonomy-release-v1-20261022.service` without assistant-managed direct execution.
- Model proposal accepted in **1** bounded attempt; schema governor hash `b45d09650438f54b0cad0f97c6eec27e62cabd589a94a328ba87979f15dc9549`; sandbox QA **6/6 PASS**, exit 0; generated exactly `frontend/dev-autonomy-validated-v1.html` and `tests/test_dev_autonomy_validated_v1.py`; local Git review commit **`706f02d3077a3f551c6c3cf0eccc7627ed80a015`**.
- Live Matrix controller terminal state **`completed`**, QA level `synthetic_model_sandbox_review_qa`, attempts=1, no error, published=false. Sandbox receipt independently checked against `git rev-parse HEAD` and exact file-set contract. Postflight service active, source SHA unchanged, security doctor PASS.
- Explicit negative postflight: `pine_private` cross-tenant project rejected; unknown task manifest rejected. Retrying identical idempotency key returned same completed task UUID with `deduplicated:true`; no second work dispatched.
- No live Pine, TradingView, private repository, real MCP chat, order, trade, protected chart, paid API or production change.

## Certification boundary and remaining autonomous gates

| Gate | Scope demonstrated | Outstanding for general Dev Matrix |
|---|---|---|
| A1 secure executor | **PASS (strict synthetic manifest)** | New projects/files each need separately enrolled policies and source review |
| A2 bounded code/test/repair | **PASS for markup pilot** | General language toolchains, cancellation, robust multi-file retry budgets |
| A3 QA/QC | **PASS for tested scopes** | Full independent UI/security/replay suite for each future project |
| A4 Git workflow | **LOCAL review commit PASS** | Repository-specific authenticated branch/push/PR; no automatic main edits |
| A5 controlled repair | **PASS for one known markup defect** | Wider verified correction rules + failure recovery |
| A6 durable scheduling | **PASS queue/dedupe/crash conservatism** | General dependency prioritization and real thermal/concurrency QA |
| A7 MCP | Existing read-only governed docs route retained | Per-project write scopes and project-specific connector enrollment |
| A8 release controls | **PASS current synthetic E2E** | General autonomous multi-project release certification |

A critical distinction: **the Dev Matrix can now autonomously complete a specific approved synthetic coding task; it cannot yet accept arbitrary user coding requests without prior manifest/project enrollment.** The completed manifest is one-shot and cannot be replayed. Do not advertise fully generalized autonomy or automatic Github PRs.

## Rollback and handover

Rollback only if required after draining current tasks and verifying no ambiguous delegated operations:
```bash
H="$HOME/matrix-controller"
cp -p "$H/controller.py.bak-20261022-dev-autonomy-v4" "$H/controller.py"
systemctl --user restart bhm-autonomy-controller.service
systemctl --user is-active bhm-autonomy-controller.service
```
Existing receipt histories and new helper source can remain for audit; no SSH credential or root change needed. The review branch/PR is not merged, and original synthetic Pine preview is not changed.

**Next release priority:** general Dev Matrix per-project manifest registry + disposable Git checkout + repository identity scoped review PR, CI gates, stop/cancel and bounded retry. Keep all publishing/spending/protected chart actions approval-gated. Continue via Issue #2 and draft PR #3; leave issue open until A1–A8 generalized independently.
