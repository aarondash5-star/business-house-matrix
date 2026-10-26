# V4 Internal Release — Supabase Email OTP (owner enters code manually)

Date: 2026-10-26 (IST)  
Branch: `feat/v4-supabase-email-otp-release-20261026`  
Parent: `feat/v4-internal-release-broker-20261026` (draft PR #34)  
Status: **DESIGN SELECTED, SOURCE-ONLY; NOT ENROLLED, NOT LIVE, V1.3 UNCHANGED**.

## Owner decision

Replace proposed Google Authenticator TOTP and owner-operated SSH-signing UX with a **Supabase email OTP** owner-approval flow: one-time code delivered to an independently verified owner email address, **entered manually into a secure approval page**, never in ChatGPT or a Generic Linux SSH tool prompt. Do not reuse the generic Linux 4-digit passcode or assume the current Supabase project has an enrolled release-approval owner account.

Email OTP is mailbox-based authentication and is **not equivalent to authenticator-app MFA**. The selected owner-approved risk level is accepted for the bounded V4 internal development-controller release only; no production publish, customer changes, payment, trading or root-permission mutation.

## Current verified infrastructure / technical constraints

- Existing Supabase project `saczglesalubroyaucqe`, Supabase Auth and Edge Functions. Other platform/WordPress/worker tables are shared: **isolate this approval workstream by strict owner-UID policy, dedicated private schema, purpose-limited Edge Function, separate release signing identity, no user/data sharing**.
- Supabase official flow: `auth.signInWithOtp({email,options:{shouldCreateUser:false}})` sends an email; `auth.verifyOtp({email,token,type:'email'})` verifies manually typed OTP and returns a valid session. The Magic Link template must contain `{{ .Token }}` to send a numeric code; by default it may send a link. A template change may affect *other* applications using the same Supabase Auth project. **Audit template and existing sign-in consumers before changes** and test for regression. Official docs: https://supabase.com/docs/guides/auth/auth-email-passwordless
- Supabase's default email sender is not a production SMTP service and may only send to pre-authorized project team email addresses without custom SMTP. Confirm delivery to the approved owner inbox before claiming enrollment. https://supabase.com/docs/guides/auth/auth-smtp
- The V4 broker in PR #34 currently accepts **OpenSSH SSHSIG owner signatures only** and exposes `preflight` and `stage` (no fixed-purpose `activate` or `rollback`). Email OTP is not automatically a host-verifiable cryptographic signature. **Do not bypass signature checks**; build a reviewed broker adapter that verifies a separately issued asymmetric Ed25519-signed release receipt pinned to a trust key that the Dell Dev worker cannot modify.
- Current PR #34 remains draft until independent QA and owner's release mechanism certified. Previously observed host source controller V1.3 and queued Driver with zero attempts. Verify all live claims again before any execution.

## Owner UX

1. Authenticated owner opens release-approval page (mobile-first, HTTPS, no chat-exposed OTP).
2. Page shows **Dell V4**, project `matrix_dev_manager`, exact reviewed source commit plus adapter, guard and ledger SHA256, zero spend, development-controller release, rollback plan, one-time nonce and **Approve release**. No generic "approve all" option.
3. Server issues a pending challenge tied to that exact immutable manifest and the allowlisted owner UUID. Client asks Supabase Auth to send an **email code to the server-pinned owner address** (`shouldCreateUser:false`). Never accept arbitrary email for release authority.
4. Owner copies the code from email and manually enters it on the HTTPS form. The code goes **directly to the owner approval service**; no code, email contents, access token, refresh token or session are sent to ChatGPT, Dell worker, GitHub issues, logs or customer tables.
5. Supabase Auth verifies the code. The server obtains trusted user from Auth server, checks exact pre-enrolled owner UUID and verified email and that it matches the single pending challenge. The approval request expires after 5 minutes; the OTP uses the stricter of the server limit and provider expiry. Challenge is consumed atomically; code failure throttled and audit-only receipt records exclude OTP and full JWT.
6. For a *currently approved/pinned* SHA manifest, a dedicated, owner-controlled release signer issues **detached Ed25519 signature** over canonical payload (owner UUID, release ID, request/nonce, exact manifest/hash set, `host:dell-linux`, `project:matrix_dev_manager`, `production:false`, `spend:false`, `single_use:true`, issued_at, expires_at within 5m). The private signing key is server-owned, never accessible to Dev worker or stored in GitHub.
7. Dell fixed-purpose broker independently validates signature with pinned public key, immutable source pins, challenge expiry, single-use local and cloud replay ledger, release gate and independent QA, then invokes a separately certified bounded host activation runner with backup/service health/rollback. Anything unknown **fails closed**.
8. Approval UI shows actual post-execution verified terminal receipts; never claim success when only OTP or queue submission succeeded.

## Back-end release policy

Use the existing Supabase Auth provider for OTP transport and verification; use a separate purpose-limited release approval Edge Function and **private** Postgres schema/tables with no anon or general authenticated write privileges. Server-owned release ledger binds SHA, OTP challenge, owner UUID, nonce, trusted Auth verification, issuance, expiry, single-use, rollback receipt and outcome_unknown. Verification must be based on **server-authoritative Supabase Auth identity** rather than a client-supplied email or `user_metadata` claim. RLS and exact, narrow database permissions are mandatory. Avoid a `public` SECURITY DEFINER RPC. Do not mint release approvals on generic dashboard login alone; require a fresh OTP verified as part of this exact challenge.

To avoid an uncontrolled Ed25519 key or bespoke crypto: use standard WebCrypto only after independent key custody, public-key pinning, signature-format compatibility and negative tests are certified. Existing OpenSSH `ssh-keygen -Y verify` expects the SSHSIG format: a raw WebCrypto signature is **not** interchangeable. Select and QA a precise verified format before changing the live broker. Owner confirmation in chat must never be converted into fake owner signing evidence.

## Required negative tests (release gating)

Wrong owner UUID/email, nonexistent/unverified account, no configured owner, wrong OTP, expired OTP/challenge, duplicate challenge, resend rate abuse, wrong project/host, altered artifact/QA hash, changed original V1.3 SHA, changed source branch after approval, unsigned receipt, mismatched signing public key, cross-tenant record, replayed release ID, clock skew, absent rollback, offline Dell, outcome-unknown SSH task and tampered rollback artifacts must all fail closed. Test delivered code manually with a dedicated test owner account; do not send OTP from live Supabase until recipient and email transport are verified. GitHub source CI alone does not certify this flow.

## Critical gates remaining

1. Verify owner-controlled **email recipient** and Supabase Auth allowlisted owner UUID; ensure there is no open sign-up, impersonation or unsolicited email issue. Avoid hardcoding personal email in Git/Docs.
2. Audit existing shared project's Magic Link/OTP email template and SMTP deliverability without breaking connected applications. A dedicated auth tenant may be justified only if isolation cannot be safely achieved using the existing project; check ongoing cost first.
3. Implement privately scoped OTP challenge and verification with audit/ledger. The code must be entered on a secure page, not pasted into chat.
4. Implement independently signed host release receipt and correctly matching fixed-purpose verification. Do not reuse or weaken the SSH-signature validator.
5. Independent QA of both OTP positive/negative flow and real signed receipt, safe host activation, rollback and one workflow canary. Merge/deploy only after gates pass.

## Reuse / cost

Reuse existing Supabase Auth, verified owner session identity, existing Supabase Edge + Postgres private-schema ledger, project GitHub, Dell Generic Linux SSH transport, Python controller, OpenSSH/WebCrypto and existing V1.3 backup/canary requirements. Expected new software licence cost: zero. Email delivery may need custom SMTP if the owner address is not in the Supabase project team or the default service cannot meet operational needs; no paid service approved.

## Handover status

`AUTH_METHOD_SELECTED_EMAIL_OTP` / `OWNER_RECIPIENT_NOT_ENROLLED` / `EMAIL_TEMPLATE_NOT_AUDITED` / `RELEASE_SIGNER_NOT_ENROLLED` / `BROKER_OTP_ADAPTER_NOT_DEPLOYED` / `V1.3_PRESERVED` / `V4_NOT_LIVE`.

This document records a decision and integration specification, **not** a verified live Supabase change or signed release. No Supabase Master event until an independently verified material change.
