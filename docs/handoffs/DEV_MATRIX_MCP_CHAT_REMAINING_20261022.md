# Dev Matrix Autonomy + Modular MCP Chat — Remaining Work Handover

**Date:** 2026-10-22 (IST)  
**Owner/project:** Business House Matrix, `aarondash5-star/business-house-matrix`  
**Existing tracker:** [Issue #2](https://github.com/aarondash5-star/business-house-matrix/issues/2) — leave open until independently certified  
**Reference branch:** `docs/modular-mcp-chat-template-20261022`  
**Working host:** `dell-linux`; separate Pine private owner/repository must not be mixed with public Matrix workspace.

## Verified baseline — do not rebuild
- Dell Generic SSH bridge online, established control/operations/development lanes; existing autonomy controller/queue and task receipts.
- Existing local Pi via Ollama `qwen3:4b-instruct` returned `READY` with tools/MCP/extensions disabled in a sufficiently long bounded test. It generated valid JSON for a synthetic fixture in a separate probe. Earlier 35-second timeout was not persistent connectivity failure.
- Bubblewrap bounded **reviewed-patch** execution verified: no network, no host-private or cross-project files, allowed-path and SHA overwrite checks. Five negative/functional tests passed. This is **not** an unrestricted autonomous coding agent.
- New live `pine_chat_stage` controller action: project `pine_mcp_chat`, manifest `pine_chat_v1`, private synthetic-only source staging; existing service restarted/active without SSH/privilege changes. Task `ba39d446-554f-40a6-ae89-5adbaf95d07e` completed with `private_synthetic_chat_preview_qa`, attempts=1, no error.
- Chat prototype at `prototypes/pine-mcp-chat/index.html`, SHA-256 `b604dccfd396ef0d1549c4909d76d69a49d4f6ef5b31a51799da3c42afb639db`. Private Dell preview `~/matrix-controller/private-previews/pine_mcp_chat/index.html`. Real browser tests passed at 320/360/390/430/768/1440 px (basic chat flow, reset, inspector, no overflow or JS errors); no live MCP or private Pine access.
- Prior detailed receipt: [PINE_MCP_CHAT_MATRIX_STAGE_RELEASE_20261022.md](../receipts/PINE_MCP_CHAT_MATRIX_STAGE_RELEASE_20261022.md). Scope/design: [MOBILE_FIRST_MCP_CHAT_TEMPLATE_2026-10-22.md](../architecture/MOBILE_FIRST_MCP_CHAT_TEMPLATE_2026-10-22.md).
- **Known block:** An open-ended model-to-code executor attempt hit platform safety restrictions. Never bypass security or silently grant cross-repository access.

## A. Dev Matrix — autonomy backlog (ordered gates)

- [x] Dell SSH bridge/controller and durable task queue operational.
- [x] Local model responds to bounded no-tool tests.
- [x] Restricted Bubblewrap patch runner, negative tests and scoped fixed-source staging verified.
- [ ] **A1 — Source-governed secure code executor.** Review, version and certify the actual controller additive diff; implement an authorized, project-enrolled model proposal → strict structured validation → isolated file apply path. Require negative tests for filesystem escape, secrets, symlinks, network, unintended commands and cross-tenant access. Do not bypass prior platform restriction.
- [ ] **A2 — Coding feedback loop.** Implement bounded build/test/debug/retry with resource/time limits, receipts, cancellation, deduplication and fail-closed escalation; allow only scoped nonproduction files.
- [ ] **A3 — QA/QC gate.** Independent unit/integration/UI/security review; enforce evidence before statuses such as `qa_pass` or `completed`.
- [ ] **A4 — Git workflow.** Per-task isolated branch/worktree; approved repository account and credentials; commit/PR review; no direct `main` edits, merging or auto-publishing.
- [ ] **A5 — Safe self-repair.** Known-defect repair rules, retry budgets, rollback and escalation; preserve existing controllers and sessions.
- [ ] **A6 — Autonomous scheduling.** Task prioritization, dependencies, concurrency/thermal limits, status/audit receipts and user escalation.
- [ ] **A7 — External MCP connectors.** Independently enroll narrowly allowlisted services and tools; implement tool-level read/write permissions, explicit approval for sensitive actions, expiry and auditing.
- [ ] **A8 — Security + certification.** Separate account/tenant credentials/customer data; end-to-end test task generation, code edits, QA, PR, recovery and no-spend/no-publish guarantees. Only then label coding autonomy certified.

## B. Modular MCP Chat — product backlog (ordered gates)

- [x] Synthetic mobile-first chat prototype, mock interactions and six-width browser QA.
- [x] Private nonindexed staging output; no real Pine commands.
- [ ] **B1 — UX/frontend.** Refine the mobile-first responsive UI into reusable modules (chat shell, composer, threads, tool cards, approvals, settings); keyboard/focus/accessibility and visual QA.
- [ ] **B2 — Backend and MCP transport.** Build modular app backend and secure gateway; transport/authenticated tool registry, server discovery, schema validation and rate limits.
- [ ] **B3 — Real model experience.** Integrate authorized local/approved model routing, streaming, tool call/result UI, structured errors, loading/cancellation and reconnect.
- [ ] **B4 — Data and authentication.** Proper login and per-user session isolation, encrypted conversation history/persistence, retention/erasure policy and minimal audit records.
- [ ] **B5 — Tool controls.** Tool-specific scopes, human approvals, execution receipts, progress/status and safe retries; no cross-project privilege inheritance.
- [ ] **B6 — Content features.** Secure attachments, file size/type controls, code/Pine syntax rendering and copy/export.
- [ ] **B7 — Pine adapter.** Enroll separate private Pine repository and account with explicit owner-authorized MCP permissions; preserve protected chart/Windows control and current oracle QA. Workflow: spec → Pine v6 → native compile → independent bar parity → save/reload → Replay → realtime nonrepaint → user approval. Keep mocks until verified, do not trade/publish.
- [ ] **B8 — QA and release.** Comprehensive security, mobile visual, accessibility, performance, regression and real-tool integration tests; private end-to-end staging; separate approval before production release.

## Immediate next actions

1. Read the original GitHub handover/issue, current live controller receipt and branch before any code. Follow Golden Rule 0: reuse existing code, vetted open-source components and working infrastructure; do not duplicate task IDs.
2. Advance **A1** with a reviewable, separately tested integration proposal and security gate rather than enabling an unrestricted agent. Preserve the existing live `pine_chat_stage` path and do not disturb Moksha website or unrelated Matrix tasks.
3. In parallel, work on **B1/B2 only within public synthetic staging**; do not touch the private Pine account until enrolled.
4. Append verified evidence (exact task ID, branch/commit, tests, pass/fail, limitations, rollback) to **Issue #2** and this handover. Keep the issue open while A1–A8 or B1–B8 remain incomplete.

**Hard constraints:** No unauthorized spending, public publishing, production changes, secrets disclosure, unrestricted root/model shell, cross-tenant credential/data sharing, or bypass of tool/platform controls. Keep Ashwakaal — Support Channels separate. For verified platform/support-channel integrations, follow the authorized Supabase Master event inbox reporting policy; never route Ashwakaal into the Matrix repo without explicit approval.

## Shortest new-chat handover prompt

> Continue Dev Matrix autonomy + Pine MCP Chat. Read `aarondash5-star/business-house-matrix/docs/handoffs/DEV_MATRIX_MCP_CHAT_REMAINING_20261022.md` on branch `docs/modular-mcp-chat-template-20261022` and Issue #2. Resume A1/B1 without rebuilding, preserve security gates; execute and verify.


## 2026-10-22 follow-up — A1/B1 governed review branch

The source-governed, review-only A1 validator and 12 unit tests were added. Dell and independently Mac passed 12/12 each. The original B1 synthetic mobile UI was enhanced with ephemeral in-tab threads and search, accessible nav and a denied tool-intent inspector; Dell Chrome/Playwright passed 63/63 checks across 7 widths. Screenshots saved on Dell in isolated local staging. Complete receipts, commit references, controller source drift, rollback and limitations: [ISSUE2_A1_B1_GOVERNED_QA_20261022.md](../receipts/ISSUE2_A1_B1_GOVERNED_QA_20261022.md).

**Status remains review-only.** Live controller contains extra unversioned additive actions relative to public reference; independently review exact source before promoting A1. Existing live fixed-source preview unchanged; autonomous code, real MCP transport, private Pine integration, authentication and production deploy NOT CERTIFIED. Issue #2 OPEN. No root, spend, publish, or credentials changed.
