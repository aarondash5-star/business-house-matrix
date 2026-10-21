# Business House AI Matrix

Independent, recursive nine-department AI operating-system project. **Not connected to Moksha Master.**

**GitHub home:** [aarondash5-star/business-house-matrix](https://github.com/aarondash5-star/business-house-matrix) (**public**, as approved on 2026-10-18).

## Approved architecture

- **Open WebUI** — first pilot interface (not deployed).
- **LangGraph** — central Brain and nine recursive departmental Brains (starter is simulation-only).
- **Temporal** — durable task execution and recovery (not deployed).
- **FastMCP + ContextForge** — tool interface and centralized access control (not deployed).
- **Ollama, PostgreSQL, MLflow + Promptfoo** — planned inference, persistence and EVOLUTION evaluation.
- **OpenClaw** — deferred until the pilot is accepted; **LibreChat is not selected**.

Nine departments: Concept, Design, Development, QA/QC, Marketing, Sales, Accounts, Support, **EVOLUTION** (train, correct, evolve).

## Cloud deployment decision

GitHub Actions runs validation and, after separate cloud identity/configuration approval, controlled provider CLIs. **Oracle Always Free is preferred; Google Cloud Run is fallback.** No paid tier or cloud provisioning is authorized merely by these documents. The Render `render.yaml` is an **obsolete historical prototype**; do not deploy it.

## Start here

- [Current status](docs/STATUS.md)
- [SearXNG research deployment and network handoff](docs/RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md)
- [**Marketing Brain — verified live checkpoint (2026-10-21)**](docs/MARKETING-CURRENT-STATE-2026-10-21.md)
- [Marketing Phase 1 history](docs/MAC-MARKETING-PHASE1.md)
- [Marketing modular provider router](docs/MAC-MARKETING-API-ROUTER.md)
- [Architecture decision ADR-0003](docs/ADR-0003-github-cloud-control.md)
- [Public-repository exception and CI policy ADR-0004](docs/ADR-0004-public-github-and-safety-ci.md)
- [Cloud bootstrap prerequisites](docs/CLOUD-BOOTSTRAP.md)
- [Free/cloud rollout plan](docs/ROLLOUT-github-cloud.md)
- [Local UI-only Compose pilot](pilot/README.md)

**Safety:** Do not commit credentials, private data, user conversations, database snapshots, backups, uploads or encryption keys. The CI scan is not a substitute for thorough security review. Existing business projects and cloud accounts are not shared with this Matrix.
