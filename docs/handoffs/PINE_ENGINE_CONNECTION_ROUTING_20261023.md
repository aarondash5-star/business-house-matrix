# Pine Engineer — Canonical MCP Routing

**Effective:** 2026-10-23 (IST)  
**Status:** CURRENT ROUTING / OWNER BETA

## Use these integrations

| Task | Approved integration | Current limitation |
|---|---|---|
| Pine beta chat, feature discovery, QA request journal, feedback, paper-order simulation, dry-run events and receipts | **`pine-chat-mvp-mcp` private skill-based plugin v0.2.0** | Ten tools are registered in the Supabase MCP server, but full ChatGPT callable exposure still requires a new-session verification |
| Native Windows and TradingView Controller tasks | **`Pine Manbir SSH`** (`pine-manbirs-mcp-cli`) | Require owner-authenticated fresh worker heartbeat, disposable QA chart, source identity and terminal receipts |
| TradingView market data and supported screener queries | **TradingView MCP** | Not a Pine compiler or chart editor |
| Source, versioning, QA specifications and release receipts | **`karanzing1992/gpt-pine-engineer` GitHub repository** | Follow repository runbook and gated QA |

## Do not use

**`Pine ENgine USER BETA` — legacy standalone ChatGPT app: UNINSTALLED on 2026-10-23.**

It exposed only three read-only tools despite advertising ten in workspace metadata. Its archived snapshot is [here](./PINE_ENGINE_USER_BETA_APP_DEPRECATION_20261023.md). Do not reinstall or route jobs through it.

## Current beta provider

- Private plugin: `pine-chat-mvp-mcp`
- Version: `0.2.0`
- Plugin ID: `plugins_6ad9e6c5d15081918e6856287a28c61a`
- OAuth-protected MCP endpoint: `https://saczglesalubroyaucqe.supabase.co/functions/v1/pine-chat-mvp-mcp/mcp`
- Owner identity: Supabase OAuth only. The PWA PIN does not authorize MCP.
- Backend registration: ten beta MCP tools.
- Full host exposure and end-to-end tests: **PENDING**. Do not label the beta fully operational based solely on backend registration.

## Safety and certification

Live broker orders, production alerts, publishing, protected-chart mutations, and unverified native execution remain prohibited. Native QA and Phase 3 certification require actual TradingView receipts, independent parity, Replay/realtime, reload persistence, rollback and owner sign-off.

## Required next check

Open a fresh authorized ChatGPT session with `pine-chat-mvp-mcp` and verify all ten callable tools. Run owner-authenticated smoke tests with synthetic fixtures. Preserve the separate Pine Manbir SSH route and all existing scripts.

## Related project tracking

- [Business House Matrix Pine MCP chat issue](https://github.com/aarondash5-star/business-house-matrix/issues/2)
- [Legacy app deprecation archive](./PINE_ENGINE_USER_BETA_APP_DEPRECATION_20261023.md)
