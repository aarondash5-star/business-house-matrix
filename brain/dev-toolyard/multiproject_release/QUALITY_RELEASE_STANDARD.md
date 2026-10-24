# Matrix Dev Tool Yard — Universal Quality & Release Contract (v0.2.1)

**Applies to every enrolled project and all future projects.** Source branch `feat/dev-toolyard-quality-gates-20261024`. Dell runtime: `0.2.1-quality-governed` (verified in `controller.py status`). This change is independent of Delulu and does not alter original brand files.

## Non-negotiable distinctions

- **TECHNICAL BUILD COMPLETE** means source generated, local runner passed and technical receipt exists. It is **not** evidence the brief has been achieved.
- **EVIDENCE READY** means all pinned artifacts for the project-specific quality contract were present and met the required evidence types. It remains a review request, **not approval**.
- **DESIGN/PRODUCT ACCEPTED** requires explicit owner decision against the frozen brief after viewing actual results.
- **RELEASE AUTHORIZED** requires a second, explicit deployment decision and the target platform/environment must be verified before promotion. The Tool Yard's local quality governor **never issues owner approval or releases**; deployment connectors outside the Tool Yard do not automatically inherit this control.

## Required stages before anyone claims design completion

1. Capture a *frozen decision contract*: source-of-truth URI, version, immutable sha256, goal, exact acceptance criteria, mandatory/optional scope, forbidden actions, target environment and revision log.
2. Translate approved goals into a typed `quality-contract.json`, including one criterion for each required `quality_gate.PROFILES[profile]` category. Owner must approve the contract. Changing requirements requires a versioned change, not agent discretion.
3. Execute in a project-isolated Tool Yard workspace. A passing `website_stage` or `dev_project_build` returns **technical only**.
4. Collect independent QA evidence: deterministic actual screenshots and frame observations for creative work, functional acceptance and negative tests for apps, retry/rollback receipts for automation, asset/rights/caption QA for media. Record source hashes, versions, viewport/sample/timing details, accessibility and performance evidence.
5. Obtain independent human design/product review **based on actual artifacts**. A text-only LLM critique does **not** count as visual inspection, manual approval or proof that production criteria were satisfied.
6. Run `python3 quality_gate.py check PROJECT MANIFEST` and inspect `quality_gate` in the controller's receipt. **Even if evidence is ready, the gate remains owner-review pending and release_authorized=false**.
7. Prepare deploy plan (target, auth/privacy, rollback, external spend, DNS, data). Ask owner to authorize specific deployment. For Vercel/Cloudflare/GitHub etc., validate **actual returned environment**, not just requested target; unexpected production target is a blocker to treating preview as private.
8. After deployment, independently verify actual browser, API/data where relevant, a mobile smoke test, accessibility and owner acceptance. Register significant source-verified changes centrally.

## Project contract schema

At `matrix-controller/quality-inbox/<project>/<manifest>/quality-contract.json` (mode 0600, parent private):

```json
{
  "schema_version": 1,
  "project": "my_project",
  "manifest": "site_v1",
  "profile": "creative_web",
  "brief_sha256": "64 lowercase hex SHA256 of approved brief",
  "criteria": [
    {"id":"brand_trace","kind":"brief_trace","acceptance":"Must match exact, version-pinned brand and owner decisions","required":true},
    {"id":"visual_check","kind":"visual_sequence","acceptance":"Inspect timestamped actual frames against approved storyboard","required":true},
    {"id":"responsive_check","kind":"responsive","acceptance":"Test representative phone, tablet and desktop sizes with no clipping","required":true},
    {"id":"a11y_check","kind":"accessibility","acceptance":"Test contrast, focus, reduced motion and accessible navigation","required":true},
    {"id":"independent_check","kind":"independent_review","acceptance":"Independent human review actual output and record deviations","required":true}
  ]
}
```

The corresponding `evidence.json` pins each criterion ID to a real artifact relative to an `artifacts/` root and its sha256, evidence reviewer type and test status. The quality governor rejects missing/wrong/cross-project/tampered artifacts. It never grants release rights based on self-reported JSON.

## Five mandatory profiles

- `creative_web`: trace, visual sequence, responsive, accessibility, independent human review.
- `functional_app`: trace, functional tests, security, independent human review.
- `automation`: trace, negative tests, recovery, independent human review.
- `media`: trace, sampled frames, asset fidelity, independent human review.
- `documentation`: trace, source checks, independent human review.

Contract adoption is required for all new owner-facing deliverables. Existing production projects are **grandfathered only for technical execution**, never for claiming design acceptance. Older completed receipts are displayed retrospectively as technical-only; historic database rows are not rewritten.

## Changes to production

- New `quality_gate.py` fail-closed independent artifact evaluator.
- Existing controller `receipt()`: adds separate `quality_gate`, `technical_only`, `design_complete=false`, `release_approved=false` to new successful build receipts across `website_stage`, `dev_project_build`, `dev_general_build`, `dev_scoped_build`, `pine_chat_stage`, `video_preview`.
- Existing controller `show()`: labels historic completed builds retrospectively with the same quality gate, without changing old records.
- Existing controller `status()`: surfaces `quality_policy` and marks governed tasks as not release authorized.
- Mandatory test suite: incomplete contract, no evidence, bogus human signoff, tampering, foreign project, executed receipt; original controller regression and installed source SHA.
- Backed up prior live controller in `release-backups/quality-gate-20261024T150651Z`; installer has guarded restart and rollback.

**Limitations requiring next release:** this is a Tool Yard receipt and workflow quality gate, not an in-band enforcement mechanism for arbitrary external deployments initiated outside Tool Yard. Verified signed owner approvals, platform-side preview target protection and a cross-provider publish policy must be integrated before any autonomous publishing is enabled. Never describe those future controls as already deployed.
