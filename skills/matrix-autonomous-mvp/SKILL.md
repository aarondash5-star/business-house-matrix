---
name: matrix-autonomous-mvp
description: Safely operate independent Business House AI Matrix's Dell central dispatcher, source-backed research, Dev proposals, isolated Python QA and bounded EVOLUTION repairs through authenticated Generic Linux SSH.
---

# Reusable Matrix autonomous MVP skill

Source-of-truth: https://github.com/aarondash5-star/business-house-matrix/blob/main/docs/AUTONOMOUS-MVP-IMPLEMENTATION-2026-10-21.md

## When to use
Use when an approved project needs public research, a Dell Dev proposal, an approved Python test batch or task status, and when the user authorizes that specific project. Reuse CAPABILITY only, never share unrelated private project data, credentials, browser sessions or logs.

## Known live interfaces
Use the connected Generic Linux SSH plugin to access `dell-linux`. Each remote shell command may be queued: poll `linux_task_status` for a terminal completed receipt; never assume submission means execution.

Central runtime: `D=/var/lib/generic-linux-automator-exec/matrix-controller`
Python: `P=/var/lib/generic-linux-automator-exec/.local/share/matrix-dev-brain/venv/bin/python`
User service: `bhm-autonomy-controller.service` (enabled, active, nonroot, local only).

Read-only:
- `$P $D/controller.py status` and `$P $D/controller.py selftest`
- `systemctl --user is-active bhm-autonomy-controller.service bhm-searxng.service`
- `sudo matrix-brain doctor`
- `python3 /var/lib/generic-linux-automator-exec/matrix-searxng/local_search.py 'PUBLIC Python docs query' --limit 5`

Owner-approved new tasks:
- `$P $D/controller.py submit devpilot research_search 'PUBLIC docs query' --key a-unique-safe-key`
- `$P $D/controller.py submit devpilot dev_proposal 'Bounded coding task' --research-query 'PUBLIC documentation terms'`
- `$P $D/controller.py submit devpilot sandbox_qa approved-staged-batch`

## Safety gates and actual success levels
- SearXNG Dell-local search is verified; Mac cannot call it directly while physically separate Wi-Fi networks `Andaz` versus `andaz` use overlapping 192.168.0.0/24. Dell's LAN HTTP gateway remains OFF. Do not expose a research port publicly or silently change Wi-Fi.
- A Dev Brain `review_passed` means a PROPOSAL reviewer agreed, not executable code tests or repository modifications. An earlier model `TaskGroup.cancel()` sample was actually wrong despite model PASS.
- The isolated QA runner requires separately staged Python plus `test_*.py` files; executes real tests under rootless Podman with no network/read-only root/nonroot UID and bounded resources, saving 0600 receipts. Missing tests are never PASS.
- EVOLUTION automatically corrects **one** previously reproduced exact TaskGroup.cancel defect and retests in the sandbox; other defects must escalate. Do not infer general self-healing.
- Dell Controller uses idempotent durable SQLite tasks; external uncertain dispatches are marked `needs_review` rather than repeated.
- Mac creative Groq and Google Trends public RSS are working separately; no completed real-footage reel or cross-machine coordination is proven. Render/publish/spend remain disabled pending thermal, asset and QA signoff.
- Open WebUI releases >=v0.6.6 carry branding restrictions, not standard OSI-only licensing. Do not silently install current build, an old unreviewed build, or previously superseded LibreChat.
- No arbitrary model shell commands, production writes, account changes, payments, posting or privilege updates. Fresh exact-host approval mandatory for root/sudo permission changes. No automatic data sync between projects.

## Evidence and traceability
Controller source: https://github.com/aarondash5-star/business-house-matrix/blob/main/brain/mvp-controller/controller.py
Executed QA: https://github.com/aarondash5-star/business-house-matrix/blob/main/brain/mvp-controller/sandbox.py
Bounded correction: https://github.com/aarondash5-star/business-house-matrix/blob/main/brain/mvp-controller/repair.py
Reusable search skill: https://github.com/aarondash5-star/business-house-matrix/blob/main/skills/selfhosted-searxng-research/SKILL.md

Distinguish `SOURCE_COMMITTED`, `PLUGIN_PUBLISHED`, `DELL_LIVE_VERIFIED`, `MAC_LIVE_DISABLED` and `OTHER_PROJECT_ADOPTION_PENDING` in status. Existing connected tool permissions are unchanged by documentation.

## External MCP Dev integration — 2026-10-22 checkpoint
Read [modular MCP release and receipts](../../docs/DEV_MCP_MODULAR_REUSE_2026-10-22.md) before calling this feature. **Source committed is not a live capability**.

- The Mac Marketing `router.py` was adapted from the existing Dell `matrix-dev-router/matrix-route.py`; preserve model slots, key vaults and SQLite quota data. Never transfer Mac Groq keys or quotas to Dell.
- Dell has an installed MIT `mcp-server-fetch` stdio adapter, validated with a real HTTPS Matrix repo fetch and source allowlist tests.
- Dell model policy has one additive `tool_connections` slot `mcp-fetch-docs`, with 50/day, 3/min, 900-second cooldown, and no paid or private network fallback.
- Canonical adapter `brain/mvp-controller/external_mcp.py`, governance `mcp_tool_router.py`, slot contract `mcp-tool-connection.template.json`, controller `controller.py`.
- **Governed queue not yet activated:** The dedicated quota wrapper and updated controller are versioned in GitHub but not deployed while Generic Linux SSH is returning internal tool failures. Do not submit a live task until host verification, staging, controlled restart, idempotent queue receipt and negative tests pass.
- Once certified, the allowed task is `dev_docs_fetch` with one canonical HTTPS allowlisted technical documentation URL; source output is untrusted `retrieval_only`, not independently tested code, and must not trigger shell, merge, deployment, billing or publishing.


### MCP read-only Dev task — LIVE update (2026-10-22)

The earlier “quota wrapper not yet deployed / generic SSH blocked” note is **superseded** by the [completed live certification](../../docs/receipts/DEV_MCP_LIVE_CERTIFICATION_2026-10-22.md). Dell now runs the pinned `external_mcp.py`, Mac-style `mcp_tool_router.py` and controller route `dev_docs_fetch`. Verified live job `6a646a11-5c0d-410c-beb1-3ee5a3a1afe8` completed on attempt 1 with MCP source-attributed content and ledger receipt. Use `$P $D/controller.py submit devpilot dev_docs_fetch 'https://docs.python.org/3/library/asyncio-task.html' --key UNIQUE_SAFE_KEY`, then poll `show TASK_UUID` and `$P $D/mcp_tool_router.py status`. Do not re-run a completed task under a new key without need. Scope is allowlisted public HTTPS documentation only. No model-selected shell, authenticated/private repo fetch, publishing, merge, or arbitrary MCP tool execution. This is separate from existing SearXNG `research_search` and Dev model proposal flow; automatic attachment of MCP context to arbitrary proposals is NOT certified.
