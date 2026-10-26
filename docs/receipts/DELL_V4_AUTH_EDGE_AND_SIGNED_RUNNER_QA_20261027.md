# Dell V4 authentication + rollback build verification — 27 October 2026

## Verified changes

**Supabase:**
- Live Edge Function: `matrix-v4-owner-approval`, v1, `ACTIVE`, `verify_jwt=true`. Source readback matches `supabase/functions/matrix-v4-owner-approval/index.ts` byte-for-byte. No arbitrary signer endpoint; defaults to `DISABLED` because owner UID/email, independent reviewed commit, verified mail template/callback, original DEV_BETA PEM and enable flags are not enrolled.
- Migrations `matrix_v4_owner_challenges_20261027` and `matrix_v4_owner_pending_unique_20261027` completed on existing Supabase project `saczglesalubroyaucqe`. Verified `RLS=true`, `FORCE RLS=true`, anonymous SELECT false, authenticated INSERT false, zero challenge rows and one-pending-owner constraint.
- Backend supports a newly authenticated owner code or new link session under a single pending challenge, five-minute TTL, nonce + SHA-pinned release, atomic compare/update, disabled-by-default scoped Ed25519 release signer using existing DEV_BETA PKCS8 env and an independently enrolled public key. It **does not currently send email or sign a release**, and live OTP/template, redirect and sign/verify tests cannot be claimed before enrollment.
- Master Stack authorized event inbox accepted **event #170**, `review_status=pending_review`. This records *disabled platform integration only*, not live Dell release.

**Source-only signing verification and host recovery:**
- `brain/dev-toolyard/governance-v4/v4_rebased_release_verify.py`: raw Ed25519 signature verification, root-owned Dell PEM trust, source SHA-pinned original and 21-binding V4 candidate, single Dell project, five-minute expiry, immutable reviewed Git commit required. Cryptography v41.0.7 was read-only verified on Dell; no real owner key was imported to Dell.
- `v4_fixed_host_rollback_rehearsal.py`: true temporary-filesystem four-file replacement, original-three-file backup and verified restoration on faults 0–4; **explicitly rejects Dell protected controller path**. It is not the service restart/activator.
- `.github/workflows/matrix-v4-auth-check.yml`: TypeScript compile/typecheck of Supabase Auth function.
- Initial Python test runs failed due broad exception wrapping and harness typo and were fixed without weakening scope; no failed logs removed.
- **Final GitHub PR #37 CI:** at commit `13b90434f2f9ac2ef9764bbe01064f73ea142d67`, workflows `40398534421` (Python/repo safety) and `40398534741` (Deno typecheck) both **completed success**. Python result **267 passed, 63 skipped, 50 subtests passed**. Subsequent changes to docs alone may trigger a further CI run, but do not change these tested source artifacts.
- Independent reviewer `karanzing1992` requested for draft PR #37. PRs #33/#34/#35/#36 remain nested dependencies; all source reviews must complete before merge.

**Final live Dell audit:**
- Control-lane job `a8a50cce-483a-4fd0-bca5-698ff24577b7` terminal `completed`, exit 0; `bhm-autonomy-controller.service` active; version `0.2.4-manager-governance-v3`; auto-promotion False.
- Controller SHA `e6834bb2f7765ee0aa26d215a566f70276e4f8c2c87c8730fc781c27dc778836`; adapter SHA `adad20add5e247c515c48d8e2d0c61f2b91e2238d489ed8b4c2e674c845d1abe`; guard V1.3 SHA `7a989c6b484a13a4fdf349d698a6a1bf9e8d9b1afa9684508606bc08c036283e`; 20-binding ledger SHA `9c084832984c1471a22079cc606daccd0a49b78c942ddfee0800a800176c43a9`.
- No root-owned `/etc/matrix-internal-release/dev_beta_owner_public.pem`, no release approval JSON or detached signature installed. The protected controller, runtime and sudo/SSH configuration were **not changed**.

## Remaining exact steps

1. Server-authenticate the selected existing owner email and Supabase Auth owner UUID without writing personally identifying information to Git.
2. Audit shared Auth template supports both `{{ .Token }}` and `{{ .ConfirmationURL }}`; certify one owner inbox, HTML mobile web callback, redirect allowlist, deliverability. An ordinary Supabase magic link may be pre-fetched; require explicit confirmation in the UI.
3. Independently attest actual DEV_BETA public PEM/fingerprint and private PKCS8 keypair, without ever exporting private key. Do not pin blurry screenshot or Pine Beta key.
4. Independent GitHub review and signed commit freeze, and root-side enrollment of matching public PEM with owner-native authenticated terminal. No new sudoers or root policy modifications.
5. Certify an actual fixed-purpose, owner-signed Dell activation + rollback runner with queue lease, on-host backup, correct systemd user bus, active service restart and one-task canary, not just temporary rehearsal; then one controlled deployment and full readback.
6. Verify first real email OTP/link approval path against server-side owner identity, challenge atomic replay denial and signer signature compatible with Python verifier.
7. Merge only approved source and route genuine verified Dell platform release via authorized Supabase Master event inbox; do not confuse event #170 with activation.

**Release disposition: `BACKEND_DEPLOYED_DISABLED / 267_TESTS_PASS / ON_DISK_TEMP_ROLLBACK_PASS / NO_OWNER_SIGNING_ENROLLMENT / NO_LIVE_ACTIVATOR / DELL_V3_ACTIVE`.**
