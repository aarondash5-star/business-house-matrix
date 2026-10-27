# Visual-First Yard V2 — controlled release receipt (2026-10-27)

**Scope:** Isolated geometry-first 2D pixel-to-editable-vector pipeline; **NOT deployed to Dell** due to both Generic SSH Linux connector links returning internal errors. No production merge, art dispatch, or changes to generic SSH runtime.

## Reused OSI-approved foundations
- OpenCV 4.x, Apache-2.0 — color segmentation / contours
- VTracer 0.6.15 (optional), MIT OR Apache-2.0 — raster-to-SVG
- Pillow, HPND; NumPy, BSD; CairoSVG, LGPLv3
- Florence-2 is **not** installed or certified on the 8GB Dell; no false claim of object recognition. OpenCV region boxes are *unsupervised color components*, not named-object bounding boxes.

## Local independent smoke results
- Fixture: the *exact same 600 × 400* house drawing as the previous Dell benchmark, SHA-256 `7a02f3a72316378db5201c8fe38e0226ecaad8f1ab389ecd2f37fec6a65781f3`
- Earlier Dell generative caption-to-shapes benchmark: weighted closeness **57.2%**, shape IoU **45.8%**, edge F1 **20.2%**
- OpenCV **trace** alternative (from pixels, not fixture source schema): weighted closeness **91.4%**, shape IoU **93.4%**, edge F1 **95.6%**, foreground color **86.1%**
- **Quality gate: REWORK_REQUIRED** — foreground target of 90% is not met. Trace success does *not* qualify creative AI generation or Sharma Aunty resemblance.
- 7 isolated unit tests PASS, including malformed freeze, invalid SVG, missing renderer, wrong image, two unseen flat diagrams.
- VTracer candidate and Dell-native performance **untested** because dependency installation and SSH connection unavailable here.
- Complete local code and image comparisons provided to owner as `visual-first-yard-v2-pilot.zip`.

## Deployment requirements
1. Restore the existing Generic SSH Linux connector; **do not create a parallel shared runtime or modify the SSH worker deployment**.
2. Install in a separate Dell venv, under `matrix-controller/yard-certifications/visual-first-v2`; verify owner freeze before and after.
3. Test against the same SHA-256 reference and preserve old receipts. Publish new review-only artifacts in the existing authenticated gallery, do not expose anonymously.
4. Keep both Shaadi art lanes frozen. Only explicit owner approval may authorize a bounded character-art microtask.
5. Readiness is only infrastructure QA, not an artistic quality pass or production approval.

## Future work still needed
- A faster, fully verified spatial vision model on the actual Dell hardware.
- Differentiation of raster-tracing versus freehand/generative recreation in reports.
- A *real* image-difference-to-AI correction loop in generative mode, with bounded retries; current code chooses between at most 2 tracing engines, not a creative correction agent.
- Manager V3 integration through its authorized department lane after separate smoke certification, not by bypassing the freeze.
