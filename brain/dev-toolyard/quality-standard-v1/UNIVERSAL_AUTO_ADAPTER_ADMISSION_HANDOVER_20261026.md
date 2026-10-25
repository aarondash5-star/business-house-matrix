# Dell Dev Tool Yard — Universal Auto-Adapter Admission (Handover)
**Date:** 2026-10-26 (IST)  
**Project:** Business House Matrix → Dell Dev Tool Yard  
**Status:** Owner direction APPROVED; **auto-adapter discovery, generation and enforcement NOT yet implemented or certified**. This file is the execution contract for the next chat.  
**Change scope:** Controller/admission layer and reviewed Tool Yard launcher/adapters. Do not silently change production websites, external credentials, system ACLs or release permissions.

## Decision: default admission for every tool

**Universal rule:** *Any tool entering or already present in Dell Dev Tool Yard must have a verified, versioned, project-scoped QA adapter. If it has none, discover/reuse a compatible approved adapter or produce a narrowly scoped adapter, test it, certify it and then enroll it. Until certified, the tool remains quarantined/unavailable for live Tool Yard dispatch.*

**Admission is not production authorization.** A tool may be allowed to perform approved tasks after adapter certification; publishing, merging, spending, credential/security changes and production deployment remain separately owner-approved under the existing release gates.

The rule applies to: controller actions, registered tools, newly installed or discovered CLIs, browser operators, Blender/ffmpeg, game/website engines, tests, Python/Node/Build tools, Git/GitHub, Vercel, WordPress, MCP/external provider connections, local workers and future tools. Scope applies to operations routed through the governed Tool Yard. Direct SSH/root/shell and third-party connectors are **not actually intercepted today**; universal enforcement across those paths requires reviewed mediation/isolation before claiming completion.

## Required admission state machine

`DISCOVERED → QUARANTINED → ADAPTER_CANDIDATE → SANDBOX_TESTED → INDEPENDENT_QA → ADMITTED → ACTIVE`

Negative branches: `DENIED` (security/license/scope failure), `REMEDIATION` (fix and retest), `REVOKED` (drift, regression, expired approval). **No transition may skip verification.**

1. **Detect and register:** At startup, installation, discovery, dependency change and task intake, enumerate declared tool identities, executable locations/package IDs, versions, exact SHA-256/source of provenance, license, capabilities, environments and requested resource access. Track stable tool ID distinct from human-readable name. Do not read/expose secrets.
2. **Default-deny:** Unknown or changed executable, plugin or connector is `QUARANTINED` and cannot join the live dispatch registry; enforce at every actual execution entrypoint rather than only attaching a post-execution receipt.
3. **Reuse before creating:** Match a compatible audited adapter by tool family, version range, capabilities, OS/platform and declared permissions. Prefer OSI-approved open-source references/packages. If no suitable adapter, build a scoped fixed-function adapter within the already approved execution architecture—**not** arbitrary unrestricted shell or elevated root/secret access.
4. **Admission contract:** Bind `tool_id`, `adapter_id/version/hash`, project/manifest/frozen brief hash, permitted actions, filesystem/network/credential scope, capability schema, risk tier, dependency/license inventory, test plan, independent reviewer ID, owner authorization requirements, recovery behavior and expiry/drift policy. Preserve tenant and project isolation.
5. **Test before enrollment:** Syntax/compile, unit and integration, negative/security, unauthorized-tool denial, cross-project spoofing, idempotency, rollback, timeout and resource limits, genuine functional behavior, no-network/rootless sandbox QA. For visual/media/UI tools require actual visible screenshots/frames and interactive behavior on desktop/mobile, reduced-motion, fallbacks and relevant Lighthouse/axe checks. Do not treat a successful wrapper invocation as substantive tool QA.
6. **Independent admission:** Collect signed/pinned receipts bound to exact tool/adapter/source hashes, in a reviewer-controlled trust store; model/developer cannot self-sign. A user-approved project scope and independent technical QA can admit an adapter for allowed **development operations**; owner release authorization is separate for production actions.
7. **Atomic activation:** Only after successful tests, enroll in a versioned allowlist/registry, make the adapter discoverable to the controller's dispatcher, and execute a bounded canary. Save pre-change registry/controller checksums and rollback receipt. Failed canary restores previous registration and quarantines candidate.
8. **Continuously reconcile:** On tool version/hash change, adapter change, permission change, expiry, failed regression or removal, automatically re-quarantine and retest. Existing tools get grandfathered into *inventory*, **not** grandfathered into ACTIVE certification. Include an admission status API/CLI showing `ADMITTED`, `ACTIVE`, `QUARANTINED`, `REVOKED`, reasons and evidence links.

## Single source of truth and architecture

Retain existing Dell controller `matrix-controller/controller.py`, registry `project_registry_v1.json`, `quality_gate.py`, `quality_admission.py`, `toolyard_qa_standard_v1.py` and `toolyard_qa_audit_v1.py`. No replacement of V6 gates or duplicate release authority. Implement reusable additions under existing controller architecture, for example:
- `tool_adapter_registry_v1.json` (machine-readable identities, adapters, scopes, lifecycle state, pinned evidence; *never credentials*).
- `tool_adapter_admission_v1.py` (discover, match/reuse, deny, stage, independent QA, admit, verify drift, revoke, inspect).
- `tool_adapter_dispatch_v1.py` (admission preflight on every mediated invocation; strictly deny unknown/quarantined tools).
- `tool_adapter_audit_v1.py` (inventory coverage, missing adapters, stale hashes and bypassable entrypoints).
- Separate tests and durable evidence receipts, Git handover and rollback procedure.
These filenames are a proposed convention, **not files already created**.

Make automatic attachment the **default behavior** for future supported tools: discovering a tool schedules or stages adapter onboarding; it does **not** automatically grant permissions or run untrusted executables. Existing universal QA receipt requirements remain mandatory in addition to adapter admission.

## What is already implemented and verified (do not re-do or overclaim)
- Controller universal QA V1 deployed for all **13 registered controller actions** and smoke-tested. Controller post-upgrade SHA-256 `86c5c9d7dfb33abf186d05ad1146f7a941deaf6401b87ba1b565f4aa238e1617`.
- Policy tests **8/8 PASS**; in-memory controller actions **13/13 PASS**; real isolated rootless/no-network QA batch `toolyard-universal-qa-v1-20261025-r2` **6/6 PASS**, job `18d2ff0d-39d0-4825-a520-53cea535e3a7`.
- Existing controller release/owner/independent-QA gates unchanged. Private Dell backup `/var/lib/generic-linux-automator-exec/matrix-controller/release-backups/toolyard-universal-qa-v1-20261025/` with promotion receipt.
- Legacy tools executed via direct standalone CLI **NOT** automatically mediated; current controller audit explicitly flags external connectors as unmediated.
- Delulu Tech V2 motion trio frozen at commit `261306b00ce070e2f61db3a510dd0729351c33b0`, branch `frozen/delulu-v2-motion-trio-v1-20261025`; PR #7 separate for quality improvements. No production merge.

## Acceptance tests for the next session

- Newly discovered unregistered tool: cannot dispatch or release; recorded as `QUARANTINED`.
- Safe existing adapter, exact identity/scope: reused without privilege expansion; requires matching QA.
- Missing adapter: scoped candidate created and tested; **not ACTIVE** until independent admission.
- Modified binary/hash, adapter signature, manifest or scope: denied/re-quarantined.
- Spoofed project/manifest, forged independent signature, forged `published:true`, cross-project request: rejected.
- Admission failure, canary failure and rollback: prior live tools unaffected and immutable receipts produced.
- Legitimately admitted tool: executes only its fixed capabilities, with universal QA receipt, no implicit publishing.
- All 13 preexisting controller actions and selftest remain working.
- Every discovered CLI/connector listed as covered, quarantined or awaiting an enforceable mediation path; **never mark whole-yard coverage 100% while raw SSH/external routes remain bypassable**.
- Document tool-specific QA coverage and no-spend/non-root controls; no credentials in source/receipts.

## Reference docs
- [Universal QA standard](https://github.com/aarondash5-star/business-house-matrix/blob/feat/dev-yard-manager-bmad-langgraph-speckit-intake-20261025/brain/dev-toolyard/quality-standard-v1/QA_UNIVERSAL_STANDARD_V1_20261025.md).
- [Dell current coverage ledger](https://github.com/aarondash5-star/business-house-matrix/blob/feat/dev-yard-manager-bmad-langgraph-speckit-intake-20261025/brain/dev-toolyard/quality-standard-v1/DELL_COVERAGE_AND_ROLLOUT_20261025.md).
- [Delulu frozen website and QA handover](https://github.com/aarondash5-star/delulutech/blob/optimize/delulu-v2-10x-quality-20261025/website/v2-interactive/qa/DELULU_WEBSITE_FROZEN_AND_QUALITY_HANDOVER_20261025.md).
- Existing review PR: [Business House Matrix #27](https://github.com/aarondash5-star/business-house-matrix/pull/27).

**Stop condition:** If an adapter would require new permissions, arbitrary shell, secret disclosure, unreviewed root access, production publishing or bypassing a provider security denial, stop at `QUARANTINED` and request the correct narrowly scoped authorization. Do not automatically override those controls.
