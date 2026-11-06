# Six-Lane Deterministic Driver — Owner-approved implementation and release contract

**Date:** 2026-10-26 (IST)  
**Owning repository:** `aarondash5-star/business-house-matrix`  
**Scope:** six existing Generic Linux SSH lanes, three Dell and three Mac. No new transport, AI model, root, customer-data access or publishing permission.  
**Current release:** DESIGN / HANDOFF ONLY — **NOT DEPLOYED**. The six-Driver target is owner-approved, not evidence of implementation.

## 1. Requirement

A dedicated **non-AI Lane Driver** must follow each owner-authorized task through that lane, confirm actual worker and QA receipts, advance approved work, return failed QA to the responsible preceding stage for a bounded correction cycle, and eventually produce a verified terminal result or actionable blocker.

Each Driver follows the frozen workflow; it **never** creates a new project authority, changes a task's acceptance criteria, guesses at an outcome, evaluates artistic or technical quality itself, or executes model-selected shell commands. The **Dev Brain** owns worker selection/delegation; the **Super Brain** may broker the approved task and read status, not operate Dev worker internals.

## 2. Existing infrastructure to reuse (Golden Rule 0)

- Generic Linux SSH gateway v6/service 1.2.0: six owner-paired lanes, three each for `dell-linux` and `mac-linux`; existing per-lane durable task receipts, idempotency and per-lane single foreground command.
- Dell `bhm-autonomy-controller.service` (`0.2.4-manager-governance-v3` at audit) with project-scoped owner intake, quality and tool adapter admission.
- V1.3 controller-mediated execution gate (source branch `feat/dev-yard-execution-v13-20261026`), historical 36/36 + independent 8/8 tests.
- Existing `bhm-task-watchdog.timer` and `brain/automation/task_events.py` under local `matrix-gate-s-supervisor-20261023`: durable SQLite events/stalled-task warning; **observation only**, does not reroute failed jobs.
- Existing Python 3 stdlib, SQLite, `systemd --user`, structured receipts. No new package, provider, chargeable service, database or parallel bridge.

**Reuse decision:** Extend the existing owner-scoped event/receipt machinery and governed controller intake. Do **not** create a second competing controller or grant `task_events.py` command-execution rights. Proposed Driver transitions must be initiated only via an enrolled, fixed-purpose, authenticated controller action with independent receipt readback.

## 3. Instances and responsibility

Six logically isolated durable Driver identities:

| Driver ID | Host | Existing lane | Authorized scope |
| --- | --- | --- | --- |
| `dell.control` | `dell-linux` | `control` | Brief acknowledgements, state reconciliation; no long builds |
| `dell.operations` | `dell-linux` | `operations` | Existing operations tasks |
| `dell.development` | `dell-linux` | `development` | Build/test/recovery only through enrolled Dev Brain |
| `mac.control` | `mac-linux` | `control` | Brief acknowledgements, state reconciliation |
| `mac.operations` | `mac-linux` | `operations` | Existing Mac operations tasks |
| `mac.development` | `mac-linux` | `development` | Development only if separately enrolled and authorized |

A Driver is a **logical instance with a separate state/lease and audit cursor**, not an endless SSH foreground command. Never occupy or starve a control lane with a waiting process. An event-driven/bounded timer on the paired host is acceptable once source reviewed; no unrestricted background agent.

## 4. Frozen task envelope (minimum)

```json
{
  "schema": 1,
  "task_id": "owner-scoped-unique-id",
  "project_id": "exact-enrolled-project",
  "host_id": "dell-linux",
  "lane": "development",
  "approved_brief_sha256": "<64 lowercase hex>",
  "pipeline_version": "approved-version",
  "stages": ["admitted", "implement", "independent_qa", "review"],
  "responsible_stage_on_failure": {"independent_qa": "implement", "review": "implement"},
  "max_correction_attempts": 2,
  "release_allowed": false,
  "cost_allowed": false
}
```

The trusted controller MUST bind the envelope to the existing authenticated owner/project, valid task route, exact stage manifest and source identity. Client text may not supply an executable command, executable path, model shell, arbitrary URL, credential, recipient, Git remote or release override. Drivers never parse free-text instructions to select a tool.

## 5. Deterministic state machine

`NEW → ADMITTED → DISPATCH_QUEUED → RUNNING → AWAITING_RECEIPT → GATE_PENDING → (NEXT_STAGE | RETURN_FOR_REPAIR | BLOCKED | VERIFIED_COMPLETE)`.

### Required transitions

1. **Admit** only after successful owner/project/connector and stage policy checks; immutable task id, source hash, stage graph, allowed effect and release=false.
2. **Dispatch** by a controller-owned pre-enrolled fixed-purpose action. Store a transactionally reserved dispatch idempotency key, assigned lane, command hash from the controller (not the Driver), and expected downstream receipt ID.
3. **Observe** a real terminal receipt. A queued response, heartbeat or “model says done” is **not** a successful execution.
4. **Pass** only if trusted QA verifies the exact expected stage, artifact hashes and independently produced receipt. Advance one stage with compare-and-swap (CAS) on the current stage/version; write exactly one next dispatch.
5. **Fail and return** on a verified correctable QA failure only: write immutable failure evidence and a new attempt limited to the explicit `responsible_stage_on_failure` in the owner-approved stage graph. Worker owns the fix; Driver never patches files.
6. **Escalate** when failure class is noncorrectable, authorization/source or quality contract drifts, dependency missing, retry budget exhausted, task cancelled, worker offline, or receipt is `outcome_unknown`/stale. Do **not** auto-replay an uncertain action.
7. **Complete** only with matching final terminal receipt, independent gates and human review where required. `VERIFIED_COMPLETE` is NOT `OWNER_ACCEPTED` and never implies `PRODUCTION_RELEASED`.

Retries: default at most two **verified-correctable** returns per gate, with monotonic `attempt`, immutable historic receipt, backoff and one active writer per project/branch/worker lease. No retry on unknown outcomes or outside authorized scope.

### Failure routing

| Gate or event | Driver action |
| --- | --- |
| Tested code fails deterministic QA | Return to the recorded implementation stage, attach exact test/diff receipt |
| Design acceptance rejects output | Return to enrolled Design stage, attach critique; never self-certify |
| Security/auth/source hash fails | Stop and `BLOCKED_SECURITY`, never return for model self-repair |
| Worker heartbeat missing | Reconcile existing gateway journal first; `BLOCKED_UNCERTAIN` until known terminal |
| Max corrective attempts exceeded | `BLOCKED_RETRY_LIMIT`, preserve all evidence and notify owner |
| Approved stage passes | Advance exactly once, require next-stage acknowledgement |
| Cross-lane handover | Use separately authorized recipient lane, signed handoff and new correlation ID |

## 6. Data, isolation and state

Reuse SQLite with tables for immutable `driver_tasks`, `driver_attempts`, `driver_events` and idempotent `driver_outbox`; one owner/project/host/lane key; explicit foreign keys, UNIQUE dispatch idempotency key, monotonic stage_version, `BEGIN IMMEDIATE` reservation and busy timeout. File mode 0600, directory 0700, never in public Git. Each stage transition stores `source_sha256`, `receipt_ref`, `gate_status`, `actor`, `created_utc`, and a chained event hash. Validate downstream receipt through the enrolled gateway rather than reading another tenant's private journal. No credentials stored in task payloads.

The Driver must not inherit SSH sudo privileges, edit host network/bridge/system policies, scan other users' directories, connect private Pine without enrollment, access TradingView/Windows, notify customer channels or import Ashwakaal customer data.

## 7. Required smoke tests before promotion

1. **Six logical identities** created; only three Dell identities eligible while Mac is offline. Verify lane binding rejects unknown host/lane and prevents cross-project submissions.
2. Exact replay returns one existing dispatch receipt and does not duplicate worker execution.
3. Correct QA pass advances one stage, exactly once, even if the event is re-delivered.
4. Correctable QA fail returns to the recorded previous stage with test evidence; second correction can advance; third failure blocks.
5. Security failure cannot be treated as a correctable QA failure. Forged receipt, worker impersonation, stale SHA, altered plan or path, hostile task text all denied.
6. Crash/restart between dispatch reservation and acknowledgement recovers without double execution. `outcome_unknown`, stalled or expired tasks stay quarantined.
7. Offline Mac remains `OFFLINE_BLOCKED`, not `PASSED`; reconnection requires fresh authenticated heartbeat and readback.
8. Confirm resource limits, watchdog coexistence, no new network listener, no root/sudo changes and no worker-loop starvation.
9. Test all three Dell lanes with unique harmless synthetic jobs via the *existing authenticated gateway*, using individual terminal receipts and an independent safety reviewer. Test Mac's three only after online and separately authorized pairing status.
10. Canary new Driver code **beside unchanged certified controller**; rollback/drain test must preserve prior queue, task history, SSH lanes and V1.3 guard. No production release while gate tests fail.

Capture every terminal job ID, exit code, exact Git SHA, host receipt, source hashes, tests counts, negative cases, integration version, restoration path and reviewer. A syntactically valid file, a local unit test or a heartbeat is never sufficient certification.

## 8. Rollout with hard gates

- **D0:** source review and exact owner/Dev Yard integration permission. Only in an isolated `aarondash5-star/business-house-matrix` branch; no cross-repository worker borrowed.
- **D1:** implement reusable, stdlib-only Driver state machine and negative tests through the **existing enrolled Dell Dev Tool Yard**. Do not submit arbitrary code through unrelated fixed manifests.
- **D2:** establish a genuine fixed-purpose signed controller action `lane_driver_transition` and a matching read-only receipt query; audit V1.3 preflight, owner/project scopes and restart rollback.
- **D3:** run standalone staged tests and independent QA. Prove no duplicate dispatch, bounded retries and uncertain outcomes.
- **D4:** enable **Dell three Drivers** as protected nonroot supervised logical instances, then verify actual end-to-end synthetic task movement on all three lanes without slowing the control lane. Mark DELL_LIVE only after receipts, not on service start.
- **D5:** with Mac reconnected, repeat its local deployment, owner identity and three independent gate tests. Mark SIX_LANES_LIVE only then.
- **D6:** independently review no-spend/no-publish guarantees and set a source-pinned rollback checkpoint; synchronize verified platform change through authorized Moksha Master Supabase event inbox, not a new poller. Ashwakaal remains separate.

### Rollback contract

Disable only newly enrolled Driver dispatch while preserving monitoring and task journals; wait for known terminal receipts, quarantine uncertain tasks, rollback precisely new Driver files/bindings from SHA-verified backup, verify old controller/watchdog and original three SSH lanes per online host, then audit the ledger. Never blindly replay during rollback, downgrade the SSH gateway or change root/sudo.

## 9. Evidence at document creation (read-only, 2026-10-26)

- Dell `dell-linux` **online**, all three lanes fresh, owner shell enabled. Mac `mac-linux` **offline** (last lane heartbeat `2026-10-25 21:39:57–58 UTC`; age about 11.6 h at check). Six-lane release cannot be certified.
- Dell controller active; existing governance remains observation-only for manager status, proposal-only route is not a development executor.
- `bhm-task-watchdog.timer` active; `bhm-task-watchdog.service` last observed `Result=success`, `ExecMainStatus=0`, trigger 2026-10-26 14:38:25 IST. That verifies watchdog execution, **not** a newly deployed Lane Driver.
- No `driver` service appeared in live `systemctl --user list-units`. The existing fixed-function Super Brain↔Dev Brain duplex was previously proven to support only `controller_status`, not generic code dispatch.
- Dell SSH read-only terminal receipts `a090ea75-1624-40f7-acf8-f8846c980b82`, `cf9f73b5-9c80-4a0f-9dee-81394b689b29`, `37c962da-7f9c-4882-afe5-55e444049e41`, `107dbe6c-3d1e-4e29-96d3-b975527ffc9e` all completed exit 0.
- No Driver code, controller dispatch adaptation, new service or source change was deployed by these diagnostics. **Current state is D0 pending; deployment NO-GO**, rather than fabricating six live drivers.

## Source and accountable next executor

Owner-authorized development task belongs to **Matrix Development Brain**, via proper fixed-purpose controller intake after enrollment, with QA/QC independent. If that ingress does not exist, report `NOT ENROLLED`, prepare reviewable integration, and never silently direct its coding/browser workers or replace a forbidden task with unconfined SSH. Issue #2 tracks overarching Dev autonomy, and this contract should have a distinct driver-specific tracker.
