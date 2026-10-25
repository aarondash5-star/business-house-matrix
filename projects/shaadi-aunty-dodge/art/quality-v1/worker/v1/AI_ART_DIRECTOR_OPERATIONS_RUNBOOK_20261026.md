# AI Art Director / Matrix Manager — Operator Runbook
**SOP revision:** V1, 2026-10-26 • **Target:** Dell Dev Tool Yard / Shaadi Aunty's Dodge  
**Status observed at 02:31 IST:** Manager online; two local timers enabled; AI vision pull running, model **not installed**; 0 completed AI-directed cycles; release denied.

## Source of truth
- Live host: `dell-linux` via owner-authorized generic SSH control/development lanes.
- Manager: `~/matrix-controller/controller.py` (v0.2.4 with governance V3 observer).
- Fixed art worker: `~/matrix-controller/art-worker-v1/worker.py`, SQLite `jobs.sqlite3`, `latest.json`.
- Director: `~/matrix-controller/art-worker-v1/director_loop.py`, `ai_art_vision.py`, `ai_art_refine.py`, and `director_status.json`.
- Art review path: `~/shaadi-quality-v1-art-20261025/projects/shaadi-aunty-dodge/art/quality-v1/`.
- Existing editable baseline: `iterations/20261026-art-worker-v1/sharma_aunty_art_rig_wip_v1.blend` (SHA-256 `3233ce0bda132dff9e21f333429ca6e2302b04d240b250b16b5c0a3422c8b09c`).
- Isolated LTS wrapper: `tools/run_blender_4_5_lts.sh`; keep OS Blender 4.0.2 intact.
- Director outputs: `iterations/20261026-ai-art-director-v1/cycle_state.json`, `cycle-NN/vision_critique.json`, new .blend/GLB/renders/hashes and logs.
- Legacy pinned structural QA: `evidence/qa_independent_structural.json`; **not** a passing creative-gate receipt.
- Existing Git review branch: `feat/shaadi-art-quality-v1-review-20261025` in `aarondash5-star/business-house-matrix`. Local worktree may have a divergent upstream; use explicit branch-specific fetch/show and avoid forced/non-fast-forward pushes.

## One-screen read-only health check
Run on Dell as the paired nonroot operator:

```sh
date -Is
python3 ~/matrix-controller/controller.py status
python3 ~/matrix-controller/art-worker-v1/worker.py status
cat ~/matrix-controller/art-worker-v1/director_status.json
systemctl --user is-active bhm-autonomy-controller.service
systemctl --user list-timers --all | grep -E 'shaadi-ai-art|shaadi-art-worker'
systemctl --user show bhm-shaadi-ai-art-director.service -p ActiveState -p Result -p ExecMainStatus
systemctl --user show bhm-shaadi-vision-pull.service -p ActiveState -p Result -p ExecMainStatus
ollama list | grep -E 'NAME|qwen3-vl'
```

Expected: Manager active; timer(s) enabled; governance status `release_authorized=false`, `quality_certified=false`; worker jobs and director are visible under `governance_v3`. The existence of an enabled timer is **not evidence a model review completed**.

## Vision-model startup / first-run acceptance
1. Check `bhm-shaadi-vision-pull.service` and Ollama `/api/tags` for exact `qwen3-vl:2b-instruct`. The free model is configured for loopback inference, not a paid remote API. A background `ollama pull` process is only *download in progress*.
2. If the pull is stalled, inspect journal and network/disk; stop only the dedicated pull unit before a controlled retry. Do not delete global Ollama models or disrupt other workloads.
3. Verify actual local image inference completes within runtime resource limits; record model tag, response, elapsed time and image hash. Never report a completed creative review just from model presence.
4. Run one manual review-only smoke when the model is ready:
```sh
python3 ~/matrix-controller/art-worker-v1/director_loop.py
cat ~/matrix-controller/art-worker-v1/director_status.json
```
   Expected on success: `AI_ART_DIRECTOR_CYCLE_OK`, `completed_cycles=1`, a `cycle-01` folder containing model review, modified editable Blender, four PNG renders and GLB technical receipt. The owner must still examine whether this is a meaningful visual improvement.
5. Only after the first real cycle has passed may the existing 30-minute timer be relied upon for additional bounded iterations. Max profiles=3; after that the director records `needs_independent_creative_review`.

## Common incidents and prescribed recovery
| Symptom | Evidence to collect | Safe response |
|---|---|---|
| `waiting_for_local_vision_model` | Ollama tags, pull service status/journal and model registry connectivity | Wait for/repair model installation; **no** fake critique or switch to paid API |
| Vision inference times out | `cycle-NN/vision_critique.json`, local model logs, CPU/RAM, response latency | Mark `needs_review_cycle_failed`, inspect output; retry only after explicit audited decision |
| OpenCode critique exit 124 | SQLite task `opencode_art_critique`, `opencode_review.log` | Leave `needs_review`; new local VLM director is a **separate** path, not retroactive success |
| New cycle directory exists but no terminal receipt | Cycle directory hashes / process state / last model/revision log | Mark ambiguous; do not delete, overwrite or replay blindly |
| Pinned script integrity mismatch | `ai_director_enrollment.json` and SHA-256 current scripts | Stop. Review diff and obtain scope-admission decision before re-pinning |
| Source `.blend` differs from saved SHA | `cycle_state.json`, source file/manifest and mtime | Stop and investigate potential concurrent edits |
| Invalid/low-quality shape or costume | Actual front/3/4/side/face plus reference comparisons | Keep failed candidate, return specific modelling defects; never promote |
| Missing reference PNGs on Dell | Three original SHA-256s; asset access/provenance | Mark text-only comparison; obtain authorized private image transfer; don't claim pixel comparison |
| Licence uncertain | `foundation_inventory.json` and upstream source licences | Prevent final asset adoption until verified |
| Manager reporting stale | Service status, `manager-governance-v3/latest.json`, SQLite timestamps | Repair observer separately; do not mutate pending work or bypass release checks |
| Production gate requested | Original source, independent QA, exact candidate hash, owner approval record | Stop absent all approvals and a separate explicit merge/deploy instruction |

## Safety and rollback
- **Freeze a failing director safely** (retain all logs/artifacts): `systemctl --user disable --now bhm-shaadi-ai-art-director.timer`. Do not stop the entire Manager or OS Blender to handle a director incident.
- **Restore timer only after diagnosis**: `systemctl --user enable --now bhm-shaadi-ai-art-director.timer`; check next trigger and state.
- **Freeze fixed worker** separately: `systemctl --user disable --now bhm-shaadi-art-worker.timer`. This does not delete queued jobs.
- Manager governance V3 restoration is documented under `~/matrix-controller/release-backups/`; previous observer backups were created before art-worker and director adapters. Changing controller source requires comparison of saved SHA, selftest/regression, careful service restart and live status verification.
- Do not automatically advance from an interrupted `running` state; first inspect external outputs, hashes, terminal receipts and duplication risk.
- No automatic owner approval, spend, production merge, external publish or quality-score invention.

## Required QA / evidence checklist
- [ ] Original pinned references available privately as actual bytes, hashes checked.
- [ ] Foundational source licence and commercial redistribution terms verified.
- [ ] Editable .blend loads in pinned Blender, 35+ real bones and suitable weights/pose deform tests.
- [ ] Fresh neutral 360°/front/side/3/4 closeups, facial expressions and sari deformation evidence.
- [ ] Actually exported GLB clips Idle/Walk/Question/DodgeReaction, morphs Blink/Smile/JawOpen, and playback parity.
- [ ] Independent artistic reference comparison passes without hiding defects.
- [ ] Three.js integration and measured lower-end Android >=30 FPS benchmark pass.
- [ ] Exact SHA-256 asset hashes and independent QA receipt filed.
- [ ] Owner explicitly approves exact candidate; separate merge authorization if relevant.

## Validation & maintenance
```sh
cd ~/matrix-controller
python3 controller.py selftest
python3 -m unittest -q test_manager_governance_v3 test_toolyard_qa_standard_v1 test_yard_auto_adapter_v1
cd ~/matrix-controller/art-worker-v1
python3 -m unittest -v test_ai_art_director
```
Current verified test baseline: Manager suite **26 tests pass**, director suite **7 tests pass**. These are **contract** tests; a full end-to-end local VLM render/edit/export cycle is **not yet certified**.

Once changes to worker scripts are approved, update local enrolment hashes under the appropriate governance process and re-run tests. Never let a content-only doc change implicitly authorize a new executable recipe. Store all source/receipt paths and process changes in the review branch, with dates; keep the production game untouched.
