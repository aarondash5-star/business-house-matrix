# Google Search Console provider decision — REUSE Engagement Core

**Date:** 2026-10-22 IST. **Scope:** independent Business House Matrix marketing research. The user clarified that a first-party direct Google Search Console implementation already exists in the separate WordPress Engagement Core system.

## Verified source and ownership

The existing repository `karanzing1992/engagement-core` has:

- `src/class-grec-gsc.php`: `GREC_GSC` first-party Google OAuth `https://www.googleapis.com/auth/webmasters.readonly`; privately encrypted credentials and tokens in WordPress; `status`, `search`, `inspect`, `sitemaps`; WordPress daily metrics snapshot. Private controls include `manage_options`, OAuth state, same-site validation, bounded dates/dimensions/rows and protected bridging.
- `docs/GSC_NATIVE_READONLY.md`: exact OAuth setup for **Web application** Google client at `https://mokshagoa.com/wp-admin/admin-post.php?action=grec_gsc_oauth`, with admin settings at `https://mokshagoa.com/wp-admin/admin.php?page=grec-search-console`. Do not use a Mac Desktop OAuth client for this WordPress integration.
- The existing owner-scoped WP Manager connector exposes `gsc_status`, `gsc_search`, `gsc_inspect`, `gsc_sitemaps` using authenticated `wpcontrol-mcp` + WordPress `wp-control/v1/bridge`. The gateway is a trusted connector, **not an anonymous/public API**.
- Latest repository health runbook contains historical **2026-10-12** browser evidence of a **Connected (read only)** WordPress admin state and a GSC report. This is *historical evidence*, not a fresh OAuth/token health check.

Source references:
- [GSC native implementation](https://github.com/karanzing1992/engagement-core/blob/main/src/class-grec-gsc.php)
- [GSC official rollout](https://github.com/karanzing1992/engagement-core/blob/main/docs/GSC_NATIVE_READONLY.md)
- [Private WP Manager access](https://github.com/karanzing1992/engagement-core/blob/main/docs/PRIVATE_WP_MANAGER_ACCESS.md)
- [Historical production browser evidence](https://github.com/karanzing1992/engagement-core/blob/main/docs/MASTER_STACK_HEALTH_RUNBOOK.md)

## Architecture decision

**One Google consent/token owner — WordPress Engagement Core.** Business House Matrix is still an independent project; it must not silently merge with Moksha Master or take WordPress/Google tokens to the Mac. For *owner-authorized Moksha property research*, source Search Console observations by reading `gsc_search` through the already-authenticated **WP Manager bridge**. Consume only bounded results (property ID, interval, query, clicks, impressions, CTR, position) into a local read-only evidence report **when an owner-authorized bridge is accessible**.

- Do not create a second Google Cloud client, second OAuth refresh token, duplicate Search Console cron or duplicate provider subscription.
- Do not expose Google tokens, WordPress admin auth, private bridge pairing keys or a public WP endpoint.
- Never assume the private ChatGPT plugin session authorizes a separate unattended Mac daemon. For persistent unattended Mac ingestion, first implement an explicitly delegated *read-only* scoped data capability through Engagement Core using its owner permissions; test access, data minimization, revocation, request provenance, and job receipts. Until then, the existing WP Manager allows interactive read-only research where it is connected, not an automatic Mac data bridge.
- Different brands and projects remain logically isolated. No WooCommerce/guest/accounting/booking data crosses this interface.

## Actions actually executed

1. Inspected real Engagement Core GitHub source, its GSC runbook and private WP Manager documentation; verified the native Search Analytics adapter already exists.
2. Tried the connected `mcp__Wp_Manager__list_sites` and `get_profile`; both failed **internally**, so no live `site_id` could be retrieved and no fresh `gsc_status`/Search Analytics receipt could be obtained. **Do not invent a site ID or claim new metrics.**
3. Mac `gsc_metrics.py status` returned `oauth_configured=false`, `stored_query_rows=0`; redundant one-time `bhm-gsc-oauth-enroll.service` was stopped, disposable enrollment token removed, and listener `127.0.0.1:18765` verified CLOSED. No existing Google credentials existed there and none were removed. **Terminal SSH receipt:** `07b38d94-c35a-4e1f-a3dc-795b375876cb`, `status=completed`, exit 0. Existing Generic Linux SSH bridge, cron, mbpfan and thermald remain active.
4. The former `gsc_oauth_setup.py` and test remain in source history for rollback/audit but are **deprecated/not for new setup**; the previously provided localhost enrollment link is invalid. Do not relaunch the duplicate flow without a new architectural decision.
5. The existing `gsc_metrics.py` may still store **genuine read-only evidence**, but its unconnected direct Google OAuth branch is not canonical for Moksha. Treat `gsc_connection.oauth_configured=false` as local credential status, **not proof WordPress GSC is disconnected**.

## Acceptance plan / current blocker

- Restore/reconnect WP Manager in the current independent project session (it returned an internal error, not a verified WordPress OAuth failure).
- `list_sites` must provide an authentic exact site UUID. Then `gsc_status(site_id)` must show `connected=true` and the intended property.
- `gsc_search(site_id, dimensions=['query'], start_date, end_date, limit<=250)` must return genuine non-placeholder metrics for a bounded settled date range, or an explicit empty/Google error state. `gsc_sitemaps` can further verify permission. Do not interpret zero rows alone as a successful grant.
- **Only after live success**: expose an owner-approved *metrics-only* delegation to the separate Matrix runtime, without WordPress bearer/refresh tokens on Mac. Reuse the existing `gsc_metrics.save_rows` proven origin/row validation, respecting tenant permissions. No extra Google connector or scheduled job on Mac before delegated access is verified.

**Status:** Engagement Core first-party GSC implementation EXISTING and SOURCE VERIFIED; historical connection evidence exists; current connected WP Manager session INTERNAL ERROR; live first-party query NOT VERIFIED; duplicate Mac OAuth setup STOPPED. Gate 1 SearXNG and Google Trends unaffected. No auto publication/spend or WP changes.


## Operator confirmation — 2026-10-22 IST

The owner checked **WordPress → Engagement Core → Search Console** and reports its permission status reads **“read only.”** Treat this as current *owner-observed UI status* of a read-only authorization, not an independently completed live Google Search Analytics API receipt. **Do not request a new Google Cloud OAuth client, reinstall Engagement Core, or launch the deprecated Mac OAuth setup.** Attempts to call private WP Manager `list_sites` and `get_profile` in this conversation still failed with an internal connector error; canonical GSC data remains inside WordPress. To finish the Matrix data link: restore the existing private WP Manager connection, discover the real site UUID, run `gsc_status → gsc_search` with settled dates, then authorize a narrow metrics-only delegation (no Google/WordPress token propagation, no customer data) for unattended Mac Brain ingestion. The Matrix GSC local store still has no verified imported GSC rows. This does not affect the certified SearXNG/Trends research sources.
