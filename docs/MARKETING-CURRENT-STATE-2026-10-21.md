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
