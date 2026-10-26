# DEV_BETA Owner Signing — Dell + Mac Authorization and Verification Receipt

Date: 26 October 2026 (IST)
Status: **OWNER KEY USAGE AUTHORIZED; NO SIGNATURE ISSUED; TRUST NOT INSTALLED; V4 NOT DEPLOYED**

## Verified scope and provenance

The owner explicitly certified use of the **DEV_BETA** Ed25519 signing identity for **both `dell-linux` and `mac-linux`**, and requested an actual signing operation. This certifies the owner decision and does not itself constitute a byte-level Ed25519 signature or independently installed trust anchor. The Pine Beta identity **PINE_BETA_ED25519_PRIVATE_PKCS8_B64** must remain separate and must not be silently substituted.

The photographed Supabase secret-name list shows `DEV_BETA_ED25519_PRIVATE_PKCS8_B64` and `PINE_BETA_ED25519_PRIVATE_PKCS8_B64`, **but not the secret values or a machine-readable verified DEV_BETA public PEM/fingerprint**. The earlier pictured Pine Beta public key belongs to a different workflow. Photographs do not prove keypair possession, exact public bytes or release-signer authorization.

Connected Supabase project `saczglesalubroyaucqe` currently exposes the normal Supabase management tools, but **no private-secret read or dedicated authenticated DEV_BETA signing action** was verified. The live `pine-engineer-beta-mcp` Edge Function references the distinct PINE_BETA secret, not DEV_BETA. Never export/read/copy any private key to ChatGPT, the generic SSH lane, repository or device worker.

## Independent runtime host audit

Read-only Generic Linux control jobs both terminal **completed/exit=0**:

- Dell receipt `35254ffa-79a3-4123-a32a-9c5ab92a515e`: online; `bhm-autonomy-controller.service` active; no `/etc/matrix-internal-release/allowed_signers`, no `/etc/matrix-dev-release/allowed_signers`, no signed V4 JSON or detached signature.
- Mac receipt `a8ee0381-89e6-4f59-bfed-391805d211b4`: online; no BHM controller service; no installed allowed-signers trust file or signed release approval.

**No release-signing operation, cryptographic keypair possession check, public key pin, host authorization, service change, root/sudo modification or controller promotion occurred.**

## Source-only exact host policy

Created:
- `brain/dev-toolyard/governance-v4/dev_beta_owner_release_trust_v1.json` — owner-authorized hosts are exactly Dell and Mac, both Dev Matrix scope, individually bounded release names, no production/spending/cross-project authority, TTL 5 minutes, one-use nonce + host-specific journals, signer disabled until independently verified.
- `brain/dev-toolyard/governance-v4/test_dev_beta_owner_release_trust_v1.py` — negative policy tests that prevent a guessed/unconfirmed public key, automatic signature, host release or accidental Pine Beta identity reuse.

GitHub Actions run `40379055857`, commit `bd58043f25f72e57bfb78a89b9dd29d1922851e6`, returned **success**: **201 passed, 62 skipped, 20 subtests passed**; public repo safety check succeeded. This certifies source integrity only; it is not an Ed25519 signing test or host trust.

## Exact conditions to execute signing

1. Obtain the exact **machine-readable DEV_BETA public PEM and its SHA-256 fingerprint over exact PEM bytes** from the owner's generator, *not* from a photographed/transcribed Pine Beta key. Independently verify they match.
2. Independently prove possession of the private key inside its already-approved Supabase owner-side secret store using a restricted **challenge sign → public verify** test. No private key output or secret introspection. Require the signer endpoint to be accessible only after fresh server-side verified owner email OTP or a single-use emailed link, as selected by the owner, tied to the exact host/release manifest, with rate limits, owner UUID authorization and audit.
3. If the existing V4 broker remains based on OpenSSH `SSHSIG`, implement and independently verify correct **SSHSIG-compatible** signing output. Raw WebCrypto Ed25519 signatures are *not* interchangeable with SSHSIG. Alternatively adopt a reviewed raw Ed25519 detached-signature adapter with independent key pin; never bypass signature validation.
4. Enroll the independently verified public key on Dell and Mac via a **separate, owner-authenticated host administration route** (not through a Dev Yard root/shell shortcut). Host policies must restrict Mac separately from Dell and maintain project isolation.
5. Certify independent V4 activation/rollback, protected V1.3 backups, immutable SHA pins, actual positive/negative/replay/key-rotation tests and one-workflow canary before promoting V4. Mac has no current BHM controller, so Dell's release approval must not silently install one on Mac.

No synthetic `signed` receipt may be issued. Final state: `OWNER_SCOPE_ACCEPTED / PUBLIC_KEY_UNVERIFIED / SIGNING_ENDPOINT_UNENROLLED / HOST_TRUST_ABSENT / CONTROLLERS_UNCHANGED`.
