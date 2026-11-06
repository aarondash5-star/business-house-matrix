# MAID — unified multimodal AI engine: Phase 1 architecture and master plan

**Date:** 2026-11-06  
**Status:** DESIGN / INVENTORY ONLY — NOT DEPLOYED  
**Document classification:** Public architecture summary. No account identifiers, credentials, private repository details, operational logs, customer information, or copied context data.  
**Scope:** One owner-facing, license-compliant, multimodal control interface; multiple cooperating AI agents; persistent, access-controlled context; independently authorized connector access. Strict no-spend-by-default policy.

> This is a planning record. It does **not** authorize installation, connecting accounts, widening privileges, creating cloud resources, ingestion of personal/business content, starting agents, or deploying to production.

## 1. Objective and constraints

The desired outcome is a **single governed operator view and searchable index**, not a single unrestricted database or superuser token. The system must allow task-context retrieval, model and agent cooperation, mobile/desktop access, multimodal content, durable work receipts, and operation with separately unavailable workers.

Standing principles:

1. **Open-source first.** Record an OSI-acceptable software license, dependency origin, pin and security review before adoption. Distinguish OSS inference frameworks from open-weight models and proprietary hosted APIs.
2. **Free and zero-spend verified.** Treat unknown quota or pricing as **ineligible**. No paid automatic fallback or incidental subscription.
3. **Keep projects and accounts isolated.** Every source has a namespace, visibility class, owner, per-agent read policy, and action-specific credentials.
4. **Provenance and truth.** Live runtime status and terminal receipts outrank old handovers, model narratives and stale summaries. Nothing is “done” merely because it appears in Git or a queue.
5. **Owner approval for material changes.** No production write, account grant, privileged host access, external publication, destructive action, or paid call without authorized scope.
6. **Reuse before replacement.** Prefer the existing Matrix dispatcher, LangGraph graphs, task envelope, QA patterns and provider manager specifications where a current audit supports reuse.

## 2. Reusable architecture verified from existing Matrix source

| Asset | What exists in source | What is not proven |
| --- | --- | --- |
| `matrix/graph.py` | LangGraph central graph and nine recursive departmental subgraphs, simulated QA, approval interrupt, EVOLUTION proposals | Live multi-agent tools and models, durable cross-project production execution |
| `brain/mvp-controller/controller.py` | SQLite queue, idempotency, bounded allowlisted dispatch and receipt semantics | Federated cross-account orchestration or full multimodal tool autonomy |
| `brain/governance/task-envelope-v1.schema.json` | Versioned roles, scopes, approval and acknowledgement fields | That all external agents have consumed or enforce the policy |
| `cloud/model-manager` | Fail-closed Workers AI gateway scaffold and quality/free-first specifications | A populated eligible registry or successful live model inference |
| Research and QA components | Historical independent research/QA pilot design and recorded bounded tests | Current cross-machine routing, model credentials or runtime health |
| GitHub CI / Cloudflare estate | Existing source/deployment ecosystems, subject to separate business boundaries | An isolated, already-approved MAID runtime or centralized memory service |

**Architecture decision:** Extend the existing **Business House Matrix** as a governance/orchestration reference. Do not silently promote its demo graph or older prototype into production. An independently secured MAID runtime and its data store should be isolated from other projects.

## 3. Proposed target layering

| Layer | Direction (not implemented) |
| --- | --- |
| Operator UI | Accessible mobile/desktop OSI-licensed PWA with voice, file and image entry; assess MIT-licensed NextChat-derived UI or an independently maintained alternative |
| Orchestrator | LangGraph coordinator plus department/specialist subgraphs, task contracts and owner-approval interrupts |
| Memory | Dedicated PostgreSQL with pgvector; source IDs, project namespaces, ACL filtering and durable task event log |
| Retrieval | Scoped ingestion adapters, provenance, embedding worker and retrieval that checks source permissions **before** exposing content |
| Inference router | Small audited provider adapters + optional local Ollama; enforce verified model capability, licensing, data-handling and hard free-tier eligibility |
| Connections | Per-provider OAuth/MCP adapters; repo/account-scoped grants; revocation and credential references stored server-side |
| Edge entry | Authenticated Cloudflare Workers for gateway/webhook/short endpoints; heavy durable Python workloads require a separately selected host |
| Media | Isolated encrypted object store; R2 only after user approval and current account enablement, or an approved self-hosted equivalent |
| Durability | Reuse existing bounded queues first; assess Temporal or another durable engine only if retries/checkpoints outgrow existing controller |
| Evaluation | Independent QA/QC receipts, Promptfoo/other verified OSS checks, regression suites, failure injection and rollback evidence |

**Dependency note:** New Open WebUI releases (v0.6.6+) include a branding restriction and its own documentation says that the license is not OSI-approved; do not choose these releases as the strict-OSI default. See https://docs.openwebui.com/license/. Treat LiteLLM as **on hold for dependency security review** following the 2026 compromised releases; never install it unreviewed in a credential-rich shared environment. See https://www.microsoft.com/en-us/security/blog/2026/10/23/inside-the-litellm-1-107-0-supply-chain-compromise-credential-theft-through-python-startup-hooks/.

## 4. Shared-context design — security and correctness contract

The global interface references many **logically separate** stores and source systems; it is not authority to aggregate, copy or disclose every source.

Minimal indexed record fields:

- `source_system`, `source_id`, `account_id` (opaque), `project_namespace`, `uri`, `revision` and `observed_at`.
- `data_classification`, `consent_ref`, `read_acl`, `retention_policy`, `deleted_at` and `source_freshness`.
- `index_version`, `chunk_hash`, `embedding_model_revision`, `summary_version` and `citation_locator`.
- `task_id`, `agent_role`, `input_provenance`, `approval_ref`, `execution_receipt`, `qa_receipt`, `recovery_checkpoint`.

Acceptance invariants:

1. Retrieval must apply the current role/project/document ACL and never rely on an embedding match alone.
2. When a source changes or is deleted, the context index must invalidate or purge derived material appropriately.
3. The system labels stale/unverified claims and preserves a chain to the authoritative source.
4. Models cannot turn retrieved instructions into tool authority; tool grants are enforced outside the model.
5. No raw secrets, session credentials, customer identifiers or entire conversation exports enter embeddings by default.
6. Audit events are append-only where practical and independently checkable; action idempotency prevents duplicate real-world effects.
7. Per-agent memory and approvals are scoped; shared summaries are permission-aware rather than globally readable.

## 5. Five-phase implementation roadmap

### Phase 1 — inventory and architecture (**current, documentation only**)
- Reconcile currently reachable integrations and source code with older proposals.
- Identify reusable capabilities, uncovered modalities, licensing constraints and security boundaries.
- Document target architecture, dependency decisions, unknowns, owner decisions, and measurable exit gates.
- **Exit:** Versioned audit/roadmap, no claims of activated connectors, deployed runtime or persistent memory.

### Phase 2 — dedicated context and memory (**not started**)
- Approve exactly which sources and categories may be indexed and which workers may access them.
- Select an isolated durable store and hosting that meet zero-spend and backup requirements.
- Implement and verify authorization-aware ingestion, provenance, update/delete propagation, semantic retrieval, encryption and recoverable backups **on synthetic fixtures first**.
- **Exit:** Negative authorization, source-deletion, stale-source, restore and cross-agent retrieval tests pass.

### Phase 3 — multi-agent delegation and orchestration (**not started**)
- Extend existing LangGraph and governance protocol to real worker capabilities with dedicated task identity and receipts.
- Register eligible models and bounded tool adapters; implement durable checkpoints, retries, independent review, owner gate and failover.
- **Exit:** One synthetic, parallel, multi-agent task verified end-to-end, including an unavailable-worker scenario.

### Phase 4 — multimodal processing and controlled accounts (**not started**)
- Implement separate approved pipelines for text, images, audio, video and documents, respecting rights and modality support.
- Add connectors **one account/project at a time** with user-authorized least privilege and a revocation dashboard.
- **Exit:** Auth-negative tests, media QA, source citations, revocation and no cross-project leakage.

### Phase 5 — private release and certification (**not started**)
- Select a genuinely free-capacity-verified host, deploy an isolated and authenticated mobile/desktop client and durable workers.
- Verify restore, worker restart, offline recovery, model fail-closed, billing/no-spend, audits and regression coverage.
- **Exit:** Owner-accepted private beta supported by runtime receipts, not merely successful CI.

## 6. Phase 1 outstanding evidence gaps

- The existing cloud/model-manager is **configuration only** and inference is explicitly disabled.
- There is no **verified** unified cross-project durable context vault; absence of verification is not proof none exists elsewhere.
- Present model permissions, quotas, data-handling terms, free eligibility and multimodal capability are **not certified** from old receipts.
- Existing host/worker connection status does not alone establish that each application-specific agent is ready.
- The choice of isolated host, memory namespace and connector approval list remains open.
- Storage options, including R2, require a separate enablement/readiness review; no automatic bucket creation.
- A security review is needed before any Python AI gateway gains access to multiple cloud/developer credentials.

## 7. Decisions required before Phase 2

1. Approve the MAID runtime and **private** data-store placement and its free-capacity budget.
2. Approve a scope matrix for every connected account/project, starting read-only.
3. Choose the OSI-compliant PWA and decide if optional proprietary inference providers may receive restricted data.
4. Approve a secrets and identity architecture (revocable account scoped tokens, no global API key).
5. Approve a synthetic-only test plan and written go/no-go criteria before real context ingestion.

## 8. Separation of work and proof

This document is **not an implementation request**. It authorizes no deployment, GitHub Actions execution, provider inference calls, account permissions, cross-project data movement, cloud resource creation or machine changes. A docs-only review PR is a planning artifact, not a live rollout.

### Public references
- Existing architecture and governance: [Business House Matrix README](../../README.md)
- Current declared status: [Matrix rollout status](../STATUS.md)
- Model-manager source and fail-closed design: [cloud/model-manager](../../cloud/model-manager/)
- Existing governance charter: [Super Brain charter](../governance/SUPER_BRAIN_OPERATING_CHARTER.md)
- Cloudflare Workers limits: https://developers.cloudflare.com/workers/platform/limits/
- Open WebUI licensing: https://docs.openwebui.com/license/
