# Dev Matrix — modular API reuse + governed external MCP (22 Oct 2026)

## Scope and authority
Independent Business House AI Matrix. Reuse existing Dell and Mac modular routing patterns and source code **without copying credentials, ledgers, customer data, or runtime state**. No Moksha Master sync. Dev tools remain proposal/retrieval/isolated-QA only; no model-selected shell, merge, production deploy, payment or publish.

## Existing systems verified live in this chat
- **Mac Marketing** `/opt/business-house-matrix/marketing/brain/router.py`: `validate` success; `status` version 0.2.0, online enabled, five model slots; two Groq slots eligible with shared quota group, three other slots disabled; research SearXNG enabled; **8/8 router unit tests PASS**. Mac source is `marketing/mac-brain/router.py`.
- **Dell model router** `/var/lib/generic-linux-automator-exec/.local/share/matrix-dev-router/matrix-route.py`: existed BEFORE this change and is the basis Mac adapted. Nine slots, seven hosted slots disabled, local Qwen/Granite ready; model policy validation PASS. No model credentials transferred/created or new inference generated.
- **Dell existing Brain** `bhm-autonomy-controller.service` active and already owns idempotent SQLite task queue. Original source `brain/mvp-controller/controller.py`; previously 5 completed and 4 needs_review tasks. Existing Mac-to-Dell signed research relay and SearXNG remain separate, unchanged.
- **External MCP upstream** `mcp-server-fetch==2026.10.19` (MIT) installed in isolated Dell venv `/var/lib/generic-linux-automator-exec/matrix-external-mcp/venv`, MCP SDK 2.3.0. Real `initialize` succeeded with protocol `2025-11-25`, tool discovery returned `fetch`, and a live request to the Matrix GitHub README returned HTTP 200 and 3,795 captured characters. Local adapter source guard: two positive + ten negative URL tests passed. This proves **one read-only tool call**, not autonomous coding.

## Modular architecture reused
The Mac router's core design (strict provider allowlist, configured slots, independent profiles, minute/day quota, reserve-before-call, SQLite UTC ledger, cooldown on upstream failure, fail-closed policy, no-paid fallback) is ported for **MCP tool use**, not copied as a second model router.

Existing Dell model policy: `/var/lib/generic-linux-automator-exec/.local/share/matrix-dev-router/policy.json`.
- Added `tool_connections` entry `mcp-fetch-docs`, `provider=mcp-server-fetch`, `transport=stdio`, `tool=fetch`, `license=MIT`, `enabled=true`, `quota_group=matrix-dev-docs`, 50 requests/day, 3/min, cooldown 900 seconds. Model `connections` preserved exactly: **9/9**. Backup `policy.pre-dev-mcp-20261022.json` saved on Dell and model router `validate` PASS.
- Upstream adapter `external_mcp.py` limits sources to explicit public documentation domains and this Matrix repository's GitHub source; requires canonical HTTPS without query fragments/credential URLs/nonstandard ports; rejects loopback/private hosts; never launches arbitrary commands and never makes repository writes.
- `mcp_tool_router.py` is the Mac-style governance wrapper, reading the **same Dell policy**, enforcing reserve-before-call with SQLite `mcp-quota.sqlite3` and audit/cooldown, then invoking the strict adapter as a child process without shell expansion.
- Central Brain route `dev_docs_fetch` delegates to the wrapper, retains a job receipt and **QA level `external_mcp_retrieval_only`**. It is a development research step, not executable code QA or an automatic merge. SearXNG remains the discovery/search path.

## Versioned source
- [MCP adapter](../brain/mvp-controller/external_mcp.py)
- [Mac-style modular MCP tool router](../brain/mvp-controller/mcp_tool_router.py)
- [Tool slot template](../brain/mvp-controller/mcp-tool-connection.template.json)
- [Updated durable controller](../brain/mvp-controller/controller.py)
- [Mac reference router](../marketing/mac-brain/router.py) and [Mac modular API docs](MAC-MARKETING-API-ROUTER.md)

## Release state — critical distinction
**Verified Dell live:**
1. Upstream MCP installed and a real public-source fetch returned successfully.
2. Strict source allowlist selftest passed.
3. `dev_docs_fetch` route was initially added directly to Dell live `controller.py`, with syntax / controller selftests passing; rollback file `controller.py.pre-external-mcp-20261022`.
4. Dell model policy now contains the new MCP slot, and model router validation passed.

**Source committed, NOT LIVE-VERIFIED:**
1. Latest `mcp_tool_router.py` quota ledger wrapper is committed on GitHub but not yet installed on Dell.
2. The controller GitHub source now calls `mcp_tool_router.py`, but Dell live controller still calls `external_mcp.py` directly until a verified deployment.
3. No durable controller `dev_docs_fetch` job has reached terminal completion in this chat. No actual autonomous Dev Brain use of MCP retrieved data yet.

**Blocker:** Following the above successful readbacks, the connected Generic Linux SSH plugin began returning `The tool failed internally.` for both Mac and Dell status, probe and shell actions. No remote deploy/restart/job was attempted after this issue. Do not treat source commit as live deployment. Do not bypass connection/owner privileges by using a different unauthorized execution channel.

## Exact release procedure when authenticated Dell bridge recovers
1. Verify host heartbeat, Dell controller active, `status` queue empty of `queued`/`delegated`/`dispatching`, disk space, and the existing model policy slot.
2. Retrieve all **versioned** `brain/mvp-controller/{external_mcp.py,mcp_tool_router.py,controller.py}` from this repository's pinned commit (GitHub SHA `e82d5d6e7dd785cbbee9e9adcab91dbde0a2b8e1` or a later reviewed commit). Use private temporary staging and check compile/tests. Do not use arbitrary `main` without pinning.
3. Back up current three runtime files, enforce 0600 on adapters and 0700 on controller, atomically install. Compare/reconcile the initial live `dev_docs_fetch` change. Do not replace SQLite ledger or any credentials.
4. Run `/var/lib/generic-linux-automator-exec/matrix-external-mcp/venv/bin/python $D/external_mcp.py selftest`; run `$P $D/mcp_tool_router.py selftest`; run `$P $D/controller.py selftest`; verify `matrix-route.py validate` and `mcp_tool_router.py status`.
5. Controlled user service restart `systemctl --user restart bhm-autonomy-controller.service`, verify active. Issue one `dev_docs_fetch` controller task with a unique idempotency key and a public doc source URL, then poll its durable receipt and verify provider, tool slot, source citation, nonempty content and ledger reservation. Resubmit same key and verify `deduplicated=true` with no extra fetch.
6. Negative tests: invalid localhost/query/foreign repo rejected before ledger reservation; disabled tool fails closed; simulated exhausted minute quota prevents call. No arbitrary shell tools, no public listener, no unverified extra providers. Roll back adapters/controller to private backed-up files on any regression.

## Explicit status at writing
**Mac modular router: VERIFIED. Dell modular model router: VERIFIED. Dell source-restricted upstream MCP: VERIFIED. MCP slot model policy: LIVE. Governed quota wrapper in durable Dev queue: SOURCE COMMITTED / LIVE BLOCKED BY SSH CONNECTOR.**
