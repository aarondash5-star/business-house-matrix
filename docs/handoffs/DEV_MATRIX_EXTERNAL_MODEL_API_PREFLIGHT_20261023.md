# Dev Matrix external coding-model API preflight

23 October 2026 IST. Owner requested outside API integration and selected AI coding models. Status: existing router found and validated; external inference NOT activated or certified.

## Verified live state

Dell and Mac authenticated online, all three lane heartbeats fresh. Dell existing stdlib router `~/.local/share/matrix-dev-router/matrix-route.py` validates policy and zero-paid allowlist. All seven external slots disabled and all their credential references missing. This was checked using existence/mode metadata only; no key contents read or copied. `choose --profile coding` selects local-qwen (`qwen3:4b-instruct`). This proves selection, not fresh inference.

Existing Groq slots: groq-qwen-primary, groq-qwen-secondary, groq-oss120, groq-oss20. OSS120/OSS20 reference primary credential; secondary has a separate reference. NVIDIA OSS20 and Nemotron, and Cloudflare GLM are disabled. Nemotron additionally has license_review_required=true. Configured model IDs are historical candidates, not current provider availability or license certification.

Dell v6 controller active and SHA256 unchanged: b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e. Existing RC1 QA checkout contains uncommitted runtime work; preserved without edits. Gate E remains subject to its separate certification gates.

Terminal receipts, all completed exit 0: a284b940-c75a-4ba7-86a6-f769d75a25e9 (router status/validate and source inspection); 6b740a8a-ca33-4ed7-9d63-7b1ceaf0a212 (credential metadata, selection, v6 health/hash); 06e5446e-b511-4eb2-a4d7-0b55802ff751 (credential references and quota groups).

## Concrete activation sequence

1. Owner enrolls a Dev-scoped Groq Free credential using the existing hidden terminal prompt, as the existing Dell executor user:

```sh
python3 ~/.local/share/matrix-dev-router/matrix-route.py enroll groq-qwen-primary --free-plan-confirmed
```

Do this only after verifying the account is actually Free with no chargeable fallback. Never put the key in chat or GitHub. Do not copy Marketing credentials automatically.
2. Reverify official provider model inventory, upstream model licenses, free-plan limits and account billing before selecting exact models. Existing `verify-provider groq-oss120` / `groq-oss20` checks authenticated model availability without inference. A model-list response does not verify free billing or model license.
3. Before activation, reconcile account-wide and per-model quota guards: current Groq OSS and Qwen slots use different quota groups despite shared primary credential. Add account-wide token/request caps and fail-closed billing attestation; do not describe local counters as provider billing proof.
4. Preserve local private profile. Stage an external public/synthetic-text proposal route using the existing router, with explicit deadlines/output/token bounds, no tools/MCP/context files, and no private source transport. Independent Bubblewrap QA evaluates generated output. No direct modification of the Gate E offline-only model adapter or certified v6 without its release gates.
5. Test missing credentials, rejected model/license, quota exhaustion, 429 cooldown, timeout, no paid fallback and local fallback offline. Then one bounded public coding request, record actual model/usage and independent QA. Enable only verified slots with conservative budgets and rollback copy.

## Open source / reuse / cost gate

Reuse installed Python stdlib/SQLite, existing router, Pi harness, local Ollama models and Bubblewrap. No new service, dependency, credential transport or paid call created. Upstream model/provider/license/plan revalidation is pending, so no new provider/model recommendation is certified. NVIDIA and Cloudflare remain disabled; no license or provider gate waived. No publishing, merging, permission changes or production controller edits performed.

Blocking next input is secure owner credential enrollment plus actual free-plan verification. No live external smoke test can truthfully be claimed before those prerequisites. This document records preflight only, not completed API integration.
