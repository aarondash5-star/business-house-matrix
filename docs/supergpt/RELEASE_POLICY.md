# SuperGPT — branch protection, promotion and rollback policy

**Adopted project workflow:** 2026-10-25. **Source:** [Canonical SuperGPT index](README.md). This is a release policy, not evidence that GitHub admin settings have been applied.

## Branches

| Branch | Purpose | Inbound changes | Required gate |
| --- | --- | --- | --- |
| `super-gpt/dev` | Development and current specification | Feature/fix PRs or owner-approved development commits | CI policy/static integrity |
| `super-gpt/test` | QA candidate | PR from `super-gpt/dev` **only** | CI policy and standalone Android build; QA executes after promotion |
| `super-gpt/production` | Owner-accepted release source | PR from `super-gpt/test` **only** | CI policy, Android build, independent QA evidence, owner acceptance |

Never merge straight from dev to production or from arbitrary topic branches into test/production. Promotion is performed through reviewed pull requests; no CI job in this repository automatically deploys, merges, signs or publishes. Production branch presence alone does not mean an Android release exists.

## Automated checks

1. [Release policy workflow](../../.github/workflows/supergpt-release-gates.yml) runs on SuperGPT PRs and branch pushes, checks canonical files and evidence JSON, and rejects PRs arriving from the wrong source branch.
2. For a PR into production, its policy job checks populated source/build/checksum, passed install, cold-start, crash scan and independent QA plus owner acceptance references. This is a **data validation check**; independently verify referenced evidence. Evidence text by itself cannot prove a test occurred.
3. [Android build workflow](../../.github/workflows/supergpt-android-debug.yml) runs on promotion PRs, checking standalone packaging and bundling. Its build does **not** replace live Android runtime QA.
4. Workflows use read-only repository permissions and must not auto-promote on a successful run.

## Required GitHub administrator settings — NOT automatically conferred by this file

Configure a repository ruleset or branch protections with targets `super-gpt/test` and `super-gpt/production`:
- Require a pull request; minimum **one approving review** from a permitted human reviewer.
- Require CODEOWNERS review and dismiss stale approvals when new commits arrive.
- Require status checks from the **actual exact job names** GitHub shows after a successful run: policy gate (`policy`) and Android build (`android-debug`); verify the exact reported context names in the UI before selecting.
- Block force pushes and deletions; restrict bypass and direct pushes, including administrator bypass as far as platform capabilities allow.
- Require branches to be current with their base or an equivalent tested merge commit.
- Require resolved review conversations.
- Set production deployment/environment approval separately if/when production jobs are added.

Protect `super-gpt/dev` from deletion and force pushes as well; require PR reviews where practical. Code ownership rules in `.github/CODEOWNERS` need platform protection to be mandatory. **Branch protection must be verified with a GitHub admin account; this connector may not have administration permission even if file write permission exists.** Until then policy checks are advisory for direct pushes, and enforced only as CI on PRs.

## Evidence and acceptance

Maintain [release candidate evidence](qa/RELEASE_EVIDENCE.json) and link actual terminal or Actions receipts. A passing CI build is only a build pass; a release candidate additionally requires:
- pinned/reproducible source and recorded APK digest;
- successful actual install + cold start + crash scan and basic interaction on Android, with QA receipts;
- vulnerability/license/privacy checks as appropriate to the candidate;
- independent QA review with reviewer and receipt link;
- owner acceptance referencing exact release candidate;
- rollback commit/tag, package version, signing and distribution decision.

Never invent missing evidence or copy an older artifact's ZIP digest into the field intended for the APK SHA-256.

## Promotion protocol

1. Development Brain prepares a candidate in `super-gpt/dev`; keep source commit and PR description.
2. Open PR `super-gpt/dev` → `super-gpt/test`. Run policy and Android build checks; QA tests the candidate after merge.
3. On `super-gpt/test`, record device tests, reviewed QA and owner decision in the evidence record. Re-run checks and avoid changes after signoff without repeating tests.
4. Open PR `super-gpt/test` → `super-gpt/production`. Both checks and owner-approved QA must pass; human merges only after review.
5. Sign, tag, distribute or deploy only on a **separately authorized** release action. Record terminal receipts and rollback.
6. On failure: stop promotion, file blocker, fix on dev, repeat test and evidence; never fake a green check.

## Rollback and emergency

Revert faulty changes with a reviewed PR and retain prior tagged signed artifacts/receipts. Emergency production remediation requires a separate owner-approved exception, recorded in the repo and with post-incident QA. Never delete a failing receipt or rewrite protected history just to make checks green.

## Current initialization note

Initial identical commits carrying **governance documents and CI configuration only** may be bootstrapped to all three branches so each destination already has its guard workflow. This initial sync is **not an application promotion, owner acceptance or deployment**. The initial QA evidence stays pending and cannot certify a production release. Active rulesets and admin enforcement must be checked independently after bootstrap.
