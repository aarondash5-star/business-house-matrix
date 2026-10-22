# Issue #2 — A1/B1 governed QA receipt (2026-10-22 IST)

**Review-only, NOT live release.** Branch: feat/issue2-a1-b1-governed-20261022, based on docs/modular-mcp-chat-template-20261022. Issue #2 remains open.

## Existing infrastructure reused

Existing synthetic Pine chat HTML prototype, Dell Matrix controller and pinned preview path, existing rootless Bubblewrap runner, preinstalled Python standard library, Chrome 155 and Playwright. No new API, packages, credentials, accounts, spending, root/SSH changes, production deploy or public publishing.

## A1 — source governance

- New source: brain/secure-coding/source_governor.py, commit 6f419497f5f93732d57f38c656066ca35f7441d8.
- Tests: brain/secure-coding/tests/test_source_governor.py, commit 0d4475397806891aaee8bbb87d6415be0a82616a.
- Exact allowlist: public repository aarondash5-star/business-house-matrix; project pine_mcp_chat; manifest pine_chat_v1; work item pine_chat_b1_synthetic_review_v1; exact two synthetic file targets. Rejects cross-project/repo/manifest/task requests, arbitrary command fields, traversal paths, duplicate targets, unsafe source patterns, unapproved test imports, missing tests and bad size/hash metadata. Model never provides approved baseline sha. Source gate never writes, runs, approves or publishes.
- Dell: 12/12 unit tests PASS, exit 0; SSH receipt 311992c0-ff58-414b-8c61-e693fd3ab19a.
- Mac independently: 12/12 unit tests PASS, exit 0; SSH receipt c865e90a-8a5d-4c00-b09b-bf7529ad5c08.
- Remaining: source governance is an additional validation layer, NOT a certified safe model-code executor. Independent full source diff, sandbox negative tests, verified model output and approval are mandatory before any controller integration.

## B1 — mobile chat extension

- Reused and incrementally enhanced prototypes/pine-mcp-chat/index.html, commit 9c31eb364e0eda77ff9b12df29f11da70cbbeeec.
- In-file components: MockAdapter, ThreadStore, Navigation, ChatShell, Inspector. Ephemeral tab-only thread history and search, semantic live chat log, keyboard focus/Escape support, minimum touch sizes, prefers-reduced-motion CSS, denied tool-intent inspector. No real tool approval or backend call; all user text rendered safely as text.
- Browser tests: prototypes/pine-mcp-chat/tests/ui-e2e.cjs, commit f8e758930db32f22cabaf04a81d00a5ce99b4fad.
- Dell real Chrome/Playwright, widths 320 / 360 / 375 / 390 / 430 / 768 / 1440; nine per-width assertions covering mock chat, reset, in-memory search/restore, denied action, keyboard navigation, no overflow, no JS exceptions, and no external network requests. **63/63 PASS**, exit 0, receipt 869cb679-6e41-4c84-830b-a757afdc63d9.
- Screenshots, Dell local only: ~/matrix-controller/release-stage-issue2-a1-b1/repo/prototypes/pine-mcp-chat/qa-screens/b1-390.png and b1-1440.png. 390 px sample separately visually inspected. QA source HEAD f8e758930db32f22cabaf04a81d00a5ce99b4fad.
- Existing live fixed-source pine_chat_stage remains pinned to prior reviewed original HTML; this branch did not deploy into controller or authenticated Pine UI.

## Critical live controller diff to review (AST audit only)

- Actual Dell bhm-autonomy-controller.service active, not restarted or edited.
- Live Dell controller: 28,289 bytes, SHA256 448a587b6c11bfbbd4618afc65b6f90a5f56bf54b075642817720c85228aa884.
- Public branch controller: 17,960 bytes, SHA256 9726a5c71635a4fd1271f016061ef85cd0c6ad830f522d517bcb39573ad19e6c.
- Read-only AST inventory detected additional live actions dev_docs_fetch, dev_scoped_build, website_stage and pine_chat_stage, plus poll_scoped_build. Receipt 18f8e746-7bf3-4289-a843-ca4a221c4bcb exit 0. This inventory is not a security audit or exact source diff. Independently review and version additive source before promotion.

## Release decision and rollback

**A1 partial / B1 incremental; no certification of autonomous coding, real MCP/backend, Pine private adapter, production releases, or authentication.** No merge, no production or SSH changes, no paid providers, private Pine access, chart or trading actions. Synthetic review branch can be reverted or closed with no effect on existing controller or pinned preview. Local QA clone can be deleted independently. Next: independent additive controller diff + sandbox QA, then separate source-governed model pipeline certification; B1 component/backend integration and real MCP auth remain deferred behind their gates. Keep Issue #2 OPEN.
