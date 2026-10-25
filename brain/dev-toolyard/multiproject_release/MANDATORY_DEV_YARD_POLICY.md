# Business House Matrix — mandatory Dev Tool Yard execution policy

Owner directive, 2026-10-25: **"always use the dev tool yard for dev work."**

This requirement applies across Delulu Tech, Moksha, Andaz, Pine and future registered projects. It supplements the already-deployed v0.2.2 global owner-intake and release gates.

1. All code generation, refactoring, asset-pipeline execution, frontend/backend changes, website builds, Android builds, game/tooling development, animation rendering and QA must be dispatched through an appropriately registered project-scoped **Dell Dev Tool Yard** workflow. Reuse the existing Gaming Dev Toolkit for gaming / hybrid motion as applicable.
2. Planning, research, writing, retrieval and reporting may be performed outside the Dev Tool Yard; external connector operations must not masquerade as a Tool Yard-certified software build.
3. Freeze the owner brief and acceptance matrix; submit only enrolled project/manifest actions. A shared library or shell route is not permission to bypass intake, isolation, testing, review or thermal checks.
4. Require actual build receipts, source/code hashes, fixture/viewport evidence, negative tests, rollback and explicit quality-gate result. A successful technical staging receipt is *not* design approval.
5. For sites, test at minimum 360px/390px mobile, tablet, desktop, reduced motion and browsers' actual rendered viewport; verify all media final states. Distinguish screenshot/headless artifacts from live browser defects with a reproducible test.
6. Keep production releases, DNS, publishing and spend behind a separate exact deployment approval bound to environment and output artifact hash. Do not use direct WordPress/Vercel/Cloudflare/SSH actions to sidestep the project governor.
7. Preserve production, V1 rollback snapshots and other project tenants. Future Dev Tool Yard capability upgrades require reviewed code, regression tests, backup and independent smoke receipts.

First scope using this policy: Delulu homepage V2 private static stage, build job `d941f739-a64d-451f-83b0-ec6450282cc6`, frozen SVG SHA256 `d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368`. The original V1 site remains untouched. No production release was requested or approved.
