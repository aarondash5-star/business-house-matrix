# Dev Operator v6 — Full Release QA, Smoke Tests and Security Debugging

**Date:** 22 October 2026 (IST)  
**Project:** Business House Matrix (independent from Moksha Master)  
**Release classification:** **CERTIFIED / LIVE for enrolled, offline static-HTML Dev Operator only.**  
**Security result:** Previous v5 HTML acceptance gate **FAILED adversarial testing**. Corrected in v6.  
**Full general-purpose software engineering autonomy:** **NOT certified**.

## Executive verdict

The installed scoped Dell Dev Matrix now operates with the **v6 hardened static-HTML policy**, and a NEW controller-dispatched task completed with independent Bubblewrap QA and an unpublished Git review. Both Dell and Mac ran **38/38 passing source, policy, sandbox, and adversarial regression tests**; six Generic SSH lanes passed. Browser QA of the new v6 artifact passed **7/7** viewport tests.

The initial v5 release failed deeper negative security QA. The two earlier generated pages are historical receipts, not retroactively upgraded or certified under the new policy.

## Initial v5 security fault

A targeted no-side-effect audit of `brain/dev-operator/agent_loop.py` proved five classes of invalid HTML content could bypass the original regex-only output filter:

| Adversarial HTML class | Old v5 validator |
|---|---|
| Inline DOM event attributes | **Incorrectly accepted** |
| Meta refresh redirect | **Incorrectly accepted** |
| Object/embed elements | **Incorrectly accepted** |
| CSS external resource loads | **Incorrectly accepted** |
| JavaScript URL attributes | **Incorrectly accepted** |

Dell negative test receipt: `a630a50a-bdb3-4373-99d5-4a56046b9301`. This was a **QA/security release defect**, not evidence that generated code was executed.

Historical local review outputs were rechecked under v6: v4 rejected (`metadata_outside_head`); v5 rejected (`active_or_unknown_element`, interactive input outside the static-profile allowlist). The old task history was preserved without rewriting outcomes. These historical demo pages should not be treated as independently security-certified under the new policy.

## Root cause and fixes

- Old `parse_single_html` rejected obvious `script`, `iframe`, HTTP URLs and `fetch()` text only, not the full HTML element/attribute/CSS surface.
- Old independent Bubblewrap QA checked `html`, `main` and viewport presence, not active-content safety.
- New `brain/dev-operator/static_html_policy.py`: strict HTML5 structure; allowlisted inert tags/attributes; rejects active HTML elements, event handlers, link/src protocols, meta refresh, embedded assets, forms, CSS remote resource/expression features and malformed document structure.
- `agent_loop.py` now invokes the strict parser before proposal acceptance, and its model prompt requests complete inert `head` / `body` markup.
- `workcell_worker.py` independently runs the same strict validator during sandbox QA; `workcell_runner.py` binds the trusted validator into Bubblewrap read-only.
- Initial patch test exposed a check-name mismatch (`html_semantics` vs `html_semantics_and_active_content`); corrected in commit `2ea1e3c64f1e66916dec430255b62edcc9294c3f`. Afterward both hosts passed full suites.

This is conservative static document validation, **not** a general-purpose HTML sanitizer for arbitrary production web applications.

## Tested release

| Gate | Evidence | Result |
|---|---|---|
| Existing v5 runtime before patch | Active SHA256 `df0cf3f968244d2e745d941f57d2225cfcd4a4147f55f7ce29c879e87027ffe4` | Preserved for rollback |
| Security regression + unit tests (Dell) | 38/38, receipt `a816d538-9796-4a13-850d-e8c8d7e9471d` | PASS |
| Independent peer QA (Mac) | 38/38, receipt `687039e8-e11e-43cc-8af2-e9183607fe5d` | PASS |
| v6 controller self-test Dell/Mac | Both PASS, release source commit `e1d97ba35ff74c5446126891d8f56e54ac42c975` | PASS |
| Six SSH lanes (Dell+Mac) | control, operations, development on each device, all exit 0 | PASS |
| Hardened source staging | Exact copied+compared files in `~/matrix-controller/general-dev-release-v6/` | PASS |
| Negative unknown task | `foreign-project-demo` rejected before model execution | PASS |
| Live v6 promotion | `bhm-autonomy-controller.service` active; live SHA256 `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e` | PASS |
| Rollback | `controller.py.bak-20261022-static-security-v6`, SHA256 `df0cf3f968244d2e745d941f57d2225cfcd4a4147f55f7ce29c879e87027ffe4` | VERIFIED |
| Live controller-dispatched test | `matrix-dev-security-v6` — UUID `e92144e5-0755-4945-b1a3-758702de0c75` | PASS, 1 model attempt |
| Independent sandbox output QA | `html_semantics_and_active_content`, `qa_passed=true`, `tests_executed=true` | PASS |
| Verified unpublished local review commit | `2b70a5994400f4dda02cebb7a9e233691f1233d8` | PASS |
| Live controller receipt | `completed`, `manifest_enrolled_sandbox_qa`, no error, `published=false` | PASS |
| Cross-tenant, unknown-manifest and duplicate task | Rejected / deduplicated, receipt `3c031d9b-e0fb-496f-a990-2d4e488c3669` | PASS |
| Chrome responsive + network QA | 7/7, widths 320, 360, 375, 390, 430, 768, 1440; receipt `13e864e7-3d8c-44bb-9a51-404ca5f290ac` | PASS |
| GitHub Actions CI | No workflow runs returned for inspected patch source commit | **NOT AVAILABLE** |
| Production / remote GitHub publication | Disabled; not requested | **NOT PERFORMED** |

## What remains excluded

This is NOT a full general-purpose Dev agent. Exact public `matrix_dev` manifests remain enforced. The model is offline and runs with tools disabled, source writes occur in a constrained Bubblewrap workcell, QA is presently complete for the static-HTML profile, and Git artifacts remain local, unpublished review commits.

Before expanding privileges: real source checkouts and approved project enrollment, independent Node/Python application QA, isolated language-specific build/terminal tool adapters, hardened workspace resource exhaustion testing, crash/kill/cancel proof, scoped PR publishing controls and hosted GitHub CI. Preserve v2/v3 failed receipts and historic review artifacts for audit. Existing Mac/Dell root and SSH settings were not changed.

## Release operation / rollback

v6 promotion used the pre-existing owner-scoped non-root Dell SSH mechanism. It performed checksum verification, checked for zero in-flight tasks, staged an exact candidate, backed up v5 and restarted **only** the existing controller. On failure, the procedure was designed to restore v5; this rollback was **not exercised** because v6 successfully started and passed self-test.

Rollback if required: stop new submissions, drain/attest all delegated tasks, then restore `controller.py.bak-20261022-static-security-v6`, restart `bhm-autonomy-controller.service`, verify original v5 SHA. Treat v5's older validator as vulnerable unless the same security fix remains active. Do not run v5 on unknown generated HTML.

**Allowed release statement:** `Dev Operator v6 hardened scoped static-HTML autonomy passed security regression, live controller E2E and responsive browser QA. Full general-purpose autonomous Dev remains unreleased.`
