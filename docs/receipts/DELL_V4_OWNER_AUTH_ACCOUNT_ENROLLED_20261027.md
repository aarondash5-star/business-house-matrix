# Dell V4 Owner Account Enrollment — Verified Platform Receipt (2026-10-27 IST)

## Authorized owner choice

Owner supplied the selected recipient for the Dell V4 release-approval OTP/link. The email address is **stored only inside the isolated owner registry / Supabase Auth**, and is **not published to this repository or included in this receipt**. The owner chose **one email with both six-digit code and approval link, either method accepted once**. Owner authorization was previously explicitly given for bounded Dell V4 release; account enrollment is **not** a signed release.

## Independently verified changes

1. Existing Supabase project: `saczglesalubroyaucqe`. Exact case-insensitive lookup in `auth.users` returned **one** existing account, **one** with confirmed email; no account created.
2. Source migration: `supabase/migrations/20261027023500_matrix_v4_owner_registry.sql` applied successfully. The narrowly scoped `public.matrix_v4_owner_registry` binds `host_id=dell-linux`, `project_name=matrix_dev_manager`, the verified Auth user UUID and normalized email; the row must have `identity_enrolled=true` and **`release_signing_enabled=false`**.
3. Identity data was inserted by an explicitly authorized owner-admin action using a verified `auth.users` source (not an arbitrary client-provided UID). Separate readback verified **one exact owner binding**, `identity_enrolled=true`, `release_signing_enabled=false`.
4. DB readback of the registry: **RLS=true; FORCE RLS=true**; `anon` SELECT=false; `authenticated` SELECT=false; `service_role` SELECT=true. The separate `matrix_v4_owner_challenges` ledger has **zero** rows. No OTP emitted, no challenge consumed, no cryptographic signature issued.
5. Supabase Edge Function `matrix-v4-owner-approval` was updated to **version 2, ACTIVE, verify_jwt=true**. It obtains the exact owner UID/email from the service-role-only registry rather than from author-supplied environment strings. It denies missing, duplicate, disabled, invalid-identity or wrong-host/project rows and still requires all independent signer and email-template gates.
6. Independent GitHub fetch and Supabase deployed-source readback matched exactly. GitHub CI on source commit `8f351c5ad87ef5b7885ff94bd63dc4ac2ef1aef3` reports:
   - `Matrix source validation`, workflow `40399800959`: **success**, **267 passed, 63 skipped, 50 subtests passed**; repository safety success.
   - `Matrix V4 owner approval TypeScript check`, workflow `40399801866`: **success**.
7. Root/Dell controller release work was not executed as part of enrollment. Last completed Dell read-only receipt `a8a50cce-483a-4fd0-bca5-698ff24577b7` reported V3 `0.2.4-manager-governance-v3` active, no root owner public trust or signed release files.

## Secure release blockers unchanged

- The existing Supabase Auth email template **has not been certified** to include both `{{ .Token }}` and `{{ .ConfirmationURL }}`; callback allowlist and actual mailbox delivery are not verified. Do not trigger an experimental OTP to claim release signing.
- The original exact DEV_BETA public PEM and fingerprint remain unverified against server-held Ed25519 PKCS8 key. Never use the previous screenshot transcription as host trust.
- No separately reviewed source Git commit is enrolled into `MATRIX_V4_REVIEWED_COMMIT`; independent reviewer must finalize the source.
- The approval Edge service still requires the server-side owner origin, audited mail template, callback, exact reviewed SHA, DEV_BETA PEM fingerprint and independent enable flags before releasing signatures.
- Root-owned Dell trust, genuine owner-approved Ed25519 signature, actual host activation/rollback certification, host canary and source PR merges all remain pending.

## Reuse / open-source / cost gate

Reused existing Supabase Auth, Postgres RLS, Edge Functions, existing BHM governance branch and tests, no new paid provider or secrets created. Authorization remains scoped exclusively to Dell Dev Matrix; no Mac, Pine Engineer Beta, WordPress, CRM, customer or Ashwakaal data permissions granted.

**Final classification: `OWNER_AUTH_ACCOUNT_CONFIRMED / OWNER_REGISTRY_ENROLLED / EDGE_V2_LIVE_BUT_RELEASE_DISABLED / ZERO_EMAILS_SENT / NO_SIGNED_RELEASE / DELL_V3_UNCHANGED`.**
