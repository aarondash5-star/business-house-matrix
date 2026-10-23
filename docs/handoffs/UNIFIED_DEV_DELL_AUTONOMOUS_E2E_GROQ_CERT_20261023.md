# Unified Dev Matrix — Dell-only autonomous coding + external review certification

**Date:** 23 October 2026 (UTC)  
**Owner scope:** Skip Mac certification; run the **full autonomous execution loop** available on Dell, use OpenRouter or Groq for outside verification, preserve existing v6 until full integrated release gates pass.  
**Final decision:** **Dell isolated autonomous coding workcell: PASS within tested scope.** **Production unified Brain and permanent dispatcher-worker integration: NOT CERTIFIED / NO-GO.**

## Exact tested source

- Candidate branch: `feat/dev-universal-dynamic-intake-20261023`. Tested Dell candidate checkout: `068e05752ed9846f8b78ec6630a8fcf500d9aded`, source-context and failure-diagnostics patch included.
- Hosted CI branch head: `18bd4e5c5730ac80e4f1698eba58c877b3dae099` (added only a dedicated credential-free CI workflow after the candidate source commit).
- Previous static test improvements include real source-diff receipt requirements, immutable approved tests, read-only Git metadata, signed owner descriptors, rootless offline Podman, atomic replay-protected SQLite queue and named timeout cleanup.
- Certified v6 controller still active, verified SHA256 `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`. No production cutover, source replacement, permission or root changes, Git push/merge, payments, public publish or spending.

## Verified Dell test receipts

| Test | Result | Receipt |
| --- | --- | --- |
| Signed dynamic intake / deny invalid repo, identity, replay, quota and guest safety | **PASS 16/16** | `9653293e-5563-4d98-9ac6-c9bbbc0f189b` |
| Candidate source evidence, no-op rejection, git tamper, trusted QA and crash recovery | **PASS 17/17** on Dell after source-context patch | `d8b75cd7-d13e-438a-b495-7cbcbbc3acaa` |
| Real rootless Podman source edit and isolated trusted QA | **PASS**: changed fixture `app.py`, SHA evidence; protected `.git/config` write denied with read-only FS | `faa25f7f-96e9-48d2-9692-60fe2bea8be1` |
| Autonomous *local Qwen* → real guest coding → trusted QA → Git source fingerprint → ledger terminal | **PASS** in 2 real model steps, 55 seconds; `def add` fixed and test exit 0; terminal `review_ready` | `a88986fe-8f62-498d-a137-cd23982eed95` |
| Real public *Andaz* external repository (Groq free model) → model-generated command → Podman edit → signed test → source fingerprint | **PASS** one model step, 6.9 seconds, `index.html` only, test exit 0, `review_ready` | `977f83a5-b399-42d1-8915-f50c8dc1f80d` |
| GitHub-hosted credential-free candidate CI | **PASS** complete run `39957987004` and job `120428518719`: source security validator, compile and source evidence regressions | https://github.com/aarondash5-star/business-house-matrix/actions/runs/39957987004 |
| External Groq `gpt-oss-120b` evidence review of synthetic test | **Review response received**: synthetic bounded autonomous flow credible, integrated production NOT certified | `b2cc3e37-d4b7-4fb0-bb3a-a1f34e14bc49` |
| Independent external Groq `gpt-oss-20b` evidence review of real Andaz patch (different model from coding agent) | **Review response received**: bounded external edit credible, full service/production NOT certified | `4aa1dc24-24e9-4d03-8922-16eec8d199da` |
| v6 controller self-test and operational safety after candidate testing | **PASS 6/6**, active service and same certified SHA; no orphan test containers, existing SearXNG still up | `07941170-48ba-4c9d-9ced-972ac5d6eee1` |

### Real external Andaz source test details

- Public repository `karanzing1992/andaz-vibe-stay`, pinned checkout `21de8351238f9292e270a7635cbac7a08dd55c63`; modified **disposable checkout only**.
- Model: free-tier Groq `openai/gpt-oss-120b` through **existing** Dell `matrix-route.py`, explicit slot, `--public-input --development-test --no-fallback`, without exposing keys and with `PAID_API=DENIED`.
- Model changed `index.html` by adding `<meta name="color-scheme" content="light">` immediately after existing viewport meta. One source file changed. Signed trusted acceptance checked both lines; source fingerprint `de619ef89fd62a4f759aea14374cc1128e478b9063298e19da1c8ce5a65a3938`.
- Actual rootless Podman workcell executed changes offline with protected `.git` metadata; `review_ready`, `model_steps=1`, `qa_exit=0`. **This is only one small real-site source improvement; not a complete Andaz website or booking integration.** The changes were not pushed, merged or deployed.

### Negative/uncertain results preserved

- First local Qwen Andaz source job: `needs_review` after two model steps, no code diff, receipt `cd04869a-5968-4395-a8c8-77367b72d914`. Bounded source-context was then added and its unit suite passed.
- Subsequent local Qwen external-repo job: SSH timeout, **outcome uncertain**, receipt `3d07a559-1286-40cb-8bca-fe6fd73f37b5`. A separate read-only host check found no lingering test workcells and unchanged v6; job was not replayed.
- First Groq public job rejected by existing **2048-byte public-input limit** with no file edits, receipt `4734d11d-9dab-47d4-8386-7736ea39e1bf`. A new, smaller independent task was accepted and passed without changing provider limits.
- OpenRouter independent review attempt `openrouter-code` hit **HTTP 429**, did not fallback or spend, receipt `178b18bd-96ce-4c89-9e43-e15d3096c065`. A different approved free Groq `gpt-oss-20b` reviewer completed the evidence assessment instead.
- **Both external model reviews evaluated supplied public code/test evidence. They did not independently SSH into Dell or rerun the tests.** Direct external-source execution evidence comes from Dell receipts and hosted GitHub CI, not the model reviewers' words.

## Remaining release gates (Mac expressly waived)

1. **Permanent unified Brain intake:** No live authenticated Super Brain/central-v6-controller → universal workcell service route yet. Current tested jobs were directly invoked over the approved SSH CLI path in ephemeral processes; the older proposal-only Brain consumer is stopped, and `dev_proposal` must not receive new jobs.
2. **Worker orchestration:** Demonstrate the permanent Brain selects and manages existing enrolled design/dev/browser/QA workers and relays attributable terminal receipts across multiple actual tasks. The tested model+isolated workcell is not the entire departmental worker registry.
3. **Scoped CLI/bootstrap:** Previous candidate controller/CLI creation requests were blocked by platform-level tool safety checks. User authorization is recorded but does **not** override connector denial. A specifically reviewed legitimate controller interface is still required.
4. **Dev canary and rollback:** Run an isolated authenticated parallel service with monitoring, fatal/recovery and rollback drill, prove original v6 service and queue survive failures, then obtain release QA signoff.
5. **Broader actual user-project QA:** Full Andaz website/build, accessible responsive browser QA, StayCore integration (separately approved), multi-file Python/Node, dependency checks and bounded real defect repair remain outside the now-certified microtask scope. Source-writing PR identity and review controls must pass independently.
6. **Mac waiver:** Owner explicitly excluded Mac from *this* certification. Never claim Dell results prove Mac compatibility.
7. **Hosted CI drift:** CI passed exact tested branch at `18bd4e5...`, but any later source changes must rerun the same hosted safety and unit checks.

## Owner-facing status

**Certifiable claim:** Dell's isolated autonomous Dev workcell **can** accept signed jobs, use local Qwen or Groq free-tier routing to decide development actions, modify actual pinned repository code, run independent trusted tests, produce real source evidence and correctly fail closed. External model-based review and independent GitHub-hosted unit checks completed.

**Not certifiable:** A single deployed, always-running Super Brain → Development Brain → all specialists → production-ready website builder, or v6-to-new-controller production cutover. No installed new Brain service, automatic task dispatch, public website publishing or rollback drill is claimed.

**Deployment decision: NO-GO for unified production; PASS for the bounded Dell autonomous coding execution lane.** Preserve v6 and source receipts.
