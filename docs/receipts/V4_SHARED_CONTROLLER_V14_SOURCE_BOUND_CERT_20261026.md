# V4 shared-controller V1.4 candidate — independent technical certification

**Date:** 2026-10-26 (IST). **Owner:** Business House Matrix Dev Yard.  
**Review branch:** `feat/v4-source-bound-promotion-review-20261026`.  
**Source commit:** `5952cf690e65210de039f7fcd0f53caf76548c6c`.  
**Certification verdict:** **TECHNICAL-CANDIDATE PASS / LIVE SHARED-CONTROLLER RELEASE NO-GO**.

This document certifies a **detached** V4 adapter-and-V1.4 source-binding migration candidate. It **does not** authorize writing to the protected controller, tampering with original V1.3 binding ledger, restarting its service, upgrading the SSH transport, replaying the queued Driver build, installing persistent Drivers or declaring production.

## 1. Facts inspected on Dell

- `dell-linux` online with three fresh lane heartbeats, `mac-linux` offline (checked at certification).
- Live `bhm-autonomy-controller.service` active and original `controller.py` version `0.2.4-manager-governance-v3`. Source SHA256 `e6834bb2f7765ee0aa26d215a566f70276e4f8c2c87c8730fc781c27dc778836`.
- Live `yard_auto_adapter_v1.py` SHA256 `16f54c4ae1d97699786b649e84c94df2abb673b0682a20045d55399399217b79`; original live registry 80,005 bytes and old adapter 80,000-byte cap remain.
- Original `yard_execution_guard_v13.py` SHA256 `7a989c6b484a13a4fdf349d698a6a1bf9e8d9b1afa9684508606bc08c036283e`.
- Existing live `yard_exec_bindings_v13.json` has **20 source pins**, seven preserved metadata fields: `version`, `bindings`, `actions_bound=11`, `production_live=false`, `external_paths_certified=false`, `independent_human_review=false`, `review=technical_hash_and_syntax_only`; exact on-disk SHA256 `20f68602194af481d48dfaf6bcc406d383f0818f7bd082cf5d92227b24aac64e`.
- Original Lane Driver build task `884cd886-943e-4ea8-93e8-9e5fcbaf100f` remains **queued, attempts=0**, unmodified; previous single-workflow isolated Stage 2 V4 canary remains certified but is not a shared-controller promotion.
- This preflight is supported by live terminal SSH receipt `6bd32032-3591-4bce-9488-c6ee1f3d3d25` and prior `dcdf5090-ee87-4d51-8311-55b91f505e37`, both exit 0.

## 2. Reviewed V1.4 candidate pins

The pure, non-mutating review function `brain/dev-toolyard/governance-v4/v4_source_binding_review.py` checks exact original and reviewed source hashes and models an explicit four-file release bundle:

| Future release artifact | SHA256 / authority |
| --- | --- |
| V4 reviewed `yard_auto_adapter_v1.py` | `116f435279bbe7e0cc8281ab513e319926b846ab6ae25752bccc3fc6746fb773` |
| New `adapter_guard_v4.py` | `90f0a62cc6cfaf1458f0684363ffb9288c900ba0ade707908da0877447249e30` |
| Revised `yard_execution_guard_v13.py` with pinned V4 guard and policy v1.4 | `bb0339f48add0537771dec2b2e4898258bfd4bd7758e1648a62f10130a2ee3e3` |
| New `yard_exec_bindings_v14.json` | 21 pinned dependencies; preserved seven metadata fields; no live policy, signed human review or production permission granted |

The previous V1.3 guard and adapter bytes and original seven-field ledger are retained in **read-only** owner-local QA fixtures, not shipped into public Git. Read-back of the pure candidate (SSH receipt `c583903b-ed8c-4cd1-b40e-7cc27efb4648`, exit 0) reports `host_write_authorized:false`, `production_authorized:false` and source-integrity PASS.

## 3. Actual QA evidence

| Group | Test result | Host gateway terminal receipt |
| --- | --- | --- |
| Source and seven-field V1.3 metadata integrity | 16/16 PASS | `da27d9b3-e7f0-4324-b8b1-263b5905f98f` |
| Detached V1.4 Manager/Development admission, denial policies | 11/11 PASS | `da27d9b3-e7f0-4324-b8b1-263b5905f98f` |
| Detached **V1.4 → V1.3 rollback** and partial-migration rejection | **5/5 PASS** | `da27d9b3-e7f0-4324-b8b1-263b5905f98f` |
| V4 adapter and original V1 compatibility/negative regression | **63/63 PASS** | `7c549787-c1bb-4dca-bc45-a5d6687a77de` |
| Original live V1.3 enforcement guard regression | **9/9 PASS** | `7c549787-c1bb-4dca-bc45-a5d6687a77de` |
| **Total tests at this checkpoint** | **104/104 PASS** | All cited gateway tasks terminal `completed` with exit code 0 |

All candidate/rollback tests run in **rootless Podman, with network disabled, source and fixtures read-only**, 256 MiB memory cap, CPU and PID limits, `--cap-drop=ALL` and `--security-opt=no-new-privileges`. The original live V1.3 guard tests are read-only; they did not change source or controller state.

The first detached candidate test uncovered a fail-closed schema mismatch (existing ledger had seven metadata fields, not the initially assumed four), recorded by original FAILED test receipt `c24f9f5f-b6a5-4b5b-afd8-9108f6cbaa18`. The code was corrected, preserving all fields. The revised suite passed 27/27 in receipt `ddf5d3b6-399b-497c-b5de-2489d6c71718`, and later expanded to 32/32 (receipt above). The failed initial run must not be silently called a pass.

### Rollback evidence scope

The five new rollback tests recreate reviewed V1.4 source and policy **inside disposable rootless filesystem**, then restore exact V1.3 source bytes and original ledger, prove original Manager and Development preflights pass, and prove partial V1.4 release fails closed on missing guard or ledger. **The actual production-controller stop/swap/restart/rollback was NOT performed or certified**; a successful detached rollback does not imply a safe host activation.

## 4. Certification matrix and hard stop

| Gate | Outcome |
| --- | --- |
| Reviewed source SHA and full old ledger schema | **PASS** |
| V4 + original adapter bounded compatibility | **PASS** |
| V1.4 source-binding and Dev Yard preflight | **PASS** |
| Negative security and drift denials | **PASS** |
| Detached V1.4 rollback to original V1.3 | **PASS** |
| Live shared-controller signed release broker | **NOT VERIFIED / BLOCKED** |
| Exclusive shared-task writer, queue drain and reconciliation | **NOT VERIFIED** |
| Atomic host backup/swap/rollback and deployment receipts | **NOT VERIFIED** |
| Actual V4 shared-controller task dispatch | **NOT EXECUTED** |
| Durable Lane Driver real-workflow integration | **NOT EXECUTED** |
| Mac parity (3 lanes) | **OFFLINE** |
| Production or universal permission release | **NO-GO** |

The existing denial of unreviewed host adapter/controller replacement remains binding. **Do not direct-shell replace the adapter, rewrite the V1.3 bindings, stop the shared service, truncate the registry, or use a generic controller tick as a substitute for authorization.**

The only route toward host promotion is an independently reviewed owner-signed fixed-purpose release broker, with a single-executor lease, verified action admission and no unbounded shell; pre-state/source hashes and restorable on-disk snapshot; atomic candidate install; bounded live canary and independent negative tests; terminal receipts; and an independently verified rollback. The outstanding Driver build must be reconciled before a new dispatch attempt.

## 5. Reuse, costs and source of truth

Golden Rule 0: all components reused from the existing Matrix Python/SQLite, current controller V1.3 and V4 source, existing rootless Podman and Dell Generic Linux SSH six-lane gateway. **No new API, package, subscription, SSH credentials or paid service; incremental software cost zero** on existing infrastructure. No external customer data, Pine private accounts, Andaz/Moksha production websites or Ashwakaal Support Channels accessed. No project-wide permission change.

**Status to propagate:** `V4_V14_TECHNICAL_CANDIDATE_CERTIFIED`, `SHARED_CONTROLLER_DEPLOYMENT_BLOCKED`, `DRIVERS_NOT_LIVE`. Do not publish a Master event claiming V4 operational in the shared controller. Existing shadow #155 and one-workflow canary #156 remain separate.
