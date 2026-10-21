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
