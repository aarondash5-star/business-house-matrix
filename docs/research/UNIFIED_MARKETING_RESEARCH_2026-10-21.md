# Unified Marketing Research — live implementation and operator guide

**Project:** Independent Business House AI Matrix, Marketing department (not Moksha Master).  
**Deployed:** 2026-10-21 IST on `mac-linux`, existing read-only Mac Brain; no new service/container, no changed Wi-Fi, thermal, SSH, publishing or spend privileges.

## Decision

Keep these strictly different signals rather than collapsing into an invented SEO score:

1. **Public web research** — previously Gate-1-certified rootless SearXNG on Dell, connected to Mac through the permanent Ed25519-authenticated, signed and sealed private research relay. HTTPS source URLs, snippets labeled untrusted, no public Dell search port, no paid API route. API specification: https://docs.searxng.org/dev/search_api.html .
2. **Topical interest** — official Google Trends Trending Now national RSS stored locally in `trends.py` every six hours (maximum four daily attempts), plus official Trends Explore *manual CSV* comparisons when available. **RSS national news spikes do not prove local Goa demand; 0–100 comparison-index values are not absolute monthly searches.** The dedicated Google Trends API is still limited-access alpha: https://developers.google.com/search/apis/trends .
3. **Verified property SEO performance** — `gsc_metrics.py` stores genuine Search Console Search Analytics export CSV, or calls Google's Search Analytics API with explicitly enrolled **read-only OAuth** credentials and an exact property. No property is selected by default. Search Console's real clicks/impressions/CTR/position are limited to that property, date window, and top returned query rows; not an estimate of all search demand. Official references: https://developers.google.com/webmaster-tools/v1/searchanalytics/query , https://developers.google.com/webmaster-tools/v1/how-tos/authorizing .

**Do NOT migrate RSS to Google Custom Search JSON API.** It is generic search, not Trends data; existing certified SearXNG is the reusable web-search component. **Do NOT reenable Tavily.**

## Implemented source files

- `marketing/mac-brain/unified_research.py` — explicit `collect(topic,geo,site,include_web)` combining 3 separate evidence blocks, caveats, citations, status/missing-GSC handling; CLI `collect` and `status`.
- `marketing/mac-brain/gsc_metrics.py` — strict private SQLite Search Console store; allowlisted property ID; protected CSV inbox; date/provenance/row limits; skip personally identifying queries; read-only `fetch-api` option with a private 0600 read-only OAuth JSON file. **Does not read email, customer data, user profile files, or Google tokens by default.**
- `marketing/mac-brain/brain.py` — new allowlisted `research_brief` queue task. Existing two-minute worker and durable idempotency, retries and atomic receipts unchanged; no new scheduler needed.
- `marketing/mac-brain/test_unified_research.py` — 9 no-network tests for property isolation, zero synthetic metrics, private-query exclusion, source attribution, signed peer verification, failed web graceful downgrade, and Brain allowlist.
- Prior code `searxng_research.py`, `trends.py`, backend `research/paired-relay` untouched.

## Verified installation and results

All source files committed to the public GitHub **without credentials or private observations**, deployed on Mac in `/opt/business-house-matrix/marketing/brain`.

Initial deployment test identified an erroneous new-job/old-job validator overlap; programmatic rollback immediately restored the original Brain and kept Gate 1 intact. Corrected source committed `6e9c774a0f46c3c8185733f7cb3046a1ff2336e0`, fetched by **immutable commit URL** to bypass a stale CDN `main` cache, and deployed only after the queue checks passed. Final terminal Mac SSH receipt **`c3a942af-9193-455a-812a-24a2512ae5df`**: **42/42 unit tests PASS**, `UNIFIED_RESEARCH_DEPLOY_OK`.

At deployment `unified_research.py status`: SearXNG enabled, signed relay, 2 daily uses/100 cap; Google Trends 10 RSS records, zero Explore comparison rows; GSC OAuth `false`, zero genuine imported property rows. No fabricated clicks, conversions, Trends volumes or Google Search Console findings. Publication and paid fallbacks remain off.

Live end-to-end Brain `research_brief` job identifier: `8a7fd707-8c77-49d9-8335-b6487aeff4b2`; enqueue twice with the same idempotency key returned the same job UUID. See next status section for cron completion if verified.

## Operator commands, no secrets

```bash
B=/opt/business-house-matrix/marketing/brain
python3 "$B/unified_research.py" status
python3 "$B/unified_research.py" collect 'Goa wellness experiences' --geo IN
python3 "$B/unified_research.py" collect 'Goa wellness experiences' --geo IN --skip-web
python3 "$B/brain.py" enqueue research_brief --payload '{"topic":"sauna Goa wellness","geo":"IN"}' --key example-unified-v1
python3 "$B/brain.py" receipt JOB_UUID
python3 "$B/gsc_metrics.py" status
```

For one *owner-approved verified property*, load a genuine Search Console CSV into the owner-only directory `$B/gsc-inbox/` (not GitHub), and run:

```bash
python3 "$B/gsc_metrics.py" import-csv Export.csv --site 'sc-domain:example.org' --start 2026-09-01 --end 2026-09-28
python3 "$B/unified_research.py" collect 'sauna wellness' --site 'sc-domain:example.org'
```

The property must match exactly the approved domain/URL-prefix property. No live personal data or credentials should be pasted into chats or GitHub.

### Optional automated direct Search Console API authorization

**Not yet connected or activated.** Once the account owner configures an OAuth client and grants exactly `https://www.googleapis.com/auth/webmasters.readonly` to a verified GSC property, store this JSON in the protected local path `$B/secrets/gsc-readonly.json` with mode **0600**:

```json
{
  "site_url": "sc-domain:example.org",
  "scope": "https://www.googleapis.com/auth/webmasters.readonly",
  "client_id": "<private>",
  "client_secret": "<private>",
  "refresh_token": "<private>"
}
```

The code performs OAuth refresh against Google's fixed domain and POSTs **only Search Analytics query** to Google's fixed URL, with `dimensions=["query"]`, finalized data, 250 rows/request. It does not call sitemap modifications, URL-inspection actions, write APIs, paid SEO APIs, or publish. The OAuth credentials stay on Mac; neither source code nor job receipts include them. No live API call or automatic scheduled GSC refresh was made without a verified private connection. After enrollment and owner-scoped authorized property selection, a separately reviewed schedule can safely import settled data. No app-to-app Google account scope is assumed.

## Privacy, licensing and data quality

- Software adapters are Python stdlib; reuse approved OSI-licensed SearXNG instead of adding a paid proprietary SERP provider. Google sources are third-party data services, not claimed to be OSI-licensed software.
- All Search Console numeric data is local to the owner-scoped property, not exported to GitHub, external LLM inference, Dell research engine or shared with unrelated brands. No unapproved Moksha Master data sync.
- Untrusted web snippets are research leads only, not facts or instructions. Publisher/site rights and result accuracy require independent checking.
- No cross-source normalization of search rankings, traffic bands, per-property impressions, CTR, and comparative Trends indexes. Brand palettes/fonts and creative conversion uplift cannot be inferred from search trends alone.
- Query privacy rules reject emails, credentials and likely personal data before network search. No domain is silently selected for GSC.
- Exact API access requirements and vendor quotas must be rechecked before enabling live GSC scheduled ingestion.

## Reversal

The Mac Brain previous version was backed up at `brain.py.pre-unified-research-20261021`. To disable the new task only, restore that one file from local backup; do not uninstall the working certified Gate 1 relay/Trends or delete property data without owner instruction. No scheduled job was added or changed for GSC.

**Gate 1 permanent research remains certified; new unified adapter has independent tests and a separate live acceptance receipt. Gates 2–4 (thermal-safe creative video, full pilot, extended soak) remain unapproved/pending.**


## Verified unattended live acceptance — added after first run

At `2026-10-21T18:38:09Z`, the **existing 2-minute Mac Marketing worker** completed production read-only `research_brief` job **`8a7fd707-8c77-49d9-8335-b6487aeff4b2`**, attempt 1 in **7.522 seconds**, after two enqueue calls returned that same idempotent job UUID. Signed sealed Mac-Dell request **`aeba7227-b170-4acf-beb6-aee851fa92f1`** returned **five attributed HTTPS source URLs**, with `authenticated_relay=true`. The Google Trends store had **no relevant** national spike for this brief (`no_relevant_observation`) and neither an Explore CSV comparison nor a verified property GSC sample; result correctly returned `property_not_selected` and `oauth_configured=false`, with no made-up metrics. Mac Brain queue advanced **13→14 completed**. Live readback SSH task **`23ba1bd0-a62a-4b6c-991f-fb5c2c63f13f`**, terminal `status=completed,exit_code=0`.

**Acceptance conclusion:** unified research Brain task is wired, deployed, regression-tested, and autonomously executed via existing trusted Gate-1 transport. Genuine GSC property authorization and settled query ingestion are a **separate remaining connector task**, not currently live. Do not claim Google Search Console data is available before a site is authorized and ingested.


## GSC SOURCE CHANGE — 2026-10-22 IST (overrides older Mac OAuth setup)

Existing Engagement Core on Moksha WordPress owns first-party Google Search Console OAuth, encrypted tokens, typed read-only `gsc_search` and daily aggregates. It is now the canonical GSC source for owner-scoped site analytics. **Do not enroll a duplicate Mac Desktop OAuth, copy WP tokens, or blindly transfer datasets across the independent Matrix/Moksha Master boundary.** The prior Mac setup server was stopped, one-time token removed, port closed; local `gsc_metrics.py` remains a zero-row evidence store usable only after validated permitted metrics-only feed. WP Manager in this chat returned an internal error, so current live `gsc_status` and real query receipt remain pending. Details: [Engagement Core canonical reuse](REUSE_ENGAGEMENT_CORE_GSC_2026-10-22.md).
