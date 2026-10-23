# Unified Dev Brain deployment request — live verification and NO-GO (2026-10-23)

Owner requested: "Deploy the unified dev brain and integrate with existing worked [workers] and smoke test."

**Disposition: NO-GO for a live universal runtime release; existing v6 remains active and smoke-tested.**

## Actual live checks
- Dell authenticated Generic Linux SSH bridge paired/online at 2026-10-23T10:31:16Z; operations and development lane heartbeat current, control lane stale.
- Mac paired but **offline**, last worker heartbeat stale by 23,435 seconds.
- Dell certified `bhm-autonomy-controller.service` active/running. Controller `controller.py` SHA256 **`b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`** unchanged.
- Real v6 controller `selftest` **PASS 6/6**: persistent queue, idempotency, blocked production route, isolation, privacy validation, conservative recovery. Terminal receipt `6f5a413f-7238-4c56-b191-189d83a391ae`, exit 0.
- v6 status: **12 completed, 13 needs_review**; old modes `dev_proposal:proposal_only`, `dev_scoped_build:synthetic_model_sandbox_review_only`, `dev_general_build:manifest_enrolled_sandbox_review_only`. The stopped `brain.py serve` was not reactivated and the proposal intake has no executing consumer.
- No `universal-dev` or `matrix-unified` user service listed. No confirmed full task end-to-end execution through candidate.
- Candidate GitHub branch `feat/dev-universal-dynamic-intake-20261023` head `a8aba572eb03fca8b59e1f9ec310ee5da809e59d`; Dell local candidate checkout still at prior `e8ac522e92fc284a09b4f48773b1b1c9326b205f`.
- Candidate branch had no hosted CI runs when queried; candidate's earlier negative QA was **13/14** with one identity-validation failure, source fix committed but post-fix SSH test denied by platform safety. Candidate CLI/bootstrap and draft PR requests were independently denied by tool safeguards. These denials remain unapproved and were **not** reattempted via alternative routes.
- Static review also found absent change verification before `review_ready`: model can issue a trivial command, then finish while existing baseline tests pass. Proof of generated source diff and independent real project QA is missing.
- Gate E Python multi-file real-model benchmark, independent external repository edits, project-scoped PR identity, canary/rollback and Mac parity are not certified.

## Integration gate matrix

| Gate | Verified result |
| --- | --- |
| Dell SSH connection to existing v6 | PASS |
| v6 live service continuity | PASS |
| v6 built-in smoke test | PASS 6/6 |
| Candidate source and static inspection | EXISTS; NOT RELEASE CERTIFIED |
| Candidate post-fix negative tests | BLOCKED / NO VERIFIED PASS |
| Candidate CLI secure ingress | BLOCKED BY PLATFORM DENIAL |
| Real model edits/QA on independent project | FAIL/NOT CERTIFIED |
| Mac worker independent smoke | BLOCKED OFFLINE |
| New service activation and authenticated worker integration | NOT PERFORMED |
| Canary and observable rollback | NOT PERFORMED |
| Production cutover | WITHHELD |

## Release constraint / required next verified actions

1. Legitimately resolve tool-level denial through connector/security review for the narrow fixed-purpose CLI bootstrap and QA actions. Do not bypass a denied action through alternate transport.
2. Add independent source-change proof, immutable trusted test protection, and actual dynamic-source-edit isolation tests to the candidate.
3. Independently certify post-fix negative security tests and a real multi-file Python/Node task plus the Andaz static website task in disposable compute.
4. Restore/verify Mac, scoped GitHub review/write identity, controller-to-Brain-to-worker dispatch and terminal receipts without exposing cross-project secrets.
5. Only when gates pass, activate an isolated candidate canary **beside** certified v6; record bounded concurrency, crash/cancel tests and successful rollback.
6. Route Dev tasks to unified Brain only after documented acceptance. Do not submit new `dev_proposal` items to the retired legacy consumer.

**No live production changes, security bypass, model-selected shared-host shell or misleading "deployed" claim.** The owner's approval to deploy is recorded; actual release remains gated by independent evidence.
