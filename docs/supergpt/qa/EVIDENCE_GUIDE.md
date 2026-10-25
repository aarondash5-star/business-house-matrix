# SuperGPT — independent QA evidence collection

[Return to canonical source](../README.md)

**IMPORTANT:** The release-evidence JSON is an attestation index; it does not itself execute a test or establish a valid owner approval. Link independent, retrievable receipts. Never paste secrets, device identifiers, private user content or signing keys.

## 1. Build provenance

Record the exact GitHub Actions run URL, the build/source commit and immutable upstream code reference, artifact name and the **APK file** SHA256. Extract the APK from the GitHub artifact ZIP before hashing; the artifact ZIP digest is **not** the APK digest.

- Run an Android CI workflow against the candidate commit; inspect job steps, conclusion and artifact.
- Download ZIP, extract and record `sha256sum path/to/app.apk`; avoid committing the APK to this public repository.
- Use `aapt dump badging app.apk` to record the Android package/application identity.
- Check version, signing certificate and runtime permissions for the candidate.

## 2. Actual Android run

Use a physically authorized Android phone or headless emulator. For Dell, verify hardware-backed virtualization access before installing an emulator; existing `generic-auto-exec` user lacked `/dev/kvm` access. Prefer a minimal AOSP image without Play Store; if KVM remains unavailable, use an owned physical Android device, not an emulator without adequate acceleration.

Illustrative commands (replace placeholders from actual `aapt` output; do not copy literally):

```bash
adb devices -l
adb install -r ./app.apk
adb logcat -c
adb shell monkey -p ACTUAL_PACKAGE_NAME 1
adb shell pidof ACTUAL_PACKAGE_NAME
adb logcat -d -v time > android-cold-start.log
grep -E 'FATAL EXCEPTION|AndroidRuntime|ReactNativeJS|FirebaseApp' android-cold-start.log
```

Check cold launch, foreground/background/resume, networking/offline state, chat entry, navigation, logout if present, app permissions, memory/CPU on lower-end device and crash-free startup. A grep hit is not automatically fatal: QA reviews context and records the outcome. A clean grep alone is not proof of a working user journey.

Record only non-sensitive test logs/screenshots at a private QA receipt location, linked in the evidence file. Avoid uploading live customer data.

## 3. Independent QA

A reviewer separate from the implementation owner checks:
- reproduced APK digest matches tested build;
- actual Android install/start/user journey;
- no fatal native/JavaScript crashes;
- permissions, data isolation and endpoint authentication where features are implemented;
- stated limitations vs product acceptance;
- source, version, release rollback and reproducibility.

Mark each field `passed` only after a matching receipt exists. If a feature is not implemented, record `pending` or `blocked`; do not mark `passed` by substituting a mock. Reviewer identity and receipt URL are required for production policy validation.

## 4. Owner acceptance and promotion

Record approval of an exact release candidate with a link to the owner's verified GitHub issue/PR decision or other auditable authorized record. Do not infer owner acceptance from "go ahead and set up branches". QA does not grant publication authority. Production branch promotion, signed APK distribution and public launch are separate decisions. The existing `super-gpt/production` branch is a placeholder until a candidate passes.

## 5. Evidence status meaning

`pending` = never certified; `blocked` = attempted but prerequisite denied; `failed` = executed and failed; `passed` = independent receipt reviewed. CI validation checks fields and selected provenance, but branch protection and reviewer verification are separate controls.
