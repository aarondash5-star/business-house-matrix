# Lane Driver V1 — governed integration attempt and release decision

**Time:** 2026-10-26 IST  
**Source branch:** `docs/lane-driver-six-lanes-20261026`; draft PR #32; Issue #31; upstream autonomy Issue #2.  
**Disposition:** **D1 source/sandbox QA PASS; D2 Dev Yard execution BLOCKED; D4–D5 NOT DEPLOYED.** Never call this six live drivers.

## Scope and reuse

One deterministic state/receipt follower for each existing `dell-linux` and `mac-linux` control, operations and development lane. Reused Python 3 stdlib, SQLite, existing certified SSH v6 receipts, controller V1.3 gate and Dell Tool Yard `dev_project_build` reviewed-patch runner. Source is original (no imported third-party code); no paid API, additional daemon, credential, root/sudo, network exposure or production publish.

## Source built

- `brain/dev-toolyard/lane-driver/lane_driver.py`
- `brain/dev-toolyard/lane-driver/test_lane_driver.py`
- Full source commit tested: `3c554057793a4555756a9529a9333e1c2f241c54`.
- Implements exact six lane identities, frozen owner-approved task envelope, SQLite atomic reservation / compare-and-swap version, immutable event hash chain, two-correction limit, stage advance, failed independent QA return, blocked unknown outcome, stale/source/foreign-host denials. It **does not** itself connect to owner-authenticated gateway receipts, start a worker or deploy a service.
- The synthetic unit-test harness injects `owner_admit`, `admit_action`, `verify_receipt` callbacks. Synthetic callbacks are **not** a replacement for real server-side authenticated transport or independent QA.

## Actual Dell QA

| Result | Terminal SSH receipt | Evidence |
| --- | --- | --- |
| First checkout/test | `01aa14e8-bc66-40db-a82e-2505ab04d8ac` | Syntax failed, wrapper initially exited 0 due `tail` masking; not counted |
| Syntax repair check | `215a03c7-a8af-48b2-8e30-2b75825b7893` | Syntax failed, exit 1, second extra bracket |
| Corrected latest source | `8055a07a-9265-4492-959e-2b8ca4b4b58c` | **26/26 Python tests PASS**, source SHA above, exit 0 |
| Independent rootless Podman | `546b87c7-9c87-45f0-a7b2-db75f0ed740c` | **26/26 PASS**, network disabled, source read-only, no-new-privileges, 256 MiB cap, exit 0 |

Negative scenarios tested: wrong lane/host, forged scope, owner/admission withheld, source checksum mismatch, malformed receipt, absent verifier, malicious command field, stage return to future stage, duplicate task, duplicate dispatch reservation, replay after terminal, stale stage CAS, unknown terminal, retry exhaustion, denied quality gate, event hash tampering, restart/reopen and deny root/spend/release fields.

## Governed Tool Yard enrollment (reviewed source, no live code promotion)

- Dell owner/intake staging completed through SSH receipt `19f5348c-4997-4025-8e92-38f4b0f0e450` (exit 0).
- Project `matrix_dev_manager`, action `dev_project_build`, exact **new** manifest `matrix_lane_driver_v1` and reviewed patch file with two source/tests, no reuse of unrelated manifest.
- Owner brief SHA256 `9126926e09f5caf6ab229771a9945d144d006569b9f0f3a10f17d393fdae7a5a`.
- Automation quality contract SHA256 `b6a7d5ec80aac6164c9c6b0bb0bcdadb755558a350b94eb9fc3e4f93e4b66f3f`.
- `project_registry.py check` approved exact scope and `quality_admission.py intake` returned `approved_intake`, `release_authorized:false`.
- Pre-change snapshots of registry and owner approval ledger retained in `~/matrix-controller/release-backups/lane-driver-intake-20261026/`. No controller source or SSH gateway modified.
- Controller task `884cd886-943e-4ea8-93e8-9e5fcbaf100f` created by owner-approved `controller.py submit`, SSH receipt `4ed52bff-0bcc-4d50-8379-7431d8e357da`, **queued** (not executable QA pass).
- An existing controller `tick` through the authenticated development lane, SSH receipt `38ddbbcd-6d8b-4a4e-8901-4886d8dbedc1`, **FAILED exit 1** before dispatch, with `yard_auto_adapter_v1.AdapterDenied: registry_invalid`. No rerun/bypass and no manual sandbox application. Job still queued/attempts=0 at readback.

## Actual blocker, not a Driver failure

- Live Dell adapter `yard_auto_adapter_v1.py` SHA256 `16f54c4ae1d97699786b649e84c94df2abb673b0682a20045d55399399217b79` limits adapter JSON registry to **80,000 bytes**. Existing registry was **80,005 bytes** (mode 0600). V1.3 independently pinned controller SHA256 `e6834bb2f7765ee0aa26d215a566f70276e4f8c2c87c8730fc781c27dc778836` remained active.
- An existing V4 audited guard is already authored at `brain/dev-toolyard/governance-v4/` on `feat/dev-toolyard-fidelity-execution-v4-20261026`; candidate `yard_auto_adapter_v1_patched.py` SHA256 `116f435279bbe7e0cc8281ab513e319926b846ab6ae25752bccc3fc6746fb773`, guard `adapter_guard.py` SHA256 `90f0a62cc6cfaf1458f0684363ffb9288c900ba0ade707908da0877447249e30`.
- Existing V4 offline candidate re-tested **52/52 PASS** (SSH receipt `d9674168-abbe-48c8-a0f8-e65f197e9a8c`, exit 0). **V4 is NOT active**. An earlier protected-host promotion attempt was denied by safety controls, documented in the V4 README. Do not bypass by directly replacing host files, truncating the registry, altering source pins, relaxing checks or using unrelated workers.

## Gate status

| Gate | Outcome |
| --- | --- |
| D0 reviewed scope/source | PASS for original code + documented constraints |
| D1 isolated functional/security QA | PASS 26/26 twice |
| D2 enrolled Dev Yard reviewed-patch execution | **BLOCKED** by live adapter registry-size defect |
| D3 independent authenticated receipt adapter | NOT IMPLEMENTED |
| D4 Dell 3 logical Drivers integrated/live | NOT DEPLOYED |
| D5 Mac 3 Drivers integrated/live | OFFLINE / NOT DEPLOYED |
| D6 six-lane certification / Master live event | NOT ELIGIBLE |

## Deterministic next dependency

1. Obtain a **legitimate already-authorized V4 adapter promotion path**, respecting prior tool denials, controller V1.3 SHA governance and exact rollback. Re-run preflight and all V4/previous adapter tests on actual runtime. No bypass.
2. Reconcile queued task `884cd886-943e-4ea8-93e8-9e5fcbaf100f` **before** any retry or release; verify whether it already ran; no duplicate manifest build.
3. Complete server-side fixed-function `lane_driver_transition` adapter which verifies authentic gateway/worker terminal receipts, provides owner/project/lane binding and uses existing signed task intake. Synthetic callbacks are insufficient. Preserve one task writer and nonreplay.
4. Independently certify and canary Dell control, operations and development lanes with real signed transport receipts, and separate watchdog coexistence, without production publishing.
5. Mac is offline at latest recorded check; its three lanes remain uncertified until online, enrollment and live gate tests. Confirm both hosts' status at action time.

**Rollback:** Preserve the queued task ID; do not delete queue or replay it. If reverting only the new owner-intake enrollment, verify the two config files' exact current versions and no concurrent writes, restore only `project_registry_v1.json` and `owner-intake-approvals-v1.json` from `release-backups/lane-driver-intake-20261026/` using staged atomic replacement, then verify old enrollment/readback. Leave the quality brief, patch, receipts and Git history intact for audit. If a future controller deploy is attempted, it requires separate verified source-pinned backup and rollback; no live controller change took place in this session.

**Status:** SOURCE_QA_VERIFIED / RUNTIME_BLOCKED. This document and the draft PR are not production or driver-service deployment receipts.
