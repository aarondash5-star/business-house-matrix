# Pine Engineer owner beta — MCP source parity checkpoint

Date: 2026-10-23 (IST). Scope: source reconciliation only; **not a release or deployment**.

## Outcome

The deployed Supabase `pine-chat-mvp-mcp` Edge Function was read back as ACTIVE v3, health version `0.2.0`, with ten registered MCP tools. Before this change, Matrix `main` still contained the original three-tool `0.1.0` source. This branch copies the exact retrieved live `index.ts` into the existing Matrix source path and adds static regression checks. No Supabase, Vercel, ChatGPT App, Windows controller, or broker state is changed by this PR.

The ChatGPT installed **Pine ENgine USER BETA** App wrapper still exposes only the three historical tools in this conversation. The ten registered server tools must not be reported as ten ChatGPT-callable tools until the owning App registration is refreshed and individually smoke tested.

## Ten deployed server tools and actual effects

| Tool | Current effect | Limitation |
| --- | --- | --- |
| `pine_chat_workspace_info` | Read beta scope | Some compatibility labels are still historical |
| `pine_chat_workflow` | Read static process steps | No Pine generation or execution |
| `pine_chat_preview_info` | Read historical preview metadata | Not live web-app verification |
| `pine_beta_feature_catalog` | List 22 desired capabilities | Catalog is not implementation certification |
| `pine_beta_native_request` | Owner-scoped, idempotent QA job record | Status `PENDING_NATIVE_ENROLLMENT`; no Windows execution |
| `pine_beta_job_status` | Read owned QA job receipt | Does not compile Pine |
| `pine_beta_submit_feedback` | Durable owner QA feedback event | Requires actual tester evidence |
| `pine_beta_paper_order` | Per-request cash/notional simulation receipt | Not a persistent position-aware paper brokerage |
| `pine_beta_preview_event` | Alert/notification dry-run receipt | No TradingView alert or message sent |
| `pine_beta_recent_receipts` | Read recent owner event receipts | Audit visibility only |

## Auth and boundaries

- Supabase Auth bearer token is independently validated against `/auth/v1/user` and an enabled owner member row. The Vercel four-digit PIN is **not** a Supabase OAuth token and must not be upgraded into privileged tool authorization.
- Owner ID filters and idempotency are present in the event/job reads and writes. Native queue entries are journal-only.
- Protected TradingView charts remain denied. Live broker orders, TradingView production alerts, notifications, and publishing are disabled.
- The service-role key remains server-side. No token or credential belongs in the public repository.

## Reference / reuse decision

Reuse the owner-deployed Supabase Edge Function and pinned open-source MCP SDK 1.25.3, Supabase JS 2.75.0, Zod 4.1.13, existing owner-auth tables, and the private Pine repository's independent Python oracle/QA tooling. No replacement MCP framework, AI model, second browser writer, or native controller is introduced. This is an exact source-parity sync plus regression guard.

## Verification and remaining gates

- PASS: Source read-back contained exactly ten `server.registerTool` names.
- PASS: Source inspection found owner token/member check, protected-chart filter, journal-only native request, paper-only simulation, and alert dry run.
- PASS: Exact retrieved source copied onto this review branch.
- PASS: [GitHub Actions run 39903821491](https://github.com/aarondash5-star/business-house-matrix/actions/runs/39903821491), both `starter-tests` and `public-repository-safety` successful, including the new static contract test. Static inspection still is not a live MCP call.
- BLOCKED: ChatGPT App tool manifest refresh (currently 3/10 visible). Updating Matrix Git alone does not refresh it.
- BLOCKED: Manbir native worker offline at read-only check on 2026-10-23; no TradingView compile or Replay run.
- PENDING: ChatGPT-native idea → numbered spec → golden cases → Pine v6 → independent Python oracle → immutable Git receipt, executed as a real end-to-end owner beta case.
- PENDING: Durable, position-aware paper ledger and authenticated alert-ingress E2E.
- NOT CERTIFIED: Gold Phase 3 native parity/realtime/rollback/reviewer gates.

## Next execution order

1. Refresh the **existing** ChatGPT App registration against the deployed ten-tool MCP schema; verify owner OAuth and negative authorization cases. Do not create a second model or silently substitute the Vercel PIN.
2. Run one complete ChatGPT-account-powered breakout example using the private Pine repo's existing strict spec, reference fixture, Pine v6 source and validation CLI; save exact hashes and outcomes.
3. Restore/re-pair the existing Manbir worker through the approved connection flow, inspect source hash and disposable chart, then perform controlled native compile/Replay QA.
4. Add real alert gateway and stateful paper ledger only after authenticated ingress, idempotency, audit, rollback and dry-run tests pass; never enable broker orders.
5. Keep Vercel PWA separate from the ChatGPT reasoning entitlement until an approved **Sign in with ChatGPT** integration is demonstrated; its current synthetic reply UI must remain labeled demo.

Production release, chart publication, production alerts and live broker remain OFF.
