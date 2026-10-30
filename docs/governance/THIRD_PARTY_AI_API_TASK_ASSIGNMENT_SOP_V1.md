# DeluluTech — Third-Party AI API Task Assignment Handbook

**Policy ID:** DLT-BHM-API-ASSIGNMENT-SOP-001  
**Version:** 1.0.0 · **Owner approval:** 2026-10-30 · **Status:** OWNER-APPROVED / DOCUMENT-PINNED / RUNTIME-ENFORCEMENT-NOT-VERIFIED  
**Scope:** All nine Business House AI Matrix departments and their authorized sub-Brains: Concept, Design, Development, QA/QC, Marketing, Sales, Accounts, Support, EVOLUTION.  
**Authority:** [Super Brain operating charter](SUPER_BRAIN_OPERATING_CHARTER.md) and [departmental handoff](DEPARTMENT_ROUTING_AND_HANDOFF.md).  
**Companions:** [Provider, budget and QA policy](THIRD_PARTY_AI_API_PROVIDER_BUDGET_QA_POLICY_V1.md); [machine task schema](../../brain/governance/api-task-assignment-v1.schema.json); [owner approval receipt](approval-receipts/THIRD_PARTY_AI_API_TASK_ASSIGNMENT_SOP_V1_2026-10-30.json).

> **This commit authorizes documentation and policy pinning only.** It does NOT enroll/activate providers, change secrets, alter live workers/routers, launch inference, enable spending, grant new authority, publish work, merge product code, deploy or imply that running Brains have ingested this document.

## 1. Objective and decision rights

Optimize **independently accepted useful work per total token and per unit of actual cost**, not the lowest tokens per single request. A cheap model that needs repeated repair, fails evidence checks, or increases QA cost is not economical.

**Owner → Super Brain → responsible departmental Brain → authorized specialist/router → independent QA/QC → Super Brain → owner**. The receiving departmental Brain, **not the Super Brain**, decides how to partition, batch, dispatch and repair work within the existing owner-approved task envelope and resource permissions. Another department cannot borrow credentials, data, budgets or execution identity. The same policy applies recursively to sub-Brains; authority does not broaden through delegation.

Policy precedence: platform and connected-tool safety/law → latest explicit task-specific owner authorization → existing Super Brain charter and project isolation → this handbook → subordinate provider/worker configurations. A more restrictive project scope wins. Conflicts stop affected routing and are surfaced for owner decision.

## 2. Mandatory assignment gates (A0–A10)

| Gate | Non-negotiable action | Evidence before proceeding |
| --- | --- | --- |
| **A0 Owner envelope** | Read exact approved project, authority, allowed effects, scope, budget and definition of done. Policy adoption is NOT task/API dispatch approval. | Approved [task envelope v1](../../brain/governance/task-envelope-v1.schema.json), task ID and current owner decision |
| **A1 Reuse first / Golden Rule 0** | Search internal Git, prior accepted receipts, approved project RAG and maintainable OSI-approved open-source components **before calling a model**. Evaluate license, security, maintenance, cost, provenance and reuse decision. | Documented reuse/search result and verified source references |
| **A2 Deduplicate** | Check task ID, contract hash, baseline Git SHA, active leases, prior accepted patches, caches and completed work. | Unique idempotency key; no equivalent accepted/in-flight task |
| **A3 Privacy & license** | Classify inputs; remove credentials, customer/financial/private data and unrelated project context. Verify processing terms and approved model/component licenses. External model/service exceptions require explicit owner authorization; free hosting does not imply OSI approval. | Classification, consent/authorization, license review and redaction status |
| **A4 Compile minimal task** | Include exact objective, only necessary source excerpts, stable interfaces, test failure, permitted paths, output shape and budget. Retain safety-critical context and line/source hashes. | Versioned [API task packet](../../brain/governance/api-task-assignment-v1.schema.json) |
| **A5 Eligibility & cost** | Select only previously enrolled, allowlisted, task-qualified models in the authorized project. Compare predicted all-in cost and success probability; reserve conservative quota/budget before request. | Provider registry snapshot, freshness, limits, estimate and reservation ID |
| **A6 Deterministic-first** | Use grep/AST/static analysis, templates, known contracts, tests or approved retrieval without a model where sufficient. Local inference only when permitted and thermally safe. | Route decision `deterministic` / `local` / `external` with reason |
| **A7 Bounded execution** | One narrow assignment per exact source/baseline. Return concise diff/JSON. No unapproved tools, shell, messaging or network side effects. | Provider request ID and usage, normalized structured output, timestamps |
| **A8 Independent QA** | Source/contract/schema/lint/security tests and project-specific QA; ACRE for WordPress CRM where applicable. Model's assertion or self-test alone is NOT acceptance. | Reviewer distinct from generator, frozen test hashes, acceptance receipt |
| **A9 Limited repair** | For reproducible source defects, provide minimal failing assertion and relevant code. Maximum **two repair attempts** per task, including cross-provider retries; hard-limit token spend. Unknown result, nondeterministic/unchanged patch, auth/security/contract failures: quarantine/escalate. | Failure class, attempt budget, immutable original receipt, QA of fixed revision |
| **A10 Integrate & account** | Integrate only QA-approved exact source via authorized integrator; rerun independent downstream QA. Measure actual tokens, cached/batch charges, retry and QA costs; report without inferring release. | Git SHA + integration receipt + spend/usage receipts + rollback and final status |

**Fail closed** if any required gate evidence is absent. Do not turn a planning document, GitHub issue, queued task, synthetically passed test or hosted provider's verbal statement into a claim of active execution or completed integration.

## 3. Compiled task packet

Use `api-task-assignment-v1.schema.json`. Each packet extends, but **does not replace**, the owner-approved central task envelope. Mandatory fields cover:

- Identity: `packet_version`, `task_id`, `owner_envelope_ref`, `department`, `project_id`, `tenant_id`, `idempotency_key`, `baseline_sha256`.
- Scope: task profile, exact result contract, input/source SHA-256 list, RAG evidence with trust labels, dependency IDs and allowed paths/effects.
- Data: classification (`public`, `internal`, `confidential`, `restricted`), provider transfer authorization and redaction proof.
- Routing: preferred capability, allowlisted provider/model/endpoint IDs, license decision, declared runtime/billing mode, latency deadline, cache/batch eligibility.
- Budget: request, per-task, retry, project, account and department ceilings; max input/output/reasoning tokens; per-run currency and USD conversion basis. Missing explicit paid approval => external paid cap **0**.
- Quality: immutable expected tests, hashes, independent evaluator ID, rollback/failure mode and exact acceptance contract.
- Reporting: prompt and output digest, actual usage categories, cost, cache/batch evidence, provider receipt and QA/merge receipts.

**Sample shape only; not a runnable job:**

```json
{
  "packet_version": "1.0",
  "task_id": "CRM-SEARCH-001",
  "owner_envelope_ref": "approved-envelope-reference",
  "department": "development",
  "project_id": "example-isolated-project",
  "tenant_id": "example-tenant",
  "idempotency_key": "CRM-SEARCH-001:baseline-digest",
  "baseline_sha256": "sha256-of-source-snapshot",
  "task_profile": "narrow_code_patch",
  "objective": "Correct name search behavior without touching other files",
  "input_evidence": [{"ref": "source-slice:inbox", "sha256": "pinned-evidence-digest", "trust": "verified_internal"}],
  "allowed_paths": ["includes/class-example-inbox.php"],
  "forbidden_effects": ["deployment", "external_messages", "production_write", "git_push"],
  "data_policy": {"classification": "internal", "external_transfer_authorized": false, "redaction_verified": true},
  "routing_policy": {"mode": "deterministic_first", "provider_ids": [], "model_ids": [], "license_decision": "not_applicable", "batch_allowed": false, "cache_allowed": false},
  "budget": {"currency": "INR", "paid_cap": 0, "max_input_tokens": 2500, "max_output_tokens": 700, "max_total_attempts": 2, "reserved_amount": 0},
  "qa": {"reviewer_id": "independent-reviewer", "test_refs": ["frozen-search-tests"], "acceptance": ["partial name search passes", "SQL parameterization preserved"]},
  "reporting": {"receipt_ref": "record-only", "release_mode": "manual"}
}
```

An example packet has **no authority to dispatch**. A provider may never infer missing parameters, substitute endpoints, upgrade billing or expand its scope.

## 4. Context and token conservation

1. Retrieve minimal relevant symbols, failing assertions, interfaces and bounded project RAG citations; never upload the repository or chat history by default.
2. Preserve stable instructions/schema in an identical prefix for eligible provider caching. Cache hits, retention, extra cache-write/storage cost and project isolation must be **measured**, not assumed.
3. Return a unified diff, precise code span or bounded JSON. Avoid repeating inputs, long rationale or whole files when a diff suffices. Require complete files only if patching is riskier.
4. Batch **independent, nonurgent, non-side-effecting** requests only after verifying provider support, price, confidentiality and latency deadline. Each batch item retains its own ID/QA receipt; submission uncertainty must not trigger duplicate batches.
5. Share **public facts and approved generic templates**, not confidential embeddings, cached prompts or business data across tenants.
6. A model cannot compress away authorization, security requirements, negative tests, acceptance criteria, source citations or dependency contracts.
7. Cache accepted outcomes keyed by project + task contract + source/test hashes + tool/policy versions. On changed baseline, invalidate rather than replay stale patches.
8. Use locally deterministic evaluation before spending new inference tokens; every further call must have a *diagnosed* missing behavior.

## 5. Route selection

**Only eligible candidates compete.** Candidate must be already authorized and enabled for the *particular* project and department; meet OSI-approved component/model policy or an explicit owner exception; comply with privacy transfer terms; have verified credentials, remaining quota, billing eligibility, data residency and a current cost schedule; meet task accuracy/latency benchmarks.

Expected landed cost per accepted result:

`expected_total_cost = (initial_generation + predicted_repairs + cached_input_writes_and_reads + batch/storage/tool charges + measured_QA_cost) / max(observed_accept_probability, epsilon)`.

Calculate each token category at the **current provider-reported rate**, including separate input/output/reasoning, cached reads/writes, batch, storage and conversion costs. For free tiers enforce conservative local quotas **and** provider-reported limits; zero price is not infinite capacity. Cost estimates and daily caps must account for shared account keys across model slots and departments.

Prefer in order: deterministic/reusable solution → authorized qualified local model → qualified cheapest approved free/low-cost provider → stronger approved model when failure type/benchmark justifies. **No silent paid upgrade, provider substitution or proprietary-model license exception.**

Cost limits are enforced at request, task, shared-provider-account, tenant, project, department, day and sprint levels; **minimum remaining allowance** governs. Reserve before send; reconcile afterward. Treat unknown charge/usage as budget uncertainty, not zero. See [companion policy](THIRD_PARTY_AI_API_PROVIDER_BUDGET_QA_POLICY_V1.md).

## 6. Failure decisions and stop rules

- **400/schema failure:** repair the local packet once if deterministic; never charge repeated provider calls for invalid structure.
- **401/403 or licensing/security denial:** stop, do not rotate identities, bypass policy or automatically try another provider.
- **429/quota:** respect Retry-After/cooldown and shared account ledger; optionally route another *already approved* eligible slot only for a proven non-side-effecting request with confirmed no prior completion.
- **5xx/timeouts:** check the provider/task receipt before retry; unknown completion is `delivery_uncertain` and must not be blindly replayed.
- **Failed independent source/QA:** one diagnostic input plus bounded correction, **two repair attempts maximum**, then quarantine and escalate; never change tests to make the candidate pass.
- **Changed output but zero useful source delta / unchanged code / hallucinated APIs / unsafe edits:** quarantine. Do not auto-merge or certify.
- **Thermal/device risk, exhausted cost authority, privacy uncertainty, ambiguous duplicates:** stop the affected lane and preserve original artifacts.

No provider may approve its own security-sensitive actions or sign independent QA for its own generated output. Generated patches are untrusted data until verified.

## 7. Department-specific profiles

| Brain | Normal task profiles | Independent gates / restrictions |
| --- | --- | --- |
| Concept | verified research, feasibility, structured briefs | independent sources, assumptions, license/claims review |
| Design | UX concepts, design-system comparisons, asset planning | accessibility, provenance, brand approvals, no unauthorized asset purchase |
| Development | symbol-level refactor, bounded PHP/JS patch, integration reasoning | lint, existing tests, source hashes, isolated runner, Lane 7 where applicable |
| QA/QC | test plan, adversarial cases, review summaries | separate evaluator identity; frozen tests, reproducible evidence |
| Marketing | public trends, copy drafts, analytical summaries | factual claims, brand/rights review; never auto-publish or spend on ads |
| Sales | synthetic funnel analysis, CRM flow planning | no unapproved personal data transfer, pricing decisions or outbound messaging |
| Accounts | rule research, reconciliation templates | primary legal sources, human finance signoff; no payments or tax submissions |
| Support | approved knowledge summarization, case triage | no customer-data disclosure, refunds or guest-contact actions without authority |
| EVOLUTION | benchmark aggregation, error taxonomy, routing recommendations | cannot self-activate providers, budgets, new permissions or production policy |

Existing host and tenant separation remains: Dell Dev Tool Yard and Mac MAD Yard are distinct execution owners; a shared policy does not transfer Mac-only Marketing jobs to Dell or expose either host's vault.

## 8. Success metrics and pilot admission

Baseline from measured **actual** vendor usage and accepted QA receipts; missing historical usage is `not_measured`. Suggested pilot targets: >=30% lower **cost per independently accepted ticket** and >=40% lower **input tokens per accepted ticket** than comparable baseline **without decreased first-pass QA, coverage or privacy**. These are targets, NOT certified savings and NOT permission to issue a pilot request.

Mandatory zero-tolerance: unauthorized spend, off-scope provider calls, unlicensed source reuse, credential disclosure, duplicate billable dispatch, failed QA promotion, auto-publishing. Every task reports attempts, acceptance, token categories, actual billed cost if available, latency, quality, savings confidence and next dependency. EVOLUTION may propose benchmarks/model rank changes; owner approval is required to change approved policy or authority.

## 9. Versioning, adoption and rollback

- Git `main` policy file + companion schema/policy + immutable, owner-decision approval receipt are the canonical **documentation** anchor. Pin exact version and hashes in every downstream departmental adoption record.
- Existing runtime configurations, API keys, secret vaults, timer/service files, task queues and spend allowances are **unchanged by this handbook**.
- Each department must independently document policy ingestion, QA negative tests (no-secret, over-budget, quota, unauthorized model, replay, self-certification), rollback and actual runtime status *before* claiming SOP enforcement.
- Future `1.x` changes require owner-approved decision record and new immutable receipt; no in-place rewriting of a signed prior receipt. Breaking changes increment the major version.
- Rollback a future runtime adoption to its pre-adoption policy; do not roll back existing live working provider slots as a side effect of adopting documentation. In this approval-only stage, no runtime rollback is needed because no runtime change is authorized.
- A doc link or Git commit does **not** prove that Dell/Mac/other Brains automatically synchronized.

## 10. Primary provider documentation for later verification

These are dynamic **reference links**, not activated providers and not hard-coded rate/price entitlements. Verify from provider **account-specific** dashboards again at each actual provider admission:
- OpenAI: https://developers.openai.com/api/docs/guides/prompt-caching and https://developers.openai.com/api/docs/pricing
- Google Gemini: https://ai.google.dev/gemini-api/docs/caching , https://ai.google.dev/gemini-api/docs/batch-api , https://ai.google.dev/gemini-api/docs/pricing
- Groq: https://console.groq.com/docs/batch and https://console.groq.com/docs/rate-limits

Different vendors apply different caching/batch pricing and retention rules; discounts may not stack. The account's effective terms always govern. An open-source **model artifact** and its **hosted API service** must be evaluated separately for licensing and data processing.

---

**Owner instruction, 2026-10-30:** “Approve DeluluTech Third-Party AI API Task Assignment SOP V1 with initial applicability: all Business House Matrix departments. Produce and pin the governing handbook with versioned rules, task packet schema, provider/budget/QA policy and an approval receipt. Do not activate API dispatch, spend money, or deploy.”

**Recording status:** approved policy; technical integration / runtime ingestion **not authorized or verified**.