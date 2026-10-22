# Dev Matrix — Groq API integration, 23 October 2026 IST

## Decision
VERIFIED_LIVE bounded public coding routes: GPT-OSS 120B and GPT-OSS 20B. Both returned real completions and independently generated code passed six assertions each inside no-network Bubblewrap. Qwen 3.8 27B authenticates/model inventory PASS but completion returned HTTP 429; left disabled with a 900-second local cooldown marker. Its inference capability is NOT certified and it must not automatically re-enable. No claim of Gate E production signoff or full general autonomy.

## Secure credential enrollment
Owner used existing Dell HTTPS PIN/owner gateway, P-256 ECDH/AES-GCM input relay and hidden terminal prompt. Owner explicitly instructed assistant to perform Free-plan confirmation. Existing Dev key reference groq-qwen-primary is present with private file permissions. No key contents were printed, committed, copied to Mac or shared with Marketing. Receipt e501e0d5-54d3-4eab-b427-99949e8ec032 completed exit 0: secure metadata and authenticated model-list checks PASS for groq-oss120, groq-oss20 and groq-qwen-primary. Free plan is OWNER_ATTESTED, not an independent billing-console audit.

The visible encrypted entry repair is separately source-versioned in karanzing1992/engagement-core, branch fix/dell-secure-keyboard-20261023, docs/incidents/DELL_SECURE_KEYBOARD_FIX_20261023.md. This does not reconnect Business House Matrix to Moksha Master.

## Implemented in existing router
Existing path ~/.local/share/matrix-dev-router/matrix-route.py. Source snapshot: brain/dev-router/matrix-route.py, code commit ad88afd2deaa210931d105c74de5c8c32a54bdfb. Final runtime SHA256 71dba31ba6a83a5ce1eaafc135b362d7b70264ec7f74f31909d31f2401e52d8c.

- Reuse Python stdlib, urllib, SQLite quota ledger, existing owner vault, provider slots and local Pi/Ollama fallback. No dependency, paid platform or duplicate service installed.
- Groq text-only calls require explicit --public-input and reject tools. Calls without public confirmation select local-only; explicit external slot without confirmation rejects BEFORE reserving or sending. This flag is an operator declaration; it is not an automatic secret classifier. Do not pass private data.
- Fixed HTTPS completion endpoint; redirects denied; 30-second overall alarm, 15-second socket timeout, 65,536-byte response ceiling, 8,192-byte answer ceiling, 2,048-byte input cap, 1,024 completion-token cap. Incomplete output fails closed.
- Shared Groq request group: 20/day and 2/minute across all existing Groq slots. Additional conservative token reservations (prompt bytes + 1536) aggregate account-wide with 7600/minute and 80000/day local ceilings. Failed calls still consume reservations. These local guards cannot observe other keys/apps or prove billing.
- Accurate application User-Agent BusinessHouseMatrixDev/1.0 with public project URL. Default urllib POST was rejected with HTTP 403 and non-JSON error code 1010. An upstream maintained Groq integration also uses an application-specific User-Agent; no browser impersonation, proxy, credential/account change, authentication or quota bypass was used. Exact same host, key and endpoint then returned successful completions.
- Existing non-Groq provider settings and MCP tool connections preserved. Qwen secondary, Cloudflare and NVIDIA remain disabled. Existing local Qwen/Granite routes retained. No new private repository transport or model tool execution.

Usage for public text only:
```sh
python3 ~/.local/share/matrix-dev-router/matrix-route.py run --public-input --profile reasoning 'PUBLIC coding brief'
python3 ~/.local/share/matrix-dev-router/matrix-route.py run --public-input --profile fast 'PUBLIC coding brief'
python3 ~/.local/share/matrix-dev-router/matrix-route.py choose --profile private
```
Explicit single-model QA uses --slot groq-oss120 or --slot groq-oss20 with --no-fallback. Real generated code must still undergo isolated independent QA; the model response is not proof of correctness.

## Test evidence
- Original bounded adapter: 11/11 offline tests PASS, receipt f4924809-d345-4c5c-bfc3-fa9eb2a6dcde, exit 0.
- Final accurate-client-header candidate: 11/11 tests PASS, receipt a08c6b83-0854-4b8e-8022-ef5c3e064834, exit 0. Source/test isolated at api-stage-v2-20261023. Includes missing key, unsafe modes, public/tool gates, attestation, prompt cap, payload/token caps, timeout, incomplete output, shared token budget and redirect denial. Test source: brain/dev-router/test_api.py.
- GPT-OSS120: receipt 80b0cbe3-d775-401f-a656-c499f77e918d completed exit 0; generated add function independently passed 6 assertions in Bubblewrap with network unshared, read-only generated source, CPU/memory/time limits. Provider reported 102 prompt + 26 completion =128 tokens.
- GPT-OSS20: receipt 91f3e396-07d2-437e-956e-7fc74cbfba55 completed exit 0; generated is_even function passed 6 independent assertions under same isolation. Provider reported 106 prompt +28 completion =134 tokens. Exact fixture/evaluator: brain/dev-router/smoke_api.py. Its existing Dell paths must be adapted on another host.
- Qwen real completion: receipt 91807259-976c-4395-8849-cff6d0c6fb85 failed exit 1 with HTTP429; not a QA pass. No retries against that throttled model. Explicitly disabled and set one bounded local 900-second cooldown marker using existing CLI; that marker is a conservative local policy, not a claim about provider Retry-After.
- Postflight receipt 5bb3bce0-8f37-47bb-acfc-5da77199a761 completed exit 0: missing-public confirmation rejected exit2, API reservation count unchanged, private profile chooses local-qwen, v6 service active and controller checksum unchanged b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e. Temporary owner enrollment terminal stopped after key enrollment.

## Honest failure history and boundaries
Initial urllib inference returned403. Diagnostic d07e48b5-400a-49ed-8737-8418f4a5f29c identified non-JSON1010. One later release attempt da717b3d-8ca0-4193-8c38-10f649149b10 stopped source replacement on assertion because an older development-lane patch was still queued; its separately issued smoke failed403. Corrected by using a new isolated v2 stage, completing tests and only then replacing live source. Keep failed receipts; do not label them successful.

Dell control lane and later development lane became stale during the session. Operations lane delivered terminal QA/release receipts. Do not restart workers, change permissions or replay uncertain jobs to conceal delayed delivery. Old queued stage edits target only the old isolated stage, not the released v2 source.

Frozen v6 controller, Gate E PR13, original pilot and historical receipts untouched. Gate E offline-only model adapter was NOT switched to remote inference; its production gates still apply. This integration exposes bounded public coding through the existing router, not production controller enrollment for private tasks.

## Rollback and remaining work
Before deployment, backups of original router/policy were saved at ~/.local/share/matrix-dev-router/backup-groq-20261023. Preserve quota.sqlite3, keys and all historical receipts. Disable both hosted slots first for immediate local-only routing. Restore source/policy from that backup only after reconciling any later changes; do not revert shared unrelated settings. No merge performed.

Remaining: provider-authorized Qwen quota investigation/recheck once eligible, independent Free billing-console validation, longer coding benchmarks, supervised task/controller enrollment only through Gate E approvals. Mac shared credential transport not added. Current source is on isolated feat/dev-groq-api-20261023 branch.

## Open source / reuse / cost evidence
Official Groq model inventory and Free plan limits: https://console.groq.com/docs/models and https://console.groq.com/docs/rate-limits . Model licenses checked from original publishers: https://huggingface.co/openai/gpt-oss-120b , https://huggingface.co/openai/gpt-oss-20b and https://huggingface.co/Qwen/Qwen3.8-27B/blob/main/LICENSE (Apache2.0). Existing custom stdlib code extended; no upstream implementation copied. Reference for accurate application header: https://github.com/langchain-ai/langchain/blob/master/libs/partners/groq/langchain_groq/chat_models.py . Groq is the owner-approved hosted API; no claim its hosted platform is open-source. No paid plan, spending, package installation, root/sudo or network permission change.
