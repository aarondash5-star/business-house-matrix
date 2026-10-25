# Shaadi Aunty — Autonomous AI Art Direction V1

**26 October 2026 — Dell Dev Tool Yard. Owner-approved non-production execution.**

## Deployment

- Persistent service: `bhm-shaadi-ai-art-director.service`; 30-minute timer: `bhm-shaadi-ai-art-director.timer` (enabled/active on Dell).
- Existing fixed-recipe art worker remains enabled every approximately two minutes, with owner-scoped queue and `needs_review` fail-closed handling.
- Art director script: `~/matrix-controller/art-worker-v1/director_loop.py`; local model image-review script: `ai_art_vision.py`; allowlisted editable Blender profiles: `ai_art_refine.py`. All have local SHA-256 pins in `ai_director_enrollment.json`; no AI-generated code or arbitrary CLI is run.
- Source WIP: `~/shaadi-quality-v1-art-20261025/projects/shaadi-aunty-dodge/art/quality-v1/iterations/20261026-art-worker-v1/sharma_aunty_art_rig_wip_v1.blend`. Derivative, not an approved asset.
- Director iteration output root: `art/quality-v1/iterations/20261026-ai-art-director-v1/`, with `cycle_state.json`, model critique JSON, new editable `.blend`, front/3/4/face renders, exported GLB, SHA receipts and logs for any completed cycle.
- Manager V3 (Dell controller v0.2.4) includes `governance_v3.ai_art_director_v1` and `governance_v3.art_worker_v1`. Controller was restarted after the adapter update; verified.
- Safeguards: isolated writable paths, systemd memory/CPU caps, original asset hashes retained, project-only Blender 4.5.15 LTS + MPFB2, at most three preapproved revision profiles (`glasses`, `jasmine`, `zari`) before independent review, no blind retry, paid API, production merge, or automatic quality approval.
- References: **SAD-VISUAL-QUALITY-V1**, exact three source PNG SHA256s recorded in `ai_director_enrollment.json`. Original bytes remain in the owner's ChatGPT Library, verified and hash-matched, but **not copied to Dell**; the vision prompt uses a carefully defined verbal description of those visual targets. Thus local reviews are **not exact pixel-to-pixel reference comparisons**.

## Verification / Current limitations

- Seven local art-director contract tests **PASS**.
- Twenty-six Manager regression tests **PASS**.
- Manager recognizes current director as **connected** and **release_authorized=false / quality_certified=false**.
- The 30-minute director timer is enabled; the initial call exited successfully with `waiting_for_local_vision_model`.
- Free, local Ollama vision model `qwen3-vl:2b-instruct` was selected, with a pull initiated via `bhm-shaadi-vision-pull.service`; **download not completed** as of the 02:25 IST verification. The model installation MUST be verified before claiming that an actual model-reviewed cycle has run.
- No completed AI-directed revision cycles yet. The system *is scheduled and guarded*, but autonomous **visual direction is blocked until the local model is installed and tested**.
- Do not confuse technically exported four animations and three morphs with a professionally modelled/animated character. The pinned artistic acceptance remains unmet (last independent art check 5/9 character, 3/6 wedding scene); visual approval belongs to the owner.

## Supervisor commands (Dell)

```sh
python3 ~/matrix-controller/controller.py status
cat ~/matrix-controller/art-worker-v1/director_status.json
python3 ~/matrix-controller/art-worker-v1/worker.py status
systemctl --user status bhm-shaadi-ai-art-director.timer
systemctl --user status bhm-shaadi-vision-pull.service
ollama list | grep qwen3-vl
# Non-production manual dry-run, after model is installed:
python3 ~/matrix-controller/art-worker-v1/director_loop.py
```

## Next actions

1. Check vision-model pull receipt; diagnose/fix if download exceeds its safe timeout.
2. Run one end-to-end **actual VLM image** critique and bounded Blender revision; verify produced PNGs, editable `.blend`, exported GLB clips/morphs and checksums.
3. Only if that works, let the 30-minute schedule process remaining owner-allowlisted revisions. If high-fidelity face sculpt still needs a professional foundation, record a blocker rather than cosmetic self-approval.
4. Transfer real pinned reference images securely to Dell for side-by-side visual comparison; do not publish references to a public Git repo.
