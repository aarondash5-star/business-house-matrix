# Dev Matrix v6 — Gates A–C final certification evidence

**Date:** 2026-10-22 (Asia/Kolkata)
**Project:** Independent Business House Matrix; not Moksha Master
**Release scope:** enrolled offline static-HTML coding only
**Execution:** user explicitly authorized Gates A–C; subsequent user instructed "Document and deploy".
**Outcome:** A/B/C PASS, within bounded scope. Existing Dell v6 deployment confirmed active; no configuration/root/network/permission change.

## Gate A — Source, controller, peer tests

- Live Dell controller: `~/matrix-controller/controller.py`, SHA256 `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`; matches v6 candidate source at `e1d97ba35ff74c5446126891d8f56e54ac42c975`.
- Dell existing user service `bhm-autonomy-controller.service`: **active/running** (checked with `systemctl --user`). System-level service is separate/inactive.
- Dell and Mac clean QA checkouts: same Git commit `e1d97ba35ff74c5446126891d8f56e54ac42c975`; matching policy SHA256 `fd239a658ccd4d317cc2a895c1d64eec712d987b2ff5dbbf8d30da7a72f887ce` and agent SHA256 `c8f67820b1bc216f18a662d9248f790d25e37369d2fd42cde9002ec7578ff5b8`.
- Full v6 source/sandbox/unit suite: **Dell 38/38 PASS** (terminal receipt `13fde928-00aa-412f-9218-90f775a65082`, exit 0); **Mac 38/38 PASS** (terminal receipt `99739f00-b4b7-4604-806f-22ff9f4d1934`, exit 0).
- Both authenticated SSH hosts were online; control, operations, and development lane heartbeats present. Direct read-only terminal commands succeeded on both.
- Current task queue read through SQLite read-only: `completed=12`, `needs_review=11`; no pending/inflight entry reported. Do not replay historical failures.

## Gate B — Isolated real-browser check of newly generated v6 artifact

- Source: `~/matrix-controller/release-stage-general-dev-20261022/runs/matrix-dev-security-v6/local-review/frontend/dev-release-security-v6.html`.
- Verified local Git review commit: `2b70a5994400f4dda02cebb7a9e233691f1233d8`; unpublished, unpushed.
- Existing Dell `/usr/bin/google-chrome` v155 with previously installed Playwright (`~/moksha-browser/node_modules/playwright`). **No installs** or new browser dependencies.
- **6/6 PASS** at `320`, `360`, `390`, `430`, `768`, `1440` CSS px; expected visible `main`, body text, HTML5 doctype, language, viewport meta, no horizontal overflow, no JavaScript page/console errors; external browser requests intercepted/blocked and **zero unexpected requests** observed.
- Browser receipt `bbdf5259-1aa8-4576-bb6d-a7d55ac29b17`, exit 0.
- This test did not claim a complete human visual, WCAG/accessibility, or penetration assessment. An earlier 7/7 v6 viewport record exists in `docs/receipts/DEV_OPERATOR_V6_FULL_RELEASE_QA_20261022.md`; this report records the independently rerun 6/6 subset without conflating the two receipts.

## Gate C — Cross-host adversarial policy checks

- Read directly from the same independently verified `static_html_policy.py` on both hosts, without changing source or policy.
- 37 expected-rejection cases covering script/iframe/object/embed, SVG/MathML/foreignObject, event handlers, URL-bearing elements and attributes, entity decoding, CSS url/import/escape/image-set, meta-refresh, duplicate attributes, unbalanced/malformed HTML, unsafe declarations, no-value events, plus 2 safe positive controls.
- **Dell 39/39 PASS**, terminal receipt `57bbc096-e5fa-44e1-82dd-ea013db0d3b3`, exit 0.
- **Mac 39/39 PASS**, terminal receipt `487a308f-8112-475b-a206-c7e60b9c7e97`, exit 0.
- This is a bounded adversarial regression corpus, **not** a proof of all possible XSS/HTML parsing behavior.

## Pre-release preservation audit

- Live v6 controller SHA unchanged after tests.
- Rollback `controller.py.bak-20261022-static-security-v6`: SHA256 `df0cf3f968244d2e745d941f57d2225cfcd4a4147f55f7ce29c879e87027ffe4`, matching prior **v5** live controller.
- Important: `controller.py.bak-20261022-generaldev-v5` SHA256 `8d33ced5f9bebfa7eaa70bb2cd345ab63a983a48572d53e5e4b5fbea9fd74d1f` is the **v4** controller snapshot from the v5 cutover. Use the specifically named v6 pre-promotion backup for any v6 rollback assessment.
- Original v6 run receipt SHA256 `eef95251c1c05cc8671fd717bf0d6fd41389e41a2390705e8cad20570f5c2d27`; existing local commit remains intact.
- Both source checkouts remained clean; no user service restart, root changes, permissions, installs, controller replacement, model change, remote generated-code publication, or spending.
- No hosted GitHub Actions CI statuses returned for inspected source commit; **do not claim hosted CI passed**.

## Release governance / limits

- Existing `release/dev-operator-scoped-v6-security-20261022` branch is the versioned source-release channel, distinct from unmerged `main`, previous v5 release, and original draft PR #8. Release branch fast-forwarded non-force from `ce2c6dbe7042c011f34c99a468fa0ade4bffc511` to `974ab04b45219e202672a468261bdbfba0f3a850`; that final update supplied documentation only beyond tested source.
- GitHub `main` had materially diverged (93 hotfix commits ahead, 107 main commits ahead at audit). No unsafe wholesale merge of unrelated source or draft PR #8.
- Previous v5 validator had serious fail-open bugs; restoring v5 is an **incident-only**, separately authorized rollback after stopping submissions, draining queues, and reviewing exposure. Do not use v5 on untrusted generated HTML without restoring the security fix.
- Full general-purpose development agent, broad tool invocation, CI, project enrollment beyond the explicit manifests, GitHub PR writing by agents, production publishing and spend remain **NOT CERTIFIED/NOT AUTHORIZED**.

**Scope-limited verdict:** Dev Matrix **v6 hardened static-HTML offline coding release PASS** for Gates A–C; Dell service already deployed and independently reverified. No full general-purpose-autonomy claim.
