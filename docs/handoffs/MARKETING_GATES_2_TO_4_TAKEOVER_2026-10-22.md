# Marketing AI Gates 2–4 — live release log and takeover

**Date:** 2026-10-22 IST | **Project:** independent Business House AI Matrix.  
**Safety:** No publishing/spend, no Mac thermal limit bypass, no Firefox/user-tab termination, no root/SSH/router/Wi-Fi changes, no cross-project credentials.  
**Source of truth:** [Gate 1 certification](../receipts/MARKETING_GATE1_FINAL_EXPANSION_2026-10-22.md); [previous release gate baseline](../receipts/MARKETING_AI_RELEASE_GATES_2026-10-21.md).

## Initial status, 2026-10-22 01:16–01:20 IST

| Gate | State | Actual evidence / reason |
|---|---|---|
| Gate 1 — private SearXNG research, Trends, GSC | **PASS** | Prior signed Mac→Dell relay autonomous receipts, original Gate 1 certification. New Mac/Dell worker heartbeats online. |
| Gate 2 — 12-second original-asset preview under 68°C | **BLOCKED: thermal and opt-in render** | Mac Apple SMC TC0F **83.8°C**, fan **5808 RPM** at 01:16 IST; core package 79°C. Existing `render_enabled` key absent/false, safe fail-closed. Six independent `reel_bridge.mac_temperature_c()` readings across 10s: **60, 60, 62, 60, 78, 76°C**; cannot establish stable below-68°C headroom. No new render attempted. |
| Gate 3 — single unattended research→draft→edit→QA pilot | **PENDING/BLOCKED on Gate 2** | Source assets and worker available, signed research and eligible hosted free Groq model; cannot truthfully certify a newly rendered preview when thermal guard blocks and no rights/brand approval is recorded. |
| Gate 4 — extended 24h/reboot/fault soak | **FAIL/RESTART PRECONDITION BLOCKED** | Earlier `mac-thermal-soak-24h.service` already auto-aborted: `reason=cpu_92c_emergency`, peak **93.0°C**, only eight samples, unit failed after **55.289 seconds** on 2026-10-21. It is not a 24h run and must NOT be silently restarted under current temperatures. Earlier bounded Mac–Dell relay restart/recovery tests passed in Gate 1, not an extended soak. |

### Runtime inventory and supported controls

Mac: `mac-linux` worker online, `cron`, `generic-linux-automator`, `mbpfan`, `thermald` active. Apple SMC fan speed near max in earlier runs, repeated thermal spikes. Primary CPU load from existing personal Firefox content processes; **do not kill/unload user tabs without explicit user approval**. `/opt/business-house-matrix/marketing/brain/reel_bridge.py` is a monitored 100-second preview wrapper, no AI, fixed 12s/360px render with temp preflight cutoff min(70, config default 68) plus 2-second in-run abort; destination is fail-closed on existing output. Media batch `moksha-originals-20261021`: `guest.jpg` 67,344 bytes, `official-logo.jpg` 81,501 bytes, `sauna.jpg` 79,912 bytes; scan succeeded, no source licenses/human asset review verified by scan. Existing preview files under `marketing/reel-studio/smoke`, `ai-test`, `voice-test` are historical test outputs and cannot serve as evidence of a new Gate 2 Mac-owned run. Historical preview reports have `WATCH MORE` or placeholder outros and are **NOT** brand-ready.

Dell: `dell-linux` worker online, `bhm-research-relay`, `bhm-searxng`, `bhm-autonomy-controller` all active, SearXNG restricted to loopback `127.0.0.1:18889`; CPU package **47°C**, 5.5GB memory available, swap unused. Dell's cooler temperature alone cannot be used to falsely certify the expressly **Mac-owned Gate 2**.

Mac provider router: only previously owner-enrolled Groq free draft slots eligible; Cloudflare/OpenRouter/Gemini disabled. Marketing config shows `online_enabled=true`, `local_inference_enabled=false`, no `render_enabled` key (so preview rendering is DISABLED), `publish_enabled=false`, `spend_enabled=false`. Do not turn on heavy local inference. Mac prior 50/50 tests PASS; new test run and outputs documented below.

### Gate 2 preflight receipt

The original 2-minute Mac worker autonomously completed `reel_preflight` Brain job `83b5d71a-123f-4314-b2e3-319758d42c12` attempt 1, 0.005 sec, three-file media scan, render entrypoint exists, with max detected temperature **71°C**. Live independent six-sample thermal check `40a3dfc9-b9a9-46ff-b93f-c5298aee2d5e` terminal exit 0: **60, 60, 62, 60, 78, 76°C**, failed stable headroom requirement. No live render. Earlier SMC/soak findings SSH receipt `495edc19-6410-4ecd-916e-e8ddc33380ad`, exit 0; provider/asset/Dell status receipts `bc817a11-68f5-43b6-b4f0-cc54781aeff4`, `e352939a-ada1-40f7-9a55-1e052303d14a`, exit 0.

### Safe continuation / handover gates

1. **Do not render until** real Apple SMC and coretemp sample series are reliably below the **existing 68°C threshold**, with useful sustained headroom, host load manageable and `render_enabled` explicitly approved and safely toggled for a bounded preview only. Preserve existing monitored preview wrapper and keep `publish_enabled` false.
2. For any footage: verify original source ownership, contributor consent, trademark/official logo provenance, and brand review separately from `reel_preflight`. `reel_review` expressly returns `rights_verified=false,brand_reviewed=false`; don't override these booleans in code merely to mark PASS.
3. Gate 3 requires **one genuinely linked, unattended** private `research_brief` (paired relay + GSC + Trends) → qualified hosted free `hosted_draft` → real media selection → successful monitored MP4 export → actual ffprobe technical QC → rights/factual/brand review. No older smoke MP4 substitution, no automatic publication or paid vendor calls.
4. Gate 4 needs an authentic sustained soak/canary with long-window receipts, thermal-stop observation, credential/bridge stability, and reboot/interruption evidence where safe. Original **93°C thermal emergency is a failure** and precludes a heavy CPU stress restart now. A passive non-heating status observer may be launched for 24 hours separately; do not label it an active-load soak.
5. Log immutable Git SHA, new test counts, remote SSH terminal status and actual assets/QA, fail closed on unknown. Do not claim a future scheduled task already completed. Upon passing all gates, report status to user in this Matrix project alone; do not silently synchronize Moksha Master.

**Follow-on status updates will append to this file.**
