# Dev Matrix Scoped Autonomous Coding — v5 Release Certification

**Release date:** 2026-10-22 (IST)  
**Component:** Business House Matrix / Dell Dev controller and Mac QA peer  
**Release class:** **CERTIFIED — LIMITED SCOPE**  
**Release ID:** `dev-operator-scoped-v5-20261022`

## Release verdict

**RELEASE APPROVED for the currently enrolled public synthetic static-HTML coding workflows.**

**NOT certified or released**: arbitrary-project/multi-repository coding, general AI-selected shell/network/MCP tools, Python/Node application deployment, independent PR/merge by Dell, production publication, account changes, spending or cross-tenant access.

This release is not a claim of a fully autonomous general-purpose software engineering department. The current agent still has fixed manifest enrollment and the model runs with tools disabled; its validated changes are applied and tested in an offline rootless Bubblewrap capsule, then committed to an unpublished local Git review.

## Source and deployed runtime

- Source feature branch: `feat/dev-autonomy-runtime-20261022`.
- Live deployed Dell controller: `~/matrix-controller/controller.py`, SHA256 **`df0cf3f968244d2e745d941f57d2225cfcd4a4147f55f7ce29c879e87027ffe4`**.
- Controller systemd user service: `bhm-autonomy-controller.service` **ACTIVE** at final postflight.
- Checked source: `brain/mvp-controller/controller-general-dev-v5-candidate-20261022.py` (exact same SHA256 as live).
- Dev agent and guard: `brain/dev-operator/agent_loop.py`, `protocol.py`, `workcell_runner.py`, `workcell_worker.py`.
- Enrollment: `matrix-dev-dashboard-v4`, `matrix-dev-qa-checklist-v5` only (plus preserved earlier fixed-scope `dev_scoped_build`).
- Rollback v4: `~/matrix-controller/controller.py.bak-20261022-generaldev-v5`, SHA256 **`8d33ced5f9bebfa7eaa70bb2cd345ab63a983a48572d53e5e4b5fbea9fd74d1f`**.
- Final controller counts: **11 completed**, **11 historical `needs_review`**, **0 queued/dispatching/delegated**.

## Release gates and evidence

| Gate | Independent receipt | Result |
|---|---|---|
| Dell unit policies, parsers, sandbox tests | Fresh 28/28, controller selftest | PASS |
| Mac independent v5 peer QA | Fresh 28/28, controller selftest, source SHA equality | PASS |
| Dell+Mac six SSH lanes | All control/operations/development receipts returned terminal exit 0 | PASS |
| First live Matrix controller E2E | Task `ead38a98-dabf-43c2-8934-98b2a453ffe7` | PASS, local commit `e618995f006ed4fdb13a02d31fa854ff1d4ee827` |
| Second live Matrix controller E2E | Task `a412a710-a197-400e-a992-811b2d4b5aa7` | PASS, local commit `57e5b47bb761e989ff1e96c7e862dacfa7a60396` |
| Independent controller receipt and Git SHA comparison | Read-only SQLite, immutable run receipt, `git rev-parse HEAD` | PASS |
| Cross-project, unknown manifest and duplicate submission | Live deny tests and duplicate idempotency | PASS |
| Browser E2E at six widths for each generated page | 12/12 with installed Chrome | PASS, zero network calls, page errors or overflow |
| Safe output | Published=false, pushed=false, no spend, local review | PASS |
| Historical failed tasks | 11 remain `needs_review`; no replay | PRESERVED |
| GitHub-hosted CI | No PR workflow runs returned for inspected feature commit | NOT PRESENT — do not claim CI pass |
| General-purpose coding + CI across languages | Not implemented/certified | NOT RELEASED |
| Production release, external Git writes or unrestricted root | Explicitly excluded | GATED |

## Release operation and guardrails

The live Dell controller has already been promoted to v5 with exact SHA checks, independently validated source and a verified rollback; **no further runtime restart is needed**. This release designates that running capability as the supported **scoped autonomous coding MVP**. The release branch is an immutable-point-in-time *source reference*, not an auto-deployment to public production. Keep the broader draft implementation PR open for review. Do not merge an unreviewed PR or authorize new external operations implicitly.

No changes to root permissions, Generic SSH bridge settings, other project data, auth, Mac thermal controls, production sites, cloud spend or credentials.

## Exit criteria for full general-purpose release (still OPEN)

1. Trusted multi-repository enrollment with per-project identity and independently verified immutable checkout.
2. Approved file, shell and dependency tools executable **only inside isolated per-project workcells**, not on the host.
3. Python, Node and browser integration tests plus security audits as independent QA profiles; CI required.
4. Concurrency, explicit cancellation/termination receipt, scheduling, crash recovery and thermal/CPU limits under stress.
5. GitHub branch/PR creation only with per-project credentials and independent review controls, no auto merge or production publish.
6. Real multi-file and multi-language application benchmarks with fault injection and independent Mac/Dell certification.

**Status statement permitted:** `Business House Matrix Dev Operator v5 — scoped autonomous coding MVP released and certified; full general-purpose autonomous Dev department remains under development.`
