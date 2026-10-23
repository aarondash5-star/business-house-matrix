# Moksha Paid-Booking Telegram Private-Alert Route — Read-Only Verification (2026-10-23)

**Result: SOURCE VERIFIED, HISTORICAL DELIVERY KNOWN, NEW TEST NOT SENT.**
Do not confuse this route with the four-destination Engagement Core community Telegram publisher; specifically, Primary (`-1001827799147`) is the wrong destination for private Dev Matrix notifications.

## Live evidence, WordPress WP Manager only
- WP Manager `get_content(post_id=13126)`: post type `wpcode`, status `publish`, title `Moksha private paid booking Telegram alerts — administrator paired`.
- The snippet defines `GREC_Booking_Telegram::private_chat()` by reading option `grec_booking_private_telegram_chat` and requires a positive numeric private-user ID. The recipient is deliberately **not returned** by the read-only management connector; no guest/owner Telegram ID or bot token copied into GitHub.
- `GREC_Booking_Telegram::send_dm($chat,$html)` reuses existing `GREC_Telegram::credentials()` and WordPress `wp_remote_post` to Telegram Bot API `sendMessage` with `parse_mode=HTML`, checks Telegram `ok=true`, then returns Telegram message_id. The snippet's `verify` private-chat pairing action enforces chat type `private`, sender==chat, and randomized proof.
- Production events: `woocommerce_payment_complete` and `woocommerce_order_status_changed` for processing/completed; `paid()` requires actual paid WooCommerce order, nonempty `_moksha_visit_date`, not previously sent, and obtains a 120-second lock. On delivery, writes `_grec_booking_telegram_sent_at` and `_grec_booking_telegram_message_id`. Failure schedules up to 3 retries using Action Scheduler, otherwise WP Cron.
- WP Manager `list_cron`: `action_scheduler_run_queue` exists with 60-second interval.
- Paired WPCode admin UI is under WooCommerce > Booking Telegram. Its actions are pairing start/verify/disconnect and `recover` for an **eligible existing missed paid order**, which must not be used as a fake test or to replay a real booking.
- WP Manager `telegram_status` lists enabled `primary`, `moksha`, `andaz`, `exclusiv` community destinations; **none is the paired booking-private recipient**.
- WP Manager `telegram_publish(dry_run=true,targets=["grec_booking_private_telegram_chat"])` returned `enabled_count=0`: the standard publisher cannot send through that private DM path. A live `telegram_publish` with no filter would broadcast to all groups and is forbidden.
- WP Manager `get_order(13120)` showed `processing`, but the read-only response suppresses paid-status internal metadata; do not assume current checkout testing or a new send from that limited response.

## Why a new test was not sent
The existing WPCode snippet has no authorized, standalone admin action or REST ability to send a **synthetic test message** to the paired private DM. Current connected WP Manager methods cannot invoke its private `send_dm` method and do not expose an authenticated arbitrary WordPress REST method. Altering WooCommerce order status, payment records, or resurrecting a notification is inappropriate. No production snippet changes, guest-data access, duplicate booking alerts, community messages or Telegram test sends occurred during this verification.

## Minimal safe change for a future test
Add a dedicated `GREC_Booking_Telegram::test()` through a controlled reviewed WPCode change (or native Engagement Core capability), with:
- Exact same `private_chat()` and `send_dm()` methods; **no fallbacks or group destinations**.
- Admin/manage_options permission plus nonce (or WP Control scoped owner identity), fixed static message `Business House Matrix TEST: private notification channel; no payment, booking or guest data involved.`
- Rate limit and unique test receipt, no payment hooks, no order metadata changes and no token or chat ID in response.
- A callable protected `WP Control` MCP action with single-recipient confirmation and message ID; independent QA and rollback of any code changes.
- Deploy/test only under an approved nonproduction or carefully reviewed production edit, with no suspension of existing paid booking alerts.

**Do not route Dev Matrix notifications to Primary or other community groups.** Event outbox remains fail-closed until exact destination and authorized callable route are independently verified.
