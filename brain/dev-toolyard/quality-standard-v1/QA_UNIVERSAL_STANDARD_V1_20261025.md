# Dell Dev Tool Yard — Universal QA Standard V1

Effective 2026-10-25. Canonical reference: Business House Matrix Git,
`brain/dev-toolyard/quality-standard-v1/`.

## Coverage and certification boundary
- ENFORCED: all **13 controller-registered actions** via
  `controller.py -> toolyard_qa_standard_v1.receipt()` for newly completed tasks.
- NOT ENFORCED: direct arbitrary SSH commands, unmanaged CLI tools, external
  connectors, and legacy completed tasks. These require reviewed adapters
  and explicit onboarding before counting as certified.
- Existing scope enrollment, owner intake/release, independent QA,
  blocked production routes, no-spend rules and rollback remain unchanged.
- QA receipt is **technical only**; independent-human, design,
  10/10-quality and production-authorized flags always false.

## Mandatory gates for every new project/tool
0. Bind exact project/manifest, frozen brief, authorized owner scope.
1. Translate every frozen requirement to testable acceptance criteria;
   hash sources and accepted assets, no omitted must-haves.
2. Pin open-source libraries, real origin/license/version and SHA,
   check third-party privacy and security boundaries.
3. Execute actual unit/integration/negative tests; isolated sandbox QA
   and source-to-result trace. Syntax alone does not certify a build.
4. For creative/media/GUI: real screenshots of *actual deployed URL*,
   visible nonblank pixel and geometry assertions, pointer/touch/replay,
   desktop/mobile, reduced-motion, network/WebGL failures, frozen fallback.
   A DOM canvas or HTTP 200 is **not** proof of successful rendering.
5. Performance, security, accessibility and reliability:
   Lighthouse mobile/desktop, TBT/LCP/CLS, axe-core, manual keyboard,
   contrast/screen-reader where necessary, threat tests, rollback.
6. Business/marketing: real offer, real CTA and contact endpoint,
   sourced proof and consent. No invented clients/metrics/ratings.
7. Independent reviewer, distinct from developer/model; outside AI
   opinions must be labeled AI and are not human review.
8. Production: explicit artifact-matched owner release approval,
   independent signed QA and existing release_check preflight.
9. Record SHA-pinned Git source, candidate/frozen branches, tests,
   known bad fixtures, real link, recovery, uncompleted blockers.

## Profile-based requirements
`research_search,dev_docs_fetch` retrieval;
`dev_proposal` documentation;
`dev_scoped_build,dev_general_build,dev_project_build,pine_chat_stage`
functional app; `game_toolkit` interactive media;
`website_stage` creative web; `sandbox_qa` verification;
`repair_known_issue` automation; `marketing_draft` marketing;
`video_preview` media. All 13 are mapped; unmapped actions fail closed.

## Real evidence, not artificial scores
Lighthouse 100 on a non-indexed preview is impossible due to intentional
noindex; never disable staging privacy for a synthetic SEO score. A locally
indexable 100 is not public Google indexing. Automated accessibility 100
still requires manual usability reviews. Commercial 10/10 requires real
visitor/conversion results; model judgments cannot be used as receipts.
Measure repeatedly, preserve mobile/fallback quality and actual controls.

## Exact activation and rollback
Controller before: `6c1442395ea1377794045c55ed6424b586161a7e48db706a538063b14deb11a8`
Controller now: `86c5c9d7dfb33abf186d05ad1146f7a941deaf6401b87ba1b565f4aa238e1617`
Module: `72cf039354320221928f148290b526af83480dbf4b82315a7e12107d333b92ea`
Private backup `release-backups/toolyard-universal-qa-v1-20261025/`
with promotion and rollback receipt. Do NOT rollback with live in-flight tasks.
Controller selftest PASS; unit tests 8/8; in-memory 13/13 action receipts;
rootless no-network QA batch `toolyard-universal-qa-v1-20261025-r2`
6/6 PASS, job `18d2ff0d-39d0-4825-a520-53cea535e3a7`.
First QA attempt failed with sandbox directory permissions, preserved;
corrected with 0755 dir/0644 files, no bypass or privilege expansion.

## For future tools or projects
1. Enroll a project-specific manifest and immutable brief under the
   existing owner-governed registry.
2. Route through one of the existing 13 action profiles if possible;
   changing controller allowlists requires reviewed source and QA.
3. For external/CLI-only tools, supply an adapter that invokes the
   same QA profile, stores evidence, and respects owner release controls;
   until certified mark `not_covered`.
4. Rerun scope/negative/cross-project tests, rootless QA and rollback
   certification before promotion. Never claim global enforcement for
   unmanaged standalone executables.

## Audit
```bash
cd /var/lib/generic-linux-automator-exec/matrix-controller
python3 controller.py selftest
python3 -m unittest -v test_toolyard_qa_standard_v1
python3 toolyard_qa_audit_v1.py
python3 controller.py show 18d2ff0d-39d0-4825-a520-53cea535e3a7
```
