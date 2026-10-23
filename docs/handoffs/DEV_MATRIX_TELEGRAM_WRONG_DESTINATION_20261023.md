# Telegram Notification Wrong-Destination Incident — 2026-10-23

**Status: DELIVERY DISABLED; AWAITING EXACT USER-VERIFIED GROUP.**

The user requested Dev Matrix event-driven completion, stalled, failure and escalation messages in a private Telegram group. The operator incorrectly equated the configured Engagement Core destination **Primary** with that private group. Source `Wp_Manager.telegram_status` showed Primary's configured identifier was `-1001827799147`, but this did not establish it was the intended group.

A single explicitly labelled delivery-routing test was sent through the existing authenticated Engagement Core `telegram_publish` using `targets:["primary"]` only, with response `ok=true`, `failed=[]`, Telegram **message_id 1785**. No other destinations were selected. The user immediately identified it as the **wrong group**. Do not repeat or regard this as valid owner delivery. Deletion of the previous Telegram message was not possible using the exposed status/publish-only tools and is not claimed.

**Mitigations implemented immediately:**
- Reverted the notification adapter from `TARGET=primary` to **unconfigured**.
- Removed the hard-coded Primary recipient as an authorized match; added blocked destination keys primary/moksha/andaz/exclusiv and blocked previous numeric Primary group.
- `load_config`, `preflight` and `allow_target` now all fail with `DESTINATION_NOT_VERIFIED_BY_OWNER` before any Telegram network calls.
- Independent Dell fail-closed regression suite **8/8 passed**, terminal SSH task receipt `3ba186a2-5a66-4a65-8014-fc55f5de93d7`. Prior first-run failed the no-network assertion, corrected with preflight guard; current commit `5146986e143b2dc6afe3ba3cd0e5b86d641f8132` passed all.
- Existing hourly Andaz automation had already been disabled; no automatic Telegram sender unit/service was activated. There is no user-verified outbound webhook or machine key configured on Dell. Outbox remains local and durable; no new events are routed externally.

**Gate to resume:** User must specify correct private Telegram group identity, ensure Engagement Core bot has permission there, enroll a dedicated destination key after verifying its numeric chat_id; prohibit selecting the unrelated existing groups. Perform dry-run with exact target yielding **one intended destination**, then obtain explicit authorization for one test send, verify returned message ID and recipient. Never send all groups or change existing destination definitions.

The previous wrong message may be deleted manually by a Telegram group administrator if desired. No code or production WordPress changes were made. Certified v6 unchanged.
