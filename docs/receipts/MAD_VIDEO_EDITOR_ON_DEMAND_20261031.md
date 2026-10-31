# MAD Yard — Video Editor On-Demand Cutover Receipt

**Date:** 2026-10-31, Asia/Kolkata  
**Owner:** Business House AI Matrix / MAD Yard (Mac `KARAN`)  
**State:** VERIFIED LIVE — video-editor idle shutdown and automatic activation. This receipt records a *host change*, not a source deployment of any other application.

## Owner-requested change
"Make the video editor on demand service. Don't keep it running continuously."

## Before
- `mad-yard-executor-video_editor.service` was `enabled`, `active (running)`, type `simple`, PID 765.
- Original command: `/usr/bin/python3 -u .../mad_worker_bridge.py serve --worker video_editor`; polled queue every 12 seconds.
- Resource limits existed: `CPUQuota=60%`, `MemoryMax=805306368`, `Nice=12`, and process-specific protections.
- Existing lane ledger: 4 `blocked`, 5 `review_hold`, **zero ready/reserved tasks**. Outbox had 19 historical JSON files and was preserved. Neither customer data nor task manifests were printed.

## Change
1. Original service file was backed up under `/var/backups/mad-video-editor-20261031/original.service`; original SHA256 `2f2a0b30de45e61f82cfa8735bf305f1a75d7f245c0f4f2fb9b04cd2ab7d478f`.
2. Installed systemd drop-in `/etc/systemd/system/mad-yard-executor-video_editor.service.d/10-on-demand.conf`:
   - `Type=oneshot`, `RemainAfterExit=no`.
   - `ExecStart=/usr/bin/python3 -u .../mad_worker_bridge.py once --worker video_editor`.
   - `Restart=no`, `TimeoutStartSec=15min`.
   - Retained original `User`, sandboxing and resource limits.
3. Disabled and stopped the persistent video-editor service: `disabled`, `inactive (dead)`, `MainPID=0`.
4. Enabled `mad-yard-executor-video_editor.path`, using `PathChanged` on the existing video editor driver outbox directory. New task envelope creation wakes one short-lived worker invocation.
5. Enabled `mad-yard-executor-video_editor.timer`: `OnActiveSec=5min`, `OnUnitInactiveSec=5min`; low-frequency fallback for missed wakeups and retained work, **not** a persistent processing daemon.
6. Backed up `mad_manager_bridge.py` to `/var/backups/mad-video-editor-20261031/mad_manager_bridge.py.original`, then added an exact narrow registry condition that reports `service_state=on_demand`, `route_enabled=true` when the watcher and fallback timer are active. No unrelated MAD tool statuses were changed.

## Verification
- `systemd-analyze verify`: PASS.
- Direct one-shot idle invocation: `Result=success`, `ExecMainStatus=0`, returned to `inactive` without a resident process.
- Non-JSON synthetic file creation/removal in the watched directory caused fresh successful service invocations through the `.path` watcher. Temporary file removed; no job created or claimed.
- After the smoke test: `MainPID=0`, `inactive (dead)`; watcher `active (waiting)`; recovery timer `active`.
- Manager fresh-process registry returned `on_demand` and `route_enabled=true`.
- Existing `mad-yard-lane-driver.service`, `mad-yard-manager.service`, `mad-yard-autonomy-production.service` remained `active`.
- Thermal readings around the cutover: CPU TC0F approximately 70.5–75.2°C; after path smoke ~74.2°C. **No actual rendering or sustained heat/load test**. Existing render heat guard remains in source.
- Trigger smoke receipt: control task `523bbc4deb464d99a7b1d8443d7c6251`.
- Initial source + backup staging receipt: `9eaff0716b9f4bbf8d06b38a03a63c82`.
- Cutover receipt: `aa693d232a4d4e00adea12f951779e1f`.
- Manager patch receipt: `103a15e1df6e46508a20d2ec93db0316`.

## Caveats and next QA
- One `once` invocation processes at most one eligible envelope. The `.path` watcher handles new queue activity; 5-minute timer handles missed changes and outstanding queue work. High-concurrency backlog throughput was not tested.
- The manager/dashboard process may cache the old inventory module until its normal reload/restart, although the fresh CLI registry test passes. No unrelated service was restarted in this change.
- Confirm eventual end-to-end genuine licensed video task dispatch and thermal-safe render in a separate approved test. Do **not** bypass 70°C render hold to force a test.
- The Mac's broader browser-related overheating remains unresolved.

## Rollback, only if separately authorized
1. Disable and stop `mad-yard-executor-video_editor.path` and `.timer`.
2. Remove the service drop-in `10-on-demand.conf`, daemon-reload and verify original unit parameters.
3. Restore the verified backed-up `mad_manager_bridge.py` if still compatible with newer changes (never overwrite concurrent edits blindly).
4. Re-enable original service only if thermal and operations safety allow; do not automatically restart always-on polling during an overheating incident.

**No advertising, publication, WP changes, credential copying, cloud provisioning, paid inference, or unrelated MAD service modification.**
