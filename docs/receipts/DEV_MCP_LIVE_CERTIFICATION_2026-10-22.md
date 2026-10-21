# Dev Matrix external MCP — live release certification

**Date:** 2026-10-22 IST (2026-10-21 19:43–19:50 UTC).  
**Project:** independent `aarondash5-star/business-house-matrix`.  
**Result:** **PASS — Dell Dev MCP documentation retrieval service and durable controller task path LIVE**. This is a *read-only research integration*, not autonomous code modification.

## Source and deployment
- Pin: GitHub commit `e82d5d6e7dd785cbbee9e9adcab91dbde0a2b8e1`.
- Files on Dell: `/var/lib/generic-linux-automator-exec/matrix-controller/{controller.py,external_mcp.py,mcp_tool_router.py}`.
- Binary: isolated `mcp-server-fetch==2026.10.19` MIT, `mcp` SDK 2.3.0, subprocess `stdio` protocol `2025-11-25`.
- Source SHA-256 deployed: `controller.py=354ca8e8594aff22c73b6f89219baeb5c94b66ec34ec4642a43491774e45b34a`; `external_mcp.py=a506044222abb3a5c86d0def3c9b061cc4cef0d4edf05e41ec41bf0edd3c6367`; `mcp_tool_router.py=978111c92528df8b4cfcc6a4d3419d11bd47a4393764c7ad75c56813abfcb074`.
- Backup: `/var/lib/generic-linux-automator-exec/matrix-controller/release-backup-dev-mcp-20261022`, preserving pre-deploy controller and Fetch adapter. Earlier standalone source rollback `controller.py.pre-external-mcp-20261022` also preserved.
- Model routing policy: `/var/lib/generic-linux-automator-exec/.local/share/matrix-dev-router/policy.json`; 9 existing model slots preserved, no model routing/credentials changed. Additive `tool_connections` slot `mcp-fetch-docs` enabled; `daily_cap=50`, `minute_cap=3`, `cooldown=900s`, no paid fallback, no private network access. Previous policy backup `policy.pre-dev-mcp-20261022.json`.
- Controller user service `bhm-autonomy-controller.service` restarted and `active`; SearXNG and signed research relay also `active` at final check.
- No public MCP listener, no new privileged SSH access, no root/sudo change, no Mac secret or quota transfer, and no Moksha Master sync.

## Live receipts and validation
| Gate | Result / evidence |
| --- | --- |
| SSH probe | `8a4a5986-5f68-4a58-95b5-18dff108d9a0` completed, exit 0; Dell paired/online, 3 host lanes fresh |
| Stage read / compilation | `3c0a1fc2-875f-44bd-84a7-f26de313c67a` completed, exit 0; three files pulled from pinned commit, controller diff inspected; Python compile and all staged checks passed |
| Deployment | `8afdac60-4465-4414-ad80-5825f1a8b9cb` completed, exit 0; no pending queue tasks, backups created, file install, runtime selftests, model policy validation, controller restart active, hashes read back |
| Durable task submit and duplicate | SSH receipt `4e059908-366d-4f5b-a662-aede2609e5b2`, exit 0. New Central Brain task `6a646a11-5c0d-410c-beb1-3ee5a3a1afe8` with action `dev_docs_fetch`, key `dev-mcp-live-20261022-0001`; immediate second identical submission reported `deduplicated=true`, same ID |
| Live autonomous fetch completed | SSH receipt `a64ef792-830b-42c6-84d7-75aefdb35bd8`, exit 0. Controller task `6a646a11-5c0d-410c-beb1-3ee5a3a1afe8` **completed, attempt 1**, QA `external_mcp_retrieval_only`; source `https://raw.githubusercontent.com/aarondash5-star/business-house-matrix/main/README.md`; provider `external-mcp`, tool `mcp-fetch-docs`, receipt quota event `1`, content `3795` characters, `writes_performed=false` |
| URL guards | Controller rejected localhost/private IP and foreign Github repository prior to quota reservation |
| Synthetic Mac-style quota tests | SSH receipt `f66ef1cb-52e4-4914-8551-7d2ff12522c0`, completed exit 0. Isolated temp SQLite ledger exercised all 3/min reservations and denied fourth, enforced cooldown, disabled slot and private URL; no change to production ledger |
| Final health | MCP ledger daily use `1/50`; minute use `0/3` at final check; controller, SearXNG and research relay all active |

The first attempt at the deployment command `62794ac2-b7f5-4fb1-85e8-edf556677c15` exited 2 at `/bin/sh set -o pipefail`, *before running any mutable statements*. The same deployment plan was then executed successfully using an explicit Bash heredoc. This is not counted as a deployment regression and required no rollback.

## Current capability and boundary
Use the Dell central controller command:
```bash
D=/var/lib/generic-linux-automator-exec/matrix-controller
P=/var/lib/generic-linux-automator-exec/.local/share/matrix-dev-brain/venv/bin/python
"$P" "$D/controller.py" submit devpilot dev_docs_fetch \
  'https://docs.python.org/3/library/asyncio-task.html' \
  --key your-unique-safe-task-key
"$P" "$D/controller.py" status
"$P" "$D/controller.py" show TASK_UUID
"$P" "$D/mcp_tool_router.py" status
```

The tool accepts only a source-validated canonical HTTPS technical-documentation URL; the exact source and content are retained in the durable receipt and treated as untrusted retrieval evidence. Explicit source search remains through Dell self-hosted SearXNG. The Dev model's proposal runner is **not yet automatically attaching the MCP text to all generated coding tasks**, and existing `dev_proposal` output remains proposal-only unless separately tested by QA. No uncontrolled tools, code execution, Git merge, production deployment, payments or publishing were enabled.

## Rollback
With the controller queue idle, restore the backed-up controller and adapter. Remove only the newly introduced runtime `mcp_tool_router.py` if rolling back this release; leave quotas/ledger as evidence. Restart `bhm-autonomy-controller.service`, verify `active`, and inspect saved receipts. Do not delete unrelated queue or model policy data. Tool connection can be disabled via its specific, schema-validated policy setting during a controlled rollback while keeping the nine model slots intact.

**Release status:** SOURCE_COMMITTED / DELL_LIVE_VERIFIED / DURABLE_DEV_MCP_JOB_COMPLETED / QUOTA_GATES_TESTED. Mac Marketing unchanged; no claim of fully autonomous Dev implementation or 24-hour outage resilience.
