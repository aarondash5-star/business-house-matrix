# Dell Dev Tool Yard — Universal Controller Execution Enforcement V1.3
Date: 2026-10-26 IST. Scope: owner-local Dell controller. Production publishing: NOT authorized.

## Changes verified
- Guard: yard_execution_guard_v13.py, manifest: yard_exec_bindings_v13.json (mode 0600).
- Registered controller routes: 13. Executable: 11. marketing_draft and video_preview still blocked.
- Action-specific execution sources: 20 SHA-256 pins including common QA/admission source.
- Controller submit and queued-task dispatch both call the V1.3 preflight. Governance manager import calls manager_preflight before import/reconcile.
- Hash drift raises ExecutionDenied, not a silent approve/retry. V1.2 adapter registry reconciliation now preserves source-drift quarantine until separate review.
- Automatic production promotion remains disabled, and production release still requires original owner/QA gate.
- No model-selected shell commands or credential gates relaxed. V6 and existing owner intake/release requirements preserved.

## Test evidence
- 2026-10-26: 36/36 local regression tests passed across execution guard, auto adapter, manager governance and QA standard.
- Independent rootless Podman/no-network/read-only sandbox: batch yard-v13-enforcement-independent-b-20261026, receipt sandbox-receipts/yard-v13-enforcement-independent-b-20261026.json. 8/8 tests passed.
- Earlier isolated attempt was unable to read /workspace because source directory mode was 0700; corrected permissions on a separate immutable QA batch. The failing receipt was preserved.
- Controller service bhm-autonomy-controller.service restarted and returned active, with no queued/delegated tasks at activation. Guarded manager and four representative action preflights passed.
- At test point 90 tool records, 90 probe-only accepted, 0 quarantined; 13 actions registered.
- Gate-negative tests include unknown actions, owner-release synthesis, altered source, forged ledger permission/production bits, and silent re-admission of a modified binary.

## Scope boundary: NOT universal external enforcement
- Only Dell controller-mediated actions are intercepted by this gate. A pinned source and syntax test do NOT certify its actual functional, visual or business outcomes.
- Standalone SSH/CLI, directly invoked tools, third-party connectors, delegated Dev worker internals and external systems are NOT universally intercepted or certified. Do not represent these as V1.3-compliant runtime execution.
- Direct SSH remains an authorized transport with its own existing shell gates. Extending enforcement across that transport requires gateway/worker-level audited mediation; do not claim this controller patch accomplishes it.
- Independent human creative approval and separate owner production approval remain mandatory. No new production Go Live, permissions or paid services enabled.

## Rollback and change management
Backup directory: release-backups/yard-execution-v13-20261026/
Contains pre-V1.3 controller.py, yard_auto_adapter_v1.py and registry.
On rollback: pause dispatch after inspecting running jobs, restore only the exact reviewed files, restore/reconcile registry with independent QA, restart bhm-autonomy-controller.service and verify the owner security policy. Do not roll back blindly during active jobs.
Any source change requires fresh SHA pin, independent QA and separately controlled review. Do not edit the manifest simply to make a drift error disappear.
Git feature-branch handover and merge require separate source provenance checks; this local installation is not proof of Git synchronization.
