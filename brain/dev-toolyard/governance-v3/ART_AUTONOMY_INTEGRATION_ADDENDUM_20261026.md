# Matrix Dev Tool Yard Manager V3 — AI Art Worker Integration Addendum
**Date:** 2026-10-26 • **Scope:** Dell owner-local operations • **Approval:** nonproduction Shaadi art work only

This addendum updates the existing Manager V3 handover without replacing its governance, universal QA standard, task registry or release approvals. The fixed Blender worker and bounded local AI Art Director are separately enrolled **project-specific subprocesses**, **not** new universal manager privileges.

## New capabilities registered
1. **Fixed art worker V1:** `~/matrix-controller/art-worker-v1/worker.py`, SQLite queue, enrolled SHA-256-pinned scripts; two-minute systemd timer, Blender 4.5.15 LTS; bounded render/inventory and technical GLB QA; ambiguous failures mark `needs_review`. The original OpenCode art critique is still `needs_review` after timeout (exit 124).
2. **AI Art Director V1:** `director_loop.py`, `ai_art_vision.py`, `ai_art_refine.py`, project-scoped enrollment and SHA-pinned allowlisted scripts, 30-minute systemd timer, local Ollama `qwen3-vl:2b-instruct` requested. It supports at most **three fixed derivative profiles** (glasses, jasmine, zari). It does **not** execute AI-generated scripts.
3. **Observability:** Manager's read-only governance snapshot includes `governance_v3.art_worker_v1` and `governance_v3.ai_art_director_v1` with status, attempts, review requirements and `release_authorized=false`. The Manager remains responsible for preserving its legacy intake/release gate independently.
4. **Evidence contracts:** Every legitimate candidate requires source/editable .blend SHA, actual render image SHA, GLB SHA, model and revision receipt, independently verified visual QA and explicit owner acceptance of exact art hashes.

## Current verified state
At the last local check (2026-10-26, 02:31 IST), both timers were enabled, Manager v0.2.4 online, **0 AI-directed cycles had run**, and the Ollama model pull was active but not installed/usable. No new full reference-image bytes had been verified in Dell. Original owner references exist in the ChatGPT Library, with hashes pinned by the enrolment. The worker has completed render and foundation inventory jobs; neither constitutes art approval.

At the Manager integration test gate, **26 existing tests passed**; art director contract tests **7 passed**. Integration into the actual VLM/render/GLB loop has *not* been certified. Last independent structural QA stays character **5/9**, mandap **3/6**, visual grade FAIL.

## Required operating and project-admission processes
- New art task -> owner scope and immutable quality pin -> separate admission/hashes -> existing Manager/queue exposure -> bounded script -> actual output and error receipts -> independent quality assessment -> owner sign-off -> separate release workflow.
- Any model/provider/script/permission drift -> quarantine and explicit bounded retest; never rewrite approval ledgers. No opportunistic Cline/Prefect installation.
- Timer enablement, file hashes and local VLM critique do not imply artistic acceptance. The system stops on failed model pulls, timeouts, insufficient licensing, interrupted/uncertain execution and exhausted allowlisted profiles.
- The 30-minute Dell timer is a local automation; **ChatGPT hourly supervision cannot be invoked by arbitrary inbound MCP webhooks**.
- This feature does **not** implement the project-wide “every new tool auto-admitted” rule. The earlier `UNIVERSAL_AUTO_ADAPTER_ADMISSION_HANDOVER_20261026.md` explicitly states universal pre-dispatch interception is **not yet deployed**. Any other project/worker still requires separate registration and owner authorization.

## Canonical documentation
- [Formal SOP](../../projects/shaadi-aunty-dodge/art/quality-v1/worker/v1/AI_ART_DIRECTION_SOP_V1_20261026.md)
- [Operator runbook](../../projects/shaadi-aunty-dodge/art/quality-v1/worker/v1/AI_ART_DIRECTOR_OPERATIONS_RUNBOOK_20261026.md)
- [Capability registry](../../projects/shaadi-aunty-dodge/art/quality-v1/worker/v1/AI_ART_CAPABILITY_REGISTRY_V1_20261026.json)
- [Art worker handover](../../projects/shaadi-aunty-dodge/art/quality-v1/worker/v1/AI_ART_DIRECTOR_HANDOVER_20261026.md)

Paths above are relative conceptual references from `brain/dev-toolyard/governance-v3`; use the exact absolute repo paths on GitHub. All documents reside only on an isolated review branch until separately approved.

## Safe rollback / pause
Stopping `bhm-shaadi-ai-art-director.timer` does not stop Matrix Manager, erase job queues or release approval controls. Restoring manager code is handled separately from project-specific art worker scripts. Preserve logs and SHA-256 receipts for all failure investigations.

**No production game merge, external publication, payments or automatic visual QA approval is granted by this addendum.**
