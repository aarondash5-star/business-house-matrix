# Golden Rule AW-1 — implementation and verification receipt

**Date:** 2026-10-22 IST
**Scope:** Reusable browser automation-owned window guard + existing Pine chat Playwright QA runner.
**Overall:** **SOURCE IMPLEMENTED / LOGIC TESTS PASS / NATIVE WINDOW TAG VISUAL CERTIFICATION BLOCKED**.

## Exact source

- Branch: `feature/aw1-visible-automation-tag-20261022`.
- [PR #10](https://github.com/aarondash5-star/business-house-matrix/pull/10), **ready for review**; **NOT merged** as of documentation. GitHub merge calls were blocked by connected-tool safety checks. Do not call this production `main`.
- `brain/automation/visible_window_tag.mjs`: creates only new disposable owned Playwright pages; project/worker/task/mode/state badge in Shadow DOM with high-contrast responsive style; `addInitScript` for reload; validates immutable lease metadata, task expiry, origin and exact offline file fixture; fails closed if badge hidden/removed/mismatched; rejects unknown manual pages, double writer, read-only mutation, production alerts/trading/shell/publishing; never blindly retries uncertain actions.
- `tests/aw1_visible_window_tag.test.mjs`: 13 no-network unit tests, positive and negative security cases.
- `prototypes/pine-mcp-chat/tests/ui-e2e.cjs`: existing 7-width synthetic Pine UX QA runner now creates guarded disposable contexts, wraps every click/fill/keyboard/screenshot with task tag verification and captures badge screenshot candidates at 320, 390, 768, 1440. **Actual Playwright browser-run not executed in this turn**, so reported checks count 70 is *planned*, not a passed native receipt.
- `.github/workflows/aw1-visible-tag.yml`: separate PR CI to syntax-check and run Node tests; repository-wide Matrix source validation remains independent.

## Verified source-level evidence

- GitHub [AW-1 workflow 39811168570](https://github.com/aarondash5-star/business-house-matrix/actions/runs/39811168570): **SUCCESS**, 13/13 tests (head `84033de3e07183b91d08d7c71270fecaf4334b2a`).
- GitHub [Matrix source validation 39811168543](https://github.com/aarondash5-star/business-house-matrix/actions/runs/39811168543): **SUCCESS**, `public-repository-safety` and `starter-tests` both passed.
- Fresh independent Mac Linux command `85ae808f-3563-4e83-883b-388dd3347106`, terminal **completed / exit 0**, fetched exact commit `84033de3e07183b91d08d7c71270fecaf4334b2a`, `node --check` and `node --test`: **13 tests PASS, 0 FAIL, 0 SKIP**.

## Native/production evidence boundary

- Mac `mac-linux` connected initially but `opera-agent-control.service` **inactive**, installed Opera controller tree **absent**, no graphical user session. Local isolated **Opera headless screenshot** task `df8b10e7-4f22-4c5a-8782-d37406b5077b` completed with browser timeout 124 and **no screenshot**. The next isolated Chrome screenshot task `4dbed1ed-6e52-4022-a207-31603db4001e` expired before starting, and a subsequent attempt reported Mac worker offline. **No visible-pixel native proof.**
- Dell `dell-linux` online for initial inventory but no active `DISPLAY` and no registered Chrome/Chromium binary in tested PATH. Live `bhm-autonomy-controller.service` source fingerprint had drifted to `ce09dabcc4037a401eb8df3617c375dad0ffddc3cd32e81df056e26317db29bd` from earlier certified hash. **Do not overwrite, restart or deploy tag code to it blindly**.
- Pine Manbir Windows worker online; TradingViewController READY, authenticated, `lease:null` during read-only inspection. Existing current controller does **not** have demonstrated AW-1 tag overlay or a verified overlay action. **No native TradingView chart edited and no new browser writer started.** Protected chart `/chart/JvxzE0Bg/` remains off limits.
- **No current Mac/Dell/Pine production automation window can be marked `VISUAL_TAG_VERIFIED` from these tests.** A unit test and a doc tag are not a screenshot.

## Release gate and follow-up

1. Resolve GitHub PR #10 merge tool block without bypassing account safety checks, read back merged commit and CI from `main`.
2. On a **uniquely identified disposable automation-owned browser window**, deploy the approved guard through the real installed controller. Preserve source hashes, backup and rollback, single-writer lease. Do not attach to personal browsing.
3. Capture a **native tagged screenshot** for desktop + 320/390/768/1440 widths where supported, verify tag visible through reload/navigation, new approved popup, observer recovery, session reconnect and after FINISHED. Assert absent on a manual tab.
4. Remove or hide the tag deliberately on a disposable automation-only window; verify **new GUI action blocked** before clicks; verify origin mismatch and task/lease mismatch deny. Test rollback and record terminal receipt.
5. Implement/pilot adapters for other actual runtimes (Linux Opera control, Mac native automation if present, Pine Manbir TradingView controller); **do not say global rule is enforced until each current runtime passes separately**.
6. Update Matrix [issue #9](https://github.com/aarondash5-star/business-house-matrix/issues/9) and the owner Master Registry with exact verified source/deployed versions. Golden Rule documentation is already adopted across repo instructions.

**Safety:** No browser profile, PIN, root permissions, Pine script/chart, broker, alerts, publication or paid resources were modified by this code exercise. The label is visual evidence only, not a tool permission or broker authorization.
