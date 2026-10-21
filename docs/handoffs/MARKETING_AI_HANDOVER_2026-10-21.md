# Marketing AI — next-chat execution handover

**Project:** Business House AI Matrix, independent from Moksha Master  
**Checkpoint:** 2026-10-21, Asia/Kolkata (last verified during 22:13–22:37 IST session)  
**Status:** Marketing Brain, routing, research on Dell, task queue and QA foundations function; **fully autonomous research-to-video MVP has NOT passed acceptance**.  
**Canonical public repo:** https://github.com/aarondash5-star/business-house-matrix  
**Next operator:** Read this entire file plus [Marketing current state](../MARKETING-CURRENT-STATE-2026-10-21.md), [SearXNG deployment](../RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md), [Autonomous MVP](../AUTONOMOUS-MVP-IMPLEMENTATION-2026-10-21.md), and [Matrix status](../STATUS.md) **before touching hosts**.

## Rules and boundaries

1. **Golden Rule 0:** Reuse the working implementations, existing installed libraries, services, task queues, integration contracts, and rollback snapshots. Do not rebuild, duplicate jobs, swap providers, or replace live integrations unnecessarily. Audit security, maintenance, license, compatibility, and cost before new dependencies.
2. Keep the **Business House Matrix separate from Moksha Master**. Moksha is an approved example creative/test subject, not permission to sync business databases, customer information, passwords, Master Registry data, or assets into the public Matrix repo.
3. Preserve existing SSH bridge, worker credentials, host/user gates, rollback snapshots, and saved task receipts. **Do not change root/sudo permissions, Wi-Fi, router, SSH, or access controls without explicit authorization for those changes.** Do not disable unrelated services. Never write secrets, uploaded photos, runtime JSON policy secrets, or SQLite/receipt databases into public GitHub.
4. **No publishing, ad spend, or automatic posting**. Keep `publish_enabled=false` and `spend_enabled=false`; all video is preview-only and requires rights, brand and human quality approval. Local Mac AI inference stays disabled after the observed 90°C incident. Maintain thermal limits; do not override the 68°C preview limit to make a test pass.
5. Source-driven free/open-source-first Matrix rule; no paid fallback or proprietary-service substitution without explicit user approval. SearXNG can encounter public search-engine rate limits; public search snippets remain untrusted evidence, not verified facts.
6. This is a **handover, not completion evidence**. On takeover, recheck both host heartbeats and completed receipts before mutations. An SSH response of `queued` is not success; poll `linux_task_status` until terminal `completed` and exit 0.

## Last verified live state

| Component | Evidence / state |
| --- | --- |
| Mac `mac-linux` / `KARAN` | Paired, online, SSH identity probe successful; Marketing runtime at `/opt/business-house-matrix/marketing/brain`; independent Reel Studio at `/opt/business-house-matrix/marketing/reel-studio` |
| Dell `dell-linux` / `karan-Inspiron-5379` | Paired, online, SSH identity probe successful; local SearXNG rootless Podman service `bhm-searxng.service` active and enabled |
| Research engine on Dell | Live `local_search.py` query returned 3 public results. Container exposes **127.0.0.1:18889**, no public interface |
| Mac ↔ Dell transport | **BLOCKED**. Mac Wi-Fi SSID `Andaz`, IP `192.168.0.106`; Dell SSID `andaz`, IP `192.168.0.103`. These are different networks despite overlapping `192.168.0.0/24` addresses; bidirectional ping/ARP failed and Mac-to-Dell TCP returned `No route to host`. Mac scan did not display lowercase Dell SSID |
| LAN gateway and Mac research | `bhm-searxng-gateway.service` was disabled/stopped after finding unsafe IP-only authentication across overlapping networks. **Do not simply start it**. Mac `searxng-search` slot remains disabled; research fallback via authenticated Dell SSH is presently human-supervised rather than an unattended Mac integration |
| Groq hosted planning / Trends | Previously verified live; Google Trends public RSS ingestion and cron, Groq hosted draft receipt; revalidate before new large runs. Tavily deprecated; do not reinstate |
| Mac Marketing Brain | **30/30** tests passed using Python `unittest`; durable SQLite queue, idempotency, bounded retries, receipts. `cron.service` active, existing worker every 2 minutes. One duplicate enqueue returned the *same* job id and a queued `ping` completed |
| Autonomous worker preview preflight | The existing Mac cron automatically consumed staged `reel_preflight` job `295bd56f-d635-4e53-85e7-cbd36244374e` at 2026-10-21 17:02:02 UTC and wrote `completed` receipt. Brain status showed **10 completed jobs** on this checkpoint |
| Real Moksha asset staging | From owner-connected Google Drive, three verified JPEGs (sauna photo, guest photo, source logo) staged privately at `/opt/business-house-matrix/marketing/brain/media-inbox/moksha-originals-20261021/`. Preflight passed file count, MIME and size checks. These are not present in public repo |
| Mac Reel Studio render | **NOT completed**: `reel_bridge.render()` refused preview when `mac_temperature_c()` was **75°C**, exceeding fixed **68°C** cutoff. Subsequent readings 76–78°C. Significant unrelated Firefox CPU/RAM workload seen; do not kill user tabs without approval |
| Separate preview artifact | A **12.83-second, 720×1280 H.264** Moksha draft was prepared outside the Mac pipeline using originals and supplied via previous conversation download. It was not published or put in GitHub. **Do not count this as proof of autonomous Mac editing**, and do not assume the prior conversation download is mountable in a new session |
| Recovery / restart | Dell SearXNG controlled restart completed; HTTP 200 returned on readiness attempt 5 after transient startup errors. Mac task idempotency and scheduler receipt confirmed; no lengthy disconnection/24-hour recovery certification yet |
| Publication and spend | Disabled. Local Mac inference also disabled. No changes to root/sudo, router, network credentials, or public access were made |

## Remaining gates — execute in dependency order

### P0 / Gate 1 — Private Mac ↔ Dell research transport

**Problem:** Two distinct, overlapping Wi-Fi networks; no direct route. Do not conflate a healthy cloud SSH bridge with LAN connectivity.

1. Read [SearXNG deployment](../RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md) and [reuse contract](../REUSABLE-RESEARCH-CONTRACT.md). Inspect both active network attachments, route tables, SSIDs/BSSIDs and identities read-only.
2. Prefer a **verified existing authenticated/private transport** or network admin-approved fix. Assess an SSH/overlay/tunnel only after checking host trust, least privilege, cost/licensing and automatic recovery. Do **not** expose `18888`/`18889` to WAN, use an unauthenticated IP-only gateway, or risk disconnecting the remote owner by blindly changing SSIDs.
3. Once transport is healthy, make a bounded Mac-initiated `/health` check and **actual JSON search** to the trusted Dell service. Confirm correct host identity, query source citation, rate limits, failure behavior, and service boot/reconnect persistence.
4. Only then review/backup Mac `provider-policy.json`, enable `searxng-search` and test a real `research_search` Brain job with a terminal receipt. No Tavily fallback or private research queries.
5. **Pass:** Mac Marketing Brain autonomously receives properly attributed SearXNG results with a safe persistent private link, verified after reconnect. Otherwise keep adapter disabled and log blocker.

### P0 / Gate 2 — Thermally safe real Reel Studio render

1. Inspect Mac `sensors`, `reel_bridge.mac_temperature_c()`, sustained CPU use, Firefox and other workloads, free memory and fan. Preserve existing user apps and services unless explicitly approved for closure. Do not run expensive local LLMs.
2. Review the existing Reel Studio entrypoint, isolated venv, tests, safety settings and staged footage. The actual Mac render is currently absent; do not create duplicate output in a nonempty destination.
3. With ambient/CPU state stable **below the existing 68°C cutoff**, execute a **bounded** `reel_bridge.render()` preview using `moksha-originals-20261021` and preview-only config. Guard stops in-run if too hot; respect any abort. Never raise the cutoff as a workaround.
4. Verify `report.json`, MP4 existence, `ffprobe` duration, resolution/orientation, nonempty audio/video characteristics, asset provenance, manual brand and factual accuracy, and `reel_bridge.review()`. Deliver an actual preview, with QA flags kept distinct from publishing permission.
5. **Pass:** Mac produces its own valid preview with thermal guard intact and no prior-output overwrite. If system remains too hot, report hardware/workload blocker rather than inventing a successful render.

### P1 / Gate 3 — One fully autonomous Moksha video pilot

1. Run one idempotency-keyed test in the **existing** Marketing Brain: public SearXNG/Trends evidence → Groq creative brief/concept → owner-approved, original footage/logo → Reel Studio editing → technical QC and source/rights/brand checks → finished preview for user approval.
2. No stock footage/images without verified reuse rights; do not invent Moksha physical-location visuals or claim that sauna/ice bath are somewhere else. Original user-provided footage is preferred. No auto-posting.
3. Capture stage IDs, transitions, timings, input provenance and terminal receipts. Check failed-stage retry/escalation without duplicating rendering or publishing.
4. **Pass:** A single unattended linked execution produces an authentic approved-for-review video, with a complete audit trail and no publication/spend. A separately manual draft does **not** pass.

### P1 / Gate 4 — Unattended operation and recovery certification

1. Test/review cron and systemd boot persistence, background service health, SearXNG readiness retries, Wi-Fi loss/reconnection, provider 429/timeout, SSH bridge interruption, stuck task recovery, deduplication and service restarts.
2. Run tests first with non-destructive synthetic/preview jobs. Record timeouts, max attempts, escalation and receipts. **Never replay an unknown-outcome mutation**; inspect prior receipt.
3. Run a bounded unattended soak of the connected path; require stable recovery evidence rather than counting a successful one-time command. Preserve thermal limits and do not reboot both hosts together without explicit approval.
4. **Pass:** Reconnects and restarts lead to recoverable, idempotent completed/failed receipts; no silent lost work, uncontrolled retry storms, unintended content publication or unsafe heat.

## Exact operator reference

Use connected **Generic Linux SSH** tools with `host_id: mac-linux` and `host_id: dell-linux`, first `linux_host_status` and `linux_probe`. For `linux_ssh_run`, capture the returned task UUID then inspect `linux_task_status`.

Read-only / benign checks:

```bash
# Mac -- existing nonroot executor
B=/opt/business-house-matrix/marketing/brain
python3 "$B/brain.py" health
python3 "$B/brain.py" status --verbose
cd "$B" && python3 -m unittest discover -p 'test_*.py' -v
python3 -c 'import sys;sys.path.insert(0,"/opt/business-house-matrix/marketing/brain");import reel_bridge;print(reel_bridge.mac_temperature_c())'
systemctl is-active cron.service
crontab -l
ip -br -4 addr
ip route

# Dell -- existing nonroot executor
systemctl --user is-active bhm-searxng.service
systemctl --user is-enabled bhm-searxng.service
podman ps --format '{{.Names}} {{.Status}} {{.Ports}}'
python3 /var/lib/generic-linux-automator-exec/matrix-searxng/local_search.py 'wellness sauna Goa' --limit 3
ss -ltn
```

Other relevant paths:
- Mac Marketing Brain and reel code: `/opt/business-house-matrix/marketing/brain/{brain.py,reel_bridge.py,searxng_research.py,router.py,provider-policy.json}` and `/opt/business-house-matrix/marketing/reel-studio/reel.py`.
- Mac private staged originals: `/opt/business-house-matrix/marketing/brain/media-inbox/moksha-originals-20261021/`; private output area `/opt/business-house-matrix/marketing/brain/renders/`.
- Dell SearXNG: `/var/lib/generic-linux-automator-exec/matrix-searxng/`, image `ghcr.io/searxng/searxng:2026.10.19-81371861f`, `127.0.0.1:18889`.
- Durable Dev/Matrix scheduler: `bhm-autonomy-controller.service` on Dell (different from Mac Marketing cron). Do not replace one with the other.
- Portable SSH plugin skills: `skills/matrix-autonomous-mvp/SKILL.md` and `skills/selfhosted-searxng-research/SKILL.md` in this repository; existing plugin skills were previously released but **no update/re-release is implied by this documentation commit**.

## Explicit non-goals for handover

Do not install LibreChat or OpenClaw as part of this Marketing task. Do not roll out broader Matrix architecture, switch model vendors, publish social posts, trigger advertising, create a paid subscription, reset Wi-Fi, change root privileges, or synchronize Moksha Master. Keep scope to four release gates.

## Deliverables expected from the next chat

- Actual outcomes for Gates 1–4, each **PASS / BLOCKED / NOT TESTED** with dated live receipts and concrete blocker.
- A real playable Mac-produced Moksha preview (if thermal/safety gates permit), with proper QA and no automatic publication.
- Updated [current state](../MARKETING-CURRENT-STATE-2026-10-21.md), [status](../STATUS.md) and this handover when substantive states change; commit SHA and GitHub readback.
- No premature statement that the autonomous MVP is fully finished.

## Copy/paste prompt for the next chat

> Continue the **independent Business House AI Matrix Marketing AI MVP** from this handover: https://github.com/aarondash5-star/business-house-matrix/blob/main/docs/handoffs/MARKETING_AI_HANDOVER_2026-10-21.md . First use the connected GitHub app to read the **entire** handover, the linked Marketing current-state document and SearXNG architecture. Use the connected Generic Linux SSH app to verify the live Mac and Dell state (host heartbeat and terminal receipts) before actions. Follow Golden Rule 0; reuse all existing services, code, queues, skills, assets and safety gates. Execute remaining gates in order: (1) secure persistent Mac-to-Dell research, (2) thermally safe real Mac render, (3) one unattended real-asset Moksha research-to-video-and-QA pilot, (4) restart/reconnect/retry/soak certification. Do not change Wi-Fi, router, SSH/root privileges without my explicit approval; do not override thermal guards; do not publish or spend. Keep Business House Matrix independent from Moksha Master. Update GitHub documents and report verified PASS/BLOCKED outcomes with exact job receipts.


## Next-chat update — 2026-10-21 22:45–22:54 IST takeover receipts

**New canonical receipt index:** [Live 4-gate evidence](../receipts/MARKETING_AI_RELEASE_GATES_2026-10-21.md). All four gates remain open. The earlier instructions and restrictions in this handover still apply.

| Gate | Latest live result | Consequence |
| --- | --- | --- |
| 1. Authenticated private Mac→Dell search | **BLOCKED** — Mac curl health HTTP 000/timeout, ARP failed; different SSIDs and no existing approved overlay. Dell localhost search works; gateway OFF; Mac slot OFF | Need safe approved private transport and new Mac-origin JSON search before policy enable |
| 2. Thermally safe Reel Studio render | **BLOCKED** — Mac hottest SMC 77°C then 75°C > 68°C limit; three real photos preflight PASS; no real Mac MP4 | Wait for sustainable safe heat conditions without killing user processes or changing thermal cutoff |
| 3. Single linked autonomous video | **BLOCKED/NOT RUN** — no end-to-end research-to-render path yet | No duplicate video pilot or fabricated approval |
| 4. Reconnect/restart/retry/soak | **PARTIAL** — Mac tests 30/30, Dell controller and sandbox tests pass, two unique jobs each deduplicate and complete unattended; 24h/fault soak NOT TESTED | Continue only safe bounded recovery drills after dependency repair |

**New terminal job receipts:** Mac marketing `ping` `881a4f47-646c-4565-a2eb-7bc822a3729c` completed first attempt at 17:22:01Z via original 2-minute cron; Brain count rose 10→11. Dell central `research_search` `8f39e7eb-4fa7-45fa-a800-19ad7b423716` completed first attempt at 17:20:58Z with 5 attributed public results; second identical submission reported `deduplicated=true`. Both authenticated Linux probe task receipts finished with exit 0. Dell bridge heartbeat became stale once and automatically recovered, and a previously queued read-only check returned terminal completed/exit 0 without resubmission. Journal access for Dell user service insufficient; no permissions were changed.

**Safety continuity:** No changes to code, network, root/sudo, SSH permission, fan, thermal guard, published channel, spend, model vendors or project data boundaries. No Mac render was forced. The evidence file indexes precise host check UUIDs and job IDs without storing photos, secrets, or runtime databases. 

## Immediate next-chat progress — 2026-10-21 ~23:20 IST

**Permanent device handshake / transport established and live tested.** The former cross-SSID LAN problem is bypassed *without altering the LAN* using separately scoped, encrypted, signed **outbound** HTTPS research relay on the already owner-operated Supabase bridge. Do NOT rework/re-pair anything. [Full source/runbook/receipts](../../research/paired-relay/README.md).

**Completed:**
- Both Mac/Dell generated stable local Ed25519+Curve25519 credentials and cross-pinned verified public keys; no private key export or human PIN reuse.
- New owner-only `bhm_research_*` queue (deny-all RLS for non-service roles), `bhm-research-relay` Edge Function v2, Dell nonroot boot-enabled `bhm-research-relay.service`. Existing SearXNG still localhost-only.
- Two actual end-to-end Mac-origin, Dell SearXNG, encrypted signed search results, request IDs `dc1ede2b-d686-43fe-b236-c04bd66d1b11`, `0d929763-667f-44d7-a9c3-955753b2da3d`; second passed after only the research service was restarted. Unauthorized signed API negative check returned HTTP 401.
- Existing `marketing/mac-brain/searxng_research.py` source updated for opt-in relay and Mac live source deployed after backup; Mac regression 30/30 PASS in still-disabled router mode.

**Remaining Gate 1 substep:** Mac `provider-policy.json` `searxng-search.enabled=false` *remains OFF* (direct policy write was blocked by execution controls). Select a supported/approved policy activation that includes `transport=encrypted_signed_relay_v1`, preserve quotas and other safeguards, enqueue one `research_search` via existing Brain and wait for an autonomous cron completed receipt. Do NOT bypass a policy/tool gate. Then do longitudinal/reboot verification. Gates 2–4 do not become PASS just because transport works.

No root, Wi-Fi, router, generic SSH shell gate, publishing, spending, browser PIN/OTP mechanism, or Moksha Master business data was modified.
