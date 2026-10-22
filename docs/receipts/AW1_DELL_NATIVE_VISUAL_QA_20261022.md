# AW-1 — native Chromium visible-tag certification on Dell (disposable browser)

**Date:** 2026-10-22 IST  
**Status:** **PASS — isolated native-browser AW-1 tag display**, **NOT a live-controller rollout**.

## Scope and source

- Reuses the merged AW-1 guard `brain/automation/visible_window_tag.mjs` from Matrix `main`, prior PR #10 merge `cd764b750ae3fb25d5c30e52b645634cfece8f2a`.
- New repeatable standalone native test: `tests/aw1_native_visual_qa.mjs`, commit `0fa5417b669d298701c34161936a89d09bf44ee4`.
- Dell worker `dell-linux`, x86_64 Linux, Chromium binary `/opt/google/chrome/google-chrome`, running as SSH worker with an **isolated disposable headless browser profile**; local file:// fixture only, no network websites, no CDP attachment to any user browser or TradingView.
- Source download receipt `b2eb6b25-f643-4214-a32f-421d9377f384`, command terminal completed exit 0. Full four-width test `da386f35-be21-488d-b261-d2a69935b0c1`, terminal **completed / exit 0**. Native-image SHA receipt `781ad8cb-cdc9-4be5-a08f-42bed8f4618c` exit 0.
- Installed Chromium executed separately for DOM content with measured CSS visibility and the screenshot. It verified exact text `AUTOMATION | PINE-QA | DELL | AW1-TEST-ONLY | READ-ONLY | RUNNING`.

## Actual native output

| Width | Screenshot dimensions | Computed visible | Exact identity | PNG bytes | PNG SHA256 |
|---|---|---|---|---:|---|
| 320 | 320×850 | PASS | PASS | 23,308 | `8b9a05cb1da6237c283a811605c8ef83fd36431c01637062aa0e3de91ec721ab` |
| 390 | 390×850 | PASS | PASS | 24,346 | `f62be62fad8ba6210986c629831a2366153243b1dc9e641cc7a1dd0461f6eeea` |
| 768 | 768×850 | PASS | PASS | 26,173 | `4f6d901a68327ba6c824e929606f10a09368b232395e20a5c2567f1a6a65e48a` |
| 1440 | 1440×850 | PASS | PASS | 28,684 | `9a55b80a7d18ed9d4f4b545091be80f82e4108b86d62804d1d24ff3a990c1d22` |

Screenshots are retained **on Dell** in `/tmp/aw1-native-visual-disposable-20261022/aw1-tag-<width>.png` and not copied into public Git. A top-cropped 390 screenshot was independently retrieved and visually inspected, confirming readable white lettering, dark pill/strip and correct project/worker/task/mode/state. Do not mistake the test fixture's synthetic `AW1-TEST-ONLY` ID for an actual live lease.

## Companion logic evidence

- AW-1 Github Actions [run 39811168570](https://github.com/aarondash5-star/business-house-matrix/actions/runs/39811168570): **13/13 PASS** on the source commit, including tag removal, wrong/missing lease, read-only action denial, one writer, cross-site URL rejection, FINISHED state and post-action ambiguity; later source was squash-merged into `main`.
- Connected Mac read-only Node test receipt `85ae808f-3563-4e83-883b-388dd3347106`: **13/13 PASS**, exit 0. (That Mac did **not** host the documented Opera control service.)
- This page was rendered through the standalone isolated test script, **not through the deployed Matrix coding service or the Pine Manbir Windows controller**. Those user-facing GUI endpoints are distinct.

## Remaining deployment gates

1. **Dell Matrix runtime:** deployed `~/matrix-controller/controller.py` SHA drifted under another concurrent worker; last observed `df0cf3f968244d2e745d941f57d2225cfcd4a4147f55f7ce29c879e87027ffe4`, service active. Verify authoritative identity, add AW1 to its real browser launch/action dispatch only on owned sessions, preserve backups and retest; don't overwrite concurrent edits.
2. **Mac Opera:** connected `mac-linux` lacks the previously documented `opera-agent-control.service` and extension runtime, so source tag cannot be hot-installed there. Identify actual active Opera controller host and extension before installation; never create duplicate workers or relabel manual user windows.
3. **Pine Manbir Windows:** `tvcontroller status` READY, authenticated, CDP, `lease:null` in a read-only check. Add/verify a tag only through the authorized existing TradingView Controller against a disposable layout, and demonstrate screenshot, owner/tab integrity, missing-tag rejection and exact rollback. Protected `/chart/JvxzE0Bg/` cannot be touched.
4. **Native negative UI checks:** beyond the 13 unit tests, show removal/mismatch fail-closed in a real browser during an attempted automation command; verify overlay persists through site navigation/reload, completion and reconnect and is absent in manual sessions.
5. Retain **NOT CERTIFIED** for any target runtime without its own source/deployment/visual/denial receipts. No new production browser writers, brokers, alerts, trading, scripts or PIN changes authorized by this fixture test.

**Overall:** native display certified for Dell *disposable Chromium test only*; production fleet AW-1 universal enforcement remains **PARTIAL**.
