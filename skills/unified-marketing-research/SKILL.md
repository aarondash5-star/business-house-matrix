# Unified Marketing Research — source skill

**Scope:** Independent Business House AI Matrix Marketing Brain. **Source of truth:** [unified research runbook](../../docs/research/UNIFIED_MARKETING_RESEARCH_2026-10-21.md), official SearXNG and Google Search Console API documentation. Never synchronize to Moksha Master automatically.

## Input

Enqueue `research_brief` with `{"topic":"PUBLIC keyword/topic","geo":"IN","site":null,"include_web":true}`. Uses existing Mac 2-minute cron and idempotency keys. Valid geos IN/GB/RU/US. Optional exact *authorized* GSC property; never silently assume a brand.

## Source contracts

- SearXNG: Dell rootless AGPL3 metasearch; authenticated Mac-Dell encrypted research relay `encrypted_signed_relay_v1`, no public search listener, 3/min 100/day Mac cap, public-only query, HTTPS citation URLs, untrusted web snippets. **Gate 1 certified.**
- Google Trends: national Google public Trending Now RSS cached 6-hourly, up to 4 reads/day, plus real manually imported Google Explore CSV. No invented local volumes or cross-comparison normalized trends.
- Google Search Console: owner-approved private site; `gsc_metrics.py` local store, CLI import of actual Search Analytics CSV; optional read-only Google OAuth Search Analytics API after separate account approval. Never copy site data, credentials, booking/customer info or user tokens to GitHub, Dell, LLM providers or unrelated projects. Missing GSC is an explicit `property_not_selected` or `no_property_data`, not zero search demand.
- Do not blend web SERP results, GSC clicks and normalized Trends indices into the same numeric ranking, and do not derive brand colors/fonts directly from Trends.

## Verified state — 2026-10-21

42/42 Mac regression tests PASS, and unattended Brain job `8a7fd707-8c77-49d9-8335-b6487aeff4b2` completed on attempt 1 via Mac cron and encrypted relay, 5 HTTPS sources, no relevant Trends hit, GSC unconfigured explicitly. Gate 1 unaffected; Gates 2–4 still pending. No paid fallback, auto publication, thermal-unsafe inference, direct Google CSE JSON, Tavily, or cloned new SearXNG.

## Fail-closed and QA

Always use pinned GitHub commit for runtime deployment (raw `main` may be cache stale), backup `brain.py`, execute `python3 -m unittest discover -p 'test_*.py' -q`, enqueue a unique safe-topic task, and verify terminal job `receipt` before saying integrated. If all sources are missing/unavailable, return transparent missing evidence; no dummy content. Never open a billing permission for GSC, whose documented API is quota-limited rather than a paid SERP proxy.

## Useful commands

```bash
B=/opt/business-house-matrix/marketing/brain
python3 "$B/unified_research.py" status
python3 "$B/brain.py" enqueue research_brief --payload '{"topic":"Goa wellness","geo":"IN"}' --key demonstration-r1
python3 "$B/brain.py" receipt JOB_ID
python3 "$B/gsc_metrics.py" status
```

**OAuth not enrolled as of first certification:** obtaining an authorized, verified site property and read-only consent is an explicit remaining integration step; never treat it as complete based solely on module availability.


## Direct GSC OAuth provisioning (2026-10-22)

The independent Matrix's Mac now includes `gsc_oauth_setup.py` as a **temporary localhost-only, owner-mediated Google Desktop OAuth enrollment**. It does not use Windsor or GSC Wizard; read-only `webmasters.readonly`, PKCE, CSRF state, private 0600 token storage, verified property `https://mokshagoa.com/` or domain equivalent and post-consent direct Search Analytics sampling. User must consent from browser **on Mac** and upload a legitimate Desktop OAuth client JSON created in their own Cloud project. Do not paste Google tokens/client secrets to ChatGPT, public GitHub or relay. OAuth external Testing refresh tokens may expire in 7d. 47/47 Mac tests passed; verified loopback form and host guard, **NOT yet authorized or GSC source-connected** until Google consent and first real receipt. Reference [provisioning guide](../../docs/research/DIRECT_GSC_OAUTH_ENROLLMENT_2026-10-22.md).


## Current GSC canonical provider supersedes Mac OAuth (2026-10-22)

**Important source correction:** Existing Moksha WordPress **Engagement Core** is the canonical Google Search Console OAuth/data owner, with `GREC_GSC` first-party readonly Google API, encrypted WP credentials and private owner-scoped `WP Manager` tools `gsc_status`, `gsc_search`, `gsc_inspect`, `gsc_sitemaps`. Historical OAuth connected snapshot exists, **live connected status not yet verified** because this ChatGPT project's WP Manager tools returned an internal error. Stop recommending the old Mac 127.0.0.1/Desktop OAuth page: one-time enrollment stopped, setup token removed and listener closed. Preserve independent Matrix/Moksha Master boundaries: only explicitly owner-approved *metrics-only* research data may cross, and never WP or Google refresh tokens. Source [canonical reuse decision](../../docs/research/REUSE_ENGAGEMENT_CORE_GSC_2026-10-22.md), WordPress [first-party source](https://github.com/karanzing1992/engagement-core/blob/main/src/class-grec-gsc.php). On WP Manager recovery, discover `list_sites` to obtain legitimate site ID then check `gsc_status` and run read-only `gsc_search`. No silent second OAuth client or duplicate reporting cron.


## GSC first working data link — 2026-10-22 (supersedes previous disconnected status)

Owner-reconnected **WP Manager** can now retrieve live Engagement Core GSC data using authentic site UUID `79e365b9-fdbb-42cc-82c4-78d7fb8d344f`: `gsc_status` connected read-only + WordPress daily sync; `gsc_search` default date range delivered 50 genuine query rows for 2026-09-20..2026-10-18; `gsc_sitemaps` passed. Preserve WordPress as sole Google OAuth owner; no token transfer. Matrix's `gsc_metrics.import_engagement_core()` is approved for an explicit **owner-authenticated snapshot import** only, validating source `google-search-console-direct`, exact selected site and 1–250 bounded query rows; `engagement_core_gsc_readonly_bridge` is persisted in private Mac SQLite. Mac test **49/49 PASS**, 50 rows imported, original autonomous Mac cron independently consumed 10 relevant observations in completed job `78369f74-4d48-4802-b006-3b54dd6da5ad`. WP Manager tool's explicit date inputs are schema-bugged (double escaped regex); use default settled date range until properly fixed. **No unattended WordPress-to-Mac daily pull is active**; never transplant private WP Manager bearer into Mac. Read [live handoff](../../docs/research/ENGAGEMENT_CORE_GSC_LIVE_HANDOFF_2026-10-22.md).


## Daily GSC handoff orchestrator — activated, first schedule unverified

The owner enabled a **ChatGPT automation named Matrix GSC Daily Sync**, daily about **08:00 IST**. Reuse existing owner-authenticated `WP Manager` read-only GSC and `Generic Linux SSH` to deliver a **bounded property-specific, sanitized 50-row metrics snapshot** to `mac-linux` through the existing `gsc_metrics.py import-bridge` CLI; no Google/WordPress OAuth/token/bearer is put on Mac or in GitHub. Do not create a second scheduler or open a WordPress endpoint. Demand `list_sites` owner pairing, exact `gsc_status` readonly property, `gsc_search` provenance and settled dates, transport receipt terminal exit 0, local GSC status and optional Brain research evidence readback. WP Manager explicit date fields currently have malformed JSON-schema regex: omit dates until source is fixed, then use 28 settled days. Fail closed if plugin unavailable or backend status uncertain; no blind duplicate write. **First scheduled automation execution has not been observed yet.** Reference [GSC handoff](../../docs/research/ENGAGEMENT_CORE_GSC_LIVE_HANDOFF_2026-10-22.md).


## Video release gate status and takeover (2026-10-22)

Core signed research **Gate 1 remains PASS**. A new existing-Mac-Brain `reel_pilot` task now links private staged original photos, `unified_research.collect` signed public SearXNG with independent GSC/Trends evidence, a **public-source-only** Groq OSS hosted concept, and strict fail-closed Mac thermal render prerequisites, with no authorization to spend or publish. **57/57** tests on pilot deployment; unattended first pilot `02904304-941d-4d66-9477-c1c96542a88f` produced 4 source leads + creative DRAFT but stopped `BLOCKED_RENDER_DISABLED`, **no video**. The Apple SMC observed 83.8°C and Gate sensor series 60→78°C breaches 68°C cutoff, so DO NOT toggle render to pass a gate. Existing active-load 24h soak failed at 93°C after ~55s. The passive no-CPU-load observer `passive_soak.py` is now running on Mac, 5-minute samples over a proposed 24-hour window; **62/62** regression tests pass. This observer cannot certify active-load, reboot or service recovery. Current gates: **1 PASS; 2 BLOCKED; 3 partial source/draft PASS, video not certified; 4 active soak FAILED, passive monitoring only**. Canonical [takeover and receipts](../../docs/handoffs/MARKETING_GATES_2_TO_4_TAKEOVER_2026-10-22.md). Escalate cooling or critical blockers, never replace a required new MP4 with historical smoke reels. No Moksha Master sync.
