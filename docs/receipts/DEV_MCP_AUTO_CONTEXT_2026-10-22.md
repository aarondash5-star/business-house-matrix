# Dell Dev Matrix — automatic MCP source-enrichment release (2026-10-22)

## Release verdict
**DEPLOYED / SOURCE-ENRICHMENT PIPELINE PASS.** Automatic MCP evidence is now integrated into the live LangGraph Dev Brain before its planning/coding/QA text stages. A real upstream source was fetched by MCP and injected into all three stage prompts under isolated deterministic model stubs.

**Full unattended real-model coding and independently executed QA: NOT CERTIFIED.** Initial real local Granite job ended with MODEL_TIMEOUT at QA review; its MCP fetch also degraded in that particular run. This failure is preserved. Never infer working code from the synthetic model-stage test.

## Changes
- Dev Brain source: `brain/dev-brain/brain.py` (new canonical versioned source, originally copied from verified existing Dell instance).
- Context helper: `brain/dev-brain/dev_mcp_context.py`. Strict allowlisted public technical documentation host selection from SearXNG results or fixed public technical topic mapping. No private prompt content inserted into network URL; read-only subprocess calls into the existing governed `mcp_tool_router.py`; bounded excerpt (2000 chars), source URL, SHA256 and quota event. Untrusted content is marked as data, not instructions.
- Graph edges: `public_research → mcp_documentation → plan → develop → qa_review`. The MCP context is passed into all three stage prompts. `docs.json` is stored alongside `research.json`, `plan.md`, `implementation.md`, `review.md` and `result.json`.
- Results include `mcp_docs_attached`, `mcp_source_url` and `mcp_content_sha256`. Coding jobs for which official documentation is relevant cannot obtain the internal text-review PASS when source retrieval is unavailable.
- Central controller source: `brain/mvp-controller/controller.py`, now requires `mcp_docs_attached=true` before reporting `dev_proposal` as `completed`, and includes source evidence in the returned payload.
- No network listener, root/sudo permission change, Mac API key transfer, uncontrolled Pi MCP tool, production repository write, publish or spend. Existing Matrix model router and QA sandbox are preserved.

## Verified live receipts
1. Dell host online, three lanes fresh, original Dev Brain service `matrix-dev-brain.service` active.
2. Original source staged separately as `brain.mcp-staged.py`, helper pulled from GitHub commit `2fb263bcbf36fe5ea2c5965924971172293c82e5`. Graph stage modification tested with temp SQLite and independent synthetic MCP response. Staged selftest PASS: `PASS_SEARXNG_OPT_IN_SOURCE_CONTEXT_AND_RECEIPT` and `PASS_LG_GRAPH_3_NODES_CHECKPOINT_SQLITE_ARTIFACTS` (legacy selftest label; graph now has five stages). SHA after first installation: `brain.py=6ae53f00d8618a185a3b4fe212e13bab9cc2f3fb88f0fb44bbf2bf67fac6a291`; `dev_mcp_context.py=2bc987f33bd183454e4db7ae11293689b6a30c98dfb8dad2c0933e2add03e66f`.
3. First service restart after copying Brain staged source: SSH receipt `2ffcf6f5-7515-4a3c-aa2f-f2e256a57bc8`, `matrix-dev-brain.service active`. Backed-up original executable `brain.py.pre-mcp-20261022`.
4. First real model job via central controller: Central `1b72242c-73ed-49d7-a4c1-e4422e991ac6`, remote Dev `10e7a60a-d92c-4538-913c-326ba16d689d`. SearXNG fetched Python TaskGroup public sources; checkpoint proved `mcp_documentation` executed but `docs_receipt.available=false` / `reason=mcp_unavailable` on that first attempt (quota event NOT recorded). Job reached QA review but ultimately `failed` with `MODEL_TIMEOUT` at `2026-10-21 20:17:50 UTC`. Existing error receipt and checkpoints preserved, no manual replay.
5. A separately bounded direct live MCP call from the same Dell Dev environment **succeeded** for `https://docs.python.org/3/library/asyncio-task.html`, with SHA256 `31f6389230edfc8085d2996c36c57907a478757087ecbefd166ffaf7ec94e595`, quota event `2`. This proved the package, transport, allowlist and tool ledger were operational independent of the transient first job.
6. Corrected source gates to fail closed: source pin `a46ff0c8a2b2d684291cbeb26d45a4ba2a823b57`; pinned staged syntax/Brain regression/adapter selftest/controller regression passed under SSH receipt `c90296d8-1fed-4b40-bb9b-2174a43a3747`. Live deployment with backup files `brain.py.pre-mcp-gate-20261022`, `dev_mcp_context.py.pre-mcp-gate-20261022`, `controller.py.pre-mcp-gate-20261022`: SSH receipt `49bac6a6-3e32-446e-80d0-8ae62d94899b`, both Dev system service and controller user service `active`.
7. Real SearXNG + MCP, synthetic model-stage QA under **isolated temporary database**, no production model calls: SSH receipt `3be23de3-6d0a-451d-83b4-e0a3ffbe951e` `completed/exit 0`; `LIVE_GROUNDED_GRAPH_CHECK_PASS`. `mcp_docs_attached=true`, source Python TaskGroup URL, SHA256 above, quota event `3`, `prompts=3`, `all_prompts_include_source=true`, five correct stage transitions, and `tests_executed=false` correctly recorded. This is strong evidence for **source integration** but synthetic model text is not an actual LLM or executable-code QA success.

## Why full autonomy remains open
- Local `fast` route currently chooses `ollama/granite4:3b` through the existing Pi router. CPU/RAM diagnostic after timeout found ~5.4 GiB available RAM, zero swap activity; model generated plans and code, then timed out on QA review at 240 s. No auto-paid provider switch, forced retry or system privilege escalation.
- Dev model is still proposal-only and cannot edit repository. Independent rootless no-network Python QA remains a separate approved `sandbox_qa` action, not automatically executing arbitrary model-generated source.
- No reboot/24-hour soak on the new five-node graph has been performed.

## Runbook and rollback
- Live Brain `/var/lib/generic-linux-automator-exec/.local/share/matrix-dev-brain/brain.py`; source module `dev_mcp_context.py`.
- Central controller `/var/lib/generic-linux-automator-exec/matrix-controller/controller.py`.
- Model policy and ledger unchanged. MCP tool quota remains 50/day, 3/min, 900-second cooldown; one Docs Fetch tool only, public HTTPS allowlist.
- Submit via central `controller.py submit devpilot dev_proposal 'Task' --research-query 'Public technical search' --key UNIQUE`. Inspect central `show TASK_UUID`, remote `brain.py show REMOTE_UUID`, `artifacts/REMOTE_UUID/docs.json`, and `result.json`. A `review_passed` string is NOT proof of executed QA. Source missing or model error must be `needs_review` / failed, not fully completed.
- Roll back only when Dev queue idle by restoring `brain.py.pre-mcp-gate-20261022` and `controller.py.pre-mcp-gate-20261022` plus exact preserved helper, then restart the existing two services; keep DB/checkpoints/receipts. To revert all five-stage changes restore `brain.py.pre-mcp-20261022`. Never delete failed receipts or alter SSH/root rights.

## Follow-on
Optimize local Granite/Pi response bounds or activate a separately enrolled, confirmed free Dev model route; run a fresh idempotent live real-inference task using already proven MCP tool and confirm terminal completion. Then add independent bounded sandbox QA for generated Python artifacts with distinct external test fixtures. Do not label this pipeline fully autonomous until that succeeds.
