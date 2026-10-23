# Dev Matrix Unified Runtime — legacy shutdown and smoke checkpoint

**Date:** 2026-10-23 UTC. **Owner instruction:** stop the old Dev Brain, upgrade through the existing SSH CLI, integrate one unified Dev service, then smoke test.

## Verified actions

- Connected via existing owner-authorized Generic Linux SSH operations lane to Dell; control lane remained stale. Mac was offline at preflight and could not provide independent certification.
- Inspected live `brain.py serve` (PID `1739822`) and separately running certified v6 `matrix-controller/controller.py serve`.
- Verified the Dev Brain had **no currently queued or running jobs**; historic `cancelled queued` was only a cancelled record with a stage field and did not indicate unfinished work. The first safety guard therefore aborted without touching any processes; after parsing the status column correctly, the controlled stop succeeded.
- **Retired old proposal-only Dev Brain** with SIGTERM. Terminal receipt `3775124b-7d26-4bac-90f8-991650a1e3d7`: `STOP_PREFLIGHT NO_ACTIVE_JOBS`, `LEGACY_DEV_BRAIN STOPPED`, `CERTIFIED_V6_CONTROLLER active`, exit 0.
- Performed real `controller.py selftest` after shutdown: **6/6 PASS**, covering persistent queue, idempotency, blocked production route, isolation, privacy validation, conservative recovery. Terminal receipt `dce5291e-1f95-49d5-81c0-0db19a223803`, exit 0.
- Controller service remained active; original `controller.py` SHA256 **`b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`** was unchanged. No historical DB, credentials, bridges, workers or production services were deleted.

## What did NOT happen

**Unified Dev runtime is not installed or activated.** The candidate source on `feat/dev-universal-dynamic-intake-20261023` was never fully certified: original negative QA 13/14, identity bug fixed but post-fix rerun denied by platform safety checks, candidate CLI/bootstrap creation blocked, source diff/acceptance gate missing, and no multi-file external-repository success or rollback canary. None of those denials was bypassed by using SSH or another tool.

**Important current gap:** The active v6 controller still advertises `dev_proposal` even though its separate `brain.py serve` consumer was shut down. Do **not** send new `dev_proposal` tasks: they could remain unprocessed. The preserved controller's other certified capabilities remain available subject to their exact task envelopes. No Andaz coding execution is claimed.

## Required to fulfill unified release

1. Get legitimate clearance for the denied isolated CLI/bootstrap and test process through the relevant connector/security review process. Do not bypass.
2. Fix candidate's missing requirement to prove actual modified source before `review_ready`; rerun original negative and post-fix QA on exact source.
3. Certify real multi-file coding and independent trusted tests inside disposable compute, project isolation, cancellation, crash-recovery and resource caps.
4. Connect one authenticated general Dev intake to the replacement Brain runtime, then test user-to-Brain-to-worker and worker-to-QA-to-owner receipts. Preserve caller identity, project permissions and idempotency.
5. Run isolated restricted canary, Mac/independent QA and full rollback drill before touching v6 routing. Promote only after independent release signoff.

## Safe current operating state

**Old proposal consumer: stopped. Existing certified controller: active, 6/6 smoke PASS, unchanged. Unified candidate: source-only, NO-GO.** Reinstating the original `brain.py serve` process should be considered only after explicit owner decision or approved rollback if old proposal processing is required; never claim it was replaced by the new runtime.

Sources: `tasks/dev-general-autonomy/OWNER_DIRECTIVE_2026-10-23.md`, `docs/handoffs/DEV_MATRIX_UNIVERSAL_CERTIFICATION_DECISION_20261023.md`, GitHub Issue #2, draft Gate E PR #13.
