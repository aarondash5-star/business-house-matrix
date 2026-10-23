# Verified private Telegram route — Dev Matrix event delivery handover

**Date:** 2026-10-23 (Asia/Kolkata). **State:** VERIFIED private test, **production Dev Matrix event relay NOT YET ACTIVATED**.

## Exact verified route

The Moksha WordPress site `https://mokshagoa.com` has:
- Existing **active** WPCode snippet **#13126**, `Moksha private paid booking Telegram alerts — administrator paired`.
- `GREC_Booking_Telegram::private_chat()`: reads `grec_booking_private_telegram_chat`, checks positive numeric private chat ID, does **not** use Engagement Core community destinations.
- `GREC_Telegram::credentials()` supplies the existing encrypted bot credentials. Delivery goes via the official Telegram Bot API and returns a Telegram message ID on acknowledgement.
- Admin-only **active** one-time test WPCode snippet **#13355**, `BHM one-time private Moksha Telegram route test (admin only)`. It sends a synthetic text (no booking/payment/customer data) to the existing paired private recipient, saves an attempted marker before sending to suppress duplicate attempts, and records the exact receipt.

## Actual live test receipt

Authenticated WPVibe WP-CLI read-only source (not an inferred receipt):
- `option get bhm_private_tg_test_attempted_20261023`: **2026-10-23T08:12:25+00:00**.
- `option get bhm_private_tg_test_receipt_20261023 --format=json`: **`{"status":"delivered","message_id":11,"sent_at":"2026-10-23 13:42:26"}`**.
- The user confirmed the message was received.
- Existing community `Primary` destination **is the wrong recipient**. Earlier test `message_id=1785` was mistakenly sent there; it must remain blocklisted for Dev Matrix notifications.
- The public `Wp_Manager.telegram_publish` tool selects among community destinations and **cannot** target the paired private-booking route; `targets=["grec_booking_private_telegram_chat"]` dry run returned `enabled_count=0`. This is expected, not a reason to broadcast.

## Safe connection contract for Dev Matrix completion / escalations

Event outbox is implemented in `brain/automation/task_events.py` and `brain/automation/receipt_bridge.py`: `completed`, `failed`, `blocked`, `approval_required`, `stalled`, `escalation`, `resumed`. SQLite deduplicates and persists receipts; it does not authorize execution.

Next integration must use **only the already verified paired private recipient** via an authenticated WordPress **fixed-function** event relay:
1. Expose a narrowly scoped event-only REST action under a *new reviewed* snippet/plugin with a dedicated identity credential and timestamp/event-id replay protection. Never expose `chat_id`, bot credentials or generic Telegram recipient parameters to callers.
2. Validate an allowlisted event type, short sanitized summary, approved evidence link, timestamp and unique event ID. Reject guest PII, webhook secrets, commands, arbitrary HTML and bulk/group sends.
3. Use the existing encrypted `GREC_Telegram::credentials()` and private chat option `grec_booking_private_telegram_chat` (same verified recipient as snippet #13126); never modify #13126, payment events or WooCommerce orders.
4. Send only once; maintain an idempotency receipt and stop on unknown/timeout rather than silently re-sending. Check returned recipient identity and Telegram message ID, and report delivery separately from task completion.
5. Provision dedicated secret in owner-controlled credential storage; never commit to GitHub, forward to chat or reuse a broad publisher credential.
6. End-to-end private test requires separate owner-reviewed activation of the fixed-function event relay, independently verified test and rollback. Certified v6 execution permissions remain unchanged.

**Do not send periodic reminders. Do not claim that a Telegram message can automatically create a new ChatGPT reply.** It can notify the owner privately. The prior hourly automation is disabled. No live event relay worker is connected or activated as of this verification.

## Decision

**Private delivery transport: VERIFIED. Automatic Dev Matrix terminal-event delivery: NOT YET WIRED.** The source of truth for the target is the paired WordPress private-chat option; no numeric ID may be invented, hard-coded from a group or published.
