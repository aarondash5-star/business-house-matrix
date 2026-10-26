# DEV_BETA Screenshot Extraction + Keypair Attestation Deployment — 2026-10-26

## Outcome

**Supabase Edge Function deployed in a disabled / fail-closed state.** This is *not* a cryptographically certified owner release and is *not* a Dell or Mac trust deployment. Owner's scope remains `dell-linux` and `mac-linux`, with project `matrix_dev_manager`; Pine Engineer beta and all other workstreams excluded.

### Image evidence extraction

Two user-supplied photographs show **distinct keys**:

1. The prior screenshot is labeled Pine Beta and is associated with `PINE_BETA_ED25519_PRIVATE_PKCS8_B64`. It must never be used as DEV_BETA.
2. The second screenshot shows a DEV_BETA-generated Ed25519 public PEM and a displayed hash, while a separate screenshot identifies two *secret environment variable names* but **not their secret values**.

From the blurry DEV_BETA image, the observed SHA-256 text appears to be:

`1eee3d266eb1d362b9c7f36d0301b831a8a527828682505ff286d2738606eec7`

The tentative SPKI Base64 transcription is:

`MCowBQYDK2VwAyEAqKeblk/QLUfKDouPOhJSNV1nnH06lYY8gsP8JYDMTE=`

**This transcription is not a valid 60-character Base64 representation of a 44-byte Ed25519 SPKI**: it has only 59 characters. It cannot be imported as a trustworthy public key or matched against a private key. Exhaustive one-character insertion and one substitution failed to reproduce the visually observed fingerprint under canonical LF-terminated PEM. The photographed hash itself may also contain transcription ambiguity. Treat both strings as **unverified image evidence**, never as trusted release input. Use the original generator's Copy public PEM/fingerprint or an independently authenticated public-key derivation/attestation. The public key is *not* pinned to either machine.

### Verified implementation

New restricted Edge Function:
- Project `saczglesalubroyaucqe`
- Function: `matrix-devbeta-attest`, version **1**, status **ACTIVE**, `verify_jwt=true`
- Release mode: **always disabled** (there is **no** `/sign-release`, `/activate` or `/rollback` endpoint).
- Endpoint source: `supabase/functions/matrix-devbeta-attest/index.ts` on PR #35; connected Supabase readback confirmed byte-for-byte equality with GitHub.
- No new secret created or exfiltrated. Existing `DEV_BETA_ED25519_PRIVATE_PKCS8_B64` is accessed only if independently configured attestation is explicitly enabled and a server-authoritative owner user ID is authenticated.
- For future owner-authenticated keypair attestation, the service generates a fresh in-memory challenge, checks canonical public PEM and SHA256, signs only the prefixed **non-release attestation challenge**, verifies Ed25519 signature against public key and returns a status without exposing signature or secret.
- Required environmental gates (currently **not confirmed provisioned**): `MATRIX_DEV_BETA_ATTEST_ENABLED=true`, `MATRIX_DEV_BETA_OWNER_UID`, `MATRIX_DEV_BETA_PUBLIC_PEM`, `MATRIX_DEV_BETA_PUBLIC_SHA256`, existing server-side DEV_BETA PKCS8 secret.
- Edge Function deployment is live but cryptographic test is **not yet runnable** because no exact verified public material and no independently enrolled owner release identity were proven.

### Tests and audit

- GitHub workflow for `7acf64187bb6b84f02e5dec190bf53a5d75b6093`: success.
- GitHub workflow for `2f40fe8e3627987952e0aeeee637603920ecb43e`: success, including source and public-repository safety.
- Existing source policy `brain/dev-toolyard/governance-v4/dev_beta_owner_release_trust_v1.json` updated to record screenshot uncertainty, **enabled=false**, `issue_signatures=false`, `allow_host_activation=false`, and attestation-service version.
- Dell and Mac are connected, with fresh 3-lane heartbeats confirmed during this turn.
- Earlier read-only host receipts verify no trusted `allowed_signers` present; no new writes to Dell or Mac were issued.
- Master Stack authorized event inbox accepted event #**166** (`bhm-matrix-devbeta-attest-edge-v1-20261026`) and read back `pending_review`; not published to Master Doc, not represented as a completed V4 release.

### Next actual release gates

1. Exact public PEM/fingerprint attestation against existing Supabase private key (no private secret export). 
2. Owner authorization via **single email containing link AND OTP**, with one successful verification consuming the release request atomically. No OTP collected inside ChatGPT; verify owner UID server-side and single-use, hash-pinned, 5-minute release intent.
3. Separately reviewed cryptographic release-signature format and independent host public-key enrollment; never treat an Auth JWT or an email OTP as a release signature.
4. Host-specific activation/rollback implementation, independent canary and V1.3 recovery before promoting Dell V4; Mac must have its *own* release manifest and authorization.

**Final certification**: `SUPABASE_ATTEST_FUNCTION_ACTIVE_BUT_DISABLED / PUBLIC_KEY_TRANSCRIPTION_UNVERIFIED / OWNER_SIGNING_NOT_EXECUTED / DELL_V1.3_ACTIVE / MAC_CONTROLLER_ABSENT / HOST_TRUST_UNCHANGED`.
