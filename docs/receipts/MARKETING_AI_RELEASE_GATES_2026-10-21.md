# Marketing AI MVP — live release-gate evidence (2026-10-21)

**Scope:** Independent Business House AI Matrix. **Evidence window:** 2026-10-21 22:45–22:54 IST (17:15–17:24 UTC).  
**Verdict:** **NOT CERTIFIED**. Never infer a completed cross-host production chain from separately passing unit tests.

## Terminal bridge probes and baseline

| Host | Bridge probe UUID | Result |
| --- | --- | --- |
| Mac `mac-linux`, hostname `KARAN` | `4f14ab78-c8a0-4ac7-bc66-b8829b09fbbd` | `completed`, exit 0, identity `generic-auto-exec` |
| Dell `dell-linux`, hostname `karan-Inspiron-5379` | `db805f5a-b598-4603-8a28-f8e1feb97395` | `completed`, exit 0, identity `generic-auto-exec` |

Host baseline SSH task receipts: Mac `5cf2f709-9b12-414c-902c-96250095b1f5`, Dell `7f2b73ba-a79c-4a9b-84cf-a182f5417e34`; both terminal `completed`/exit 0.

## Gate 1 — private Mac → Dell research: BLOCKED

- Network identities reverified: Mac `Andaz`, 192.168.0.106/24; Dell `andaz`, 192.168.0.103/24, distinct BSSIDs/networks with overlapping subnets. The Mac ARP neighbor was FAILED/INCOMPLETE.
- Mac HTTP health check `192.168.0.103:18888/health` timed out (HTTP 000), SSH task `cb2979bb-c1be-4e11-a464-794bb327f492` terminal completed/exit 0 **for the diagnostic wrapper**, not a successful network request.
- Neither host has an active Tailscale/WireGuard overlay; no approved private alternative found. No IP-only gateway can be trusted when the networks overlap.
- Dell `bhm-searxng.service` enabled/active; engine is rootless and listens only on `127.0.0.1:18889`. `bhm-searxng-gateway.service` inactive. Dell-local SearXNG returned three public source-attributed results.
- Mac `searxng-search.enabled=false`, correctly fail-closed. **No Mac-initiated JSON search or policy activation occurred.**
- Blocker: owner-approved common trusted LAN or authenticated private transport, explicit endpoint identity/authentication and boot/reconnect review, then Mac live `/health` and JSON query.

## Gate 2 — thermal-safe Mac-owned Reel Studio video: BLOCKED

- Mac `reel_bridge.mac_temperature_c()` measured **77°C**, subsequently **75°C**, against existing **68°C** preview cutoff. Fans measured ~4636 RPM at initial inspection; Firefox/isolated web processes remained in use. No processes were killed or fan/thermal rules changed.
- Existing `moksha-originals-20261021` batch preflight succeeded (three privately staged JPEGs, total 228,757 bytes; source includes official-logo.jpg, guest.jpg and sauna.jpg). It is preview-only and not a rights/brand signoff.
- Existing Reel Studio entrypoint and isolated environment were inspected, and Mac `unittest discover` passed **30/30** current regression tests.
- **No hot render attempted**, no MP4 or report.json produced by Mac, no valid autonomous editor output. Previously generated ChatGPT-workspace preview is specifically not counted.
- Blocker: naturally stable sensor readings below 68°C with enough margin for guarded in-run monitoring, without bypassing the guard or terminating unrelated apps without approval.

## Gate 3 — one unattended real-asset video: BLOCKED / NOT RUN

- The existing Mac Brain, Groq and Google Trends, Dell research and original assets are retained; no duplicate production job was submitted.
- Mac-to-Dell research delegation remains unverified and Reel Studio render remains thermally disallowed. An unsupported manual draft or public search alone cannot pass this gate.
- No publication/ad spend occurred. **One linked research → concept → original-asset edit → technical/factual/brand/rights QA → review-only preview job still required.**

## Gate 4 — unattended / recovery certification: BLOCKED (smoke PASS; extended tests NOT RUN)

- Mac 30/30 tests passed, `cron.service` active with the original 2-minute `worker.sh` and 6-hour Trends job intact.
- Two Mac `ping` submissions using the **same** idempotency key `marketing-release-gate4-20261021-2251` returned the **same** Brain job UUID: `881a4f47-646c-4565-a2eb-7bc822a3729c`. Existing cron automatically completed it at **2026-10-21T17:22:01Z**, attempt 1, result `ok: true`. Brain queue advanced from **10** to **11 completed**. Remote SSH receipt for terminal readback: `cdfe692b-48c0-4429-8d27-194392dc34a6` (completed, exit 0).
- Dell controller/sandbox selftests passed; `bhm-autonomy-controller.service` and `bhm-searxng.service` both enabled and active, controller restart policy `on-failure` / 12s, reported `NRestarts=0` at baseline.
- Dell controller received two identical `research_search` submits with key `marketing-release-gate4-20261021-2251` and returned the **same** task UUID `8f39e7eb-4fa7-45fa-a800-19ad7b423716`, second `deduplicated=true`. The existing daemon completed the job on **2026-10-21T17:20:58Z**, attempt 1, `qa_level=retrieval_only`, with five public SearXNG-attributed sources. Remote terminal readback receipt `ed094ee6-61bc-458c-83d1-d5a202bf7481` (completed, exit 0).
- Dell authenticated SSH heartbeat became stale/temporarily offline (age 68s at 17:22:13Z) and was online again at **17:23:45Z** (age 1s) **without operator intervention**. A queued read-only status request was **not resubmitted** and later returned terminal completed/exit 0. This demonstrates a transient bridge recovery, **not** proven fault-tolerant machine-to-machine research or a full soak.
- Journal reads for Dell user service returned insufficient permissions; no permissions were changed.
- Not run: deliberate Wi-Fi outage, SSH kill, router changes, machine reboot, thermal-heavy render, 24h soak, provider exhaustion. They require safer scheduling / appropriate authorization and cannot be asserted as passed.

## Safety and continuation

- Golden Rule 0 followed: no component replacement, duplicate job, secret export, hardware safety bypass, new paid subscription, Wi-Fi/router/SSH/root/sudo/access policy change or Mac local inference.
- `publish_enabled=false`, `spend_enabled=false`, Dell `auto_publish=false`; Moksha source assets remain private and **Moksha Master is untouched**.
- **Next:** (1) owner-approved trusted private transport, verify endpoint identity before enabling Mac SearXNG; (2) address Mac ambient heat/workload without killing user applications without approval, then bounded original-asset render under 68°C; (3) one idempotent linked pilot; (4) planned non-destructive fault/soak certificate with terminal receipts.
- This document is a **redacted evidence index**, not a copy of the live SQLite DB, private media, host passwords or raw internal policy.
