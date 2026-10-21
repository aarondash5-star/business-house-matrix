# Mac Marketing Brain — Phase 1 Runtime

Host: `mac-linux` (KARAN). Source is tracked in this public repository. The Mac's runtime is an isolated copy under `/opt/business-house-matrix/marketing/brain`; existing `reel-studio` is preserved.

## What is implemented
- `brain.py`: dependency-free Python 3.12 fail-closed local job processor.
- SQLite durable job queue, idempotency keys, bounded retries, stale-worker recovery and per-job atomic receipts.
- Local Ollama models discoverable through `localhost:11434`.
- Allowlist: `ping`, `ollama_health`, `draft_plan` only. Does not execute code suggested by AI.
- Policy file `config.json` (owner-only): all online providers, social publishing and spend disabled.
- Creative inference default **disabled** after a 90°C CPU observation. Available RAM >= 1900 MB and coretemp < 86°C were initial pre-run floors but did not prevent thermal buildup during generation.
- Nonroot worker `worker.sh`, serialized with flock; system cron runs it every 2 minutes, at most 100 seconds per job. Cron persistence depends on `cron.service` being active/enabled.

## Operator commands (on Mac)
```bash
B=/opt/business-house-matrix/marketing/brain
python3 "$B/brain.py" health
python3 "$B/brain.py" status --verbose
python3 "$B/brain.py" enqueue ping --key my-unique-key
python3 "$B/brain.py" enqueue ollama_health --key my-health-check
python3 "$B/brain.py" enqueue draft_plan --payload '{"brief":"Create a three-concept reel plan for a sample product"}' --key sample-draft
python3 "$B/brain.py" receipt JOB_UUID
tail -25 "$B/worker.log"
crontab -l
```

## Boundaries
- This does not yet connect or replace `reel-studio`, and does not schedule any social publication.
- LangGraph, external provider APIs and Dell-router integration are NOT implemented at this stage. Their deployment follows dependency, license, quota and interface audits.
- Ollama creative inference is **SAFETY-LOCKED OFF**: `local_inference_enabled=false` in runtime config and source default. `draft_plan` cannot make an inference request until explicitly re-enabled after thermal mitigation and validation.
- No secrets in the public GitHub repository. Do not commit runtime config, user footage, queue database, receipts or worker logs.
- Current cron job only runs allowed local tasks; no arbitrary shell or root privilege.

## Rollback / Stop
1. Save `$B/data/queue.sqlite3` and `$B/receipts` if audit continuity is needed.
2. Remove only the line labeled `BHM_MAC_BRAIN_PHASE1` from the `generic-auto-exec` user's crontab.
3. Do not touch `generic-linux-automator.service`, `ollama.service`, or `bhm-reel-autodraft.path`.
4. Restore the prior `brain.py.rollback-v0.1.0` if specifically reverting the guard patch.
5. The new `brain` directory may be archived separately; preserve receipts and logs before deletion.

## Next Phase 1 steps
- Verify cron consumes an enqueued job without manual invocation and writes a receipt.
- Confirm creative inference under thermal/memory limits.
- Inspect Dell's actual API-router contract; add disabled-by-default provider adapters with free quota accounting.
- Install compatible MIT-licensed LangGraph into an isolated venv after dependency/licensing review.
- Connect to a read-only Reel Studio adapter and run a zero-publication workflow.
- Complete restart/recovery/fault tests and update the Phase 1 status ledger.

## 2026-10-21 thermal incident
An autonomous 64-token Qwen3 draft passed but drove the CPU sensor to 90°C and maximum fan. Mac runtime now enforces a fail-closed local inference lock. Keep the worker running for low-impact queue tasks; do not re-enable model generation merely by raising the thermal threshold. Use an optimized smaller model or remote worker after validating performance and recovery.

## Research router update — 2026-10-21
- Tavily deprecated; SearXNG replaces it as the only allowlisted research tool, source `searxng_research.py`.
- Mac `research_search` is wired to the client but the operational policy entry remains disabled until private Dell reachability is restored (the two Wi-Fi peers currently cannot ARP one another).
- Dell self-hosted rootless SearXNG is live and can be researched manually through Generic Linux SSH with `python3 /var/lib/generic-linux-automator-exec/matrix-searxng/local_search.py 'query'`.
- Do not publish or make paid provider calls. See [SearXNG deployment](../../docs/RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md).
