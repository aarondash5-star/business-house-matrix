# Dell V4 owner approval: OTP demo and complete release blocker register

**Created:** 27 Oct 2026 IST (UTC dates can differ)
**Status:** `DEMO_SOURCE_ONLY / LIVE_EMAIL_NOT_SENT / NO_RELEASE_SIGNED / DELL_CONTROLLER_UNCHANGED`

## Scope and evidence

- Demo source: `brain/dev-toolyard/governance-v4/demo_owner_email_approval.html` — mobile-first self-contained **offline simulation**, no real emails, no Supabase access or controller changes.
- Automated contract tests: `test_demo_owner_email_approval.py`; tests assert mock-only and one-time consumption behavior in source. These source checks do not replace browser, API or production auth penetration tests.
- Supabase official email template variables can support both **`{{ .Token }}`** (six-digit code) and **`{{ .ConfirmationURL }}`** (magic link) in the same message. Documentation: https://supabase.com/docs/guides/auth/auth-email-templates and https://supabase.com/docs/guides/auth/auth-email-passwordless
- The shared project's **actual email template and SMTP deliverability have NOT been verified**. Do not edit the live shared email template before regression testing other apps and receiving an approved target owner email/UID. Never paste a real OTP into ChatGPT.
- Reviewed host status from terminal Dell control jobs: active `bhm-autonomy-controller.service` reports `0.2.4-manager-governance-v3`; Dell adapter `yard-auto-adapter-v1.2.0-20261026` and 20 bindings; `auto_promotion=false`.
- The Driver task `884cd886-943e-4ea8-93e8-9e5fcbaf100f` has completed an isolated 52-test technical build, but its receipt says `published=false`, `release_approved=false`, `design_complete=false`.
- PR #33 (V4 source-bound controller V1.4), PR #34 (signing broker with preflight/private staging) and PR #35 (Supabase approval method) are **draft and unmerged** at source audit; check again at promotion time.
- Existing `matrix-devbeta-attest` Supabase Edge function v1 is **active but intentionally disabled for key attestation**; it does **not** implement sending email OTP, issue release signature, or authorize controller cutover.
- DEV_BETA Ed25519 public-key image transcription is **not confirmed**; private-key match and release-signer trust are unproven. Never substitute Pine Beta key.

## Complete pending register, in execution order

| ID | Deliverable | Current evidence | Next release gate |
|---|---|---|---|
| A1 | Authorized owner identity | No independently verified, release-scoped Supabase Auth owner UUID/email | Enrol pre-existing owner account; exact owner UID, verified email and membership; deny user creation |
| A2 | Shared Auth mail template | Actual shared production template not audited | Non-mutating audit of Magic Link email template / redirect allowlist; test impact to all consumers |
| A3 | Both code **and** link in one email | Verified supported template placeholders, offline demo only | Approved template/staging and real end-to-end owner inbox delivery |
| A4 | Time-limited challenge issuance | Demo uses local five-minute timer only | Server-generated unpredictable challenge + immutable manifest SHA, single owner/host, 5-minute TTL |
| A5 | One-winner atomic consumption | Demo models this locally only | Private Supabase DB transaction and unique consumed state shared across code/link |
| A6 | Authentication hardening | Not certified | Rate limiting, resend throttling, replay rejection, wrong owner, expired/used token, authorized redirects, CSRF/state binding, audit without secrets |
| A7 | DEV_BETA public-key match | Unverified photographed PEM/hash | Obtain exact original public PEM/fingerprint or independently derive public key in secure signer context; run sign/verify proof, no private-key export |
| A8 | Scoped cryptographic release signer | Disabled attestation Edge only | Independent owner-auth release signer, exact SHA/payload, detached Ed25519/SSHSIG format compatibility, no arbitrary signing |
| A9 | Host-specific signature verification | Missing Dell/Mac trusted release public key | Root-owned, independently installed trust policy, exact host/release scope and source-digest pins; no changes to SSH login/root rights |
| R1 | V4 source review and CI | Draft PR #33, source candidate QA from prior receipt 104/104 | Recheck live adapter/ledger drift, review final diff, get independent signed QA approval; freeze release artifacts |
| R2 | Broker and deployment runner | PR #34 staging-only, no active fixed-purpose activation/rollback | Implement and independently test atomic backups, singleton lease, graceful queue drain, health checks and forced rollback |
| R3 | Negative/recovery certification | Current CI does not certify real signed release | Wrong signature, expired receipt, host mismatch, source drift, replay, disconnected host, rollback and power-loss simulation |
| R4 | Dell V4 one-lane canary | Controller still V3 runtime | Bounded Dell-only canary with terminal receipt, post-restart hash/version readback, service and lane monitoring |
| R5 | Lane Driver admission | 52-test technical-only build | Complete lane trace, negative/error recovery, deterministic re-route, independent quality review and owner-specific release admission |
| R6 | Mac release | Mac is a separate worker; no BHM controller reported | Explicit Mac manifest, separate host trust and tests; do not copy Dell runtime or release grant |
| R7 | Repository governance | PR #33/#34/#35 draft, no PR #34/35 independent reviews | Review, merge only approved source, separate release signature from GitHub merge |
| R8 | Deployment receipts and reporting | Verified-live Supabase Master event #166 exists for **disabled attester only** | Emit new, distinct event after verified V4 runtime release; include rollback receipts; never mark staging as live |

## Demo acceptance test

1. Open the offline demo file in a browser. Confirm banner **DEMO ONLY**.
2. Click **Generate simulated email**. It reveals both a mock six-digit code and a mock approval link, the same challenge, five-minute simulated expiry.
3. Enter a wrong code; it must be rejected. Enter the correct code; it reports **verified mock owner**, **not signed**, **not deployed**.
4. Attempt to use the other method; it must be blocked because the challenge was consumed.
5. Reset; generate a new mock email; use link first. Verify OTP is rejected after the link wins.
6. Test expiry and max attempted code checks.
7. Check no browser network calls and no root/SSH/GitHub/Supabase service mutations.
8. Before any real OTP, validate Supabase Auth template, sender and owner identity, then test with an approved owner inbox and implement server-side consumption. Offline demo success is **not** an authentication certificate.

## Exact deployment decision

`GO` only when A1–A9 and R1–R4, R7–R8 have concrete independent positive and negative receipts. The Driver/Mac expansion (R5/R6) remains separately gated. Otherwise `NO_GO`; keep V1.3 controller operational, preserve Dev Matrix work queues and worker identities.

**Cost / reuse:** existing Supabase Auth + Postgres/Edge Functions + current Dell SSH lanes + GitHub; no new SaaS, no purchase or usage authorization. Email sender may require a verified SMTP provider; no paid configuration without approval.
