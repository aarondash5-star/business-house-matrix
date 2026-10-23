# Gate E — VSCodium/Aider isolated coding-backend comparison
**23 October 2026 IST | Candidate only | Certified v6 unchanged | Production NO-GO**

## Owner request and boundary
Owner authorized deploying and evaluating VSCodium + Aider against the currently failing Python development backend, retaining only a proven better Gate E candidate. This does **not** authorize removing shared local models, bypassing sandbox/QA, GitHub merge, expanding permissions, enabling production traffic or publishing.

## Baseline and source of truth
- Draft PR #13, feature branch `feat/dev-matrix-gate-e-general-runtime-20261022`, certified v6 base `release/dev-operator-scoped-v6-security-20261022`.
- Handover: `docs/handoffs/DEV_MATRIX_GATE_E_NEXT_CHAT_HANDOVER_20261023.md`; decision: `docs/handoffs/DEV_MATRIX_GATE_E_RC1_RELEASE_DECISION_20261023.md`.
- Dell protected v6 controller was verified active on 23 October with unchanged SHA256 `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`; receipt `f972b3e4-9a3c-4c31-a8d0-f49659378836`, exit 0.
- Dell developer worker online; VSCodium already present at version `1.140.06880`; Aider absent before this experiment. Mac developer worker online; no VSCodium/Aider command in its user PATH. No Mac installation requested as prerequisite for headless benchmark.
- Available Dell local models: `granite4:3b`, `qwen3:4b-instruct`, `ministral-3:3b`, `qwen3:4b`, `matrix-granite-lite:3b`; do not delete globally shared models.
- Historical failed `gate-e-rc1-python` and `gate-e-rc1-python-json` tasks must not be replayed, rewritten or relabeled.

## Proposed isolated evaluation
- Stage a dedicated nonproduction owner-scope candidate; Aider version pinned to PyPI `aider-chat==0.86.2` in a user-only pipx environment, no root/system Python changes. Installation request Dell SSH job `d1651067-6fce-4d86-8bb2-f50b139a65a7` (final terminal result required).
- Compare Aider-controlled local coding proposals against historical direct Granite Python failure, using only the existing trusted source/test baseline `fbcea95fd22218aabc5a03be48811b23aa15cc66`.
- Trusted independent task: `benchmarks/gate_e/money.py`, `benchmarks/gate_e/invoice.py`; owner-authored `tests/test_gate_e_invoice_rc1.py` (6 tests). The model may change only the two approved sources; never trusted tests, repository policy, or production files.
- Prefer Aider headless mode; disable telemetry, update checks, git auto-commits, shell suggestions, auto-tests/auto-lint, and all external-model keys. Model endpoint only the preexisting local Ollama loopback. Never weaken mandatory network-disabled Bubblewrap used for trusted QA.
- Evaluate on identical pinned inputs, checking model-actual output, syntax, immutable tests, allowed file paths, timeout/resources, no push/publish, and valid local review. Aider's mere installation is **not** evidence of improved model performance or Gate E certification.
- On failure or inconclusive evidence, leave existing Granite proposer as historical/default, preserve candidate receipts, and make no production changes. On reproducible independent QA success, keep only the best *Gate E staged backend* and do not remove shared AI runtimes/models used by other departments.

## Required release gates after candidate selection
External public repository model-generated patch with exact owner-approved SHA/tests; project-scoped PR write/review identity security approval; Dell isolated canary, observable rollback; signed final checks on exact release SHA; explicit v6 parity checks and independent signoff. Until then PR #13 remains draft and production NO-GO.

## Receipts / terminal status
- Dell read-only host / protected v6 preflight: `f972b3e4-9a3c-4c31-a8d0-f49659378836` **exit 0**.
- Mac read-only host preflight: `c8146aa0-cfcb-490e-870c-955b6c54af4e` **exit 0**.
- Dell inventory: `26b2ae4b-82fd-4ec8-a894-174004f63285` **exit 0**.
- Mac inventory: `97f0da2a-eb70-47d2-b937-5cf9367018a7` **exit 0**.
- Aider installation: **PENDING receipt check**.
- Fresh Aider model-generated multi-file Python benchmark: **NOT CERTIFIED**.
- No live Gate E canary / merge / production deployment.


## 23 Oct 2026 — Actual installation and independent benchmark receipts
- Dell user-only Aider `0.86.2` **INSTALLED** in `~/.local/share/pipx/venvs/aider-chat-gatee`. Two bounded pip attempts timed out (SSH receipts `d1651067-6fce-4d86-8bb2-f50b139a65a7`, `0cd5f918-9f9c-4095-b7ca-3c20838caf8a`); isolated capped `bhm-gate-e-aider-install-20261023.service` subsequently completed successfully, `ExecMainStatus=0`; verification receipt `a9402276-20bf-45f5-9367-60de25bf2a94`.
- Public test/spec staged in `~/matrix-gate-e-aider-comparison-20261023` from immutable SHA `fbcea95fd22218aabc5a03be48811b23aa15cc66`; trusted Python test SHA256 `627abdaca57dbf7977acdd7fb8563c76c11b0fcec4de31f4e0982f6c31a2d402` (receipt `1a1be6df-5ef3-4c2d-8360-92f0cebc4212`).
- First Aider CLI launch failed pre-inference because `/dev/null` is not valid YAML configuration (service exit 2); no generated content. Fresh distinct `bhm-gate-e-aider-qwen2-20261023.service` used **local-only Ollama `qwen3:4b-instruct`** and successfully generated two Python files. Editor had `--no-git`, no auto-test/auto-lint, no command suggestions, telemetry disabled; no remote push/publish. Model job ended exit 0 (terminal receipt `039b9926-4107-43a2-bb92-3a246cce3a48`).
- Mandatory isolated Bubblewrap doctor **PASS**. Independent unchanged 6-test Python QA **FAILED (5 failures, 3 errors)** due to model-created code correctness errors (missing import, invalid strings accepted); receipt `b5a6d570-3279-4ad0-8391-1a5bde5fb588`; syntax checks passed but `qa_passed=false`. Aider/Qwen is **NOT** proven superior, and **NOT** promoted.
- Separate staged repair evaluation `bhm-gate-e-aider-qwen-repair1-20261023.service` dispatched with sanitized QA feedback, distinct workspace, 210s/2200MB/100%CPU caps, `NoNewPrivileges=yes`, `Restart=no`, receipt `89b2a225-ddde-42db-a2cc-4dcd0c38d38b`; at time of this entry no terminal repair QA was available. No production change or auto-promotion permitted.
- Dell certified v6 controller rechecked active, SHA256 `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e` unchanged. Mac worker currently offline, so independent Mac peer certification is pending. No Gate E canary, merge, production deployment, root/security changes, or shared model deletion.
