# Dev Matrix Tool Yard — Super Brain Operator-Led Mode

**Project:** Independent Business House Matrix  
**Effective:** 2026-10-23 (Asia/Kolkata)  
**Host:** Dell `dell-linux`; Mac QA waived / not changed  
**Decision:** Replace the continuously running **Matrix autonomous dispatcher** with an **on-demand development tool yard controlled by the ChatGPT Super Brain (owner approval path)**.  
**Runtime status:** **LIVE for on-demand operations/development SSH lanes; autonomous dispatcher OFF**.  
**Scope:** No publishing, spending, production website changes, root/sudo grants, model-provider changes, or uncontrolled background Dev job execution.

## Executive result

The existing `bhm-autonomy-controller.service` was **disabled and stopped**, with terminal Dell receipt `a4fbbba0-0ff8-407c-a162-53eff0cbdde7` (exit 0). Readback returned `ActiveState=inactive`, `UnitFileState=disabled`, `MainPID=0`.

The Matrix Dev environment remains a reusable **tool yard**, not an independent autonomous Brain. The Super Brain receives owner tasks, chooses and operates the already approved tools through the v6 SSH bridge, supervises their receipts, writes/reviews code only within an approved isolated checkout, runs QA, and reports results for owner decision. No separate self-directed Dev agent is authorized to pick up or execute tasks.

The existing fixed-function Super ↔ Dev duplex remains enabled as a **status-only sidecar**, not a job runner. Since the autonomous controller is intentionally off, its fixed status response reports `controller_service=inactive` and `state=degraded`. That means “autonomy off,” **not** “tool yard unusable.” The direct authenticated SSH operations and development lanes were exercised successfully after deactivation.

## What was deactivated, retained, and not touched

| Component | Final state | Reason |
|---|---|---|
| `bhm-autonomy-controller.service` | **disabled, inactive** | Stops 20-second autonomous Matrix dispatch loop |
| v6 Generic Linux SSH operations/development lanes | **retained, tested** | Super Brain on-demand execution transport |
| `bhm-superdev-ssh-duplex.service` | **enabled, active** | Fixed read-only status reply; no arbitrary code dispatch |
| `bhm-searxng.service` | **active** | Reusable local research/search tool |
| `bhm-marketing-research-api.service` | **active** | Independent owner-local research API |
| `bhm-research-relay.service` | **active** | Existing signed research-only relay |
| `bhm-task-watchdog.timer` | **enabled, retained** | Passive task-stall/event receipts; not the autonomous Dev dispatcher |
| Failed legacy Gate E/Dev benchmark units | **left untouched/inactive** | Preserve history and receipts; no automatic resurrection |
| Mac, Pine, WordPress, browser accounts, production sites | **not changed** | Outside this Dell conversion |

The existing Matrix controller file SHA-256 was unchanged:
`b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`.

**Impact:** Tasks previously dependent on the 20-second dispatcher will no longer progress autonomously, including non-Dev tasks in that shared controller queue. The separate research services continue to run, but they do not replace the stopped dispatcher. The owner must authorize any reactivation.

## New operating contract

1. **User → Super Brain:** The owner gives a task and its permission boundaries. The Super Brain confirms only decisions that materially require owner choice or higher authority.
2. **Super Brain → Tool Yard:** Use the existing authenticated Dell SSH bridge directly, selecting an operations or development lane. Do not enqueue into the stopped `controller.py serve` dispatcher.
3. **Development workspace:** Reuse an existing project checkout where safe; otherwise create a named isolated worktree/checkout. Preserve other work and repo history. No unattended edits in production paths.
4. **Execution:** Run exact scoped build/test/inspection commands. No generic model-driven arbitrary shell bootstrap or credential bypass. Keep one writer per project/worktree.
5. **QA:** Syntax/build/unit tests, isolated runtime tests, browser/mobile QA where relevant, security and regression checks, negative-path tests, and actual artifact review. A model proposal is not execution QA.
6. **Audit:** Wait for terminal SSH receipts; inspect exit code, logs, diff, artifacts, and independent QA outcomes. Repair failures under the same task scope; never replay uncertain jobs blindly.
7. **Decision gate:** Report evidence and blockers to owner. Merge, publish, spend, root/security changes, and cross-project access require their normal separate approvals.
8. **Record:** Update the project GitHub branch/handover with code SHA, receipts, test matrix, rollback and next action.

This converts the Dev Matrix into a supervised engineering capability under the Super Brain, not a competing decision-maker or independently acting agent.

## Verified local tool inventory

| Tool | Dell state | Tool-yard use |
|---|---|---|
| Python | 3.12.3 | Code, standard-library tests, scripts |
| Git | 2.43.0 | Isolated checkouts, diffs, review |
| Node.js | 24.22.0 | Front-end builds and tests |
| npm | 11.19.1 | Existing project dependency tooling; no auto installs |
| Mozilla Firefox | 146.0.1 | **Real offline headless render passed** |
| Podman | 4.9.3, rootless=true | **Networkless, read-only constrained container passed** |
| SQLite | installed | Local private ledgers and regression fixtures |
| ripgrep / curl / jq | installed | Inspection/data processing |
| Ollama | installed; **not used** | Requires separate model-license/thermal/expense review before task use |
| Aider | installed in a separate pipx venv but not on PATH; **not certified** | Optional future reviewed tooling only |
| pytest / Playwright / Selenium CLI/modules | absent | Not required for this release; no auto install |
| Google Chrome | installed; **not selected** | Firefox preferred for OSI-first browser QA |

All release tests used existing local software. No new paid SaaS/API, model, package download or root installation was introduced.

## Regression and smoke certification

**Disposition: PASS for the exercised operator-led tool yard scope; bounded limitations below.** These are real terminal receipts, not queued acknowledgments.

| Gate | Receipt / evidence | Outcome |
|---|---|---|
| Disable autonomous dispatcher | `a4fbbba0-0ff8-407c-a162-53eff0cbdde7` | PASS: inactive, disabled, PID 0 |
| Preserve other services/v6 controller | `9870adf9-4bf5-48ae-8a04-80a81978b2fb` | PASS: status sidecar + research services active; original SHA |
| Existing controller safety selftest | `bfa6693b-0e31-4467-bfbb-18f720996d36` | PASS: 6 checks — queue persistence, idempotency, blocked production route, isolation, privacy, conservative recovery |
| Installed tools discovery | `3faf0ccb-e73e-44ab-8431-936543bf327b`, `c83936c9-5bb5-48cb-ba28-59690b29cfb6` | PASS: versions and missing tools honestly inventoried |
| Operator-led synthetic integration suite | `813132fa-9f92-4095-8471-18044f95c0d5` | **PASS: 11/11** in ~22s, exit 0 |
| Direct Super Brain → development SSH command | `df95ac96-8c93-441e-896d-29f54202ed7c` | PASS: exact stdout and exit 0 |
| Gateway idempotent retry | Same idempotency key returned same job ID `df95ac96-8c93-441e-896d-29f54202ed7c`, `deduplicated=true` | PASS: no duplicate execution |
| Status sidecar with controller intentionally off | Send `c6daac2f-5507-417e-b39c-d1a593fdf5b7`; reply `52a63037-785e-46da-a9ea-b0541308f6b8` | PASS: reply correlated, chain verified; dispatcher remained inactive |
| SSH failure/exit propagation | `7515b746-cebe-4f55-9c90-cb8ca19438ad` | PASS: deliberate synthetic failure surfaced as `status=failed`, `exit_code=17` |
| Existing duplex safety regression | `06dd7b0a-3ca3-4cb9-8ab4-51306c28e458` | **PASS: 12/12**, exit 0 |
| Rootless sandbox inventory | `4a9e69a3-70c8-44e0-be77-366b1045d227` | PASS: rootless Podman and existing local Python image confirmed |
| Bounded rootless sandbox execution | `8b7c1f87-ab9f-4b94-9011-8788a46e657e` | PASS: existing Python image, `--pull=never --network=none --read-only --pids-limit=64 --memory=128m --cpus=0.25` |
| Final state readback | `d69d20ea-6e2b-4be8-b01e-5428ac76dbc6` | PASS: autonomy still disabled; other services active; checkout clean; v6 hash unchanged |

The 11-case operator-led suite covers:
1. Autonomy remains disabled.
2. Status sidecar remains available.
3. Research services remain active.
4. v6 controller SHA is intact.
5. Isolated Python edit and compile.
6. SQLite unique-key constraint and transaction.
7. Node runtime JSON execution.
8. Git init/add/commit/status in temporary workspace.
9. Nonzero exit handling.
10. Bounded subprocess timeout.
11. Real local Firefox headless HTML render/screenshot.

Source: `tests/test_dev_toolyard_operator_smoke.py` on this branch. It uses only Python standard library, fixed subprocess argv (`shell=False`), a temporary test workspace and no external network. The script is a test fixture, **not** a generic remote shell broker.

## Known limits and explicit NO-GO items

- **SSH control lane:** Direct `linux_control_run` returned `INVALID_ARGUMENT`; control heartbeat was stale since 2026-10-22. It was **not certified** in this change. The operations and development lanes were healthy and tested. Do not bypass the control-lane denial through alternate credentials or raw gateway calls.
- **Autonomous Dev dispatch:** OFF intentionally; no unattended task execution certification is claimed.
- **Exhaustive testing:** “All possible situations” is not provable. This suite covers representative positive, negative, recovery, isolation and runtime paths. Physical reboot, extended WAN failure, heavy sustained load, Mac cross-host QA, full user-driven five-page Andaz delivery and production browser funnels were **not** tested here.
- **Existing Andaz workcell:** Previously ended `needs_review` after 35 steps due invalid Python edit syntax and step-budget exhaustion; it was not silently resumed or overwritten.
- **Watchdog:** Existing passive timer remains enabled and can create task-stall event receipts. It does not re-enable the stopped autonomous controller; verify that again during future changes.
- **External models:** Ollama/Aider are not an excuse to select unverified non-OSI models or invoke paid providers. Their presence is inventory, not certification.
- **No website publishing, spending, PR merge, permission change or production deployment** occurred as part of this conversion.

## Daily reuse commands and release discipline

Run through the **existing authenticated Dell SSH plugin**; do not use public inbound SSH or pasted credentials.

**Operations lane — confirm mode:**

```bash
systemctl --user show bhm-autonomy-controller.service -p ActiveState -p UnitFileState -p MainPID
systemctl --user show bhm-superdev-ssh-duplex.service -p ActiveState -p UnitFileState
systemctl --user is-active bhm-searxng.service bhm-marketing-research-api.service bhm-research-relay.service
```

**Development lane — run regression suite:**

```bash
python3 -m unittest -v /var/lib/generic-linux-automator-exec/matrix-dev-toolyard-cert-20261023/tests/test_dev_toolyard_operator_smoke.py
```

**Development lane — isolated sandbox example (pre-existing local image only):**

```bash
podman run --rm --pull=never --network=none --read-only --pids-limit=64 \
  --memory=128m --cpus=0.25 docker.io/library/python:3.12-alpine \
  python -c 'print("isolated QA")'
```

For a real task, the Super Brain must select exact named worktree, source SHA, commands and output target, then inspect all terminal receipts and diffs. Do not use `controller.py submit` expecting an autonomous worker while the service is disabled.

**Reactivation / rollback of this architecture (owner approval required):**

```bash
systemctl --user enable --now bhm-autonomy-controller.service
```

This would restore the previously enabled autonomous dispatcher and is **not** authorized by this report. It must be explicitly approved as a separate future change and followed by fresh regression tests. Until then, preserve the disabled state.

## Open Source / Reuse / Cost Gate

- **Reused:** owner-approved v6 SSH/CLI, Git, Python, Node, Firefox, Podman, SQLite, existing Matrix code and QA assets.
- **New code:** Dell-specific supervised Tool Yard regression suite only; no new general-purpose autonomous agent or transport.
- **New paid services/calls:** none.
- **New installs:** none. Existing third-party license inventory remains subject to the project's OSI-first policy. Installed proprietary Chrome was not selected.
- **Rollback:** re-enable the old controller only with explicit authorization; no code/data cleanup or deletion needed.

## Handover

**Next task:** Have the Super Brain execute an approved, narrowly scoped real development task directly using Dell operations/development lanes, with branch isolation, source-to-claim QA, browser checks and receipts. The Andaz five-page job is a suitable candidate after a fresh bounded task brief. Do **not** switch autonomous dispatch back on to run it.

**Short continuation prompt:**  
`Continue Matrix Dev Tool Yard operator-led mode. Read this handover on feat/dev-toolyard-superbrain-control-20261023. Keep bhm-autonomy-controller disabled. Use Dell SSH operations/development lanes directly, preserve v6, execute an approved isolated Dev task, collect receipts and audit. No publish/spend/root changes.`

## Post-release control-lane diagnostic

Read-only Dell systemd receipt `cb30299e-5b10-4847-8390-14f17e159813` showed all three underlying SSH worker system units (`generic-linux-automator.service`, `generic-linux-automator-lane@development.service`, `generic-linux-automator-lane@control.service`) **loaded, active and enabled**. However ChatGPT `linux_control_run` still returned `INVALID_ARGUMENT` and the gateway control heartbeat remained stale. This points to client/gateway command admission or lane routing rather than proving the control worker process is stopped. **No alternate credential/transport bypass was attempted; control command execution remains unverified.**
