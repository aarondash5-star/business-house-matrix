# Mac Marketing Department — Phase 1 Foundation (2026-10-21)

Status: **APPROVED TO START**, execution in progress. Scope: independent Business House AI Matrix, NOT Moksha Master.

## Objective
Turn mac-linux (KARAN) into a low-resource, autonomous Marketing submatrix, controlled from GPT and the Matrix Brain via Generic Linux SSH/MCP. Offline-first orchestration, online creative workers when permitted. No auto-publishing or paid transactions without explicit authorization.

## Current verified baseline (2026-10-21)
- Linux Mint 22.3; Intel i5-5350U (2 cores/4 threads); 7.7 GiB RAM; Intel HD Graphics 6000; ~53 GB free disk.
- Ollama service active; qwen3:1.7b, moondream:v2, qwen2.5-coder:3b installed.
- Generic Linux Automator outbound bridge online, shell enabled; service auto-start enabled.
- Reusable local source: `/opt/business-house-matrix/marketing/reel-studio` (reel.py, finisher.py, stock.py, beats.py, autodraft.sh). `bhm-reel-autodraft.path` enabled, service inactive (triggered service).
- Python reel-studio virtualenv contains PySceneDetect/OpenCV/Pillow/NumPy; system FFmpeg and ffprobe installed.
- The /opt/business-house-matrix path on Mac is NOT a Git checkout; treat production host as runtime, GitHub as canonical source. Do not alter existing Reel Studio or service units during foundation stage.
- Dell online; existing API-router deployment path was not identified by the generic worker account. Do not claim router reuse is implemented before locating and auditing actual contract.

## Hierarchy
Business House Matrix Brain -> Marketing Department Brain -> Research / Creative / Copy / Video / Design / Distribution / Analytics / QA / EVOLUTION.
Every worker returns evidence, outputs, cost/latency metadata, and status. EVOLUTION can propose changes; actual code/model/policy promotion requires controlled tests and authorization.

## Phase 1 work packages
1. Inventory and non-destructive safety baseline (completed).
2. Write architecture, machine-specific limits, capability map, licensing decisions, rollout log and rollback plan.
3. Install separate `marketing/brain` foundation without replacing the existing Reel Studio. Prefer standard-library compatibility and optional MIT-licensed LangGraph once dependencies verified.
4. Local durable queue, claim/retry states, SQLite store, idempotency keys, bounded attempts, atomic hand-off to processing.
5. Local Ollama adapter: health/list and lightweight test; model selection by task. No model pulls without checking memory/disk.
6. Pluggable API-router interface: disabled by default until Dell router format, provider keys, pricing and license policy verified; secrets never stored in repo.
7. Sandbox / safety policy: dry-run first, allow-listed tasks, explicit human approval for publication, spend, credentials, root changes, external writes; no arbitrary shell from LLM outputs.
8. Smoke test: queue -> worker -> Ollama/checkpoint -> receipt; offline queuing; graceful fallbacks and restart recovery.
9. Controlled boot persistence as a distinct later step after smoke tests, with health, resource limits, monitoring, and rollback.

## Golden Rule 0 — reuse and licensing
Reuse the existing reel-studio scripts and bridge. Validate OSI-approved licenses for software and approved open licenses for model weights BEFORE enabling external dependencies; review security, maintenance, compatibility and cost. LangGraph is MIT and APScheduler is MIT, but neither should be assumed installed. Never deploy newer Open WebUI without separately resolving its OSI licensing restriction. OpenClaw stays deferred.

## Safety and operating limits
- On this 8 GB CPU-only machine: only one local inference or video render job at a time; start conservatively, monitor thermal and memory behavior, do not run new heavy models concurrently.
- Permit autonomous research/drafts, local editing and internal QA; keep publishing/new campaigns/spend privileged changes in human approval.
- Offline mode stores work locally and marks network-dependent tasks pending; avoid repeated expensive API retry storms.
- Persist receipts, model/provider used, errors and actions. Keep credentials out of stdout, logs, git and chat.
- Every service/config change must have a rollback path and preserve the SSH bridge/Ollama/reel service.
- Full root access is not presumed from connector capability; verify authorization and avoid changes to system security without consent.

## Acceptance gates
P1 foundation: isolated runtime installed, no existing editor regressions, local Ollama reachable, queued dry-run task survives worker restart, no unintended external effects, receipt and restore path validated.
P2 first three finished vertical reels from same input, technical QC and approved assets.
P3 channel integration behind approval; P4 measured outcomes driving EVOLUTION.

## Status ledger
- [x] Architecture and deployment constraints specified.
- [x] Mac/Dell online/read-only inspection.
- [x] Existing editing stack discovered for reuse.
- [ ] Isolated Marketing Brain runtime installed and smoke tested.
- [ ] Dell router contract located, audited and integrated.
- [ ] Boot service enabled following validation.
- [ ] External providers integrated with verified quotas/licensing.
- [ ] Editing pipeline connected to Marketing Brain.

## Rollback
Production Reel Studio is left untouched; separate Phase 1 directory is removable after saving audit logs. If any foundation task fails, stop the new runner, preserve work receipts, restore previous file snapshots, and leave existing SSH bridge/Ollama/reel autodraft service unchanged.

Documentation owner: Business House AI Matrix / Marketing department.
