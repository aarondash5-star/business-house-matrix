# Marketing AI Gate 1 — FINAL CERTIFICATION: PASS

**Independent Business House AI Matrix | 2026-10-21 23:38 IST (18:08 UTC).**  
**Gate:** durable, authenticated Mac Marketing Brain → Dell self-hosted SearXNG research path with citations, safe retries, persistence, no Internet-facing search listener.

## Certification verdict

**GATE 1 PASS** based on fresh live receipts, not only on architecture or synthetic tests. Original Mac and Dell Wi-Fi networks remain isolated and unchanged; the approved permanent signed/outbound HTTPS relay replaces the unusable direct-LAN path.

### 1. Live identities and hardened transport

- Both existing Generic Linux SSH workers online, identity/host probes previously verified. Final heartbeat: 2026-10-21 18:08:24Z, Mac last_seen age 2 sec, Dell age 5 sec.
- Device public signing fingerprints unchanged: Mac `a14b45012cbc7d39b52b6a68`, Dell `fb011d3c5f91d65b50c7184c`. Locally held signing and encryption keys not exported.
- Signed Ed25519 requests, per-request replay-nonce/time verification, encrypted Curve25519 sealed boxes, Dell reply signature verified by Mac; browser human PIN *not* reused or needed for device-to-device transport.
- Existing Supabase bridge infrastructure reused with dedicated `bhm_research_*` objects and `bhm-research-relay` v2; no transfer of customer/booking/account/Moksha Master datasets.
- Dell `bhm-research-relay.service` enabled/active, nonroot rootless research-only worker; pinned local SearXNG and no general shell or publishing tools.
- SearXNG listener **`127.0.0.1:18889` only**; the previous unauthenticated IP-only LAN gateway `18888` remains closed.

### 2. Approved activation, backups, and negative tests

- Added auditable, narrowly scoped `router.py activate-research-relay` CLI. Preflight validates trusted Mac and Dell public-key fingerprints, relay health, fixed `self_hosted=true`, source license approval, `paid_fallback_allowed=false`, allowed request cap, and `publish_enabled=false`, `spend_enabled=false`, `local_inference_enabled=false`. Fail closed for mismatched identity or unsafe flags.
- Versioned code: `marketing/mac-brain/router.py` and `marketing/mac-brain/test_research_activation.py`; live Mac router/backups retained. Activation via the **supported CLI** finished with SSH receipt **`2eb2928e-f139-4d31-b668-016bd2f00767`**, terminal completed/exit 0, returned `enabled=true,transport=encrypted_signed_relay_v1`. No unapproved direct policy mutation or permission bypass.
- Mac source and new tests deployed after saving `router.py.pre-paired-activation-20261021`; existing provider policy privately backed up to `provider-policy.json.pre-bhm-research-20261021`.
- **33/33** Mac `unittest discover -p 'test_*.py'` passed after deployment and **again after activation** (final test SSH receipt **`110efbf6-aca3-4773-b6ae-06406895934f`**, completed/exit 0).
- Test suite checks accepted paired activation, idempotent reactivation, snapshot protection, mismatched signing fingerprint rejection, and denial when publishing is allowed. A live PII search `someone@example.com` was rejected locally **before relay** (receipt **`30182faa-bd9a-403e-827b-d41321b64c6b`**, completed/exit 0).
- Remote unsigned poll had previously returned HTTP **401**. Supabase RLS/privileges final readback: two enabled device identities, **zero** ordinary-client table grants and **zero** pending/stale claims.

### 3. Proof: real unattended Marketing Brain workflow

The **existing Mac two-minute cron worker**, not a manually invoked worker, consumed these queued, idempotency-keyed production read-only research jobs.

| Check | Mac Brain UUID | Sealed relay request UUID | Completion (UTC) | Result |
| --- | --- | --- | --- | --- |
| Initial autonomous research | `9979207f-3d99-4e83-a2b8-6c0af505af61` | `a35b6926-d13a-4ce7-b869-ca1caef28770` | 18:04:09Z | **completed**, 1 attempt, 7.585s, 5 attributed HTTPS results |
| Reused link after Dell research service restart | `0d65e36d-a6f7-45ef-8358-490ef0be29a4` | `9d2557c8-3cb0-4d52-af42-52259f3dc7ce` | 18:06:12Z | **completed**, 1 attempt, 11.339s, 5 attributed HTTPS results |

Each identical repeated enqueue returned the **same** job UUID, not a duplicate. Mac provider accounting advanced from **0 to 2** requests, local daily cap **100**, no paid fallback. Brain queue advanced from **11 to 13 completed jobs**; no stuck marketing research tasks. Second terminal receipt readback via Generic SSH: **`22278582-9f62-4b4b-b921-2ace9d953169`**, completed/exit 0.

The results returned `provider=searxng`, `mode=self_hosted_encrypted_paired_relay`, `citations_required=true`, `untrusted_external_content=true`, `paid_fallback=false`, `publish_approval=false`, and `device_peer_verified=true`. A source snippet is discoverable evidence, **not independently verified fact or rights clearance**.

### 4. Restart and live outage recovery

1. Controlled restart of **only** Dell's dedicated `bhm-research-relay.service`, not Wi-Fi, generic SSH worker, SearXNG container or router. SSH task **`c6ccca9b-c60b-4661-8171-5f83a65dc1a3`** terminal completed/exit 0, service active and enabled after restart; device fingerprint persisted.
2. The *second Marketing Brain job above* was submitted after that restart and autonomously completed by cron.
3. A bounded outage interrupted **only** `bhm-research-relay.service` for approximately 24 seconds (Dell SSH receipt **`a688d41c-778d-4a86-a801-17baa2868e65`** completed/exit 0). Script's exit trap restored and verified service active/enabled, no root/SSID changes.
4. Mac originated a search **while the research worker was down**, then received verified Dell results after worker recovery, without a fresh enrollment: sealed relay request **`3ea74e16-7349-4cbb-97d3-31587c41eac7`**; Mac SSH receipt **`369df008-be31-47e0-b7f6-f54b0563c5d0`** terminal completed/exit 0, 5 attributed results.
5. Supabase final administrative status: **2 paired devices**, **5 completed encrypted jobs total** (including earlier direct tests), **0 queued/claimed**, **0 expired stale claims**, **0 unsafe client grants**. Both workers heartbeat online.

### 5. Boundaries and remaining unrelated gates

**Gate 1 PASS** means a functioning, credential-persistent, authenticated private research channel with live autonomous Brain job receipts, tested after restart and through a transient offline interval. The channel reuses working services; it does not imply unrestricted worker control.

**Still NOT certified:** Gate 2 thermal-safe Mac video rendering, Gate 3 single unattended research-to-finished-video/QA, and Gate 4 extended 24-hour/reboot/general-fault soak. Do not mistake this bounded restart/24-second outage for sustained resilience across all components.

**Unchanged:** no publish or advertising spend, no local Mac heavy inference, no new SearXNG listener, no root/SSH/router/Wi-Fi privilege changes, no new model vendor, no Moksha Master data sync, no browser PIN copied, no raw device keys/host secrets committed. Sources, source attribution and data privacy remain subject to independent review.

**Reference:** [Permanent research transport](../../research/paired-relay/README.md) and [initial gate checks](MARKETING_AI_RELEASE_GATES_2026-10-21.md).
