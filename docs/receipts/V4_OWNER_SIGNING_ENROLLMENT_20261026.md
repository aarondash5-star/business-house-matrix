# Owner-controlled V4 release signing — enrollment and approval handover

**Status:** OWNER CHAT APPROVAL RECEIVED / CRYPTOGRAPHIC OWNER SIGNATURE NOT YET ENROLLED / DELL SHARED CONTROLLER V1.3 ACTIVE / V4 BROKER SOURCE-ONLY.

**Scope:** \`dell-linux\` only; project \`matrix_dev_manager\`; release \`matrix_v4_controller_v14\`; exact reviewed V4 adapter/guard. No Mac rights, cross-tenant permissions, production publishing, new sudoers entries, worker SSH grants or customer data.

## Independently verified facts (26 October 2026 IST)

- User explicitly approved proceeding with the controlled Release Broker and V4 path in ChatGPT. A chat instruction authorizes intent but is **not** a cryptographic release artifact.
- Read-only Dell SSH terminal receipt \`d3e28727-face-47a9-aee5-c069cbf4ba6e\`, exit 0: \`bhm-autonomy-controller.service\` active, original controller SHA \`e6834bb2f7765ee0aa26d215a566f70276e4f8c2c87c8730fc781c27dc778836\`, original adapter SHA \`16f54c4ae1d97699786b649e84c94df2abb673b0682a20045d55399399217b79\`, V1.3 guard SHA \`7a989c6b484a13a4fdf349d698a6a1bf9e8d9b1afa9684508606bc08c036283e\`. Lane Driver task \`884cd886-943e-4ea8-93e8-9e5fcbaf100f\` queued/attempts=0.
- Required owner trust file \`/etc/matrix-internal-release/allowed_signers\` **MISSING**; canonical owner approval \`~/.matrix-release-authorizations/v4-owner-release.json\` **MISSING**; broker host deployment directory **NOT INSTALLED**.
- The first earlier Dell broker staging command was blocked by platform execution safety checks. **Do not reroute it through a different lane or connection.**
- Repository CI source validation for commit \`787899cddb8fc9bc3c6406514aba3ca4f0ffaedc\`, GitHub Actions run **40356607890**, terminal **success**. Log: **193 passed, 62 skipped, 20 subtests passed**; the host-fixture-dependent suites are intentionally skipped in the repository checkout. This is source-level QA only, not independent signer acceptance or Dell runtime certification.

## Security model

The release authority must remain independent from the Dev Yard worker. **Never give the private signing key, passphrase, SSH agent socket, or owner-only workstation account to ChatGPT or generic-linux SSH.** Do not generate the private signing key in the worker home, GitHub Actions runner, repo, or remotely through the ChatGPT tool bridge. The private signer remains on an owner-controlled local computer/account separate from the Dell Dev worker.

The public Ed25519 key may be enrolled by the owner into the independently root-owned file \`/etc/matrix-internal-release/allowed_signers\`, under the exact principal \`matrix-v4-release-owner\`. File and parent directory must be owned by root and not group/world writable. Enrollment does not require a new root account or any sudoers adjustment. Owner must perform this through their **separate, independently authenticated host administration route** and read back permissions; it is not safe to substitute the Dev worker's existing generic shell privileges.

An owner-controlled station may use existing OpenSSH tooling:

\`\`\`sh
# Run on the independent owner station, NOT on the Dell Dev worker.
umask 077
ssh-keygen -t ed25519 -a 64 -C 'matrix-v4-release-owner' \
  -f "$HOME/.ssh/matrix_v4_release_owner"
# Keep the private key ONLY here; copy only the .pub key for trust enrollment.
\`\`\`

The owner's trusted Dell administrator should provision a root-owned allowed-signers file whose exact single line has the form:

\`\`\`text
matrix-v4-release-owner ssh-ed25519 <PUBLIC-KEY-BASE64>
\`\`\`

The trust file's key must be the public half of the independently held owner signing key. Do not include any real private key or secret in the Git repository or chat.

## Signed approval scope

The independently prepared approval must be canonical JSON encoded as **sorted keys, compact separators and one final newline**. Sign with OpenSSH:

\`\`\`sh
# Execute from the independent owner workstation only, after verifying payload.
ssh-keygen -Y sign -n matrix-v4-host-release \
  -f "$HOME/.ssh/matrix_v4_release_owner" v4-owner-release.json
\`\`\`

The resulting \`v4-owner-release.json.sig\` is the detached signature. Only transmit the signed JSON and detached signature to the Dell owner-controlled approval inbox after verifying the exact commit and receipts. Never transmit the private signing key.

Expected fields and reviewed pins:

| Field | Required value |
| --- | --- |
| schema | 1 |
| host | \`dell-linux\` |
| project | \`matrix_dev_manager\` |
| manifest | \`matrix_v4_controller_v14\` |
| action | \`internal_component_release\` |
| source_commit | \`5952cf690e65210de039f7fcd0f53caf76548c6c\` |
| adapter_sha256 | \`116f435279bbe7e0cc8281ab513e319926b846ab6ae25752bccc3fc6746fb773\` |
| guard_sha256 | \`90f0a62cc6cfaf1458f0684363ffb9288c900ba0ade707908da0877447249e30\` |
| v14_gate_sha256 | \`bb0339f48add0537771dec2b2e4898258bfd4bd7758e1648a62f10130a2ee3e3\` |
| qa_receipts | Exactly \`da27d9b3-e7f0-4324-b8b1-263b5905f98f\`, \`7c549787-c1bb-4dca-bc45-a5d6687a77de\` |
| release_id | Fresh identifier matching \`v4-controller-20261026-[a-z0-9]{12,40}\` |
| expires_utc | Timezone-aware UTC date within **one hour** of use |
| max_activations | 1 |
| production | false |
| spend | false |

The owner should generate/inspect the canonical payload privately; do not reuse a template approval with an expired time or a previous release ID. The existing code requires exact pins and will reject any mismatch.

## Release gates after enrollment

1. Independent QA of the new broker including **real signature verification** with a temporary owner-controlled test key and replay/expiry/forgery checks. GitHub source CI alone does not suffice.
2. Reviewed host runner with fixed-path-only activation, exclusive queue lease, crash journal, restorable backup, timeout, health checks and **actual on-host rollback**; the current source broker implements **preflight and private staging only**, not V1.4 activation.
3. Independent owner signature on final release payload plus an independently audited host deployment action; do not reuse the general SSH lane as a substitute for the prior platform safety denial.
4. Only then enable a single live V4 workflow, certify terminal receipts and preserve V1.3 recovery. Complete real Lane Driver and Mac parity in later separately gated steps.

**Explicitly prohibited:** generating owner-signing private key inside the Dev Yard; self-signing owner approval; copying a signing key, generic root permission change, direct controller patch, approval-ledger forgery, suppressing QA failure, premature service restart, or claiming this document is a live deployment.

**Status:** \`OWNER_INTENT_APPROVED / INDEPENDENT_SIGNER_MISSING / BROKER_SOURCE_CI_VERIFIED / DELL_INSTALL_BLOCKED / LIVE_CONTROLLER_UNCHANGED\`.
