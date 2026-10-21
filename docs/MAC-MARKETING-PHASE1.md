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
- [x] Isolated Marketing Brain v0.1.0 installed and smoke tested; all four unit tests passed.
- [x] Dell router contract and provenance located; read-only architecture audit completed.
- [ ] Dell-compatible Mac provider adapter integrated; hosted connections intentionally disabled.
- [x] Nonroot cron worker enabled at 2-minute cadence; autonomous handoff tested (host cron service enabled).
- [ ] External providers integrated with verified quotas/licensing.
- [ ] Editing pipeline connected to Marketing Brain.

## Rollback
Production Reel Studio is left untouched; separate Phase 1 directory is removable after saving audit logs. If any foundation task fails, stop the new runner, preserve work receipts, restore previous file snapshots, and leave existing SSH bridge/Ollama/reel autodraft service unchanged.

Documentation owner: Business House AI Matrix / Marketing department.

## Execution record — 2026-10-21 15:24 IST
- GitHub source: `marketing/mac-brain/brain.py`, `worker.sh`, `test_brain.py`, `README.md`.
- Live isolated runtime: `/opt/business-house-matrix/marketing/brain`.
- SQLite queue initialized, persistent receipt writer active, allow-listed local tasks only.
- Ollama health returned three existing local models: `qwen3:1.7b`, `moondream:v2`, `qwen2.5-coder:3b`.
- Baseline queue and model-discovery tasks PASS; idempotency PASS; attempted unauthorized publish task rejected.
- Four isolated tests PASS: durable queue, rejection of unsafe actions, stale-worker recovery, resource limits.
- Cron `*/2 * * * *` enabled for `generic-auto-exec` with `flock` and `timeout`; autonomous ping receipt ID `4e024353-6fa8-4237-9484-5d9c2e2771fd` completed at 09:54:01 UTC.
- CPU `coretemp` check and available-RAM guard deployed: new `draft_plan` jobs defer above 86°C or below 1900 MB available RAM; guard tests passed.
- Cron, Ollama and SSH automator remain active; prior Reel Studio and existing services unchanged.
- Last independently observed sensors included ~81–83°C on Apple SMC and a ~4800 RPM fan, later `coretemp` around 65°C. Further creative inference requires live thermal check.
- No outside API credentials, providers or social publishing actions connected. No video edits executed yet.
- Rollback copy: `brain/brain.py.rollback-v0.1.0`; original crontab saved to `brain/data/crontab-before-marketing-phase1.txt`.
- Next: first creative model draft under resource policy, isolate LangGraph dependencies, Dell router contract audit, Reel Studio read-only adapter, restart/offline tests.

## Dell router compatibility discovery — 2026-10-21
- Confirmed Dell routing documentation `/opt/business-house-matrix/MATRIX_API_ROUTER_2026-10-20.md` and CLI `/usr/local/bin/matrix-route`.
- Existing implementation is a stdlib-based **Pi CLI router**, not a general HTTP API gateway. It manages preference profiles, policy allowlists, conservative quota reservations, per-provider cooldown, fallback and SQLite audit ledger.
- Existing hosted Groq/Cloudflare/NVIDIA slots disabled; no hosted production-access assumption. Free-plan and model-license gates are required before activation; NVIDIA developer endpoints have production use restrictions. Do not copy keys or policies unreviewed.
- Mac adapter should reuse **policy semantics and tests**, not call Dell's privileged CLI over an unrestricted remote shell. For Mac, provider enrollment and account authorization remain separate. Use localhost-only adapters and explicit per-provider enablement.
- Live Dell dev brain `matrix-dev-brain.service` active under `generic-auto-exec`; it is separate from the Mac Marketing Brain. No Dell changes performed.
- Local Mac creative pilot now uses max 64 generated tokens, 2048 context and 2 inference threads to reduce load. First `draft_plan` job queued for autonomous resource-gated processing; result not yet verified at this point.
