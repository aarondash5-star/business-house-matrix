# Secure Dev Matrix Autonomy — Restricted Pilot and Certification Plan

Date: 2026-10-22 (Asia/Kolkata)  
Target: Dell Inspiron 5379, existing Business House Matrix  
Tracker: `aarondash5-star/business-house-matrix`, Pine chat issue #2

## Governance

Owner authorized autonomous development capability and project-scoped deployment. This pilot does **not** authorize a generic shell or filesystem agent, installing paid APIs, changing the existing SSH bridge/root permissions, connecting private Pine trading data or self-publishing. All accounts, credentials and private customer data stay isolated. Ashwakaal Support Channels remains separate. Cross-project verified integrations are reported through the authorized Supabase Master event inbox; no new Master repository route is assumed.

## Golden Rule 0 / Reuse / Cost

- Existing Dell Matrix controller v0.1.0: durable SQLite tasks, idempotency, existing QA and deterministic EVOLUTION repair. Preserve current working service.
- Existing `@earendil-works/pi-coding-agent` **v1.3.0, MIT**: [upstream npm](https://www.npmjs.com/package/%40earendil-works/pi-coding-agent), already installed with local Ollama. Model invoked explicitly without tools, MCP, extensions, skills, context files, session, or remote provider.
- Existing Ollama Qwen3 4B local model; [Qwen Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B) **Apache-2.0**.
- Existing [containers/bubblewrap](https://github.com/containers/bubblewrap) **LGPL-2.0-or-later**, v0.9.0, already installed, unshared user/mount/network/PID namespace.
- Existing secure-coding sandbox worker and reviewed-patch runner: `brain/secure-coding/sandbox_worker.py` and `reviewed_patch_runner.py`; tests `tests/test_runner.py`.
- No new npm/pip install, paid inference, model subscription or hosting. Runtime cost is local compute/electricity. No additional license redistribution obligations beyond preservation of upstream notices if bundled in the future.

## Deployment strategy and current boundaries

Architecture stages:
1. **Intake and identity:** exact project ID + exact task manifest. No arbitrary user-supplied command or repository path.
2. **Proposal:** fixed synthetic-only prompt to installed local Pi with no tools and local Ollama. Proposal is untrusted JSON data.
3. **Validation:** allowlisted frontend/backend/tests/docs paths; bounds on total bytes and file count; block external calls and credential source patterns; reject symlinks/traversal.
4. **Write:** the existing reviewed-patch runner enters Bubblewrap with only a synthetic workspace writable, no network and no host home or private data.
5. **QA:** independent Python unittest and Node built-in tests inside the sandbox; no test means no pass.
6. **EVOLUTION:** at most one additional model proposal, bounded by deterministic failed-QA context. No unbounded retries.
7. **Commit:** copy only SHA-verified generated files to a new review-only directory, create a **local** Git review commit with no credentials, hooks, push, merge or public deployment.
8. **Promotion:** after negative isolation tests, receipt validation, code review and no model-selected tool permissions. Public staging release requires a separate authorized deployment route and approval.

The pilot is `brain/secure-coding/scoped_dev_pilot.py` on `docs/modular-mcp-chat-template-20261022`. The only enrolled workload is synthetic Pine Engineer chat accessibility work. No other project is enrolled, no private Pine repository is mounted, and no TradingView controller access is possible from the sandbox.

## Evidence and corrections

- Preflight verified Bubblewrap probe PASS (workspace writable, home/foreign project hidden, network blocked), and 5/5 existing negative/unit tests PASS.
- First pilot `pine_ui_accessibility_v1` created a terminal `blocked` receipt before generating files: explicit Python environment selected Node v18; Pi requires the installed Node v24.
- Fixed exact runtime executable search path to `/usr/local/bin:/usr/bin:/bin`, resolving the installed `/usr/local/bin/node` -> `/opt/node/node-v24.22.0-linux-x64/bin/node`. Committed fix on the existing review branch; the first failure receipt is retained.
- Started a single fixed-runtime pilot `pine_ui_accessibility_node_retest_v1` via the owner's unprivileged **user** systemd instance, bounded by `RuntimeMaxSec=400` and `MemoryMax=1200M`. It must be judged solely from `autonomous-code-state/<task>/receipt.json` and reviewed committed artifacts, not the service start alone.
- As of this document composition, post-model QA and review commit not yet certified; read fresh receipts before enabling a Matrix controller route.

## Mandatory stop conditions

Fail closed if model times out, output invalid, source/network/secret pattern rejected, sandbox private access exposed, test code fails, file SHA does not match, local Git commit absent, or request attempts a non-enrolled project. Never silently rerun an ambiguous job. Do not infer a remote GitHub commit from a local review commit. No automatic merge/publish/trading/billing.

## Remaining production gates

- Complete one demonstrably passing end-to-end model-generated synthetic source test and local review commit, record SHA and negative tests.
- Independently code review existing staged pilot and check that a model cannot read owner workspace or attach credentials.
- Add a single manifest-scoped action to the durable Matrix controller only after the pilot succeeds, tested in an independent DB and with rollback backup; no default free-form code execution.
- Obtain repo-specific enrollment and separate app-specific staging deploy approval for additional projects; integrate approved GitHub PR automation using per-repo credentials only after credential-isolation tests.
- Restore only the original controller after draining jobs if rollback is needed; do not change live SSH or other workers.

## Source of truth

Working GitHub review branch: `docs/modular-mcp-chat-template-20261022`. This document and code are a bounded pilot, not proof that Matrix's general `dev_proposal` capability has changed from proposal-only.
