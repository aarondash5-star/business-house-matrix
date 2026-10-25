# Handover — Universal Auto-Adapter Enrollment for Dell Dev Tool Yard
**Date:** 2026-10-26 IST
**Project:** Business House Matrix / Dell Dev Tool Yard
**Status:** REQUESTED, DESIGN HANDOVER ONLY. **Do not claim auto-adapter enrollment was implemented or deployed in this handover.**

## Owner's latest decisions
1. Implement a **yard-wide universal rule** that automatically attaches to **every tool** in the Dell Tool Yard, both currently present and newly introduced.
2. **Any tool without an approved adapter must first receive an appropriate adapter and pass admission/QA** before becoming an accepted/live Tool Yard tool.
3. Govern all projects by the same quality/security/release principles. Do not relax existing project boundaries, owner permissions, no-spend requirements, review procedures, or rollback.

## Verified starting point
- Dell controller `/var/lib/generic-linux-automator-exec/matrix-controller/controller.py` SHA-256 `86c5c9d7dfb33abf186d05ad1146f7a941deaf6401b87ba1b565f4aa238e1617` from prior completed rollout.
- Universal QA module `toolyard_qa_standard_v1.py` applies project/action-specific conservative QA receipts to **13/13 controller-mediated action types**. It **does not intercept arbitrary direct SSH/CLI executions** or external connectors.
- Previous verification: 8/8 unit tests; 13/13 in-memory receipt paths; 6/6 rootless/no-network independent QA. Existing owner/release gates remain separate.
- Existing canonical standards: [QA Universal Standard V1](./QA_UNIVERSAL_STANDARD_V1_20261025.md) and [Coverage Ledger](./DELL_COVERAGE_AND_ROLLOUT_20261025.md).
- Source repo `aarondash5-star/business-house-matrix`; feature branch `feat/dev-yard-manager-bmad-langgraph-speckit-intake-20261025`; draft PR #27.
- Prior visual QA lessons from Delulu V2 (HTML 200 and WebGL canvas presence do **not** prove a visible result) should apply universally, adapted by tool category.

## Next implementation — fail-closed enrollment
Implement a shared **Tool Discovery → Adapter Selection/Creation → Sandbox Certification → Registry Admission → Authorized Invocation → Project QA Receipt → Release Gate** pipeline.

1. **Discover** installed Dell tools, tools exposed by app/plugins and registered capabilities. Inventory tool name, version, origin, binary path/API, supported operations, project scope, license and trust status without scraping secrets. Do not automatically alter global PATH or untrusted system tools.
2. **Select or generate a bounded adapter** based on capability family (CLI process, media/Blender/ffmpeg, browser/Playwright, Git/deployment, WordPress/CRM, API/research/AI, test/build, etc.). Favor reusable, source-controlled adapters and existing official tool schemas. Default capabilities to *minimum safe permission*, no arbitrary shell/root.
3. **Stage adapter:** newly discovered tools get `pending_adapter`; once candidate adapter exists, `qa_pending`. Never silently interpret auto-generation as certification. Unknown, untrusted or denied tools remain `quarantined` or `denied`.
4. **Certify:** run contract/schema, version/license, project-binding, negative security, tenant isolation where relevant, sandbox, dry run, source SHA, rollback and independent QA tests. For visual tools require real rendered pixels/frames, desktop/mobile, accessibility and fallbacks.
5. **Admit:** only when all required technical checks have genuine evidence mark `accepted_for_scoped_execution` and register the fixed-function adapter. Project-specific trust and permissions still apply. Any missing gate must fail closed.
6. **Invoke:** route Tool Yard manager/brain requests through the central registry/admission dispatcher so each tool automatically inherits Universal QA Standard V1. Log tool ID, adapter version, project/manifest, scope, artifact/input hashes, test receipt, approver when needed and outcome.
7. **Release separately:** `accepted_for_scoped_execution` **never** means permission to merge, spend, publish or deploy production. Keep pre-existing `quality_admission.release_check`, independently controlled reviewer evidence, owner-specific release decision and rollback.
8. **Continuous checks:** detect versions/new tools and reclassify changed tools as `revalidation_required` until approved. Maintain a dashboard of `discovered / adapter_pending / qa_pending / accepted / blocked / retired`. Record exceptions explicitly, never falsely report whole-yard coverage.

## Non-negotiable acceptance tests
- Existing registered 13 actions remain functional, project-isolated and conservative.
- New safe tool with no adapter: **cannot run**, adapter candidate created/staged, negative/positive certification tests required, accepted only after QA.
- Unknown or malicious/untrusted tool and mismatched project/manifest: denied.
- Fake approval, fabricated SHA/quality score, invalid reviewer or attempted publishing: denied.
- Standalone direct tool not mediated by yard: **must be recorded as unmediated**, not falsely marked universally controlled. Use approved managed entrypoints; do not claim transparent interception of all operating-system processes without an actual mechanism.
- Version change/revoked adapter/failed sandbox test: automatic de-admission and no live execution.
- No changes to frozen Delulu V2, production, existing project applications, secrets, root security, external spend or owner permissions during certification.

## Suggested deliverables
- Source-controlled `tool_adapter_registry`, `adapter_factory` (templates with strict allowlists), `tool_admission_guard`, `qa_receipt_bridge`, `inventory_auditor` and reference adapter schemas.
- Immutable enrollment journal, rejected fixtures, approval/rollback receipts, coverage table by *actual tool*, and smoke tests in the Dell Tool Yard controller.
- Document exact Git commits, reviewed patches, runtime checksums, Dell worker status, remaining external/unmediated gaps and a concise user-facing GO/NO-GO verdict.

## Current execution boundary
This document only records the next task. The user's immediate request was **"document and very short prompt for new chat"**; automatic adapter generation/enrollment must be performed and verified in the next execution conversation, not backdated as already implemented.

## One-line handover
Continue from this document and the canonical Dell universal QA standards. Implement default-on, fail-closed adapters for existing/new tools, independently test admission and denial, preserve owner release gates, document receipts, and report remaining coverage gaps.
