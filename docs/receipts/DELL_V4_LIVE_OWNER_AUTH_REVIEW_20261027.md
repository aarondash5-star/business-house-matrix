# Dell V4 — Live Owner Authentication Review Gate
**Date:** 27 Oct 2026 IST

**Result:** Owner login/review **enabled for real user testing** on an SSO-protected HTTPS portal; owner sign-in **not yet performed**. Release signing and Dell V4 installation remain DISABLED.

## Owner review location
- Owner-facing URL: https://matrix-owner-key-preview.vercel.app/
- Vercel project: `matrix-owner-key-preview` (`prj_tIan42uLIMPFb7tcfQgCJVUzwQ13`)
- Deployed production-alias UI: `dpl_Gdf6KHyRE3tEEYwVDtqLtuS8TLh2`, independently `READY`; Vercel Authentication applies to **all** deployments. Production alias describes static UI availability, **not** Dell controller deployment.
- Login uses existing Supabase Auth owner email, existing public publishable client key, one-time code or magic-link Auth session; no service-role key, private signing key, owner UUID, or password in browser source. Owner clicks **Send Supabase sign-in email**, verifies a code or follows the link, and reviews in the same portal. Supabase GoTrue's *shared* email template and redirect allowlist are not certified; no claim that both delivery options currently arrive in one email.
- **The user must enter the emailed code into the portal, not in ChatGPT.** The project has not sent an email during this tool turn; request is owner-initiated via the web UI.

## Independent server check
- Supabase `matrix-devbeta-public-attest` version **3**, `ACTIVE`, `verify_jwt=true`, source readback exact-match GitHub. Supports `POST /owner-session` for exact existing Auth owner + private RLS registry, `POST /review` for **UI-only** feedback, and `POST /derive-public` for public-only DEV_BETA keypair proof. All fixed to `dell-linux` and `matrix_dev_manager`.
- Exact owner portal Origin `https://matrix-owner-key-preview.vercel.app` in reviewed source; no wildcard. CORS allows `apikey`, `authorization`, `content-type`.
- Read-only HTTP live-negative test from Dell control lane `53fa0a49-f1a2-46d5-b1b1-b900c451d77f`, exit 0:
  - Owner portal origin preflight with publishable-key header → **HTTP 204**
  - Unauthorized `POST /owner-session` with no JWT → **HTTP 401**
- **No authenticated owner POST** was performed. Therefore the real session verification and original DEV_BETA private-key/public-key pairing are **not yet proven**.
- New restricted `public.matrix_v4_owner_ui_reviews` RLS/FORCE RLS review ledger; anonymous SELECT denied, ordinary authenticated INSERT denied, service-role INSERT only; **0 UI review rows** and **0 release challenge rows** at verification.
- Review actions are `ui_acceptable` or `needs_changes`; optional 500-character notes. Database constraint **`release_approved=false`** prevents interpreting portal review as a Dell release-signing grant.

## QA and security gates
- GitHub workflows on source head `12b818788e4d0544629555cf65d9a6677076e1f8` passed: `40406975825` owner portal JS/safety, `40406975800` Deno TypeScript, `40406975705` source and repository checks.
- Prior CI baseline after adding review gates: **276 tests passed, 63 skipped, 50 subtests passed**; additional CORS change type-checked successfully.
- Existing `matrix-v4-owner-approval` release signer remains separately **disabled**. No private DEV_BETA key was exported, no release signed, no Dell root trust installed, no SSH/sudo permission change, no controller restart or V4 canary.
- Because this is a shared Supabase project, **do not modify the global Auth Magic Link email template**, SMTP or URL allowlist blindly. Real email deliverability and magic-link redirect are not certified; if link cannot return to the portal, add the exact portal callback through the independently authorized Supabase Auth admin interface after backing up settings, without loosening other apps' security.

## Owner test protocol
1. Open https://matrix-owner-key-preview.vercel.app/ and complete Vercel Authentication if prompted.
2. Enter the already verified Supabase owner email and click **Send Supabase sign-in email**.
3. Enter the six-digit code if one was supplied, or open the email link. If the link redirects elsewhere, do not paste access tokens or OTPs in ChatGPT; do not change the project's global Auth configuration without auditing it.
4. Wait for **“Verified existing owner”** from the server-side registry before proceeding.
5. In the same portal submit **“UI acceptable”** or **“Needs changes”** with optional notes. This records UX review only.
6. Optionally select **Verify DEV_BETA keypair**; only the public PEM/fingerprint may be returned. No release activation is possible through this UI.

**Final status:** `LIVE_OWNER_LOGIN_UI_AVAILABLE / SESSION_NEGATIVE_TEST_PASS / AUTH_EMAIL_DELIVERY_UNVERIFIED / OWNER_REVIEW_AWAITING_USER / SIGNER_DISABLED / DELL_V3_PRESERVED`.
