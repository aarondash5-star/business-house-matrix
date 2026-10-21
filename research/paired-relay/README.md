# Permanent device-paired Mac → Dell SearXNG research transport

**Live checkpoint:** 2026-10-21 ~23:19 IST. **Transport:** LIVE and cryptographically paired. **Normal Mac Marketing Brain job route:** still **OFF** pending supported policy activation and final queue-to-receipt test.

## Why this exists
Mac `Andaz` and Dell `andaz` are distinct Wi-Fi networks with overlapping `192.168.0.0/24` addressing. Existing Dell SearXNG must remain bound to `127.0.0.1:18889`; there is no safe direct LAN route. The existing owner-operated outbound Supabase bridge already has independent persistent worker identity for both machines. Reuse **its outbound relay principle**, not its generic SSH command queue or browser PIN/session authority.

## Components
- `transport.py`: MIT-compatible PyNaCl-based **Ed25519 device signatures**, per-machine long-term pinned signing public keys, **Curve25519 sealed boxes** for encrypted request/results, short-lived signed nonces, SQLite Mac request-id retention, hardcoded HTTPS relay endpoint, Dell fixed local `local_search.py` only. No arbitrary command execution; no stock scraping; no local LLM inference.
- `edge/index.ts`: independent `bhm-research-relay` Supabase Edge Function, deployed **v2** with `verify_jwt=false` only because every non-health operation has application-layer Ed25519 authentication, timestamp/nonce checks, fixed `mac-linux`/ `dell-linux` roles and replay rejection. Public unsigned `POST /poll` smoke returned **401**. HTTP health reveals only service status.
- `migrations/20261021_private_relay_v1.sql`: 3 `public.bhm_research_*` tables, **RLS enabled and deny-by-default for anon/authenticated** plus revoked table privileges; only existing Supabase service role can perform scoped Edge function DB operations. No trigger, open RPC, cross-Moksha sync, API key or privileged host shell.
- Dell user service `bhm-research-relay.service`: `systemctl --user`, enabled and active, nonroot `generic-auto-exec`, memory bounded, `ProtectSystem=strict`, `NoNewPrivileges=yes`, restart on failure. Outbound HTTPS polls; no inbound TCP listener. Existing service-account lingering was already configured.
- Mac runtime code: `/var/lib/generic-linux-automator-exec/matrix-research-transport/transport.py`. Private identities under `identity.json` (0600) and peer public-key pins `peer.json`, service directory (0700). Same on Dell.
- Mac Marketing adapter `marketing/mac-brain/searxng_research.py` **code** now supports opt-in `transport=encrypted_signed_relay_v1` with existing 3/min and 100/day quotas. **Live policy remains disabled** because a direct policy-edit command was rejected by execution controls; do not bypass that restriction. Revalidate via supported/approved policy operation before enabling.

## Security boundary and lifecycle
The browser PIN is a short-lived *human unlock* credential, NOT a machine secret. Devices were enrolled once using their **public** keys; private keys never left local hosts. Each request is authenticated with device-specific Ed25519 signatures; the relay stores only sealed opaque payloads, so it cannot read plaintext query/result. Dell returns a signed receipt within the encrypted response, which Mac verifies against its pinned Dell key.

Messages have bounded query scope, expiry (~175–180 s), UUID identity/deduplication and 60-second anti-replay windows. Worker writes receipt state before confirming. Nonces are probabilistically pruned after 10 minutes to prevent unbounded database growth. Revocation = owner disables the relevant `bhm_research_devices.enabled` record; **never** overwrite pinned keys silently. Recovery from an ambiguous search cannot authorize publishing or spend.

The independent Matrix shares only the owner-operated *infrastructure* of an existing Supabase project. It does **not** share Moksha Master tables, credentials, private documents, booking data, browser cookies or PINs. The bridge is signed/E2E-sealed rather than general-purpose cross-project command routing.

## Exact verified receipts
- Dell public signing fingerprint `fb011d3c5f91d65b50c7184c`; Mac `a14b45012cbc7d39b52b6a68`.
- Two host `init` and `selftest` operations each passed encryption roundtrip, signed-message verification and negative/tamper checks. Host SSH receipts: Mac `74373448-85aa-44ad-a303-cd1a3d90745f`; Dell `3c7982e8-4423-40a3-a08f-3015bfeac04a`; both terminal exit 0.
- Enrolled as 2 enabled device public-key records in Supabase, no private material recorded.
- First **Mac-origin → HTTPS Supabase → Dell localhost SearXNG → signed encrypted Mac response**: job `dc1ede2b-d686-43fe-b236-c04bd66d1b11`, 5 HTTPS attributed sources, terminal Mac SSH receipt `0d247b99-e8f0-4d09-acb6-51c7924ea0bf`, completed/exit 0.
- Controlled restart of ONLY the new Dell user research service: SSH receipt `8e57bd52-6e38-4821-8209-d45cbfd71241` completed/exit 0; service active/enabled, memory ~13.9 MB; SearXNG still localhost-only.
- **After service restart**, second full Mac-to-Dell live search: job `0d929763-667f-44d7-a9c3-955753b2da3d`, 5 attributed HTTPS results, terminal Mac SSH receipt `75e92b90-91b9-454f-8993-8f9f87bd3c24`, completed/exit 0.
- Anonymous/untrusted `POST /poll` returned HTTP **401**. Signed health and peer trust verified.
- Supabase administrative SQL checkpoint: **2** enabled paired devices, **2** completed jobs, **0** pending, **0** ordinary-client grants, **0** public RLS allow policies.

## Remaining release-gate work
1. Normal Marketing `brain.py research_search` must use the **new** `searxng_research.py` opt-in branch, via approved policy editor. Preserve `publish_enabled=false`, `spend_enabled=false`, `local_inference_enabled=false`, other providers unchanged. Tests were **30/30 PASS** after the source update while policy disabled. The unsupported direct policy-write attempt was blocked; no bypass performed.
2. With router policy legitimately enabled, enqueue one idempotent `research_search` Brain task, let the **existing 2-minute Mac cron** consume it, verify terminal receipt/results and quotas.
3. 24-hour unattended/reboot recovery with guaranteed reconciliation still required; a controlled service restart is useful but insufficient for full certification. Monitor ambiguous `claimed` jobs before treating the whole chain as certified. Do not restart Wi-Fi, router, root SSH, or both machines together.

## Read-only operator
```bash
# On either host: private keys stay local
python3 /var/lib/generic-linux-automator-exec/matrix-research-transport/transport.py identity
python3 /var/lib/generic-linux-automator-exec/matrix-research-transport/transport.py selftest
# Dell
systemctl --user is-active bhm-research-relay.service bhm-searxng.service
# Mac: signed direct test without enabling the Marketing Brain route
python3 /var/lib/generic-linux-automator-exec/matrix-research-transport/transport.py search 'public Goa wellness research'
```

No ports 18888/18889 are exposed. **Do not use the browser's PIN as a machine authentication credential.**
