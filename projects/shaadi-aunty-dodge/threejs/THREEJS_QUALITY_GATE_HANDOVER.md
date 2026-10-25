# Shaadi Aunty's Dodge — Three.js stays canonical

**Engine decision:** Three.js retained. No Godot or other engine migration.
**Gate:** SAD-VISUAL-QUALITY-V1 pinned, owner-approved visual style. The actual
master Blender rigs, playable visual parity and release remain UNAPPROVED.

## What the Three.js lane now does

- Preserves deterministic 10-second Three.js gameplay prototype in src/.
- src/artContract.js rejects incomplete owner receipts, evidence, license
  provenance, asset SHA-256 and mobile QA data.
- Browser checks actual GLB bytes using WebCrypto SHA-256 before parsing.
- Runtime checks skinned mesh, >=35 bones, exact Idle/Walk/Question/
  DodgeReaction clips, Blink/Smile/JawOpen morph targets, and editable
  wedding-scene mesh count before atomically replacing debug geometry.
- assets/asset-manifest.json intentionally starts wholly unapproved; debug
  procedural meshes must never be described as finished artistic assets.
- No production deploy or merge. Existing production gameplay unaffected.

## Verification on Dell, October 25 2026

npm test: **9/9 pass** (4 gameplay + 5 quality contract).
npm run build: success, js_gzip_bytes=168633 with Three.js 0.186.1.
The checks exercise logic and bundling; they DO NOT establish runtime mobile
FPS, human visual parity, rig retargeting, commercial source provenance,
or artistic quality. All those are independently blocking.

## Remaining hard blocks

- Character's actual real Blender source failed pinned visual review, not
  an approved Sharma Aunty.
- Current source lacks verified animated Idle/Walk/Question/DodgeReaction and
  Blink/Smile/JawOpen retargeted expressions.
- Wedding venue lacks the approved grand mandap's layered photoreal-stylized
  composition, mobile graphics/performance data, and certified provenance.
- Signed/persisted owner approval of exact binary hashes and a real-world visual
  art director review remain pending.
- Art GLBs are intentionally absent. No arbitrary manifest flag authorizes a
  deployment. The browser-side manifest is a fail-closed developer safeguard,
  not a trusted approval service or signed release receipt.

## Continuation path (Three.js only)

Blender professional sculpt+costume+rig -> independent Blender deformation
QA -> export sealed glTF/GLB -> glTF Transform/meshoptimizer optimization ->
Three.js staging with real animations and scene -> Playwright screenshots at
320px/390px/430px and real low-end Android FPS -> compare against all three
pinned visual references -> independent art director -> owner approval ->
release separately under explicit instruction.

Project-local node_modules is symlinked to preinstalled Dell dependencies
only while running tests, and excluded from version control.
