# Dell V4 Guided Installer — Owner-Authenticated One-Window Workflow

Date: 27 October 2026 IST
Source branch: `feat/dell-v4-guided-installer-preflight-20261027`
Status: **PREFLIGHT CODE READY FOR REVIEW; INSTALLATION BLOCKED. NO LIVE CONTROLLER CUTOVER.**

## Owner-approved workflow

Owner accepted a guided CLI installation path. The owner will authenticate directly in an independently authenticated Dell terminal if and when the operating system requires an admin password. Do not ask the owner for credentials in ChatGPT or capture terminal password input in application logs. Current Generic Linux SSH may already have passwordless sudo: do not alter sudoers to force a password prompt. *OS authentication and release authorization are distinct.* The final release still requires a verified, source-pinned approval (owner's preferred Supabase email with link + OTP, consume once), a matching cryptographic signing key and a separately certified fixed-purpose host activation/rollback runner.

## Actual remote access verification

Vercel project **`dell-private-login-ui`** is independently confirmed `READY` at production alias `https://dell-private-login-ui.vercel.app/`, deployment `dpl_9dZMqYPvwrtvtfuk9To8akALSgEa`. Deployment contains a `src/index.html` titled "Dell Secure PIN Login" with a PIN screen and remote desktop UI. **The actual secure password handling, TLS session bindings, API identity/isolation, remote desktop worker, input interception resistance, terminal process and current functional login are NOT end-to-end verified.** A Vercel READY deployment and HTML title are not a security certification. Do not enter an administrator password or private key there until its full authentication and terminal transport are independently reviewed. Use a directly trusted terminal with a native, unlogged OS password prompt in the interim.

## Implemented in this branch

- `brain/dev-toolyard/governance-v4/guided_dell_v4_install_preflight.py`: fixed-host, read-only preflight. Supports ONLY `preflight`; it cannot install or restart. The program prints a structured, nonsecret JSON status and non-zero exit when blocked. Hard-pins controller source hashes and exact legacy adapter/ledger hashes expected by draft PR #33. Checks source drift, service presence, Symlink traps, private approval-file presence, root-owned signer trust. **Explicitly denies automatic authorisation even if files are present**; status of signature verification and activation/rollback remains `false`. No sudo/SSH calls, no privileged configuration writes, no owner password capture, no approvals minted.
- `test_guided_dell_v4_install_preflight.py`: negative tests for modified hashes, symlinks, spoofed trust, missing and faked signed approval, service state and forbidden activation. Test runner must execute with repository CI / disposable isolated sandbox, not as a replacement for real host canary.

Reviewed candidate can only be promoted after exact source rebasing; fake grant, forced install, SSH brute-force, or copying DEV_BETA private credentials are not approved workarounds.

## Current Dell evidence

Read-only SSH terminal receipts `d62b3cfd-9138-4aad-91bd-c9d46520d16b` and `78b5b9b4-8db5-44c4-a5f2-29c9745a7333` completed exit 0:

| Subject | Actual live Dell | PR #33 original source pin | Result |
|---|---|---|---|
| Controller | `0.2.4-manager-governance-v3` / `e6834bb2...` | `e6834bb2...` | Controller SHA matched |
| Guard | `7a989c6b...` | `7a989c6b...` | Original guard SHA matched |
| Adapter | `adad20add5e247c515c48d8e2d0c61f2b91e2238d489ed8b4c2e674c845d1abe` | `16f54c4ae1d97699786b649e84c94df2abb673b0682a20045d55399399217b79` | **DRIFT: release candidate stale** |
| Binding ledger | `9c084832984c1471a22079cc606daccd0a49b78c942ddfee0800a800176c43a9` (20 bindings) | `20f68602194af481d48dfaf6bcc406d383f0818f7bd082cf5d92227b24aac64e` | **DRIFT: release candidate stale** |
| Driver task | `884cd886-943e-4ea8-93e8-9e5fcbaf100f`: `completed`, `attempts=1`; 52 tests | Previously queued | Technical build only; not released |
| Owner signature/trust | No trust file or signed release approval | Required | **MISSING** |
| Fixed-purpose activation/rollback | Not installed/certified | Required | **MISSING** |
| V4 PR source | PR #33/#34/#35 draft | Independent review required | **REVIEW PENDING** |

Current running `bhm-autonomy-controller.service` **was not restarted or changed**.

## Executable owner path — only after authorization and installer certification

1. Audit Dell remote UI; ensure a true isolated, authenticated terminal with a **native** sudo/OS password prompt, protected session, no keylogger or password relay through ChatGPT, and no root/sudo permission changes. Alternatively use direct Dell terminal.
2. Rebase and independently review PR #33 V4 adapter/bindings against live hashes above, re-run exact detached QA and rollback scenarios, freeze candidate commit and hashes.
3. Enroll original exact DEV_BETA public PEM only after live private-key possession attestation in owner-controlled Supabase Edge; do not infer bytes from photographs. Verify email template, receiver, SMTP and owner Auth UID; one email may contain both `{{ .Token }}` and `{{ .ConfirmationURL }}`. Implement atomic server-owned one-use challenge.
4. Independently issue the signed release grant bound to frozen host `dell-linux`, project `matrix_dev_manager`, source SHA, five-minute owner grant expiry, one-time release ID, zero spend, no production. Verify with root-owned trust outside worker write scope.
5. Review and certify a **separate fixed-purpose activation/rollback runner** with exact file allowlist, backups, dry-run, queue lease, drain, service restart health, negative tests and real restore. Only then present a single `sudo` password prompt to the owner if a native OS prompt is actually required; do not add one if current sudo authenticates without password.
6. Run a single Dell V4 canary, poll terminal receipts, verify PID/health/installed source hashes and rollback state. Mac work is separate and cannot inherit Dell's release.
7. Update release issue, PR review and authorized Master inbox only for independently verified changes; no false claim that this preflight is live V4.

## Safe CLI usage after code is reviewed and locally installed

```sh
python3 guided_dell_v4_install_preflight.py preflight
```

The preflight returns exit code **3 when blocked**. This is expected on the current Dell source and is **not** a request to bypass. This file does not provide an `install` or `activate` command. Its name reflects its place in the guided installation pipeline, not an executable active release.

**No approval repeat required:** the owner's intent to proceed was accepted; the remaining gates are technical cryptographic and reproducibility certification.

## Reuse / cost

Python stdlib, existing Dell SSH six-lane transport, Vercel existing remote UI (after audit), existing Supabase Auth/Edge, OpenSSH/Ed25519, existing source QA and systemd. No new subscription, secret, privilege change or spending. Fallback remains the active V1.3 controller.
