# Delulu Tech × Matrix Game Toolkit — production animation lane integration

**Status: verified toolkit; fixed Delulu recipe pending enrollment and owner-pinned Tool Yard intake.** Date 2026-10-25.

## Inventory and live receipts

- Dell game toolkit: `/var/lib/generic-linux-automator-exec/matrix-game-toolkit-20261025` (isolated from Shaadi G3 and every other project).
- Toolkit smoke: **13 passed, 0 failed** on 2026-10-25, including Three.js, tween.js, postprocessing, glTF Transform, Meshoptimizer, Chrome/Playwright.
- Portable Blender 4.5.15 LTS: headless smoke PASSED, Eevee Next/Cycles available, MPFB2 import works but is irrelevant to this logo.
- FFmpeg H.264 encoder `libx264` and system Chrome installed; thermals sampled at 25°C, **single sensor reading is not a sustained rendering thermal certification**.
- Frozen brand archive verified SHA-256 `f50f164e40e6a90bfc97a994cf8d0f0de9abb1e15e247115937e31dadb4508d6`; approved mobile-white SVG SHA-256 `d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368`.
- Tool Yard controller `0.2.2-global-intake-governed`: service active, `video_preview` BLOCKED until thermal QA. Gaming toolkit is installed but its controller integration says `controller_enrolled: false`, `runtime_connected: false`. **An authorized Dell SSH lane is not the same as a quality-governed Matrix action.**

## Art direction; proposal for owner's versioned acceptance

Preserve all frozen geometry by treating the **original approved SVG** as the sole alpha/silhouette and color source. **No generated logo reconstruction**, no retyped letters, no deformation of master path coordinates.

- Use the isolated Three.js + tween.js pipeline for a GPU-assisted **path-reveal illusion** with a moving leading edge, ribbon-following violet rim lighting and a short Volt peak. Render white original artwork as untouched end state.
- The 2.5D animation may mask the source SVG; all revealed white pixels must come from the original file. To avoid deceptively claiming a physical 3D fold, the visual must be judged against the original storyboard. If physical fold remains mandatory, first produce a **Blender 4.5.15 isolated extruded curve** proof, preserve master path data, and compare against fixed original silhouette. No uncontrolled camera perspective on text.
- Proposed 4 s, 30 fps, 120 frames each in 1920x1080 and 1080x1920. Prefer GPU/browser render first, FFmpeg only for deterministic packaging. No automatic sound.
- Explicit "skip/reduced-motion" static original logo remains accessible, not an animated substitute.
- Hold output locally, no public deployment or video publishing.

## Exact controller adapter required (do not bypass with arbitrary SSH)

Implement a narrowly scoped `game_logo_render_v1` adapter after owner-authorized approval, with constant project `delulu_tech`, immutable manifest `logo_motion_final_v1`, hash-pinned SVG and quality contract. The only parameter variation allowed is one of `landscape`, `portrait`, `both` after validation.

Allowed fixed steps:
1. Verify `quality_admission.intake_check('delulu_tech','game_logo_render_v1','logo_motion_final_v1')` and pin contract SHA. No entry = STOP.
2. Read original SVG from the enrolled, project-owned immutable source. Reject manifest/hash mismatch and any foreign paths or symlinks.
3. Render isolated deterministic frames using verified game toolkit dependencies, with bounded CPU/RAM/disk and thermal logging. Do NOT execute caller-supplied Node, Blender or shell commands.
4. Compare source/vector hashes and final settled frame against reference, inspect minimum 30 actual frames per orientation, report dropped/blank frames, verify exact frame count, logo crop/readability, colors, flashing and mobile playback.
5. Encode MP4 via fixed audited FFmpeg recipe. Emit frame hashes, output SHA-256, dimensions, codec, runtime and independent QA receipt.
6. Return **technical render ready for owner review** only. Neither complete design nor public release can be inferred. Tool Yard release-check remains separate.
7. Do not modify or merge `shaadi_aunty_dodge` runtime; shared dependencies are read-only tooling only.

## Runtime gate decisions

**Owner action required**: approve the separate project-specific brief and its five-category `media` acceptance contract, allow a reviewable fixed-controller adapter to the installed gaming toolkit, certify sustained thermal rendering load, and authorize the private render. The existing user instruction to use the gaming lane directs the tool choice; it does not authorize bypass of frozen owner intake/publishing gates.

Next: create an immutable `logo_motion_final_v1` brief and acceptance JSON in owner-controlled `quality-inbox`, pass independent adapter tests, then enroll. Never mark this document as a finished animation.
