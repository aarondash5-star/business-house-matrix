# Unified Dev Matrix — Real Autonomous Flow Certification (23 October 2026)

**Owner decision:** Skip Mac verification; run and certify the autonomous Brain development workflow on Dell; use OpenRouter or Groq as an external verifier. **Result:** **DELL SYNTHETIC AUTONOMOUS FLOW CERTIFIED**, **PRODUCTION UNIFIED DEV SERVICE NO-GO (separately)**.

## Concrete verified passes

1. **Rootless OCI workcell smoke PASS** on Dell with owner-approved existing Generic Linux SSH operations lane. Tested pinned locally cached Python image `docker.io/library/python@sha256:1b668429b3511ab407d8e00648891631b0b1a4d7e15e3ca70f38ab5b91ad4ab4`. A disposable independent `app.py` was genuinely edited inside container; source fingerprint was confirmed; independent tests exited 0; an attempt to overwrite `.git/config` returned `OSError [Errno 30] Read-only file system`. Receipt **`a73a3254-842f-4527-8382-294d78c8a827`**, exit **0**. Existing unrelated SearXNG container left running.
2. **Local candidate regression suite PASS 17/17** on pinned source `2d885b6fb8cf8f43792de74e1f93b2931ca36eae`. Covers owner-signed task intake, forged signatures, malformed repo identity denial, pinned OCI identity, offline workcell flags, Git metadata protection, source-change hashing, no-op rejection, immutable tests, Git baseline tampering, crash quarantine and rollback-safe queue transitions. Receipt **`00a35cc0-2192-4cad-8e57-d32a39f4e243`**, exit 0.
3. **External model connection PASS — Groq GPT-OSS-20B**, public synthetic prompt through existing `matrix-route.py`, `--public-input --no-fallback` with paid API policy disabled. Receipt **`fd1bcd36-8238-43c5-866c-f27756133298`**, exit 0, model replied `GATE_OK`. OpenRouter free model passed connectivity and declared cost `0` in receipt **`23b83f77-4912-425f-bf49-e1f42e49338c`**, exit 0.
4. **Genuine full autonomous two-file coding PASS using Groq GPT-OSS-120B via existing free-tier router**. An owner-signed synthetic `synthetic-groq120-autonomy` task went through `JobLedger.submit -> execute_job -> external model output -> rootless PodmanWorkcell.execute -> verified_source_changes -> independent immutable Python QA -> review_ready`. The model generated **one command** (length 750), actual shell/guest edit exited **0**, independent `PYTHONPATH=. python3 -B tests/test_fixture.py` exited **0**, both `calc.py` and `invoice.py` appeared in hashed source-change proof, and final state `review_ready`, model steps **1**. A transient `tempfile` workspace was used, never published or installed; task source contained only public synthetic financial-math fixture, no Andaz/PMS/guest data. Receipt **`b00a5567-4ed1-407f-9f29-22343cfa132f`**, exit **0**, stdout `REAL_MULTI_FILE_AUTONOMOUS_ACCEPTANCE_PASS`.
5. **Independent outside review by different model — Groq GPT-OSS-20B**, explicit review of the *public synthetic receipt summary* (not a rerun of source tests, nor an independent review of full generated files). It corroborated the evidence for the scoped synthetic coding flow but explicitly said it **does not establish production readiness** or full worker/controller integration. Receipt **`12f81426-dc5a-464a-9b41-e9a6e0617e9c`**, exit 0.
6. **Latest-source regression PASS 17/17** at Dell candidate HEAD **`068e05752ed9846f8b78ec6630a8fcf500d9aded`**, which added bounded pinned source context and diagnostic failure receipts. Receipt **`30096b91-feb4-40bf-b44a-a1d25bed8b03`**, exit **0**. Candidate git checkout clean, no uncommitted changes. Note the autonomous smoke started after the HEAD update was committed but did not independently print its source SHA during the run; a later SHA read confirmed candidate HEAD.
7. **Existing production safety unchanged** at postcheck: `bhm-autonomy-controller.service` **active**, v6 controller SHA256 **`b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`**. Only the previously existing SearXNG container appeared in `podman ps -a`. Paid model usage blocked by router policy. Postcheck receipt **`aeb99bad-13c3-44cb-bcd8-d1d7c0fe144f`**, exit 0.

## Honest failed attempts / corrections

- Groq-OSS20 first full test was blocked by per-minute quota: `681a7018-7fc4-400b-897a-afc2906bb119` (no model execution).
- OpenRouter free provider connectivity PASS but subsequent live coding task returned `OPENROUTER_POOL_FAILED_RuntimeError`, no code execution; receipt `5686d7b4-596a-48c0-a631-13f15e6b2f33`.
- First Groq-OSS20 multi-file task reached real model command execution twice but final `needs_review` after QA failed; a test harness importing modules from `tests/` without `PYTHONPATH=.` was identified as likely cause. Receipt `8069660f-7f78-4748-8a1a-a60bf3ce1251`. Separate Groq-OSS120 fixture with corrected trusted command later PASS.
- All failed attempts remained fail-closed: none reported `review_ready` or modified production.

## Certification scope

| Item | Status |
| --- | --- |
| Dell SSH bridge → local test harness | PASS |
| Owner-signed job and durable SQLite ledger | PASS in synthetic workflow |
| External hosted free-tier model coding response | PASS (Groq OSS120) |
| Actual model-generated two-file code inside rootless guest | PASS |
| Hash-based actual source change proof | PASS |
| Independent signed immutable test command | PASS in synthetic fixture |
| Automatic QA-based terminal `review_ready` | PASS |
| Fail-closed quotas/provider rejection | PASS (correctly blocked) |
| External Groq second-model evidence review | PASS with caveats |
| Latest Dell unit/recovery regression tests | PASS 17/17 |
| Mac tests | **OWNER-WAIVED** for this Dell-only release track |
| OpenRouter as dependable autonomous coder | NOT CERTIFIED (provider pool error) |
| Persistent autonomous service/CLI and authenticated controller ingress | **NOT DEPLOYED / NOT CERTIFIED** |
| Production worker registry, dispatch, permissions / retries under real multi-project load | **NOT CERTIFIED** |
| Real Andaz website external-repository code execution / browser QA | **NOT CERTIFIED** |
| External GitHub PR write identity and reviewed output | NOT CERTIFIED |
| Canary, rollback and production routing switch | NOT PERFORMED |

## Release conclusion

**PASS:** The candidate software's Dell-only, *synthetic* automatic model → sandboxed source edit → immutable test → verified receipt execution path is now certified with evidence.

**NO-GO:** Do not state or assume that the full Business House Matrix Dev department is deployed, that its persistent secure CLI/controller ingress is active, or that Andaz development has been completed. The retired `brain.py serve` proposal-only process remains stopped; certified v6 controller remains live. The temporary scripts used for QA were test harnesses, not a new always-on service or an SSH access control change.

**Remaining requirements to production release:** legitimately approved fixed-purpose persistent CLI/Brain ingress (earlier deployment attempts were blocked by tool safety checks); scoped project source identity and worker registry authorization; real external repo test/Andaz staging with autonomous coding and browser QA; independent CI and system load/crash tests; restricted GitHub review identity; canary and rollback. Mac QA is waived by owner's 2026-10-23 request, not falsely marked passed. Only deploy once mandatory non-Mac gates are independently verified.

**External verifier caution:** The second Groq model reviewed a factual receipt summary supplied to it. It did not independently run the code or inspect complete ephemeral source files. The actual code execution proof comes from Dell's terminal receipts and independent in-container Python tests.
