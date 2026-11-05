# Visual-First Dell Yard V2 (isolated review pilot)

Implements geometry-first 2D image tracing, independent pixel QA, per-attempt receipts, fail-closed quality gates and mobile-ready review. **This is not an AI illustration generator or a 3D artistic likeness certifier.** It vectorizes the input image into editable shapes. In the last Dell art evaluation a caption-to-JSON generator scored 57.2% weighted closeness; this code provides an alternative pathway for the flat 2D benchmark.

## Run (isolated, no game mutation)

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install -r requirements-optional.txt  # optional VTracer wheel
.venv/bin/python -m visual_yard_v2 run --reference /path/to/original/target.png \
  --output /path/to/review-only-results --freeze /var/lib/generic-linux-automator-exec/matrix-controller/docs/SHAADI_ART_LANES_OWNER_FREEZE.json
.venv/bin/python -m unittest discover -v
```

`--freeze` is required for any Dell installation. If the freeze record is invalid the process fails before rendering. If VTracer is unavailable, the auto mode falls back to OpenCV quantized contours; if both fail, results are `FAIL_CLOSED`. Image evaluation is always independent from the vectorization module; the test oracle is never passed to either worker.

### QA and correction policy

- Two bounded attempts at most (VTracer, then OpenCV) with receipts per attempt. This is **candidate selection, not a self-correcting creative vision loop**.
- `global_rgb_similarity_pct` is background-dominated: foreground colour, silhouette overlap and edge alignment are primary gates.
- Proposed flat 2D thresholds: silhouette >=90%, edges >=80%, foreground >=90%, plus separate owner signoff; owner and creative approval are **never** set by code.
- Review in output `index.html` after calling `visual_yard_v2.review.make_review(...)`, or open `side_by_side.png`.
- The pipeline only outputs to the isolated review directory. No art dispatch, `.blend` mutation, production merger or game deployment.

### Open-source reuse research

- **VTracer** (MIT OR Apache-2.0): colour raster/vector tracing. Pinned optional wheel `vtracer==0.6.15`. Python API from [visioncortex/vtracer](https://github.com/visioncortex/vtracer).
- **OpenCV** (Apache-2.0 4.5+): contour extraction and colour segmentation, pinned major version 4.x.
- **CairoSVG** (LGPLv3): local safe raster validation. LGPLv3 is OSI-approved; invoke as an independent Python library.
- **Pillow** (HPND): fixture/rendering. **NumPy** (BSD): image metrics.
- **Florence-2**: proposed optional region-detector future stage, NOT installed here. Do not claim the Dell 8GB machine is certified for it until benchmarked; licensing and dependencies must be reviewed separately. The current demo does not make object-level semantic bounding-box guarantees.

### Dell deployment / integration gate

Code is intentionally isolated in a review-only package. It is not wired into `manager_governance_v3.py` art-dispatch functions. The owner has frozen both art lanes. **Do not unfreeze or alter the generic SSH runtime.** Once SSH is restored, install only in a dedicated virtual environment within a separate visual yard directory and execute against the existing `yard-certifications/drawing-e2e-20261027/target.png` (SHA256 `7a02f3a72316378db5201c8fe38e0226ecaad8f1ab389ecd2f37fec6a65781f3`). Surface the verified output to the existing private gallery. Preserve original 57.2% receipt for comparison.

`ready_for_owner_visual_review` is not production approval. Tests should certify both technical success and honest **creative-unapproved** state. Keep unrelated project queue isolated.
