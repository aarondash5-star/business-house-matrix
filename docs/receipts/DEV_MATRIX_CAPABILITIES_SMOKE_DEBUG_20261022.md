# Dev Matrix capability rollout — smoke test, diagnosis and release gates

**Date:** 22 October 2026 (IST)  
**Project:** Independent Business House Matrix  
**Host:** Dell `dell-linux` (active controller), Mac `mac-linux` (support/QA)  
**Tracker:** [Issue #2](https://github.com/aarondash5-star/business-house-matrix/issues/2)  
**Reference reviewed release:** [Draft PR #3](https://github.com/aarondash5-star/business-house-matrix/pull/3)

## Actual release decision

**PASS: existing narrowly enrolled, synthetic-only autonomous coding MVP remains operational.**  
**NOT APPROVED/CERTIFIED: unrestricted multi-project coding, arbitrary shell/filesystem/model tools, generic delegated-task cancellation, autonomous machine-side GitHub push/merge, MCP write tools, spend, production publication, private Pine/TradingView or user-account privileges.**

Requested broad controller operations expansion was stopped by platform security checks before any code change. No alternate privileged route was attempted. Continue scoped extensions only after permitted enrollment, exact source review, negative tests and independent deployment approval. Do not describe unenabled features as live.

## Fresh real smoke receipts

| Test | Host | Receipt | Outcome |
|---|---|---|---|
| Existing controller service and 6-point selftest | Dell | `107c993c-a93a-4d74-8f3e-e431d61d2436` | PASS exit 0 |
| Governance unit tests | Dell | `6b629a67-462b-4611-bbf0-f75284995c9d` | 13/13 PASS |
| Guarded model agent unit tests | Dell | Same receipt | 7/7 PASS |
| Bubblewrap isolation and functional regressions | Dell | Same receipt | 5/5 PASS |
| Cross-tenant workspace denial | Dell | Same receipt | PASS, `project_not_enrolled` |
| Independent governance + agent unit tests | Mac | `211bb143-7d19-4437-b5f3-7f28cc9145db` | 20/20 PASS |
| Offline no-tools/no-MCP Granite model inference | Dell | `ea0822e5-4971-4aaf-9d1a-cabcfb37ab3a` | `READY`, exit 0 |
| Synthetic browser regression | Dell | `bda4da5d-c698-4352-a017-11079800e207` | 63/63 PASS, widths 320/360/375/390/430/768/1440 |
| Previously completed model→sandbox QA→local review | Dell | Same browser/receipt probe | Git SHA verified, 6 tests PASS, `published=false` |
| Dell control / operations / development SSH lanes | Dell | `42e37885-c1cf-4212-8376-3654b7c17ada`, `95826361-1800-49fc-8ef0-2ad614d7af80`, `3446cd7f-019c-40e2-b4ad-e4c40578ae37` | 3/3 PASS exit 0 |
| Mac control / operations / development SSH lanes | Mac | `72b4860c-1e12-4a8f-9a11-80f1f15cf225`, `931c186c-17f1-4527-95f9-902c29fd9b0e`, `fe23461d-ad3b-4e3c-a432-5c72c63dc809` | 3/3 PASS exit 0 |
| Legacy sandbox batch-path safety selftest | Dell | `dc3c25f2-1e1e-4d9b-8376-b0738f4558e0` | PASS exit 0 |
| Previous deterministic TaskGroup compatibility repair | Dell | `ad0a25c6-4de1-4a54-8a51-21df3174e819` | Historical `repair_known_issue` task completed with `new_qc=tests_passed` |

**Controller live SHA256 (reconfirmed):** `0e0060cfafae64a27cbdca34e0e63d03150ca84e54bde8ca5294ccc4cd6c6367`.  
**Rollback file SHA256 (reconfirmed):** `448a587b6c11bfbbd4618afc65b6f90a5f56bf54b075642817720c85228aa884`.  
**Live service:** `bhm-autonomy-controller.service` ACTIVE. No restart/config changes in this smoke pass.

## Debug results — nine historical needs_review tasks

All nine were already in the controller queue before this pass. The current queue contains nine completed and nine needs_review; there were **no queued or delegated jobs** during first preflight.

- **1 previous `dev_scoped_build`:** older v2 source was blocked by the receipt contract (missing required HTML `main` marker). The subsequent v3 and live v4 guarded jobs completed independently; do not reinterpret the old failure as passing.
- **5 `dev_proposal` tasks:** primarily incomplete proposal receipts, one remote proposal never reached approved outcome, one with missing explicit error. Still needs independent review; do not blindly replay.
- **3 older `sandbox_qa` tasks:** original batch runner failure; historical `/workspace` permission denied; known `TaskGroup.cancel` API incompatibility. Current Bubblewrap regression tests pass, and the saved `repair_known_issue` receipt for the TaskGroup pilot says `tests_passed`. Old failure receipts remain immutable for audit.
- **No new failures** in the fresh controller, governance, model, sandbox or browser suites.

## Capabilities, actual boundaries

| Gate | Available verified capability | Still gated |
|---|---|---|
| A1 | Fixed project + exact manifest, no-tool offline local model, strict validation, rootless Bubblewrap | Arbitrary-project code execution |
| A2 | Bounded model attempts, isolated unittest, SHA verified local review | Generic language build/retry/cancel |
| A3 | Independent Dell/Mac source tests, sandbox security, seven-width browser tests | Continuous production CI/QA for arbitrary apps |
| A4 | Local review commits; owner-scoped ChatGPT GitHub draft PR #3 | Dell autonomous remote repo credentials, auto-push/PR/merge |
| A5 | Known-defect guarded repair, verified older TaskGroup fix | Safe generic self-modifying or unbounded repair |
| A6 | Durable SQLite/idempotency, 6 SSH lane receipts | Proven dependency scheduling, fair throttling, active-worker cancellation |
| A7 | Previously deployed governed read-only developer document/MCP route | MCP write permissions, arbitrary endpoints/cross-project access |
| A8 | End-to-end synthetic-only live task certified, rollback and no-publish guarantees | General autonomous engineering release for new projects |

## Follow-up implementation policy

1. Retain known-working controller and bridge. Never reset/overwrite historical needs_review receipts or automatically replay ambiguous jobs.
2. Enroll each new public Matrix repo/manifest using a reviewed, exact-path policy and isolated worktree; maintain separate owner/tenant credentials for other repositories.
3. Implement stop/cancel with crash-safe receipts and race checks before allowing delegated-worker cancellation. Current platform prevented this general controller-operations expansion; do not circumvent.
4. Gate GitHub remote PR automation on reviewed per-repository credentials, independent diff/CI, and no-auto-merge; no user secrets on public workers.
5. Repeat exactly scoped end-to-end test after each approved change, plus independent Dell/Mac QA; preserve local commit and rollback.

**Summary:** all currently authorized bounded capabilities were smoke-tested and remained healthy. All proposed additional, unapproved general-purpose capabilities remain OFF rather than silently bypassing safeguards.
