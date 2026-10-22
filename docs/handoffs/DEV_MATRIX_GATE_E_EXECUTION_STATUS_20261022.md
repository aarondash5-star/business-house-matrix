# Business House Matrix — Gate E execution handover and QA status

**Started:** 22 Oct 2026 IST; continuation of certified scoped v6.  
**Branch:** `feat/dev-matrix-gate-e-general-runtime-20261022`  
**Review:** [Draft PR #13](https://github.com/aarondash5-star/business-house-matrix/pull/13), base `release/dev-operator-scoped-v6-security-20261022`.  
**Decision (updated 23 Oct 2026 IST):** **DEVELOPMENT CANDIDATE / NOT RELEASE-CERTIFIED.** Real Granite Python pilot and full Dell/Mac 52/52 regression runs passed, including active subprocess cancellation. Hosted CI and broader durable autonomy gates remain open. Do not merge into v6.

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
- [x] Dell final 52/52 v6+Gate E suite passed. [x] Mac independently passed 52/52 in an isolated public checkout on 23 Oct; prior platform block was respected and its old checkout preserved.
- [ ] Run real model-driven Python and Node benchmarks on externally approved, non-sensitive repositories beyond the committed fixture; independent evaluator/QA required.
- [x] Proved cancellation while a bounded child process was running, including process-group reaping, on Dell and Mac. [ ] Active full model/QA-run receipt cancellation, workload concurrency cap, crash/hard-kill recovery still OPEN.
- [ ] Add independent multi-repository enrollment registry, secret-free source transport and nontrivial multi-file patch benchmark. No private Pine/Moksha mounts.
- [ ] Verify GitHub-hosted/self-hosted CI with explicit resource budget, project-scoped PR identity and review gates; do not allow automatic merge/publish.
- [ ] Integrate staged operator with existing durable v6 controller **only after** successful Gate E certification, documented migration plan and independently verified rollback.
- [ ] Perform release signoff with hashes, read-only Mac/Dell parity, negative scope tests and a versioned Gate E source release.

## 23 October 2026 — Independent continuation evidence

**Status:** Draft Gate E development candidate, **not release certified**. No merge, deployment, model push, publishing, spending, permission changes or changes to v6 controller.

**Peer QA / exact receipts:**
- Mac independently checked out original PR head f2d1f9d670c9eb40fffb6a723048822ff8a62aa8, 52/52 tests PASS, exit 0 (receipt 4a3e5e5e-8ff0-4eaf-9d47-933a345e9df7). Mac's preexisting stage at 0559f27... was not replaced.
- Dell live child cancellation: receipt e809728a-3f79-4578-8897-58a97660419f, exit 0. Mac live child cancellation: receipt b1d9e98d-4b3d-4e16-b6e9-045ca53ea951, exit 0. Both started a real child, observed its PID marker before requesting cancellation, received Cancelled, and verified the process was reaped. This is narrower than durable model/QA job cancellation.
- After narrowly scoped CI corrections, both hosts tested code commit 2829f9fcf3c9631adba9f14402b4642324df09e0 from separate isolated public clones. Dell receipt 12361710-3507-48b9-a024-1f373a621d09: 52/52 tests and 145-file public source safety PASS, exit 0. Mac receipt 088b7daf-3901-4118-8fe3-1a5d1feedc6c: same 52/52 and 145-file safety PASS, exit 0. No v6 files, permissions or existing stages were modified to achieve these results.
- Dell control receipt 37fde806-bee0-4a9f-acfd-251ebf333c43: certified v6 controller ACTIVE; controller.py SHA256 unchanged at b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e. Existing backup directory matrix-controller/release-backup-dev-mcp-20261022 present. Temporary original Gate E pilot service is inactive with Result=success and Restart=no. No rollback drill attempted.

**Hosted CI blockers and corrections:**
- PR #13 initial Actions run 39834880471 failed public-repository-safety because the scanner matched a private-key *pattern inside the policy module's own security regex*, not an actual disclosed secret. Gate E branch scanner now suppresses only that exact regex token if the **entire audited policy Git blob** is unchanged (blob a45de0dfdbfb86313e0c15bf272cadf647a78f98); any change restores full scanning, fail-closed. Certified v6 policy source is unchanged.
- General pytest discovery previously failed importing the benchmark output, intentionally absent until model generation. The branch test wrapper now skips the six benchmark tests only in checkouts without the generated source. Inside the enrolled workcell generated source exists and the tests run. The immutable enrolled source baseline 265c3aab7931e1f67bcea9dbe27d5f602d600cd3 and original independent benchmark test fixture at that pinned base remain unchanged.
- Actions run 39836254364: **public-repository-safety PASS**. Hosted **starter-tests FAIL**, summary 22 failed, 118 passed, 6 skipped, 66 passing subtests. The hosted runner lacks /usr/bin/bwrap, causing the security sandbox suites to fail closed; a separate marketing resource guard is also environment-sensitive. Do not mark full hosted CI green, weaken isolation tests or bypass runner security.
- These code changes are confined to the **draft feature branch**, not v6. The present handover commit only updates documentation.

**Open release gates:** (1) independently secure and certify Bubblewrap-capable CI; (2) real Node and nontrivial model benchmarks in separately approved non-sensitive repositories, without replaying completed Granite task or bypassing rejected JS write; (3) concurrency limits, durable receipts and restart/crash recovery including full model/QA cancellation; (4) multi-project enrollment and transport, controlled PR identity and verified rollback drill; (5) explicit release signoff. GitHub PR #13 remains DRAFT; v6 remains frozen and working. All prior receipts and historical needs_review jobs must be retained.

**Next-chat starting instruction:** Read this handover and draft PR #13. Dell/Mac 52/52 peer QA, active child cancellation and source safety PASS. Resume only remaining CI, multi-project/model benchmarks, durable recovery, scoped PR identity and release signoff. Preserve v6 and completed Granite receipt. No merge, publish, spending or permission changes without explicit authorization.

## 23 October 2026 — Complete runtime verification audit (follow-up)

**Certification decision: NO-GO for a complete Gate E runtime release.** This audit verified what is currently implemented, without assuming that tests prove missing durability or autonomy functions.

### Live evidence
- GitHub PR #13 remains **open/draft/unmerged**, base `release/dev-operator-scoped-v6-security-20261022`; observed head before this documentation update: `76d81c4740a0195600bcb8c594190c59c812db1d` (the immediately prior changes after `2829f9fc...` affected only documentation).
- Dell and Mac generic SSH heartbeat authenticated and online in this verification. The Dell bridge showed intermittent scheduling/availability delays; do not claim permanent transport stability.
- Dell controller **active**, verified SHA-256 `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`; historical backup directory still exists. No controller or permissions modification.
- Dell real Granite pilot: directly re-read receipt `~/matrix-gate-e-stage-20261022/runs/gate-e-public-python-parse/receipt.json`. It confirms one model attempt, isolated QA six assertions PASS, `verified_local_review`, local Git commit `13cdd560f19e3e9031e0f2ead2dc81958005f85c`, `published=false`, `pushed=false`. Operator `status` returns same terminal status; **never replay this job**. Dell Ollama system service is `active`, installed model list includes `granite4:3b`; binary and required `/usr/bin/node`/`/usr/bin/bwrap` exist. The old pilot systemd unit is inactive and reports success/no restart.
- Mac standalone independent Bubblewrap doctor **PASS** (`home_hidden`, `foreign_project_hidden`, `host_service_hidden`, `net_namespace`, `workspace_writable`). Invalid owner enrollment was rejected with `PolicyError` in the same isolated inspection. Receipt `eb39888f-986d-4d1b-bad8-590d8906dd4f`, exit 0.
- Official offline Gate E CI entrypoint **PASS** on both existing isolated checkout workspaces, without network clone: Mac source `2829f9fcf3c9631adba9f14402b4642324df09e0`: **52/52 PASS**, exit 0, receipt `5b01e724-c44e-4cad-b3a5-705ecd290d23`; Dell stage `b7ede29f33fd9ec812f5b686e6d58dad191f4218`: **52/52 PASS**, exit 0, receipt `ae3602c5-ed6d-46dc-a562-0dacd42a1f72`. Note Dell stage is older; **both** hosts also independently passed 52/52 at code SHA `2829f9fc...` as previously documented.
- Earlier verified live cancellation of bounded child subprocesses on both hosts remains valid. No owner-enrolled production/full-model job was cancelled during this audit.

### Current blockers and design gaps found
1. **Hosted CI failed:** latest observed GitHub Actions run `39837131660` completed with source-safety **PASS**, starter-tests **FAIL** (`22 failed, 118 passed, 6 skipped, 66 passing subtests`). Hosted runner lacks `/usr/bin/bwrap`; one marketing resource-guard assertion also fails. No weakening of sandbox policy or permission/setup change was performed.
2. **Real multi-repo/general coding benchmark absent:** current approved Gate E operator enrolls only a public Python parse fixture. Real independently evaluated model-driven Node, multi-file and external-repository benchmarks have not passed. Synthetic Node tests do not replace model-driven proof.
3. **Python QA cancellation gap:** Gate E calls `workcell_runner.isolated()` for Python QA; this runs `subprocess.run(..., timeout=40)` without observing the owner cancel marker mid-QA. Model calls and Node QA use the cancellable `bounded()` path, but whole-job active Python QA cancellation has not been certified.
4. **Non-hard total deadline:** the `TIME_BUDGET=240` budget is checked between attempts, not enforced continuously across all model, worker, and review stages. The `bounded()` output-size check occurs after `communicate()` buffers output, so the posthoc limit is not a streaming memory bound. Both require bounded negative tests/remediation before full autonomy certification.
5. **Durability/controller integration absent:** no global concurrency controller, durable crash/hard-kill restart state machine, generalized registry/secret-free source transport, scoped PR write identity, or executed rollback drill. A missing receipt is `needs_review`; it is not an autonomously resumed task.
6. **Git source transport observation:** attempted exact-head fresh clones on both hosts stalled during `git clone` / `index-pack`. SSH jobs `28b6d651-fdc2-46ba-8309-952dfb677cf0` (Dell) and `464d490f-b40e-4e12-a139-06fe2b6dae41` (Mac) timed out with remote outcome uncertain, **before the QA script started**. Read-only inspection showed no cloned HEAD or test.log, only ongoing clone/index-pack, so do not mislabel as test failures or successful head rechecks. Explicitly targeted the new stuck verification child processes for termination; existing old checkouts, v6 services, permissions and rollout remained intact. Prior `2829f9fc...` full code-parity remains the applicable last successful cross-host source QA.

### Gate E disposition
- **Verified:** immutable public Python fixture, model-generated local source, trusted QA, no-network Bubblewrap workcells, local Python/Node integration tests, negative scope handling, bounded child-process cancellation, and unchanged certified v6.
- **Not certified:** hosted/self-hosted green CI, ongoing source transport stability, general multi-project model work, whole-job cancellation and resource hard caps, concurrency/crash recovery, controller integration, PR write approvals, rollback drill and release signoff.
- **Action:** retain PR #13 as draft. First fix hosted runner environment and runtime hard caps/cancellation, then certify independent real Node/Python multi-project benchmarks and durable recovery. Do not merge, publish, spend or change permissions as part of verification.

