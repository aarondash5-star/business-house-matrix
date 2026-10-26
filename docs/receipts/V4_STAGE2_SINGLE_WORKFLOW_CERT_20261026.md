# V4 Stage 2 — Dell one-workflow isolated live canary, 2026-10-26

**Disposition:** `SINGLE_WORKFLOW_LIVE_CANARY_PASS` — one authenticated SSH-dispatched, actually executed fixed probe in a separate, isolated V4 controller. **NOT a shared-controller V4 promotion, NOT a six-lane driver activation, NOT production.**

**Scope approved by owner:** Deploy Stage 2 of the limited canary after Stage 1; single nonproduction workload on Dell, separate controller/queue, preserve security denials and unchanged shared runtime.

## Source and reuse

- Repo: `aarondash5-star/business-house-matrix`, branch `feat/dev-toolyard-fidelity-execution-v4-20261026`.
- Code source commit **`f19d0cb9bf921cbf2aa9a936e92d9c98af973aab`**.
- New fixed-function controller `brain/dev-toolyard/governance-v4/v4_stage2_canary_controller.py`; negative tests `test_stage2_canary_controller.py`.
- Reuses V4 reviewed adapter `yard_auto_adapter_v1_patched.py` SHA256 `116f435279bbe7e0cc8281ab513e319926b846ab6ae25752bccc3fc6746fb773` and V4 guard SHA256 `90f0a62cc6cfaf1458f0684363ffb9288c900ba0ade707908da0877447249e30`.
- Original source snapshot (80,005 bytes, 91 tools) SHA256 `76cd6bcdf3c947012a1b83e551cef4e4ed206aa0ba6975fd876715631e325dc8`. V4 guard checked actual unchanged snapshot before execution.
- Uses only Python stdlib / SQLite and existing owner-authenticated Generic Linux SSH six-lane service, rootless Podman and cached Python 3.12 Alpine image. No paid API, new customer data, private Pine access, service token, public listener, endpoint or new ongoing worker.

## Deployment boundary

- Owner-local Dell source checkout: `~/matrix-v4-stage2-source-20261026` at exact commit.
- Isolated stage: `~/matrix-v4-stage2-canary-20261026`, mode 0700; `app/` read-only inside container with source files mode 0600; isolated `state/` mode 0700 and writable *only inside the separate rootless container*.
- Rootless Podman parameters: `--userns=keep-id`, explicit non-root UID 995, `--network=none`, `--read-only`, `--cap-drop=ALL`, `--security-opt=no-new-privileges`, `--pids-limit=64`, 256 MiB memory limit and 1 CPU.
- No host controller DB, live registry, secrets, SSH key or other projects mounted into container.
- Entrypoint accepts only `execute-exactly-once` with **hardcoded** project `matrix_dev_manager`, manifest `v4_stage2_single_probe`, action `probe_version`, tool `python3`, task `v4-stage2-canary-20261026`; release and spend flags false. No arbitrary executable or command string accepted. The only allowed command is actual container Python `--version`, verified by V4 `preflight()` and `probe()`.
- Transport: user-initiated, authenticated `dell-linux/development` MCP command. This is **not** a new separately signed network API or a general-purpose Dev Brain worker dispatcher. No recurring controller service enabled.

## Terminal evidence (all checkable by owner)

| Gate | SSH task receipt | Verified result |
| --- | --- | --- |
| Live host preflight | `f2ecf095-ad6e-487c-82ac-ecffd186ccd9` | Dell three lanes online, legacy controller active, no shared changes, old Driver build queued / attempts zero |
| Stage 2 fixed source checkout | `60af4860-4e48-4a64-b380-9b6e9dac78db` | Git commit `f19d0cb9bf921cbf2aa9a936e92d9c98af973aab`, clean, V4 guard/adapter pins pass; exit 0 |
| Private workcell staging | `dc1ceea4-167f-41bb-a66e-af972b203505` | Separate 0700/0600 source/state; original shared controller unchanged; exit 0 |
| Independent negative/recovery suite | `e3488fe5-a6db-4205-a63e-a54920b1a1d4` | **14/14 PASS**, rootless/no-network container, exit 0 |
| Final empty-state/shared-controller preflight | `632df870-cfc2-4951-b95e-55b231fe85a5` | Dedicated DB absent before first run, original hashes unchanged, old task queued, exit 0 |
| Container nonroot/snapshot preflight | `539d10f2-f157-48fd-b409-c41b61852a93` | Actual euid 995, guard PASS, 91 tools, no production, state empty; exit 0 |
| **Exactly one real fixed-tool task** | **`f0243456-8c15-4363-b1c2-af3cf1d8e118`** | **COMPLETED exit 0**, actual V4-preflighted subprocess `python3 --version`, `reused:false`, receipt persisted |
| Independent SQLite and shared-host QA | `168f0910-f8a2-49b2-9cfa-77e18b920b70` | **COMPLETED exit 0**, exactly one row with status completed and attempts=1; immutable scope/no spend; original controller active/hashes intact; original Driver build queued/0; no leftover canary container |
| Terminal replay suppression | `7ca96caa-da89-4de3-8d5e-bc5ed1ffd52b` | **COMPLETED exit 0**, `reused:true`, exact original receipt, attempts stays 1; no second version-probe execution |
| Final V1.3 shared-security regression | `32c48eb2-6a18-4c0b-b90c-b941a4167a56` | **9/9 PASS**, controller active, hashes unchanged, original build queued, Stage 2 DB completed attempts=1 |

Stage 1 independently passed **63/63** V4 and original adapter tests via SSH `5e0b1a4b-3774-4472-86c5-85f5c2ca5802`; see `V4_LIMITED_SHADOW_CANARY_20261026.md`. Stage 1's stale-running prior attempts remain documented; Stage 2 did not replay them.

## Persisted exact output

`~/matrix-v4-stage2-canary-20261026/state/stage2-canary.sqlite3`:

- task ID `v4-stage2-canary-20261026`
- `status=completed`, `attempts=1`, `project=matrix_dev_manager`, `manifest=v4_stage2_single_probe`
- `actual_operation=python3 --version`; source-binary SHA256 `8a225e021fcee4c6d493a243da73e8604feb2df88576e3910254c248ea38bc95`
- registry snapshot SHA and number of tools match pinned preflight
- `production:false`, `spend:false`, `network:false`, `qa_only:true`

Only dedicated canary state was written. Registry creation used V4 `adapter.save` into `state/v4-stage2-probe-registry.json`, 0600, with sole approved tool and no arbitrary operations. No public endpoint or persistent listener exists.

## Shared runtime was NOT promoted

- Protected `~/matrix-controller/controller.py` SHA256 **`e6834bb2f7765ee0aa26d215a566f70276e4f8c2c87c8730fc781c27dc778836`** remains unchanged.
- Original `yard_auto_adapter_v1.py` SHA256 **`16f54c4ae1d97699786b649e84c94df2abb673b0682a20045d55399399217b79`** remains unchanged; old live 80,005-byte cap defect still exists.
- Service `bhm-autonomy-controller.service` remains active on old version; no additional service enabled.
- Existing Driver build task **`884cd886-943e-4ea8-93e8-9e5fcbaf100f`** remains `queued`, `attempts=0`; no blind replay.
- Mac remains offline at the last check. No Stage 2 deployment to Mac.
- Earlier security denial against changing protected shared controller remains binding. This one-shot canary does not grant promotion approval.

## Rollback and release continuation

Stage 2 canary has completed and does not run persistently; no service needs stopping. To remove only Stage 2's private artifacts, first capture its SQLite terminal receipt/source hash and independently verify no active canary container; then archive only `~/matrix-v4-stage2-canary-20261026` after owner records retention decision. Never modify shared controller, SSH gateway or original task journal as "rollback" for this isolated canary.

**Certified now:** one real **owner-authenticated isolated V4** workflow, exactly-once receipt/duplicate suppression, stage-source security checks and zero shared-controller impact.

**Not certified:** a general-purpose separately signed Dev Brain controller/worker ingress, persistent multi-task V4 routing, V4 live adapter in the shared controller, six Lane Drivers, production deployment or Mac parity. Any next live promotion requires its own reviewed versioned source pins, workcell authority, independent approvals, negative/rollback tests and a separate owner decision.

**Classification for Master event reporting:** `V4_STAGE2_ISOLATED_CANARY_VERIFIED`; do not describe it as `V4_PRODUCTION`, `SHARED_CONTROLLER_UPGRADED` or `SIX_LANES_LIVE`.
