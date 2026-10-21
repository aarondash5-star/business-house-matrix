# Current Business House AI Matrix rollout status

**Matrix-wide baseline:** 2026-10-18; **Marketing checkpoint verified:** 2026-10-21

| Stage | State |
|---|---|
| Architecture | Approved: Open WebUI, LangGraph, Temporal, FastMCP/ContextForge, Ollama, PostgreSQL, EVOLUTION |
| GitHub migration | Complete: public `aarondash5-star/business-house-matrix`, original Git history preserved |
| CI / public-repository safety | Proposed in branch `ci/cloud-readiness-20261018`; verify PR checks before merging |
| Oracle Always Free | Target selected; tenancy, identity and capacity not yet verified |
| Google Cloud Run | Backup target selected; Matrix identity and free quota not yet verified |
| Open WebUI runtime | Not deployed |
| LangGraph | Starter simulation only; no live model or tools |
| Temporal / MCP | Planned, not connected |
| OpenClaw | Deferred until pilot acceptance |

Next exit gate: passing, reviewed GitHub validation checks. Next required external decision: which separately authorized cloud tenancy/project to use, and verify its actual free capacity before any deployment.


## Marketing Department — verified 2026-10-21

For accurate Marketing facts use **[current-state handoff](MARKETING-CURRENT-STATE-2026-10-21.md)**; chronological records appear in [Phase 1](MAC-MARKETING-PHASE1.md) and [API router](MAC-MARKETING-API-ROUTER.md).

- Mac Marketing Brain: isolated SQLite autonomous queue, cron runner and receipts functioning; **5 completed jobs** at verification.
- Groq: **GPT-OSS 120B and Qwen3.8 27B authenticated and live**, including end-to-end Marketing Brain job; **2 recorded local API requests**, shared conservative cap 40/day.
- **11 passing regression tests** (7 provider-router + 4 Brain) on Mac; Generic Linux SSH, cron and Ollama active.
- Tavily and Gemini **registered but disabled**; Gemini has proprietary licensing conflict with Matrix's open-source rule. Cloudflare/OpenRouter configured but disabled.
- No live video pipeline integration or ready-to-publish autonomous output yet; existing Reel Studio is present.
- Local creative inference disabled after ~90°C test; social publishing and spending disabled.
- Next stage: QA-gated Reel Studio integration using real footage, then Tavily research connector and controlled provider expansion.

The earlier Matrix-wide pilot status above remains independently tracked. No Open WebUI/Temporal/MCP production deployment is implied by Marketing's successful Groq pilot.


## Research engine change — 2026-10-21
- Tavily **deprecated**: removed from operational Mac research provider registry and Brain imports; old code/database archived locally.
- Dell self-hosted rootless **SearXNG live and boot-persistent**; native and Dell-local CLI search verified.
- Mac replacement client and task connection deployed, **disabled pending private reachability**. Wi-Fi hosts cannot ARP each other; Mac-to-Dell SSH and TCP failed before gateway. No public endpoint exposed.
- [Detailed rollout, safety, blocker, restart and rollback](RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md).


## SearXNG correction and Dell Dev expansion — 2026-10-21
- Dell SearXNG remains available at **localhost only** and starts at boot. LAN gateway was disabled as the network is two DIFFERENT SSIDs/routers (`andaz` vs `Andaz`) using overlapping `192.168.0.0/24` private ranges; do not claim Mac-to-Dell access works.
- **Dev Brain research integrated and tested:** `matrix-brain research-search`, optional public `--research-query` and evidence-containing LangGraph research node, with source receipts. Existing queue retained. No model-directed search, repository edit or paid API.
- Mac Marketing Brain SearXNG still disabled until trusted inter-network connectivity is established; Tavily remains retired.
- Full details: [Deployment and Dev integration](RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md).

## Cross-project research skill release — 2026-10-21
- Published **private Generic Linux SSH MCP plugin v0.1.17**, release `pluginrel_6ad8b8350ef88191b4fec49bb4f876f9`, with new discovered skill `selfhosted-searxng-research` and updated README. Verified plugin file list confirms all existing skills preserved.
- User-facing plugin: https://chatgpt.com/plugins/plugins_6ad64adab5e481918832cd516e779009 .
- Portable repo skill: [SearXNG Research Skill](../skills/selfhosted-searxng-research/SKILL.md); stable [reusable research contract](REUSABLE-RESEARCH-CONTRACT.md) and [JSON response schema](../research/contracts/searxng-search-response-v1.schema.json).
- Cross-project reuse is **documentation and safe calling guidance**, not automatic enablement, new MCP tools, project-data sync or additional machine privileges.
- Dell local SearXNG search remains live. Mac SearXNG adapter remains disabled because machines are on separate Wi-Fi networks; host-private gateway stopped. Dev Brain query works locally via authorized SSH.
- The installed plugin's root/sudo owner-approval skill remains unchanged; no root/sudo policy edits performed with this plugin release.


## 2026-10-21 — Verified Dev research completion
SearXNG-supported Dell Dev Brain job `cad4904e-7aec-4678-ad71-d170ad2c4841` completed with `review_passed`, a saved source-evidence file, plan, implementation, review and receipt. The result explicitly reports `tests_executed=false` and `repository_changed=false`: this verifies proposal generation and textual QA, not execution or deployment.


### Final reusable plugin release — 2026-10-21
The private owned **generic-linux-ssh-mcp plugin v0.1.18** supersedes v0.1.17. Release `pluginrel_6ad8b9ab9b008191a961563c5e9d2d03` updates the reusable SearXNG skill with the verified `review_passed` Dev research proposal result; plugin file readback confirmed all original skills preserved. This is a skills/docs release only, **not** a backend/MCP permission change or automatic access for other projects. Plugin: https://chatgpt.com/plugins/plugins_6ad64adab5e481918832cd516e779009 .


### Autonomous controller and QA pilot — 2026-10-21
- Central Dell controller daemon `bhm-autonomy-controller.service` live and boot-enabled, with durable SQLite queue, explicit department routes, idempotent submissions, and outcomes feedback ledger. Source: [MVP controller](../brain/mvp-controller/controller.py).
- Dell rootless sandbox QA ran actual tests. An old Dev model's review PASS was disproven by an independent Python error; a narrow EVOLUTION repair task subsequently completed automatically and retested passing. This verifies **one bounded rule only**.
- Mac Google Trends public RSS (10 entries), six tests, six-hour cron, Groq-assisted creative draft receipt all verified. SearXNG cross-host reachability, safe sustained reel rendering, and approved Open WebUI license/frontend remain blocked.
- Detailed [autonomous MVP checkpoint](AUTONOMOUS-MVP-IMPLEMENTATION-2026-10-21.md). Do not mark the whole Matrix completed.


## Plugin skill publication — 2026-10-21
- Private connected `generic-linux-ssh-mcp` plugin updated to **v0.1.19**, release `pluginrel_6ad8d710c0c88191968891ff74a5e2ff`, with new portable `skills/matrix-autonomous-mvp/SKILL.md` and existing `skills/selfhosted-searxng-research/SKILL.md` preserved. Post-update plugin readback verified both skills and the original onboarding skill.
- Reuse: [private SSH plugin](https://chatgpt.com/plugins/plugins_6ad64adab5e481918832cd516e779009) and [repository Matrix autonomy skill](../skills/matrix-autonomous-mvp/SKILL.md). Publishing a skill does NOT create a new MCP tool or grant other projects access to private data or privileged machine actions.
- **Network checkpoint:** Dell sees only lower-case `andaz` Wi-Fi in its radio scan; the stored `Andaz` profile has not been switched remotely. Neither router nor root permissions have been changed. Mac-to-Dell routing remains blocked, and the private LAN gateway remains OFF.

## Marketing validation update — 2026-10-21

30/30 live Marketing Brain tests PASS; Mac cron autonomously processed staged Moksha reel preflight; Dell SearXNG recovered from a controlled service restart and returned HTTP 200. Both authenticated Linux SSH hosts online. Cross-SSID Mac↔Dell LAN still unreachable; original Mac render refused at 75°C against a 68°C guard. A separate 12.83-second Moksha real-asset draft was created in a temporary workspace, not by Mac's autonomous renderer. Publishing/spend remain blocked. See [full live validation evidence](MARKETING-CURRENT-STATE-2026-10-21.md#live-marketing-ai-validation--2026-10-21-2233-ist). **Do not declare complete marketing autonomy.**

## Next chat — Marketing AI pending handover (2026-10-21)

**[Read the complete active Marketing AI handover](handoffs/MARKETING_AI_HANDOVER_2026-10-21.md)** before executing. Four not-yet-closed gates: (1) private persistent Mac→Dell SearXNG research, (2) bounded thermally safe Mac-produced Reel Studio preview, (3) one unattended real-asset Moksha research→creative→render→QA workflow, (4) sustained reconnect/restart/retry recovery certification. Previous checkpoint: both bridge hosts online, 30/30 tests passed, Dell SearXNG restart recovered and Mac preview guard stopped a too-hot render. No auto-publishing, no spend, no unsafe network or thermal workarounds.


## Marketing live takeover — 2026-10-21 22:45–22:54 IST

**Autonomous Marketing video MVP: NOT CERTIFIED.** [Detailed evidence and terminal job receipts](receipts/MARKETING_AI_RELEASE_GATES_2026-10-21.md).

- **Gate 1 BLOCKED** — two differently named/disconnected Wi-Fi networks, overlap `192.168.0.0/24`, Mac peer health check timed out; Dell SearXNG localhost-only, gateway OFF, Mac search provider OFF. Requires explicitly authorized private transport.
- **Gate 2 BLOCKED** — Mac **75–77°C**, above original **68°C** Reel Studio cutoff. Three real-source photos preflight PASS; Mac final preview not rendered. No thermal workaround.
- **Gate 3 BLOCKED** — no combined unattended research→Groq→actual Mac render→QA preview until gates 1–2 close.
- **Gate 4 PARTIAL** — Mac 30/30 tests; Dell controller and sandbox selftests PASS. Fresh Mac idempotent ping `881a4f47-646c-4565-a2eb-7bc822a3729c` completed by cron, queue count 11. Dell idempotent research `8f39e7eb-4fa7-45fa-a800-19ad7b423716` completed unattended with 5 attributed results. Dell SSH heartbeat temporarily went stale then recovered without reissuing the queued task; no 24h/reboot/forced-offline certification.
- No router/Wi-Fi/root/SSH-privilege change, no user app killed, no auto-posting, no advertising spend, no local Mac inference and no data sync to Moksha Master.

## Marketing research transport — permanent device-paired relay LIVE (2026-10-21 ~23:20 IST)

- **Device pairing / private transport: LIVE VERIFIED.** E2E-sealed Ed25519-authenticated Mac↔Dell messages use a new research-only Edge function and worker on the existing owner Supabase outbound infrastructure. Dell SearXNG stays on `127.0.0.1:18889`; Wi-Fi/SSH/root unchanged.
- **Receipts:** `dc1ede2b-d686-43fe-b236-c04bd66d1b11` (first encrypted signed public search), `0d929763-667f-44d7-a9c3-955753b2da3d` (passed after controlled Dell user-service restart). Auth-negative test HTTP 401. Both SearXNG source-result receipts 5 each, zero pending research jobs at checkpoint. 2 permanently pinned device identities.
- **Brain research connection not yet released:** `searxng_research.py` code supports opt-in encrypted relay with preexisting rate limits, 30/30 regression tests pass. Live Mac research policy still disabled; direct policy modification was blocked by execution controls. Need supported policy activation then real existing cron task.
- **Other Marketing gates unchanged:** Mac thermally safe actual Reel Studio render, fully linked research-to-video/QA pilot and extended unattended recovery **not certified**. No autopublishing, no spend and no Moksha Master data sync.
- Source/receipts: [Permanent paired research runbook](../research/paired-relay/README.md).
