# Business House Matrix — AI Agent Operating Defaults

This repository has live Matrix systems on Dell/Mac and public source for Pine chat prototypes. A Git commit is **not** a live deployment.

## Golden Rule AW-1: Persistent visible tag in every automation window

**Owner default, effective 2026-10-22:** Each automation-owned browser tab/window, desktop/remote GUI window or terminal must show a persistent and human-readable `AUTOMATION | PROJECT | WORKER | TASK-ID | MODE | STATE` tag. It must be visible before any automated GUI action and in screenshots, persist through navigation and reconnect, and match the verified single-writer task receipt.

- **Ownership first:** identify the task lease, exact automation-owned tab/window, allowed origin and worker. Never inject a tag into an ordinary/manual browser session or unknown Pine chart.
- **Fail closed:** if absent, obscured, stale or mismatched, set `BLOCKED:UNLABELED_WINDOW`; stop new clicks, keystrokes, fill, scroll and navigation until exact owned window is reacquired and tag is visible. Continue safe read-only diagnostics only.
- **Privacy:** no PINs, OTP, passwords, keys, cookies, customer identifiers, sensitive source, financial or chart data in tags.
- **Mode:** READ-ONLY / EDIT-QA / STAGING and READY / RUNNING / PAUSED / BLOCKED / FINISHED must reflect actual permissions and task state. Never use the label to elevate permissions.
- **Default policy, not deployed proof:** every new GUI automation implementation must implement the tag and test at 320/390/768 pixels, reload/navigation, manual-tab noninterference and forced missing-label denial; existing Dell/Mac/native Windows runtime requires authorized staged installation, backup/rollback and a fresh tagged screenshot before `VISUAL_TAG_VERIFIED`.

Full canonical policy: https://github.com/karanzing1992/engagement-core/blob/main/docs/AUTOMATION_VISIBLE_WINDOW_TAG_GOLDEN_RULE_20261022.md

## Other standing rules

Reuse working existing implementations before creating replacements; keep private Pine source and protected TradingView charts outside Matrix public code and browser adapters; no uncontrolled native GUI write tools, public publishing, spending, broker actions, production alerts or live trading. Use signed source identity, narrow scope, single-writer receipts and explicit evidence for claims. Do not promote Pine Gold Phase 3 to CERTIFIED while gates remain unverified.
