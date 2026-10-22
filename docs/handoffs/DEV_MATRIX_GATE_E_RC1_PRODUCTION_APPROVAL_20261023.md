# Gate E RC1-to-production authorization and release gates

**Authorized by owner:** 2026-10-23 IST, "Document and approve all implement them". This approval covers all five sequential phases **subject to passing their prerequisite gates**. Authorization is not evidence of certification.

**Source:** Draft [PR #13](https://github.com/aarondash5-star/business-house-matrix/pull/13), branch `feat/dev-matrix-gate-e-general-runtime-20261022`, base certified `release/dev-operator-scoped-v6-security-20261022`.

## Owner-approved implementation phases
1. **RC1 Runtime hardening:** bounded model execution and all QA, cancellation and child reaping, global runtime and output caps, bounded concurrency, crash-safe receipts and fail-closed recovery. Tests/receipts required.
2. **RC1 CI and security:** secure Bubblewrap-enabled CI runner and explicit resource budget, source policy checks, test matrix and host peer QA. No bypass of absent sandbox or failed unrelated regression.
3. **Autonomy certification:** owner-enrolled non-sensitive real Python/Node multi-file benchmarks with independent tests, security rejections and traceable model runs. Do not replay existing completed Granite pilot.
4. **Dell production canary:** only after (1)–(3) pass, deploy separate owner-scope Gate E service; limited enrolled test jobs, without changing v6 controller, integrations or permission boundaries; observe faults and run rollback drill.
5. **Release:** only after clean canary + rollback and independently auditable signoff, create versioned release and enable approved multi-project autonomous development orchestration. GitHub PR write identity must be project-scoped and independently verified.

## Global invariants
- Preserve certified v6 SHA-256 `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`, its active service, rollback copies and historical receipts.
- No spend, private data mount, model-controlled host commands, arbitrary shell, unattended code merge, business-site publishing, credential expansion, or changes to root/SSH permissions. All are separate capabilities beyond this authorization.
- Fail-closed on any missing sandbox or CI failure; do not label verification as a production deployment.
- The existing `gate-e-public-python-parse` task is **finished** and must not be rerun; its valid pilot receipt remains immutable.
- Keep PR #13 draft until all release criteria pass; if a stage fails, document blockers rather than silently progressing.

## Initial known blockers (at approval)
- Hosted GitHub Actions starter-tests fails: hosted runner missing /usr/bin/bwrap, plus a marketing guard test.
- Mac/Dell exact-head Git clone stalled; avoid network-dependent staging until source transport is independently certified.
- Gate E Python QA subprocess cannot be cancelled mid-test; need hard global deadline and streaming output bounds.
- Durable multi-job controller, concurrency, restart recovery, independent Node + external multi-file model evaluation, PR write identity and rollback drill not certified.

## Evidence ledger
Append implementation commits, SHA, host receipts, CI IDs, rollback result, gate pass/fail and exact deployment identity here. Never mark any phase green without terminal machine evidence.

## 23 Oct 2026 IST — RC1 implementation receipts

### Implemented on **draft Gate E branch only**
- Security-reviewed hosted CI updates in `.github/workflows/validate.yml`: install Bubblewrap on ephemeral hosted job and **mandatory sandbox doctor before pytest**; no sandbox skip or network-isolation relaxation.
- Deterministic Marketing Brain thermal-guard unit fixture in `marketing/mac-brain/test_brain.py`, exercising the actual guard with synthetic coretemp sensor on hosts that have none.
- `workcell_runner.py`: active QA cancellation via marker polling, process-group termination on cancellation and timeout, shared deadline support, bounded output polling, and RLIMIT_AS cap of 512 MiB.
- `gate_e_runtime.py`: shared model/QA deadline propagation, cancellable sandbox calls, bounded Node subprocesses, incremental output checks, fsynced atomic final receipt; new live Python QA cancellation, exceeded-job-budget and output flooding tests.
- `gate_e_operator.py`: model calls obey shared deadline; nonblocking exclusive per-stage owner-only single-job capacity lock; no model-chosen host command/permission or source identity.
- **New candidate** `gate_e_queue.py`: SQLite WAL durable owner-enrolled job queue with transaction-safe single claim, idempotency keys, at-most-once dispatch, no replay of existing task dirs, and post-crash `orphaned_needs_review` quarantine preventing new claims until review. Six new offline security/recovery tests. This is **not** a production service and is **not** installed/activated.

### Peer test evidence
- At pinned code commit `d96f086577cd8b46f11bc75618a667c85a196bda` (Git object hashes individually verified against the GitHub blobs), **Dell 55/55 Gate E PASS** and **4/4 Marketing Brain PASS**, terminal receipt `693083ef-32f3-4c65-929b-f9d2f7eb83fd`, exit 0; **Mac 55/55 Gate E PASS** and **4/4 Marketing Brain PASS**, terminal receipt `241e3465-e184-45a9-bd2a-f3ab882f0cc3`, exit 0.
- After candidate queue and six tests at `ce417e0639e46ac9c92d2089764629cdf52a79bd`, **Dell 61/61 Gate E PASS**, terminal receipt `16946781-4f43-4cd9-a4b7-09c99fc712b0`, exit 0; **Mac 61/61 Gate E PASS**, receipt `43b43cfb-3389-4410-a6e5-94f8b7fff5bb`, exit 0. The two new files also matched exact GitHub blob hashes. These are **pinned-source equivalent local QA**, not a GitHub runner certification or a signed release artifact. Earlier completed Granite pilot was not re-run.
- Hosted Actions `39845526017`: `public-repository-safety` **PASS**, starter test workflow **FAIL** at the mandatory Bubblewrap doctor. Ubuntu hosted runner supplies `/usr/bin/bwrap` after apt installation but cannot configure its isolated network loopback: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. This is a **genuine security-environment gate**. Keep fail-closed; do not relax `--unshare-all` or disable the test. A protected isolated runner with a working namespace capability is required.

### Gate states after implementation
1. **Runtime hardening:** development tests PASS with new cancellation and limits; additional negative fault-injection of operator crashes and independent design review of hard memory/output budgets **still required**.
2. **CI/security:** **BLOCKED** by hosted runner network namespace, despite hosted public-source safety PASS and two-host local suite PASS. Registering an adequately isolated/ephemeral scoped self-hosted runner (or changing CI runner isolation) requires explicit security review and actual proof; do not expose the existing v6 worker's home to untrusted PR jobs.
3. **Real autonomy:** prior public offline Granite Python pilot PASS and synthetic Node path tests PASS. Independent real model-driven Node, multi-file and separate approved public repositories not completed. No retry of completed pilot.
4. **Canary/rollback:** **NOT DEPLOYED** while gates 1–3 and protected runner gate are open. Only isolated Dell/Mac QA copies and candidate durable queue source were used; the certified v6 controller and backups remain independent.
5. **Production release:** **NOT AUTHORIZED TO ACTIVATE under this gate policy yet** because mandatory evidence is missing, notwithstanding owner's conditional approval of the complete program. PR #13 remains **open/draft/unmerged**.

### Next controlled execution order
- Provision security-isolated CI and achieve full green mandatory checks; maintain no-network Bubblewrap semantics.
- Complete adversarial hard-kill/restart and cancellation/concurrency stress tests on the durable queue/operator with reviewable terminal receipts.
- Develop and certify independently evaluated, approved, non-sensitive real Node and multi-file Python model benchmarks; no automatic private source mounts or credential exposure.
- After gate signoff, run a Dell-only time-bounded candidate canary, collect monitoring and actual rollback proof, then produce versioned release evidence before production routing to Gate E. All deployment must preserve v6 hash/backup and historical receipts.

