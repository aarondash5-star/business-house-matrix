# PRIVATE TELEGRAM NOTIFICATIONS — Handover and Multi-Project Reuse

**Date:** 2026-10-23 · **Status:** local sender and receiving code implemented; protected remote WordPress activation **PENDING**; **NO LIVE AUTONOMOUS NOTIFICATIONS SENT** from Dev Matrix yet.

## 1. Verified existing recipient and bot route
Live Moksha WPCode #13126 is active and paired to a private numeric Telegram chat via option `grec_booking_private_telegram_chat`. It obtains bot token through encrypted `GREC_Telegram::credentials()`. Independent synthetic private test via one-time active WPCode #13355 was delivered 2026-10-23 13:42:26 IST, private Telegram **message_id 11**, with the user acknowledging receipt. No customer orders/guest details were created or modified. The earlier `Primary` community group test (message_id 1785) was the **wrong recipient** and is blocklisted.

## 2. Reusable implementation and scope
| Layer | Verified artifact |
| --- | --- |
| Shared Engagement Core WordPress bridge | [integrations/private-notifications/bhm-telegram-relay.php](https://github.com/karanzing1992/engagement-core/blob/main/integrations/private-notifications/bhm-telegram-relay.php) |
| Shared canonical reuse instructions | [PRIVATE_TELEGRAM_TASK_NOTIFICATIONS.md](https://github.com/karanzing1992/engagement-core/blob/main/docs/PRIVATE_TELEGRAM_TASK_NOTIFICATIONS.md) |
| Dell/Mac-local event outbox | `brain/automation/task_events.py` |
| Event-to-receipt bridge | `brain/automation/receipt_bridge.py` |
| Signed delivery client | `brain/automation/private_telegram_sender.py` |
| Dispatch and stall monitoring units | `deploy/systemd/user/bhm-private-telegram-dispatch.*`, `bhm-task-watchdog.*` |
| Independent unit tests | `tests/test_private_telegram_sender.py` + `tests/test_task_events.py` |

Architecture: a local worker posts an evidence-backed terminal/stall event to SQLite; Ed25519 sender signs body and fixed endpoint request; live WordPress verifies the public key, timestamp, event ID and schema; WordPress selects **only** the previously paired private paid-booking chat via the pre-existing option; existing Engagement Core bot sends Telegram and returns confirmed message ID. Caller cannot specify chat ID, audience, payment amount, guest data or arbitrary executable action. Live booking snippet #13126 is unchanged.

Initial Dell signer public SHA-256 fingerprint: `98f4720c9120314af70584aa8320c2b8d4a83c01fbf11bb6a6183d08930c1d59`. Private signer PEM is stored ONLY on Dell at `~/.local/state/business-house-matrix/private_telegram_ed25519.pem`, owner file mode 0600; never add it to Git. Other independent workers must enroll new public keys after review rather than copying Dell's secret.

Supported kinds: `completed`, `failed`, `blocked`, `stalled`, `resumed`, `approval_required`, `escalation`. Task/run IDs provide namespaces for each project; no periodic notification when nothing happened. SQLite statuses: 0=pending, 1=receipt-confirmed, 2=attempt-uncertain/no auto retry. WP also reserves unique event IDs before network sends; duplicate and timeout cannot silently spam.

## 3. Actual tests and receipts
- Dell unit test `tests/test_private_telegram_sender.py`: **13/13 PASS**. Verified signature validity/tamper rejection, private fixed endpoint, no outbound until activated, success receipt, idempotency, wrong-recipient reject, timeout ambiguity, protected key, accepted event kinds. Terminal receipt `5f637e31-2c0b-410f-b853-d1ebe916b239`.
- Existing outbox suite `tests/test_task_events.py`: **15/15 PASS** with same terminal receipt (combined **28/28 PASS**).
- Systemd templates syntax verified by `systemd-analyze verify` (exit 0), receipt `6fd6e123-4fc1-4bfa-ba36-4f7b74b7b313`. Sender reports `{"queued":0,"runtime_enabled":false,"sent":0,"uncertain":0}`.
- Four systemd user-unit templates initially copied on Dell; confirmed `ActiveState=inactive` and `UnitFileState=disabled`, receipt `f60b0e37-11fd-4193-9b7a-121df026668a`. A subsequent source hardening adds `ReadWritePaths` restricted to the SQLite state directory; must re-sync staged templates before activation.
- Standalone paid-booking synthetic Telegram route passed earlier (message 11); this is **NOT** an end-to-end test of new Dev Matrix-to-WordPress signed delivery.

## 4. WordPress live-connection gate
Prepared WPVibe `code_snippet_create` operation `op_b1a754351f774fad`:
[Open administrator approval](https://mcp.wpvibe.ai/approve/op_b1a754351f774fad?t=kAOW__4tthFGPzu0R5pAxHfXNMqADt3rrGvmX0U1kAQ)

**At last check this was pending.** It requires explicit owner approval; WPVibe then saves the snippet **OFF**. Only the owner can enable it in WPCode. Do not assume code published on GitHub deploys to WordPress. Until enablement, no signed Dev Matrix notification endpoint is available.

After enablement: inspect WPCode active/fatal-error state and WordPress REST index for `/bhm-private-events/v1/notify`. Send only **one new signed synthetic event** from Dell (unique event ID) and reconcile `message_id` with the same private DM. Only then place `BHM_PRIVATE_TELEGRAM_ENABLE=1` in the owner-private systemd `EnvironmentFile`, sync hardened service templates, and enable path/timer. No broadcast to community destinations and no untrusted AI-prompt control of message destination.

## 5. Reusable CLI (after certification)
```sh
python3 -B brain/automation/task_events.py register --run-id dev-matrix:andaz-101 --task-id andaz-website --stage build --idle-seconds 3600
python3 -B brain/automation/task_events.py heartbeat --run-id dev-matrix:andaz-101 --stage qa
python3 -B brain/automation/task_events.py approval_required --run-id dev-matrix:andaz-101 --stage final-qa --detail "QA evidence ready for owner review" --evidence-url https://github.com/karanzing1992/andaz-vibe-stay/pull/2
python3 -B brain/automation/private_telegram_sender.py status
```
Use the established shared outbox for Marketing Matrix, Pine Engineer, Andaz and other separately approved projects; existing signing key belongs only to Dell, and each execution worker's identity/permissions remain enforced independently. A non-Dell runner needs its own key and reviewed server-side public-key enrollment.

## 6. Outstanding
- Approval + enable new relay WPCode snippet; PHP WordPress runtime lint/fatal check; fixed endpoint registration verification.
- Genuine Dell→WordPress→Telegram signed canary; check private target and message receipt. Do not replace the working original paid-booking notification snippet.
- Re-sync/hardened service units and enable automatic path/timer ONLY after canary.
- Wire actual Dev Matrix job runtime and per-project heartbeat emission, not just mocked or reference jobs. Verify independent worker identity and real source/QA receipts before alerts.

**Release verdict:** secure reusable source and Dell local unit/simulation gates PASS. **Live automatic notification integration remains BLOCKED ON OWNER WP APPROVAL/ACTIVATION AND END-TO-END CANARY.** No direct injection into this ChatGPT conversation is provided; Telegram alerts the user only.
