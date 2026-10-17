# Business House AI Matrix — Approved target architecture

**Status:** Stack approved; Open WebUI-first pilot delivery prepared 2026-10-18. Runtime deployment requires selected host and verified Docker startup.

## Responsibilities and trust boundaries

| Plane | System | Owns | Must not own |
|---|---|---|---|
| Operator UX | Open WebUI | Multi-user chat UI, conversations and access entry point | Primary reasoning, production execution |
| Optional edge | OpenClaw | Operator-facing chat channels, skills and restricted device operations | Central orchestration, cross-tenant trust, bypassing approvals |
| Intelligence | LangGraph | Central Brain, routing, recursive departmental subgraphs, cognitive QA/feedback | System-level work scheduling and authoritative retries |
| Durability | Temporal self-hosted | Task/run lifecycle, worker queues, timer/schedule, fault recovery, durable approvals, workflow audit | Choice of cognitive solution or unrestricted side effects |
| Tool interface | FastMCP | MCP services wrapping approved abilities | Authorization by client hints alone |
| Tool governance | ContextForge | Tool catalog, identity, server-side authorization and logging | Agent planning |
| Inference | Ollama, independently validated model licence | Local model serving | Authorization, business truth |
| Persistence | PostgreSQL | Temporal back end plus separately governed application data/memory | Model intelligence |
| Learning | MLflow + Promptfoo | Outcomes, feedback datasets, experiments, regression/security tests | Automatic unapproved deployment |

**Execution sequence:** Open WebUI receives an operator request → authenticated adapter starts a Temporal workflow → Temporal Activity invokes LangGraph Central Brain → Central Brain delegates to one or more departmental subgraphs → authorized subgraphs call tool services through governed MCP access → results, QA, state and durable workflow status are recorded → EVOLUTION receives verified outcome data → improvement candidates are tested and approved before promotion.

**API adapter is a missing component, not something the starter already includes.** Validate compatibility with the selected Open WebUI OpenAI-compatible connection or approved integration interface. The adapter must provide authentication, streaming where supported, correlation IDs, tenant/role mapping, cancellation and status retrieval; never expose unrestricted Temporal or MCP endpoints directly to users.

## Recursive nine-department system

1. Concept
2. Design
3. Development
4. QA/QC
5. Marketing
6. Sales
7. Accounts
8. Support
9. **EVOLUTION — training, correction and controlled evolution**

Every departmental subgraph has the same structural pattern: **intake → local Brain/plan → execute → department QA → scoped correction/escalation → result and feedback**. The Central Brain routes requests and synthesizes results. Departmental subgraphs may call each other through central orchestration, not through arbitrary ungoverned lateral actions.

The QA/QC department verifies deliverables and standards. Other departments perform local QA on their own work as well. EVOLUTION analyzes validated outcomes across all departments, curates datasets, evaluates prompts/retrieval/tools/models, proposes improvements, documents failure patterns and sends gated candidates for release. It may suggest fine-tuning later, but actual model training requires separate compute and evidence that it improves outcomes.

## Temporal integration boundary

**Initial stable pattern:** A Temporal Workflow owns the end-to-end business process. The LangGraph run is invoked inside a Temporal Activity. Side-effecting operations are separately wrapped as authorized Activities or protected by idempotent, auditable adapters. Temporal retries can repeat Activities: use idempotency keys for payments, emails, publishing and external operations.

**Future evaluation:** Test Temporal's dedicated LangGraph integration against pinned releases in an isolated environment. Do not assume preview APIs are production-ready. Avoid independently replaying both graph checkpoints and Temporal history for the same unit of work unless a tested design makes it necessary.

Worker unavailability is a recoverable condition, not a promise of uninterrupted execution. Define timeouts, heartbeats for long-running activities, resource budgets, retry policies and failure escalation.

## Security and operations

- Run a separate business Matrix identity/permission domain, repositories, configuration, data and backups; never share secrets or automatic master synchronization with other projects.
- Define departmental MCP allowlists **server-side** in ContextForge, not solely in prompt instructions, UI roles or client filtering.
- Treat tool descriptions, files, documents, websites and model outputs as untrusted instructions/data; validate tool parameters and approvals at execution boundaries.
- Keep OpenClaw isolated from customer-facing/multi-tenant infrastructure; require authenticated bridge calls and least-privilege tools.
- Use separate authorization gates for financial, public, destructive, security-related, credential and production actions.
- Maintain version pinning, backups, tested restore, traceability, resource quotas, observability and rollbacks before expansion.

## Rollout-order lock

The first concrete runtime milestone is **Open WebUI only**, installed with the reviewed official upstream Docker image and the project pilot Compose file and available solely on localhost. Connect local AI and the LangGraph/Temporal/MCP components incrementally after UI checks. The **OpenClaw edge is absent from every pilot deployment and may be evaluated only after explicit pilot acceptance**. This is a sequencing decision, not a change in the target architecture.

## Deployment scope

Local-first and hybrid-ready. Target zero mandatory software licence/API subscription fees; hardware, power, connectivity, backup media and optional external channels may incur fees. Verify exact licences for packages, model weights and redistributed assets before use. Open WebUI is the selected primary interface and is free to self-host but **not OSI-open-source** under its current branding-protected licence. No LibreChat pilot or OpenClaw pilot; OpenClaw is a future optional edge only.

## Status

All components in this document beyond the existing LangGraph v0.1 sample are **design selections only**, not working integrated services. For delivery order and acceptance criteria, see [ROLLOUT.md](ROLLOUT.md).
