# Shaadi QA Preview Deployment Gate

Deploy target: isolated `preview/shaadi-lane1-quality-20261028` Git branch.

Cloudflare Pages build command: `node qa-preview/build-gate.mjs`; output folder: `qa-preview`.

The gate validates pinned hashes of all preview assets plus original 36/36 browser, 8/8 brand, and 4/4 CDN smoke-test receipts. Build failures block newly modified or uncertified previews.

Only synthetic staging assets are published. Main branch, game production, Blender rigs, and owner-frozen art lanes are untouched.
