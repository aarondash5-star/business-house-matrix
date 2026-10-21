# Marketing Matrix — Modular Third-Party API Router (Mac, 2026-10-21)

## Scope and provenance
The Mac's Marketing router is based on the **actual Dell Matrix Dev modular router** at:
- Dell: \`/var/lib/generic-linux-automator-exec/.local/share/matrix-dev-router/matrix-route.py\`
- Dell reference: \`/opt/business-house-matrix/MATRIX_API_ROUTER_2026-10-20.md\`
- Mac: \`/opt/business-house-matrix/marketing/brain/router.py\`
- Canonical source: \`marketing/mac-brain/router.py\` and \`provider-policy.template.json\` in this repository.

Reuse: policy-defined provider/model slots, priority by task, grouping quotas across same account, SQLite UTC ledgers, reserve-before-send, cooldown/retry, secure private credential vault, explicit human enrollment and no-paid policy. Mac uses bounded Python stdlib HTTPS instead of Dell's Pi CLI: original Pi npm package is deprecated, additional packages are unnecessary for text-only marketing drafts, and online AI workers are not granted shell tools.

## Configured hosted slots (disabled until enrolled)
| Slot | Provider/model | Roles | Local conservative max |
|---|---|---|---|
| groq-creative-oss120 | Groq openai/gpt-oss-120b | Creative/research/review | 40 requests/day, shared |
| groq-copy-qwen | Groq qwen/qwen3.8-27b | Copy/vision/fast | Shares same Groq key and budget |
| cloudflare-vision-qwen | Cloudflare @cf/qwen/qwen3.8-27b | Vision/copy/creative | 8 requests/day, 2/min |
| openrouter-free-qwen | OpenRouter qwen/qwen3.8-27b:free | Emergency fallback | 8 requests/day, 2/min |

All hosted slots initially \`enabled:false\`, \`free_plan_confirmed:false\`; Mac Brain \`online_enabled:false\`, \`publish_enabled:false\`, \`spend_enabled:false\`, \`local_inference_enabled:false\`.

**Important:** Cloudflare's real free budget is 10,000 neurons/day, **not** 8 requests; the conservative cap cannot prove unused free neurons. The provider account must be Workers Free (no paid upgrade). OpenRouter free variants are rate limited and the local cap is tighter than the vendor's. Groq Free model/request/token ceilings vary per model/account; local counters are only guards, not vendor billing proofs. No paid calls are permitted.

## Operations (interactive Mac terminal only)
Use the dedicated Marketing service account with permissions to \`/opt/business-house-matrix/marketing/brain\`. Do not paste API keys into ChatGPT, shell commands, logs, or GitHub. Enrollment uses a **hidden interactive prompt** and writes key files under \`secrets/\` with 0600 permissions.

\`\`\`bash
cd /opt/business-house-matrix/marketing/brain
python3 router.py validate
python3 router.py status

# Before each enrollment: verify the provider account uses Free plan and billing cannot incur charges.
python3 router.py enroll groq-creative-oss120 --free-plan-confirmed
python3 router.py activate groq-creative-oss120
python3 router.py activate groq-copy-qwen
# Cloudflare account ID is not the API key:
python3 router.py set-account cloudflare-vision-qwen --account-id YOUR_32_CHARACTER_HEX_ACCOUNT_ID
python3 router.py enroll cloudflare-vision-qwen --free-plan-confirmed
python3 router.py activate cloudflare-vision-qwen
python3 router.py enroll openrouter-free-qwen --free-plan-confirmed
python3 router.py activate openrouter-free-qwen

python3 router.py status
\`\`\`

Provider keys are **not present** as of initial installation. The Mac's automated SSH job runner is noninteractive, so never pass keys with \`linux_ssh_run\` command arguments. Use an approved interactive terminal/credential gateway.

Once an account has been verified and a bounded live smoke test performed, a separate policy update must set \`online_enabled:true\` in the Mac's private \`config.json\` before the queued \`hosted_draft\` job type can make hosted calls. Do not enable automatically merely because a key was enrolled.

## Operator quick checks
\`\`\`bash
cd /opt/business-house-matrix/marketing/brain
python3 test_router.py
python3 test_brain.py
python3 router.py validate
python3 router.py choose --profile creative
python3 router.py status
python3 brain.py status
\`\`\`

A \`choose\` result of \`null\` while no account is enrolled is **expected**. No cloud inference was performed during installation.

## Control plane behavior
- Allowed profiles: creative, copy, research, vision, review, fast.
- Only fixed, allowlisted models/endpoints. No arbitrary URL, tools or user-provided executable arguments reach providers.
- \`hosted_draft\` is the only online task attached to the Brain queue; output is a draft and cannot publish content.
- Requests are reserved in SQLite **before** invoking vendor APIs; group quotas prevent multiple Groq slots from manufacturing extra daily capacity.
- For non-side-effecting drafts, failures cause 15-minute cooldown and bounded failover across different slots.
- A provider's HTTP 429, error, exhausted cap, missing/unsafe credential, plan-ineligible slot or unavailable free model makes that slot ineligible.
- If no eligible free endpoint remains, jobs fail with an auditable receipt rather than using paid or thermally restricted local inference.
- Local Qwen creative inference on this Mac remains explicitly disabled after the 90°C test.
- No credentials, runtime policy, quota SQLite, media, logs or outputs belong in the public repo.

## Verified 2026-10-21
- Mac router source installed, schema validation PASS: four slots, paid inference denied.
- Six synthetic isolated router tests PASS: strict allowlist, all-disabled no-network status, fail-closed run, interactive enrollment restriction, grouped quota enforcement, and simulated 429 automatic fallback with two auditable reservations.
- Four preexisting Brain unit tests PASS and online-task disabled guard PASS.
- File permissions: credential vault 0700, policy/router/quota database 0600.
- Cloudflare account-ID format negative test PASS.
- Bridge, Ollama and cron remain active. Reel Studio is untouched.
- **No real provider authentication, billing eligibility or live hosted response tested**, because provider keys were absent.
- Two-stage rollout remains: securely enroll -> validate actual response and vendor usage/rate headers -> enable policy at the Brain -> benchmark creative quality -> link Reel Studio output.

## Rollback
1. Keep \`online_enabled:false\` in \`config.json\`.
2. Disable hosted slots using \`python3 router.py disable SLOT_ID\`.
3. Preserve audit database \`provider-quota.sqlite3\` and private vault before removing router files.
4. Restore \`brain.py.rollback-pre-router-integration\` if reverting the hosted task.
5. Existing Mac cron, Ollama, Generic Linux SSH and Reel Studio are unaffected by this module.


## Groq-first activation — 2026-10-21
Groq remains the first preferred provider. The existing two Groq slots share one securely enrolled key and a conservative 40-request-per-day accounting group.

Verified official Free-plan docs: both \`openai/gpt-oss-120b\` and \`qwen/qwen3.8-27b\` are listed at 30 RPM, 1,000 RPD, 8,000 TPM and 200,000 TPD as standard Free plan limits (subject to the account dashboard). Source: https://console.groq.com/docs/rate-limits . Groq's API supports chat completions at \`https://api.groq.com/openai/v1/chat/completions\` (source: https://console.groq.com/docs/api-reference).

Groq key creation: https://console.groq.com/keys ; Free plan: check Billing and Limits in https://console.groq.com/settings/limits.

**From the Mac's human login, interactive terminal** (not SSH job arguments):

\`\`\`bash
sudo -u generic-auto-exec python3 /opt/business-house-matrix/marketing/brain/router.py enroll groq-creative-oss120 --free-plan-confirmed
sudo -u generic-auto-exec python3 /opt/business-house-matrix/marketing/brain/router.py verify-provider groq-creative-oss120
sudo -u generic-auto-exec python3 /opt/business-house-matrix/marketing/brain/router.py verify-provider groq-copy-qwen
\`\`\`

The enrollment step prompts invisibly and saves a 0600 secret file. \`verify-provider\` checks authentication and model availability via the authenticated model-list endpoint, **without performing inference**. Activating the slots is a separate decision; leave \`online_enabled\` false until Groq Free plan/no-billing is confirmed and a bounded live test has passed.

Current status: Mac online and queue active, **no Groq key enrolled**, Groq slots disabled. A no-credential verification was tested to fail safely and ten isolated router/brain regression tests passed after adding the authenticated model check.

## Groq live activation — 2026-10-21, 16:50–16:52 IST
- The owner completed secure interactive Groq key enrollment and Free-plan confirmation.
- **Live checks:** `verify-provider` authenticated both `groq-creative-oss120` and `groq-copy-qwen` using the single private key (file mode 0600) and returned available model IDs, without inference for these checks.
- Activated both slots; preserved the shared `groq-one-account` quota group. `online_enabled:true` set in Mac private Brain configuration with rollback copy `config.json.pre-groq-live`.
- Real GPT-OSS 120B creative smoke request succeeded using `https://api.groq.com/openai/v1/chat/completions`.
- Real Qwen3.8 27B copy request via autonomous Brain queue and worker succeeded, job `b14cb180-1253-4eac-8567-7793ce5c956f`, state `completed`, receipt persisted, attempt 1.
- Local ledger recorded **2 requests total** shared across Groq slots. This is local request accounting, not a provider-confirmed billing statement.
- `publish_enabled:false`, `spend_enabled:false`, `local_inference_enabled:false`. Cloudflare and OpenRouter still disabled and credentialless. Generic SSH, Ollama, cron remained active.
- **Creative QA needed:** a sample generated hook asserted unverified "zero waste". Draft outputs require factual/brand review before any customer-facing publication.
- **Operational QA outstanding:** compare two recorded calls against Groq dashboard meters and perform real 429/free-limit checks during normal free-tier use; do not synthesize a real rate limit by deliberately spamming an account.
- No changes to Dell, Moksha Master, or existing Reel Studio.


## Newly shortlisted: Tavily research + Gemini Flash — 2026-10-21

Both candidates have been registered **disabled**, preserving the existing live Groq credentials and operational routes.

### Tavily — research tool, NOT an LLM
- Role: trend research, competitive-intelligence discovery, external source lookup, factual checks for reel drafts.
- Vendor Researcher Free plan: **1,000 API credits per month**, no credit card required; credits reset on the first day of each month. API usage stops at the free cap unless the plan is upgraded.
- Registered in `provider-policy.json` under **`tool_connections`**, ID `tavily-search` (not as an inference slot).
- Current state: `enabled=false`; no credential and no Tavily API adapter/network call. The router actively rejects activating this tool until a separate dedicated research adapter, secure credential path, external-service licensing review, and quota controls pass testing.
- Suggested initial operational budget after approval: **100/1,000 monthly credits**, basic-depth search only, evidence links retained.
- Official sources: https://www.tavily.com/pricing , https://docs.tavily.com/documentation/api-reference/endpoint/search

### Gemini 2.5 Flash — multimodal model candidate
- Official Gemini API Free Tier includes input/output at no monetary charge on supported models and project-specific rate limits. Free-tier prompts/responses may be used to improve Google products.
- **Proprietary model**: conflicts with Business House Matrix's default open-source-only model-selection policy. No exception has been approved.
- Registered as `gemini-flash-candidate`, `provider=gemini`, `model=gemini-2.5-flash`, with `enabled=false`, `model_license_approved=false`, `license_review_required=true`, `free_plan_confirmed=false`.
- Adapter explicitly blocks Gemini API invocation pending a conscious model-licensing and data-processing decision. No Google API key stored or requested. Do not send unpublished customer footage, guest data or business-sensitive assets through the free tier.
- The associated API project must remain Free Tier without paid billing; free quotas, data processing and access are specific to the actual account.
- Official sources: https://ai.google.dev/gemini-api/docs/pricing , https://ai.google.dev/gemini-api/docs/billing

### Verification and rollback
- Existing production Groq creative and copy slots were left enabled and credential reference unchanged, with ledger intact.
- Added fifth **model candidate slot** and first **research-tool candidate** using additive configuration migration only.
- Regression: seven router tests and four Brain tests PASS. Active Groq route selection and cron, Ollama, Linux SSH bridge health PASS; no external inference or Tavily search executed.
- On Mac, rollback files `router.py.pre-tavily-gemini-20261021` and `provider-policy.json.pre-tavily-gemini-20261021`.
- Activation not part of this shortlist update. Next gated milestone: Tavily research-adapter licensing evaluation, then Gemini open-source-policy exception decision and private-data processing assessment.
