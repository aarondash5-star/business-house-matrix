# DeluluTech WP Manager private CI check reconciliation — 8 November 2026

**Owner authorization:** finish missing WP Manager OAuth Consent QA coverage using existing public GitHub Actions host, retain private source and no production deployment.

**Status:** EXTERNAL QA PARITY VERIFIED FOR ALL APPLICABLE TEST EXECUTION; ORIGINAL PRIVATE ACTIONS CHECK CONTEXTS REMAIN FAILED. **DO NOT MERGE SOURCE PR #57 OR RELEASE PRODUCTION** until original protections, independent review and live Google owner consent are satisfied.

## Reproducible identity and evidence

- Private owning repository: `aarondash5-star/delulutech`, draft [source PR #57](https://github.com/aarondash5-star/delulutech/pull/57), head SHA `4bff39c2acb868fad212d82c42ef4bd252041bea`, target `production/wp-manager`.
- Exact original workflows read from pinned private SHA:
  - `.github/workflows/wp-manager-production-checks.yml`, blob `9a1df0042cca67715d3bd1150fdc45897dac49ba`.
  - `.github/workflows/wp-manager-2-0-oauth-consent-qa.yml`, blob `58abce572ab7e3bb3fb8bb7cf5495623afeb7ebd`.
- Public standard GitHub-hosted runner: `aarondash5-star/business-house-matrix`, owner-only reviewed CI branch `ci/dlt-wpmanager-public-runner-20261108`, draft PR #45.
- GitHub Environment **name** `DELULUTECH_SOURCE_READ_TOKEN`. Actual used Environment secret **name** `DELULU_PRIVATE_TOKEN`. Its value never printed, copied to Git or documented. Credential confirmed source-owner identity and private source read access; source checked out with `persist-credentials:false`. The owner expressly left the Environment unrestricted; this is a temporary risk-accepted exception, not the reusable secure default.
- Original external production CI execution: [run #42462288388](https://github.com/aarondash5-star/business-house-matrix/actions/runs/42462288388), job `128673963110` **SUCCESS**, source SHA verified. Production suite covers PHP lint, connector, npm test, native auth/platform regressions, both Cloudflare production candidates, syntax and legacy dependency checks; no bundle upload.
- Original OAuth Consent QA executable parity: [run #42464447351](https://github.com/aarondash5-star/business-house-matrix/actions/runs/42464447351). All three applicable separate job executions **SUCCESS**, not merely a partial synthetic canary.

## Exact consent workflow job parity matrix

| Original job | External public-runner job | Result and retained steps |
|---|---|---|
| `consent-assets-and-tests` | `consent-assets-and-tests` / job `128680587635` | **PASS**: Node22; `npm ci`; consent.mjs JS syntax; `npm test`; connector PHP syntax; native-platform D1/vault tests; esbuild + wrangler 4.47.0; `cloudflare/build-assets.mjs`; native Worker bundle/syntax; public-smoke syntax; **local workerd `smoke-native.mjs`** |
| `legacy-preview-test-baseline` | `legacy-preview-test-baseline` / job `128680587399` | **PASS**: isolated `chatgpt-app` Node22 lockfile install and its independent `npm test` |
| `native-cloudflare-oauth-v2-build` | `native-cloudflare-oauth-v2-build` / job `128680587724` | **PASS**: Node22; npm ci; esbuild and Cloudflare OAuth provider 1.2.4; both auth/resource bundles; JS checks; original Supabase endpoint denylist; five original native-auth isolation/consent regression tests |
| `live-staging-public-http-qa` | Not applicable to source PR #57 | **Original conditional skip, expected.** GitHub workflow expressly requires `pull_request.number == 10` and same source repository. This is not a missing test for PR #57; no live staging claims are made. |

**Safe public-runner deviations:** The original private workflow prints full base64 Worker bundle bytes to Actions logs and uploads three compiled artifacts. The external public workflow deliberately **does not print bundle bytes, upload private artifacts or cache private source/dependencies**; it performs equivalent compilation and syntax/functional tests. Thus **functional test coverage parity is verified for eligible jobs**, while **full original workflow output/artifact parity is intentionally NOT provided** and must not be represented as byte-for-byte workflow parity.

Each job uses isolated checkout of the exact pinned SHA, passes minimal GitHub permissions, runs only on an owner-controlled approved branch and push, suppresses private test output in public logs, removes source and temporary test logs, and cannot deploy live infrastructure. Any test failure stops the job and produces a sanitized failure marker; no masking by CI pass.

## Original source repository checks remain outstanding

At the **same exact source PR head SHA**, original GitHub Actions runs continue to show **FAILURE**, and their historic logs are unavailable:

- [WP Manager 2.0 OAuth Consent QA — private run #42404634487](https://github.com/aarondash5-star/delulutech/actions/runs/42404634487), original three eligible jobs recorded failure and staging job skipped.
- [WP Manager production checks — private run #42404634489](https://github.com/aarondash5-star/delulutech/actions/runs/42404634489), original production validation recorded failure.
- Public-runner external success **does not change these source-repo GitHub Actions CheckRun objects or required status-check context conclusions**. It is prohibited to forge a check, suppress a required status, merge by bypass, or treat external job names as official source GitHub Actions checks.
- Attempt to inspect source `production/wp-manager` branch rules through private read-only CI token returned `SOURCE_BRANCH_RULES_API=UNAVAILABLE_WITH_READONLY_TOKEN`; formal ruleset/branch protection required-check list is **unverified**. Rules that cannot be inspected must not be deemed absent. Owner may inspect in source-repo Settings → Branches / Rules → Rulesets.
- Do not rerun private-account hosted CI merely to obtain a green badge until current private-hosted GitHub Actions allowance/billing and one-time cost are verified; user requested avoid unnecessary private chargeable quota. If owner approves one source Actions run for an immutable check context, run once with receipts, preserve protections. Alternatively a separately enrolled, isolated and safe self-hosted runner may avoid private hosted compute, subject to current GitHub billing terms and runner credentials. Never enroll a shared Dell/Mac dev yard without separate security review.

## Production and merge gates still NOT satisfied

Source PR #57 is a **release-disabled Google OIDC / central OAuth source candidate**, not a completed production authorization service. Google client registration/consent, real OAuth issuer/audience/redirect on staging, secret bindings, Meta/WACRM tenant authorization and owner release acceptance remain separate gates. No Google/Meta live auth, message send, credential change, deployment, DNS, production branch merge or source branch protections changed by external CI.

Public PR #45 is CI infrastructure only. It must be reviewed for public repository trust and its unrestricted GitHub Environment risk before any merge; no production effects are authorized merely by testing.

## Hygiene, cost and rollback

- Use a **short-lived fine-grained source repository Contents:read** token; never share with other venture accounts. The old unused `DELULUTECH_SOURCE_READ_TOKEN` **secret name** in earlier workflows may have consumers; do not blindly revoke without auditing all workflows. The effective current secret is `DELULU_PRIVATE_TOKEN`, not the Environment name.
- Limit GitHub public CI repo writers, ideally enforce review + GitHub Environment branch allowlist. Current unrestricted Environment is a **documented owner exception with residual exfiltration risk if an authorized writer changes workflow code**. Branch code `if` guards alone are not a substitute for Environment/branch restrictions.
- Standard public GitHub-hosted runner compute is generally free; private hosted Actions may be billable after plan quota, and larger public runners/storage/services may still incur cost. Cross-account token access requires exact source authorization. See [Master cross-project free-first SOP PR #252](https://github.com/karanzing1992/engagement-core/pull/252).
- Rollback: revoke the public CI Environment secret; disable/delete only this isolated public-runner CI branch/workflows after owner review, preserving original private GitHub workflows unchanged. Source branch PR #57 and live WP Manager service remain unaffected.
- Source status of this record is **CI_VERIFIED_EXTERNALLY / SOURCE_CHECKS_RED / NO_PRODUCTION_DEPLOYMENT / RELEASE_NO_GO**. Do not claim `FULLY_SYNCED` until Master GitHub source, canonical doc, consumer skills and independent live release gates are verified.
