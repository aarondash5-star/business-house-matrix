# Pine ENgine USER BETA — Deprecated App Reference

**Date:** 2026-10-23 (IST)  
**Status:** UNINSTALLED — legacy ChatGPT app; archived for reference only  
**Change scope:** The exact legacy ChatGPT app was uninstalled on 2026-10-23 at owner request. No Supabase deployment, auth configuration, chart, alert, broker, or successor-plugin change was made.

## Exact legacy target

- ChatGPT app display name: `Pine ENgine USER BETA` (preserve capitalization for identification).
- App-specific permission: `Use my default`; observed global default `Allow low-risk actions`.
- Runtime connection: authenticated requests to its exposed tools succeeded.
- Exposed callable tools on 2026-10-23:
  1. `pine_chat_workspace_info`
  2. `pine_chat_workflow`
  3. `pine_chat_preview_info`
- The app's underlying MCP URL was **not independently returned by app-configuration tooling**. Its responses matched the Pine Chat MCP workspace payload; do not assume the exact URL without inspecting the app configuration.

## Advertised versus callable functions

The workspace metadata advertised these ten functions:
1. `pine_chat_workspace_info`
2. `pine_chat_workflow`
3. `pine_chat_preview_info`
4. `pine_beta_feature_catalog`
5. `pine_beta_native_request`
6. `pine_beta_job_status`
7. `pine_beta_submit_feedback`
8. `pine_beta_paper_order`
9. `pine_beta_preview_event`
10. `pine_beta_recent_receipts`

Only the first three were callable through `Pine ENgine USER BETA` in the verified ChatGPT tool inventory. The remaining seven were **not exposed** through that app, even though they appeared in workspace metadata.

## Last observed runtime responses

`pine_chat_workspace_info`:
- `project=pine_mcp_chat`
- `tenant=owner_oauth_only`
- `state=mvp_protocol_connected`
- `mode=read_only`
- `can_execute_native=false`
- `can_trade=false`
- `can_read_private_files=false`

`pine_chat_preview_info`:
- `status=private_demo_generated`
- `live_ui_hosted=false`
- `live_tradingview_connected=false`
- `real_chat_model_connected=false`
- Synthetic prototype source: https://github.com/aarondash5-star/business-house-matrix/blob/docs/modular-mcp-chat-template-20261022/prototypes/pine-mcp-chat/index.html
- Reported mobile viewport checks: 320, 360, 390, 430, 768, 1440 pixels.

These values are endpoint self-reports, not proof of deployment, model connection, or native TradingView certification.

## Canonical successor

- Personal/private skill-based plugin: `pine-chat-mvp-mcp`
- Plugin ID: `plugins_6ad9e6c5d15081918e6856287a28c61a`
- Verified release: `0.2.0`
- Release ID at archive time: `pluginrel_6adaf3216ef881919b5c126dd540e7e4`
- Configured MCP URL: `https://saczglesalubroyaucqe.supabase.co/functions/v1/pine-chat-mvp-mcp/mcp`
- Transport: streamable HTTP
- Authentication: Supabase OAuth, DCR; `email` and `offline_access` scopes.
- Its current package documents all ten tools. This does **not** alone prove all ten are callable through ChatGPT.

Keep the separate `Pine Manbir SSH` plugin unchanged. It is the only approved route for native Windows/TradingView operation and is not a replacement for the beta chat plugin.

## Deprecation decision and recovery

1. Treat `Pine ENgine USER BETA` as a legacy app; do not use it for new beta capability work.
2. Pre-removal recommendation was to verify all ten successor tools first. The owner requested immediate legacy removal; that removal is complete, while the successor's full ChatGPT tool exposure and owner-authenticated smoke tests remain **PENDING**.
3. The owner explicitly requested removal on 2026-10-23; the Plugin Management connector returned `status=uninstalled` for the exact app `Pine ENgine USER BETA`.
4. If reference is needed, use this document, the current personal plugin release, and the existing Supabase Edge Function source. No credentials or OAuth tokens are archived here.
5. Reinstallation/rollback may require app-owner configuration access; this document is an operational reference, not a restorable app export.

## Confirmed removal receipt

- Exact target: `Pine ENgine USER BETA`
- Action: uninstall/disconnect legacy ChatGPT app
- Connector result: `uninstalled`
- Date: 2026-10-23 (IST)
- Preserved: `pine-chat-mvp-mcp` v0.2.0 and `Pine Manbir SSH`
- Recovery: this is a reference archive, not a restorable app export. Recreating the old app would require owner-authorized app configuration.

## Safety boundaries

No live broker, production alerts, publishing, protected-chart changes, or private Windows/TradingView actions are authorized by this legacy app or this archive.

## Project reference

https://github.com/aarondash5-star/business-house-matrix/issues/2
