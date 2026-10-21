# Mac Linux — reversible debloat and thermal baseline (2026-10-21)

**Machine:** `mac-linux` / hostname `KARAN`, Apple Intel HD Graphics 6000, 7.7 GiB RAM, Ubuntu/Linux Mint/Xfce, signed Generic Linux SSH worker. **Execution window:** 23:43–23:49 IST. **Scope:** safe OS-background cleanup before Marketing Gate 2 render; preserve separate Shaadi game worker, host session, fan safeguards, Gate 1 research transport and all security infrastructure.

## Initial live audit

- 7.7 GiB RAM, ~5.5 GiB used / 2.1 GiB available, ~859 MiB compressed zram swap, disk /dev/sda2 at 50% used (53 GiB free).
- CPU `coretemp` initially ~81°C; Apple SMC TC0F ~80°C, later as high as 83.8°C; exhaust fan 6418–6493 RPM out of 6500 maximum. **Mac Gate 2 68°C render preflight is not met**; no rendering, stress testing, fan policy change or temperature override.
- Firefox is the overwhelming memory/CPU consumer; individual content processes measured ~2.0–2.35 GiB RSS and ~1.0–1.26 GiB RSS, with main process ~590 MiB RSS. These belong to `karan`'s active interactive session; **none killed, no browser tab lost**.
- 263 apt `autoremove` candidates mostly Node.js dev libraries. Dry-run ONLY; no packages removed, no mass cache deletion. `.npm` ~402 MiB and executor cache ~156 MiB retained for reproducible/offline developer workflows. 50%-used disk not a bottleneck.
- Important processes to preserve: `generic-linux-automator` inbound loopback ssh/outbound Supabase bridge, `cron` 2-minute marketing worker and Google Trends refresh, `mbpfan`, `thermald`, NetworkManager/Wi-Fi, CUPS, avahi, Ollama models, Firefox session, and separate `actions.runner.KaranZi-shaadi-aunty-dodge.shaadi-KARAN` + `shaadi-mac-bridge`.

## Verified changes and receipts

**Executed as reversible owner-requested background-service cleanup, without altering sudo/root permissions:**

| Service/application | Change | Live verification |
|---|---|---|
| `kerneloops.service` | `sudo systemctl disable --now` | inactive + disabled |
| `switcheroo-control.service` | `sudo systemctl disable --now` | inactive + disabled; GPU hardware inspection found Intel HD 6000 only |
| `fwupd.service` | `sudo systemctl stop` | inactive, still static/activatable; `fwupd-refresh.timer`, APT security-update timers untouched |
| Linux Mint System Reports tray startup | Installed `/home/karan/.config/autostart/mintreport.desktop` with `Hidden=true` for next login; preserved Update Manager | Override exists; no Update Manager change |
| Currently running `mintreport-tray` process | Attempted soft close **did NOT succeed** because `sudo -u karan` requires a password; preserved permission boundary | PID 1683 still present on final check |

**Commands were submitted through authenticated Generic Linux SSH and read to terminal state.** Baseline SSH receipt `556c0bbf-e024-4d03-aeef-6504851d26e9`, audit receipt `1a0dd082-df0f-4897-8397-6bb503e8c70f`, dry-run/dependency receipt `a752a6db-b585-4af8-a8d4-254389c4e3e9`, changes `bad3b4e3-f771-48a5-8d40-0a26f4c1951f` terminal completed/exit 0, postchange `eec3ca73-e76d-414d-938d-2d202fff3aad` completed/exit 0. Attempted tray close `c79f4959-ba56-4b84-aeba-21cc9ebf8dfe` wrapper exited 0, **but stderr confirmed sudo refused**, therefore close action failed.

**Local rollback notes:** `/var/lib/generic-linux-automator-exec/matrix-debloat/rollback.txt` (owner restricted). Restore `sudo systemctl enable --now kerneloops.service switcheroo-control.service`; `sudo systemctl start fwupd.service` if required; and remove only the specific user override if original Linux Mint Reports autostart should return. No host credentials or browser artifacts copied to GitHub.

## Postchange independent QA (23:49 IST)

- `generic-linux-automator.service`, `cron`, `mbpfan`, `thermald`, `ollama`, `cups`, `avahi-daemon`, `NetworkManager`, Shaadi runner: all **active**.
- 33/33 existing Mac Marketing regression tests PASS.
- `router.py validate`: `valid=true,connections=5,paid=false`.
- Paired research relay cryptographic self-test PASS: sealed box, Ed25519 valid signature, tamper rejection and private-query rejection. Gate 1 provider remains enabled/no-paid, counters intact.
- RAM remained ~5.5 GiB used and ~2.1 GiB available; ~854 MiB swap still occupied. **No meaningful measurable RAM or heat improvement should be claimed.** Final Apple SMC sensor TC0F ~83.8°C, exhaust ~6466 RPM; package temperature fluctuated. Gate 2 **NOT thermally ready**.
- Main unresolved load is the user's active Firefox content processes. Recommended next action: **owner-guided tab/process audit** via Firefox's `about:processes` / `about:memory`, voluntarily close unnecessary tabs (especially heavy 2+ GiB process) while preserving unsaved forms and active AI work. Do not indiscriminately kill Firefox or adjust fan speed/cooling guards.

## Golden Rule 0 / boundaries

No new optimization daemon, no apt uninstall or autoremove, no package-manager meddling, no GPU/fan kernel settings, no disabling firmware-update schedule, no password prompt override, no router/SSH/root permission change, no changes to existing Matrix Mac/Dell research handshake, no changes to Marketing publishing/spend flags, and no Moksha Master data sync.

**Verdict:** limited safe debloat COMPLETE, real thermal/performance gains require controlled browser workload reduction and later remeasurement. **Gate 1 remains certified; Gate 2 not certified.**
