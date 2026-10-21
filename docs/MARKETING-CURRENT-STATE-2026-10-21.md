# Business House AI Matrix — Marketing Department Current State & Handoff

**Snapshot date:** 2026-10-21, verified from `mac-linux` at approximately 17:03 IST  
**Status:** Phase 1 marketing *brain and hosted text inference* operational; creative reel production integration and broader rollout **not complete**.  
**Project boundary:** Business House AI Matrix only; entirely independent of Moksha Master and its assets/accounts.  
**Canonical repository:** https://github.com/aarondash5-star/business-house-matrix (public; **never commit secrets or runtime databases**).  
**This file is the current-state reference.** Earlier phase and router docs contain chronological entries, including once-correct staging states that are now superseded.

## 1. Executive snapshot

The Mac `KARAN` is the Marketing Department coordinator. It has an isolated Python Marketing Brain, durable SQLite task queue, nonroot cron worker and task receipts, a modular free-only hosted-model router derived from Dell Matrix Dev's established policy design, and live Groq inference. The existing FFmpeg/Reel Studio pipeline has **not yet been attached** to the Brain for finished video production.

- **Working today:** automated queue scheduling; local health checks; API routing and provider selection by profile; GPT-OSS 120B and Qwen3.8 27B live via Groq; quota reservation and grouped accounting; creation/storage of draft text receipts.
- **Not working/connected yet:** independently sourced real-time research from Tavily; Gemini creative inference; additional live API providers; automated frame analysis/selection and reel finishing through the Brain; QA-backed ready-to-publish campaigns; autonomous publishing.
- **Critical distinction:** autonomous *drafting* is tested, autonomous *finished reel production* is **not**.

## 2. Verified live state

| Layer / item | Verified state | Evidence or details |
|---|---|---|
| Linux bridge | Online | `mac-linux` worker heartbeat; `generic-linux-automator.service` active |
| Marketing Brain | Running via scheduled jobs | `brain.py`, `worker.sh`, cron service active, queue `completed=5` |
| Brain model request routing | Enabled | Private `config.json`: `online_enabled=true` |
| Groq creative | **Active** | `groq-creative-oss120` -> `openai/gpt-oss-120b`, authenticated and actual completion returned |
| Groq copy | **Active** | `groq-copy-qwen` -> `qwen/qwen3.8-27b`, actual queue-to-API-to-receipt job completed |
| Groq credential management | Active | Single owner-enrolled private file; shared credential reference; model availability verified; key value never committed or logged here |
| Groq local quota accounting | Active | Shared `groq-one-account` request group: **2 requests recorded**, conservative **40/day cap**; this is a local ledger, not a verified external billing statement |
| Cloudflare hosted model | Disabled | Slot configured, no enrolled credential |
| OpenRouter hosted model | Disabled | Slot configured, no enrolled credential |
| Gemini Flash candidate | **Disabled** | Registered `gemini-flash-candidate`; `model_license_approved=false`; explicit proprietary-licensing / free-tier data-use review required |
| Tavily research candidate | **Disabled** | Registered separately as `tool_connections.tavily-search`; no credential, adapter or live search; research provider is not an LLM |
| Local creative inference | **Safety-locked** | `local_inference_enabled=false`; prior local CPU run reached approximately **90°C** |
| Advertising spend | Disabled | `spend_enabled=false` |
| Social publishing | Disabled | `publish_enabled=false` |
| Core system services | Healthy at verification | `cron`, `ollama.service`, `generic-linux-automator.service` active |
| Reel Studio | Present but unconnected | Existing `reel.py`, `finisher.py`, `stock.py`, `beats.py`, `autodraft.sh` untouched |
| Tests | **11 passed** | 7 router and 4 Brain tests run on live Mac, including synthetic quota and 429 failover cases |

**Live API receipts:** GPT-OSS 120B smoke response completed; Qwen3.8 27B `hosted_draft` queue job `b14cb180-1253-4eac-8567-7793ce5c956f` finished on attempt 1. Output must undergo fact-checking and brand review before customer-facing use.

## 3. Architecture and location

```text
Business House Matrix central Brain (planned full coordinator)
    └── Marketing Department Brain on Mac (implemented pilot)
          ├── SQLite durable queue + cron runner + JSON receipts
          ├── Task router (creative / copy / research / vision / review / fast)
          │     ├── Groq GPT-OSS 120B        [ACTIVE]
          │     ├── Groq Qwen3.8 27B         [ACTIVE]
          │     ├── Cloudflare Qwen          [DISABLED]
          │     ├── OpenRouter free Qwen     [DISABLED]
          │     └── Gemini 2.5 Flash        [DISABLED / PROPRIETARY]
          ├── Tavily research tool          [REGISTERED / DISABLED]
          ├── Existing Mac Reel Studio      [NOT WIRED TO BRAIN]
          └── Creative QA + EVOLUTION       [DESIGNED / NOT FULLY DEPLOYED]
```

**Runtime Mac paths (not Git-tracked):**
- Brain and router: `/opt/business-house-matrix/marketing/brain/`
- Private runtime config: `brain/config.json`
- Private model policy: `brain/provider-policy.json`
- Private provider keys: `brain/secrets/` (0700 directory; 0600 key files)
- Provider quota: `brain/provider-quota.sqlite3`
- Queue database: `brain/data/queue.sqlite3`
- Job receipts: `brain/receipts/`
- Operations docs: `/opt/business-house-matrix/marketing/docs/`
- Preexisting Reel Studio: `/opt/business-house-matrix/marketing/reel-studio/`

**Versioned GitHub paths:**
- `marketing/mac-brain/brain.py`
- `marketing/mac-brain/router.py`
- `marketing/mac-brain/provider-policy.template.json`
- `marketing/mac-brain/test_brain.py`
- `marketing/mac-brain/test_router.py`
- `marketing/mac-brain/worker.sh`
- `docs/MAC-MARKETING-PHASE1.md` — historical implementation timeline
- `docs/MAC-MARKETING-API-ROUTER.md` — provider architecture, onboarding and rollback
- **`docs/MARKETING-CURRENT-STATE-2026-10-21.md` — this checkpoint**

Dell Matrix Dev uses a related modular policy and quota model, but the Mac does **not** tunnel unsupervised commands through Dell. Both projects remain isolated at the runtime and secret levels. The Mac uses a restricted Python HTTPS adapter instead of the Dell Pi CLI.

## 4. Completed work ledger

1. Audited hardware, existing services, media editing stack and available local models.
2. Set up isolated Marketing Brain with SQLite queue, idempotency, receipts, stale-task recovery, one worker at a time and 2-minute cron scheduler.
3. Evaluated local Ollama creative inference; observed unsafe 90°C test and **disabled** further CPU-intensive local creative inference.
4. Audited existing Dell Matrix Dev provider router, then adapted its conservative selection / license / quota / cooldown controls to the Mac.
5. Added and tested task routing, shared Groq quota grouping, secure hidden-prompt key enrollment, whitelist-based provider endpoints and explicit no-paid gate.
6. Owner enrolled the Groq Free plan key; authenticated both model IDs without exposing credentials.
7. Activated both Groq models and completed real API tests, including autonomous Brain queue -> Groq -> stored receipt.
8. Added Cloudflare and OpenRouter as disabled backup options; added Gemini as disabled proprietary-model candidate; added Tavily as a separate disabled research-tool candidate.
9. Ran the router and Brain regression suites successfully (**7 + 4 tests**) after latest changes.
10. Preserved publishing, spending, local creative-inference restrictions, untouched Reel Studio and existing SSH/Ollama/cron services.

## 5. Safety rules and known limitations

- **Open source / governance:** The independent Matrix defaults to OSI-approved software and genuinely open-licensed model weights. Gemini is proprietary; its registration is a **candidate**, not authority to run it. Tavily is a hosted search service; review usage terms and any proprietary dependencies before activation.
- **Free-tier billing:** A `paid_inference_allowed=false` setting and local request cap do not constitute a payment-provider hard spending cap. Verify the vendor console's Free plan, billing configuration, request/token counters and relevant terms.
- **Data privacy:** Gemini free-tier content processing differs from confidential paid processing; never forward private business data, identifiable guest material or unpublished sensitive footage without an approved data-handling review.
- **Quality:** A synthetic creative test produced an unverified “zero waste” claim. Add grounded factual QA, brand accuracy and human sign-off before publishing.
- **Thermals:** Previous 90°C CPU inference requires that `local_inference_enabled` remain false until continuous in-run thermal limits and safe model performance are validated.
- **Scope:** Online Groq *text drafting* works. Video editing, stock retrieval, content rights verification, computer/browser operation, analytics and social posting are not thereby authenticated or production ready.
- **Rate-limit testing:** Simulated 429/quotas passed. Real provider exhaustion and account meter comparison have not been validated, and should not be induced by spamming.
- **Recovery:** The cron/bridge services are active, but a complete reboot/offline recovery test of the entire Marketing workflow is still pending.
- **Security:** Never commit credentials, runtime policy or DB snapshots to this public repository; do not expose keys through shell command arguments, chat or logs.

## 6. Prioritized remaining work (handoff checklist)

| Priority | Work package | Completion criterion |
|---|---|---|
| P0 | Source/asset licensing and quality gates | Validate every model/tool/service license; reject unsupported marketing claims and unlicensed media |
| P1 | Reel Studio integration | Feed approved raw footage/photos to Mac Reel Studio, return finished rendered vertical draft and edit recipe with receipts |
| P1 | Marketing QA automation | Scene sequencing, 9:16, captions, audio rights, visual identity, factual claims, no invented assets, render QC and approval queue |
| P1 | Resource-aware render scheduler | Serialized FFmpeg jobs, sensor polling during rendering, recovery from cancellation, bounded disk/cache management |
| P1 | Groq usage/billing validation | Compare logged requests with official console and adjust per-model token/rate budgets |
| P2 | Tavily research connector | Verify account Free plan and licensing, implement web-search-specific adapter plus evidence citations, quota and safe credential enrollment |
| P2 | Additional fallback providers | Confirm model availability, free entitlement and license per account; then activate Cloudflare/OpenRouter one at a time |
| P2 | Gemini decision | Explicit project-policy exception required to use a proprietary model; assess data retention and billing before any integration |
| P2 | Offline/reboot and remote failover drills | Verified non-destructive restart, queued-job persistence, network outage recovery, no runaway API calls |
| P3 | Authorized channel distribution and analytics | Platform accounts, API permissions and publication review gates; no unattended publishing by default |
| P3 | EVOLUTION feedback | Track quality, review corrections, engagement and benchmarked worker/provider selection; no uncontrolled model/policy self-mutation |

**Next execution milestone:** connect existing Reel Studio to the Marketing Brain while continuing to use Groq for remote creative planning/copy, then render **one real-footage draft** without granting publication authority.

## 7. Operator check and safe rollback

Read-only status:
```bash
B=/opt/business-house-matrix/marketing/brain
python3 "$B/router.py" validate
python3 "$B/router.py" status
python3 "$B/brain.py" status
python3 "$B/test_router.py"
python3 "$B/test_brain.py"
systemctl is-active cron generic-linux-automator.service ollama.service
```

**If hosted calls must be stopped:** set `online_enabled=false` in private Brain config using a guarded atomic write; disable Groq slots with the router's `disable` action. Do not delete the receipts, provider ledger or secret vault. Keep SSH bridge, cron and Ollama service intact. Prior safe configuration copy: `brain/config.json.pre-groq-live`. Router/policy snapshots before Tavily/Gemini addition: `router.py.pre-tavily-gemini-20261021`, `provider-policy.json.pre-tavily-gemini-20261021`. Do not restore older files without reconciling later production changes.

## 8. Reference and citation rules for future sessions

**When resuming:** read **this** checkpoint first, then consult:
1. `docs/MAC-MARKETING-PHASE1.md` for detailed chronological actions and thermal incident.
2. `docs/MAC-MARKETING-API-ROUTER.md` for provider commands, risk decisions and testing.
3. `marketing/mac-brain/README.md` for queue operator usage.
4. Live Mac status and test results. **Never assume this dated document is live truth after 2026-10-21.**

**Explicit exclusions:** no modifications to Moksha Master, no OpenClaw before first pilot evaluation, no LibreChat (Open WebUI selected), no unsupported claims of complete nine-department or video autonomous operation. 


## Update — Tavily keyless, 2026-10-21

- Source: https://docs.tavily.com/documentation/keyless . Tavily Search and Extract keyless endpoints supported, no account/key required, free but rate-limited. External Tavily is a proprietary SaaS (not an open-source model).
- Mac research adapter installed, connected to Brain tasks `research_search` and `research_extract`; only public non-sensitive queries or public HTTPS URLs permitted. **No Tavily key stored**.
- Activated Tavily's public-only keyless registry entry with self-imposed 2/minute, 15/day, 100/month caps and no paid fallback, leaving Groq live.
- First **real** Tavily keyless search returned **HTTP 429**; it did **not** return successful research results. Stored the rejection and started a 1-hour local cooldown against repeated calls.
- Verified 25 tests passed (8 router, 7 Tavily research, 4 Brain, 6 Reel Studio bridge). The HTTP request mock verified no Authorization header.
- **Current Tavily operational state: integrated but rate-limited/unavailable for live results**. The next step is a bounded retry after cooldown or owner enrollment of Tavily's separate 1,000-credits/month free API key.
- Existing Groq API routing remains operational; Gemini, Cloudflare and OpenRouter disabled; publishing, spending, local creative inference and rendering remain disabled.
- See [Marketing API Router](MAC-MARKETING-API-ROUTER.md) for exact controls, no-key mode and rollback.

## Research engine replacement checkpoint — 2026-10-21
- **Tavily retired** from live Marketing Brain routing. Historical Tavily files and request records are retained for rollback only.
- **SearXNG** deployed and proven live on Dell via official AGPL container. Boot-persistent rootless service, localhost engine and restricted private LAN gateway. Live Dell-local searches returned relevant cited results.
- **Mac SearXNG code deployed** and 24 automated tests passed. The live SearXNG policy slot remains disabled pending network reachability; Groq models stay active.
- Blocker: Mac and Dell are isolated at Wi-Fi layer (ARP failure / no route to host in both directions), not merely the SearXNG gateway. Do not expose port to the public internet to bypass the issue.
- See [deployment and detailed handoff](RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md) for verified commands, service names, private addresses and rollback. Earlier mentions of Tavily in this historical document are superseded by this entry.


### Network clarification — 2026-10-21
Mac `Andaz` and Dell `andaz` are DIFFERENT Wi-Fi networks (distinct BSSIDs/gateway responses), even though both were assigned `192.168.0.x`. Their overlapping subnets cannot reach each other. Mac Marketing's SearXNG adapter therefore remains disabled. The unused Dell LAN gateway was stopped to prevent LAN exposure; Dell Dev can search SearXNG locally with no cross-network dependency. No unapproved SSID changes or paid relay were made. See [updated SearXNG deployment](RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md).

### Capability reuse reference — 2026-10-21
Private Generic Linux SSH plugin v0.1.17 now includes the [SearXNG cross-project skill](../skills/selfhosted-searxng-research/SKILL.md) with [read-only API contract](REUSABLE-RESEARCH-CONTRACT.md). This adds instructions for approved Dell-local read-only research to other projects but **does not activate** Mac `searxng-search`; the two Wi-Fi networks are still isolated. Other projects require their own explicit adoption and data policy.

## Live Marketing AI validation — 2026-10-21 22:33 IST

Verified against the live `mac-linux` (KARAN) and `dell-linux` (karan-Inspiron-5379) via the existing authenticated Generic Linux SSH connector:

- Both hosts were paired, online and passed identity/kernel SSH probes. No root/sudo policy, router or Wi-Fi profile was changed.
- Dell SearXNG rootless Podman service `bhm-searxng.service` remains boot-enabled; Dell-local public SearXNG search returned three source-attributed results. A controlled service restart recovered to HTTP 200 on readiness attempt 5 (~16s). Search is localhost-only on Dell.
- Mac and Dell are on different case-sensitive SSIDs (`Andaz` versus `andaz`), assigned overlapping 192.168.0.0/24 subnets, with failed ARP/ping and `No route to host` cross-access. The Mac radio scan did NOT show the lowercase Dell SSID. Mac SearXNG network policy therefore remains disabled; it is **not** a functioning cross-host research connection. Do not open the search service to the Internet.
- Mac Marketing Brain `python3 -m unittest discover -p 'test_*.py'` passed **30/30** current tests. Idempotency duplicate enqueue produced identical job ID; a live queued `ping` completed with a receipt. The two-minute cron and `cron.service` remain active.
- A real `reel_preflight` job was queued at 17:00 UTC and was automatically processed by the existing scheduler at **17:02:02 UTC** (receipt `295bd56f-d635-4e53-85e7-cbd36244374e`); preflight passed, and publication remained denied. Mac Brain queue currently reports 10 completed jobs.
- Three original Moksha images (a guest in sauna, sauna cleaning, and official logo source) were retrieved with the connected owner Drive app and staged in the existing private Mac media inbox `moksha-originals-20261021`; all JPEG MIME/size checks passed. No business footage was added to this public repository.
- Mac's own Reel Studio `reel_bridge.render()` refused the first live preview at **75°C** due to its existing **68°C** thermal cutoff. Later sensors reached 76–78°C, with long-running Firefox consuming resources. No thermal limit was raised and no hot render was forced.
- Separately, a **12.83-second 720×1280 H.264 draft** was rendered from the verified originals in the ChatGPT temporary processing environment, visually sampled, and returned as a conversation download. This is *not* evidence of Mac autonomous video rendering and was not uploaded to GitHub or published.
- Publishing, advertising spend and local inference on Mac remain disabled. Dell research and Mac queue continuity have been smoke-tested. No root permission changes or new cloud project have been made.

**Unresolved release gates:** (1) authenticated persistent Mac↔Dell research transport / router-level isolation fix; (2) thermally safe Mac Reel Studio rendering under the existing guard; (3) a verified single autonomous Marketing Brain run spanning research → planning → finished video → QA; (4) sustained longer-duration host/network recovery evidence. Avoid claiming fully autonomous MVP until these pass.

Independent Matrix project only. Do not synchronize private Moksha Master data into this repository.


## Latest takeover verification — 2026-10-21 22:45–22:54 IST

**Status: NOT CERTIFIED; three production-path gates BLOCKED, recovery certification PARTIAL.** The entire preexisting Marketing runtime was reused without code, secret, network, root, thermal or publication changes. See [exact verified SSH and job receipts](receipts/MARKETING_AI_RELEASE_GATES_2026-10-21.md).

- Both `mac-linux` and `dell-linux` initially passed authenticated identity probes; existing nonroot service identity and scheduler services survived. Mac's **30/30** latest tests, Dell controller/sandbox selftests PASS.
- **Gate 1 BLOCKED:** `Andaz` Mac and `andaz` Dell on separate overlapping `192.168.0.0/24` networks; Mac HTTP `/health` to `192.168.0.103:18888` timed out, no authenticated overlay present. Dell localhost SearXNG works, LAN gateway OFF; Mac research policy OFF. No speculative tunnel, IP allowlist or Wi-Fi change.
- **Gate 2 BLOCKED:** Mac SMC reached **77°C**, later **75°C**, above the enforced **68°C** render cutoff. Original three-photo batch passes preflight, but actual Mac Reel Studio render was not attempted at unsafe heat; no Mac-owned MP4 exists yet.
- **Gate 3 BLOCKED:** Do not submit a fake full pilot until trusted Mac→Dell search and safe Mac rendering are actually functioning. No new full-video production job was created.
- **Gate 4 PARTIAL:** Duplicate-key Mac ping returned one job `881a4f47-646c-4565-a2eb-7bc822a3729c`, unattended cron completed it first attempt 17:22:01Z; Mac completed count **11**. Dell controller duplicate-key public-search test returned one job `8f39e7eb-4fa7-45fa-a800-19ad7b423716`; daemon completed first attempt 17:20:58Z with five public attributed SearXNG results. Dell SSH bridge heartbeat briefly went stale and automatically returned online, and the original queued readback was recovered without resubmission. Deliberate disconnect/reboot and long unattended soak not tested.
- **Safety confirmed:** `publish_enabled=false`, `spend_enabled=false`, `local_inference_enabled=false`, `searxng-search.enabled=false`; no paid fallback and no Moksha Master synchronization.

**Next order:** owner-approved trusted common LAN or authenticated private relay → thermally safe in-run Mac render → one real linked research-to-video QA pilot → extended controlled recovery/soak. This update supersedes prior queue counts and earlier wording that could imply Mac research or finished editor autonomy.

## Verified permanent Mac↔Dell handshake — 2026-10-21 ~23:20 IST

**New:** permanent, revocable owner-paired cryptographic research relay actually deployed and live-tested. This removes the previous **network transport** blocker while preserving isolated `Andaz`/`andaz` Wi-Fi, local-only SearXNG and all root/SSH/privacy gates. Separate E2E-encrypted `bhm_research_*` queue and Edge Function v2 run on the preexisting owner Supabase infrastructure; browser PIN and Generic SSH command queues are unchanged.

**Live evidence:** Both hosts independently generated signing/encryption keys and verified pinned public fingerprints. Dell research-only nonroot `bhm-research-relay.service` enabled/active. Two Mac-initiated requests finished with signed, encrypted Dell results and five HTTPS references each: `dc1ede2b-d686-43fe-b236-c04bd66d1b11`, `0d929763-667f-44d7-a9c3-955753b2da3d`; the second was completed *after a controlled service restart*. Unsigned polling returned HTTP 401. Admin readback: 2 active paired keys, 2 completed jobs, none pending, no ordinary-client SELECT/INSERT/UPDATE/DELETE grants and no RLS allow policies.

**Still pending:** Enabling the existing Mac Marketing Brain `searxng-search` slot through a supported/approved policy method, then verifying `research_search` is autonomously consumed by its established cron with a terminal receipt. The new repo Mac adapter supports `transport=encrypted_signed_relay_v1` and 30/30 tests passed after source deployment while slot remained disabled; a direct policy-edit tool command was rejected, and it was not bypassed. Long-duration uptime, full reboot, replay and thermal-safe video remain un-certified. `publish_enabled=false`, `spend_enabled=false` preserved. This keeps Matrix separate from Moksha Master as a logical application; common cloud transport infrastructure does not grant shared data access.

[Permanent handshake runbook and exact receipts](../research/paired-relay/README.md).
