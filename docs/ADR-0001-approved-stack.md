# ADR-0001: Approved independent Matrix stack (free/self-hosted first)

- **Date:** 2026-10-18
- **Status:** Accepted architecture, documentation-only; not implemented
- **Context:** A standalone, recursive Business House AI Matrix with one Central Brain and nine departmental Brains needs a multi-user interface, durable execution, governed tools and continuous improvement without mandatory paid orchestration/model subscriptions.

## Decision

1. **Open WebUI** is the primary browser-based conversational interface for human operators, superseding the prior LibreChat choice. No LibreChat deployment or fallback in the pilot.
2. **OpenClaw** is optional and later-stage for multichannel messaging, skills and tightly constrained device operations. It **does not replace** Open WebUI, LangGraph or Temporal.
3. **LangGraph** is the single Central Brain/agent logic orchestrator with **nine recursive department subgraphs**: Concept, Design, Development, QA/QC, Marketing, Sales, Accounts, Support and **EVOLUTION**.
4. **Temporal (self-hosted)** owns durable execution, scheduling, workflow histories, approval waits, activity retries and distributed workers. Start with LangGraph invoked inside a Temporal Activity; verify advanced integrations separately.
5. **FastMCP + IBM ContextForge** supply MCP service development and centralized, server-enforced tool governance, introduced progressively.
6. **Ollama**, an independently licensed local model, **PostgreSQL**, **MLflow**, **Promptfoo**, Git and Docker Compose form the cost-conscious base.
7. **EVOLUTION** owns validated training-data capture, corrections, measured evaluation and controlled improvement promotion; no unapproved self-modifying production system.
8. Project resources, credentials, repositories and docs must remain independent of **Moksha Master**.

## ADR-0002 implementation sequencing (revised 2026-10-18)

**Open WebUI-first pilot is now the approved deployment order.** Start with an isolated localhost-only Open WebUI UI based on its maintained upstream Docker image and a minimal pilot Compose file, then connect self-hosted inference, LangGraph Central Brain, Temporal and a narrowly scoped read-only MCP tool in successive gated increments. The full nine-department Matrix follows only after the single-department pilot is validated.

**OpenClaw is explicitly deferred and excluded** from the pilot: no OpenClaw installation, process, image, container, credentials, secrets, networking, channel or dependencies. Evaluate it only after the Open WebUI / LangGraph / Temporal pilot has been deployed, measured and explicitly accepted. LibreChat is out of scope.

This is an implementation-order amendment; the underlying target stack remains as previously approved. See `ROLLOUT.md` and `../pilot/README.md`.

## Reasons

- Minimizes duplicate agent frameworks: LangGraph thinks, Temporal reliably executes, MCP governs actions, Open WebUI is the interface.
- No mandatory paid interface or model subscription; Open WebUI is free to self-host and its source can be inspected, subject to its specific licence.
- Allows OpenClaw to be added only when chat-channel/device needs are concrete, with fewer privileges than the Brain.
- Enables measured reliability and safe, auditable EVOLUTION rather than opaque autonomous self-editing.

## Licence exception and trade-offs

- Open WebUI v0.6.6+ is **source-available, not OSI-open-source**, because of its branding clause. We accept this for the selected free self-hosted pilot, retain official branding, and must re-evaluate legal needs before distribution or wider deployment. https://docs.openwebui.com/license/

- More upfront integration work: Open WebUI needs a compatible authenticated Brain API adapter; Temporal and LangGraph need explicit durability boundaries.
- Local inference requires adequate hardware and careful licensing checks for each model.
- Self-hosting imposes operational and security maintenance costs despite free software licences.
- OpenClaw increases attack surface and operational complexity if added. Treat it as opt-in.

## Consequences

This decision **updates the documentation only**. Existing sample files, tests and package dependencies remain the original v0.1 implementation. Execution phases need separate authorization.

See: [ARCHITECTURE.md](ARCHITECTURE.md) and [ROLLOUT.md](ROLLOUT.md).
