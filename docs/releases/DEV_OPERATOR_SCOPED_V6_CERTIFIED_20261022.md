# Dev Operator v6 — Hardened Scoped Release (22 Oct 2026)

**Release channel:** `release/dev-operator-scoped-v6-security-20261022`
**Release classification:** **CERTIFIED & LIVE — owner-enrolled, offline static-HTML coding only**
**Source-of-truth tested code:** commit `e1d97ba35ff74c5446126891d8f56e54ac42c975`; subsequent hotfix changes up to `974ab04b45219e202672a468261bdbfba0f3a850` were documentation-only.
**Deployed machine:** Dell `dell-linux`, existing nonroot `bhm-autonomy-controller.service` **user service**.
**Operational status:** Deployment already active before this release record. No needless restart or binary replacement performed during this promotion.

## Release decision

**PASS — bounded v6 hardening/source release.** The independent Business House Matrix Dev Operator has a proven, owner-enrolled, no-network/no-tools model coding route producing local, unpublished Git review commits with independent Bubblewrap static-HTML QA. The v6 strict inert HTML5/CSS policy is validated at proposal acceptance and independently inside the sandbox. v4/v5 failures and receipts remain part of history.

**NOT a general-purpose autonomous developer or a blanket security guarantee.** No model-selected host commands, root access changes, private cross-project mounts, network access in workcells, production publishing, remote generated-code pushes, purchased APIs or unauthorized enrollment.

## Exact release build

| Artifact | Verified value |
|---|---|
| Controller source | `brain/mvp-controller/controller-general-dev-v6-candidate-20261022.py` |
| Running Dell controller SHA256 | `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e` |
| Dell/Mac v6 policy SHA256 | `fd239a658ccd4d317cc2a895c1d64eec712d987b2ff5dbbf8d30da7a72f887ce` |
| Dell/Mac coding agent SHA256 | `c8f67820b1bc216f18a662d9248f790d25e37369d2fd42cde9002ec7578ff5b8` |
| v6 deployment directory | `~/matrix-controller/general-dev-release-v6/` |
| Enrolled manifest | `brain/dev-operator/enrollments/matrix-dev-security-v6.json` |
| Task ID | `e92144e5-0755-4945-b1a3-758702de0c75` |
| Local review Git commit | `2b70a5994400f4dda02cebb7a9e233691f1233d8` |
| Published / pushed generated output | **false / false** |

## Acceptance evidence

- **Gate A PASS:** independently sourced clean Dell/Mac peer revision and policy SHA parity, each `38/38` unit/security/sandbox tests PASS, exit 0; controller active and checksum matched.
- **Gate B PASS:** newly generated v6 static-HTML page passed Dell Chrome/Playwright checks at 320, 360, 390, 430, 768, 1440 CSS px, `6/6` PASS; no external request, page error, or horizontal overflow detected. Existing installed Chrome and Playwright reused.
- **Gate C PASS:** 37 adversarial negative tests and 2 positive controls on **each host** `39/39 Dell`, `39/39 Mac`, all exit 0. Cases include unsafe HTML, CSS URLs, entities, escaping, SVG/MathML, malformed structural cases and fail-closed rejection.
- Independent earlier release document `docs/receipts/DEV_OPERATOR_V6_FULL_RELEASE_QA_20261022.md` also records historical 7/7 v6 browser test and controller self-test, with receipts.
- **Exact fresh IDs**, test assertions and retained SHA checks: `docs/receipts/DEV_MATRIX_V6_GATES_ABC_CERTIFICATION_20261022.md`.
- No GitHub-hosted CI workflow success is asserted; source and on-host runtime certification are distinct.

## Promotion performed by user instruction "Document and deploy"

1. Read original STOP handover and used already certified A–C evidence. The user expressly authorized documentation and deployment after completion of A–C.
2. Reverified Dell running v6 checksum, user service active, Mac peer source, v5 rollback checksum, outstanding queue and unpublished local generated output.
3. Confirmed that the v6 source branch is a direct descendant of the scoped v5 release and that changes after certified `e1d97ba...` are only documentation.
4. Reused the **pre-existing** versioned v6 release branch, fast-forwarding it (non-force) to encompass current v6 handover/receipt documents. Added this authoritative release decision and the new detailed A–C receipt record.
5. **No controller reinstall/restart** was necessary or performed: already-live, independently verified deployed candidate is the exact certified release. No GitHub `main` merge, no alteration of PR #8, no production website publishing, and no expanded tool permissions.

## Rollback & recovery

The source-of-truth pre-v6 controller backup is:
`~/matrix-controller/controller.py.bak-20261022-static-security-v6`
SHA256 `df0cf3f968244d2e745d941f57d2225cfcd4a4147f55f7ce29c879e87027ffe4` (**v5**).

**Caution:** v5 is known to have had a permissive active-content validator. Treat rollback as an incident operation subject to separately granted authorization; stop submissions, attest zero delegated tasks, assess exposure, restore and re-verify only under a controlled incident plan. Do not assume older v5 is safe for unknown HTML. The `controller.py.bak-20261022-generaldev-v5` file contains a v4 SHA and is not the pre-v6 v5 snapshot. Preserve all backups and previous SQLite/local run receipts.

## Mainline governance and further development

- `main` and the hotfix branch have substantially diverged; **do not merge wholesale** or silently replace later `main` work with older features.
- Preserve existing v5 release branch, original draft PR #8, and Issue #2 independently. Any future mainline cherry-pick/rebase needs isolated diff review and hosted CI.
- Remaining **Gate E** is *not* included: arbitrary approved repositories, multi-language isolated edit/build/test adapters, project-scoped PR write identity, independent Python/Node acceptance tests, cancellation/recovery/fault injection, CI and cross-project benchmarks.
- Existing governance gates and local model isolation remain intact.

**Approved concise status statement:** "Dev Matrix v6 hardened scoped offline static-HTML Dev Operator is live on Dell and has passed independent Dell/Mac unit, browser and bounded security certification. Source is versioned on a dedicated release branch. Unrestricted general-purpose Dev autonomy remains out of scope."
