# Delulu V2 — Interactive Hero Integration and Protected Preview (2026-10-25)

**Decision/status:** Private Vercel preview deployed and smoke-verified; **not production released / not independently human-certified**.

## Preview
- Vercel project: `prj_eWQI7KVuIF6xKszSyHFJupln734R` (`delulu-tech-v2-review`).
- Deployment: `dpl_BTknuhQoqnDMBwoXrU6YSwLvxod8`, READY, target **preview** (not a production promotion), URL https://delulu-tech-v2-review-muwuxpe2d-karanbizweb360-3479.vercel.app
- Vercel project retains SSO protection; a temporary share URL is available from authenticated Vercel interface, not preserved in public Git docs.
- Existing V2 marketing layout, header, sections and copy retained; the hero animation system alone was changed.
- Source in the **private** `aarondash5-star/delulutech` repository draft [PR #5](https://github.com/aarondash5-star/delulutech/pull/5), branch `review/delulu-v2-interactive-20261025`, path `website/v2-interactive/`.

## Three-level progressive enhancement
1. **Interactive real-time Three.js**: original SVG imported through `SVGLoader`, two original vector paths converted into `ExtrudeGeometry` with physical depth, morphed on the GPU to simulate four Blender-derived folding phases, automatic four-second sequence, pointer/touch tilt and replay. The path data are derived from the original SVG, not drawn as a replacement outline. Three.js modules `0.170.0` (MIT) loaded from a pinned jsDelivr URL. No glTF network payload required; CDN failure automatically activates level 2.
2. **Lightweight actual-fold video:** `assets/delulu-v4-light.mp4` 6,736 bytes, SHA-256 `970244cd3a82252e882b8cdb06d4d183a9608f963b5c4b4c5a3a94eceeac1bd4`. Used on data-saving/low-memory devices, WebGL failure, missing third-party modules or rendering errors. Uses the genuine Blender V4 animation, not rejected 2D mask video.
3. **Frozen approved SVG:** `assets/delulu-tech-mobile-white.svg`, SHA-256 `d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368`. Rendered immediately, for reduced-motion preferences, when skip is clicked, and when media cannot play; no blank hero.

## Dell browser and deployment QA
- Browser runner: Google Chrome via Playwright on Dell, local static serving; desktop 1440×900, mobile 390×844, reduced-motion mobile and data-saver mobile.
- Desktop/mobile: `logo-motion is-interactive`, real canvas present, no horizontal overflow, replay control present.
- Reduced motion: frozen logo visible, no WebGL canvas, replay hidden.
- Low-data: `is-playing` video fallback, no canvas, frozen SVG available on failure.
- Browser JavaScript parsed with `node --check`. Initial QA server root-path test error was repaired in the test harness and all four page behavior tests passed. One desktop 404 was favicon; favicon link added after test and the deployed SVG reference was verified HTTP 200.
- Vercel `get_deployment`: READY. `web_fetch_vercel_url`: index, JS and frozen SVG all returned HTTP 200. Deployment file tree verified **six** files and SHA1 references:
  - `index.html` SHA1 `4bfe7711c918103e21f075dbb5fb08142ae8ae4f`
  - `assets/interactive-motion.mjs` SHA1 `676824e5542754c8a1f0f2cb90fdceff9e52d091`
  - `assets/delulu-tech-mobile-white.svg` SHA1 `40abdc9e28e93258a4c2595e3cb1767e90a674e8`
  - `assets/delulu-v4-light.mp4` SHA1 `303885bf848a8a977050675a0196a60007b8240c`
  - `robots.txt` SHA1 `63657cbb7d7086c56b0cd4e5c6999bb683664868`
  - `vercel.json` SHA1 `b9998fe07397abd49397c576d3ca4271b1de7f4c`
- `robots.txt`, `X-Robots-Tag`, `noindex` retained for review preview.
- Temporary URL authorization is scoped to the specific deployment; no changes to global SSO/project access rules.

## Release/certification boundaries
- No changes to Delulu production website or current V2 default alias, no merge, no spending or permission changes, no changes to the original frozen logo.
- The dynamic interactive renderer is a **new browser implementation**, procedurally using V4 geometric deformations on the frozen SVG. It is not a direct playback of the V4 Blender .blend or glTF scene. The 3D *rendered appearance* still requires owner creative acceptance.
- Independent signed human visual/media QA and global Dev Yard Manager autonomous dispatch/connector certification remain pending. This preview build does **not** confer release authorization.
- Main quality-admission owner release gates remain closed.

**Next:** Owner verifies desktop and mobile visual appearance from the preview. If accepted, complete authenticated independent review and explicit production release gate before merging or changing live aliases.
