# Business House Matrix — Third-Party AI Provider, Budget and Independent QA Policy V1

**Policy ID:** DLT-BHM-PROVIDER-BUDGET-QA-001 · **Version:** 1.0.0 · **Approved:** 2026-10-30  
**Applies to:** Concept, Design, Development, QA/QC, Marketing, Sales, Accounts, Support, EVOLUTION, including sub-Brains.  
**Parent:** [Task Assignment SOP V1](THIRD_PARTY_AI_API_TASK_ASSIGNMENT_SOP_V1.md). **Enforcement status:** policy documented; no new runtime dispatcher or financial authority enabled.

## Provider admission registry (policy contract, not activation)

Each department maintains a **project-specific** allowlisted provider record. Never copy actual credentials or business records into the public registry. A record must include:

| Field | Admission requirement |
| --- | --- |
| `provider_id` / `model_id` / `account_group` | Exact allowlist; all slots sharing one provider account share a quota/budget ledger |
| `authorized_departments` / `authorized_projects` | Positive owner-approved scope, host/data boundary; never global-by-implication |
| `endpoint_allowlist` | Pinned HTTPS API product/interface; no arbitrary proxy/URL |
| `model_license` / `dependency_license` / `service_terms` | OSI review for source/model policies and separately vetted service terms; any proprietary exception explicit, not inferred from this SOP |
| `enrolled_and_enabled` | Both true from existing authenticated runtime state; documents never flip these flags |
| `data_policy` | Explicit data-transfer authorization, retention, provider training terms, geographic processing, privacy classification |
| `billing_tier_verified` / `quota_proof` | Actual authorized account plan/limits; no assumptions from generic marketing pages |
| `price_snapshot` | Timestamped exact model rates for input/output/cached write/read/storage/batch/tools and currency |
| `qualifications` | Task-profile benchmark QA, first-pass acceptance, rate/quota, quality confidence, measured cost |
| `health` / `cooldown` | Auth status, 429 Retry-After, circuit breaker, thermal limits for local fallback |
| `last_verified_at` / `expires_at` | Finite freshness window; stale, missing or ambiguous provider rights => ineligible |

**Candidate != approved != active.** Existing previously enrolled providers retain their *existing* explicit permissions and operational status; this document neither activates nor disables any. Gemini, OpenAI/other proprietary models, free inference websites and hosted open-weight endpoints require separate license/processing approval wherever the Matrix's OSI-only policy would otherwise exclude them. A provider may be considered but remain **disabled**.

## Budget hierarchy and zero-spend default

Before a request, effective allowance is the minimum of: globally permitted project spend, departmental allocation, tenant/project allocation, shared provider account cap, daily/sprint cap, ticket cap and single-call cap.

- Default for **new** routes and budgets: **paid allowance = zero**, **dispatch authorization = false**. A free plan does not authorize a new provider call under this documentation-only approval. Existing approved free slots remain governed by their prior authorization.
- Hard max for repair attempts **2 per task**. Original call and reattempt accounting must be explicit; no unlimited retries. Total calls, overhead and queued batches must fit the ticket and shared-account reservations.
- Reserve in an atomic, auditable quota ledger before an external request. After completion, reconcile provider-reported usage and charges; release unused reservation only on terminal confirmed outcome.
- For unknown completion/timeout: keep the reservation and mark `delivery_uncertain`; do not replay or release until independently reconciled.
- If provider reports 429, obey Retry-After and cooldown; 401/403/licensing denial stops the provider route. Never route to paid fallback, bypass shared quotas, or rotate accounts.
- A previously approved local model can only run within its thermal/memory constraints. “Local free” is not zero CPU/thermal/QA cost.

Cost formula for each task:

`cost_task = sum(actual_uncached_input_tokens × input_rate + cached_read_tokens × cached_read_rate + cache_write_tokens × cache_write_rate + output/reasoning_tokens × output_rate + storage_hours × storage_rate + provider_tools + batch_fees + retried_calls) + separately_reported_local_QA_cost`.

Rates must use matching units and timestamp; convert reported billing currencies with a recorded FX source/time (never invent exchange rates), separate **estimated** from **provider-confirmed**. For provider terms that already bundle a cache write charge, do not charge it twice.

Rank candidates by **empirical accepted-work yield**: (quality/first-pass rate, independent QA cost, expected retries, estimated billed tokens, latency and data restrictions). A successful low-token but incorrect result is not economic success. All dashboards show both expected and actual costs.

## Provider-specific optimization is conditional

- **Prompt caching:** use stable common prefixes **only if the supported model/account terms and privacy permit**. Measure hit tokens, cache-write vs cache-read rates, minimum prefix lengths, cache lifetime and storage. Do not expose tenant A content to tenant B for cache reuse. Cache may not reduce rate-limit consumption the same way on all providers.
- **Batch:** use only for non-urgent and independent jobs with approved private-data handling, supported models, explicit latency windows and verified batch prices. Provider-native batch submission can be non-idempotent; use batch IDs for reconciliation. Batch prices may not combine with caching discounts.
- **Free tier:** verify supported models, current org/account request and token limits and whether vendor may use submitted free-tier content to improve its products. Public/approved synthetic text only unless project processing is explicitly authorized.
- **External models:** do not confuse host service API compatibility (e.g. OpenAI-format JSON) with independent model licensing or source availability.

Official references checked when the SOP was adopted:  
https://developers.openai.com/api/docs/guides/prompt-caching  
https://developers.openai.com/api/docs/pricing  
https://ai.google.dev/gemini-api/docs/caching  
https://ai.google.dev/gemini-api/docs/batch-api  
https://ai.google.dev/gemini-api/docs/pricing  
https://console.groq.com/docs/batch  
https://console.groq.com/docs/rate-limits

These links supply *capability guidance*; the specific account dashboard and latest agreement determine quota/price. Never freeze a free-tier entitlement or public price in the SOP.

## Independent QA and acceptance

1. The generating model's own “PASS” is **advisory only**. A separate QA/QC authority and deterministic project-specific test harness decide admission.
2. Verify task scope, RAG provenance and source SHA-256, diff boundaries, license/rights, sensitive data removal and output schema before executing tests.
3. Test in isolation: static checks, interface/contract tests, unit/integration tests, security negatives, real application behavior when approved; WordPress uses ACRE where applicable. Maintain frozen test hashes, original source snapshot and independently recorded results.
4. Require unchanged baseline outside approved paths and no test tampering. Integrator must produce exact Git commit, conflict checks, source fingerprint and original rollback reference; rerun QA on **integrated commit**.
5. On failure, send minimal diagnosed evidence for at most **two repair attempts** within the original budget and authorization. Quarantine ambiguous, self-certifying, unchanged or still-failing output. Do not increase allowed repair budget via provider failover.
6. Preserve immutable audit entries: task contract hash, request/response digests (not raw secrets), provider and model, quote/usage, request IDs, source SHAs, reviewer, tests, failure classification, integration commit, cost and restoration result.
7. Release/outbound messaging, credential mutation, public posts, paid API upgrades and production changes remain **outside the SOP approval** and require separate existing gates.

## Pilot scorecard — gates, not asserted achievements

| Measure | Target or hard gate |
| --- | --- |
| Cost per independently accepted ticket | >=30% improvement vs matched, measured baseline |
| Input tokens per independently accepted ticket | >=40% improvement vs matched baseline |
| First-pass QA correctness | No degradation from baseline |
| Repair | <=2 bounded attempts; no “retry until green” |
| Unauthorized spend/transfer/deployment | 0 (hard fail) |
| Duplicate billable assignment | 0 (hard fail) |
| Unlicensed assets/unsafe output accepted | 0 (hard fail) |
| Data or provenance uncertainty | Quarantine, do not count as accepted |
| Reporting | Actual/estimated separately; missing historical metrics labelled “not measured” |

Pilot dispatch, provider enrolment, configuration edits, changing daily caps, service restarts and production deployment were **not authorized** in the 2026-10-30 owner approval. Department-by-department ingestion and runtime negative testing are separate future approval/verification stages.

**Rollback:** For documentation-only adoption, revert a future Git documentation revision if explicitly approved; do not change running provider slots. For future separately authorized runtime adoption, retain a pre-change snapshot, scoped rollback, owner approval and independently verified healthy service.