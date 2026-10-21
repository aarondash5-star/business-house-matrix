# Direct Google Search Console API enrollment — Mac Marketing

**Date:** 2026-10-22 IST. **Project:** Independent Business House Matrix; never synchronize automatically with Moksha Master.

## Decision

Use Google's **official Search Console API** with `webmasters.readonly` only. No Windsor.ai/GSC Wizard reading dependency and no Custom Search JSON API. Direct Search Console API is free within Google's usage quotas. OAuth 2.0 user consent is mandatory; neither this repo nor ChatGPT can silently inherit tokens from unrelated connectors.

## Implemented

- Created `marketing/mac-brain/gsc_oauth_setup.py`: one-time owner-driven **127.0.0.1:18765-only** enrollment page running on `mac-linux`. The page locally accepts a Google-issued **Desktop OAuth client JSON**, launches Google's real consent flow with short-lived state + PKCE S256, requests only `https://www.googleapis.com/auth/webmasters.readonly`, and receives loopback callback. No email address, Google client secret, authorization code, access token or refresh token is committed to GitHub, pasted to ChatGPT, logged by the web server, or passed through the Dell relay.
- Upon consent, script verifies Google `GET /webmasters/v3/sites` lists either exact `https://mokshagoa.com/` or `sc-domain:mokshagoa.com` with readable permission. Only then executes a bounded first-party read-only Search Analytics query for 28 settled days, stores genuine rows locally in `gsc-metrics.sqlite3`, and commits refresh-token/client secret exclusively to Mac owner-only `/opt/business-house-matrix/marketing/brain/secrets/gsc-readonly.json` with 0600. Existing `gsc_metrics.py fetch-api` becomes usable afterward; no property fallback other than those exact two previously identified variants.
- Added `test_gsc_oauth_setup.py`, including Desktop-client-only acceptance, one-time token, secret not overwritten, missing grant rejection, forbidden file upload.
- **47/47 Mac Marketing tests passed** after deployment; Mac receipt `fc80a572-6930-43cf-8b79-d85a12ac582b`, completed/exit 0.
- Initial temporary `systemd-run --user` process died after the SSH session because `generic-auto-exec` had `Linger=no`. Changed **only that existing unprivileged account's** login lingering to `Linger=yes` via `sudo loginctl enable-linger generic-auto-exec`, then restarted temporary ephemeral user service. No SSH bridge root access, published port, Wi-Fi, browser, other login user or fan changes. Receipt `293aca1b-c629-46b1-8d88-edb6ee70527e` completed/exit 0.
- The temporary service is `bhm-gsc-oauth-enroll.service` with runtime cap 1150 seconds, bound to `127.0.0.1:18765`, memory limit 128MB, NoNewPrivileges. The one-time enrollment token expires after 1200 seconds. **Never place the transient link in the public repository**. Once consent completes or expires, enrollment service exits; it is *not* a permanent open listener.
- Post-SSH-session smoke test receipt `029abf1b-b562-4867-97e5-95ec666b16b3`: service still **active**; verified GET setup page **HTTP 200** with client-file upload, malformed Host **HTTP 403** (basic DNS-rebinding guard), `GSC oauth_configured=false` before owner consent, all generic-linux-automator/cron/mbpfan/thermald **active**.

## User action needed — ON THE MAC MACHINE

1. In a browser **on `mac-linux` (KARAN)**, open the one-time private 127.0.0.1 enrollment link returned by the authorized SSH operation. Never send the link's token to third parties.
2. In Google Cloud Console, select/create a project, enable **Google Search Console API** at `https://console.cloud.google.com/apis/library/searchconsole.googleapis.com`.
3. In Google Auth Platform, configure consent/audience and add the Google account that can read Moksha's Search Console as a test user if the app is in Testing. Create an OAuth client of type **Desktop application** at `https://console.cloud.google.com/auth/clients` and download its **client JSON** to that same Mac.
4. Upload the JSON at the loopback-only form, authorize Google's exact *Search Console read-only* permission in Google's official consent screen. The redirected local success page reports verified property and actual settled query-row count; no credentials displayed.
5. Check `python3 /opt/business-house-matrix/marketing/brain/gsc_metrics.py status` and run a direct `fetch-api --start ... --end ...` with settled dates; only enable read-only scheduled imports **after** terminal live verification and owner approval.

**Important:** Google's OAuth external testing refresh tokens generally expire after **seven days** for scopes such as Search Console readonly. A persistent production connection requires correctly configured Google Auth Platform publishing/verification as applicable, or another supported authorization approach; do not call the test-mode token permanent merely because the Mac worker persists. Google references: https://developers.google.com/identity/protocols/oauth2/native-app ; https://developers.google.com/identity/protocols/oauth2/ ; https://developers.google.com/webmaster-tools/v1/how-tos/authorizing ; https://developers.google.com/webmaster-tools/v1/searchanalytics/query ; https://developers.google.com/webmaster-tools/pricing .

## Status and safeguards

**Direct API enrollment endpoint: READY and verified. OAuth permission: NOT YET GRANTED. Real Search Analytics read: NOT YET VERIFIED. Permanent data sync: NOT ENABLED.** No fabricated Search Console metrics; no upgrade, additional data exporter, publishing, spend, Google CSE, browser session change or bypass of user consent.

After on-device Google authorization, inspect terminal `gsc_metrics.py status` and first-party request receipts before changing this status. If expiration occurs before owner consent, the nonroot service naturally exits and the token is cleaned; a new enrollment may be issued on explicit retry. The service account linger change can be reverted if no longer needed via `sudo loginctl disable-linger generic-auto-exec`, but only after checking whether other user services have begun to depend on it.


## SUPERSEDED — Existing WordPress provider discovered later on 2026-10-22

The user identified existing first-party **Engagement Core WordPress GSC**. The owner should **NOT** create or upload a separate Desktop OAuth client for the Matrix. The temporary Mac enrollment service was stopped, disposable token removed, localhost listener 18765 closed. No Google credentials ever configured on Mac. This prior operational record is retained for history only. Follow the newer [Engagement Core reuse decision](REUSE_ENGAGEMENT_CORE_GSC_2026-10-22.md): confirm the existing WordPress OAuth status by the properly authenticated WP Manager connector, and use only bounded read-only performance metrics with owner-approved project separation. Existing private GSC OAuth settings in WordPress should NOT be changed merely because WP Manager currently returns an internal tool error.
