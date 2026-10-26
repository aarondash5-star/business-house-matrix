# Dell V4 source rebase and offline rollback certification — 27 October 2026

**Verdict:** **REBASED SOURCE TECHNICAL PASS / LIVE DELL DEPLOYMENT NO-GO.** This receipt does not grant authorization, attest an independent signer, or certify on-host service restart/rollback.

## Exact real-host readbacks

Connected Dell `dell-linux` control-lane jobs were **completed / exit code 0**:

1. `5eab6fdf-8c82-43f2-91f4-ee448ff60f4b`: active controller `0.2.4-manager-governance-v3`, controller SHA256 `e6834bb2f7765ee0aa26d215a566f70276e4f8c2c87c8730fc781c27dc778836`, current adapter **V1.2.0** SHA `adad20add5e247c515c48d8e2d0c61f2b91e2238d489ed8b4c2e674c845d1abe`, V1.3 guard SHA `7a989c6b484a13a4fdf349d698a6a1bf9e8d9b1afa9684508606bc08c036283e`, 20-binding ledger SHA `9c084832984c1471a22079cc606daccd0a49b78c942ddfee0800a800176c43a9`. Adapter AST has 14 functions, V1.2 limits 1 MiB and 512 registered tools.
2. `f2c29f7a-6183-4d9b-8018-46e7a469cd47`: unified diff proved the stale V4 adapter candidate changed only adapter version, V1.2 constants, `load()` and `save()` validation. These are independently reviewed read-only facts, not a claim the old V4 was compatible.
3. `7a8e1a26-f5cd-49cc-9db8-4df85d84f7f5`: currently installed `yard_tool_adapters_v1.json` is **106,940 bytes** and contains **121** tools, each in `accepted_qa_probe_only` state; read-only, mode 0600, non-symlink. Under both V1.2 and V4 size/count limits.
4. `a0c34b4e-5a12-47bb-a2c9-7ad280a34887`: independent read-only pure derivation from **actual live guard and ledger** returned exactly pinned V1.4 gate SHA `664d4681747282561755dd34201210ce19306e15beeb506c8c02a024bf7ae644` and canonical ledger SHA `81edd213acfd4c66359d1a217a62c392c283358e972a7ea87b4948687fc5012f`, 21 source bindings. No host writes or source installation occurred.

## Rebased release contents

| File to be installed only after signing | SHA256 |
| --- | --- |
| `yard_auto_adapter_v1.py` (rebased V1.2.2 bounded) | `2ea43e8953c59726f510b6db9a8d0127a64efd7acb0fb824db5c70cb130a8837` |
| `adapter_guard_v4.py` | `90f0a62cc6cfaf1458f0684363ffb9288c900ba0ade707908da0877447249e30` |
| `yard_execution_guard_v13.py` (V1.4 enforcement code) | `664d4681747282561755dd34201210ce19306e15beeb506c8c02a024bf7ae644` |
| `yard_exec_bindings_v14.json` canonical sorted compact JSON with LF | `81edd213acfd4c66359d1a217a62c392c283358e972a7ea87b4948687fc5012f` |

Freeze is in `brain/dev-toolyard/governance-v4/v4_rebased_v12_release_manifest.json` (unsigned, **not a release approval**). Source files:
- `v4_rebase_live_v12.py`: pure, exact-Dell-SHA validated reconstruction of V1.2.0 from earlier V4 candidate, strict transform to V1.2.2 and full 21-binding policy, pins guard + ledger with independent Dell checks.
- `yard_auto_adapter_v12_rebased_v14.py`: exact generated candidate, SHA pinned.
- `test_v4_rebase_live_v12.py`: independently checks reconstruction against actual observed Dell SHA, tests guard load/save with real reviewed V4 registry guard, 512-tool cap, invalid-operation rejection, symlink/permission safety.
- `guided_dell_v4_install_preflight.py`: updated to **current** real Dell V1.2 adapter and ledger digests while retaining all downstream release blockers.
- `v4_in_memory_release_transaction.py` and corresponding test module: in-memory only four-step apply/three-file restore model, injected interruptions before and after each step; **no filesystem writes, service calls, owner auth or deployment**.
- `v4_rebased_v12_release_manifest.json`: independently hash-pinned, `release_authorized=false`, `deployed=false`.

## Automated CI readback

GitHub `Matrix source validation` workflow run **40391098279**, source commit `0c4f7069d964e0f1c2903da81bfdc8d8a9518eaa`: **SUCCESS**; `starter-tests` **242 passed, 63 skipped, 30 subtests passed** and `public-repository-safety` succeeded. Earlier tests of exact frozen candidate source passed at commit `1e72151660fdab946d6f7073e735b46be556f051` (230 passed). Skipped suites are host-private fixtures and are **not** a certification of the live installation or rollback.

The in-memory transaction check restores all original synthetic files on faults after steps 0, 1, 2, 3 and 4; no actual controller file changed. **Only a real host-side canary with guaranteed rollback can certify host activation.**

## Remaining protected release gates

1. The **existing PR #34 SSHSIG broker is pinned to the stale pre-V1.2 adapter** and cannot accept this manifest as written. Review and implement a **new rebased broker / correct owner-signed payload**, not a runtime override or command-flag bypass.
2. The existing Supabase `matrix-devbeta-attest` is **deployed but disabled** and cannot issue owner-approved release signatures. Required: exact original DEV_BETA public PEM/verified keypair, verified server-side owner UID, live approved email containing **both OTP and link**, atomic single-use release challenge, independent signer, replay/failure tests. Do not reuse Pine key or treat owner chat instructions as a detached signature.
3. Root-owned Dell trust store, signed per-release artifact, encrypted independent approval inbox and 5-minute validity have not been enrolled; prior host readback found these absent.
4. Certify a fixed-purpose **host activation/rollback runner** with private 0700 backups, dry-run, worker queue drain and exclusive lease, stage-once audit, systemd stop/start/health, actual stop/restart recovery, hash readback and rollback under failure. The source model is a component, not the live host runner.
5. Independent review of PRs #33, #34, #35, #36 (including new rebase) remains pending. Do not merge source or install candidate from a draft branch without approval/QA.
6. Complete Dell-only bounded V4 canary and verify controller version/source digests/service/queue integrity before reporting live. Mac is a separate release.

## Owner secure CLI

Vercel `dell-private-login-ui.vercel.app` was confirmed `READY`, but credential entry / terminal transport has not been audited end to end. Do not direct owner to type an admin password into it before that security QA. Existing Dell six-lane SSH is online and adequate for read-only inspection. No root/sudo policy or credentials were modified.

**Status:** `SOURCES_REBASED_AND_SHA_PINNED / CI_242_PASS / SIMULATED_ROLLBACK_PASS / OWNER_SIGNER_MISSING / REBASED_BROKER_PENDING / HOST_ACTIVATOR_PENDING / PR_REVIEW_PENDING / V3_CONTROLLER_UNCHANGED`.

**Open-source/reuse/cost gate:** Reused existing Python 3 stdlib, GitHub Actions, OpenSSH, Supabase Auth/Edge, and existing Dell service. No paid components or subscriptions added. Actual private signer key remains Supabase-side; no key material embedded in repository or transmitted through chat.
