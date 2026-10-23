# Gate S v2 — Unconstrained Planning Architecture, Strong Reference and Evaluation

**Date:** 23 October 2026. **Scope:** Development-planning intelligence only. **Overall status: NOT CERTIFIED / NO PROMOTION.**
Branch `feat/dev-supervisor-gate-s-20261023`. v1 untouched as historical baseline; v6 controller unchanged.

## Decision
The owner asked to remove the shallow output restrictions and compare against a strong model's robust plan. Interpret 'remove restrictions' as remove arbitrary **cognitive/output** restrictions, not bypass permission, tool, billing, execution, data-access, privacy, SSH transport or production security boundaries.

### What changed
- New `brain/supervisor/gate_s_v2.py`, isolated from Gate S v1 and certified controller. No fixed five-role chain. Model may propose **6–30 work packages** with independently chosen research, design, development, QA, security and human review phases; non-linear dependency DAG; deliverables, per-task acceptance criteria, milestones, assumptions, risks, strategic rationale, P0/P1/P2 prioritization.
- Prompt supports owner task context to 12 KB (rather than 350 characters), local context `num_ctx=6144` rather than 2048, and generated budget `num_predict=2800` instead of 520 (this local hardware budget is still **not enough to guarantee a 16-task deep plan**).
- Strict schema + approval gate stays: proposal only, `execute=false`, `publish=false`, `push=false`, `spend=false`, `privilege_change=false`, human review required. No model-generated direct shell commands; no direct worker dispatch.
- `benchmarks/gate_s/andaz_website_deep_brief_20261023.md`: authentic business context and explicit unknowns; website/PMS not claimed inspected.
- `benchmarks/gate_s/andaz_gpt6_reference_plan_20261023.json`: a **GPT-6 model-authored strong-quality reference**, 16 tasks, 5 milestones, five assumptions, seven concrete risks. All tasks include measurable acceptance and concrete deliverables; dependencies reflect allowable parallel work.
- `benchmarks/gate_s/run_andaz_deep_eval.py`: single-use controlled local Qwen pilot runner (not automatically activated). Preserves a terminal JSON receipt without executing any proposed task.

### Verification receipts
1. Dell S2 contract suite `tests/test_gate_s_v2.py`: **20/20 PASS** on cloned isolated branch, terminal SSH receipt `4903cfd7-838a-4659-8950-f94aa9f62fdf` (branch at `84069232207e5772d24ebc794fcf23cede4a9b08` at the time). Covers acceptance, rich task counts, dependency DAG, human review, unknown roles, unauthorized root fields, no execution/push/spend, and input bounds.
2. Strong reference verification `tests/test_gate_s_v2_reference.py`: first **7/8** due overly literal `verify` substring not matching `verified`. Test match adjusted to `verif`, preserving original reference, and independently **8/8 PASS**. Terminal receipt `e357dbdc-1bda-4cc9-bf18-b56f8561d220`, exit 0 at branch commit `8c9a9c6850cf9ebe2163f293223f71a84a0c34bb`.
3. Historical Gate S v1 real Andaz Qwen `qwen3:4b-instruct`: generated the old five-step generic plan in **104.052 s**. Previous 12/12 keyword coverage / 8/8 safety, but no deliverables, per-work-package acceptance, source citations, audit workplans or granular milestones. This was a *different, very restrictive prompt/format*, so it is **NOT a fair head-to-head model-ability comparison** against the GPT-6 reference.
4. **Gate S v2 Qwen live run and separate OpenRouter stronger-provider run: NOT EXECUTED.** Generic SSH command-security check denied attempted model launch / provider invocation. No execution receipt exists and no live model comparison is claimed. Do not bypass this connector security denial or report a hypothetical success. Existing Dell provider-router files were located read-only; no provider credentials extracted, copied or modified.
5. Mac peer remains unavailable in the latest heartbeat; no cross-host QA. Certified v6 was active and original SHA `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e` was independently rechecked earlier in Gate S and Andaz experiments; no controller changes in this session.

### Strong reference plan milestones and distribution
- **M1 Discovery** T1–T3: audited canonical site/PMS, scoped competitor research, conversion paths.
- **M2 UX & design** T4–T6: sitemap/wireframes, verified photography and content truth, original responsive design system.
- **M3 Private implementation** T7–T11: staging/backups, templates, PMS booking/WhatsApp contract, SEO/analytics/consent, privacy threat model.
- **M4 QA/security** T12–T15: mobile/a11y/image authenticity, booking regression with synthetic guests, security review, Core Web Vitals/SEO/rollback.
- **M5 Human signoff** T16: evidence dossier, explicit blockers and separate approval before any live change.
Specific acceptance examples include 360/390/768/1280px layouts, no invented inventory, source-mapped real images, preserved room selection, verified WhatsApp deep links, review of guest ID collection, and no false kitchen operational claim.

### Comparative interpretation
| Dimension | Real Qwen4B Gate S v1 (restrictive) | GPT-6 reference with Gate S v2 contract |
| --- | --- | --- |
| Work packages | 5 (preassigned) | 16 (task-specific) |
| Explicit milestones | None | 5 |
| Deliverables per task | None | Yes |
| Acceptance criteria per task | None | Yes |
| Explicit risks | None | 7 |
| Concrete website system audit | Mention only | Pin source, inventory/PMS/routes/analytics |
| Real-photo handling | 'real photo placeholders' | Evidence/rights and claims map |
| Booking regression design | Brief mention | Detailed synthetic fixture/negative-case matrix |
| Planning-only safety | Yes | Yes |
| Reasonable evidence of superior *model ability* | **No**, confounded by radically different prompts and tests | **Reference target**, not a head-to-head result |

## Open acceptance gates
- Operator security owner needs to approve an available **fixed-function supervisor inference** action through the existing authorized Dell provider transport, not unrestricted SSH shell; or an equivalent audited job runner. Do not route around a denied shell gate.
- With the **same deep brief, prompt, schema, grading rubric and inference budgets**, benchmark at least two models (Qwen local vs one stronger supported licensed remote model such as Qwen3.8 27B or a comparable open-weight supervisor candidate).
- Test detailed semantic fidelity, architecture feasibility, valid priorities/dependencies, unknowns versus claims, approval/security protection, repeatability, rate limits, time-to-first-token and total completion latency. Add negative prompt-injection and worker-outage scenarios. All tests must be independent of model-generated acceptance.
- Reconnect Mac for independent QA and sign off before routing any live v6 work to a supervisor. Gate E unchanged NO-GO.

## Owner-facing decision
**Unrestricted cognitive planning format and stronger reference delivered; Dell tests PASS. Actual equal-conditions Qwen-vs-strong-model inference comparison remains blocked, not falsely called completed.** Do not merge, deploy, publish, spend, modify v6 or downgrade permissions to force a test.
