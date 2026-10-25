# Quality Gate V1 — actual execution/QA handover

**Status: FAIL / DEVELOPMENT CANDIDATES ONLY / NO MERGE.**
Gate: SAD-VISUAL-QUALITY-V1, owner-approved reference baseline in Library. These native Blender files do **not** match the approved images. Never silently swap or lower that gate.

| Candidate | Blender file | Review render | Structural checks | Visual |
| -- | -- | -- | -- | -- |
| Sharma Aunty | candidates/sharma_aunty_editable_v1_candidate.blend | previews/sharma_v1_full.jpg, sharma_v1_face.jpg | 5/9 | FAIL |
| Wedding | candidates/grand_wedding_scene_editable_v1_candidate.blend | previews/wedding_v1_wide.jpg, wedding_v1_phone.jpg | 3/6 | FAIL |

Full independent mechanical evidence: evidence/qa_independent_structural.json; audit script independent_structural_audit.py. Generator source: character_v1.py and wedding_v1.py.

**What is real:** Body 19,158 vertices, 53-bone MPFB skeleton, 18 body shape keys, weighted separate sari fabric; modular Blender wedding architecture with 1,537 editable objects and 9:16 camera. This is technical feasibility, not premium art fidelity.

**What fails:** Character identity and facial anatomy, costume construction and surface richness, anatomical deformation check, eye/blink controls, studio-quality lighting; venue has repetitive bloom meshes and generic decoration instead of rich Indian palace/mandap depth; no Android FPS or runtime parity certification. Source provenance not fully packaged.

**Next qualified action:** Replace stylized source with professionally authored licensable character & detailed venue kits, sculpt mature Indian proportions, tailor ornate sari, rig face eyes and pallu, add authentic wedding architecture, then re-render turnarounds and mobile captures. Art-director independent signoff must occur before owner sees an approval candidate. Explicit owner approval must be tied to file hashes. No production merge.

**Scope:** separate review branch only. The previous 2026-10-25 v0.2 Sharma and v0.1 scene are rejected. Do not use procedural prototypes as release assets.
