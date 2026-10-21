# Modular MCP Chat — mobile-first product & engineering contract
**Date:** 2026-10-22 IST  
**Product owner:** user  
**Executor:** existing Dell Business House Dev Matrix, via its verified task controller  
**Status:** DESIGN / TASK HANDOFF; not a deployed application  
**Codebase lane:** this Matrix repository for generic code only; separately authorized per-project adapters remain in their private owning projects.

## 1. Product target
Ship a **world-class, responsive, installable PWA-like chat experience**, optimized for 360–430 px handsets and scaling to desktop. One shell supports separately authorized project-specific MCP adapters. First target is a private Pine Script engineering workflow; **no proprietary Pine source, customer data, secrets, TradingView sessions, or private project code may be copied to this public Matrix repository.** Use synthetic data and stub contracts here.

A ChatGPT-hosted custom MCP integration is separate from the independent mobile web UI; do not claim that building Flask routes installs a ChatGPT app or makes tools available on ChatGPT mobile. Preserve existing provider-side MCP endpoints and authorization.

## 2. Golden Rule 0 / reference and reuse gate
Inspect existing Matrix and owner-authorized gateway/client assets before coding. Required upstream audit:
- https://github.com/GongRzhe/Open-MCP-Client (FlaskMCP.py, MIT; archived 2026-03-03): candidate for chat/MCP server discovery and UI concepts, but NOT deploy unmodified; audit dependencies and security.
- https://github.com/modelcontextprotocol/python-sdk (official Python MCP SDK; pin stable release and verify license).
- https://github.com/modelcontextprotocol/modelcontextprotocol (current protocol and backwards compatibility).
- Accessible existing project-specific owner OAuth/Supabase MCP gateway **only through its approved authenticated contract**; DO NOT duplicate it or copy its secrets.
- Existing Matrix dev brain/router, research, sandbox QA, EVOLUTION feedback; reuse where verified.
- Frontend: audit existing compatible FOSS components before picking one. Accessible candidate React/Vite or Svelte, Tailwind CSS and audited FOSS component library; no new proprietary UI/platform or paid hosted dependency.

Document exact commit/version, license, maintenance, CVE/dependency scan, cost (software/license ₹0; existing compute not literally free), reuse rationale and rollback before implementation. No from-scratch client protocol or wholesale replacement of FlaskMCP.

## 3. User journeys and UX requirements
**Primary:** user opens saved chat, selects project, types or speaks (voice is optional, only if existing free local capability passes privacy gate), attaches authorized text/file, reads streaming responses, inspects cited knowledge and structured tool receipts, safely authorizes a bounded action, follows progress, resumes conversation across devices.
**Mobile 1st:** responsive at 320/360/375/390/430/768/1440 px; safe-area insets; sticky conversation header; bottom anchored composer above virtual keyboard; one-thumb navigation; tap size >=44 px; accessible contrast, semantic landmarks, keyboard/screen-reader support, reduced motion/dark/light; no horizontal scrolling. Long code/results wrap with copy, expand/collapse and syntax highlights.
**Visual quality:** refined typography, restrained high-quality color system, consistent spacing/tokens, polished empty/loading/error/approval states, skeleton transitions, no layout shift, icons, crisp density. Native-feeling PWA affordances but browser is the canonical delivery; graceful non-PWA fallback.
**Shell:** sidebar/project selector, project-scoped chat history and search, chat/new chat, project files/citations (access-controlled), attachments, connection health, permission cards, tool timeline, retry/cancel on supported jobs, settings, account/session management. Desktop gains split-pane workspace (conversation + inspector).
**Conversation:** token streaming, reconnect and replay of safe status events, client-side optimistic draft, idempotent message submission, editable/regenerate drafts without repeating remote tool effects, long-message virtualization, Markdown tables/code/math with sanitization, local draft retention without secrets, system error recovery with request ID. Pagination and search with backend-scoped storage where authorized.
**Action model:** read-only by default; tool card describes exact target, scope and effects; low-risk actions explicitly allowlisted; write actions require server-enforced confirmation and expected target identifiers; destructive/external publish/order/trading actions prohibited unless separate verified authorization. No privilege granted by the UI's controls alone.
**Model/runtime:** use existing approved Matrix model-router and quotas; show actual model/provider and offline/fallback mode, never silently switch to paid APIs. Models produce plans, but authenticated server tools enforce policy.

## 4. Proposed architecture (adapt, don't fork blindly)
```
Mobile/desktop browser (PWA shell, FOSS UI)
    -> first-party session-authenticated thin backend
       -> conversation engine / existing model router
       -> project registry + policy engine (server-side)
       -> official MCP client/adapter around vetted FlaskMCP patterns
          -> authenticated per-project MCP server (existing OAuth gateway)
             -> individually scoped tools / real execution receipts
```
- Project adapter manifest: stable `project_id`, owner/tenant, display capabilities, auth issuer/audience, allowed host/repository/site IDs, MCP endpoint identifier, tool schema versions, policy profile, audit sink, retention rules. **Never** accept a client-supplied arbitrary MCP URL for execution without server-side allowlisting and separate project enrollment.
- Auth: existing OAuth 2.1-compatible bearer resource-server checks and least-privilege scopes, token audience/expiry/rotation/revocation, CSRF/XSS/SSRF/session-fixation mitigations, origin validation, secure cookies, TLS; no client-side storage of API keys.
- MCP: pin official SDK, support negotiated Streamable HTTP and approved legacy transport only where necessary; verify protocol-version negotiation and 2026-07-28 request headers when supported by the server. Separate GPT integration from web UI.
- Storage: isolated project/user scoped persistence and audit receipts; prefer existing storage and encryption. Database RLS/server checks, no cross-tenant reads, no publicly accessible prompt/receipt uploads.
- Streaming: abort and dedupe **UI requests**, but never blindly re-run unknown-outcome remote actions. Preserve canonical job IDs and receipts.
- Observability: privacy-preserving request traces, correlation IDs, failure classes, project identifiers, duration, authorization denials, rate/queue limits. Redact prompts and secrets by default.

## 5. Adapter API contract
- `list_project_capabilities(project_id)` -> allowed high-level features only.
- `list_allowed_tools(project_id)` -> filtered schemas based on authenticated identity.
- `start_chat(project_id, thread_id?, message, attachments?)` -> immutable message ID, permitted provider, stream/request ID.
- `request_tool(project_id, tool_name, validated_arguments, idempotency_key)` -> `denied|approval_required|queued` with exact scoped intent and receipt ID.
- `approve_tool(intent_id, expected_target, one_time_nonce)` -> authenticated server authorization, action audit; approval cannot grant root or change base policy.
- `get_task_receipt(job_id)` -> `queued|running|completed|failed|outcome_unknown|blocked` + redacted artifacts.
- `list_threads/search_threads` -> project/user scoped; never cross-owner.
Version schemas; no dynamic shell or arbitrary URLs as generic MCP tools.

## 6. Minimum screens
(1) Welcome/locked auth, (2) project list, (3) conversation with composer and streaming, (4) conversations/history/search, (5) capability/tool inspector and approval review, (6) execution/activity receipts, (7) connection diagnostics and settings, (8) offline/reconnect and critical error states. Pine adapter adds engineering workspace tabs (spec, Pine code, compile diagnostics, parity, replay/realtime, release gates) backed by permitted tools, not UI fiction.

## 7. Autonomous Matrix execution procedure
**MANDATORY FIRST GATE:** current Dell controller v0.1.0 advertises `dev_proposal=proposal_only`, `sandbox_qa=isolated_test_execution`, `repair_known_issue=bounded_verified_autorepair`. Do NOT claim autonomous coding/commits exist. Reuse a verified preinstalled coding agent with a real fenced workspace; run negative permission/isolation tests before enabling commit-capable execution. If no secure coding lane exists, produce exact adapter/source PR proposal and an explicit CRITICAL_CAPABILITY_BLOCKER receipt. Never use a public Matrix runner to fetch private Pine source or ingest Pine OAuth/SSH credentials.
Sequence:
1. Discover repository instructions, running services, owner scopes, current HEAD/dirty state and existing assets. Record reuse decision, task UUID and allowed paths.
2. Implement safe generic UI in isolated new branch/worktree; write storybook/component/synthetic demo, adapter interface, mocked MCP tools. Independent design + accessibility review.
3. Implement secure generic backend/transport to existing approved MCP without storing upstream secrets; integration tests in fake/local environment only.
4. Isolated tests: vitest/pytest as appropriate, Playwright mobile/browser matrix (320–1440), keyboard/screen reader, screenshot comparison, auth denial, IDOR/CSRF/SSRF, prompt injection, stale results, network loss, duplicate/replayed actions, two-project isolation, strict CSP, SSRF target allowlist, no arbitrary shell.
5. EVOLUTION bounded self-repair on test failures, retry small reversible changes, independently rerun QA. Save receipts, screenshot evidence, performance metrics and source SHA; do not mark done on self-graded textual PASS.
6. Produce reviewable branch/PR, handoff checklist and a staging preview only in the already-authorized isolated environment; **do not publish to public domain, alter auth/root/SSH/network, deploy Pine or enable TradingView mutations** without a separate scope-specific approval.
7. Escalate ONLY: cannot establish safe repo-scoped coding execution; missing legally compliant licensed source; required account consent, inaccessible private Pine source, suspected data leakage, dangerous security/permissions change, irreversible action or unapproved spend. Routine lint/tests/UX/dependency errors are autonomously handled within bounded budget.

## 8. Definition of done
- Working code, NOT just model draft. Project selector and complete Pine-like synthetic chat flow, streaming and safe demo tools.
- Every page meets WCAG AA and touch/safe-area constraints; 320–1440 screenshots, dark/light and reduced motion; no severe Lighthouse mobile failures, target >=90 Accessibility/Best Practices where feasible and measurements shown.
- Tests cover isolation/unauthorized tools, action idempotency, zero unknown-action replay, protocol negotiation and failure recovery; independent QA evidence, checked-in lockfiles, SBOM/license table, pin/rollback.
- Reviewer-ready PR with actual CI/test receipts, source SHA and architecture decision. Generic PR must not contain any private Pine data.
- Pine integration is separately gated by Pine's private project owner; adapter contract may be reviewed before access. Actual TradingView compile and release gates remain incomplete and must never be overwritten by chat UI claims.

## 9. Autonomous task-state reporting
Report actionable milestones in existing Dell controller receipts only: `RESEARCHED`, `FRONTEND_BUILT`, `MOCK_MCP_CONNECTED`, `PINE_ADAPTER_DESIGNED`, `INDEPENDENT_QA_PASS`, `PR_READY`, or `CRITICAL_BLOCKER`. A queued command or generated proposal is not an implementation receipt. Preserve all existing Matrix marketing work, its thermal guards, and ongoing controller jobs.
