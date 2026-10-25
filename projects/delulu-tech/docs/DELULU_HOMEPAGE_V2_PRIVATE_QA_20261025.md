# Delulu Tech Homepage V2 — Dell Dev Tool Yard handover & QA

**Date:** 2026-10-25. **Result:** technical private stage completed; design/owner acceptance still pending.

## Authoritative stage and integrity

- Controller: `0.2.2-global-intake-governed`; independent project `delulu_tech`, manifest `delulu_homepage_v2`, exact reviewed brief and owner intake record pinned.
- Successful production Tool Yard **private stage task**: `d941f739-a64d-451f-83b0-ec6450282cc6`.
- Immutable local private stage: `/var/lib/generic-linux-automator-exec/matrix-controller/staging-private/delulu_tech/91f2510385bb7d2f6157/`. No public domain.
- V2 stage `index.html` SHA-256 `be647f8fdaf277b30d175947ed808123f743782967dc5ed095238d508f0b5b2d`.
- Frozen logo SVG SHA-256 `d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368` unchanged.
- 1920×1080 H264 video SHA-256 `21def85965218f3361e66c5ab3609fd5642d8ab500670bb3430a4f5cce4642e7`.
- 1080×1920 H264 video SHA-256 `096a978c36e69546ac491ca288cb4e1f058cc2bfa367d59d0dc064a2fe49b6d5`.
- Video properties independently validated: both exactly 4.000 seconds, 120 frames at 30fps, no audio.
- Temperature samples during both Dell renders: 25°C on available thermal sensor. This is a bounded-run observation; **not** a fleet-wide thermal certification.
- V1 stage untouched; earlier V2 stage also retained for rollback. Controller static-staging engine gained SHA-pinned MP4 support with `ftyp` validation; backup `release-backups/static-stage-before-media-20261025T081157Z.py`; legacy manifest validation and controller selftest passed.

## Runtime and front-end

- Development: GitHub draft PR #25, all implementation executed/tested on isolated Dell Dev Tool Yard checkout `delulu-site-v2-20261025`.
- Hero: original frozen vector retained as nav, autoplay-failure fallback, reduced-motion equivalent and persistent end frame. The 4s mobile/desktop render is silent, plays inline, non-looping and will hide itself on end.
- Site: redesigned responsive private one-page identity concept. No fake services/client numbers, no invented contact details. Internal navigation works and sections are intentionally copy-pending for owner approval.
- Quality script: `projects/delulu-tech/staging/v2/test_site.cjs`; test reports and actual viewport screenshots under `staging/v2/qa-evidence/`.
- **Automated checks passed:** viewport widths 360, 390, 768, 1440, reduced-motion mobile and desktop, skip animation, logo present, media decodable, no page errors, no horizontal overflow or dead internal anchors.
- **Corrected actual visual defect:** desktop's finished video surface appeared blank in some headless capture states. Explicitly hide finished video; display frozen master SVG after playback. Actual 1440px viewport pixels verify white logo present. Store viewport captures separately from full-page captures, which can omit composited video surfaces.
- Encoded frames: sampled 30 from each output via FFmpeg contact sheets `qa-evidence/landscape-30-frames.png` and `portrait-30-frames.png`.
- Quality evidence stored under `matrix-controller/quality-inbox/delulu_tech/delulu_homepage_v2`: source-trace, motion QA, responsive QA and accessibility QA passed, **independent human review pending**. `quality_gate.py check` returns `evidence_not_passed` for `independent_review` only.

## Release boundaries and follow-up

**Do not call V2 publicly launched or owner-approved.** There is no approved V2 release target and no direct external publishing connector gate. The authenticated Vercel link `delulu-tech-preview.vercel.app` still serves earlier V1. No Vercel/Cloudflare/WordPress/GitHub Pages deployment was made in this task.

Next step: owner visually reviews V2 (actual viewport captures and animation videos). After accepted changes and independent review, create an exact artifact/target/time-bounded owner release approval before any authenticated Vercel preview upload. Keep old V1 until owner separately authorizes replacement.
