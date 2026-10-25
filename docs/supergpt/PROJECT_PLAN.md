# SuperGPT — product concept, architecture and execution plan

**Status:** OWNER-APPROVED FOR PROJECT STRUCTURING AND RELEASE-GATE SETUP; PRODUCT RELEASE NOT APPROVED
**Version:** 1.0 · 2026-10-25 · **Canonical index:** [README.md](README.md)
**Business boundary:** Business House Matrix; no inherited Moksha, Andaz, Pine or other venture secrets.

## 1. Product intent and non-goals

SuperGPT is the user-facing, mobile-first conversational command center for the independent Business House Matrix. It should let an authenticated owner submit decisions and scoped tasks; route approved envelopes to the existing appropriate departmental Brain; show task queues, execution receipts, evidence, blockers and QA; access authorized AI inference with a local/offline fallback where available. The interface must tell the difference between a suggested action, a queued job, authenticated Brain acceptance, completed execution, a CI build and a production deployment.

**Non-goals for the current prototype:** claiming to embed the user's ChatGPT subscription as a freely callable backend API; granting automatic root or cross-project credentials; bypassing security/connector gates; autonomous publishing, financial spend or production deployment; replacing the nine departmental Brains; equating PocketPal's default offline-chat features with verified Matrix orchestration.

## 2. Architecture and contracts

```text
Owner → SuperGPT client (Android-first, desktop UI later)
       → authenticated HTTPS API / session transport
       → Super Brain governance + approved task-envelope v1
       → authorized Matrix controller/dispatch/receipt API
       → responsible department Brain (Dev, QA/QC, Marketing, etc.)
       → its enrolled workers / models / MCP tools
       → receipts + independent QA + owner approval → client
```

A local model may answer on-device or provide a graceful limited offline experience; it must NOT fabricate an online task dispatch, receipt or final approval. Server-side provider routing can select authorized cost-controlled APIs; no API keys in APK/source or exposed to the mobile client. Authentication, authorization, replay protection, audit trails, project/data isolation, encryption and least privilege are required before connecting privileged worker routes.

**Candidate technology:** existing PocketPal-derived React Native Android shell (temporary prototype), existing Matrix controller/department workers, approved HTTPS/MCP APIs, OSS/on-device model adapter; reuse Open WebUI/Matrix work where actually integrated. **Decision gate:** compare upstream licensing and dependencies against the project's OSI-approved open-source rule before adopting any client or model. Do not assume all downloadable weights, mobile packages or API terms meet it.

**Unknowns requiring engineering validation:** client application identity and signing; final UI/navigation specification; authenticated session provider; stable Matrix dispatch endpoint; real two-way receipt/event streaming; secure provider router; local model package sizes/compatibility; Play Store/privacy requirements; resilient Android KVM/device smoke tests.

## 3. Work breakdown, accountability and current state

| ID | Package | Accountable Brain | Acceptance evidence | State |
| --- | --- | --- | --- | --- |
| SG-00 | Canonical plan, branch lanes, reviewer policy and automated promotion checks | Development + QA/QC | Committed docs, workflow, tests, branch-enforcement audit | In progress; admin enforcement unverified |
| SG-01 | Reproducible mobile prototype build and upstream pinning | Development | Traceable commit, Android build success, APK checksum, license report | Build success; reproducibility/license audit pending |
| SG-02 | Lightweight emulator and physical-device smoke test | Development + independent QA/QC | ADB install/launch, logcat crash scan, screenshot, device/OS matrix | Blocked; KVM access denied |
| SG-03 | Product screens and UX for task submission, chat, queues, receipts, settings | Concept + Design, Development implements | Signed-off flows; accessible, mobile-first QA | Not certified |
| SG-04 | Authenticated client-to-API session and typed tool endpoints | Development | Security review, no secrets in APK, scoped authorization, negative tests | Not certified |
| SG-05 | Real Matrix task-envelope dispatch and receipt lifecycle | Development + relevant department Brains | Actual authenticated Brain acceptance/job IDs and traceable result | Not certified |
| SG-06 | Open-source inference routing and local/offline fallback | Development + EVOLUTION | License inventory, provider failure tests, offline truthfulness | Not certified |
| SG-07 | Security, privacy, accessibility, resilience and mobile matrix | QA/QC + Development remediation | Independent test records and clear critical defects | Not certified |
| SG-08 | Signed release candidate and acceptance | QA/QC, owner decides | Reproducible APK/AAB, checksum, owner approval reference, rollback | Not certified |

The accountable Development Brain controls its enrolled workers under existing Matrix governance. ChatGPT's Super Brain is the approval and reporting interface, not an assertion of a running build process. GitHub changes are **documentation/workflow implementation only** until verified in an actual Brain runtime.

## 4. Execution stages and Definition of Done

**Stage A — Project and release infrastructure.** Establish dev/test/production branches, source-of-truth document, QA schema, CI PR gates, ownership rules. Audit repository rulesets separately; CI failure alone cannot block force-push/direct merge without GitHub branch protection. DONE only when checks and enforced settings are independently verified.

**Stage B — Working Android shell.** Pin tested upstream revision; identify package/app label; run APK build; install on emulator or physical Android device; capture startup, background/foreground, permission prompts and crash logs. Prototype status changes from `build_passed` to `runtime_tested` only on receipts.

**Stage C — Secure connectivity.** Implement approved authentication and backend gateway, distinguish offline LLM answers from Matrix task execution, negative authorization tests, retry/idempotency, clear statuses and protected local storage. No plaintext secrets or uncontrolled general shell.

**Stage D — Matrix integration.** Connect real task-envelope v1 ingress, validate routing to at least one real departmental Brain and its enrolled workers, display controller job IDs, retries and failures. Scope other departments separately; no claim of integration without receipts.

**Stage E — Quality/candidate.** Run automated tests, independent mobile QA, security and permissions review, resource/thermal checks, offline/reconnect drills, rollback rehearsal, accessibility and privacy checks. Document each failure and re-test.

**Stage F — Production.** `super-gpt/test` → `super-gpt/production` PR with all checks and owner acceptance. Release packaging/signing/deployment require a separately approved operation; branch promotion by itself is NOT deployment.

## 5. Decision and task-state model

Use existing `brain/governance/task-envelope-v1.schema.json`. A task must carry a project ID, owner-confirmed scope, receiving Brain, forbidden effects, idempotency key, test/rollback criteria and reporting destination. UI state machine:

`draft → awaiting_owner_confirmation → approved → dispatch_pending → brain_accepted → executing → qa → review_ready → owner_accepted → closed`.

Exceptional states `blocked`, `failed`, `cancelled`, `delivery_uncertain`. Never display `executing` merely because a GitHub issue/SSH command was queued.

## 6. Milestones and measurable acceptance

- **M0 repo governance:** all three branches present, source-of-truth linked, CI gate validated, active branch protections reviewed.
- **M1 Android prototype:** APK builds from pinned source and installs/launches on one authorized Android environment without fatal logs.
- **M2 secure interaction:** authenticated chat, sign-in/out, valid session expiry, no client secrets, no unauthorized cross-project requests.
- **M3 actual delegation:** submit one owner-approved test task to real connected Dev Brain; collect distinct transport, controller, Brain and worker receipts plus QA evidence.
- **M4 beta:** stable retries, offline indication, local inference fallback when tested, documented known limitations, basic accessibility and low-resource usability.
- **M5 production release:** all release evidence passes, reviewer/owner decision recorded, GitHub protection enforced and release signing/deployment verified separately.

There are no promised dates: milestone completion is evidenced rather than assumed.

## 7. Risks, prerequisites and truthfulness

1. **Build ≠ app certification.** Existing GitHub Actions build succeeded but emulator/device startup is unverified.
2. **KVM access.** Generic SSH worker lacks access to `/dev/kvm`. Use legitimate host-level administration; do not silently escalate root. A physical device is a fallback.
3. **Mutable upstream checkout.** Current PocketPal workflow uses upstream `main`. Pin immutable SHA before making reproducible release claims.
4. **Branch protection.** CODEOWNERS and CI jobs do not enforce review/PR unless GitHub branch rulesets are actually installed and active.
5. **Integration.** A standalone React Native UI is not an autonomous Matrix Brain client.
6. **Licensing/data.** Verify all dependencies against OSI-approved rule; isolate tokens, data, secrets and credentials.
7. **External spend/publishing.** No publication, purchases, production release, root changes or credential grants follow merely from this plan.

## 8. Change control / next execution contract

Requirements changes go to `super-gpt/dev` in PRs with rationale and new scope; testing requires the documented independent QA gates; production requires owner acceptance. Record verified evidence in [QA evidence](qa/RELEASE_EVIDENCE.json), link runtime receipts, and maintain the immutable release history. Escalate material architecture, security, budget or public-distribution decisions to the owner per the Matrix charter.
