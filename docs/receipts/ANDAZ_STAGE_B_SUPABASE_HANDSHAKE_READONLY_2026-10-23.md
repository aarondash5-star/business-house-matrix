# Business House Matrix — Stage B Supabase handshake read-only verification

**Date:** 23 October 2026 IST.
**Request:** Investigate reusing the existing Supabase handshake for the Mac/Dell research connection rather than shell-based Mac preflight.
**Disposition:** **EXISTING SUPABASE AUTHENTICATED TRANSPORT REGISTRY / STORED RELAY VERIFIED. MAC FIXED-FUNCTION ATTESTATION NOT ACTIVATED.**

## Live source and architecture inspection
- Connected Supabase project `saczglesalubroyaucqe` (`constituency-ops-v1`, ap-south-1, `ACTIVE_HEALTHY`). Used Supabase read-only MCP operations to list functions and inspect existing Edge function source and minimized database health metadata. **No secrets or private signing keys read.**
- Active `generic-linux-automator` Edge Function **deployed version 7**, SHA `467925900f3f08afedb6a691433c81ff98f48796afabe7e2cb18c1a4ed62e30f`. Its code declares runtime/service `1.2.1`; the older project handover's v6 / service v1.2.0 is historical.
- Active `bhm-research-relay` Edge Function **deployed version 2**, SHA `818e984c748cb57d4737afd6e4ba02df03a7ac599f4b86738b6d3c990baebca9`, using signed Mac/Dell Ed25519 identity verification, strict `/submit`, `/poll`, `/finish`, `/status` operations, nonce/replay checks and encrypted payload boxes. This is the existing research transport; no new one needed.
- Live Generic SSH code uses `generic_auto_jobs` and accepts `kind=probe` or `kind=shell`; its existing seven MCP tools do **not** expose a typed `mac_attestation` action. The Mac worker must also implement any new job kind before one can be used.
- Project lists **no Supabase development branches**. Do not create one without checking/authorizing costs. All live functions preserved.

## Read-only registry checks (non-sensitive projection only)
- `public.generic_auto_hosts`: both `mac-linux` and `dell-linux` marked enabled and paired; each worker version `linux-ssh-v1`, existing control/operations/development heartbeats present. Snapshot observed 2026-10-22 ~21:05 UTC.
- `public.bhm_research_devices`: enabled Ed25519 *public-key identity registrations* exist for both hosts. Query returned only `has_enabled_research_identity` boolean; **did not retrieve signing keys, token hashes, IDs, secrets or application data**.
- `public.bhm_research_jobs`: 43 rows in `completed` state, latest `created_at` 2026-10-22 18:46:45 UTC and `completed_at` 18:46:53 UTC. This confirms existing historical relay traffic was recorded; it **does not** attest payload semantic correctness, new Mac preflight compliance or fresh end-to-end attestation.
- Tables `generic_auto_hosts`, `bhm_research_devices` and `bhm_research_jobs` reported `rls_enabled=true`.

## Why a new Supabase endpoint is not automatically clearance
- The previously attempted **Mac fixed-function** `linux_probe` was denied before an MCP invocation reached the connector: `This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.`; Dell's identical fixed probe completed with task `97f5421e-54d6-497f-a51e-1e6bb57b467b`.
- No observable data suggests the existing Supabase gateway itself is broken. The denial happens *upstream* of gateway dispatch. Repackaging the rejected Mac operation through a separate Edge route, SQL, browser, alternate worker, injected job or private tool would circumvent rather than resolve this control, so **none was attempted**.
- Source-only [fixed Mac attestation collector](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/marketing/andaz_stageb_mac_collector.py), [14/14 offline tests](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/marketing/test_andaz_stageb_mac_collector.py), [MCP input schema](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/marketing/schemas/linux_mac_fixed_attestation_v1.json) remain unmerged. They have **not** been installed or run on Mac.

## Approved path for integration once connector owner/security review succeeds
1. Keep Supabase `generic-linux-automator` v7 and `bhm-research-relay` v2 intact; obtain explicit security-owner approval for a **new fixed-shape, read-only Mac attestation MCP action** with `host_id=mac-linux`, nonce and no `command`/`url`/`path` inputs. Explicit platform safety authorization is essential; owner user approval by itself is not enough.
2. Reuse existing authenticated owner/paired worker and independently validated Ed25519 research identity. No service-role token exposure, new SSH key, root or generic device grants. Preserve fail-closed replay/freshness and no changes to existing search envelope.
3. Bind a pending one-time nonce to owner, Mac identity, short expiry and a reviewed static-operation type; the pre-authorized Mac collector returns signed fixed timer/config/hash state. Supabase verifies signature and consumes nonce exactly once, returning a minimal sanitized receipt. No arbitrary commands or private data in the request or result.
4. Test an isolated copy first with synthetic identities, anti-replay/expiry/role/host/unknown-operation negatives and rollback. Do not assume an existing production worker understands a new job kind; release the worker and gateway only through approved versioned rollout.
5. Review robots/terms for only `https://www.happypandahostel.com/` and `https://thepeacehostel.in/`, enroll real reviewer identities and independently approve exact-page grants before any signed extraction. Do not promote source text to verified fact or price automatically.

## Evidence and status summary
| Gate | Result |
|---|---|
| Supabase project ownership/access | READ-ONLY INSPECTION PASS |
| Gateway existing source and versions | VERIFIED, v7 and research relay v2 |
| Both worker registry heartbeats and identities | VERIFIED at observed timestamp |
| Existing relay historical completed jobs | 43, STATE ONLY |
| New live Mac fixed-function attestation | NOT PRESENT |
| Platform safety exception/approval | NOT GRANTED |
| Mac worker write, direct job enqueue, alternate transport | NONE |
| Mac/Dell services, root, permissions, spend, publish, site, merge | UNCHANGED |

**Decision:** Existing handshake infrastructure is usable for a **future approved** typed Mac attestation. Stage B remains fail-closed and blocked until platform and connector authorization, robots/terms, source/reviewer identity and live QA requirements pass.

**References:** [Approval Issue #14](https://github.com/aarondash5-star/business-house-matrix/issues/14), [draft PR #4](https://github.com/aarondash5-star/business-house-matrix/pull/4), and [Mac fixed-function collector receipt](ANDAZ_MAC_FIXED_ATTESTATION_COLLECTOR_2026-10-23.md).
