# Business House AI Matrix — GitHub → OCI / Google Cloud rollout

**Status:** APPROVED PLAN ONLY; NO EXECUTION. Reference decision: [ADR-0003](ADR-0003-github-cloud-control.md).

| Gate | Scope | Evidence before proceeding |
|---|---|---|
| 0 — Repository | Select one GitHub identity. Create a **new private independent** Matrix repo only after approval. Import reviewed project source; put provider-specific code under `infra/oracle/` and `infra/google/`. | Reviewable repo contents, no secrets, isolation check |
| 1 — Safety CI | Add lint/secret scanning, tests, container checks, OpenTofu `fmt`/`validate`/`plan`, immutable image references and protected environments. | Safe PR checks without cloud-write access |
| 2 — Cloud authentication | Verify account/tenancy, Oracle capacity, budget, Google billing. Configure only per-environment scoped, short-lived CI identities. | Read-only CLI checks, audit trail, cost review |
| 3 — Oracle pilot | Try **Always Free** OCI Arm VM with private durable volumes. Secure HTTPS; deploy only Open WebUI using reviewed container. | Real URL, healthy startup, auth/signup controls, persistence, logs, cost and backups |
| 4 — Fallback / migration rehearsal | If OCI capacity or compatibility blocks the pilot, deploy Open WebUI on **Cloud Run** within the verified free allowance with external persistent PostgreSQL/storage. Keep no default paid dual hosting. | Same app data/auth checks, measured quota/latency, tested export/restore |
| 5 — Intelligence | Only after UI pilot passes, connect inference then LangGraph Central Brain and one departmental subgraph. | Approved AI responses and delegation trace |
| 6 — Reliability + capabilities | Add Temporal, first read-only FastMCP capability; introduce ContextForge when operationally justified. | Worker outage recovery, activity idempotency, access-denied audit |
| 7 — Learning and expansion | QA/QC and EVOLUTION loop, then expand to all nine departments. | Evaluation benchmarks, human-reviewed changes, rollback test |
| 8 — Deferred option | Consider OpenClaw only **after pilot acceptance and separate approval**. | Independent security/need review |

## Conceptual Git structure — NOT created

```text
business-house-matrix/
├── .github/workflows/
│   ├── validate.yml
│   ├── deploy-oracle.yml
│   ├── deploy-google.yml
│   └── rollback.yml
├── apps/open-webui/
├── brain/langgraph/
├── infra/oracle/
├── infra/google/
├── config/
├── scripts/
└── docs/
```

### Required safeguards

- No direct cloud CLI modifications on unreviewed PRs; no credentials to untrusted branches.
- Manual deploy approval, separate target environments, pinned images, all actions logged.
- Encrypted database/volume backups outside Git, tested recovery prior to real data.
- Always Free is a quota and tenancy entitlement, **not** a promise of available VM capacity or zero bill. Chargeable extras and egress must be explicitly blocked or reviewed.
- No mixing business accounts, production data, secrets or shared state with existing projects.
- No enabled OpenClaw or LibreChat containers in the pilot.

## Current status (2026-10-18)

- Agreed: GitHub as portable deployment control; Oracle preferred; Google fallback; Open WebUI first.
- Not yet done: remote repository, external CLI credentials, IAM, cloud account verification, IaC execution, image compatibility and live deployment verification.
- Previously prepared Render Free template is historical/superseded; **do not deploy it as the approved target**.
