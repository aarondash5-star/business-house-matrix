# Main-account public GitHub runner — private WP Manager CI boundary

**Verified 8 Nov 2026:** Source-owner environment secret `DELULU_PRIVATE_TOKEN` was connected successfully; production source tests and scoped OAuth consent/isolation tests BOTH PASS on [GitHub Actions #42462288388](https://github.com/aarondash5-star/business-house-matrix/actions/runs/42462288388). Source commit `4bff39c2...` validated. **Original private-repo required-check parity and full OAuth consent workflow parity remain pending; no production deployment.**

**Cross-project reusable policy:** [Moksha Master Stack — Public CI runner / private source cost and security SOP (review PR #252)](https://github.com/karanzing1992/engagement-core/pull/252). Applies repo-by-repo only; this Business House Matrix public host is a pilot, not a shared credential grant for unrelated projects.

## Historical owner configuration (completed for this pilot; see latest verified state below)

1. Sign in to GitHub as `aarondash5-star`. In the **public** repository `aarondash5-star/business-house-matrix`, navigate to **Settings → Environments**: https://github.com/aarondash5-star/business-house-matrix/settings/environments.
2. Use the owner's newly created Environment named **`DELULUTECH_SOURCE_READ_TOKEN`**. This is an Environment name, not automatically an Actions secret.
3. **Default security recommendation for future adoptions:** Require selected branch only `ci/dlt-wpmanager-public-runner-20261108`. **Pilot exception:** the owner deliberately left this Environment unrestricted; per-workflow actor/ref controls remain but weaker, and this choice must not propagate to unrelated repos.
4. **Historical step superseded:** The successful Environment secret is **`DELULU_PRIVATE_TOKEN`**, not `DELULUTECH_SOURCE_READ_TOKEN` (which is only the Environment name). Its value must be a *valid, authorized and nonexpired* fine-grained GitHub token whose resource owner is `aarondash5-star`, repository selection only `delulutech`, permission **Contents: Read-only**, short expiration. The connected ChatGPT GitHub account's interactive access is not automatically an Actions token.
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

## Owner decision: unrestricted Environment, 8 Nov 2026

The owner explicitly chose **no GitHub Environment branch restrictions** and requested CI continue. The extra branch-policy API preflight was therefore removed from both test jobs. The source workflow still checks the exact public repository name, reviewed branch `ci/dlt-wpmanager-public-runner-20261108`, actor `aarondash5-star`, and `push`/manual-dispatch event. Public PRs continue to produce skipped token jobs. This is weaker than deployment-branch restrictions: a malicious or accidental future workflow change by an authorized public-repository writer could expose Environment credentials. Restrict repository write access, maintain PR reviews, keep token read-only and short-lived, and rotate it if it was accidentally made accessible elsewhere.

**Observed execution:** [main-account owner push run #42461819488](https://github.com/aarondash5-star/business-house-matrix/actions/runs/42461819488): both jobs started, no branch-policy block, but failed at `SOURCE_READ_DENIED`. Production job emitted `TOKEN_ACCOUNT_SOURCE_OWNER=false`, `SOURCE_REPOSITORY_READ=false`. The Environment secret was nonempty; checkout, source tests and builds did not run. No production mutations and no source data copied. **Status: AUTH_DENIED / FULL_CI_NO_GO.**

**Next manual owner action:** In the newly selected GitHub Environment `DELULUTECH_SOURCE_READ_TOKEN`, replace the **Environment secret of the same name** with an existing valid token that actually can access `aarondash5-star/delulutech` (`Contents: Read-only`). A token generated under another resource owner or restricted to the public repo will not work merely because its Environment is unrestricted. Do not paste it in GitHub comments or ChatGPT. If needed, verify resource owner and selected repository under `aarondash5-star` GitHub account token settings; tokens may be shown only at generation time.

## Verified source-owner token integration — 8 November 2026

**Current best evidence:** [Successful public-hosted private-source CI run #42462288388](https://github.com/aarondash5-star/business-house-matrix/actions/runs/42462288388), owner branch commit `3c0eed569e3344f9905353ef1f6d1ff1f0b2169d`, job receipts `128673963110` (production) and `128673963407` (OAuth isolation). **Both jobs completed SUCCESS**.

Actual action logs confirm `TOKEN_ACCOUNT_SOURCE_OWNER=true`, `SOURCE_REPOSITORY_READ=true`, successful checkout of private `aarondash5-star/delulutech` at exact SHA `4bff39c2acb868fad212d82c42ef4bd252041bea`, Node setup and the intended source test/build steps, and successful temporary source cleanup. The production job exercised PHP lint, connector build, npm test, native-platform/native-auth regressions, and Cloudflare Worker candidate bundles. The OAuth job exercised the selected access-boundary/consent tests. All GitHub Actions steps concluded success; no production deployment, private code publishing or public artifact upload.

**Important credential naming correction:** The owner created an Environment secret **`DELULU_PRIVATE_TOKEN`** within the Environment **`DELULUTECH_SOURCE_READ_TOKEN`**. Both workflow jobs now reference `secrets.DELULU_PRIVATE_TOKEN`. The earlier secret `DELULUTECH_SOURCE_READ_TOKEN` returned source access denied, and is NOT used by the successful workflow. Keep tokens confidential and rotate/revoke the unused old token if no other consumer requires it.

**Security decision:** Owner explicitly opted for an Environment with no deployment-branch restriction; code-level repository/branch/actor/event checks and PR skip guards remain. This is a known residual risk for a public repository: any actor who acquires sufficient repository write access to change executed workflow code may undermine those code-level guards. Prefer reducing authorized writers, requiring reviews, limiting token lifetime and revoking when unnecessary. No third-party PRs were given source token access in the verified run.

**Certification classification:** `MAIN_ACCOUNT_PUBLIC_RUNNER_FULL_SOURCE_PRODUCTION_TESTS_PASS`; `SCOPED_OAUTH_ISOLATION_PASS`; `ORIGINAL_SOURCE_REQUIRED_CHECK_PARITY_NOT_PROVEN`; `PRODUCTION_RELEASE_NO_GO`. The separate original source repo required status checks, original full OAuth Consent QA workflow parity, merge/release, and any live Google/Meta consent are NOT certified by this external successful run. The proof is a passing source test workflow, not production deployment.
