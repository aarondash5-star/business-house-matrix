# ADR-0002 — Cloud pilot target & Git migration

Date: 2026-10-18. Decision: **render Free pilot** proposed, pending account connection, provisioning and live validation. No active deployment verified.

## Decisions

- Launch only **Open WebUI** first. Neither OpenClaw nor LibreChat in pilot.
- Use a **new private GitHub repo** isolated from all other projects, with `render.yaml` for reproducible cloud provisioning and original LangGraph scaffolding for future work.
- Choose Render Free because the available connected Vercel deployment environment is serverless and unsuited to running this stateful Python server; use the Render connector after account approval.
- For limited pilot use **isolated Render Free PostgreSQL** (time-limited 30 days); user data must be treated as disposable/test-only until migrated and backed up.
- Never reuse existing Supabase projects from other businesses. No hidden paid API subscriptions or model providers.
- Open WebUI `v0.11.3-slim` is pinned; model and LangGraph integrations deferred until UI passes QA.

## Reuse and upstream refs

- Open WebUI: https://github.com/open-webui/open-webui and https://docs.openwebui.com/getting-started/quick-start/
- Render Free limits: https://render.com/docs/free
- Render blueprint syntax: https://render.com/docs/blueprint-spec
- Open WebUI admin bootstrap: https://docs.openwebui.com/reference/env-configuration/
- Open WebUI external database: https://docs.openwebui.com/getting-started/advanced-topics/scaling/

## Required validation

App can start within Free 512MB RAM, `/health` returns 200, only bootstrap admin can sign in, no public signup, Postgres persists across restart, no secrets in Git, cloud services stay within free usage. Record expiry and a migration rehearsal before handling valuable data.

## Pending and prohibited

- Pending: connect Render, select one of the two available GitHub identities, create isolated private repository, deploy and check the live URL.
- Prohibited: reuse existing Supabase databases, publish admin credentials, expose unauthenticated Open WebUI, upgrade to paid hosting without approval, turn on OpenClaw, add real business data.
