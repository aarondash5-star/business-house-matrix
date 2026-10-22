# Dev Matrix OpenRouter integration — 23 October 2026 IST

## Current state
ADAPTER_DEPLOYED / OFFLINE_QA_PASS / OWNER_KEY_ENTRY_PENDING / LIVE_INFERENCE_NOT_VERIFIED.
Owner authorized adding OpenRouter. Existing Dell development router extended on isolated branch feat/dev-groq-api-20261023; no merge or v6 controller enrollment. Selected slot openrouter-code, model cohere/north-mini-code:free. Slot stays disabled until credential validation and live sandbox QA pass. No OpenRouter inference has been sent as of readback6949fad6-a92e-4bb5-ae23-ffde7266c01b.

## Live selection correction
Original recommendation qwen/qwen3-coder:free relied on a still-visible model page. Live Dell catalog and endpoints were checked before asking for a key: catalog receipt5cc3f6e6-9a7a-4b2f-997e-0fc3626f8497 exit0 listed468 models and17 free variants, with no Qwen Coder free variant. Endpoint receiptcaeb71c0-e697-462c-b812-143a74d02a29 exit0 explicitly returned endpoints=[] for Qwen Coder free. It returned a Cohere endpoint for cohere/north-mini-code:free, zero prompt/completion pricing, context256000, and max_tokens support. This proves public advertised availability, not authentication or a successful inference.

North Mini Code Apache2.0 confirmed from original publisher https://cohere.com/blog/north-mini-code and https://huggingface.co/CohereLabs/North-Mini-Code-1.0 . Retained all existing NVIDIA license gates; did not substitute Nemotron, Gemma, or Poolside without the project's required license verification. Initial Qwen staging history retained in Git; current allowlist and policy select North Mini Code only.

## Bounded adapter
Reuse stdlib urllib/SQLite router; fixed endpoint https://openrouter.ai/api/v1/chat/completions and exact free-model allowlist. Explicit --public-input required; private inputs remain local-only, no tools, images, paid model fallback, plugins, redirects, or automatic model selection. Request provider settings data_collection=deny and max_price.prompt=0/max_price.completion=0; no privacy relaxation if this yields no eligible provider. max_tokens1024, prompt2048 UTF8 bytes, response65536 bytes, output8192 bytes, socket30sec/total45sec. Incomplete output, unexpected model ID, or reported nonzero cost rejected. Null cost is not independent billing verification.

Separate OpenRouter token ledger:7600 reserved units/minute,20000/day; prompt byte length+1536 conservatively reserved before requests, including failures. Local request caps20/day,2/minute, shared quota group openrouter-dev-one-account; these caps do not promise the provider's capacity. Existing Groq/NVIDIA quota ledgers retained. The free-only owner flag records authorized route selection, not a billing-account audit.

verify-provider openrouter-code calls only fixed /api/v1/key with redirect denial, bounded size/time, sanitized errors, and prints allowlisted numeric free-quota metadata only. It rejects management/provisioning keys; no key labels/account IDs/raw responses printed. Authentication success alone does not prove model inference.

## Executed tests and deployment
35/35 offline unittest cases passed locally after final model selection. The count comprises25 pre-existing/inherited regression cases plus10 OpenRouter-specific cases; it is not35 independent new security properties. New checks cover paid-model rejection before network/budget, private/tool rejection, zero-price/privacy payload, symlink credentials, response bounds, wrong-model/nonzero-cost output, isolated token budget, sanitized429, restricted key metadata, and CLI private-input rejection before reservation.

Final Dell stage/deploy receipt5c0d5d6a-50ae-4578-8350-2664f7326e74 completed exit0 at21:32:32.865Z, 35/35 cases passed, policy validate PASS, disabled slot installed. Final source SHA256 a71f670ab1ae1d49f6d2f61d46da2c02bc5fa0cc907aa8f03012b0fe6d308e45; source commit d3671318d1b2140b89e851064806fccadcb188f7, tests a792accfe2069a1658f6843fc4b6d43ba7a36ee4, smoke evaluator2dd617747b70f5d68d609017462a6253ad6eb8cc. Files brain/dev-router/matrix-route.py, test_api.py, smoke_openrouter.py.

Earlier staging receipt635a46ee-4782-4588-b622-afb44285c4e3 exit0 tested the initial Qwen candidate; receipt9cce5a90-b328-4899-993c-cd221d5b3391 exit0 installed it disabled. Readback a640c3e0-1f95-4c89-839d-c3edaad77c33 exited1 after verifying entry and state, because its Qwen inventory lookup raised StopIteration. This triggered the live-catalog correction; do not relabel that receipt as success or infer a provider outage from it.

Final separate readback6949fad6-a92e-4bb5-ae23-ffde7266c01b completed exit0: correct final source hash; OpenRouter disabled and key absent; zero OpenRouter inference reservations; every pre-existing connection unchanged; Groq OSS120/OSS20 enabled; NVIDIA routes disabled; v6 active and checksum b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e unchanged.

## Owner secure entry and next action
Reuse https://dell-private-login-ui.vercel.app/ and existing owner PIN/ECDH-AES-GCM input relay. Focused masked terminal verified. New specific transient unit matrix-openrouter-code-owner-enroll-20261023.service runs existing enroll openrouter-code --free-plan-confirmed with NoNewPrivileges and RuntimeMaxSec1800. Superseded initial entry unit was stopped by exact name before replacing the disabled candidate. No browser profile, relay, SSH service, sudo/root policy or permissions changed.

Owner creates a regular inference key at https://openrouter.ai/settings/keys without buying credits, then sends it through Private text to Dell and Enter, never chat. Existing enroll refuses overwrite and saves private0600 credentials in the existing vault.

After owner entry: verify only file metadata, call verify-provider openrouter-code and inspect provider-reported remaining free quota. Then one bounded public coding request through ~/.local/share/matrix-dev-router/openrouter-north-stage-20261023/smoke_openrouter.py. It tests a clamp function with six independent assertions in existing Bubblewrap: no network, clear environment, read-only mounts, Python isolation, CPU/memory/file/deadline bounds. Evaluator is staged, not yet executed against a model. Use try/finally to disable on any API/QA failure; no paid substitution, privacy bypass, repeated retry or expanded deadlines. Only after API+QA PASS consider enabling public development routing.

## Open Source / Reuse / Cost Gate and rollback
Reuse existing owned Python/SQLite router, secure vault/relay, Bubblewrap, Git branch and local fallback. North Mini Code weights Apache2.0; no model weights redistributed or new SDK/package installed. Hosted OpenRouter is an external service and is not represented as open-source infrastructure. Its use was explicitly selected by owner. Fixed :free model plus provider price ceiling; no paid subscription, credits purchase or chargeable calls authorized. Free quotas/availability can change. Official schema/privacy/limits references:
- https://openrouter.ai/docs/api/reference/overview
- https://openrouter.ai/docs/guides/routing/provider-selection
- https://openrouter.ai/docs/guides/privacy/data-collection
- https://openrouter.ai/docs/api_reference/limits
- https://openrouter.ai/docs/api/api-reference/api-keys/get-current-api-key

Pre-OpenRouter source/policy snapshot ~/.local/share/matrix-dev-router/backup-openrouter-20261023 retains the working Groq+paused-NVIDIA state. Reconcile newer changes before restoring those exact files with original modes. Keep all keys, receipts, staged files and quota ledgers. Do not restore older pre-Groq snapshots. Business House Matrix remains independent from Moksha Master; no shared registry federation or FULLY_SYNCED claim.
