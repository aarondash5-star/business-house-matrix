# Gate S Supervisor — Real Equal-Prompt Inference Evaluation (23 Oct 2026)

**Decision: NO PROMOTION; CERTIFIED v6 UNCHANGED.**

## What was executed
- User expressly authorized the proposed fixed-function Gate S evaluation through the existing secure free-only Dell model router, not changing the live controller.
- Docker, SSH authentication/security, provider-credential vault, paid API policy, Git merge, source approval and production permission controls all retained.
- Source on isolated branch `feat/dev-supervisor-gate-s-20261023`, runner `benchmarks/gate_s/andaz_router_comparison_v1.py`, commit `30956046f6ab81598a3379f1cf84c2fd0d1c68c8`.
- The trusted existing router `~/.local/share/matrix-dev-router/matrix-route.py` caps public input at 2048 bytes, completion at 1024 tokens, no tools, no redirects, secure local key vault, $0 cost (reject any nonzero OpenRouter cost), daily/minute quotas and provider identity. **These limits were NOT weakened.** Rich context is therefore broken into three independently reviewed phases: discovery, build, verify.
- Exact model/provider IDs from router preflight: `local-qwen` -> `qwen3:4b-instruct`, `openrouter-code` -> reviewed Apache-2.0 North Mini Code free model, `groq-oss120` -> `openai/gpt-oss-120b` (ready zero-paid).
- Payload is public non-sensitive text. All plans return only proposals; no worker dispatch or website/PMS access. Prompt hash is recorded for identical model comparison.

## Verified terminal results (no successes inferred from queued tasks)

| Run | Model / slot | Phase | Prompt SHA-256 (prefix) | Result | Duration | Terminal SSH receipt |
| --- | --- | --- | --- | --- | ---: | --- |
| 1 | OpenRouter dynamic free / `openrouter-code` | discovery | `406d06fc4bc8` | **FAIL**, `OPENROUTER_POOL_FAILED_RuntimeError`; no usable model response | 21.087 s | `43b7b6b3-a77e-40b1-86ea-48a271cc523a` |
| 2 | Groq `openai/gpt-oss-120b` | discovery | `406d06fc4bc8` | **PASS structured**, five detailed plan tasks | **3.016 s** | `9691d1f3-b8a4-4606-a42d-7861ae83eab0` |
| 3 | Local Ollama `qwen3:4b-instruct` | discovery | `406d06fc4bc8` | **FAIL**: local CLI/model exceeded 115-second cap without valid plan | 115.104 s | `8a31b7ec-53f9-45cc-a293-338e76d4621d` |
| 4 | Groq `openai/gpt-oss-120b` | build | `56075e88e6e` | **FAIL structured validation**: model assigned combined role `security|review`, which is not in allowlist | 2.898 s | `97798ded-2977-4c98-81fe-e72c05cee63c` |
| 5 | Groq `openai/gpt-oss-120b` | verify | `c91ad347eac8` | **FAIL**: router reported `PROVIDER_OUTPUT_INCOMPLETE` | 3.013 s | `36fcae98-83f6-498f-8cbc-a2e699e56d6a` |

- Detailed immutable local receipts: `~/matrix-gate-s-andaz-comparison-20261023/{north-discovery,oss120-discovery,local-discovery,oss120-build,oss120-verify}.json`.
- Model inference against **exactly the same 1241-byte discovery prompt** (matching SHA above): Qwen timed out, Groq GPT-OSS 120B passed, OpenRouter routed request failed. This demonstrates Groq model responsiveness and usable structured output for **one phase**, not end-to-end supervisor autonomy.
- Hosted GPT-OSS 120B discovery: proposed (1) site/PMS booking audit, (2) three competitor evidence comparison, (3) IA and 6–8 mobile wireframes, (4) photo copyright/rights ledger, (5) baseline security report. Each has deliverable, acceptance, dependencies. Prompt tokens 351; completion 930; finish reason stop. **Quality caveat:** contains inappropriate assumptions that admin/password access to WordPress/PMS/WhatsApp logs will be given; arbitrary 90%-under-three-taps UX benchmark and 5% scan false-positive target not independently justified. The output remains untrusted planning text.
- Groq build output was otherwise substantive, but `security|review` is an unapproved combined role and **correctly rejected**. It also invented assumptions that the PMS uses REST API, WhatsApp uses webhooks, staging could be WP Engine, and that opening WhatsApp would decrement inventory. None are verified or automatically authorized.
- Groq verify output was incomplete per router and was therefore never approved. **No model produced an accepted complete Andaz plan on the current restrictive single-response hosted transport.**
- Neither unsuccessful run was replayed; no silent failover/promotion.

## Interpretation
| Dimension | Qwen 4B on Dell | GPT-OSS 120B hosted | North Mini Code free |
| --- | --- | --- | --- |
| Same discovery input | YES | YES | YES |
| Returned complete parseable planning proposal | NO | YES, 5 tasks | NO |
| Time | 115.104s timeout | 3.016s | 21.087s router error |
| Full 3-section robust plan | NO | NO (only 1 of 3 valid) | NO |
| Permission boundary | preserved | preserved | preserved |
| Ready to replace Gate S/v6 | **NO** | **NO** | **NO** |

**The older 16-task GPT-6 authored Andaz reference remains a benchmark target, not a fair independent provider comparison.**

## Confirmed infrastructure and security after runs
- Dell `bhm-autonomy-controller.service`: **active**.
- Protected controller `controller.py` SHA-256 remains `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`, checked in terminal `6f7a1b48-ee63-4b25-bb04-f3fdfb4867e7`, exit 0.
- Mac still offline at last checked heartbeat. No cross-host certification.
- No production merge, deployment, spending, live Andaz website change, secrets copying, unbounded shell, connector safety bypass or provider policy change.

## Root issues and next fixes (needs separate candidate and fresh enrollments)
1. Hosted inference free-only router has legitimate strict 2048-byte input and 1024-completion-token limits. For detailed plans **use additional small fixed-function phases (2–3 tasks each) and assemble a DAG** with independent semantic QA, or approve a separate explicitly reviewed length-bounded supervisor endpoint; never weaken existing shared router policies.
2. Strengthen the supervisor contract to force **one exact role per task**, independent QA/security/owner approval, and explicit unknowns/source claim markers. A role like `security|review` must fail closed.
3. Benchmark on unseen tasks and include factual hallucination checks. Do not treat descriptive model assertions of PMS REST API or WordPress staging provider as evidence.
4. Address the local CPU 115s planning timeout (reduce local target or use remote specialized supervisor through approved $0 channels); do not use Qwen 4B as the high-frequency default.
5. Investigate OpenRouter pool denial through existing router-owner review with terminal redacted diagnostic. Do not bypass the pool/429 or free-only gates.
6. Repeat equal prompts on at least two fully approved provider models, track per-phase valid ratio, semantic QA, token/latency/cost, negative worker failure tests, Mac cross-host independent QA, and human release approval.

**Final NO-GO:** No promoted supervisor, no automatic live adapter, Gate E still NO-GO. All new work isolated on Gate S branch.
