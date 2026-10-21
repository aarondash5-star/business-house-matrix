# Engagement Core GSC → Business House Matrix Marketing Brain: verified read-only handoff

**Live evidence date:** 2026-10-22 IST / 2026-10-21 UTC  
**Scope:** User-approved per-property Google Search Console research metrics for Moksha Wellness; this does NOT link Business House Matrix's architecture or credentials to Moksha Master.

## Owner authorization and verified production source

The user confirmed Engagement Core's Google Search Console admin says **“read only”**, then reconnected the existing private ChatGPT WP Manager connector. Fresh authenticated live reads succeeded:

- `WP Manager list_sites` returned **Moksha Wellness Goa**, `https://mokshagoa.com`, site UUID `79e365b9-fdbb-42cc-82c4-78d7fb8d344f`, active. This UUID is an owner-scoped routing identifier, not a Google credential.
- `gsc_status(site_id)`: `configured:true,connected:true,scheduled:true`, property `https://mokshagoa.com/`, scope exactly `https://www.googleapis.com/auth/webmasters.readonly`; last daily snapshot `2026-10-21T15:16:43Z` with **155 clicks, 2,448 impressions**. This is the prior WordPress daily aggregate snapshot, not the total derived from top query rows.
- `gsc_search(site_id,dimensions:["query"],limit:50)` returned 50 actual query Search Analytics observations for **2026-09-20 to 2026-10-18**, source `google-search-console-direct`. Specific examples: `mud bath goa` clicks 5, impressions 97, avg position 1.48; `ice bath in goa` clicks 5, impressions 34, avg position 3.21. Per-query CTR and position preserved as given by Google. Do not claim these are absolute search volumes or all property totals.
- `gsc_sitemaps` returned `https://mokshagoa.com/sitemap.xml`, `warnings=0`, `errors=0`, last downloaded **2026-10-20**, confirming live read-only API functionality.
- **Connector input-schema issue:** passing explicit date strings to the `gsc_search` tool surfaced an incorrectly double-escaped input regex that rejects normal `YYYY-MM-DD` strings. Omitting date arguments invokes the Engagement Core audited server-side default period; the successful response supplies actual `start_date` and `end_date`. This bug should be corrected in the private WP Manager tool schema in its normal approved release process, not by weakening WordPress date validation or fabricating a query period.

## Matrix implementation and real data transfer

The source `marketing/mac-brain/gsc_metrics.py` has a new strictly validated `import_engagement_core(report,expected_site)` and CLI `import-bridge --site`:

- Requires exact expected HTTPS property, `source=google-search-console-direct`, `dimensions=["query"]`, genuine start/end dates, a bounded 1–250 query rows, five allowlisted numeric/query fields, no extra schema fields.
- Removes likely private/email/secret queries; validates numeric impressions, clicks, CTR, position; writes the **metrics-only** payload as source `engagement_core_gsc_readonly_bridge` into owner-permissioned Mac SQLite. Does NOT copy WordPress access token, GSC OAuth refresh token, WordPress bridge bearer, secret or cookie.
- Idempotent content-based batch digest; retains exact property and query period. Existing `unified_research.collect(topic,site)` displays these as site-scoped evidence alongside SearXNG and Trends without combining their numeric meaning.
- Source committed `e1a494e4b6853a3d6ccbac426854b442959253e0`, verified tests commit `9aab04cb472a55af52934cea93752589ef089104`. Mac deployment via pinned immutable GitHub source, private `gsc_metrics.py.pre-engagement-core-bridge-20261022` rollback backup, **49/49** regression tests PASS. Authenticated Mac SSH deployment terminal receipt `d28db34a-bd44-455f-bf3b-6c1dc76c32ca` exit 0.
- First source-verified import: **50 rows**, site `https://mokshagoa.com/`, source `engagement_core_gsc_readonly_bridge`, period `2026-09-20..2026-10-18`, Mac batch `d08c6c7e079ba074df39ad0aeb588da3`. Terminal SSH receipt `5d2d74e1-18d7-41c3-8d6e-bf6aa008aa3e`, exit 0. Independent local `gsc_metrics.py brief 'mud bath sauna ice bath spa' --site 'https://mokshagoa.com/'` showed verified rows and matching metric values.
- First autonomous Brain `research_brief` job queued with user-approved `site:"https://mokshagoa.com/"`, `include_web:false`; UUID `78369f74-4d48-4802-b006-3b54dd6da5ad`. Brain's existing 2-minute cron, no new service, no paid inference or publishing. **See later receipt for terminal acceptance state**.

## Connection levels — don't overclaim

**Verified now:** (1) Engagement Core's existing Google OAuth and read-only Search Analytics API, (2) private WP Manager authenticated access, (3) one-shot metrics-only data import into independent Mac Matrix Brain with accurate origin/date/row validation.

**Not enabled:** a permanent **unattended cross-system refresh from WordPress to Mac**. The current ChatGPT WP Manager connector uses an interactive owner authorization; that bearer must NOT be copied to Mac cron. To automate daily future GSC ingestion, first deploy a **narrow, revocable metrics-only delegation** through the existing Engagement Core / paired authenticated bridge, scoped to the exact GSC property, bounded settled query dates/rows, no passwords/customer data, no broader WordPress API. Preserve the current owner-controlled Google OAuth and WordPress daily sync. Then test that delegated token's expiry, RLS/ACLs, quota, logging and revocation. This is separate from the successful one-time snapshot; no unattended GSC pull should be claimed until certified.

**No re-consent needed:** The previously deployed Mac Desktop OAuth enrollment is discontinued, `bhm-gsc-oauth-enroll.service` stopped, disposable token removed and localhost listener closed. No Mac-side Google credentials ever configured.

## Operational commands

```bash
B=/opt/business-house-matrix/marketing/brain
python3 "$B/gsc_metrics.py" status --site 'https://mokshagoa.com/'
python3 "$B/gsc_metrics.py" brief 'mud bath sauna ice bath' --site 'https://mokshagoa.com/'
python3 "$B/unified_research.py" collect 'Goa mud bath wellness' --site 'https://mokshagoa.com/' --skip-web
python3 "$B/brain.py" receipt 78369f74-4d48-4802-b006-3b54dd6da5ad
```

**Keep credentials inside WordPress; no direct public GSC proxy; no WordPress change made.** No publication/spending enabled, Mac 68°C render protection unchanged, Gate 1 research transport unchanged.


## Final autonomous acceptance — verified

**Mac cron completed** `research_brief` job `78369f74-4d48-4802-b006-3b54dd6da5ad` **on attempt 1**, without manually invoking `work-once`, in **0.011 s**. The result independently reports `verified_property_performance.status="observed"`, source `engagement_core_gsc_readonly_bridge`, property `https://mokshagoa.com/`, **10 relevant source-attributed query observations** from the persisted 50-row snapshot and `publish_approval=false`. Queue state advanced **14→15 completed**. SSH final receipt `22390ef7-6179-455b-9f46-66f692b46eae` terminal status completed, exit 0. This proves the **local GSC evidence is consumed autonomously**, **not** that the original Google data source is fetched unattended from WordPress to Mac. WordPress stays the only Google OAuth owner.


## Daily unattended handoff — enabled via existing ChatGPT app permissions (2026-10-22 IST)

**Minimal-reuse decision:** Rather than install a new WordPress exporter, public endpoint, OAuth client, Mac private-bridge token, or background daemon, use a daily **ChatGPT scheduled task** as the owner-authorized orchestration boundary. Task title **Matrix GSC Daily Sync**, cadence approximately **08:00 Asia/Kolkata**, enabled by the owner in this conversation. The task dynamically rediscovers the owner-paired site via the existing private `WP Manager`, checks `gsc_status` for the exact property and `webmasters.readonly` scope, reads up to 50 authentic `gsc_search` query rows (using WordPress-side default settled interval while tool's explicit-date JSON schema is broken), validates provenance, source, row types and privacy, and transports *only* a bounded JSON metrics document via existing `Generic Linux SSH` to `mac-linux` for `gsc_metrics.py import-bridge --site https://mokshagoa.com/`. Mac SQLite digest makes repeated snapshots safe to reimport. No Google or WP token is given to the independent Mac Brain.

**Acceptance distinction:** The task has been successfully **created and enabled**. Prior Mac bridge importer and autonomous Brain consumption are verified (49/49 unit tests; 50-row import and 10-row research-brief), **but this newly scheduled automation has not yet performed its first daily run**. A separate one-shot CLI smoke attempt immediately after creating the task returned a *transport-layer internal SSH connector error without a receipt*, followed by two failed read-only host status calls; treat the test as **outcome unconfirmed**, do not claim live scheduled-run success and do not blindly retry commands with uncertain execution. Existing historical receipt remains valid. The daily task will mark source/connection failures honestly, without writing synthetic data or exposing secrets.

**Run boundaries:** user-visible notification only when newly ingested or material blocker; fail closed on stale/missing source, invalid property/Google scope, WP connection failure, Mac bridge unavailability, unexpected schema or privacy data, or ambiguous task receipt. No modifications to WordPress, Google OAuth, GSC provider cron, root, Wi-Fi, firewall, paid inference, publishing or temperature guard; no data files in public GitHub. Scheduled task requires *continued* authorization of **both** WP Manager and Generic Linux SSH in the ChatGPT account and access to those plugins at task runtime.

**Potential future move:** If daily task-based orchestration proves fragile, design a formally scoped expiring metrics-only service-to-service delegation with owner approval and independent release QA; never copy WP bridge/admin bearer or Google tokens to Mac. No new backend is currently deployed.
