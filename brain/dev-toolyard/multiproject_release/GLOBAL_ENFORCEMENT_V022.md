# GLOBAL DEV TOOL YARD ENFORCEMENT v0.2.2 — LIVE DELL

**Release status:** independently verified live 24 Oct 2026. Dell controller `0.2.2-global-intake-governed`, authenticated service active. Previous controller preserved at `release-backups/global-gates-20261024T151735Z`. Code source branch: `feat/dev-toolyard-global-gates-v022-20261024`.

## Binding policy for ALL projects

- No new build/stage/isolated repair/video run without an **immutable quality contract**, its exact SHA-256-linked owner brief `brief.md`, and one matching owner-approved intake record. The owner-controlled ledger starts empty. An existing project registry enrollment grants a *route*, not authority to skip quality intake.
- The controller enforces `quality_admission.intake_check()` **at task submission and again immediately before queued dispatch**. Already completed records remain readable. Read-only research, proposals and isolated QA remain available under their existing permissions. Existing delegated tasks are not silently interrupted.
- Profiles are universal (`creative_web`, `functional_app`, `automation`, `media`, `documentation`). Required acceptance categories remain enforced by `quality_gate.py`; evidence must be hashed and tied to the approved brief.
- No AI-generated text, static smoke test or external model critique can declare the product visually complete. Actual browser/media evidence, independent human review and explicit owner acceptance remain separate required checkpoints.
- `quality_admission.py release-check PROJECT MANIFEST --platform ... --environment ... --artifact-sha256 ...` is a **deny-by-default preflight** for future Tool Yard-mediated publishing. It requires independent evidence and a distinct exact artifact/target/time-bound owner release record. It **never performs deployment**. No owner release approvals were enrolled on installation.
- If a brief, contract, evidence bundle, requested destination or artifact hash changes, intake or release preflight denies. No fallback to a different model, project, environment or permission route is allowed.
- The runtime does not add new root, paid API, auto-publish, cross-project reads, plugin credentials or direct cloud permissions. Existing production sites and old task records are unchanged.

## Owner-approved onboarding sequence

1. Confirm the **specific** project, manifest, revision and approved acceptance criteria with the owner.
2. Store a private `quality-inbox/<project>/<manifest>/brief.md`. Compute its SHA-256 and create `quality-contract.json` using the required five-profile criteria schema. Review all functional/creative promises before any coding.
3. Record an explicit owner-reviewed GitHub/registry approval reference and pinned `contract_sha256`, `brief_sha256`, profile, project and manifest in the private `owner-intake-approvals-v1.json`. This is an owner-managed ledger, **not a cryptographic attestation**; protect its write route.
4. Verify `quality_admission.py intake PROJECT MANIFEST --action ACTION` returns `approved_intake`. Submit scoped job through controller. Dispatch rechecks the same hashes.
5. After actual QA, populate evidence and conduct independent visual/product review. Owner reviews the built output. Evidence readiness is NOT owner approval.
6. Prepare a separate release record pinned to the precise artifact SHA, platform and environment, bounded expiry and explicit owner reference in `owner-release-approvals-v1.json`. Run the dedicated release-check. An authorized preflight is still not a deploy.
7. Deployment/publishing is a separate owner action and must verify the actual remote environment, access controls, output content and rollback.

## Regression and recovery

- `test_quality_admission.py` covers absent contract, missing owner approval, brief/contract tampering, wrong project, evidence absence, missing release approval, wrong platform/environment/hash and expired approval.
- `test_quality_gate.py` validates quality contract and evidence handling. Controller selftest exercises existing read-only flow, isolation, legacy blocked routes and failure on unapproved coding.
- Guarded installer `deploy_global_gates.py` checks exact previous controller SHA, tests an isolated patched copy, backs up the original, deploys/restores service, and automatically restores the controller on failure.
- Live receipt: `b2435440-59fb-48e4-bb5d-84e2613f228f`, exit 0. `status()` reports `prebuild_owner_admission_required=true`, `dispatch_revalidates_admission=true`, `release_preflight_required=true`, `external_connectors_mediated=false`.
- Historical task counts remained `completed: 13, delegated: 1, needs_review: 14` at deployment verification.
- **Important boundary:** External GitHub/Vercel/Cloudflare/WordPress plugin actions invoked directly outside the Tool Yard do NOT yet call this preflight and cannot be truthfully claimed globally blocked. Preventing bypass requires individually wrapping their publish controls and credential access. Until then, treat external publishing as separately owner-authorized; do not infer a Tool Yard preflight occurred.
- Policy does not guarantee creative excellence; it makes explicit promises, owner decisions and proof required before completion and release claims. It does not replace actual expert inspection.

## Do not silently weaken

Never create wildcard/all-project approvals, auto-approve owner ledgers, substitute source-only evidence for browser observation, or treat model reviews as human sign-off. Future amendments require independent regression + owner signoff + documented new version. The master stack record must cite the verified Dell runtime release, not simply Git code presence.
