# Business House AI Matrix

Independent, recursive nine-department AI operating-system project. **Not connected to Moksha Master.**

**GitHub home:** [aarondash5-star/business-house-matrix](https://github.com/aarondash5-star/business-house-matrix) (**public**, as approved on 2026-10-18).

## Owner-approved operating hierarchy (23 October 2026)

**Owner → Super Brain (ChatGPT decision interface) → appropriate departmental Matrix Brain → its authorized workers/resources → independent QA → Super Brain reporting → owner acceptance.**

The Super Brain confirms material decisions and scope with the owner, delegates to the appropriate Brain and reports verified results. Department Brains own execution and can autonomously use their already-approved workers within that scope; the assistant does not directly commandeer departmental workers. New permissions, production effects and other material changes remain separately gated. **A GitHub task is not proof of Brain execution.**

- [**Canonical Super Brain operating charter**](docs/governance/SUPER_BRAIN_OPERATING_CHARTER.md)
- [Nine-department routing, delegation and handover](docs/governance/DEPARTMENT_ROUTING_AND_HANDOFF.md)
- [Reusable Super Brain governance skill](skills/matrix-super-brain-governance/SKILL.md)
- [Machine-readable approved task envelope](brain/governance/task-envelope-v1.schema.json)

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
- [**Reusable research integration contract**](docs/REUSABLE-RESEARCH-CONTRACT.md)
- [**Cross-project SearXNG skill**](skills/selfhosted-searxng-research/SKILL.md)
- [**Marketing Brain — verified live checkpoint (2026-10-21)**](docs/MARKETING-CURRENT-STATE-2026-10-21.md)
- [Marketing Phase 1 history](docs/MAC-MARKETING-PHASE1.md)
- [Marketing modular provider router](docs/MAC-MARKETING-API-ROUTER.md)
- [Architecture decision ADR-0003](docs/ADR-0003-github-cloud-control.md)
- [Public-repository exception and CI policy ADR-0004](docs/ADR-0004-public-github-and-safety-ci.md)
- [Cloud bootstrap prerequisites](docs/CLOUD-BOOTSTRAP.md)
- [Free/cloud rollout plan](docs/ROLLOUT-github-cloud.md)
- [Local UI-only Compose pilot](pilot/README.md)

**Safety:** Do not commit credentials, private data, user conversations, database snapshots, backups, uploads or encryption keys. The CI scan is not a substitute for thorough security review. Existing business projects and cloud accounts are not shared with this Matrix.


## Marketing AI — active next-chat handover

**Start here for the pending Marketing MVP work:** [Marketing AI next-chat execution handover (21 Oct 2026)](docs/handoffs/MARKETING_AI_HANDOVER_2026-10-21.md). It contains the four release gates, safe operator commands, last verified evidence, and the copy/paste takeover prompt. **Do not declare Marketing autonomy complete** until cross-host research, safe Mac rendering, the unattended Moksha pilot, and resilience certification pass.

## Autonomous MVP pilot checkpoint — 2026-10-21
- [Live autonomous MVP implementation, QA, and blockers](docs/AUTONOMOUS-MVP-IMPLEMENTATION-2026-10-21.md)
- [Central durable dispatcher](brain/mvp-controller/controller.py) · [isolated QA](brain/mvp-controller/sandbox.py) · [bounded correction](brain/mvp-controller/repair.py)
- Dell research/proposal/isolated unit-test and one unattended known-error EVOLUTION correction are verified. Mac public Trends and Groq creative planning are verified. Cross-machine routing, finished reels, safe OSI-approved UI and full department autonomy are still incomplete.

## SuperGPT project (Android-first client)

**Canonical SuperGPT specification:** [project index on super-gpt/dev](https://github.com/aarondash5-star/business-house-matrix/blob/super-gpt/dev/docs/supergpt/README.md) · [architecture and execution plan](https://github.com/aarondash5-star/business-house-matrix/blob/super-gpt/dev/docs/supergpt/PROJECT_PLAN.md) · [release policy](https://github.com/aarondash5-star/business-house-matrix/blob/super-gpt/dev/docs/supergpt/RELEASE_POLICY.md).

Environment branches: [dev](https://github.com/aarondash5-star/business-house-matrix/tree/super-gpt/dev) → [test](https://github.com/aarondash5-star/business-house-matrix/tree/super-gpt/test) → [production](https://github.com/aarondash5-star/business-house-matrix/tree/super-gpt/production). GitHub Actions compilation of an upstream-derived standalone Android prototype is **not** certification of the connected SuperGPT product. Runtime testing, Matrix integration, independent QA and production acceptance remain separately gated. Branch rulesets require separate GitHub-admin verification.
