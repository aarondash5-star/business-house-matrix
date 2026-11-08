# Main-account public GitHub runner — private WP Manager CI boundary

**Status:** Workflow prepared in draft PR #45. **Private full-source checks are NOT certified until GitHub Environment credentials are configured and both jobs pass.** No production deployment.

## Owner configuration (required one time)

1. Sign in to GitHub as `aarondash5-star`. In the **public** repository `aarondash5-star/business-house-matrix`, navigate to **Settings → Environments**: https://github.com/aarondash5-star/business-house-matrix/settings/environments.
2. Use the owner's newly created Environment named **`DELULUTECH_SOURCE_READ_TOKEN`**. This is an Environment name, not automatically an Actions secret.
3. Under **Deployment branches and tags**, choose **Selected branches and tags** and allow **only** `ci/dlt-wpmanager-public-runner-20261108`. Do not authorize `main`, wildcards or pull-request heads. Optional: require a trusted reviewer, but ensure the runner can run after approval.
4. Within that specific Environment (not in repository-wide Actions secrets), add or update an **Environment secret** exactly named **`DELULUTECH_SOURCE_READ_TOKEN`**. Its value must be a *valid, authorized and nonexpired* fine-grained GitHub token whose resource owner is `aarondash5-star`, repository selection only `delulutech`, permission **Contents: Read-only**, short expiration. The connected ChatGPT GitHub account's interactive access is not automatically an Actions token.
5. Never paste the token into chats, issue comments, commits or CI logs. Do not transfer credentials from `karanzing1992/Matrix-House`; that account is a separate runner and has unrelated credential scope.
6. Once the environment and secret are saved, trigger the owner-controlled branch's `.github/workflows/dlt-main-private-source-cert.yml` workflow via a reviewed push to that branch (or a manual dispatch with branch selected if GitHub exposes it). Check **two** jobs: `Pinned WP Manager production QA - private checkout` and `Pinned WP Manager OAuth consent and isolation - private checkout`.
7. Record the exact GitHub Actions run link and verify source pin `4bff39c2acb868fad212d82c42ef4bd252041bea`, all step results, sanitized test summaries and the no-deploy gate. Any source update requires owner-reviewed exact new SHA pin and independent re-run.

## What can and cannot run

**Only** a push or manual dispatch on `ci/dlt-wpmanager-public-runner-20261108` by `aarondash5-star` is eligible for private-source jobs. Pull requests (including forks) **never execute secret-bearing jobs**. The secret belongs to an environment with explicit branch restrictions, not the general public repository.

Jobs fail closed if the environment token is missing, invalid or lacks private source access. Source checkout uses pinned `actions/checkout`, immutable SHA and `persist-credentials:false`. Runner directories and private test log files are removed, even on failure. There is no artifact upload, dependency cache, source mirroring, deployment, real Google/Meta call or customer data operation. Only PASS/FAIL test markers and a reviewed source SHA appear in public GitHub logs and step summaries.

**Production validation** mirrors the original WP Manager production-check job's PHP lint, native connector build, NPM suite, wide native-auth/platform Node regression selection, and both Worker compilation/syntax/legacy dependency checks. It intentionally withholds source and full test-output logs from the public account and does not publish candidate Worker artifacts.

**OAuth consent/access-boundary job** is a scoped set of source tests. It is **not** equivalent to every test in the original `WP Manager 2.0 OAuth Consent QA` workflow until exact original job parity is independently compared and verified. Do not mark original required checks green, lower branch protection, merge private source PR #57 or release any central OAuth/Meta integration because the public CI canary passed.

## Source and linked work

- [Original private WP Manager source PR #57](https://github.com/aarondash5-star/delulutech/pull/57), pinned candidate `4bff39c2acb868fad212d82c42ef4bd252041bea`.
- [Public runner draft PR #45](https://github.com/aarondash5-star/business-house-matrix/pull/45).
- [Independent synthetic public runner PASS #42454928679](https://github.com/aarondash5-star/business-house-matrix/actions/runs/42454928679): upstream package audit/PKCE/JWT checks only; this does not exercise the private source.
- [Private external Central OAuth source mirror PR #6](https://github.com/karanzing1992/Matrix-House/pull/6) (a different isolated account/workstream).

**Open-source/reuse/cost:** GitHub Actions hosted runner and existing `actions/checkout` and `setup-node`, Node test runner, `@cloudflare/workers-oauth-provider@1.2.4`, `jose@6.1.0`, `esbuild@0.25.12`; no new paid service, data broker or custom runner. Private read-only source token is the only new access requirement. Existing security and ownership controls remain binding.

## Verified follow-up: 8 November 2026 — new Environment selected, safe-block verified

The owner's newly created public-repository Environment `DELULUTECH_SOURCE_READ_TOKEN` exists, but the GitHub API returned `deployment_branch_policy: null` (no selected-branch restriction). Two isolated jobs now explicitly target that Environment, both run a **pre-secret public API branch-policy check** and require exactly one custom branch policy for `ci/dlt-wpmanager-public-runner-20261108` before the secret-read step can execute.

The controlled [branch push run #42461451517](https://github.com/aarondash5-star/business-house-matrix/actions/runs/42461451517) confirmed BOTH jobs failed at `Verify public-repo environment is restricted to this owner branch` and skipped token validation, private source checkout and tests. PR-triggered runs still skip both secret-bearing jobs. **No private source/test bytes were accessed or emitted in this run.** Source remains private. The user must select the exact branch in the new Environment's deployment branch settings, and make sure an Environment secret `DELULUTECH_SOURCE_READ_TOKEN` exists inside it with a fine-grained `aarondash5-star` source-owner token, only `delulutech`, Contents: Read-only. After the owner has saved both controls, trigger one new owner branch run and inspect actual job receipts. No build certification or production release is claimed yet.
