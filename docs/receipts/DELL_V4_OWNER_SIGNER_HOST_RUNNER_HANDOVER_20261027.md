# Dell V4 owner approval and release implementation handover — 27 Oct 2026

**Status:** Supabase ledger and JWT-gated Edge Function deployed **disabled**; source verifier and host temp-filesystem rollback rehearsal under draft PR #37; Dell V3 unchanged.

## User-approved flow

The owner's agreed interface is **one owner email that contains both a six-digit OTP and a magic link**; the owner uses either, and the first valid use wins. Their account must be a pre-existing verified Supabase Auth owner identity, not an arbitrary email address. The code/link must be entered or clicked in a secure approved HTTPS flow, never pasted into ChatGPT or Generic SSH logs. Admin/sudo password is separate and only entered in a verified native terminal if needed; password entry does not authenticate release signatures.

Supabase documentation confirms the Magic Link/OTP email template can include both `{{ .Token }}` and `{{ .ConfirmationURL }}`. Its template is shared by other users of this Supabase project, and redirect allowlists may affect existing apps: audit before editing. Set up a secure page at the single allowlisted `MATRIX_V4_OWNER_ORIGIN` with a callback at `/owner-release/confirm`, and explicitly require an owner confirmation gesture after link sign-in to prevent mail-prefetch link consumption. The existing preview/demo contains simulated code/link only, not real Supabase sessions.

## Delivered and verified infrastructure

- Supabase project `saczglesalubroyaucqe`: migrations `matrix_v4_owner_challenges_20261027` and `matrix_v4_owner_pending_unique_20261027` succeeded. Table `public.matrix_v4_owner_challenges` is empty on verification; RLS and FORCE RLS enabled, `anon` SELECT denied, `authenticated` INSERT denied, `service_role` UPDATE permitted. One pending owner challenge at a time; five-minute maximum lifespan; no OTP code stored in table.
- Edge Function `matrix-v4-owner-approval` version **1**, **ACTIVE**, `verify_jwt=true`, deployed source byte-for-byte matches `supabase/functions/matrix-v4-owner-approval/index.ts`. **ACTIVITY IS DISABLED** until all owner + template + redirect + signing enrollment settings are true. No owner OTP request or signed release has been made.
- Uses actual Supabase Auth `/auth/v1/otp` (send to server-pinned owner email; no user creation), `/auth/v1/verify` (six-digit code) or fresh signed email-link session (Auth `/user`, time + factor checks); one SQL compare/update on the pending challenge before signing. Exact manifest and request nonce hashes prevent generic approvals. Emits a canonical detached raw Ed25519 signature for one Dell-only five-minute release with SHA-pinned old/current source and new candidate. No unrestricted signing endpoint, host operations or spending capability.
- Edge signer references **`DEV_BETA_ED25519_PRIVATE_PKCS8_B64`** only *inside the owner-controlled Supabase environment*. It requires independent enrolled `MATRIX_V4_OWNER_PUBLIC_PEM` and exact SHA-256 of canonical LF PEM bytes. Signs and then self-verifies via WebCrypto; never exports private key.
- New `v4_rebased_release_verify.py` on Dell source side: raw Ed25519 detached verifier using installed `cryptography` (Dell reported 41.0.7), exact `dell-linux` and `matrix_dev_manager`, four old pins and four V1.4 pins, reviewed exact full commit, <=5-minute UTC, one-time release id/nonce, independent *root-owned* `/etc/matrix-internal-release/dev_beta_owner_public.pem`. The certificate does not imply host activation.
- New `v4_fixed_host_rollback_rehearsal.py`: four-file real **temporary** filesystem swap with private backups and rollback injected at each step; deliberately rejects the real Dell `matrix-controller` path, cannot start systemd or change sudo. This is a preflight QA component, not the live activator.
- CI: GitHub `Matrix source validation` and `Matrix V4 owner approval TypeScript check` workflows; the initial Python test failures (signature error remapping, typo in fault-injection argument, replay ordering) were corrected without bypassing tests. Keep original failure job receipts.

## REQUIRED secure enrollment to make email flow live

No further generic permission prompts: owner has already approved scoped Dell release work. Enrollment still requires independently verifiable **facts**, not repeated approval:
1. The intended existing Supabase Auth owner's verified **user UUID** and verified **email**, configured server-side as `MATRIX_V4_OWNER_UID` and `MATRIX_V4_OWNER_EMAIL`. Do not put the email or UUID in Git.
2. Audit shared Magic Link email template for exact `{{ .Token }}` + `{{ .ConfirmationURL }}`, deliverability/SMTP, project Auth email configuration, existing callback URLs, allowlist `MATRIX_V4_OWNER_ORIGIN`; certify a mobile-first HTTPS callback that receives the new Auth session without exposing tokens to logs, analytics or link prefetch. Then server-set `MATRIX_V4_EMAIL_TEMPLATE_VERIFIED=true` and `MATRIX_V4_OWNER_REDIRECT_VERIFIED=true`.
3. Independent code review and exact commit freeze; set `MATRIX_V4_REVIEWED_COMMIT` to that Git SHA. No arbitrary self-supplied SHA; review must be outside Dev Yard execution identity.
4. Exact **original copied DEV_BETA public PEM** and SHA-256 fingerprint, attested against existing Supabase private PKCS8 key via a harmless sign/verify challenge without exporting key. Never substitute photographed/transcribed Pine Beta public key.
5. Only then turn on `MATRIX_V4_OWNER_APPROVAL_ENABLED=true` and `MATRIX_V4_RELEASE_SIGNER_ENABLED=true` server-side and perform real owner code/link positive, wrong-user, wrong-token, wrong link, replay, expiry, unknown-outcome and SMTP failure tests. The service requires an existing owner JWT to request the *fresh* release OTP; the web session-login path must be independently enrolled.

## REQUIRED host release gate

- Root-enrol the genuine matching public PEM at `/etc/matrix-internal-release/dev_beta_owner_public.pem` by an independently authenticated Dell admin using native terminal, not Dev Yard worker-issued sudo or ChatGPT.
- Freeze the reviewed full commit in an independent release configuration; the Python verifier denies if not enrolled.
- Define and certify fixed-purpose host actual activator with queue lease, original three-file backup and hashes, private stage, owner signature verified, one-time durable journal, staged four-file atomic replacement, systemd restart on correct user bus, hash + service + one-task canary and guaranteed on-host rollback with actual recovery verification. Temp-file replay tests cannot certify this.
- PRs #33/#34/#35/#36/#37 are still separate draft dependencies; no self-approval or blanket merge.
- Mac remains a separate manifest and rollout; DEV_BETA owner identity reuse does not automatically authorize Mac V4 activation.

**Absolute prohibition:** no brute-force SSH, no weakening signature requirements, no copying private key into repository/CLI logs, no public inbound root SSH or sudoers changes, no uncontrolled production publish/spending.

**Final classification:** `SIGNED_RELEASE_BACKEND_DISABLED / PRIVATE_SINGLE_USE_LEDGER_VERIFIED / DEV_BETA_OWNER_ENROLLMENT_PENDING / ROOT_HOST_TRUST_MISSING / REBASED_V14_SOURCE_PINNED / TEMP_ROLLBACK_TESTED / V3_ACTIVE`.
