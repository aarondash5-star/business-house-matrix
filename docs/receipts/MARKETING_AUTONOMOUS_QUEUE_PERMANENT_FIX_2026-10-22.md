# Business House Matrix — Permanent Marketing Queue Worker Fix
**2026-10-22, ~20:45–20:53 IST | Verified on Mac | Main branch canonical units**

## Root cause and actual autonomy finding

The research-engine API and signed Dell relay were already healthy. At first, a real `research_market` test was queued with `attempts=0`, while the only visible systemd Marketing service was a passive thermal/health soak. Further investigation found an **existing cron dispatcher**:

`*/2 * * * * flock -n /opt/business-house-matrix/marketing/brain/worker.lock timeout -k 5s 100s /bin/sh /opt/business-house-matrix/marketing/brain/worker.sh # BHM_MAC_BRAIN_PHASE1`

This cron dispatcher **did pick up and complete** the original test, job `42f2178a-8a17-4055-a686-3f4774d2c3f0`, once at **2026-10-22T15:14:13Z**. Therefore the system was *not completely lacking a worker*. The permanent reliability defect was slow cron cadence, opaque lifecycle/health and a 100-second maximum runtime. The existing `worker.sh` properly invokes `brain.py recover` followed by `brain.py work-once`; retain that functioning logic.

## Deployed permanent fix

- Installed **user-level systemd** `bhm-marketing-queue-worker.service` and `bhm-marketing-queue-worker.timer` on `mac-linux`.
- Canonical sources, retained directly on `main`:
  - [service](../../marketing/systemd/bhm-marketing-queue-worker.service)
  - [timer](../../marketing/systemd/bhm-marketing-queue-worker.timer)
- Timer is **enabled and active**, starts 15 seconds after activation and launches again **40 seconds after prior worker completion**. This avoids overlapping long jobs and shortens idle-to-work latency relative to cron.
- Service invokes the original worker script with **the existing single-instance `flock`**, a bounded 160-second task timeout and 170-second service startup timeout. `MemoryMax=640M`, `TasksMax=64`, `NoNewPrivileges=true`, private temporary directory, owner-only umask and journal receipts.
- The Mac's `generic-auto-exec` user has **`Linger=yes`** and is active, meaning its systemd user manager is configured to be started without an interactive login. A full host reboot has **not** been performed; reboot persistence is configured but must be separately cold-boot validated.
- Backed up the complete prior crontab to `$HOME/.local/state/bhm-marketing-backups/crontab.before-systemd-worker-20261022` (mode 0600) and removed **only** the line tagged `BHM_MAC_BRAIN_PHASE1` after successful systemd first-run certification. **Google Trends cron** `BHM_TRENDS_RSS_IN` remains unchanged.
- Existing read-only Search Console, signed research relay, self-hosted SearXNG, Dell loopback Research API and offline model policy were not reconfigured. No publishing or spend permissions granted; `brain.py status` still reports `publish_enabled=false`, `spend_enabled=false`.

## Live receipts and verification

| Stage | Verified outcome |
|---|---|
| Mac user service startup | `Linger=yes`; timer **enabled**, **active**, with next wake visible |
| First no-work poll | Worker `Result=success`, `ExecMainStatus=0`, at **20:49:12 IST**, timer scheduled another trigger |
| Deconfliction | Old two-minute cron worker removed; Google Trends cron preserved |
| Real unattended Moksha task | ID `b93df5b0-549f-4eda-af64-a65a4ec4c2c5`: moved queued → running automatically by timer → **completed** on first attempt, no error, **20:50:55 IST**; service exit **0** |
| Timer restart | `systemctl --user restart bhm-marketing-queue-worker.timer` succeeded; still **enabled**, **active** |
| Duplicate-safe enqueue | Two calls with identical idempotency key `bhm-permanent-autonomy-duplicate-safe-20261022` returned the **same** job ID `b04191d5-7635-4f2f-b77c-5d8ca1c63511` |
| Auto execution after restart | The single `ping` job completed **20:52:20 IST**, first attempt, zero error, worker service `Result=success`, exit code **0** |
| Final queue state | **27 completed; zero queued/running** after the restart test |

The earlier signed research run produced five evidence records and three unverified provider leads; the new scheduler proves *self-execution* rather than independent business judgment. End-to-end factual verification, monitoring-target approval and evidence-quality/Design thresholds remain separate open gates in [Issue #5](https://github.com/aarondash5-star/business-house-matrix/issues/5).

## Diagnostics

```bash
systemctl --user is-enabled bhm-marketing-queue-worker.timer
systemctl --user is-active bhm-marketing-queue-worker.timer
systemctl --user list-timers --all --no-pager | grep bhm-marketing-queue-worker
systemctl --user status bhm-marketing-queue-worker.service --no-pager
journalctl --user -u bhm-marketing-queue-worker.service -n 40 --no-pager
cd /opt/business-house-matrix/marketing/brain && python3 brain.py status --verbose
```

The upstream APIs may still be CAPTCHA-blocked or offline; these conditions remain bounded and are not silently bypassed. The worker's pre-existing `recover` step detects jobs abandoned for five minutes and uses the queue's pre-existing exponential retry/attempt cap. **Timeout fault recovery and full machine cold-boot have not been fault-injected**; avoid claiming 100% no-outage certification.

## Rollback: one scheduler only

1. `systemctl --user disable --now bhm-marketing-queue-worker.timer` and wait for any running worker service to finish; do not disable the SSH bridge or Dell research API.
2. Review `$HOME/.local/state/bhm-marketing-backups/crontab.before-systemd-worker-20261022`. If restoring the original cron scheduler, compare against today's crontab and restore only the line tagged `BHM_MAC_BRAIN_PHASE1`; never overwrite unrelated current cron entries (especially Trends).
3. Check `crontab -l`, `brain.py status`, and `systemctl --user list-timers` to ensure one worker scheduler. No root needed.

## Scope

This is a **permanent scheduling and recovery fix** for the existing Marketing Brain, not permission to access authenticated Opera sessions, publish, spend, execute arbitrary shell or silently certify competitor prices. The source is stored independently in Business House Matrix's main GitHub branch, while [research engine PR #4](https://github.com/aarondash5-star/business-house-matrix/pull/4) remains draft for its unrelated evidence-quality gates.
