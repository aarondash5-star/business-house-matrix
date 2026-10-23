# Unified Dev Matrix — owner authorization and certification receipt (23 October 2026)

**Owner instruction:** "Authorise and then certify."

**Decision:** Owner task authorization **RECORDED**. General-purpose candidate **PARTIALLY VERIFIED, PRODUCTION/GENERAL-AUTONOMY CERTIFICATION NO-GO**. Do not confuse user permission with the platform's separate connector security clearance.

## Actor, project and isolation

- Owner-authorized Super Brain used existing Generic Linux SSH operations transport to evaluate a development **candidate** on Dell, separate from certified v6.
- Candidate source: `feat/dev-universal-dynamic-intake-20261023`, pinned at tested **`79c26498c99100370ba54f07a15710a82e2e4933`**.
- Certified v6 Dell controller remains active, unchanged SHA256 **`b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`**. Retired old proposal-only Dev Brain process remains stopped. No changes to production permissions, ssh daemon, plugins, root, payment/PMS, CI, public publishing or current SearXNG.
- Mac worker offline at preflight, independent Mac peer QA remains OPEN.

## Verified achievements with exact terminal receipts

1. **Current post-fix dynamic-intake negative suite: PASS 16/16.** Candidate checkout was updated to `a8aba572...` after owner's renewed authorization (source receipt `b0b35b4b-58e8-4b81-b8e3-5a13289861e6`). Unit negative tests cover signed dynamic intake, forged-request denial, bad repository owners/paths, pinned image/trusted QA requirement, idempotency, duplicate/replay protection, atomic claim, orphan quarantine and offline guest configuration. Terminal `9653293e-5563-4d98-9ac6-c9bbbc0f189b`, exit 0.
2. **False-finish/real source-change proof added.** Candidate `universal_dev_dispatch.py` now checks pinned HEAD/origin, actual tracked/untracked file modifications, protected test hashes, disallows symlinks/overlarge changes, fingerprints source files, and rejects model no-ops before `review_ready`. Git metadata additionally overmounted read-only in isolated Podman worker.
3. **Persistent offline regression tests added.** `tests/test_universal_dev_dispatch.py` covers correct signed intake, malformed scope, immutable trusted tests, no-op rejection, real synthetic diff, source/remote tampering, crash recovery, mock job lifecycle, readonly git metadata argv. **13/13 PASS** on Dell at pinned candidate `ed6a1bbd2d03c6cdd63e7844f6501e2f09feef7e`; terminal `9b3d457f-1ea4-47d0-b3d0-f3c60902fcca`, exit 0.
4. **Rootless workcell engine environment patched.** First actual Podman isolated file-edit smoke failed with `stat : no such file or directory` due to empty engine runtime/storage environment values, terminal `78935621-db62-4b48-a21c-ee1c11a61ff4`, exit 2. Code patched to preserve rootless engine's host-only context without passing it into the guest, commit `79c26498...`.
5. **Latest candidate branch regression: PASS 13/13** at exact `79c26498...`; terminal `010ada70-d173-4ce0-9a95-1d57568d687b`, exit 0. v6 service still active.
6. **Actual rootless Podman guest remains FAILED.** On updated `79c26498...`, model workcell smoke attempting to write only a disposable fixture `app.py` via pinned local Python digest timed out, returned `GUEST_EDIT 124 workcell_timeout`. Terminal `821cd00d-19be-498a-8f87-125ef646d094`, exit 2. Therefore readonly Git metadata and independent QA were **not reached in that real guest smoke**, irrespective of passing mocked unit tests.
7. **Container state/host continuity checked.** Read-only Podman diagnostics confirmed Podman 4.9.3, rootless=true, pinned Python image digest exists, and the only listed running container was the preexisting SearXNG container, not a test artifact. Diagnostic warning was `Found incomplete layer ..., deleting it`, **suspected not proven** to explain Podman timeout. Terminal `5268aaaf-542f-4509-8453-83fc7833523c`, exit 0. v6 checksum unchanged.

## Certification table

| Gate | Result |
| --- | --- |
| Owner authorization for staged upgrade and evaluation | RECORDED |
| Existing authenticated Dell SSH route | PASS |
| Dynamic signed intake validation and security unit checks | PASS 16/16 |
| Source-change proof and simulated lifecycle regression | PASS 13/13 |
| Actual disposable rootless OCI runtime executing code | **FAIL: timeout** |
| Real protected Git-metadata mount enforcement | NOT TESTED END-TO-END |
| Real independent guest tests after model edit | NOT TESTED END-TO-END |
| Genuine autonomous external project Python/Node/Andaz coding | NOT CERTIFIED |
| Authenticated unified Brain CLI/ingress | NOT DEPLOYED; previously blocked by tool safety checks |
| Mac independent QA | BLOCKED: offline |
| Project-scoped GitHub PR/review identity | NOT CERTIFIED |
| Canary, rollback and production cutover | NOT PERFORMED |
| Existing certified v6 service | ACTIVE, PRESERVED |
| **Unified Dev Brain release** | **NO-GO** |

## Next safe execution order

1. Investigate the **rootless Podman actual-container timeout** with constrained host logs, storage health and pinned image smoke without changing protected SearXNG or global rootless Podman configuration. Keep all diagnostics separate from production.
2. Certify actual guest source modifications, `.git` readonly denial, trusted QA and fail-closed cancellation against pinned container digest, plus negative cross-project/secret isolation.
3. Review previously blocked candidate CLI/ingress with connector/security owner, legitimately authorize a **fixed-purpose project-scoped** interface; do not attempt to bypass earlier tool safety denials via a different shell or connector.
4. Certify real model-driven multi-file Python/Node and external Andaz static site generation with independent QA, genuine source diff and receipt.
5. Restore independent Mac testing or obtain a separately accepted independent equivalent, project-scoped PR/review identity and hosted CI for exact candidate.
6. Only after previous gates are certified, run a bounded canary alongside unchanged v6 and observable rollback; then production promotion may be considered. No auto-merge/publish/spend.
7. Until then, do not send new `dev_proposal` tasks to the stopped old Brain consumer; the existing v6 controller should remain healthy and unchanged.

**This is a partial engineering certification milestone, not authorization to weaken the host, nor a successful general-purpose Dev Brain release.**

## Follow-up mount isolation diagnostics, 23 October 2026

**New distinction:** Direct plain rootless Python image guest boot with `--network=none --read-only --cap-drop=all --security-opt=no-new-privileges` returned `PODMAN_GUEST_START_OK`, exit 0 (SSH receipt `0ca0b174-9912-488b-9913-71747b83c1d4`). This proves the installed local Python image can boot without a workspace mount.

- With a temporary disposable workspace and normal rootless Podman, **single workspace bind mount and nested read-only Git metadata bind mount both timed out** using the original `:Z` labeling options. SSH receipt `4c4fc9c0-fa3e-412c-b071-70d2906f8bdb`, process exited 0 only because diagnosis reported both timeouts explicitly.
- Docker-compatible Podman is rootless and **SELinux disabled**, AppArmor disabled, ext4 host storage with free capacity; diagnostic terminal `333cbd7f-c3e7-421a-852a-a084d27caf4e`, exit 0.
- Retested both single workspace and nested read-only Git bind mounts **without `:Z`** (SELinux already off). Both again timed out, terminal `24066c95-7d82-459a-a89d-cd730be521fe`. Therefore **SELinux relabel option alone is not the cause**.
- The rootless workcell failure is now narrowed to **bind-mounted project workspace/container storage/runtime behavior**, rather than universal failure to start any container. The exact underlying cause remains unverified.
- Do not disable host security, clean unrelated Podman storage, change the live SearXNG container or claim successful guest edit/test. A future reviewed solution may use a disposable copy-in/copy-out OCI workcell with a declared output manifest and independent diff hashes, but that design requires its own security review and QA; it is **not deployed or certified**.

**Updated final release disposition remains NO-GO** for unified Brain integration, source-editing and production cutover. Independent unit certifications **16/16** and **13/13** remain valid for their pinned test targets only. The existing certified v6 is still active and unchanged.

