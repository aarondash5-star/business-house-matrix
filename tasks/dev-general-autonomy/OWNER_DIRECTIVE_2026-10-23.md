# Dev Matrix universal execution — remove fixed manifests, role caps and sandbox-only task restrictions

**Owner directive:** 23 October 2026: "Remove the manifest and rolled and sandbox limitations from the Matrix Dev setup."

**Responsible executor:** Dev Matrix Brain through its existing authenticated Dell controller/SSH bridge; Dev Brain controls and uses its workers. The ChatGPT Super Brain is the decision/dispatch/QA intermediary, **not the code editor or direct worker operator**.

**Priority:** P0 (Dev Matrix capability prerequisite for Andaz and other multi-project work).  
**State:** Owner-approved capability request. **Source/production modification NOT executed or certified by creation of this document.**

## Owner-intended outcome

Dev Matrix is a generally capable self-directed engineering department, not a simulated text-proposal generator or finite list of three prepackaged static demos. It can accept arbitrary owner-approved software development briefs, select the best available developer/model/tool stack, inspect an approved repository, plan, make real multi-file changes, run project-appropriate commands and tests, debug failures, perform UI/browser QA, integrate external projects through authenticated controls, and hand back reviewable code and receipts. Its Dev Brain—not Super Brain—owns specialist delegation.

**Remove as capability restrictions:**
1. **Static `GENERAL_DEV_TASKS` and per-task manifest allowlist:** Replace finite task-name enrollment and fragile hash-pinned benchmark-only workflow with a **dynamic project/job descriptor created after owner scope approval**. Descriptors are for resource accounting/identity and audit, not a manual block on new programming work. Existing tasks/receipts remain readable.
2. **Artificial role/action routing barriers:** One general `development_task` intake; Brain selects design, research, implementation, coding, QA, security and documentation specialist paths based on task, not hardcoded synthetic `matrix_dev` roles. No assistant control of workers. The Brain may request or add integrations through legitimate approved permissions; do not self-grant external credentials.
3. **Sandbox-only narrow execution capability:** Remove restrictions that make Dev merely proposal-only, static-HTML-only, fixed Python/Node benchmark-only, or fixed-command-only. Provide **full practical code/build/test/debug tooling in disposable, nonproduction development compute**. Unrestricted *inside an isolated guest/workcell* is acceptable; arbitrary unconfined commands on the **shared credential-bearing Dell/Mac host** are not a safe replacement and must not expose secrets or bypass existing bridge security. Isolation boundary remains between task and host/other tenants; do not let a model run arbitrary privileged host shell.
4. **Single programming language restrictions:** Any languages/build tools/SDKs supported by selected workcell and properly licensed; dependency installation and network-enabled package retrieval within an explicit project policy, with provenance, supply-chain checks, quotas and isolation, rather than flat disabled for every job.
5. **Oversimplified one-shot model tasks:** Permit planning, author/test/fix recursion, bounded parallelism, long-running resumable development, model escalation and evidence-based retries without replacing owner/task-level permissions. Do not claim a failed model test passed because it used a stronger model or longer timeout.

## Enforcement at the actual trust boundary

Retain the *host and side-effect* controls independently of capability:
- Preserve certified v6 controller, owner/GitHub/SSH connector authentication, historical failure receipts, safe rollback and source integrity until a independently certified replacement meets release gates.
- No secrets export, credential mounts, cross-project data access, arbitrary root elevation or changes to SSH bridge permissions without separate approved access and connector allowance.
- Keep publication, production deployment, destructive database changes, paid APIs/spend, payments, live customer/PMS modification and GitHub merges subject to the appropriate owner decision.
- Untrusted generated code must not read owner machines' secrets, touch unrelated projects or alter host security. A disposable isolated VM/container/microVM may run arbitrary development commands **within that protected boundary**; no mandate to keep an artificially tiny HTML/Python-only tool whitelist within the guest.
- Fail closed on uncertified privileges; document exact denial and propose scoped alternative. Do not mislabel development model output or mocked receipts as real tests.

## Release milestones and acceptance

**R1 — Dynamic work intake.** `andaz_static` + one distinct synthetic external-project request accepted using authenticated project identity, without editing a hardcoded per-task manifest list. Wrong project identity and replay denied; task accepted with durable idempotency ID.

**R2 — Real multi-file development.** One non-sensitive external repo code task with model-driven file edits and project-appropriate nontrivial tests; one standalone Andaz mobile-first frontend build with complete honest booking enquiry UI. Build/test/debug receipts must be signed or independently verified.

**R3 — General toolchain, not just fixed files.** Brain selects language and development tools, configures controlled dependency access in ephemeral dev guest, uses a real test runner, and performs browser QA via **its own** authorized worker. At least Python + JS/Node + static frontend end-to-end. Record model choice and resource usage.

**R4 — Robustness.** Test failed code changes, retries, cancellation, hard-kill recovery, duplicate job denial, offline/reconnect recovery, cross-project isolation, deleted/stale source, failed dependency/package install, no-secret-exfiltration and negative privilege checks. Review full logs.

**R5 — Safe canary and rollback.** Independent Dell/Mac evaluator reviews results. Canary the new controller beside unchanged v6, no auto production cutover. Save backup, test revert and remote-authenticated intake. Final release only after actual signed receipts meet gates. Any unpassed gate stays OPEN.

## Dev Matrix Brain's first linked assignment

**Andaz:** https://github.com/aarondash5-star/business-house-matrix/issues/16  
**Andaz approved envelope:** https://github.com/aarondash5-star/business-house-matrix/blob/main/tasks/andaz-static-website/ENVELOPE_2026-10-23.json

The live v6 `dev_general_build` has only `matrix-dev-dashboard-v4`, `matrix-dev-qa-checklist-v5`, `matrix-dev-security-v6` hardcoded. In this condition it cannot build Andaz. Dev Matrix Brain must implement and QA the universal runtime R1–R4 independently within its legitimate capabilities and notify Super Brain about any actual gap it cannot satisfy; do not bypass the external-project/release gates. After certification, enqueue one real Andaz implementation job (not just `dev_proposal`), preserving all previous receipts.

## Existing source

- Current v6 controller: `brain/mvp-controller/controller.py` source and live Dell deployment are distinct. Branch/PR #13 provides draft Gate E candidate; its Python/external-project QA and release gates were **NO-GO** on last verified checkpoint. Never promote by changing a feature flag.
- Super Brain SSH-only approved handoff: `docs/governance/DEPARTMENT_ROUTING_AND_HANDOFF.md`.
- Owner adopted charter: `docs/governance/SUPER_BRAIN_OPERATING_CHARTER.md`.

## Honest reporting

**Not complete** until actual remote Brain-owned source changes, independent tests and verified runtime deployment receipts exist. Sending this document through GitHub/SSH is a handoff, not a live self-upgrade. Do not infer background execution without a running, authenticated job.
