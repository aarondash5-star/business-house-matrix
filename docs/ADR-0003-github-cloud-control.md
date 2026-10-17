# ADR-0003 — GitHub-Controlled, Cloud-Portable Deployment

**Project:** Business House AI Matrix (independent of Moksha Master)
**Decision date:** 2026-10-18
**Status:** APPROVED ARCHITECTURE — DOCUMENTATION ONLY / NOT DEPLOYED
**Supersedes:** Render Free as the primary target in `docs/CLOUD-DEPLOYMENT-DECISION.md` (former ADR-0002). Preserve that file only as historical research. The previous Render-specific `render.yaml` is **not** an approved deployment path under this decision.

## Decision

1. **GitHub is the canonical source and deployment-control plane.** Use a new, independent **private repository** for the Matrix. Commit source, config templates, IaC, CI/CD workflows, docs and tests. Never commit credentials, chat history, databases, uploads, encryption keys or model weights.
2. **Oracle Cloud Infrastructure (OCI) Always Free is the preferred persistent pilot host**, conditional on a verified account, Arm-capable availability, application compatibility, actual available quota and tested persistent storage. No use of paid capacity without separate approval.
3. **Google Cloud Run is the alternate / migration target**, not a simultaneous default production deployment. Stay within free usage and verify billing requirements, runtime capacity, startup performance and external persistent storage first. Cloud Run is suitable for the UI and stateless components, not automatically for the full persistent Matrix stack.
4. **GitHub Actions launches the official provider CLI operations**: `oci` for Oracle and `gcloud` for Google Cloud; optional OpenTofu configuration for infrastructure declared in code. GitHub Actions is not a permanent worker/host.
5. **Open WebUI is the only pilot interface.** Ollama/local inference, LangGraph Central Brain, Temporal durable execution and MCP interfaces roll out after the frontend pilot passes its stage gates. The ninth department is **EVOLUTION** (training, correction and controlled improvement). **LibreChat excluded; OpenClaw postponed until the pilot is accepted and separately approved.**
6. **Complete project isolation:** no reuse of Moksha Master, its cloud credentials, its Git repositories, or existing Supabase projects used by other businesses. No automatic master sync.

## Role boundaries

| Layer | Owner | Job |
|---|---|---|
| User interface | Open WebUI | Secure chat/operator dashboard |
| Intelligence | LangGraph | Central Brain + nine recursive departmental subgraphs |
| Durability | Temporal | Task queues, retries, scheduling, approvals, recovery |
| Tool interface | FastMCP | Expose approved capabilities |
| Tool governance | ContextForge | Scoped routing, tool access and audit (after scale justifies it) |
| Model serving | Ollama with licensed open-weight models | Optional local/private inference; not hosted in GitHub Actions |
| Durable data | Dedicated PostgreSQL + encrypted off-host backups | State, business data, recoverability |
| Evaluation | MLflow + Promptfoo | EVOLUTION learning and regression/security tests |
| Deployment control | GitHub Actions + OCI CLI/gcloud | Planned change, approved deploy, check status and rollback |
| Infrastructure portability | Docker/Compose, environment templates, OpenTofu | Recreate service on a different host/provider |

## Approved control flow

`ChatGPT (review/propose) -> private GitHub repo/PR -> CI safety checks -> protected deployment approval -> GitHub Actions -> provider CLI -> cloud target -> external verification + audit evidence`

Provider control is **not** the same as an interactive SSH shell. On an OCI VM, `oci` can provision and inspect the machine, but deploying the container within it additionally requires an authenticated restricted deployment mechanism (e.g., narrow SSH/SSM-equivalent runner). On Cloud Run, `gcloud run deploy` can directly publish the reviewed container.

## Identity & security rules

- Prefer short-lived identity federation between GitHub Actions and cloud identities: **Google Workload Identity Federation** for GCP; **OCI GitHub token exchange / workload identity federation** only after compatibility and tenant IAM setup are verified. Otherwise require explicit review of any narrowly scoped credential bootstrap. No cloud keys in repository files or logs.
- Separate service principals / namespaces / compartments per environment; least privilege; protected branches and GitHub Environments, with manual approval for every provisioning, deployment, rollback or destructive command.
- Workflows triggered by PRs run lint, static tests and an IaC plan only; PRs may not receive privileged cloud credentials. Use manual `workflow_dispatch`/approval for deploys, with commit SHA and target environment recorded.
- Deny paid shapes, region-switching that incurs fees, unmanaged log retention, surprise egress costs and implicit paid tier upgrades. A budget alert is **not** a hard spend cap. Review chargeable-resource lists before deployment.
- Require authentication and HTTPS for public access. No default/public signup. Restrict external ports and MCP access; do not expose Ollama without strong authentication and network restriction.
- Keep secrets, backups and other business projects fully separate. Enable audit logs, rotation and revocation plan.
- Actions and Activities that can cause duplicate side effects must be idempotent and subject to authorization.

## Portability and migration contract

- Pin reviewed upstream image versions or immutable digests, checking **linux/arm64** compatibility for OCI and Cloud Run's required platform. Maintain IaC/Compose definitions, environment variable contracts, schema migrations and a provider-neutral storage interface.
- Treat cloud storage, PostgreSQL data, object uploads and encryption keys as separate portable state; Git alone does **not** migrate runtime data.
- Export via encrypted and tested `pg_dump` / `pg_restore` (or approved alternative). Store backup artifacts in a distinct secure destination, **never Git**. Restore with consistent secrets and test account login, content integrity and permission policy.
- Record source commit, image digest, schema version, provider/region, CPU/RAM, DB engine version, environment fingerprints (not secret values), rollback point and recovery test results.
- OCI persistent VM can host several services after sizing. GCP Cloud Run fallback may initially host **Open WebUI only**; do not assume it can replace Temporal, Postgres and Ollama in-place within free quota.

## Go/no-go gates

1. Separate private GitHub repo and explicitly selected account.
2. OCI tenancy/region/Always Free availability and quotas verified; separate billing controls. If unavailable, evaluate Google Cloud Run.
3. Identity federation and scoped permissions verified using read-only test before privileged actions.
4. Source + workflow static validation, licence and architecture checks, no secrets or inherited project configuration.
5. User approves cloud creation after costs and risks are displayed.
6. Deploy Open WebUI only; verify HTTPS/auth/signup disabled, startup/memory, persistence, restart, logs and backup/restore.
7. Pilot acceptance before inference/Brain/Temporal/MCP expansion; OpenClaw only after separate approval.

## Explicitly not authorized by this ADR

No cloud provisioning, GitHub repository creation, Git pushes, workflow installation/execution, authentication setup, service/account changes, subscriptions, payment-method changes, deployments, purchases, or other external actions. Those require a later execution instruction and relevant approvals.

## References for future implementation review

- GitHub Actions: https://docs.github.com/en/actions
- Google auth action (OIDC): https://github.com/google-github-actions/auth
- Google Cloud SDK action: https://github.com/google-github-actions/setup-gcloud
- OCI CLI: https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cliconcepts.htm
- OCI GitHub OCI CLI Action: https://github.com/oracle-actions/run-oci-cli-command
- OCI Always Free: https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier.htm
- Cloud Run pricing: https://cloud.google.com/run/pricing
- Open WebUI: https://github.com/open-webui/open-webui
- OpenTofu: https://opentofu.org/

> Provider allowances, licences and federation mechanics should be reverified at deployment time. No live tenancy, quotas, charges or application compatibility was confirmed by this documentation change.
