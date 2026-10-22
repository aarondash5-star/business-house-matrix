# Business House Matrix — General Dev Operator release plan

Date: 2026-10-22 | Owner-requested full autonomous Dev Matrix

## Definition of done

The Dev Matrix accepts a natural-language software goal, binds it to an enrolled repository and immutable baseline, independently designs, edits, tests and repairs code within a disposable isolated workspace, reports exact QA results, and creates a reviewable Git artifact. Failures must return a terminal receipt; external publication, spending, configuration escalation and tenant changes must not occur without separate authorization.

## Reuse: no new orchestration stack

- Existing Dell `matrix-controller` durable SQLite queue, idempotency and recovery.
- Existing `matrix-pi-local` (MIT coding-agent frontend) and local Ollama Qwen/Granite models. No paid API.
- Existing Bubblewrap network/host-isolation, reviewed-patch runner, source governor, QA/QC and EVOLUTION.
- Existing GitHub connector for review branches/PR creation under authenticated account.
- Mac as independent reviewer. Open WebUI remains the approved interface; OpenClaw and LibreChat remain deferred.
- Matrix is **independent** from Moksha Master and private Pine. Do not import protected source data.

## Operating model

1. **Enroll**: an operator approves a project manifest with repo identity, base SHA, readable context paths, writable file globs, language test profile, model usage cap, and reviewer.
2. **Plan**: local agent reads only the enrolled source snapshot, produces a bounded plan and patch proposal (no executable tool grants encoded in model output).
3. **Act**: controller validates the patch against policy, applies it only inside a disposable workspace; tools are presented as fixed operations, not an unrestricted host terminal.
4. **Test**: run project QA inside Bubblewrap with no network, no host home, no cross-project mounts, finite CPU/memory/runtime; use independent test cases.
5. **Repair**: supply sanitized failure output to the model for at most two revised proposals; enforce identical scope, independently retest.
6. **Review**: preserve hashes, diff, local review branch/commit and receipt; request human review at material failure/permission/new-project boundaries.
7. **Deliver**: authenticated GitHub PR/staging preview through separately enrolled, approval-controlled connectors; never auto-merge/deploy.

## Hard constraints

- Default deny for un-enrolled projects, SSH privileges, shell escape, arbitrary URLs, credential use, external write APIs and changed host settings.
- No production deployments, trading, payment, social publication, root/sudo changes or cross-tenant data.
- Crash-safe idempotency; never replay a task whose downstream outcome is ambiguous.
- Missing QA, ambiguous external side effects, failed isolation probes or absent hash-pinned baseline are hard stop conditions.
- Per-job stop/cancel must be race-checked; an active task needs a proven termination receipt before terminal cancellation is acknowledged.

## Staged gates

A1 exact repository scope and immutable base; A2 bounded autonomous coding loop; A3 isolated multi-language QA; A4 reviewable Git artifact; A5 bounded self-repair; A6 durable queue and cancellation; A7 scoped MCP (read-only before per-project writes); A8 live benchmark with fault injection and rollback. Each gate requires test evidence and a source reference before promotion.

## Release rule

A future code or review artifact is not a deployment. The operator must be wired into the live controller, tested on an independently enrolled real-world but non-sensitive project, and verified running before stating **FULL GENERAL DEV AUTONOMY CERTIFIED**. The existing `dev_scoped_build` success is a *restricted synthetic-only* precedent, not sufficient by itself.

## Current status

Implementation and test progress are recorded in `docs/receipts/DEV_AUTONOMY_RUNTIME_DEPLOYMENT_20261022.md`. The existing controller must remain healthy and reversible while additional capabilities are developed.
