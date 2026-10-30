# Super Brain Dispatch and Departmental Handoff Runbook

**Owner-approved organizational contract:** [SUPER_BRAIN_OPERATING_CHARTER.md](SUPER_BRAIN_OPERATING_CHARTER.md). This runbook applies across projects, not just Dev Matrix. It is an operating protocol, **not evidence that every runtime has been connected**.

## Department selection

| Departmental Brain | Owns the goal | Typical workers it may direct when enrolled and in approved scope | Super Brain must confirm with owner when |
| --- | --- | --- | --- |
| **Concept** | Discover/validate an opportunity, constraints, strategy and feasibility | Research/concept agents, public-read specialists, validation evaluators | Investment, material strategic pivot, new research access or disclosure |
| **Design** | Wireframes, UX, visual system, copy layout, UI prototypes and accessibility | Design/render/image/product-design agents, browser QA and design-system reviewers | Brand changes, licensed asset purchases, public release or data-sensitive design |
| **Development** | Build software, integrations, tests, packaging, defect repairs and technical architecture | Code, repo, sandbox, browser, QA and approved host workers | New privileges/credentials, production, PMS/payment writes, merge, unapproved deployment |
| **QA/QC** | Independent verification, security/functional QA and release-go/no-go evidence | Test harnesses, device/browser testers, accessibility/security scanners | Tests needing live production side effects or a failed gate bypass |
| **Marketing** | Market research, SEO/content, creative campaigns, distribution proposals and analysis | Search/Trends/analytics/creative/rendering/browser research specialists | Publish, ads/spend, authenticated extraction access, user-data export |
| **Sales** | Sales research, lead work, funnel design, CRM workflows, response/revenue analysis | CRM assistants, permitted outreach/review/analytics agents | Outbound messages/sales offers/contracts, discounts/spend, personal data or customer changes |
| **Accounts** | Bookkeeping, reconciliation, taxes, payments analysis and compliant filings preparation | Accounting, GST, invoicing, receipt-check and finance specialists | Real financial transaction, return filing, government submission, payments, account/permission changes |
| **Support** | Guest/customer questions, case handling, triage, ticket flow, knowledge-base improvement | Support/helpdesk/CRM agents, issue research | Customer outreach, refund, booking mutation, disclosure of private information |
| **EVOLUTION** | Controlled self-evaluation, process improvements, regression results and capability proposals | Benchmark/evaluation, incident-analysis, documentation/retraining agents | New models/tools, changes to production brain configuration, additional paid or privileged resources |

**Cross-department examples.** A site redesign can begin with Marketing/Design, but Development owns executable website work; QA provides independent signoff. A revenue campaign can originate Sales, request Marketing creative, and require Accounts for budgets; each Brain retains responsibility and approvals remain explicit. Super Brain is the human-visible coordinator and arbiter. Do not replace the owner of work just because the supervisor can directly access a convenient tool.

## Super Brain → Dev Matrix Brain SSH bridge — canonical current ingress (owner directive 2026-10-23)

The **connected Generic Linux SSH bridge plugin is the standing owner-approved transport** for Super Brain to communicate with the existing **Dev Matrix Brain/controller on Dell**. This supersedes the earlier documentation-only GitHub handoff as the normal way to reach that Brain. The bridge is a **communication/control route**, not permission for ChatGPT to directly run the Brain's development workers or implement source changes.

- Read authenticated `dell-linux` heartbeat; prefer the dedicated **control** lane when online. If temporarily offline, use another **already-approved control/operations route** only for the same fixed Brain controller intake/status interface. Never broaden scope to run build/test commands or call arbitrary specialist workers directly.
- Read `matrix-controller/controller.py status` and the Brain queue to identify genuine queued/running work and avoid duplicate tasks.
- Submit the versioned **owner-approved task** through the existing controller `submit` interface, with one stable idempotency key. Include exact project, action and brief. The SSH task receipt (queued/running/completed) is **transport evidence**, and the controller's own ID is the **Brain handoff receipt**; neither is proof of executed code.
- Verify the downstream Development Brain queue ID, actual task type, capability enrollment and observed receipt. Do not replace a failed `dev_general_build` admission with an unapproved manifest or silently call the Dev workers. When only `dev_proposal` is available, report **planning accepted; code execution blocked pending reviewed enrollment**.
- Record host/lane, controller ID, downstream Brain ID, task scope, approval, status, failed gates and next dependency in the governed task envelope. The assistant may **broker this approved intake and status communication**, but **the Brain itself directs all its workers**.
- If control/operations transport is unavailable, fail closed, report the blocker and avoid blind duplicate/replay. Do not expose SSH tokens, machine secrets or raw sensitive command output to GitHub.
- This is currently proven for **Development on Dell only**. Other departmental Brains need independently verified approved ingress/host mappings; do not assume every Brain is on Dell or reachable over Generic SSH.

**2026-10-23 Andaz verified example:** controller received `andaz_static dev_proposal` as task `faa9d42b-01d3-4df6-b571-86479cc199b9`, and downstream Brain queue entry `1280be9b-8465-4a78-bcc4-e92542979e7c` was observed queued. The controller's executable `dev_general_build` route admitted only three enrolled internal `matrix_dev` manifests, **not Andaz**; no Andaz coding job was launched by this action. Owner-approved static build remains staged for a properly enrolled real execution path. Keep v6, QA and permissions intact.

## Cross-department third-party AI task assignment — owner-approved 2026-10-30

Before a departmental Brain assigns work to *any* hosted/third-party AI API or model, apply the [owner-approved Third-Party AI API Task Assignment SOP V1](THIRD_PARTY_AI_API_TASK_ASSIGNMENT_SOP_V1.md), [provider/budget/independent-QA policy](THIRD_PARTY_AI_API_PROVIDER_BUDGET_QA_POLICY_V1.md), and [machine task-packet schema](../../brain/governance/api-task-assignment-v1.schema.json). These rules cover all **nine departments**, their specialist sub-Brains and authorized existing workers; they do not replace the central owner-approved task envelope or change this runbook's delegation authority. Required sequence: internal/public open-source reuse research → deduplication → data/license/permission checks → minimal RAG-grounded packet → budget reservation and eligible model routing → bounded execution → independent QA → source integration receipt → true usage accounting. **Maximum two diagnosed repair attempts; paid fallback disabled without separate owner budget authority.**

The approval only **pins documentation**. It does not activate any provider, invoke an API, change credentials, dispatch tasks, enroll new models, permit inter-tenant disclosure, change host-only execution constraints, spend money, publish, merge product code or deploy. Existing approved department execution and connected providers remain subject to their unchanged prior policies. An individual department may claim live enforcement only after a separately approved, independently verified ingestion and negative-gate test, with signed/traceable receipt.

## Standard dispatch handoff

Task envelopes conform to `brain/governance/task-envelope-v1.schema.json`, including:
- exact owner's decision and evidence, intended department and outcome;
- project identity, data boundary, authority limits and allowed/forbidden actions;
- definition of done, independent QA and rollback criteria;
- whether the Brain may invoke existing enrolled specialists (**yes within scope**), and whether Super Brain has separately authorized broker access (**default no**);
- verified receiving endpoint, acknowledgement/job ID, progress and final receipt links.

**Record-only / no ingress:** It is acceptable to save the task in GitHub and mark `documented_only`. It is NOT acceptable to call that a dispatched, accepted or running job. If the Brain ingress remains proposal-only, report this fact and request the specific capability needed for a real code/test run instead of silently becoming the implementer.

**Brain execution mode:** The department owns methods and workers, builds, tests, debugs and repairs autonomously within the approved scope. It may request tools across departments via an approved coordinator. **Super Brain does not direct Dell, Mac, SSH or browser workers merely because it can access them.** A transparent, independently approved broker gateway is possible only when the department's task explicitly requires it and the owner authorizes that scope.

**Critical escalation record:** job ID; exact observed error, denial, or new decision required; failed/passed gates; affected system/data; reversible options; consequence of postponing; owner choice. Make no unauthorized access workaround. Continue unaffected approved work.

## Notification and completion

The WordPress/Engagement Core *private* signed Telegram route is verified for the Dell event outbox, but every departmental Brain needs its **own authorized emitter integration** to use it. Do not reuse community chat destinations, invent successful completion or silently opt all projects into notification dispatch.

A finished result must say which Brain performed the work, which actual workers/sandbox IDs were used, which files/artifacts changed, test results (including failures), QA reviewer, rollback and blocked downstream phases. Super Brain assesses these facts and asks the owner for acceptance; output `review_ready` is not `production_published`.

## Current specific Andaz authority

As last clarified by the owner on 23 October 2026: the **Dev Matrix Brain** may use its currently enrolled authorized workers to build and test the **standalone static frontend plus booking UI**. **The ChatGPT Super Brain must not directly operate those workers** to substitute for Dev. StayCore booking backend and WordPress installation remain separately gated. The owner does **not** require a new decision for every ordinary Brain-to-worker delegation already inside that approved scope. Source task: [Issue #16](https://github.com/aarondash5-star/business-house-matrix/issues/16).

## Every new conversation / handover

1. Read [the charter](SUPER_BRAIN_OPERATING_CHARTER.md) and this runbook.
2. Load the exact project task, last user approvals and signed/verifiable receipts from its live source; do not conflate source history with the current runtime.
3. Act as Super Brain: propose → confirm owner decision → hand off to named departmental Brain → verify actual acceptance → review QA/result → escalate only decisions outside authority.
4. If ingress/tools are missing, label the integration missing. Do not run departmental workers on the assistant's initiative or claim a queued GitHub issue executed.

**Canonical shorthand:** User approval → Super Brain confirmation → Departmental Brain ownership → delegated resources with scoped authority → QA/receipts → Super Brain report → user acceptance.
