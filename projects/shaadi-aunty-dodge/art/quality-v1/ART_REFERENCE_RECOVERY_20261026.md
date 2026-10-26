# Shaadi Aunty’s Dodge — reference-aware art recovery (26 Oct 2026)

**Scope:** Dell Matrix Dev Tool Yard / nonproduction review branch only  
**Gate:** `SAD-VISUAL-QUALITY-V1` (immutable; **not passed**)  
**Owner authorization:** Resume art worker, repair 30-minute oversight, load original approved references, improve rigs, rerun QA, present candidates. **No production merge.**

## Recovery receipts

1. **Dell connectivity:** paired/online; control, operations, development lane heartbeats current during checks.
2. **Original pinned visual references ingested privately** to `projects/shaadi-aunty-dodge/art/quality-v1/references`. Local SHA256 verified:
   - Sharma Aunty turnaround: `936b282ebcb1fb9ca5ef47b0ed1b3b471191bb654aa4c2f6925a469dbb667d3b`
   - Grand mandap: `6802cc9c839fcb6be65da162eed9b4ea9028b938bac4007155597bb412e9760a`
   - Portrait runway: `5ccb9756a43706f19bd208fdebe3723a252d86e91473771c04510145db2bfd5d`
   - **Do not commit source reference PNGs to this public repository.**
3. **Critical occlusion bug:** `ai_art_refine.py` captured a sphere's world matrix before applying its small scale to Blender’s evaluated transform. The glass nose pads and jasmine flower components rendered as ~2-meter primitives over the character. Isolated staged recovery corrected **170 decorative meshes**, max observed dimension 2.0m -> 0.03m. Derived editable Blender candidate SHA256: `ac0e3ea7a49d73d0ace818e7fe6ba0828b6b8c7793c9ef38f536805db4773aea`.
4. **Fresh genuine Blender evidence** from corrected candidate: four actual PNG renders and GLB export. Front PNG SHA256 `126d0fb1e18cdddedaf433d7145b73b86056cd4ebc22cdadd8b3e6cc70c804a8`. GLB SHA256 `1843aaeb647700baa289c9c7661ebf3089f3ca8590c791b37a1e00f78ccbbf62` (~10.27 MB), passing four named animation clips (Idle, Walk, Question, DodgeReaction) and three morphs (Blink, Smile, JawOpen). **Not a visual pass.**
5. **Reference-aware comparison** stored locally as `iterations/20261026-occlusion-correction-review/side_by_side_character_v1.jpg` plus `reference_comparison_qa.json` (SHA256 of contact sheet `76da152c5ab16fd9cb8a639baf08641949e7856932a6d52a859ca2efe4087ee7`). Visual QA explicitly **FAIL_REFERENCE_FIDELITY**.
6. **AI Art Director V2**: locally pinned enrolled scripts under `worker/v2` on this review branch. It validates exact reference SHA256, uses a downscaled *actual pinned turnaround* as image one and current candidate as image two, enforces allowlisted model outputs, fixes empty `cycle-03` directory retry bug, and fixes decorative transform order; no generated code, no paid providers, no self-certification. `8/8` dedicated contract tests and `8/8` Manager V3 regression tests pass. The first real reference-aware two-image inference was initiated at ~10:35 IST; **do not mark a third cycle complete before a terminal receipt**.
7. **Scheduling**: Replaced broken elapsed-only 30-minute systemd timer with a half-hour `OnCalendar=*:0/30` drop-in; next-fire verification succeeded. The timer was then paused while V2 was patched and one bounded manual trial started. **Restore only after inspecting that trial’s outcome and any blocked state.**

## Current artistic deficiencies — hard blockers

- Mature facial identity and facial performance diverge sharply from the approved turnaround.
- Garment is still a plain, cone-like pink sari prototype without credible tailored pleats, zari detail, hand pose or cloth deformation proof.
- Hair/jewellery/accessories remain insufficiently authentic and polished.
- Wedding palace/mandap fidelity is independently still **3/6**; character historical structural baseline **5/9**.
- Actual interactive 9:16 Three.js footage and sustained Android 30 FPS measurement remain unverified.
- Independent creative QA, licences/origins reconciliation and **exact owner art-hash approval** are missing.

## Mandatory next worker course

**Do not spend cycles polishing only glasses/jasmine/zari on the rejected baseline.** Use a correctly licensed richer character/cloth foundation, mature sculpt and sari topology, real facial animation, authentic mandap meshes and mobile runtime scene. Produce actual Blender front/3-quarter/side/back/face evidence, posed sari deformation, GLB animation/morph checks, mobile Three.js capture and Android FPS data. Compare side-by-side to all three immutable references. Fail closed on missing evidence. Obtain owner approval of exact new model, venue and playable build hashes before any merge.

## Scope controls

No raw owner reference artwork in public Git; no production merge or release; no paid API, permissions escalation, unrelated projects, or automatic owner sign-off. Preserve rollback directory `~/matrix-controller/art-worker-v1/release-backups/director-reference-v2-20261026/` and original candidate sources.
