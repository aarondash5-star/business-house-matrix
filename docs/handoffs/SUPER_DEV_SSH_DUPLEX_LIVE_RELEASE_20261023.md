# Super Brain ↔ Dev Brain SSH Duplex — Live Release Report

**Project:** Independent Business House Matrix  
**Release date:** 2026-10-23 (Asia/Kolkata)  
**Host:** Dell `dell-linux` only  
**Release classification:** **GO — persistent fixed-function two-way status communication**; **NO-GO — general autonomous Dev job execution**  
**Source branch:** `feat/super-dev-ssh-duplex-20261023`  
**Deployed source commit:** `eb66bd0cc7006f47576d538c8e0213876b8933ab`  
**Deployment model:** Existing authenticated Generic Linux SSH v6 gateway, nonroot user service, private SQLite mailbox; no new public endpoint.

## Executive result

The Super Brain can submit a typed, bounded `controller_status` request through the existing authenticated Dell SSH bridge. The persistent Dell listener detects the request and writes a correlated Dev Brain result back to the same hash-chained SQLite mailbox. The Super Brain then retrieves and verifies that result using the existing SSH operations lane. Canary, production, and post-restart exchanges all completed with exit code 0 and verified two-event chains.

The sidecar service `bhm-superdev-ssh-duplex.service` was installed into the existing `generic-auto-exec` user systemd manager and enabled. Latest readback at **2026-10-23 20:32 IST**: `LoadState=loaded`, `ActiveState=active`, `SubState=running`, `UnitFileState=enabled`, `MainPID=50789`, `NRestarts=0`.

This is **not** a release of free-form task/code execution, independently signed local roles, model orchestration, Git merging, publishing, spending, or a full nine-department autonomous Matrix.

## Architecture and trust boundary

```text
ChatGPT Super Brain
    |
    | existing owner-authenticated Generic Linux SSH v6 task
    v
Dell nonroot command lane: super_dev_ssh_duplex.py send
    |
    v
Private SQLite append-only, hash-chained mailbox
    |
    | 3-second polling by systemd user sidecar
    v
super_dev_ssh_listener.py → super_dev_ssh_worker_once.py
    |
    | fixed read-only controller_status adapter only
    v
Existing Matrix controller status + service active check
    |
    v
Correlated Dev `result` in mailbox
    |
    | existing SSH operations lane: poll / verify
    v
ChatGPT Super Brain
```

- No new TCP/HTTP listener or public SSH port in the duplex code path.
- No new credential, model provider, paid API, or privileged/root service.
- SSH-facing CLI is restricted to Super messages. The fixed Dev adapter uses internal mailbox methods. This is defense-in-depth, **not independent cryptographic sender authentication**.
- SQLite default: `~/.local/share/matrix-dev-brain/ssh_duplex_v1.sqlite3`; file mode 0600, parent created mode 0700. Messages are bounded to 16 KiB; threads to 256 events.
- Message IDs are idempotent; reply correlation and chain verification are tested.
- Unit constraints: `NoNewPrivileges=yes`, `UMask=0077`, `MemoryMax=128M`, `CPUQuota=25%`, `TasksMax=32`, `LimitNOFILE=128`, `Restart=on-failure`.
- Existing v6 controller file SHA-256 remained `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`; original controller service remained active.

## Certification gates and real Dell receipts

All listed job receipts reached terminal `completed` with `exit_code=0`. A queue acknowledgement alone was not treated as success.

| Gate | Evidence / receipt | Result |
|---|---|---|
| Source unit/compile QA | `fc8d8de5-79ef-4fd9-b30f-7beee14e2d41` | **PASS** — 12 tests, Python compile, source head `eb66bd0` |
| Existing-controller preflight | `b6a4871a-084d-4976-9563-90daab2d0546` | **PASS** — active and original SHA |
| Isolated release checkout | `66f81859-39de-45b7-8d2d-a2e37bd985bf` | **PASS** — exact commit, clean working tree |
| Transient fixed-function canary | `9d288285-a06e-4a30-986a-4a58f4867ab9` | **PASS** — `systemd-run --user` start |
| Canary Super → Dev send | `f608c77a-5b56-43ea-b729-647d59d11ec8` | **PASS** — request seq 3 |
| Canary Dev → Super response + verify | `eb49d8ad-6db4-4b0c-b7e1-ab74e79459a9` | **PASS** — nonce matched, `state=ready`, seq 4, chain verified |
| Canary rollback/expiry readback | `bff0bdc0-f494-41de-b5bd-fbdffec55526` | **PASS** — `Result=success`, inactive, original controller unchanged |
| Persistent user-unit installation | `5c719284-f138-4f48-8444-31130f86a182` | **PASS** — unit loaded, initially disabled/inactive |
| Live activation | `7eac789d-f555-4dac-8ee6-25513d985c6a` | **PASS** — enabled + active, PID 48014 |
| Live Super → Dev send | `44ead138-98b9-4c97-8299-1a55d7552205` | **PASS** — request seq 5 |
| Live Dev → Super response + verify | `1bdcc1f2-5b49-4d35-86cf-b2cc24195fd1` | **PASS** — nonce matched, `state=ready`, seq 6, chain verified |
| Controlled service restart | `9686d958-b20e-4b10-b554-c3ab6d3fab6b` | **PASS** — active, PID changed to 50789, v6 unchanged |
| Post-restart Super → Dev send | `e3aa5e7f-8a02-4836-8080-1517680a7580` | **PASS** — request seq 7 |
| Post-restart Dev → Super response + verify | `888e8db6-dba6-4d0c-bb87-941c43bac0a3` | **PASS** — nonce matched, `state=ready`, seq 8, chain verified |
| Later live health/readback | `bccfa957-f6be-435c-8b0e-4995c57135b4` | **PASS** — enabled/running, PID 50789, zero restarts, source head and v6 SHA unchanged |

The three response threads were:
- `super-dev-canary-20261023-01` with nonce `canary-20261023-01`.
- `super-dev-live-20261023-01` with nonce `live-20261023-01`.
- `super-dev-restart-20261023-01` with nonce `restart-20261023-01`.

Every Dev result included `auto_publish=false`, `paid=false`, `controller_service=active`, `host=dell-linux`, and `state=ready`. The result's `in_reply_to` matched the corresponding Super request ID.

## Deployment inventory

| Item | Location |
|---|---|
| Immutable-intent release checkout (Git worktree) | `/var/lib/generic-linux-automator-exec/matrix-superdev-duplex-release-20261023` |
| User systemd unit | `/var/lib/generic-linux-automator-exec/.config/systemd/user/bhm-superdev-ssh-duplex.service` |
| Listener source | `brain/dev-operator/super_dev_ssh_listener.py` |
| Fixed adapter | `brain/dev-operator/super_dev_ssh_worker_once.py` |
| Mailbox CLI and schema | `brain/dev-operator/super_dev_ssh_duplex.py` |
| Source unit template | `deploy/systemd/user/bhm-superdev-ssh-duplex.service` |
| Tests | `tests/test_super_dev_ssh_duplex.py`, `tests/test_super_dev_ssh_worker_once.py` |

The checkout is pinned by the recorded Git commit at release time; it is **not** configured as an automatic updater. Do not pull new commits into a running release without a new test/canary cycle.

## Reuse / operator runbook

Use the existing owner-authenticated Generic Linux SSH connector and Dell lanes. No direct public SSH access or copied gateway tokens.

**Check status (read-only):**

```bash
systemctl --user show bhm-superdev-ssh-duplex.service \
  -p ActiveState -p SubState -p UnitFileState -p MainPID -p NRestarts
sha256sum /var/lib/generic-linux-automator-exec/matrix-controller/controller.py
```

**Submit a fixed read-only status request via the authenticated development lane:**

```bash
P=/var/lib/generic-linux-automator-exec/matrix-superdev-duplex-release-20261023/brain/dev-operator/super_dev_ssh_duplex.py
python3 -B "$P" send \
  --message-id super-task-example-20261023-01 \
  --thread-id super-dev-example-20261023-01 \
  --sender super --kind task \
  --body-json '{"operation":"controller_status","nonce":"example-20261023-01"}'
```

Choose a fresh unique ID and nonce for each new task. Do not replay a task with an uncertain outcome; inspect the mailbox/SSH receipt first.

**Retrieve and verify via the authenticated operations lane:**

```bash
python3 -B "$P" poll --recipient super --after 0
python3 -B "$P" verify --thread-id super-dev-example-20261023-01
```

Confirm `sender=dev`, `kind=result`, `in_reply_to`, matching nonce, `state=ready`, and `chain_verified=true`. A queued SSH job is not evidence; wait for its terminal receipt.

**Controlled service restart after an approved change:**

```bash
systemctl --user restart bhm-superdev-ssh-duplex.service
systemctl --user show bhm-superdev-ssh-duplex.service -p ActiveState -p MainPID
```

**Rollback only this sidecar (preserves v6 and mailbox data):**

```bash
systemctl --user disable --now bhm-superdev-ssh-duplex.service
systemctl --user show bhm-superdev-ssh-duplex.service -p ActiveState -p UnitFileState
```

Do not delete the SQLite mailbox or release checkout as part of emergency rollback; preserve receipts for audit. To re-enable after review, use `systemctl --user enable --now bhm-superdev-ssh-duplex.service` and repeat the two-way smoke test. Another host must receive a separate host-specific authorization and path/service review; this Dell unit is not drop-in portable.

## Open Source / Reuse / Cost Gate

- **Reused:** existing Supabase v6 authenticated SSH gateway; Dell's Python 3 standard library (including `sqlite3`), OpenSSH, and systemd; existing Matrix controller status adapter.
- **New code:** small bounded mailbox, one-shot read-only worker adapter, three-second listener, user-unit template, regression tests.
- **New paid services/models:** **none**. No API spending was authorized or used by this release flow.
- **Licensing:** no external third-party package was added. Existing platform/component licenses remain governed by their upstream distribution and the repository's project policy; this report does not assert an unverified whole-repository OSI license.
- **Fallback:** disable only the sidecar; continue using the preexisting v6 SSH/Matrix controller unchanged.

## Scope exclusions and remaining gates

1. **No arbitrary code/SSH execution via the mailbox.** Only `controller_status` is implemented and certified. General dynamic Dev Brain intake remains blocked pending a security-reviewed, fixed-authority dispatch contract, independently authenticated/signed requests, path/action policy, and dry-run/rollback certification.
2. **Role identity:** the upstream owner-authenticated v6 gateway is the real ingress boundary. Local `sender` fields and CLI restrictions are not independent cryptographic role proof.
3. **Not tested:** physical Dell reboot, extended network outage/reconciliation, cross-host/Mac participation, full Andaz website browser QA through this mailbox, unattended multi-step development workflow.
4. **Mac QA:** explicitly waived by owner for this release; no Mac changes.
5. **Release scope:** this report and source live on the feature branch only; no merge to `main`, no PR approval implied, no production website publishing, no spending, no root/sudo/permission changes.

## Final disposition

**CERTIFIED LIVE for fixed-function Super Brain ↔ Dev Brain status exchange on Dell.** Persistent listener enabled and running, canary/rollback, live response, restart recovery, and later health checks verified with terminal receipts. **NOT CERTIFIED** as a general-purpose autonomous Dev Brain ingress or full Unified Dev Brain release.
