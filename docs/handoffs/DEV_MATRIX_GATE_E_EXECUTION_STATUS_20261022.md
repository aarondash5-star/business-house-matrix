# Business House Matrix — Gate E execution handover and QA status

**Started:** 22 Oct 2026 IST; continuation of certified scoped v6.  
**Branch:** `feat/dev-matrix-gate-e-general-runtime-20261022`  
**Review:** [Draft PR #13](https://github.com/aarondash5-star/business-house-matrix/pull/13), base `release/dev-operator-scoped-v6-security-20261022`.  
**Decision:** **DEVELOPMENT CANDIDATE / NOT RELEASE-CERTIFIED.** Do not merge into v6 or claim full autonomous Dev release.

## What was implemented on isolated branch

- Additive `brain/dev-operator/gate_e_runtime.py`: owner-enrolled hash-pinned public-repository baseline; exact source/test/context paths; deny symlinks and submodules; bounded source/manifest sizes; no dynamically chosen host commands.
- Reuse certified `protocol.py`, `workcell_runner.py`, `agent_loop.local_review` without changing their v6 files.
- Isolated Python `unittest` using existing Bubblewrap worker and independent tests from immutable source; Node built-in `node --check` / `node --test` inside a no-network Bubblewrap capsule using existing `/usr/bin/node`. No npm dependency installation.
- Disposable **new workcell on every attempt**. This fixes a test-discovered Python bytecode cache invalidation flaw where two same-sized patches could run against stale `.pyc` and create false negatives.
- 3-attempt, no-replay/idempotent task directory; negative tests for credential source, repository identity, test mutation, forbidden enrollment, symlink baseline, source parity, failed isolated QA, process group timeout and cancellation. Failed or ambiguous jobs require manual review.
- Owner-only `gate_e_operator.py` CLI: `run`, `status`, `cancel`, only manifest files matching enrolled task prefix. Offline `granite4:3b` via existing `matrix-pi-local` with `--no-tools --no-mcp --offline`. No remote publishing or model-selected filesystem paths. A cancellation request is not treated as completed until a terminal receipt confirms it.
- Self-hosted offline regression entrypoint `scripts/ci_dev_matrix_gate_e.sh` (no hosted CI pass claimed).
- Separate public immutable Python benchmark `benchmarks/gate_e/README.md` and committed trusted `tests/test_gate_e_parse_pairs.py`, enrolled at exact pre-manifest Git commit `265c3aab7931e1f67bcea9dbe27d5f602d600cd3`.

## Verified testing

1. Dell initial full run **48/52**; Mac initial **48/52**. Failures exposed repeated policy module loading and class identity mismatch. Fixed with a cached module.
2. Mac follow-up **51/52**; Dell found the same one remaining failure. First QA attempt left timestamp/size-equivalent Python bytecode; second changed source but inherited cached result. Fixed by generating a pristine immutable workspace on **each** repair attempt.
3. Dell full v6+Gate E suite **52/52 PASS**, exit 0, read-only development-lane terminal receipt `2e1f2907-4655-43de-b6e9-9dc38050e3bd`, against code commit `c386324db88cfe1129c63f91d36fc151ebd139db`. Includes independent real Python and Node JS local-only review end-to-end tests, repeated repair case, malicious path rejection, and worker cancellation/timeout tests.
4. The subsequent Mac final rerun was **blocked by platform safety checks**. Do not bypass; Mac peer certification remains OPEN.
5. Code evolved after the 52/52 pass: output limits, operator CLI, enrolled public pilot, offline CI entrypoint. Therefore **fresh full-suite QA is required on the final branch HEAD** before any release. No claim that GitHub-hosted CI ran.

## Bounded real offline-model pilot and live status caution

- Dell stage: `~/matrix-gate-e-stage-20261022/repo`, distinct from certified v6.
- Dell preflight verified enrolled base SHA, trusted tests, model binary, service active and unchanged v6 controller checksum `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`.
- Owner-scope transient `systemd-run --user` launch of `gate_e_operator.py gate-e-public-python-parse run` succeeded, terminal receipt `0f66c1e2-b81b-420d-80e0-17e0dcbf0d26`, exit 0. Temporary unit `matrix-gate-e-public-python-20261022.service` is capped to `RuntimeMaxSec=390`, `MemoryMax=1G`, `CPUQuota=100%`, `NoNewPrivileges=yes`.
- First read-only inspection saw service active and task directory present but **no terminal task receipt yet** (reported `needs_review`, which can mean in-progress/unknown, not definitive task failure).
- At 2026-10-22 18:41 UTC, Dell bridge heartbeat became **offline/stale** (~74 seconds), although Mac remained online. Do not infer pilot success or failure; its final result is **UNKNOWN** until Dell reconnects and terminal receipt + service status can be read. Do not replay the same task.
- The temporary unit has a maximum runtime and no restart/autostart policy was configured by this Gate E workflow.
- A proposed separate JavaScript public benchmark file was blocked during connector write by platform safety checks; **not added**. The existing isolated Node test suite still covers Node capability.

## Certified v6 remains untouched

- Preflight `systemctl --user is-active bhm-autonomy-controller.service` returned `active`.
- Controller SHA unchanged at `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`.
- No replacement of `~/matrix-controller/controller.py`, no release-branch merge, no Mac/Dell SSH/root/network/system permissions change, no package installation or spending, no model Git push/publish. Keep all v5/v6 backups, old test receipts and 11 `needs_review` historical tasks.
- The new feature branch is a direct descendant of the certified scoped v6 release; its draft PR does **not** target diverged `main`.

## Remaining Gate E release gates

- [ ] Read Dell host state; assess SSH stale heartbeat without destructive recovery. Locate transient unit terminal code and `~/matrix-gate-e-stage-20261022/runs/gate-e-public-python-parse/receipt.json`; check local commit if successful. **No blind replay**.
- [ ] Rerun current full branch HEAD Python/Node + v6 tests on Dell and Mac; Mac prior security check cannot be bypassed.
- [ ] Run real model-driven Python and Node benchmarks on externally approved, non-sensitive repositories beyond the committed fixture; independent evaluator/QA required.
- [ ] Independently prove bounded per-job cancel while a model or QA subprocess is actually active, workload concurrency cap, crash and hard-kill recovery.
- [ ] Add independent multi-repository enrollment registry, secret-free source transport and nontrivial multi-file patch benchmark. No private Pine/Moksha mounts.
- [ ] Verify GitHub-hosted/self-hosted CI with explicit resource budget, project-scoped PR identity and review gates; do not allow automatic merge/publish.
- [ ] Integrate staged operator with existing durable v6 controller **only after** successful Gate E certification, documented migration plan and independently verified rollback.
- [ ] Perform release signoff with hashes, read-only Mac/Dell parity, negative scope tests and a versioned Gate E source release.

**Next-chat starting instruction:** Read this document and draft PR #13; inspect Dell only if reachable, do not replay running/ambiguous tasks, preserve certified v6. Gate E remains a candidate until all outstanding items are proven.
