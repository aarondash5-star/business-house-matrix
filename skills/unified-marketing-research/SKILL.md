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
