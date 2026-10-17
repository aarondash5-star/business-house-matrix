# Business House AI Matrix — Open WebUI-first cloud pilot

**Approval:** Open WebUI first; OpenClaw deferred. **Deployment target:** Render Free. **Status:** deploy-ready specification, NOT confirmed live. **Isolation:** new Git repository, dedicated Render web service and disposable Render database. No Moksha/Andaz/other project assets.

## Why this deployment

- Reuse official pinned `ghcr.io/open-webui/open-webui:v0.11.3-slim` container. No from-scratch web frontend.
- `render.yaml` creates an HTTPS web-service on Render Free plus isolated free PostgreSQL database. It requires an independently connected Render account.
- `WEBUI_ADMIN_EMAIL` and `WEBUI_ADMIN_PASSWORD` are prompted privately by the platform on initial Blueprint creation. Do not place them in the repository or chat.
- DB credentials are wired via Render Blueprint `fromDatabase`, and `WEBUI_SECRET_KEY` is generated server-side.
- `WEBUI_AUTH=true` and `ENABLE_SIGNUP=false` eliminate unauthenticated use or first-user signup race; admin is precreated from secret env values.
- There is no model backend yet; this is UI-first only. LangGraph, Temporal, MCP and Ollama remain architecture components for later phases, not cloud components now.

## Blockers / feasibility risks

- Render Free is **512 MB RAM**. Even the slim Open WebUI release may exceed that. Real startup, memory and login tests are mandatory. Do not automatically upgrade to a paid instance.
- Render Free sleeps after 15 min idle and has no persistent disk; use external PostgreSQL. **Its free PostgreSQL instance expires 30 days after creation, and has no managed backup**. This is a *temporary pilot only*. Export database securely (out-of-band, not Git) before expiry.
- Knowledge-file uploads and local vector cache will be lost on restart/redeploy. **Do not upload important files or use knowledge/RAG during this pilot.** Cloud object storage or a persistent VM comes after pilot.
- No model access is preconfigured; users can authenticate, but cannot get AI responses until a separately reviewed inference endpoint is connected. Exposing a local Ollama port publicly is forbidden.
- Render workspaces can bill for quota excess when a payment method exists. Confirm monthly spend limit and usage policy in Render before provisioning.
- Open WebUI is free/source-available under licensing restrictions, not OSI open source; preserve its attribution.

## Deployment checklist (not yet executed)

1. Install/connect Render in ChatGPT with account approval. Choose free plan and review app + DB cost before deploy.
2. Create **new private independent GitHub repository** under the explicitly selected connected account; push all tracked files. Do not push into Moksha Master.
3. Import `render.yaml` as Blueprint from the Git repository. Supply admin email and strong unique password through Render's secret-configuration screen only. No public signup window.
4. Check build and instance logs for memory exhaustion and PostgreSQL driver errors; test `/health`, login, signup-denied, and a cold-start after idle.
5. Record image digest, instance size, service URL, database expiry, health-test evidence and cost. Do not claim deployed until verified.
6. After pilot, migrate database with `pg_dump` + `pg_restore` to durable dedicated PostgreSQL; switch `DATABASE_URL` without losing `WEBUI_SECRET_KEY`. Do not put exports in Git.
7. If memory or startup fails, stop: choose another verified free-quota compute service. Never silently switch to a paid tier.

## What is versioned

The repository stores upstream image reference, infrastructure-as-code, application architecture and tests. It **does not store** passwords, user history, operational database content, uploads or model weights. Use a separate secure backup for data migration.

See `docs/CLOUD-DEPLOYMENT-DECISION.md` for gate-by-gate rationale and constraints.
