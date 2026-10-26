# Dell V4 — exact DEV_BETA public key comparison and independent trust cutover

Date: 27 October 2026 IST  
Classification: **OWNER PUBLIC CANDIDATE VERIFIED / NONROOT DELL STAGED / LIVE SIGNER MATCH STILL AWAITING NEW OWNER PORTAL PROOF / ROOT TRUST NOT ENROLLED / DELL V3 UNCHANGED**

## Existing verified owner evidence

- User provided exact canonical LF-terminated Ed25519 SPKI public PEM and `SHA256(PEM)=1eee3d266eb1d362b9c7f36d0301b831a8a527828682505ff286d2738606eec1`.
- Independent local parse with Python `cryptography` reports `Ed25519PublicKey`, exact SHA-256 fingerprint and canonical PEM bytes.
- Existing Supabase `matrix-devbeta-public-attest/derive-public` returned **HTTP 200** under verified owner session on 27 October, per server logs, but logs do **not** prove exact bytes of the returned PEM.
- Owner's `ui_acceptable` review is stored separately, with `release_approved=false`, and there are **zero** signed V4 release challenges.
- The fingerprint, without the PEM file, is recorded in `brain/dev-toolyard/governance-v4/v4_rebased_v12_release_manifest.json`; repo safety prevents checking in a `.pem` file and was not bypassed.

## New controlled preparation (no release authority)

1. Owner portal `brain/dev-toolyard/governance-v4/owner_release_portal/confirm/app.js` now uses `crypto.subtle.digest("SHA-256", exact returned UTF-8 PEM)` and requires **both** the independent computed SHA and server-advertised SHA to equal the owner-approved `1eee3d...` fingerprint. Any mismatch hides the returned material and produces `KEY MISMATCH`. It never signs or installs.
2. Updated preview deployed on `https://matrix-owner-key-preview.vercel.app/` as Vercel deployment `dpl_8hnnjLwBshVyPVVtbXGbggjYwweJ`, independently read back `READY`, **Vercel Authentication enforced on all deployments**. It remains an owner-authenticated public-key review UI, not V4 production.
3. Dell Generic SSH **development** task `8442e9c0-c5ca-4a61-bc4c-b9d63d2bac9b` completed exit 0, staging a non-root public-only copy at `$HOME/.matrix-v4-owner-review/candidate-dev-beta-public.pem` with 0700 directory and 0600 file. It validated Ed25519 SPKI, exact fingerprint and readback. The file is **worker-owned candidate only**, not a root trust anchor; no root permissions, services, SSH or controller files were modified.
4. A fixed-purpose owner-native trust installer `brain/dev-toolyard/governance-v4/owner_native_public_trust_enroll.py` is **source only** in draft PR #37. It accepts canonical public PEM via stdin, pins exact SHA-256, restricts installation to `/etc/matrix-internal-release/dev_beta_owner_public.pem`, refuses non-root callers and conflicting existing trust, writes atomically as root, and provides readback. It has no signer, SSH/sudo password collection, service restart or activation operations.
5. Its negative tests are `test_owner_native_public_trust_enroll.py`. Actual root-path execution and on-host restart tests remain **not run**, pending independent review.
6. The reviewed Supabase `matrix-devbeta-public-attest` deployed version 3 remains unchanged. A proposed automatic server-side fingerprint check was not deployed; the new check runs only in the protected owner browser after authentication and independently verifies the public response.

## Required next owner-secure steps

- In https://matrix-owner-key-preview.vercel.app/ complete existing Supabase owner authentication **directly in the protected portal**, then click **Verify DEV_BETA keypair**. Accept only the displayed **`DEV_BETA PUBLIC KEY MATCH`** status. Do not share JWT, email OTP, passwords or key secrets in chat.
- Independent reviewer must approve PR #37's trust installer and exact four-file release candidate. The system administrator must acquire the approved script and public PEM through an **independently controlled root-owned location**; **never execute root scripts directly from the writable Dev Yard staging directory**.
- From Dell's **native authenticated administrator terminal** (not the nonroot Generic SSH worker), validate installer source and owner key fingerprint, then execute the reviewed fixed-purpose trust installer only after the portal match. This step may prompt for the local administrator password in the native terminal. Never place passwords in scripts, logs or ChatGPT.
- Read back root ownership, permissions, path and exact trust PEM SHA. Root trust enrollment is distinct from V4 release signature and cannot approve deployment alone.
- Complete reviewed Git commit freeze, independent five-minute Supabase email OTP/link signing ceremony, verify Ed25519 signature bound to the frozen Dell V4 manifest, certify on-host backup/lease/systemd restart/rollback, and run a single Dell-only canary. No Mac or cross-project release authority inherits these checks.

## Fail-closed outcome

`DRAFT_SOURCE_ONLY / OWNER_BROWSER_PUBLIC_MATCH_PENDING / PRIVATE_DEV_REVIEW_CANDIDATE_STAGED / INDEPENDENT_ROOT_ENROLLMENT_PENDING / RELEASE_GRANT_ABSENT / DELL_V3_ACTIVE`.

Open source / cost gate: existing Python 3, `cryptography` (already present on Dell), WebCrypto SHA-256, GitHub Actions and Vercel hobby static preview. No new paid provider, runtime credential or sudoers modification.

