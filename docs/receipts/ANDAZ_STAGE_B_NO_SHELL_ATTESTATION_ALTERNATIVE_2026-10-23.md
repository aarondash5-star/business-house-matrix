# Andaz Marketing Brain — supported Stage B alternative to blocked Mac shell preflight

**Date:** 2026-10-23 IST. **Disposition:** SOURCE-ONLY ALTERNATIVE PREPARED / OFFLINE TESTED; **NOT LIVE, NOT A SAFETY BYPASS, NOT STAGE B CERTIFIED**.

## Reason for change
- Stage B Mac `linux_development_run` preflight failed **before the Mac worker received a task**: `This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.`
- The specific Generic SSH Linux ChatGPT plugin was already configured with **Allow all actions**. User consent, transport pairing, and online heartbeat do **not** override platform safety protection.
- Official guidance: [OpenAI troubleshooting for plugins/apps](https://help.openai.com/en/articles/20001497-troubleshooting-plugins-and-apps-in-chatgpt) explicitly says some tool requests are denied without an approval prompt, and changing app permissions or saved approval does not override safety protection. [OpenAI Support response on erroneous read-only MCP blocks](https://community.openai.com/t/chatgpt-app-mcp-tool-calls-blocked-by-openai-safety-checks-before-reaching-mcp-server/1386059/24) describes ongoing investigation and requests the failure time, connector, conversation/request ID, and whether the server received the invocation.
- No trace ID or internal rule is available. **No alternative SSH lane, browser automation, root path or split-command retry is authorized.**

## Prepared bounded architecture (draft PR #4 branch only)
- [Offline Mac preflight attestation verifier](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/marketing/andaz_stageb_fixed_attestation.py).
- [Offline verifier regression tests](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/marketing/test_andaz_stageb_fixed_attestation.py).
- Instead of accepting an arbitrary shell command, a **future security-reviewed fixed-function connector action** would return a small signed JSON attestation from the existing authorized Mac identity with:
  - Required host identifier `mac-linux`, freshness window no more than five minutes and caller nonce;
  - Only the existing Marketing Brain queue timer state (must be `active`);
  - SHA-256 fingerprints under exactly three fixed labels: `marketing_report_orchestrator.py`, `searxng_research.py`, and `matrix-research-transport/transport.py`;
  - Explicit `extract_gate_active=false`, `publish_enabled=false` and `spend_enabled=false`;
  - Ed25519 signature verified against an **independently pinned, already approved Mac public key**. No incoming key substitution.
- Proposed verifier has no SSH, subprocess, OS command, website access, credential loading, identity enrollment, URL grant mutation, shell or publishing functionality. It rejects extra fields, arbitrary file labels, stale/mismatched nonce, wrong host, invalid digest, signature forgery, unsafe flags and active extraction.
- Output is deliberately `preflight_evidence_only`, `stage_b_certified=false`, `extract_allowed=false`, `source_permissions_granted=false`, `publish_allowed=false`. This **cannot authorize a deployment**.
- The corresponding Mac-side fixed-function attestor **has not been built or installed** and should be implemented only as a separately reviewed connector capability. A new connector action is not exempt from platform safety checks.

## Offline QA receipt and limits
- Source/test code committed to existing **unmerged** `feat/marketing-research-engine-20261022` branch (draft PR #4).
- Local isolated Python + OSI-open-source `cryptography` 46.0.4 test run: **14/14 passed**, exit 0. Coverage: valid signed evidence remains non-authorizing, mutated signature, wrong pinned key, wrong host, wrong/stale/future nonce/timestamp, timer down, arbitrary or secret-bearing fields, extraction already active, publishing/spending flags, invalid hash and malformed envelope.
- Local test run does **not** represent tests on Mac, Dell, Generic SSH, the live relay, any real reviewer, robots.txt, or live extraction. GitHub CI and host terminal receipts were **not** run for these new files; don't confuse local tests with release certification.

## Remediation / secure transition checklist
1. Ask OpenAI Support to inspect the denied Mac `linux_development_run` call around **2026-10-22 20:04 UTC (23 Oct 01:34 IST)**, with the exact error, connector name, account/workspace and absence of any worker task ID. The Dell comparison task `3d58e1b6-df42-4513-a4c1-043ea3513178` completed successfully, but does not clear the Mac call.
2. Have the connector/security owner formally review the fixed-function attestation contract and propose a distinct constrained action through the established plugin release/approval process. Explicitly prohibit arbitrary shell input; use only existing paired identity signing after its custody/authorization is verified. Do **not** deploy solely on the basis of this source-only prototype.
3. Independently verify robots/terms for exactly `https://www.happypandahostel.com/` and `https://thepeacehostel.in/`. Previous `robots.txt` reads were inaccessible and remain unknown, not permissive.
4. Vet and enroll a real human reviewer with revocation/audit trail, and check the transport source fingerprints/backups and all connector safety gates using an approved tool. Any rejection means STOP, not alternate-route execution.
5. Only if those conditions pass, seek an explicit Stage B implementation/security release and run one source at a time with bounded signed receipts plus negative security checks. No OTA login, broader URLs, root access, spending, publishing, merging or production change without new approval.

## Support-ready issue text
**Subject:** Generic SSH Linux plugin — pre-execution safety denial on a read-only Mac development preflight

**Details:** On 2026-10-22 around 20:04 UTC, a ChatGPT text conversation invoked the `linux_development_run` action with `host_id=mac-linux` to check the existing Marketing Brain queue timer, LangGraph marker and signed transport file metadata. The platform returned `This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.` No Mac worker job ID, stderr or terminal receipt exists. The Mac host was paired/online; Dell's separate read-only preflight completed as task `3d58e1b6-df42-4513-a4c1-043ea3513178`. ChatGPT plugin-specific permission was already `Allow all actions`; no policy ID or diagnostic trace was exposed. Please supply the denial category/request trace and supported remediation for a least-privilege, fixed-schema health/fingerprint attestation. **We have not bypassed the blocked action or changed live permissions or services.** Redact secrets and private paths from any screenshots.

**Final:** This path prepares a safe **replacement design**, not a workaround that evades platform protections. Stage B remains BLOCKED until approved tools and source-policy gates succeed.
