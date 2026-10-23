# Business House Matrix — Cloud Multimodal Model Manager v1
Date: 2026-10-24
Status: SPECIFICATION ONLY — NOT IMPLEMENTED OR DEPLOYED
Owner: Matrix Super Brain; execution owner: Dev Matrix
Policy: quality-first, free-only, automatic fallback enabled.

## Objective
One cloud multimodal model-routing service for Super Brain and departmental brains. Super Brain owns task planning, permissions and approvals; this manager only selects, invokes, validates, and fails over model inference. Preserve existing workers, MCP/SSH integrations, API credentials and security gates.

## Scope
- Text, reasoning, code, research synthesis, image understanding, document interpretation, audio transcription and generation only when a verified provider/model supports the modality.
- Discover and reuse existing OpenRouter, Groq, NVIDIA and direct-provider adapters where actually installed; local Dell model is an optional offline fallback, not a cloud provider.
- No new keys, subscriptions, model purchases, account creation, deployment, changes to production or permission escalation in v1 planning.
- Do not claim provider availability from memory; inventory endpoints, entitlement, models, limits and modality via read-only checks after approval.
- Model licensing: record license, hosted-provider terms, and whether open-source/OSI compatibility is verified; do not silently treat open-weight as OSI-approved. Gate unsupported license policies.

## Architecture
Super Brain -> authenticated internal inference API -> policy/intent classifier -> capability registry -> eligibility filter -> quality-ranked candidates -> provider adapter -> output validation -> telemetry.
Fallback controller reranks remaining eligible candidates for transient failure. Department brains consume the same gateway and can provide task-specific capability requirements, but cannot override spending, privacy or authorization gates.

## Core request contract
POST /v1/route (internal authenticated only):
request_id, department, task_type, modality_inputs, output_modality, quality_tier, latency_budget_ms, context_tokens_estimate, data_classification, provider_allowlist, tools_required, max_attempts, idempotency_key, user_approval_ref.
Response: selected_provider, selected_model, model_version, reason_codes, result, latency_ms, attempts, fallback_used, token_usage_if_reported, cost_estimate, policy_decision, trace_id.
Additional read-only endpoints: GET /v1/models, GET /v1/providers/health, GET /v1/decisions/{trace_id}. No public unauthenticated inference endpoint.

## Registry record
provider_id, adapter_type, model_id, exact_revision_if_available, endpoint_reference (no secrets), modality_input/output, vision/audio/document/tool/json support, context_window, max_output_tokens, task benchmarks/evidence timestamp, latency observations, health status, rate limits, free_quota_evidence, price_per_token_verified, license_evidence, privacy classification, approved_data_classes, credential_secret_reference, enabled.
Mark unknowns as UNKNOWN, not supported or free by assumption.

## Routing algorithm
1. Authenticate caller, validate department scope, request size, modalities, classification and consent.
2. Reject tasks requiring external publishing, spending or privileged actions: inference routing never authorizes tool side effects.
3. Filter candidates: enabled + verified modality/context/tools + approved data handling + compatible license + healthy + confirmed zero-charge tier with remaining quota. UNKNOWN pricing is ineligible.
4. Rank eligible candidates primarily by measured task-specific quality (evidence freshness, evaluation reliability), then success rate, latency and remaining free quota. Never optimize for speed at expense of clearly superior quality without a stated latency constraint.
5. Invoke selected provider with deadline, bounded retries, structured output checks, trace ID and privacy-safe logs.
6. On 429, timeout, 5xx or provider unavailability, use exponential backoff only within budget then switch to next eligible provider; do not fall back to a provider with weaker privacy, modality, free-tier or license eligibility.
7. On schema/quality validation failure, one bounded alternate-model attempt if useful; return explicit error if none eligible. Do not conceal errors or fabricate success.
8. For mixed-modal workflows, route separate stages (e.g. audio -> transcription -> reasoning) with per-stage eligibility and provenance.

## Free-only cost control
Hard fail-closed zero-spend policy. No automatic top-ups, paid API calls, fallback to paid tiers or ambiguous free labels. Free quotas tracked per provider/model; if exhausted, return FREE_CAPACITY_UNAVAILABLE or use an approved local fallback. A $0 charge is not assumed from a zero cost estimate; confirm the provider's specific free entitlement and limits. Retain circuit breakers for cost and quota anomalies.

## Security and governance
Use existing secrets vault/environment injection; no credentials in Git, prompts, logs or mobile APK. Server-side gateway only; mobile clients receive short-lived scoped auth, never provider API keys. Encrypt transport, segregate department scopes, apply PII redaction/data classification, explicit retention limits, provider egress allowlist, per-tenant rate limits and audit trails. Protect against prompt injection and tool-call privilege escalation. Respect existing SSH/MCP, security denial and root permission controls. No publication, spending, deployment or permission change without explicit user approval.

## Telemetry and quality
Record request/trace IDs, department, task class, provider/model/revision, eligibility reasons, quality score/evidence version, health, timeouts, attempts, tokens and verified charges (if available), redacted failure codes. Do not log raw prompts by default. Benchmark suite: coding correctness, reasoning, multilingual, OCR/vision, audio, document extraction, schema adherence, prompt-injection resistance, fallback resilience, rate limit and quota exhaustion.

## Suggested open-source implementation components (subject to license/version review)
Python FastAPI internal service; LiteLLM or existing equivalent only if its actual current license and required features meet project policy; Pydantic request/response validation; PostgreSQL/Supabase existing persistence for registry/telemetry where authorized; OpenTelemetry-compatible metrics. Reuse existing Matrix runtime, do not create a parallel orchestration stack.

## Implementation gates (require separate execution approval)
G0 READ-ONLY INVENTORY: enumerate actual installed integrations and secret references without revealing values; identify owner, provider, license, current API reachability and free tier.
G1 DESIGN REVIEW: finalize adapters, routing scores, privacy policies, API schemas, threat model, migration/rollback.
G2 ISOLATED IMPLEMENTATION: feature branch, local mock providers, unit tests, no live paid inference.
G3 NON-PRODUCTION CERTIFICATION: consented free-only provider smoke tests, failure injection, zero-spend audit, security review, benchmark report.
G4 RELEASE APPROVAL: user reviews receipts, cost/license compliance, rollout plan; deployment separately authorized.
G5 CANARY/ROLLBACK: only after release approval; monitor zero-spend and quality thresholds.

## Acceptance criteria
- Verified free-only eligible models; no chargeable API path.
- Quality-first selection demonstrably chooses strongest eligible task model based on versioned evaluations.
- Automatic fallback on simulated 429/timeout/5xx, bounded retries and correct error when no eligible model.
- Multimodal inputs rejected gracefully unless compatible provider confirmed.
- Credentials never reach client or logs; access scoped and auditable.
- Existing integrations and security gates unchanged; full rollback documented.
- GitHub CI tests and receipts attached; no deployment without approval.

## Handover prompt
Continue Business House Matrix Cloud Multimodal Manager v1 from this document. First perform a READ-ONLY inventory of existing provider integrations and report exact availability, verified free quotas, licensing and security gates. Do not spend, deploy, rotate secrets, alter permissions or invoke paid inference. Present findings and G1 plan for approval before implementation.
