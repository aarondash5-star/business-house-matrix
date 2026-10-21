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

## Major step 2 — Linked Gate 3 pilot software delivered and tested

- Reused existing Brain queue, authenticated encrypted SearXNG, Google Trends RSS, authenticated read-only Engagement Core GSC import, confirmed hosted free model and original media inbox; **no new daemon/model/API/vendor/paid plan**.
- New `marketing/mac-brain/pilot_pipeline.py` source commit `9a0dc15682b9d92747bd7814e38f343e0f3f6e7f`. New `reel_pilot` Brain task and validation commit `c8fba3da932cb9c11fc08983286c0eff1ef21d33`. New tests `test_pilot_pipeline.py` in commits `33ebc38b49d35354a91fa1ae695c4cbf2875a176`, `1971ffdf3d1a4f8384d8bee037284205f6c4ae05`.
- Pipeline is a **single idempotent job**: safe media scan → source-attributed verified paired `unified_research.collect` → sends ONLY public source titles and sanitized HTTPS links (never GSC queries/metrics) to already-enrolled zero-paid hosted creative API → records concept DRAFT → checks explicit `render_enabled` and, if enabled, five temperature samples and original `reel_bridge.render` in-run guard → calls technical review → ALWAYS leaves human rights and brand approval false, no publishing.
- Mac deployed `brain.py`, `pilot_pipeline.py`, test file with original Brain backed up as `brain.py.pre-gate3-pilot-20261022`; preflight/production checks **57/57 regression tests PASS** (SSH `82899da7-236a-4aab-9a62-0dc4470bd600`, completed exit 0).
- Production scheduled-job ID `02904304-941d-4d66-9477-c1c96542a88f`, idempotency key `marketing-gate3-linked-pilot-20261022-001`. **Autonomously completed** by existing Mac 2-minute cron at **2026-10-21 19:56:10 UTC** on attempt 1 (8.631s). Research PASS: four verified public signed SearXNG sources; GSC observed; Trends no relevant topic in its cache. Creative DRAFT READY using already confirmed Free Groq `openai/gpt-oss-120b`. Final explicit pipeline state **BLOCKED_RENDER_DISABLED** because `render_enabled` is not opted-in in existing Mac Brain config. `video_produced=false`, `published=false`, `paid=false`. No fake MP4, no brand or rights signoff. Post-readback SSH `7e2ba775-9798-4f39-ac23-36afecb5c737`, completed exit 0. Brain completed queue advanced to **17**.
- Gate 3 verdict **SOFTWARE RESEARCH+DRAFT CHAIN PASS; FULL FINISHED VIDEO NOT CERTIFIED**. Gate 2 remains blocked because six earlier thermometer readings varied 60→78°C under a 68°C cutoff, and original active thermal soak already failed at 93°C.

## Major step 3 — Non-invasive 24h Gate 4 passive observer started

- New stdlib-only `marketing/mac-brain/passive_soak.py` at source commit `b16180fa7abe7b48011092fa3b9cccef413049eb`, `test_passive_soak.py` at `f1d987ebaac3b293c5600ba94f1b867744b6fd3d`. Runs **passive read-only** 5-minute sensor/fan/load/service samples; no synthetic CPU stress and no Wi-Fi, fan, SSH or app changes. Writes owner-only `data/gate4/passive-20261022-soak/status.json` and `samples.csv` (0600) and never reports an active-load PASS.
- Deployed on `mac-linux` using pinned GitHub commit; full **62/62 Mac regression tests PASS**, SSH `41f5bd98-197b-4f49-ac30-a516a0950f56` terminal completed exit 0.
- Started low-priority isolated existing-user transient systemd unit `bhm-marketing-gate4-passive.service` at **2026-10-21 19:58:07 UTC / 22 Oct 01:28:07 IST**, configured `RuntimeMaxSec=87300`, `NoNewPrivileges=true`, `PrivateTmp=true`, `MemoryMax=80M`, 300-second sample spacing. `generic-auto-exec` already had user `Linger=yes` from prior OAuth user-service handling, so no new root/permission change.
- First *independently read* status: `state=running`, `kind=passive_no_load`, `samples=1`, `max_observed_c=80.0`, `service_failures=0`, `thermal_emergency=false`, `result=NOT_CERTIFIED`. All four protected services initially active. SSH start receipt `54f05e4b-883a-42f6-b43f-e2396a75e1d6`, terminal exit 0, and separate readback `7e2ba775-9798-4f39-ac23-36afecb5c737` terminal exit 0.
- **The old active-load Mac soak is permanently recorded FAILED**, peak 93°C with emergency abort after ~55 s. Do NOT restart active load or claim the *new passive* telemetry means Gate 4 pass. After 24h (no earlier than **2026-10-22 19:58:07 UTC / 2026-10-23 01:28 IST**), verify elapsed wall clock, sample continuity, service gaps and temp ranges; label **passive observation only**, not full Gate 4.
- Existing ChatGPT task limit prevents a sixth active automation. The already-active one-time **Mac 24h Thermal Test Review** was safely re-targeted to **Matrix Gate 4 Audit**, scheduled **2026-10-22T20:10:44 UTC / 2026-10-23 01:40:44 IST**, to audit both the old failure and this passive log, update this handoff and notify accurately. No additional active slot consumed. Existing daily GSC sync remains enabled.

## Current final gates and operator takeover decision

| Gate | Strict outcome | Next required real evidence |
|---|---|---|
| 1 — authenticated research, Trends and GSC evidence | **PASS** | Check first GSC daily scheduled automation receipt separately; not part of original certified paired research |
| 2 — newly Mac-rendered 12-sec technical preview | **BLOCKED / NOT RENDERED** | Stabilize **below 68°C with headroom**, safely authorize preview via existing config or explicitly ephemeral audited override without removing temperature checks, run `reel_bridge.render` at 12s/360px with in-run abort and verify real MP4, `ffprobe`, `report.json` |
| 3 — one unattended full creative workflow | **PARTIAL SOFTWARE PASS / VIDEO BLOCKED** | Existing `reel_pilot` produced 4 valid research citations and Groq draft; needs thermal-safe genuinely new preview, technical QA, and separate asset-rights / brand / factual signoff; never recycle smoke media |
| 4 — full 24h/resilience/reboot/fault proof | **FAIL for old active-load soak / ongoing passive observation only** | First passive telemetry observation completes 24h, then only undertake controlled active/reboot/load faults if Mac has actual thermal stability, maintenance window, retained sessions and explicit safe approval |

### Quick takeover commands

```bash
B=/opt/business-house-matrix/marketing/brain
python3 "$B/brain.py" receipt 02904304-941d-4d66-9477-c1c96542a88f
python3 "$B/brain.py" status --verbose
python3 "$B/passive_soak.py" status passive-20261022-soak
systemctl --user status bhm-marketing-gate4-passive.service --no-pager
cat /var/lib/mac-thermal-soak/status.json
python3 -m unittest discover -s "$B" -p 'test_*.py' -q
python3 - <<'PY'
import sys
sys.path.insert(0,'/opt/business-house-matrix/marketing/brain')
import reel_bridge
print(reel_bridge.mac_temperature_c())
PY
```

**Takeover rules:** Do not rerun the pilot under a new key just to rack up jobs. If unknown result or suspended SSH task, inspect original immutable receipt before any retry. Review media source consent/rights and approved official logo separately. Never set `render_enabled=true` while the thermal readings spike to 78–84°C and never alter 68°C guard/fan/PID settings as a shortcut. Existing Firefox multi-tab user browsing is a source of substantial CPU load; don't close tabs or kill parent process without owner permission. Dell cooler ~47°C is NOT proof Mac Gate 2 passed. No source or password sync to Moksha Master; keep this independent.

## Status-log index

| UTC time | Milestone | Result | Main receipt |
|---|---|---|---|
| 19:46 | Mac hardware/soak baseline | 83.8°C SMC, prior soak 93°C abort | `495edc19-6410-4ecd-916e-e8ddc33380ad` |
| 19:47 | Mac source inventory, Dell research state | Three local images; Dell relay/SEARXNG/controller active | `bc817a11-68f5-43b6-b4f0-cc54781aeff4`, `e352939a-ada1-40f7-9a55-1e052303d14a` |
| 19:49 | Mac thermal stability series | 60,60,62,60,78,76°C — **FAIL 68°C stable cutoff** | `40a3dfc9-b9a9-46ff-b93f-c5298aee2d5e` |
| 19:55 | Linked pilot deployed | **57/57 tests** | `82899da7-236a-4aab-9a62-0dc4470bd600` |
| 19:56 | Unattended pilot run | 4 signed sources + GSC + hosted Groq draft, blocked before render | Brain job `02904304-941d-4d66-9477-c1c96542a88f` |
| 19:57 | Passive observer deployed | **62/62 tests** | `41f5bd98-197b-4f49-ac30-a516a0950f56` |
| 19:58 | Passive 24hr monitor started | Running, first sample 80°C, no service gaps, no CPU load | `54f05e4b-883a-42f6-b43f-e2396a75e1d6` |
| 20:00 | Follow-up audit reuse | Existing one-time task rescheduled for 24h+ review | `Matrix Gate 4 Audit` |

**Never label a queued/scheduled job as a passed final test.** The original Gate 1 is **certified**; Gates 2/3/4 have the explicit state shown above.


## Updated 2026-10-22 01:36–01:48 IST — owner-authorized Mac workload cleanup + actual video rendering

**User authorization:** "kill all heavy mac tasks and try rendering"; owner reconfirmed existing root access and directed use of documented Generic Linux SSH permissions. Read authenticated production docs in \`karanzing1992/engagement-core/docs/GENERIC_SSH_THREE_LANES_ROLLOUT_20261021.md\` and \`GENERIC_SSH_MCP_SCHEMA_PLUGIN_RELEASE_20261022.md\`: both Mac and Dell retain passwordless root via \`generic-auto-exec\` sudo, and six-lane authenticated SSH schema. Verified live \`sudo -n /usr/bin/id -u\` returned **0** on Mac. **No sudoers, authentication or bridge permission changes.**

### 1. Before cleanup

At 01:36 IST Mac had ~**82.8°C** SMC TC0F, ~**77°C** core package, **6496 RPM** fan, two large Firefox isolated web content processes (verified PIDs **4923** ~2.4GB and **134336** ~1.0GB RSS) and main desktop Firefox process **4669**. The two children cumulatively accounted for high CPU; numbers from \`ps\` represent cumulative process activity rather than point-in-time utilization. All four protected Mac services (\`generic-linux-automator\`, \`cron\`, \`mbpfan\`, \`thermald\`) ACTIVE, passive Gate4 observer active.

Initial overly strict \`sudo -n -u karan true\` permission probe failed, despite working root sudo. After root access confirmed, first Python PID validator correctly did not kill anyone because Firefox exposed a *single combined cmdline* and the code incorrectly checked \`b'-contentproc' in args\`. An inspection verified both were genuine \`karan\`-owned Firefox content children. A subsequent root Python script correctly validated uid=1000, exact \`/usr/lib/firefox/firefox-bin\`, and both \`-contentproc\` and \`-parentPid 4669\` in the cmdline before issuing **SIGTERM to exactly those two PIDs**. **Termination successful**, terminal SSH receipt \`fa0dbbc8-fec8-44d8-8e17-8a1c137492e3\` exit 0; no \`kill -9\`, privilege grant, unrelated PID termination or signal to SSH workers. Remaining Firefox processes also exited following child terminations; the user's browser session may need reopening and tab restoration.

After cleanup: **5.3 GiB available RAM**, 591 MiB swap used; 8 SMC max series **69,55,55,54,53,53,53,53°C**, fan ~3993 RPM and package ~53°C. No cooling or sensor threshold changes.

### 2. Preview render trials

The owner approved a render attempt. Scope: preview only, **never publish or spend**, original 3 already-staged files \`guest.jpg\`, \`sauna.jpg\`, \`official-logo.jpg\`, 228,757 bytes. Existing \`reel_bridge.render\` protects output with real-time \`mac_temperature_c\` read, **68°C cutoff**, forced preview-only \`--no-ai\` original Reel Studio, 100s bounded subprocess, periodic in-run abort. Render permission \`render_enabled\` was supplied **in memory to exactly this call**; persistent \`brain/config.json\` unchanged, publish/spend still false.

1. **Initial monitored Mac render**: 6 preflight readings 52,52,55,52,52,51°C. ffmpeg began encoding, but in-run sensor tripped the unchanged 68°C cutoff. The wrapper killed its child process group, returned \`Reel preview stopped by in-run thermal monitor\`, terminal Mac SSH task \`b48d7695-41eb-4f32-82fc-88f5a4cfb6bc\` **failed**, exit 6. Partial segments existed, no report or complete MP4. **Not certified as successful video.**
2. First CPU-affinity retry was **blocked before encoding** due one 62°C headroom spike while using stricter self-imposed 60°C stable target; task \`915da001-4572-44f0-b20c-8a54cfafd88a\` exit 7, no files moved or overwritten.
3. **Success, CPU-constrained retry**: used Linux \`nice -n 19 taskset -c 0\` to restrict one invocation and inherited child FFmpeg processes to **one CPU core** with lower scheduling priority. Six preflight max SMC readings **48°C consistently**, and original 68°C in-run emergency guard retained. Preserved first aborted attempt's partial files in a separate owner-private archive \`renders/moksha-originals-20261021.failed-thermal-attempt1-20261022\` via atomic rename; original 3 private source images untouched. Render completed: **9.6 seconds, 360 × 640 vertical MP4**, 3 staged source images, \`reel_bridge.review\` returned \`technical_checks_passed=true\`, \`preview_only=true\`, \`vertical=true\`, \`has_video=true\`, \`duration_sensible=true\`. New MP4 path: \`/opt/business-house-matrix/marketing/brain/renders/moksha-originals-20261021/reel_preview.mp4\`. **No publication**; \`not_generic_outro=false\` (ends in "WATCH MORE"), \`rights_verified=false\`, \`brand_reviewed=false\`. State \`DRAFT_NEEDS_HUMAN_QA\`, so **NOT publication-ready**. Post-render Mac max sensor **69°C**; in-run guardian did not trip at its sampled intervals. Success **terminal development-lane SSH receipt \`a088c739-4468-4fa2-94de-87696fbb1443\` exit 0**, message \`GATE2_PREVIEW_RENDER_TECHNICAL_PASS\`. This proves a low-load actual Mac-owned MP4 was produced; **not** unattended end-to-end Gate3 nor 24h thermal load stability.

### 3. Independent ffprobe and bridge outage — unresolved

A subsequent **read-only** \`ffprobe\`, SHA-256, file stat, renderer report readback and idempotent Mac \`reel_review\` enqueue was queued on original operations SSH lane as **\`f18b10b2-b295-4950-aef4-bf04fa12ce77\`**. It was still \`running\` without stdout/exit status when all three Mac lane heartbeats fell offline; Mac \`linux_host_status\` at **2026-10-21 20:17:32 UTC** returned \`online=false, age_seconds=77\`. Dell SSH still ONLINE. Independent control lane request rejected \`Requested SSH lane offline; no job queued\`. **Do not replay that in-flight idempotent operation until its terminal receipt is known.** There is no evidence that ffprobe finished, despite the earlier renderer's embedded ffprobe and review succeeding. The fault cause (Wi-Fi, sleep, bridge, host shutdown, etc.) has NOT been established. This new bridge interruption is **Gate4 resilience evidence requiring separate recovery diagnosis**, not a certification success.

### 4. Current release verdict / next actions

| Gate | Status after cleanup | Evidence |
| --- | --- | --- |
| Gate 1 | **PASS**, existing certification | Research relay independently certified. New Mac worker outage prevents claiming *current* uptime, does not erase historical receipts. |
| Gate 2 | **MONITORED PREVIEW RENDER PASS; FINAL RELEASE QA PENDING** | New 9.6s vertical MP4, monitored/single-core, no publish. Formal manual brand, asset rights and generic outro correction needed; ffprobe independent follow-up delayed by Mac outage. |
| Gate 3 | **PARTIAL** | Autonomous signed research + hosted concept had earlier completed with \`BLOCKED_RENDER_DISABLED\`; a **separate supervised** render succeeded, not one continuously linked autonomous video/QA job. |
| Gate 4 | **NOT CERTIFIED** | Old active 24h soak failed at 93°C after 55s. Passive service had been running, but is currently not observable through SSH due Mac offline. Reboot/network recoveries not independently verified. |

**Takeover commands after Mac restored (READ ONLY first):**

\`\`\`bash
B=/opt/business-house-matrix/marketing/brain
python3 "$B/brain.py" status --verbose
python3 "$B/passive_soak.py" status passive-20261022-soak
stat "$B/renders/moksha-originals-20261021/reel_preview.mp4"
ffprobe -v error -show_entries format=duration,size,bit_rate -show_entries stream=codec_name,codec_type,width,height -of json "$B/renders/moksha-originals-20261021/reel_preview.mp4"
python3 "$B/brain.py" receipt 02904304-941d-4d66-9477-c1c96542a88f
sensors | grep -E 'Exhaust|TC0F:|Package id 0:'
systemctl is-active generic-linux-automator.service cron.service mbpfan.service thermald.service
\`\`\`

Check Mac host heartbeat first and recover only according to [existing certified SSH runbook](https://github.com/karanzing1992/engagement-core/blob/main/docs/GENERIC_SSH_THREE_LANES_ROLLOUT_20261021.md). Do **not** duplicate unknown in-flight task \`f18b10b2-b295-4950-aef4-bf04fa12ce77\`, delete the new video, repeat renderer, change cooler/fan/thermal guard, claim human rights approval or publish. Browser reopening/tab restore may be needed by the desktop owner. Additional user-approved production creative review and 24h safety/load evidence remain necessary.
