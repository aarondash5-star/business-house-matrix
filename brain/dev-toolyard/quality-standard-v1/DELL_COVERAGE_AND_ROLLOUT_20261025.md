# Dell Dev Tool Yard — QA V1 Rollout, Coverage & Certification Ledger

**Date:** 2026-10-25 (IST)  
**Reference standard:** [Universal QA Standard V1](./QA_UNIVERSAL_STANDARD_V1_20261025.md)  
**Scope:** All current and future Dell Tool Yard work must follow one quality process. **Runtime enforcement is currently limited to the 13 controller-mediated actions.** Direct tools still need reviewed adapters; do not label them certified.

## What was really changed

On Dell `dell-linux`, the central controller gained `toolyard_qa_standard_v1.receipt()` for **every new completed controller task**, instead of only the prior partial annotation for certain artifact builds. It uses the actual project, action, manifest and existing quality contract; includes the required profile-specific test list, and explicitly sets `independent_human_accepted=false`, `production_release_authorized=false`, `score_10_of_10_certified=false`. Forged `published:true`, `design_complete:true` or `release_authorized:true` output is rejected, not promoted.

Already-existing `quality_gate.py`, `quality_admission.py`, registry, owner ledgers, project isolation, cost/security policy, V6 controls and rollback logic remain in place. **No default release, signoff, publishing or spending authority was created.** The controller still reports `external_connectors_mediated=false`.

### SHA-verified runtime and rollback

| Artifact | SHA-256 |
|---|---|
| Controller before | `6c1442395ea1377794045c55ed6424b586161a7e48db706a538063b14deb11a8` |
| Controller after | `86c5c9d7dfb33abf186d05ad1146f7a941deaf6401b87ba1b565f4aa238e1617` |
| Universal standard module | `72cf039354320221928f148290b526af83480dbf4b82315a7e12107d333b92ea` |
| Standard unit tests | `26f3d3bb32e8418d5a677da36bbc3d200106ee1c39985e7ad2b209209e9d8b7f` |

Owner-private backup:
`/var/lib/generic-linux-automator-exec/matrix-controller/release-backups/toolyard-universal-qa-v1-20261025/`. It contains old and candidate controllers, policy/test copies and `PROMOTION_AND_ROLLBACK_RECEIPT.json`. No private host paths or tokens have been converted into public deployment secrets. Never restore over an in-flight job.

### Real smoke tests and failure trail

- Controller original safety selftest: **PASS** after promotion (read-only research, idempotency, blocked production, unapproved build denial, project isolation, privacy, conservative recovery).
- Universal standard tests: **8/8 PASS** including unknown action, forged approvals, foreign project, incomplete/invalid SHA reports.
- SQLite simulated controller receipt integration: **13/13 profiles PASS**, forged publication claim explicitly rejected.
- **Rootless/air-gapped independent QA**: batch `toolyard-universal-qa-v1-20261025-r2`, `6/6 PASS`, real controller job `18d2ff0d-39d0-4825-a520-53cea535e3a7`. `universal_quality_standard` persisted in its output with release/human/10-of-10 **false**.
- An earlier first batch `57f25b46-899c-4bdd-b598-35d18715a6b3` failed due to a `0700` directory inaccessible to the non-root container user. Corrected batch used `0755` directory and `0644` source, no privilege bypass; immutable failure receipt preserved.
- `python3 toolyard_qa_audit_v1.py` confirms **13 mapped, zero unmapped/stale registered actions** and reports standalone tools separately.

## Profile rollout across ALL 13 controller capabilities

| Controller action | Quality class | Required essentials |
|---|---|---|
| `research_search`, `dev_docs_fetch` | Retrieval | Source/provenance; bounded no-write facts |
| `dev_proposal` | Documentation | Source trace; frozen brief; reviewer |
| `dev_scoped_build`, `dev_general_build`, `dev_project_build`, `pine_chat_stage` | Functional app | Unit/negative/security; auth; UI if applicable; recovery |
| `game_toolkit` | Interactive media | Real visuals/asset origin; interaction/touch; fallbacks; independent QA |
| `website_stage` | Creative website | Pixel-visible desktop/mobile screens; SEO/a11y/perf; failover; marketing claims |
| `sandbox_qa` | Independent verification | Rootless no-network tests; negative evidence; terminal receipts |
| `repair_known_issue` | Automation | Scoped repro; adversarial tests; recovery |
| `marketing_draft` | Marketing | Evidence-backed claims, human review, permission to spend |
| `video_preview` | Media | Real source frames, audio/caption QA, rights, owner review |

**Critical:** These are requirements recorded on newly completed tasks. They do not mean every action has executed each check. Existing quality gates only release when genuine independent evidence and owner authorization exist; retroactive historical tasks remain legacy-unassessed.

## Dell tools and workspaces discovered; adapter status

**CLI found:** Python, Node, npm, Git, Blender, ffmpeg, Google Chrome, Podman, npx, GitHub CLI. These executables are **not individually hooked to controller QA** when used directly via SSH. `vercel` CLI and a global `pytest` binary were not found; deployment API and isolated Python/unit test tooling may still be available through supported routes.

**Existing Dell workspaces inspected for presence:** `matrix-controller`, `threejs-tool-yard`, `matrix-game-toolkit-20261025`, `delulu-site-v2-20261025`, `matrix-andaz-site-v2-20261023`, `wp-manager-oauth-gate-20261025`, `eccrm-wordpress-qa-20261025`, plus existing Matrix development/release workspaces. Mere presence is **not** proof of tool-specific certification.

| Tool family | Standard to require | Runtime admission status |
|---|---|---|
| Python / Node / npm app build | Frozen manifest, unit/negative/reload/security receipts, dependency hash, release approval | Enforced when controller-mediated; direct CLI **pending adapter** |
| Blender / ffmpeg / 3D or video assets | Original SHA, actual frame/geometry fidelity, playable previews, sampled screenshots, human visual approval | Through enrolled media/game actions where supported; raw CLI **pending** |
| Chrome / Playwright / Three.js / web builders | Actual screenshot pixel assertions and behavior, mobile/touch, reduced motion, Lighthouse, axe, fallbacks | Governed website/game actions require profile; standalone browser **pending** |
| Podman rootless QA | No network, read-only workspace, non-root, negative tests, immutable receipts | Governed sandbox path **verified** |
| Git / GitHub / CI / Vercel deployment | Frozen SHA, signed verification, explicit independent QA and owner release, rollback | Controller owner release gate exists; external Git/Vercel APIs **not universally mediated** |
| WordPress / CRM / WP Manager / OTA | Tenant isolation, auth/security, regression, data minimization, staging and human approval | Project-specific tools need explicit adapters and live QA certification |
| AI research / marketing / external APIs | Provider/source provenance, no fabricated evidence, consent/privacy, free/no-spend policy | Governed retrieval path where applicable; external models outside controller **not auto-governed** |

## Mandatory future onboarding to achieve *actual* whole-yard enforcement

1. For every standalone tool, identify the specific project/owner scope and register a fixed-function adapter in the existing action registry (or a separately reviewed controller action). **Never authorize unrestricted commands to solve an integration failure.**
2. Bind exact manifest, immutable brief, source and artifact SHA. Treat unknown sources/tools as fail-closed.
3. Apply the relevant universal profile and project contract; require genuine rootless negative tests.
4. Attach authentic artifact-local receipts and build hash, with visual pixels/screenshots and functional interactions where relevant.
5. Keep reviewer identities independently controlled; do not accept self-generated reviewer signatures.
6. Integrate into the existing `quality_admission.release_check`, **not** a parallel publish bypass. Preserve explicit owner approval and receipt scope.
7. Certify and document preflight, rollback, deny tests and canary before marking that particular adapter `certified`; otherwise `pending`.

**Open blocker:** Dell’s Manager v2 global multi-project autonomous role orchestration and external connector mediation are **not** certified by this policy rollout. The earlier Delulu challenge identified cross-project identity binding/independent-human evidence concerns. Universal QA receipt addition does not automatically resolve those.

## Permanent Dell reference and verification

Local: `/var/lib/generic-linux-automator-exec/matrix-controller/docs/QA_UNIVERSAL_STANDARD_V1_20261025.md`  
Auditor: `/var/lib/generic-linux-automator-exec/matrix-controller/toolyard_qa_audit_v1.py`

```bash
cd /var/lib/generic-linux-automator-exec/matrix-controller
python3 controller.py selftest
python3 -m unittest -v test_toolyard_qa_standard_v1
python3 toolyard_qa_audit_v1.py
python3 controller.py show 18d2ff0d-39d0-4825-a520-53cea535e3a7
```

**Project reference:** [Delulu website frozen-quality handover](https://github.com/aarondash5-star/delulutech/blob/optimize/delulu-v2-10x-quality-20261025/website/v2-interactive/qa/DELULU_WEBSITE_FROZEN_AND_QUALITY_HANDOVER_20261025.md).

**Decision:** controller-mediated QA standard **DEPLOYED AND SMOKE-VERIFIED**; whole Dell CLI/tool ecosystem QA enforcement **PARTIALLY IMPLEMENTED / pending individually reviewed adapters**. No production domain/site, owner-release or security settings changed.
