# Shaadi Aunty's Dodge — Art Worker Handover
**Date:** 2026-10-26  
**Scope:** Sharma Aunty first; grand wedding environment second.  
**Engine:** Three.js only. **Authoring:** Blender + suitable licensed open-source/professional foundations.  
**Status:** ART IN DEVELOPMENT; pinned V1 NOT MET; NO PRODUCTION MERGE.

## Non-negotiable visual baseline
Owner-pinned gate: **SAD-VISUAL-QUALITY-V1**, accepted as a *look target* on 2026-10-25, **not** as acceptance of any rig. Do not replace, re-interpret downwards, or claim a code/test pass is artistic approval.

Canonical reference images (original bytes in owner's Library):
- Sharma Aunty turnaround — SHA256 `936b282ebcb1fb9ca5ef47b0ed1b3b471191bb654aa4c2f6925a469dbb667d3b`.
- Grand mandap — SHA256 `6802cc9c839fcb6be65da162eed9b4ea9028b938bac4007155597bb412e9760a`.
- Wedding runway 9:16 — SHA256 `5ccb9756a43706f19bd208fdebe3723a252d86e91473771c04510145db2bfd5d`.

**Art direction:** Original feature-animation-quality 3D, between realism and cartoon. Recognizable mature Indian Sharma Aunty: distinctive face and expressive eyes/brows, glasses, bindi, jasmine-adorned bun, layered jewellery, genuinely constructed magenta/saffron/gold saree with believable surface detail and skinned/draped pallu; coordinated richly layered Indian wedding architecture and cinematic lighting. Optimized for 9:16 mobile gameplay as well as full turnarounds.

## Existing evidence — DO NOT mistake for finished work
On Dell, local review worktree:
`/var/lib/generic-linux-automator-exec/shaadi-quality-v1-art-20261025`

Art directory:
`projects/shaadi-aunty-dodge/art/quality-v1/`

Candidate sources: `candidates/sharma_aunty_editable_v1_candidate.blend` and `candidates/grand_wedding_scene_editable_v1_candidate.blend`. Original authoring scripts: `character_v1.py` and `wedding_v1.py`. Mechanical audit: `independent_structural_audit.py`; evidence: `evidence/qa_independent_structural.json`; renders: `previews/`.

Last audit: **character 5/9; scene 3/6; creative QA FAIL**. Character includes a 19,158-vertex human body, 53 bones, 18 shape keys and weighted pallu, but lacks approved likeness, tested eye/blink and cloth deformation, and completed provenance. Scene includes editable geometry and portrait camera but not approved mandap quality. All existing candidates are **technical starting points**, never release-ready or eligible for a visual-signoff claim. The .blend binaries live on Dell; previous remote Git upload contains scripts, QA and thumbnails, not guaranteed current native .blend files.

## Work order — character quality first
1. Locate/read all three exact owner references and the V1 acceptance notes; inventory existing Dell character and usable openly licensed foundations. Capture exact asset origin, file hash, permitted redistribution/commercial terms; reject sources with unclear licenses. Do not spend money without owner approval.
2. **Replace—not merely decorate—the weak character foundation** where needed. Sculpt the mature face/body silhouette and correct jewellery/hair/eyewear/bindi, build physically believable saree folds, embroidery, pallu layering and hand/foot proportions.
3. Make native **editable** Blender master: coherent deforming armature, face controls, eyes/blinks, mouth/brows, hands, cloth weighting/posed deformation. Supply controlled Idle, Walk, Question, DodgeReaction clips and Blink, Smile, JawOpen expressions; test for clipping and wrong normals across poses. Do not fake animation with a still render.
4. Capture true Blender render evidence: front/back/left/right/3/4, close-up face, materials/costume, side-by-side reference comparisons, articulated pose + expressive action frames. Preserve source .blend, textures, rig tests, source licenses, hashes and editable hierarchy.
5. Then upgrade the venue from generic repeated arches to genuinely detailed mandap, floral layers, architecture, warm lighting, props, parallax and mobile camera framing. Preserve modularity and mesh/performance budgets.
6. Export actual GLB files through Blender; optimize with glTF Transform and Meshoptimizer; integrate in **isolated Three.js staging** using `projects/shaadi-aunty-dodge/threejs/`, whose manifest is intentionally unapproved. Test actual clips and morphs, Playwright gameplay, WebGL failures, 320/390/430px screenshots and real Android FPS (target >=30 FPS). **Never flip approved flags to bypass checks.**

## Worker cadence and governance
Use the existing Dell Matrix Tool Yard Manager (**controller v0.2.4 / governance v3**). Its persistent observations are in `/var/lib/generic-linux-automator-exec/matrix-controller/manager-governance-v3/latest.json` and append-only events `events.jsonl`; these are reporting receipts, not authority for production release. The ChatGPT supervision task reviews Manager state hourly. Use event-driven task replenishment and a 30-minute health/recovery check *if a separately authorized local art executor is installed*; do **not** pretend the observation-only Manager automatically runs a modelling agent.

For every iteration: record task ID, Blender file path + SHA256, source asset licenses, changed geometry/rig features, failed tests, rendered review files, independent QA, current gate status, next bounded task and owner decisions required. Keep prior candidates recoverable, respect existing task admission, never retry an uncertain external action blindly, never merge or publish production.

## Exit / approval
A candidate can be sent for approval **only** when technical source QA and an independently reviewed visual comparison both pass against the pinned owner references, and the real Three.js mobile gameplay renders correctly with measured device performance. External AI art opinions are not independent human signoff. The owner must explicitly approve exact final asset hashes. Until then: **V1 FAIL / release unauthorized**.

**Source branch:** [Shaadi art review](https://github.com/aarondash5-star/business-house-matrix/tree/feat/shaadi-art-quality-v1-review-20261025/projects/shaadi-aunty-dodge/art/quality-v1).  
**Next immediate action:** create a materially better, licensable, mature Sharma Aunty **face + costume + body** base, then show proper front/3/4/side close-ups before expanding animations or scenery.
