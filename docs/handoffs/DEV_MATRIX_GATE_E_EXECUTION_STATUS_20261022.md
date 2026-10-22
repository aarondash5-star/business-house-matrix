# Business House Matrix — Gate E execution handover and QA status

**Started:** 22 Oct 2026 IST; continuation of certified scoped v6.  
**Branch:** `feat/dev-matrix-gate-e-general-runtime-20261022`  
**Review:** [Draft PR #13](https://github.com/aarondash5-star/business-house-matrix/pull/13), base `release/dev-operator-scoped-v6-security-20261022`.  
**Decision:** **DEVELOPMENT CANDIDATE / NOT RELEASE-CERTIFIED.** Successful real Granite Python pilot and Dell 52/52 regression run confirmed; Mac final QA and wider autonomy gates remain open. Do not merge into v6.

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
5. After new operator/pilot/CI changes, Dell reran full branch tests at `b7ede29f33fd9ec812f5b686e6d58dad191f4218`: **52/52 PASS**, exit 0, terminal receipt `97cad3bc-23d1-4569-9b21-e3aa422a7bea`. v6 controller unchanged and active. Mac final peer QA remains OPEN. No hosted GitHub CI pass claimed.

## Bounded real offline-model pilot — independently verified PASS

- Dell stage: `~/matrix-gate-e-stage-20261022/repo`, distinct from certified v6.
- Dell preflight verified enrolled base SHA, trusted tests, model binary, service active and unchanged v6 controller checksum `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`.
- Owner-scope transient `systemd-run --user` launch of `gate_e_operator.py gate-e-public-python-parse run` succeeded, terminal receipt `0f66c1e2-b81b-420d-80e0-17e0dcbf0d26`, exit 0. Temporary unit `matrix-gate-e-public-python-20261022.service` is capped to `RuntimeMaxSec=390`, `MemoryMax=1G`, `CPUQuota=100%`, `NoNewPrivileges=yes`.
- Initial inspection found the task in progress. Later read-only check **verified terminal success**: status receipt `8ac24391-1cea-4bed-b436-69af31831ef3`, completed `2026-10-22T18:40:58Z`, `status=verified_local_review`, 1 Granite attempt, independent Python QA **6/6 PASS**, Bubblewrap probe PASS, `published=false`, `pushed=false`. Exact local review commit `13cdd560f19e3e9031e0f2ead2dc81958005f85c`. Temporary unit finished with `Result=success`, exit 0, inactive.
- At 2026-10-22 18:41 UTC, Dell bridge heartbeat became **offline/stale** (~74 seconds), although Mac remained online. This was transient bridge instability, **not** pilot failure; subsequent terminal receipt confirms the pilot succeeded. Do not replay the completed task.
- Dell briefly returned online at 18:43 UTC, then heartbeat again became stale by 18:44 UTC (~63 seconds). That status command subsequently completed and confirmed the task's success. This is **intermittent bridge availability**, with root cause unverified. The approved temporary systemd unit retains its automatic RuntimeMaxSec safety cap; do not dispatch a duplicate job or modify bridge settings merely to obtain a status.
- The temporary unit has a maximum runtime and no restart/autostart policy was configured by this Gate E workflow.
- A proposed separate JavaScript public benchmark file was blocked during connector write by platform safety checks; **not added**. The existing isolated Node test suite still covers Node capability.

## Certified v6 remains untouched

- Preflight `systemctl --user is-active bhm-autonomy-controller.service` returned `active`.
- Controller SHA unchanged at `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`.
- No replacement of `~/matrix-controller/controller.py`, no release-branch merge, no Mac/Dell SSH/root/network/system permissions change, no package installation or spending, no model Git push/publish. Keep all v5/v6 backups, old test receipts and 11 `needs_review` historical tasks.
- The new feature branch is a direct descendant of the certified scoped v6 release; its draft PR does **not** target diverged `main`.

## Remaining Gate E release gates

- [x] Dell pilot receipt and local commit verified. [ ] Investigate intermittent Dell bridge heartbeats separately. Never replay completed task.
- [x] Dell final 52/52 v6+Gate E suite passed. [ ] Mac final peer rerun still pending; do not bypass prior security checks.
- [ ] Run real model-driven Python and Node benchmarks on externally approved, non-sensitive repositories beyond the committed fixture; independent evaluator/QA required.
- [ ] Independently prove bounded per-job cancel while a model or QA subprocess is actually active, workload concurrency cap, crash and hard-kill recovery.
- [ ] Add independent multi-repository enrollment registry, secret-free source transport and nontrivial multi-file patch benchmark. No private Pine/Moksha mounts.
- [ ] Verify GitHub-hosted/self-hosted CI with explicit resource budget, project-scoped PR identity and review gates; do not allow automatic merge/publish.
- [ ] Integrate staged operator with existing durable v6 controller **only after** successful Gate E certification, documented migration plan and independently verified rollback.
- [ ] Perform release signoff with hashes, read-only Mac/Dell parity, negative scope tests and a versioned Gate E source release.

**Next-chat starting instruction:** Read this handover and draft PR #13. Resume Gate E with Mac final QA and remaining certification gates; preserve certified v6 and do not replay the completed Granite pilot. No merge, publishing, spending or permission changes without explicit authorization.
