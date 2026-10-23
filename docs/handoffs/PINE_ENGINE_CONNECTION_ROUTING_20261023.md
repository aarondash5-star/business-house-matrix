# Pine Engineer — Canonical MCP Routing

**Updated:** 2026-10-23 (IST)  
**Status:** OWNER MANUAL BETA CONNECTION PENDING

## Use these integrations

| Task | Integration | Status / rule |
|---|---|---|
| Pine Engineer beta chat, feature discovery, feedback, paper orders, event preview, receipts | **Owner-selected beta plugin, to be connected manually** | **PENDING** owner selection, OAuth, tool discovery and smoke tests; do not assume any current beta plugin is certified |
| Native Windows and TradingView Controller tasks | **`Pine Manbir SSH`** (`pine-manbirs-mcp-cli`) | Preserve; require fresh owner-authenticated worker heartbeat, disposable QA chart, verified source identity and receipts |
| TradingView market data and supported screener queries | **TradingView MCP** | Data only; not a Pine compiler or chart editor |
| Source, versioning, QA specifications and release receipts | **`karanzing1992/gpt-pine-engineer` GitHub repository** | Follow the repository runbook and QA gates |

## Deprecated — do not use for new beta work

1. **`Pine ENgine USER BETA`**, legacy standalone ChatGPT app: **UNINSTALLED 2026-10-23**. It exposed three of ten advertised tools. [Archive](./PINE_ENGINE_USER_BETA_APP_DEPRECATION_20261023.md).
2. **`pine-chat-mvp-mcp`**, private skill-based plugin v0.2.0: **DEPRECATED 2026-10-23 at owner request**. ChatGPT Plugin Management returned **`not_installed`** for both its exact plugin ID and name, so no installed connection remained to uninstall. Its private owner-held definition/release may still exist; do not select it for new beta work.

## Archived `pine-chat-mvp-mcp` reference

- Plugin ID: `plugins_6ad9e6c5d15081918e6856287a28c61a`
- Last verified version: `0.2.0`
- Last verified release ID: `pluginrel_6adaf3216ef881919b5c126dd540e7e4`
- Old OAuth-protected MCP endpoint: `https://saczglesalubroyaucqe.supabase.co/functions/v1/pine-chat-mvp-mcp/mcp`
- Backend server previously registered ten tools, but **0/10 were callable in the most recent ChatGPT tool inventory**. Owner-authenticated beta smoke tests were **BLOCKED**.
- This is reference metadata, not an instruction to reconnect, deploy, or reuse credentials.
- No Supabase function, OAuth identity, source code, broker configuration, native worker, chart, script or production alert was changed by this deprecation.

## Manual beta connection acceptance test

1. Owner manually connects the intended beta plugin to ChatGPT.
2. Record its exact name, ID, version, MCP URL and OAuth principal, without storing secrets.
3. Verify the ten expected tools are **callable** (not merely listed in an endpoint description): `pine_chat_workspace_info`, `pine_chat_workflow`, `pine_chat_preview_info`, `pine_beta_feature_catalog`, `pine_beta_native_request`, `pine_beta_job_status`, `pine_beta_submit_feedback`, `pine_beta_paper_order`, `pine_beta_preview_event`, `pine_beta_recent_receipts`.
4. Run owner-authenticated synthetic read-only/dry-run smoke tests. Record pass/fail, IDs, timestamps and terminal receipts. Native request tests must not mutate unknown or protected charts.
5. Update this canonical routing guide **only after** the newly connected plugin is verified.

## Safety and certification

No live broker orders, production alerts, publishing, protected-chart mutations, or unverified native execution. Phase 3 certification still requires native TradingView compile diagnostics, same-feed signal parity, Replay/realtime checks, save/reload persistence, rollback and explicit owner sign-off.

## Related tracking

- [Business House Matrix Pine MCP chat issue](https://github.com/aarondash5-star/business-house-matrix/issues/2)
- [Legacy standalone beta app archive](./PINE_ENGINE_USER_BETA_APP_DEPRECATION_20261023.md)
