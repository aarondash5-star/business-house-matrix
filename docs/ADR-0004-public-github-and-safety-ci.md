# ADR-0004 — Public Aaron GitHub repository and deployment safety gate

**Project:** Business House AI Matrix (separate from Moksha Master)
**Date:** 2026-10-18
**Status:** Accepted public-repository exception; CI review requested

## Decision

The user accepted a **public** repository under `aarondash5-star/business-house-matrix`. This supersedes ADR-0003's earlier requirement that the repository be private; all other architecture and cloud approval rules remain intact.

- GitHub is the source of truth and migration anchor. Original Git history and 23 tracked source files were verified after transfer.
- Source, architecture decisions, pilot templates and general CI workflows may be public.
- No live passwords, token material, user/customer data, runtime database content, private logs, keys, backup archives or business-sensitive work may be checked in.
- The first CI gate runs offline public-repository safety checks, Python compilation and existing starter tests on PRs and main. It uses read-only GitHub permissions, no cloud identities and no deployment calls.
- The safety script provides a *high-confidence lightweight screening*, not proof that arbitrary secrets are absent. Additional secret-scanning tools and human review are required before cloud credentials are configured.
- `render.yaml` is historical; Render is not the approved host. The historical import workflow was removed when the original commit was restored.
- OCI Always Free remains primary, Google Cloud Run remains fallback. Do not initialize cloud CLI authentication, run deployments, use charged resources or mutate external cloud state without the separate gated rollout.
- Open WebUI is the sole first-phase UI. LibreChat excluded; OpenClaw deferred until pilot acceptance.

## Remaining approval gates

1. CI green and reviewed.
2. Confirm selected OCI or GCP project/tenancy and real current free-quota capacity.
3. Set up a project-specific, least-privileged identity, ideally short-lived workload federation.
4. Add manual-only deployment workflows gated by a GitHub Environment. Never deploy on a PR or raw push.
5. User approves any actual cloud resource creation after reviewing exact costs and security boundaries.

Public visibility is a user-approved exception only for this codebase; it does not authorize publication of data belonging to other projects.
