# Gate E RC1-to-production authorization and release gates

**Authorized by owner:** 2026-10-23 IST, "Document and approve all implement them". This approval covers all five sequential phases **subject to passing their prerequisite gates**. Authorization is not evidence of certification.

**Source:** Draft [PR #13](https://github.com/aarondash5-star/business-house-matrix/pull/13), branch `feat/dev-matrix-gate-e-general-runtime-20261022`, base certified `release/dev-operator-scoped-v6-security-20261022`.

## Owner-approved implementation phases
1. **RC1 Runtime hardening:** bounded model execution and all QA, cancellation and child reaping, global runtime and output caps, bounded concurrency, crash-safe receipts and fail-closed recovery. Tests/receipts required.
2. **RC1 CI and security:** secure Bubblewrap-enabled CI runner and explicit resource budget, source policy checks, test matrix and host peer QA. No bypass of absent sandbox or failed unrelated regression.
3. **Autonomy certification:** owner-enrolled non-sensitive real Python/Node multi-file benchmarks with independent tests, security rejections and traceable model runs. Do not replay existing completed Granite pilot.
4. **Dell production canary:** only after (1)–(3) pass, deploy separate owner-scope Gate E service; limited enrolled test jobs, without changing v6 controller, integrations or permission boundaries; observe faults and run rollback drill.
5. **Release:** only after clean canary + rollback and independently auditable signoff, create versioned release and enable approved multi-project autonomous development orchestration. GitHub PR write identity must be project-scoped and independently verified.

## Global invariants
- Preserve certified v6 SHA-256 `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`, its active service, rollback copies and historical receipts.
- No spend, private data mount, model-controlled host commands, arbitrary shell, unattended code merge, business-site publishing, credential expansion, or changes to root/SSH permissions. All are separate capabilities beyond this authorization.
- Fail-closed on any missing sandbox or CI failure; do not label verification as a production deployment.
- The existing `gate-e-public-python-parse` task is **finished** and must not be rerun; its valid pilot receipt remains immutable.
- Keep PR #13 draft until all release criteria pass; if a stage fails, document blockers rather than silently progressing.

## Initial known blockers (at approval)
- Hosted GitHub Actions starter-tests fails: hosted runner missing /usr/bin/bwrap, plus a marketing guard test.
- Mac/Dell exact-head Git clone stalled; avoid network-dependent staging until source transport is independently certified.
- Gate E Python QA subprocess cannot be cancelled mid-test; need hard global deadline and streaming output bounds.
- Durable multi-job controller, concurrency, restart recovery, independent Node + external multi-file model evaluation, PR write identity and rollback drill not certified.

## Evidence ledger
Append implementation commits, SHA, host receipts, CI IDs, rollback result, gate pass/fail and exact deployment identity here. Never mark any phase green without terminal machine evidence.
