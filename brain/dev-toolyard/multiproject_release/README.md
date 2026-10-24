# Multi-project Matrix Dev Tool Yard — production release v0.2.0

Owner approval: 24 Oct 2026. Source: Issue #19. Scope: the Dell Matrix controller and locally isolated Dev Tool Yard; **not** external website publication.

## What changes

- Retains `moksha_overhaul/moksha_overhaul_v1` on the identical legacy staging renderer.
- Adds `project_registry_v1.json`: owner-reviewed exact project, action and manifest tuples. No wildcard, executable path, shell command or secret may be supplied through a task brief.
- Adds `dev_project_build`: accepts an enrolled reviewed patch from the private engineering inbox, applies it in a per-project Bubblewrap workspace using the existing Tool Yard patch runner, and executes the project's tests. Failed tests remain needs-review.
- Adds `website_stage` static-v1 runner for enrolled projects with SHA-256-pinned local assets and `noindex`; never starts a web server, publishes, spends or calls outside APIs.
- Adds precise SHA checks on the currently installed controller/patch runner, staged compile and regression tests, durable rollback copy, service restart/readback. The installer fails closed on mismatches and restores prior binaries if activation fails.

## Adding the next project (no new controller code)

1. Record owner approval in the project task envelope and review its exact project identifier/manifest.
2. Add a single registry entry naming the project and approved `website_stage` or `dev_project_build` manifest. Maintain mode 0600 on the owner-local production registry. No all-project wildcard is supported.
3. For `dev_project_build`, place the reviewed patch JSON at `engineering-inbox/<project>/<manifest>.json`; it must use the existing isolated allowed extensions and provide runnable `tests/test_*.py` or `tests/*.test.js`.
4. For `website_stage` (static-v1), provide `staging-inbox/<project>/<manifest>.json` with exact SHA-256 hashes and the corresponding files in `staging-inbox/<project>/<manifest>/site/`.
5. Check `project_registry.py check <project> <action> <manifest>`, run project-specific negative tests, then submit through `controller.py submit <project> <action> <manifest>`. The controller consumes one bounded task and records QA receipts.
6. Promote only separately authorized artifacts after review. Do not infer public site publication from a private stage.

## Current initial entries

- Moksha: legacy private `website_stage`.
- Delulu Tech: `dev_project_build` and private static `website_stage`.
- Pine: isolated reviewed-patch capability.
- Andaz website: isolated reviewed-patch capability; deployment input pending.

## Rollback

The release installer writes a timestamped backup under the existing controller's `release-backups` path, holding the byte-for-byte old controller and reviewed patch runner. On an activation/test failure, the installer restores both, removes only the three freshly installed release modules (if it created them), and restarts the prior user service. It does not change root/sudo permissions, network exposure, billing or publishing.

## Limits

This release upgrades deterministic execution of reviewed project code and private static site staging. It does **not** automatically grant a proposal-only AI model the right to write arbitrary code, auto-merge, spend, access foreign secrets or publish. Model-created patches must still enter the reviewed patch inbox with independent QA. For dynamic apps beyond static websites, use project-isolated Dev builds and a separately reviewed deployment recipe.

## Acceptance tests

- Existing Moksha enrollment PASS; Delulu enrollment PASS; Andaz reviewed patch enrollment PASS.
- Foreign project/manifest and path traversal DENIED.
- Existing controller self-test PASS.
- Project sandbox doctor PASS, no network/foreign project/home exposure.
- Controller service ACTIVE after promotion, version `0.2.0-multiproject` visible.
- Delulu private static stage only after its source/manifest checksum package is explicitly prepared; public release remains blocked.
