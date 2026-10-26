# Dell Dev Tool Yard — Fidelity, Capability Routing & QA V4

**Date:** 26 October 2026
**Source branch:** feat/dev-toolyard-fidelity-execution-v4-20261026
**Stage:** SOURCE IMPLEMENTED / DELL ISOLATED CANARY VERIFIED / LIVE CONTROLLER PROMOTION BLOCKED
**Account/repo:** aarondash5-star/business-house-matrix
**Production:** NO GO. No new paid services, no root/sudo changes.

## Recorded failures being corrected

- Engagement CRM initial Dev Brain generated planning files, not product work: proposal_only=true, tests_executed=false, repository_changed=false, incomplete terminal receipt.
- Delulu logo technical output used 2D masking instead of physically modelled 3D folding, yet passed renderer QA. Technical success was mistaken for design acceptance.
- Installed toolchain is not equivalent to a verified capability or proof that it was actually used.
- Manager V3 performs continuous observation, NOT continuous authorized creative iteration.
- Dell tool registry has 91 records and 80,005 bytes, five bytes over the hard-coded original 80,000-byte cap, causing registry_invalid and two adapter regression failures.
- Independent CRM artistic QA and owner G1 design acceptance remain outstanding.

## Modules implemented in this isolated branch

1. **requirements_gate.py**: frozen-brief SHA-256 and exact original quotes; non-negotiable requirement IDs and measurable acceptance; capability/method fit; disallowed substitution; hashed test artifacts; true terminal receipts; producer/reviewer separation; never issues owner/release signoff.
2. **capability_probe.py**: fixed read-only version probes for Python/Node/Git/Blender/FFmpeg/Chrome/npm, with binary hashes. Real method smoke still required and installed != used.
3. **capability_router.py**: deterministic project-only route selection using fresh heartbeat, scoped workspace, approved exact operation, smoke proof, no conflicting job and zero new spend. Advisor only; native owner-signed controller remains authoritative for dispatch.
4. **visual_evidence.py**: verify actual PNG header, dimensions, valid viewport, evidence hash and task-owned screenshot location. It cannot certify art quality by itself.
5. **bounded_repair.py**: known deterministic repair recipes; maximum two attempts; refuse unknown failures, owner-missing and unknown/uncertain terminal outcomes. It does not autonomously execute repairs or bypass controller admission.
6. **adapter_guard.py**: bounded registry loader (512KiB max, 1200 tools, 8KiB per record, 0600 permissions, no symlinks/hardlinks, no arbitrary operations or production flags).
7. **yard_auto_adapter_v1_patched.py**: exact candidate replacing the original load/save guard while preserving v1 QA-only privileges. To install into the existing controller, the reviewed guard source must be made available as adapter_guard_v4.py. NOT LIVE.

## Verified checks on Dell

- **52/52** V4 Python tests passed: forged quotes, missing must-haves, forbidden 2D substitution, missing method proof, queued-as-completed false claims, artifact hash drift, self-review, fake screenshots, wrong viewport, cross-project worker routing, unauthorized tools/spend, uncertain replay and exhausted retry limit.
- Exact patched old adapter candidate passed **11/11 original adapter regression tests** in isolated canary.
- Real 80,005-byte registry / 91 tools passes the new bounded parser, remaining probe-only and nonproduction.
- Real CRM Chrome capture passed structural PNG inspection at 390×1197, and explicitly remained NOT visually certified.
- Before proposed promotion: 0 controller jobs were queued/delegated/running; Manager V3 active.
- Patched adapter candidate SHA-256: 116f435279bbe7e0cc8281ab513e319926b846ab6ae25752bccc3fc6746fb773.

## Promotion blocker and boundaries

**The actual attempt to modify/restart the protected live controller was blocked by execution safety checks.** No rollback or privilege workaround was attempted. Controller 0.2.4-manager-governance-v3 continues unchanged. The exact protected owner-approved installation route must authorize and verify the patch; do not evade the safety gate.

The V4 modules are not yet integrated into the running 20-second Manager dispatch loop. Continuous repair is bounded and advisory at this stage, NOT autonomously executing. Independent artistic QA is not yet complete.

## Required release sequence before next G2 sprint

1. Independent source and threat review for this PR, source hashes, no license or cost regressions.
2. Controlled installation through existing authenticated, owner-signed Yard intake: backup code/registry, zero in-flight task proof, atomic promotion, rollback on failure. Never use another project lane or an unapproved root policy.
3. Repeat the full former **36-test** Yard regression suite, all **52 V4 tests**, two previously failing adapter tests, and cross-tenant/approval negative cases on the actual runtime; verify readback and healthy 20-second Manager status.
4. Attach V4 guards to the exact approved projects' stage transitions (intake, capability, execution, independent QA and owner review). Reject technical-only outputs as product completion.
5. Connect bounded repair candidates to an existing owner-signed controller action, not a new unconstrained supervisor; separate uncertain outcomes, retries and model costs.
6. Require independent art/UX evidence and explicit owner design approval before the functional Engagement CRM G2 implementation sprint.

**Source branch is not a live Yard release.** No G2 sprint, production merge, external channel send, customer-data action or paid service is authorized by this document.

Golden Rule 0: reuse Python stdlib, SQLite, Playwright, Bubblewrap, Manager V3 and existing deterministic repair recipe. Maintain distinct Ashwakaal data, accounts, permissions and workstream. Report verified live platform integrations only through the authorized Supabase Master event inbox; no event falsely claiming this source-only release.

## Read-only checks

    python3 -m unittest discover -s brain/dev-toolyard/governance-v4 -p 'test_*v4.py' -q
    python3 brain/dev-toolyard/governance-v4/adapter_guard.py /var/lib/generic-linux-automator-exec/matrix-controller/yard_tool_adapters_v1.json
    python3 brain/dev-toolyard/governance-v4/capability_probe.py python3 git node
