# Business House Matrix — Dev Matrix Release QA / Security v6 Handover

**Recorded:** 22 October 2026 (IST)  
**Repo:** [aarondash5-star/business-house-matrix](https://github.com/aarondash5-star/business-house-matrix)  
**Ownership:** Independent Business House Matrix (NOT Moksha Master).  
**Handover purpose:** Transfer all verified deployment, certification, debug and outstanding work into the next chat without repeating failed jobs or silently expanding permissions.

> **STOP STATE / LAST USER INSTRUCTION BEFORE THIS DOCUMENT:** The user said **"Stop"** after the v6 release audit. The assistant stopped tests, deployments, debugging and GitHub edits at that point. A subsequent user message authorized ONLY documentation and preparation of this handover. **Do not resume execution, testing, deployment, restarts or authorization changes unless the next user explicitly directs it.** Do not confuse stopping agent operations with stopping the already-running Dell systemd controller.

## 1. Executive snapshot — what is and is NOT done

| Area | Last verified result | Confidence |
|---|---|---|
| Dell Generic SSH | Online during last v6 verification | Live heartbeat then; recheck on resumption |
| Mac Generic SSH | Online during last v6 verification | Live heartbeat then; a Mac v6 certification command was blocked by platform checks |
| Dell Matrix controller v6 | **Active**, SHA256 **`b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`**, matching v6 candidate source | Direct read-only terminal receipt |
| Dell v6 controller selftest | PASS, six governance assertions | Direct terminal receipt |
| Dell security+unit suite | **38/38 PASS** on deployed-candidate code | Direct terminal receipt |
| Mac strict security-patch code suite | **38/38 PASS** on an earlier v6 security-patch revision | Direct terminal receipt from preceding patch phase |
| Final v6 Mac controller/source peer check | **NOT independently re-verified** — specific fresh Mac tool call was blocked by platform checks | OPEN gate |
| v6 autonomous coding smoke task | **PASS**: isolated QA, local review commit verified | Direct terminal receipt |
| v6 generated output browser QA | **NOT VERIFIED** after the hardened release | OPEN gate |
| v5 browser suite | 12/12 PASS at 320/360/390/430/768/1440px for two *older* outputs | Historical evidence; does not certify v6 page |
| Controller queue | **12 completed, 11 needs_review**, **0 in-flight** at v6 audit | Last live audit |
| Full general-purpose Dev autonomy | **NOT certified**. Only owner-enrolled, synthetic static HTML offline coding lane is proven | Architectural scope |
| Production publishing, remote Git push, spend or root changes | Not authorized; remain gated | Security policy |

**Terminology:** “v6 deployed” means its controller and strengthened offline QA code were observed live on Dell. It does **not** mean the v6 GitHub source was merged, tagged as a general-availability release or authorized for arbitrary projects. The v5 source release and v6 hotfix source are distinct.

## 2. Exact source-of-truth locations

- **Active v6 security hotfix branch:** `fix/dev-operator-static-html-hardening-20261022`
- **Verified v6 controller source:** `brain/mvp-controller/controller-general-dev-v6-candidate-20261022.py` — Git commit `e1d97ba35ff74c5446126891d8f56e54ac42c975`; live/controller file SHA256 `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`.
- **Strict HTML policy:** `brain/dev-operator/static_html_policy.py`.
- **Coding agent:** `brain/dev-operator/agent_loop.py`.
- **Policy, workcell and sandbox:** `brain/dev-operator/protocol.py`, `workcell_runner.py`, `workcell_worker.py`.
- **New adversarial regression suite:** `brain/dev-operator/tests/test_static_html_policy.py`. Existing parser, manifest and workcell tests remain.
- **Enrolled v6 smoke manifest:** `brain/dev-operator/enrollments/matrix-dev-security-v6.json`.
- **Base v5 released source branch:** `release/dev-operator-scoped-v5-20261022`, release document `docs/releases/DEV_OPERATOR_SCOPED_V5_CERTIFIED_20261022.md`.
- **Original feature branch:** `feat/dev-autonomy-runtime-20261022`; development **draft PR [#8](https://github.com/aarondash5-star/business-house-matrix/pull/8)** still points to this v5-oriented branch, *not* the v6 hotfix branch, last checked.
- **Open expansion [Issue #2](https://github.com/aarondash5-star/business-house-matrix/issues/2)**.
- Historic v4/v5 detailed live receipts: `docs/receipts/DEV_MATRIX_V4_V5_LIVE_CERTIFICATION_20261022.md`.
- **This handover:** `docs/handoffs/DEV_MATRIX_RELEASE_QA_V6_HANDOVER_20261022.md` (hotfix branch).

## 3. Architecture and immutable bounds

Existing components: Dell `~/matrix-controller/controller.py` durable SQLite/stateful `bhm-autonomy-controller.service`; local Pi/Ollama `granite4:3b` in offline **no-tools/no-MCP** mode; owner-enrolled repository/project/path/immutable baseline SHA/test-profile manifests; rootless **Bubblewrap** separate no-network workcell; capped 3 model attempts, independent sandbox QA, unpublished **local-only Git review** commits and controller attestation. Mac is the independent QA peer. Three Generic SSH lanes per machine: control, operations and development. Preserve existing integrations, rollback files, model cache and session architecture.

Never silently grant unrestricted model-selected host commands, root, private Pine/Moksha credentials, cross-project mounts, remote GitHub merges, production publishing, purchase/spend, unapproved MCP writes or project enrollment. This release is independent of Moksha Master. OSI-compatible open-source models/components required.

## 4. Progress history and verified working baseline

### A1 / synthetic coding route

Original `dev_scoped_build` executed the enrolled Pine synthetic, no-private-data sample `dev_matrix_synthetic_release_v1`, 6/6 isolated QA and local-only Git review. GitHub PR #3 remained a separate draft review track. Not a general-purpose tool-using developer.

### v4 / first general coding live pass

- Controller v4 SHA256 `8d33ced5f9bebfa7eaa70bb2cd345ab63a983a48572d53e5e4b5fbea9fd74d1f`.
- Manifest: `matrix-dev-dashboard-v4`, controller task `ead38a98-dabf-43c2-8934-98b2a453ffe7`.
- Two model attempts: first proposal rejected, second accepted; sandbox QA passed.
- Unpublished local review Git commit `e618995f006ed4fdb13a02d31fa854ff1d4ee827`.
- Earlier v2 malformed JSON (three attempts) and v3 Qwen timeouts (three attempts) failed closed and remain in historical audit, never replayed blindly.

### v5 / second distinct controller-managed pass; scoped MVP release

- Controller v5 SHA256 `df0cf3f968244d2e745d941f57d2225cfcd4a4147f55f7ce29c879e87027ffe4`.
- Manifest: `matrix-dev-qa-checklist-v5`, task `a412a710-a197-400e-a992-811b2d4b5aa7`.
- One Granite model attempt; independent sandbox semantic HTML QA PASS.
- Unpublished local Git commit `57e5b47bb761e989ff1e96c7e862dacfa7a60396`.
- Fresh cross-host v5: Dell **28/28**, Mac **28/28**, 6/6 independent SSH lanes (exit 0); both historic pages later passed 12/12 headless Chrome browser viewports, no external requests/page errors/overflow.
- Versioned source branch `release/dev-operator-scoped-v5-20261022`. PR #8 left **draft**, not merged. No PR-hosted GitHub Actions CI runs were reported: do NOT claim CI certification.
- Despite passes, v5 release is scoped, not an unrestricted autonomous Dev department.

### v6 deep release audit — discovered and fixed security defect

1. A deeper active-content negative smoke test against old HTML generator unexpectedly accepted inline `on*` event attributes, refresh metadata, `<object>`, CSS external URL loading and `javascript:` links. Initial adversarial result: safe baseline accepted; **five malicious classes erroneously accepted**. **Old v5 security certification no longer sufficient for final signoff.**
2. Added `static_html_policy.py`: structural HTML5 allowlist with permitted tags/attributes, document language and viewport, disallowed active/embedded/interactive tags, URLs, unsafe CSS, CSS imports, meta refresh and event handlers.
3. Applied validator twice: first on generated HTML in `agent_loop.py`, then independently inside the Bubblewrap `workcell_worker.py`, with read-only policy mount from `workcell_runner.py`.
4. Added `test_static_html_policy.py` adversarial tests. First combined suite found QA check-name regression (`html_semantics` vs `html_semantics_and_active_content`), fixed in `workcell_worker.py`. These intermediate failed receipts remain useful debug evidence; don't rewrite history.
5. After fix: **38/38 PASS on Dell and Mac** on patch revision `2ea1e3c64f1e66916dec430255b62edcc9294c3f`.
6. Strict validator correctly rejected BOTH historical generated pages: v4 incomplete document `metadata_outside_head`; v5 uses an interactive checkbox outside approved static scope `active_or_unknown_element`. **Do not retroactively claim those previous outputs conform to v6.** Their existing original runtime receipts are preserved.
7. Updated Granite prompt to request a complete inert HTML5 head/body/main document, no interactive content, imports or external resources (prompt fix commit `ebe3173ec16bae210f4119891b9d0bfe800712fb`).
8. Added **new** enrolled task `matrix-dev-security-v6` targeting `frontend/dev-release-security-v6.html` and controller v6 candidate.
9. **Observed deployed v6**: Dell `~/matrix-controller/controller.py` SHA256 **`b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`**, `bhm-autonomy-controller.service` ACTIVE; v6 release directory staged, candidate source commit `e1d97ba35ff74c5446126891d8f56e54ac42c975`. Controller selftest PASS.
10. **Live v6 task** `matrix-dev-security-v6`, UUID **`e92144e5-0755-4945-b1a3-758702de0c75`**: one model attempt, `status=verified_local_review`; independent QA `html_semantics_and_active_content` **PASS**; exact generated file `frontend/dev-release-security-v6.html`; local Git commit **`2b70a5994400f4dda02cebb7a9e233691f1233d8`**, independently checked against `git rev-parse HEAD`; `published=false`, `pushed=false`; controller recorded `completed` at `manifest_enrolled_sandbox_qa`.
11. **Last v6 audit:** `completed=12`, `needs_review=11`, `inflight=0`, service active. Dell final 38/38 PASS plus six controller selftest assertions. A fresh Mac v6 source/controller certification attempt was **blocked by platform security checks**, so do not claim final post-deployment Mac peer certification.
12. **User said STOP.** No further v6 tests, deployments, code changes or GitHub edits were initiated after that stop, except the later explicitly requested handover documentation.

## 5. Unresolved blockers and exact next actions — ONLY with renewed approval

**Gate A — release verification:** First read this handover, source branch, release docs, the current live controller checksum and existing receipts. Only *with user instruction to execute*, verify recent Dell + Mac heartbeats and rerun the exact **v6** Mac 38-test + controller source SHA peer QA. If a tool security check blocks the operation, do not bypass it.

**Gate B — independent rendered output:** Run bounded Chromium/Playwright smoke on newly generated v6 `frontend/dev-release-security-v6.html` at 320/360/390/430/768/1440px, with network egress intercepted; check visible main, viewport, overflow, console errors. This has **NOT** been done for v6 (the 12/12 earlier browser test covered *v4/v5*). Reuse installed system Chrome; default Playwright download/cache previously mismatched but system Chrome worked. No installs unless approved.

**Gate C — stronger security review:** Review strict parser edge cases, including HTML entities, CSS escaping and malformed markup, duplicate tags, SVG/MathML and forbidden URL-bearing attributes; test failures must fail closed. Do not equate an allowlist with complete XSS security proof.

**Gate D — v6 source release:** The *v6 hotfix branch* has not been verified merged or turned into a separately certified source release. Keep draft PR #8 and v5 release branch distinction clear. Only promote v6 when QA evidence and user-authorized release rules pass. Do not auto-merge/publish.

**Gate E — full general Dev:** Still missing independently enrolled arbitrary repositories, generic per-repo read/edit/build/run tools within isolated workspaces, Python/Node test certification, bounded worker cancellation and recovery, GitHub PR write identity, CI, independent security and cross-project real benchmarks. **Not covered by synthetic HTML MVP.**

**Rollback/incident:** Preserve prior versioned Dell controller backups under `~/matrix-controller/controller.py.bak-20261022-generaldev-v*` and historical run receipts. V5 SHA `df0cf3f9...`; v4 SHA `8d33ced5...`. A v6-specific rollback backup was **not independently verified in the final read-only status**; check it before any new promotion. Do not change SSH/root without explicit authorization.

## 6. Short copy/paste next-chat prompt

> Continue Business House Matrix Dev Matrix v6 from the GitHub handover: https://github.com/aarondash5-star/business-house-matrix/blob/fix/dev-operator-static-html-hardening-20261022/docs/handoffs/DEV_MATRIX_RELEASE_QA_V6_HANDOVER_20261022.md . Read it fully and the referenced source/receipts first. Respect the prior STOP: **report status and remaining release gates only; do not execute tests, deploy, restart or change configuration unless I explicitly authorize it.** Reuse Dell/Mac and existing integrations; preserve security gates and historical receipts.
