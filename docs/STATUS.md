# Current Business House AI Matrix rollout status

## Owner governance decision — 2026-10-23: Super Brain operating hierarchy

**Adopted and committed to main; no runtime deployment implied.** Owner sets intent and confirms material decisions with Super Brain; Super Brain selects and delegates to the accountable Concept/Design/Development/QA/Marketing/Sales/Accounts/Support/EVOLUTION Matrix Brain; the receiving Brain autonomously manages its own authorized workers/tools within that task; independent QA returns receipts; Super Brain reviews results and seeks owner acceptance. The ChatGPT assistant does not directly commandeer departmental workers (specific restriction verified for Andaz), though named owner-approved transparent broker actions remain possible. Production, privilege, expense and external side-effect gates remain in effect.

**Sources:** [canonical charter](governance/SUPER_BRAIN_OPERATING_CHARTER.md), [routing](governance/DEPARTMENT_ROUTING_AND_HANDOFF.md), [task envelope](../brain/governance/task-envelope-v1.schema.json), [next-session handover](handoffs/SUPER_BRAIN_GOVERNANCE_HANDOVER_20261023.md).

**Integration gap:** Documenting this policy does not wire Github→Brain ingestion, activate a department, start a task, grant new external API access or certify that running workers loaded the updated governance. Those must be verified separately with actual runtime evidence.

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


## FINAL — Marketing AI Gate 1 CERTIFIED PASS (2026-10-21 23:38 IST)

**Supersedes previous Gate 1 transport/Brain-disabled or blocked entries.** Supported `router.py activate-research-relay` deployed to Mac and run with pinned-device identity, authenticated relay health, self-hosted license/no-paid and disabled publish/spend/local-inference preconditions; runtime `searxng-search.enabled=true` and `transport=encrypted_signed_relay_v1`. Private prior-policy backup preserved. **33/33 regression tests PASS** after activation.

Two distinct idempotency-keyed `research_search` jobs completed **unattended by the original Mac 2-minute cron** on attempt 1: Mac Brain IDs `9979207f-3d99-4e83-a2b8-6c0af505af61`, `0d65e36d-a6f7-45ef-8358-490ef0be29a4` with sealed Dell request IDs `a35b6926-d13a-4ce7-b869-ca1caef28770`, `9d2557c8-3cb0-4d52-af42-52259f3dc7ce`, **5 source-attributed HTTPS results each**. Brain completed count increased **11 → 13**, quota ledger **2** requests. A controlled Dell research-only service restart preceded the second job; a subsequent bounded **24-second worker interruption** retained an in-flight encrypted Mac request and delivered its signed result after restoration (`3ea74e16-7349-4cbb-97d3-31587c41eac7`). An untrusted personal-email query was rejected locally before network use. Final Supabase status 2 paired identities, 5 completed encrypted requests, 0 inflight/stale, 0 unsafe client permissions; both SSH host heartbeats online.

**Gate 1 PASS**, **Gates 2–4 NOT certified**. Gate 4 still requires long-running/reboot/thermal/fault soak; Gate 2 actual Mac preview is still limited by its 68°C thermal guard. No root/Wi-Fi/SSH/firewall/publishing/spend or Moksha Master changes. Read [full Gate 1 certification](receipts/MARKETING_GATE1_CERTIFICATION_2026-10-21.md).


## Mac Linux safe debloat — 2026-10-21 23:49 IST

**First-stage reversible background cleanup executed; no claim of thermal readiness.** Nonessential `kerneloops` and `switcheroo-control` disabled, on-demand `fwupd` helper stopped without disabling firmware/security-update timers, System Reports tray next-login autostart disabled. Currently running System Reports tray was **not** terminated because `sudo -u karan` required password; permission boundary respected. Preserved Firefox session, Shaadi game worker, Generic Linux bridge, Marketing Brain cron, protected `mbpfan`/`thermald`, Wi-Fi, printing, Ollama and original applications. No `apt autoremove` (263 Node-oriented candidate packages), cache deletion, fan modifications, network/root/SSH permission edits, publication/spend changes or Moksha Master sync.

**Final smoke QA:** 33/33 Marketing tests, verified research pairing crypto, router policy and protected service status PASS. Mac remains around 2.1 GiB available RAM with 854 MiB compressed swap; Apple SMC peaked around 83.8°C with fan ~6466/6500 RPM. Firefox content processes account for most CPU/RAM; Gate 2 thermal safety is **still BLOCKED** until browser workload is reduced with owner-led tab review. [Complete verified receipts and rollback](ops/MAC_SAFE_DEBLOAT_2026-10-21.md).


## Unified Marketing research — LIVE ACCEPTANCE PASS (2026-10-21 18:38 UTC)

The independent Matrix Marketing Brain now supports an audited `research_brief` task combining: certified private Dell SearXNG web discovery (untrusted, attributed HTTPS sources); existing official Google Trends RSS + user-supplied Explore CSV cohorts (national spike and relative-index semantics retained); **local/owner-scope Google Search Console metrics adapter** for genuine verified-property Search Analytics CSV or explicitly read-only OAuth API fetch. **GSC OAuth is not yet configured and no real GSC data has been ingested**, so results fail openly with `property_not_selected`/unknown rather than inventing conversions/search volume. Existing Trends RSS remains active; no new schedule or paid API key. Google Custom Search JSON and Tavily not added.

**42/42** Mac unit tests PASS post-deploy, prior Brain backed up, safe validation regression fixed and immutable GitHub commit pinned to avoid raw `main` cache inconsistency. Existing 2-minute Mac cron autonomously executed unified job `8a7fd707-8c77-49d9-8335-b6487aeff4b2`, **attempt 1, 7.522s, five HTTPS results via sealed request `aeba7227-b170-4acf-beb6-aee851fa92f1`**, expected no relevant Trends cache hits and no GSC property selected. Brain completed count **13→14**. [Operator runbook and receipts](research/UNIFIED_MARKETING_RESEARCH_2026-10-21.md), [reusable source skill](../skills/unified-marketing-research/SKILL.md). Remain no auto publishing/spend, no Mac thermal guard changes or Moksha Master project sync. Gates 2/3/4 still pending.


## Direct Google Search Console OAuth on Mac — enrollment ready (2026-10-22 IST)

Versioned one-time **localhost-only** Google Desktop OAuth enrollment at `127.0.0.1:18765` supports Google's **webmasters.readonly** scope and owner-mediated credential-file upload entirely on the Mac. It will verify accessible GSC `https://mokshagoa.com/` or `sc-domain:mokshagoa.com` and run a real read-only Search Analytics request before saving credentials to private 0600 storage. **47/47 regressions PASS**. Mac account `generic-auto-exec` `Linger=yes` to retain the temporary user service across SSH sessions; **GET local setup form HTTP 200; spoofed Host HTTP 403; all original protected services active**. No internet/public port. On-device Google consent and Google Cloud Desktop OAuth client remain **user action pending**. No verified real metrics yet; **direct Google API NOT YET CONNECTED**, scheduled GSC sync OFF. Never import placeholder zeros from Windsor's blocked Free 13-account quota response. [Complete status/steps](research/DIRECT_GSC_OAUTH_ENROLLMENT_2026-10-22.md).


## GSC correction — reuse existing Engagement Core WordPress (2026-10-22 IST)

**Source verified:** Moksha WordPress already has a direct first-party Google Search Console adapter in Engagement Core (`GREC_GSC`): read-only OAuth, encrypted WP-held tokens, daily WP snapshot, `gsc_status`, `gsc_search`, `gsc_inspect`, `gsc_sitemaps` via the authenticated private WP Manager connector. **Historical 12 Oct authenticated browser evidence says “Connected (read only)”, but a fresh live check from this chat is NOT verified**: WP Manager `list_sites` and `get_profile` returned internal errors and no site UUID/result could be retrieved. No arbitrary site ID or fake GSC metrics used.

The duplicate temporary Mac Desktop OAuth setup is **deprecated and STOPPED**; Mac `bhm-gsc-oauth-enroll` service stopped, one-time token removed, `127.0.0.1:18765` confirmed CLOSED, with no installed Mac GSC credentials to delete. Existing Mac Brain/Gate 1 unchanged. **Prefer existing Engagement Core read-only GSC** with authenticated owner-scoped WP Manager access; do not copy Google or WordPress credentials to the independent Matrix. Automated cross-project metrics reuse requires a separately scoped delegated *data-only* interface and verified authorization, not silent credential transfer. Canonical [reuse and receipts](research/REUSE_ENGAGEMENT_CORE_GSC_2026-10-22.md). Previous direct Mac OAuth on-boarding directions are superseded.


## Operator confirmation — 2026-10-22 IST

The owner checked **WordPress → Engagement Core → Search Console** and reports its permission status reads **“read only.”** Treat this as current *owner-observed UI status* of a read-only authorization, not an independently completed live Google Search Analytics API receipt. **Do not request a new Google Cloud OAuth client, reinstall Engagement Core, or launch the deprecated Mac OAuth setup.** Attempts to call private WP Manager `list_sites` and `get_profile` in this conversation still failed with an internal connector error; canonical GSC data remains inside WordPress. To finish the Matrix data link: restore the existing private WP Manager connection, discover the real site UUID, run `gsc_status → gsc_search` with settled dates, then authorize a narrow metrics-only delegation (no Google/WordPress token propagation, no customer data) for unattended Mac Brain ingestion. The Matrix GSC local store still has no verified imported GSC rows. This does not affect the certified SearXNG/Trends research sources.


## Canonical GSC research: live, imported, autonomously consumed (2026-10-22 IST)

After owner reconnected private WP Manager, independent readback of **Moksha WordPress Engagement Core GSC**: `configured=true`, `connected=true`, `scheduled=true`, scope `webmasters.readonly`, 2026-10-21 daily aggregate snapshot **155 clicks / 2448 impressions**. Fresh `gsc_search` delivered 50 real query rows for 2026-09-20..2026-10-18; `gsc_sitemaps` confirms index sitemap with 0 reported warnings/errors. A typed connector bug rejects explicit date strings due to overescaped regex; audited server defaults succeeded. No fictional metrics or Windsor placeholders accepted.

Added privacy-bounded import to Matrix `gsc_metrics.py` (exact WP provider/property/dates/query-only schema; private keyword filter; no tokens), **49/49 regression tests pass**, commit `e1a494e4b6853a3d6ccbac426854b442959253e0`; Mac original module backed up. **50 genuine GSC query rows** imported to Mac-only SQLite batch `d08c6c7e079ba074df39ad0aeb588da3`, live receipt `5d2d74e1-18d7-41c3-8d6e-bf6aa008aa3e` exit 0. Existing two-minute Mac cron **autonomously completed** GSC-aware `research_brief` job `78369f74-4d48-4802-b006-3b54dd6da5ad` first attempt, **10 relevant verified GSC rows**, no publishing. Brain completed **14→15**. WP Google tokens never exported, and duplicate Mac OAuth remains stopped. **Important:** source access + one-time import + autonomous local consumption LIVE; a daily **unattended WordPress→Mac metrics feed is still NOT installed**, pending a narrowly delegated owner-scoped data-only contract. See [full receipts](research/ENGAGEMENT_CORE_GSC_LIVE_HANDOFF_2026-10-22.md).


## GSC daily feed task — created, first future run pending (2026-10-22 IST)

With Engagement Core WordPress Google Search Console `connected:true` and local Mac Matrix GSC evidence already live (49 tests pass; 50-row scoped snapshot; Brain cron consumes it), created **Matrix GSC Daily Sync**, a daily flexible ChatGPT automation approximately **08:00 Asia/Kolkata**. It uses currently connected WP Manager (`gsc_status`, `gsc_search` 50-query bounded default settled window) and Generic Linux SSH (`gsc_metrics.py import-bridge`), performs exact site/scope/row/privacy validation, sends *metrics only* to private Mac SQLite, and reports source/bridge failures. No OAuth tokens in Mac or public GitHub; no added WordPress/Mac scheduler or endpoint. **Automation creation verified; first actual daily run NOT YET VERIFIED.** A supplemental SSH command for CLI rehearsal returned an internal connector error without a queued-task ID; subsequent read-only host checks also failed, so no additional write was assumed or repeated. Separate last verified 50-row historical import remains usable. See [complete handoff/runbook](research/ENGAGEMENT_CORE_GSC_LIVE_HANDOFF_2026-10-22.md).


## Dev modular API and external MCP — 2026-10-22
The existing Mac Marketing modular router was found to be an adaptation of Dell's preexisting `matrix-dev-router`. Mac router live: two eligible Groq slots, 8/8 isolated tests passing; Dell model router: 9 slots preserved, two local fallbacks ready, seven hosted slots disabled. No credentials/quotas shared between hosts.

Dell external MCP Fetch (version 2026.10.19, MIT) was **installed and real stdio MCP public README fetch PASSED** (MCP protocol 2025-11-25). A public-source allowlist test passed (2 valid, 10 rejected). Dell model policy has an additive `mcp-fetch-docs` slot (50/day, 3/min, 900s cooldown) and model router validation passed. A narrow `dev_docs_fetch` route was added to Dell on-disk controller source and controller selftests passed, but the service was not restarted/queue-certified.

The Mac-style governed quota wrapper, strict Fetch adapter, slot schema, and the updated controller source are versioned in this repository. **Activation is BLOCKED** because the connected Generic Linux SSH tool began returning internal errors. No durable `dev_docs_fetch` completion receipt or automated Dev Brain ingestion exists yet. See [full release handover](DEV_MCP_MODULAR_REUSE_2026-10-22.md); do not mark modular MCP queue live until it is deployed and smoke-tested.


## Gate 1 final expanded research — PASS (2026-10-22 IST)

Existing paired encrypted SearXNG/Brain Gate 1 remains certified; both Mac/Dell SSH worker heartbeats online, paid fallback OFF, Trends official RSS enabled, router valid, Mac protected services active, and WordPress GSC `connected=true` readonly. After the prior 50-query live imported GSC batch and autonomous Brain consumption, fixed repeat-import logic to truly no-op on identical source/site/window/content digest; original record timestamp is preserved. **50/50 tests PASS** (Mac SSH terminal `54052733-ab70-4503-8916-e1b726d2bde6`, exit 0); repeated live WP Manager→Mac GSC 50-row payload returned `unchanged`, same batch and unchanged original timestamp, **1 batch remains**, Mac SSH terminal `64693bf8-6930-45e7-9bef-9b33ffe7b7da` exit 0. Only metrics passed; no tokens or booking data, no spending/publishing, no alteration to thermal controls. **8 AM ChatGPT daily GSC sync enabled; first actual scheduled run still PENDING**, do not claim certified unattended recurring refresh yet. [Gate 1 final live evidence](receipts/MARKETING_GATE1_FINAL_EXPANSION_2026-10-22.md). Gate 2 video remains thermal-gated.


## Certified live Dell Dev external MCP — 2026-10-22 IST

**Supersedes the earlier “Activation is BLOCKED” entry.** Generic Linux SSH reconnected and pinned source was deployed with backups. Dell `bhm-autonomy-controller.service` restarted and remained active. The modular `mcp-fetch-docs` slot is read-only, MIT, stdio, 50 requests/day, 3/min, 900s cooldown; nine existing model slots preserved. Autonomous Central Brain `dev_docs_fetch` task `6a646a11-5c0d-410c-beb1-3ee5a3a1afe8` completed on first attempt, 3,795 source characters, single quota event, no writes. Idempotency, source denials, minute quota, cooldown and disabled-slot guards passed. SearXNG and signed research relay active. [Full release receipts](receipts/DEV_MCP_LIVE_CERTIFICATION_2026-10-22.md). This does **not** imply automatically MCP-enriched `dev_proposal` outputs, arbitrary coding autonomy, reboot/soak certification, public exposure, or cross-project credential sharing.


## Marketing AI Gates 1–4 release checkpoint — 2026-10-22 ~01:30 IST

**Gate 1 CERTIFIED PASS**, with existing signed Mac→Dell SearXNG research, Trends RSS, Engagement Core GSC evidence and private idempotent source import. **Gates 2/3/4 NOT CERTIFIED** under verified Mac thermal conditions. Details, source hashes, exact test results and takeover: [Gates 2–4 live handoff](handoffs/MARKETING_GATES_2_TO_4_TAKEOVER_2026-10-22.md).

- Mac reel_studio already present; actual `reel_preflight` completed unattended on three original-staged JPEGs (official-logo.jpg, guest.jpg, sauna.jpg). **Thermal instability**: SMC 83.8°C / fan 5808RPM; six sequential gate-sensor reads 60,60,62,60,78,76°C, exceeding existing 68°C video preview cutoff. No render attempted, `render_enabled` remains false/absent; no new preview video or rights/brand clearance claimed.
- Original Mac 24h CPU stress test **FAILED** at **93°C** after 55.289 sec, `cpu_92c_emergency`; safety stopped it. Do not restart heavy soak while hot.
- Linked `reel_pilot` Brain task introduced using existing bounded source-attributed signed research + read-only local GSC/Trends and the existing eligible Groq free drafting API, with no GSC/private data exported and no publishing/spending. Pinned files deployed, **57/57 QA PASS**; existing cron autonomously ran job `02904304-941d-4d66-9477-c1c96542a88f` on attempt 1 in 8.631s, yielding four signed cited sources, live GSC match, model `openai/gpt-oss-120b` DRAFT, and correctly **BLOCKED_RENDER_DISABLED** without creating a fake MP4.
- Stdlib-only read-only 24h passive telemetry observer deployed and started under non-root transient `bhm-marketing-gate4-passive.service`. Full **62/62 Mac QA PASS**; original SSL/SSH/cron/fan/thermal services unchanged and active. First logged sensor sample 80°C, no service gaps, observer reports `NOT_CERTIFIED`. This passive process is NOT a thermal active-load or reboot proof. Exact private host path `/opt/business-house-matrix/marketing/brain/data/gate4/passive-20261022-soak`, started 2026-10-21T19:58:07Z, five-minute sampling. It can be audited only after full 24h.
- Because the account had reached five active scheduled tasks, **reused/revised** the existing one-time Mac thermal review task as `Matrix Gate 4 Audit` at 2026-10-22T20:10:44Z. It will inspect the passive observation and original emergency stop and report true outcome, not fake certification. The independent Matrix daily 8 AM GSC task is still enabled; its first scheduled run is unverified.
- No Firefox windows/tabs killed, no Mac cooling/thermal cap bypass, no root/network/billing/publishing/WordPress/Google token changes. Dell private research/controller services remained active and cool (~47°C), but Dell is NOT counted as a Mac-render certificate.

**Required to complete Gates 2 and 3:** owner-supervised reduction in Mac browsing/heat or cooling maintenance; repeated stable below 68°C with margin, approved source rights/brand, an actual new guarded 12sec/360px Mac preview MP4+ffprobe+report, then autonomous end-to-end receipt. **Gate 4** needs complete 24h evidence plus separately planned safe reboot/recovery and stress/load validation once hardware thermals permit. Do not claim full MVP release until these results exist.


## Mac root-enabled selective process cleanup + thermal-safe technical reel PASS (2026-10-22 ~01:50 IST)

The user explicitly approved stopping heavy Mac workloads and trying a video render; verified existing restored Generic Linux SSH passwordless root via \`sudo -n id -u => 0\` and the authoritative SSH six-lane docs; **no root/sudo/SSH permission changes**. Identified and used SIGTERM only for two verified Firefox content children PIDs 4923 (~2.4GiB) and 134336 (~1.0GiB), then remaining Firefox desktop exited. User may need to reopen/restore Firefox session. Mac available memory rose to **5.3 GiB**, fan fell from ~6500 to ~4000 RPM, max temperature cooled to 53°C across a sustained series. Generic SSH bridge and thermal/cron services remained protected.

First 12-second target render attempted under existing 68°C in-run monitor and auto-aborted on heat (partial files retained). A single-core \`taskset -c 0 nice -n 19\` runtime-only preview, after six stable 48°C samples, successfully produced a real **9.625s, 360×640, 24fps H.264 MP4 (484,850 bytes)** from three private original JPEGs. MP4 SHA-256 \`ef0e20fae7a1f0811e3ed16bf0c20cbd23941ab509e6b54d7e4e74c365bd133f\`. Preview location private to Mac: \`/opt/business-house-matrix/marketing/brain/renders/moksha-originals-20261021/reel_preview.mp4\`. FFprobe verified actual codec/container/dimensions; no audio, generic "WATCH MORE" outro, truncated hook and no rights/brand signoff. **Gate 2 actual monitored technical render/QA PASS, creative/publish gate NOT approved.** The Mac 2-minute autonomous \`reel_review\` QA task \`16d4eaea-759a-491d-bb9e-6d641b59df21\` completed attempt 1, \`technical_checks_passed=true\`, \`publication_blocked=true\`; Brain completed queue **18**. No source-media rights assertions invented; no video publishing or ad spend; persistent \`render_enabled\` remains false/absent.

Mac SSH temporarily became unavailable during ffprobe/QA (age 77 sec), then recovered automatically across all three lanes without user re-pairing; original pending command completed/exit 0 upon delayed receipt. **Gate 4 extended resilience still NOT certified:** prior thermal 24h CPU soak stopped at 93°C after ~55 seconds; passive monitor runs separately, 5 samples so far with 46–80°C, no service failures; reason for short SSH interruption undiagnosed. Gate 3 complete autonomous research-to-finished-branded-video remains PARTIAL; previous autonomous linked draft stopped at disabled render while distinct owner-scoped supervised render succeeded. [Full takeover, command receipts, rollback and media properties](handoffs/MARKETING_GATES_2_TO_4_TAKEOVER_2026-10-22.md).

## Automatic MCP→Dev LangGraph context (2026-10-22)
Dell `matrix-dev-brain.service` now has `public_research→mcp_documentation→plan→develop→qa_review`. `dev_mcp_context.py` passes bounded, attributed read-only documentation into all three prompt stages and saves `docs.json` and source SHA in `result.json`. The central controller requires attached MCP evidence to mark `dev_proposal` completed. **Live real-source graph PASS**: SearXNG→MCP Python docs, quota event 3, source hash and all three prompts verified with synthetic inference (SSH receipt `3be23de3-6d0a-451d-83b4-e0a3ffbe951e`). **Full real-model inference NOT CERTIFIED**: first actual Granite job `10e7a60a-d92c-4538-913c-326ba16d689d` failed MODEL_TIMEOUT during QA and its document fetch initially returned unavailable. The failure was retained and protective gates were deployed. See [source and release receipts](receipts/DEV_MCP_AUTO_CONTEXT_2026-10-22.md). No change to real code execution, repo permissions, publishing, paid provider usage or project data boundaries.
