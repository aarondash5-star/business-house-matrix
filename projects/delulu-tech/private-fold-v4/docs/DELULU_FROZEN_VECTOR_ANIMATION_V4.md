# Delulu frozen-vector animation V4 — private design and execution contract

**Private candidate only, 2026-10-25.** Delulu original SVG SHA-256 `d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368` is byte-preserved. Blender 4.0.2 native `io_curve_svg` imports its original two SVG paths.

## Geometry correction
Prior generic 3D strip was unrelated to the logo. This V4 uses the real original SVG letterform vertices, extrudes real front/back/edge polygons and establishes four distinct shape-key deformations of the actual mesh. By frame 49, weights for all deformation keys return to zero and exact SVG-derived planar Basis vertices are restored. No separate flat masking transition is used; the same object topology remains throughout.

## Frozen animation constraints
Frames 1/13/25/37/49 at 12 fps create a four-second preview. Mesh keyframe F-curves must persist in Blender saved file. Verify five PNG sha256s, final appearance against SVG raster and all fcurves with independent inspection. The exact *vector source* is maintained, but projected antialiasing, physical extruded edge and lighting may require owner creative refinement.

## Safety / authorization
All source is reviewed via Dell project `delulu_tech/dev_project_build/delulu_fold_review_v1`. Output only to private `~/.local/share/matrix-code-executor/delulu_tech/private-fold-v4/`. Thermal stop at above 73C; no upload/publish, no spend, no generic sandbox binary permission expansion. Product QA, independent identity, branding and release approval separately required. No merging into public site.
