# Pine MCP Chat — Matrix integration release acceptance

**Date:** 2026-10-22 IST  
**Release scope:** integrate reviewed public synthetic Dev Matrix/Pine chat source into Matrix `main`; no production service or private Pine access is conferred by this Git merge.

## Certified and source-backed

- Existing restricted `pine_mcp_chat` one-shot model → source allowlist → Bubblewrap sandbox → QA → local review commit pipeline is already **live on Dell**, exact controller SHA256 `0e0060cfafae64a27cbdca34e0e63d03150ca84e54b075642817720c85228aa884`; no deployment/restart in this PR.
- Previously verified live controller completed task `2ce7c08b-e1f2-450e-a61b-5f234416daaa`, 6/6 synthetic QA, local Git commit `706f02d3077a3f551c6c3cf0eccc7627ed80a015`, **published false**.
- Existing synthetic mobile-first UI and denied-intent inspector: Dell browser regression 63/63 across 7 widths on reviewed branch; not a functioning operational Pine MCP chat.
- Source PR #3 integrated in branch at `e841bb5c19ba8c496feca2265e009af2e8c58215`, GitHub CI run 39800996613 both jobs PASS, 80 tests PASS, 5 Bubblewrap host-only tests explicitly SKIPPED; those native cases independently passed on Dell. Source provenance/QA [release record](DEV_MATRIX_SCOPED_AUTONOMY_CERTIFICATION_20261022.md).
- The previously unrelated Marketing research test mismatch was fixed through separate PR #7 on `main`: existing exact v1.1 source and relevance helper, deterministic QA fixture. Merge commit `30c9118ff5a495fbbeab2f8042f6b939e79e1dbb`. **PR #6 must pass fresh checks against this updated main**.
- Existing PIN-gated owner PWA on Vercel `pine-engineer-chat-mvp.vercel.app` is READY, owner verified PIN unlock. PIN is sole user-facing login and must not be changed or duplicated. This is **existing deployment**, not created by Git merge.

## Explicitly not complete

- Authenticated streaming real AI model/chat and scoped Pine MCP tool execution are **not verified**; generic UI and MCP source may be synthetic/standalone.
- Supabase `pine-chat-mvp-mcp` source uses separate owner OAuth, not the existing Vercel PIN session. **Do not bridge tokens or silently equate the two auth mechanisms.** A narrow server-side enrollment and negative authorization tests are required before real tools are exposed to the PIN app.
- Pine Gold strategy **Phase 3 NOT CERTIFIED**: A PASS, B PARTIAL, C PASS, D INCONCLUSIVE, E PARTIAL, F PARTIAL, G PENDING. Owner calls for training/UAT pending tasks; not permission to fabricate PASS.
- Do not modify protected TradingView chart `/chart/JvxzE0Bg/`, open an arbitrary shell, create alerts, publish scripts, connect brokers, trade or spend.
- No automatic main merge, Vercel deploy, Dell controller restart, Supabase function publish or account permissions is authorized by this document. Existing changes must be independently verified after any Git merge.

## Handover gates

1. PR #6 main-target full GitHub CI green (independent repo safety and tests); record source SHA and merge commit.
2. Inspect actual Vercel alias deployment READY and unchanged PIN routes after source merge (do **not** claim automatic deploy).
3. For owner functional beta: authenticated PIN session → server scope check → allowed **read-only** Pine spec/draft status → receipt → logout/reload/negative paths; real model/adapter must be separately connected and tested. If absent, beta remains UX-only.
4. Publish evidence and short new-chat takeover prompt in private Pine repo, retaining Phase 3 gate ledger and human review.
