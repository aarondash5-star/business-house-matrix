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
