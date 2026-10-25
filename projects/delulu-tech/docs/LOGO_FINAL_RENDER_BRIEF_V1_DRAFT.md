# Delulu Tech — final Impossible Ribbon animation render (proposed acceptance contract)

**Status: DRAFT — awaiting explicit owner acceptance.** Prepared 2026-10-25. This document is not authorization for tool execution, release, publication or owner-ledger insertion.

## Frozen input authority

- Project: `delulu_tech`, independent of all other Matrix projects.
- Original owner-locked artwork: Option 2 **Impossible Ribbon**; frozen V1 master ZIP SHA-256 `f50f164e40e6a90bfc97a994cf8d0f0de9abb1e15e247115937e31dadb4508d6`. Use original `delulu-tech-mobile-white.svg` or wordmark white as appropriate; no redrawing, changing path coordinates, AI generation, retyping or distortion.
- Palette **Electric Paradox**: Ink `#0B0D13`, White `#F5F6F2`, Volt `#C9FF3D`, Violet `#6544EA`. Other approved neutrals `#252A36`, `#A7AEBB`. Palette proportions 65/25/8/2 as qualitative guidance.
- Canonical brand: `projects/delulu-tech/brand/BRAND_SOURCE_OF_TRUTH_V1.md`.

## Proposed render specification (not yet approved)

Deliver a **4.0 s silent, non-looping cinematic logo animation**, 30 fps, on Midnight Ink background. Output formats:
1. `delulu-impossible-ribbon-landscape-v1.mp4`, H.264 1920×1080.
2. `delulu-impossible-ribbon-portrait-v1.mp4`, H.264 1080×1920 mobile-native.
3. `delulu-impossible-ribbon-final-white.png`, clean static transparent PNG derived from the exact SVG; dark-background companion JPEG is optional.
4. Render/QA receipt with full source hashes, codec, dimensions, frame count, screenshots, thermal metrics and limitations.

Motion timeline (timings provisional):
- 0.00–0.35 s — restrained near-black entry.
- 0.35–1.70 s — original Impossible Ribbon linework/path masks emerge progressively; a dimensional unfold illusion must be apparent, rather than a plain whole-logo opacity fade.
- 1.35–2.20 s — Electric Violet light travels over the ribbon, spatially aligned to the form. Approved white paths remain immutable.
- 2.15–2.55 s — one short Volt Lime illumination on the reveal peak, then retract to the monochrome master.
- 2.55–4.00 s — settle into crisp approved white wordmark, no continuing movement or glow.

## Non-negotiable QA gates

- **Source integrity:** compare rendered vector source and freeze manifest; no new logo paths or text glyphs. No hallucinated imagery.
- **Actual motion:** capture all 120 frames per composition, independently inspect >=30 temporally dispersed frames per orientation, including frames before/during/after the lime climax. Report visible errors, ghosting, blank frames and misalignment. A textual LLM critique never substitutes for visual inspection.
- **Composition:** no logo cropping, stretching or unreadable TECH. Check final settled frames at 1920×1080, 1080×1920, and on mobile-size playback.
- **Accessibility & performance:** provide static equivalent. Avoid flash patterns, abrupt high-frequency luminance changes, and excessively bright effects. Verify playback frame rate, no dropped frames or stutters against the actual exported video; record objective measurements.
- **Render resource gates:** Dell is authorized as the worker only after Tool Yard intake approval. Do not disable existing `video_preview` thermal QA; certify thermal conditions or use an explicitly approved safe, existing renderer instead.
- **Independent review:** confirm actual video output against storyboard, then request owner visual approval. Do not mark it final if mismatched.
- **Release:** stay in private artifact storage until a second explicit, artifact-hash/target-pinned owner release approval. No public upload, no spend, no live website change.

## Tool Yard gate state at drafting

Dell online. Dev Tool Yard `0.2.2-global-intake-governed` active. No approved `quality-inbox/delulu_tech/logo_motion_final_v1` contract or matching owner intake ledger exists. The controller's `video_preview` action remains explicitly blocked pending thermal QA. This document is a **proposed scope** only. The owner must explicitly approve these deliverable specifications and rendering resource gate before work may begin.
