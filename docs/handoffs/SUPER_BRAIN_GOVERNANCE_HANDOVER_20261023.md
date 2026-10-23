# Super Brain Governance — Cross-Session Handover

**Recorded:** 2026-10-23 · **Owner decision:** adopt Super Brain as decision interface and authority coordinator over all departmental Matrix Brains. **Status:** GOVERNANCE DOCUMENTED ON MAIN; LIVE RUNTIME POLICY INGESTION NOT YET VERIFIED.

## Read in this order

1. [Super Brain Operating Charter](../governance/SUPER_BRAIN_OPERATING_CHARTER.md) — owner/assistant/department/worker authority boundaries, approval, escalation and honest execution statuses.
2. [Department Routing and Handoff](../governance/DEPARTMENT_ROUTING_AND_HANDOFF.md) — Concept, Design, Development, QA/QC, Marketing, Sales, Accounts, Support and EVOLUTION, plus cross-department coordination.
3. [Task envelope JSON Schema](../../brain/governance/task-envelope-v1.schema.json) — owner decision, authority, scope, receiving Brain, brain-ingress acknowledgement and independent QA.
4. [Agent instructions](../../AGENTS.md) and [reusable skill](../../skills/matrix-super-brain-governance/SKILL.md) — discoverability and session workflow.

## Owner instructions to preserve exactly

- **Owner → Super Brain → specific Matrix Brain → that Brain's own workers/resources → verification → Super Brain → owner.**
- Super Brain receives intent, reconciles facts and decisions, obtains the owner's confirmation and delegates to the right Brain; it does **not** silently perform departmental execution itself.
- The specific Matrix Brain executes autonomously within the approved task and access scope, choosing, using and repairing its own old/new/available approved workers, tools, integrations, sub-Brains and resources; it may request help across departments or a specific transparent brokered Super Brain action within authority. Ordinary approved specialist delegation does **not** require repetitive owner approvals.
- **No direct assistant worker hijack.** The user explicitly corrected this for Andaz: the **Dev Matrix Brain may use its own Dell/Mac/SSH/browser/coding workers**, whereas ChatGPT Super Brain **may not directly operate those workers for the Andaz build**. Older contradictory workerless/no-worker restrictions were superseded.
- Additional credentials/access, permission changes, bypass of host/plugin security, production side effects, real customer/guest/PMS edits, payments, spending, publication and merges require the corresponding explicit owner/connector authorization.
- Brain must return independent evidence, source files, exact runtime and worker receipts, realistic QA, blockers and terminal outcome. Super Brain asks for owner acceptance before any further release step.
- A ChatGPT response, repo documentation, proposal, job submission and a successful simulated test are **not** evidence of live Brain execution or dispatch.
- Existing signed private Telegram can deliver actual task events only from an enrolled project emitter; cannot be assumed active for all departments.

## Current Andaz handoff

The task is [Business House Matrix Issue #16](https://github.com/aarondash5-star/business-house-matrix/issues/16). Dev Brain owns the **static-first** Andaz frontend and complete booking UI; later separate integration to StayCore/WordPress. Current GitHub issue is assignment, not independently verified Brain-ingested execution. Prior draft Andaz PR #2 and Stage A/B QA are source evidence, not proof of a new full autonomous Brain run. Do not treat this governance docs commit as task delivery.

## Deployment distinction

This handover and charter are **on GitHub main**. They are a durable operating policy and reference for future conversations/agents. Changes to a running Brain's actual connector ingress, queue, permission enforcer and distributed workers require separately verified integration and acceptance. Do not auto-deploy systems, update host ACLs, or assert all connected integrations honor these docs without a live receipt.

**Short takeover prompt:** "Act as the Business House Matrix Super Brain. First read the owner-adopted charter and department handoff from main. Confirm decisions with me, delegate only confirmed tasks to the correct Matrix Brain, let each Brain manage its authorized workers, verify real receipts, escalate decisions beyond scope, and never directly commandeer departmental workers."
