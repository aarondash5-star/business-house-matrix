# Dev Matrix v4/v5 — live controller autonomous coding certification

**Date:** 22 October 2026 (IST)  
**Scope:** Independent Business House Matrix public synthetic work only  
**Decision:** **CERTIFIED** for two *explicitly enrolled* offline model → isolated code patch → independent static-HTML QA → local unpublished Git review workflows, dispatched through the live Dell Matrix controller. **NOT CERTIFIED** for unrestricted/general-purpose multi-language project development.

## Source and release facts

- Controller at Dell `~/matrix-controller/controller.py`, active service `bhm-autonomy-controller.service`, v5 SHA256 **`df0cf3f968244d2e745d941f57d2225cfcd4a4147f55f7ce29c879e87027ffe4`**.
- Reviewed controller source: `brain/mvp-controller/controller-general-dev-v5-candidate-20261022.py` (commit `efb90a5b2ffc935cc2a5ce871f630ed604b34a0f`), changes scoped to exact manifest routing.
- Previous v4 controller SHA256 **`8d33ced5f9bebfa7eaa70bb2cd345ab63a983a48572d53e5e4b5fbea9fd74d1f`**, retained as rollback at `~/matrix-controller/controller.py.bak-20261022-generaldev-v5`.
- No root/sudo, SSH bridge/network/auth, production deployment, remote code push, spending or private Pine changes.
- The developer worker source is under `brain/dev-operator/`; fixed files installed to `~/matrix-controller/general-dev-release-v4` and `~/matrix-controller/general-dev-release-v5`, with independently compared checksums. Both remain no-tools/no-MCP/offline model inference, network/host-isolated workcell QA and unpublished local Git reviews.

## Controller-managed live end-to-end receipts

| Task | Controller UUID | Model attempts | QA | Local-only Git review SHA | Terminal state |
|---|---|---:|---|---|---|
| Release dashboard v4, `matrix-dev-dashboard-v4` | `ead38a98-dabf-43c2-8934-98b2a453ffe7` | 2 (first rejected, second accepted) | Semantic HTML QA PASS | `e618995f006ed4fdb13a02d31fa854ff1d4ee827` | `completed`, `manifest_enrolled_sandbox_qa` |
| QA checklist v5, `matrix-dev-qa-checklist-v5` | `a412a710-a197-400e-a992-811b2d4b5aa7` | 1 | Semantic HTML QA PASS | `57e5b47bb761e989ff1e96c7e862dacfa7a60396` | `completed`, `manifest_enrolled_sandbox_qa` |

- Both model outputs went through repo/project/file-path manifests, static content checks, independent Bubblewrap QA and verified actual `git rev-parse HEAD`. Both receipts record `published=false` and `pushed=false`.
- Live negative controller tests: attempts with foreign project rejected, unknown manifest rejected. Idempotency keys returned each existing task UUID rather than dispatching duplicates.
- Existing historical failures from v2 malformed JSON and v3 Qwen timeouts remain in the durable `needs_review` audit, without blind replay.
- Final Dell SQLite controller state **`completed=11`, `needs_review=11`**; live service active and no current worker required for completed tasks.
- Independently prequalified v4 policy/agent/workcell tests **28/28 PASS on Dell and 28/28 on Mac**; the new v5 registry/controller candidate selftest, independent static diff audit and 28/28 agent tests PASS on Dell.

## Mac cross-host certification gap

The Mac became offline/unresponsive via Generic SSH during v5 tests. Its pending v5 test receipt was **queued, not executed**. Therefore **v5 cross-host certification remains outstanding**. Do not report Mac as currently connected or v5 peer QA complete. Do not restart or change the Mac bridge, root, Wi-Fi, fans or other services without explicit separate authorization.

## What is not yet full general development autonomy?

The live route is still a *narrow, exact-manifest* coding lane; the two test artifacts are short synthetic static HTML. Remaining:
1. Independent owner-approved per-project enrollment and disposable source checkout, with broader approved file types/languages and protected credentials.
2. Safe model-controlled editing and bounded development tools **inside** the sandbox, with real multi-file/source-context workflows.
3. Independently certified Python and Node test profiles (current Node profile fails closed), web browser tests of generated output, dependency/CI and security QA.
4. Durable stop/cancel for running workers, recovery/fault injection and multijob concurrency limits.
5. Project-scoped authenticated GitHub PR publishing (no auto-merge), reusable source review and CI gates.
6. Reconnect Mac and complete the pending cross-host tests.

## Rollback

Before restoring a previous controller: verify no queued/delegated/dispatching tasks remain. Copy `controller.py.bak-20261022-generaldev-v5` over `controller.py`, restart only `bhm-autonomy-controller.service`, compare SHA against the v4 hash above; preserve receipts. This rollback is not executed by this document.

**Approved status wording:** **Dev Matrix bounded autonomous coding MVP operational across two enrolled task manifests, with two live controller E2E successes. General-purpose autonomous Dev Matrix remains a staged roadmap.**


## Independent Dell browser validation — completed after live E2E

- Host: `dell-linux`; Generic SSH development lane receipt **`0baffbe8-c501-4a20-ab4e-47a9eabf2677`**, exit 0.
- Existing Google Chrome binary `/usr/bin/google-chrome` launched through installed Playwright Node API; **no dependency or browser installed**.
- Both generated artifacts from **verified local Git review checkouts** checked at widths **320, 360, 390, 430, 768 and 1440**.
- **12/12 PASS**: semantic `main` present and visible, non-empty document language, viewport meta, no horizontal overflow, no page exceptions, **zero unexpected external network requests**. Browser requests were intercepted and non-local requests denied.
- Initial Playwright default cached browser launch failed due to absent requested Chromium build; deliberately reused installed system Chrome to complete the same test. This was a browser dependency path mismatch, **not a failure of the generated page**.
- This is a bounded headless runtime check, *not* a full visual-design/accessibility/security audit. External cross-host Mac v5 tests remain pending while Mac SSH heartbeat is offline.
