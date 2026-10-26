# V4 Adapter — Dell limited shadow canary, 26 October 2026

**Owner request:** Deploy the recommended limited V4 release in idle lanes.  
**Outcome:** **STAGE 1 SHADOW DEPLOYED / SMOKE CERTIFIED. STAGE 2 LIVE WORKFLOW NOT AUTHORIZED/CERTIFIED.**  
**Owning repository:** `aarondash5-star/business-house-matrix`, source branch `feat/dev-toolyard-fidelity-execution-v4-20261026`, source commit `aba92cfd6f22a3dbe15bf5e567f939865bd6a3ea`.  
**Related work:** Dev Driver Issue #31; Driver PR #32; upstream Dev Brain Issue #2.

## Invariants

- Existing SSH gateway v6/six-lane service, shared `bhm-autonomy-controller.service`, `yard_execution_guard_v13.py`, original live adapter, actual registry, original task database, owner intake, sudo/root rights and project data **remain unchanged**.
- No full-controller replacement or restart. No new public socket, proxy, scheduler, DNS, credentials, spending, live tasks or production website changes.
- **Separate workcell**: `/var/lib/generic-linux-automator-exec/matrix-v4-shadow-canary-20261026` mode 0700, source and inventory snapshot mode 0600, not reachable from the live controller import path.
- Reused existing stdlib Python, owner-local V4 source, rootless Podman (preexisting `python:3.12-alpine` image), existing SSH authenticated lanes; zero new paid dependencies.

## Source and snapshot pins

- V4 `adapter_guard.py` and installed shadow alias `adapter_guard_v4.py` SHA256: `90f0a62cc6cfaf1458f0684363ffb9288c900ba0ade707908da0877447249e30`.
- V4 candidate `yard_auto_adapter_v1_patched.py` and installed **shadow-only** `yard_auto_adapter_v1.py` SHA256: `116f435279bbe7e0cc8281ab513e319926b846ab6ae25752bccc3fc6746fb773`.
- Snapshot of live 80,005-byte registry: `registry-snapshot.json`, SHA256 `76cd6bcdf3c947012a1b83e551cef4e4ed206aa0ba6975fd876715631e325dc8`. **No live registry truncation.**
- Original live adapter SHA256 `16f54c4ae1d97699786b649e84c94df2abb673b0682a20045d55399399217b79`.
- Original live controller SHA256 `e6834bb2f7765ee0aa26d215a566f70276e4f8c2c87c8730fc781c27dc778836`.

## Executed receipts and interpretation

| SSH job and lane | Exact observed result |
| --- | --- |
| `305e3670-220d-423f-865c-0e018c1e126c` Dell control | PASS read-only preflight: pinned V4 hashes, unchanged shared controller, 80,005-byte registry |
| `0b585e90-9a7f-4de3-951c-9cce1399d111` Dell development | **COMPLETED exit 0**: copied source, original adapter, approved QA tests, standards and registry into separate private shadow directory; integrity hashes/readback |
| `7050f1bc-448c-4edc-a63a-b11dddd6fad2` Dell development | **STALE RUNNING / NO TERMINAL RECEIPT** for first attempted Podman QA; never mark PASS, never replay the exact job. Host-side control/operations audits found **no container and no `shadow-test.log`**. Preserve gateway record for reconciliation; no live effect observed |
| `274e6eaf-a01a-45a5-9ccf-ab62f966eeac` Dell control | **STALE RUNNING / NO TERMINAL RECEIPT** for read-only process audit; separately inspected through healthy operations lane, do not replay |
| `ed231ae6-7435-4ee7-ad1c-b996e4661cb0` Dell operations | **COMPLETED exit 0** host-side audit: no Podman container, no test log, unchanged queued Driver build |
| `53e7afe7-fd55-4934-aa21-1f2da92a6663` Dell operations | **COMPLETED exit 0** read-only shadow-only admission: V4 guard accepted all **91 tools / 80,005 bytes**; original v1 rejected that identical snapshot; malicious `arbitrary_shell` denied; `dev_project_build/matrix_lane_driver_v1` inheritance returned `production_authorized:false`. **Simulated only**, no dispatch |
| `a1a4aad8-d0b1-423d-a698-77b5d650b02f` Dell operations | **FAILED exit 1** initial new rootless container regression: 62/63 tests passed, one fixture lacked `/usr/bin/git` in the minimal Alpine image. No V4 gate failure inferred; preserved genuine negative receipt |
| `5e0b1a4b-3774-4472-86c5-85f5c2ca5802` Dell operations | **COMPLETED exit 0, 63/63 tests PASS** in fresh rootless isolated container. Same read-only source mount, `--network=none`, `--read-only`, `--cap-drop=ALL`, `--security-opt=no-new-privileges`, 256 MiB, one CPU, 64 PIDs. Added only read-only host `/usr/bin/git` file as test fixture; no command execution privileges extended |
| `c91b901d-03a8-429a-b337-d58f943c3887` Dell operations | **COMPLETED exit 0** live source V1.3 guard regression **9/9 PASS**; original controller active, original hashes unchanged, 80,005-byte live registry unchanged, no separate V4 controller service |
 
63-test total: **52 V4 tests + 11 original adapter regressions**. The 9 V1.3 guard checks are additional. Passing tests of a detached candidate are not evidence of a production route, visual/product acceptance, or per-lane live dispatch.

## Live integration and promotion: NO-GO

The protected live `yard_auto_adapter_v1.py` still rejects 80,005 bytes under its 80,000-byte historical cap. The active shared controller cannot be changed through a shadow deployment. V4 candidate has no separately registered owner-authenticated action and no independently verified isolated controller/queue routing to send exactly one real workflow through it. **Do not call the offline `inherit()` result a live task.**

Driver build task `884cd886-943e-4ea8-93e8-9e5fcbaf100f` remained `queued`, `attempts=0`, `remote_job=null` on final readback and was not replayed. Existing owner/connector safety denial on live V4 promotion remains binding; do not patch the controller/registry, fake QA credentials or use raw worker shell as a substitute.

Dell three lanes were online at preflight; Mac remained offline. No Driver activated on Dell or Mac, no V4 live service installed.

**Exact remaining acceptance:** enroll a genuine owner-authenticated **separate** V4 controller route and project-isolated queue with actual prevention of shared-state writes, independent source pins, negative auth/cross-tenant/unknown-outcome/rollback tests and a reviewable release authorization. Then run a one-workflow real synthetic canary **without touching** the existing queued Driver task or shared controller. Production cutover requires a separate, explicit release and QA.

## Rollback and retention

Shadow-only rollback: after checking no active shadow process/container and recording terminal/uncertain receipts, remove or archive **only** `matrix-v4-shadow-canary-20261026`. Do not restore or edit the real controller, adapter registry, systemd units, task database, SSH queues, root privileges or original version-pinned source; they were not modified. Retain the immutable Git evidence and gateway receipts.

**Status words:** `SHADOW_VERIFIED`, `LIVE_CANARY_NOT_EXECUTED`, `PRODUCTION_NO_GO`. Do not register a Master event stating V4 is live; a shadow-only event, if recorded, must explicitly say nonproduction.
