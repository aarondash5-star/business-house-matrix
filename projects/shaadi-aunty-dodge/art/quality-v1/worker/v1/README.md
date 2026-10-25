# Shaadi Aunty Art Worker v1 — Dell handover
26 October 2026. Owner instructed: enroll and resume the dedicated Blender/OpenCode art worker. Art quality remains **FAIL SAD-VISUAL-QUALITY-V1**. The source on this branch is only a **review copy** of the running Dell worker.

## Actual deployed system
- Dell owner-local manager at `~/matrix-controller/controller.py` v0.2.4. Its `manager_governance_v3.py` now reads art-worker receipts from `~/matrix-controller/art-worker-v1/latest.json`, exposing `governance_v3.art_worker_v1`. The integration preserves existing release gates and passed 26 regression tests.
- Persistent systemd user timer `bhm-shaadi-art-worker.timer` enabled, polling every approximately **2 minutes** for queued work. Fixed-recipe one-shot service `bhm-shaadi-art-worker.service`; local SQLite queue `art-worker-v1/jobs.sqlite3`; no automatic retry on an ambiguous/crashed job. 5GB RAM and 170% CPU caps, no privileges, restricted writable paths.
- Project-scoped Blender launcher `art/quality-v1/tools/run_blender_4_5_lts.sh` uses Blender 4.5.15 LTS with MPFB2; OS Blender 4.0.2 retained.
- No arbitrary model-generated shell/code, paid APIs, production Git merge or publishing. The model is advisory-only. Any item marked `needs_review` requires an audited intervention, not automatic approval.

## Results verified
- New editable rig: `iterations/20261026-art-worker-v1/sharma_aunty_art_rig_wip_v1.blend`, SHA256 `3233ce0bda132dff9e21f333429ca6e2302b04d240b250b16b5c0a3422c8b09c`. The prior source remains untouched.
- Technical morphs generated: `Blink`, `Smile`, `JawOpen`. Bone animation actions present in actual GLB: `Idle`, `Walk`, `Question`, `DodgeReaction`.
- Unapproved GLB export: `iterations/20261026-art-worker-v1/sharma_aunty_art_rig_wip_v1.glb`, 9,153,404 bytes; SHA256 `5a2a1d8c52dcfe6499b232f7f823015b7798a5ee360384980d2e36bff2ac68cc`. Actual glTF JSON inspection confirmed all four animation clips and three morph target names, but no final gameplay animation certification.
- Art-worker `render_study` completed, with actual 480×672 PNGs: neutral front, three-quarter, smiling face, blink; alpha/pixel bounds checked. Still visually far below the owner-pinned references. No independent creative approval.
- OpenCode `--agent plan` with local Qwen3:4b timed out after 75s; safely labelled `needs_review`. A simple local Ollama generation was slow and did not yield a useful design critique. Do not blindly retry or claim autonomous AI art direction works.
- Further bounded local foundation inventory is queued, to enumerate source assets and unresolved license/provenance. This does not imply commercial clearance.

## Critical blockers
- The exact owner-approved three reference PNGs exist in ChatGPT Library but are not yet confirmed mirrored into Dell's worktree.
- Current WIP is structurally editable but NOT film-quality modelling. Need high-fidelity licensable character foundation, authentic mature facial sculpt, correctly constructed sari and jewellery, eye/blink and cloth deformation visual QA, and actual Three.js mobile FPS measured.
- Automated rig/file checks and AI impressions never equal independent creative QA or owner approval.

## Operations (Dell)
```sh
python3 ~/matrix-controller/art-worker-v1/worker.py status
python3 ~/matrix-controller/controller.py status
systemctl --user list-timers --all | grep shaadi-art
systemctl --user status bhm-shaadi-art-worker.service
# Fixed scripts are hash-pinned by owner-scoped worker_enrollment.json
```
Do not publish either the GLB or the native Blender derivative. Keep all source hashes, previous worktrees, test receipts and rollback paths.