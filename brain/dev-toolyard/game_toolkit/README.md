# Shaadi Aunty's Dodge — Matrix Dev Tool Yard integration

**Status: SOURCE STAGED ONLY. DELL BRIDGE OFFLINE AT IMPLEMENTATION (25 October 2026). NO RUNTIME DEPLOYMENT OR LIVE QA CLAIMED.**  
Source branch: \`feat/shaadi-game-toolkit-matrix-integration-20261025\`, based on Matrix controller's existing reviewed 0.2.2 global-intake gate branch. Do not merge to main or run against a different controller release blindly.

## Why this integration exists

The Dell already has an isolated game-authoring toolkit at:
\`/var/lib/generic-linux-automator-exec/matrix-game-toolkit-20261025\`.

It contains locked OSS npm tools (Three.js, Rapier, VRM, glTF Transform, Meshoptimizer, tween.js, Howler, stats.js, Playwright, postprocessing, Theatre Studio, BVH), portable Blender 4.5.15 LTS with MPFB2 2.0.18, and Kenney CC0 Food Kit source assets. Provisioning/13-of-13 smoke receipts are documented in Shaadi draft PR #407. These tools are for **asset authoring and independent QA** and cannot be added to the existing shipped G3 WebGL1 bundle by accident.

Matrix controller 0.2.2 only supports approved \`dev_project_build\` source-patch and website staging actions; its Bubblewrap code patch runner does not mount external authoring libraries. We provide a **separate, tightly controlled, static recipe runner** rather than relaxing the global patch sandbox or enabling arbitrary SSH commands.

## Current feature inventory (after approved live installation)

| Manifest | Fixed executor behavior | Side effects |
|---|---|---|
| \`shaadi_toolkit_verify_v1\` | Read pinned toolkit manifest and package-lock SHA | Read-only |
| \`shaadi_toolkit_smoke_v1\` | Execute pinned 13-check Node/Chrome/physics authoring smoke within no-network Bubblewrap | Read-only tools with ephemeral private sandbox /tmp |
| \`shaadi_mpfb_verify_v1\` | Launch pinned portable Blender and import MPFB2 extension in isolated profile | Test-only; no game scenes modified |
| \`shaadi_kenney_inventory_v1\` | Read immutable Kenney ZIP and check publisher CC0 license and SHA | Read-only |
| \`shaadi_gltf_cli_v1\` | Read glTF Transform CLI version in Bubblewrap | Read-only |

All actions use **exact project** \`shaadi_aunty_dodge\`, **exact manifest**, no arguments chosen by a model, no arbitrary path, no executable script supplied by a task, no public network access, no publishing and no spending. No work in \`KaranZi/shaadi-aunty-dodge\`, Claude v1.0.3 workspace or other Matrix projects.

**This first adapter is a verified-tool invocation layer**, not yet a production-grade optimized-GLB export pipeline. Introducing write-producing recipes, rigging models or Playwright on a live URL requires a separate owner-reviewed manifest, isolation checks and real-asset quality evidence. Blender import inside Bubblewrap must be tested on the actual Dell before claiming runtime QA passes.

## Governed Matrix registration

Code \`deploy_game_toolkit.py\` installs a minimal, additive \`game_toolkit\` action into the existing controller under the existing **dual owner approval gates**:

1. Registry allowlists the five manifests exactly under \`shaadi_aunty_dodge/game_toolkit\`.
2. Submit action calls the registry's \`enroll_check\`; no other projects or tools accepted.
3. Existing \`quality_admission.intake_check\` now treats \`game_toolkit\` as a protected action and requires owner-pinned \`brief.md\`, \`quality-contract.json\` and an owner-maintained intake approval record **before submit and again before dispatch**.
4. Dispatch executes \`game_toolkit_runner.py run shaadi_aunty_dodge <one_of_five_pinned_recipes>\` via fixed argument arrays, not the shell, and records independently inspectable technical-only QA receipts. Failure -> \`needs_review\`, no retry loop. Quality governor annotation remains present in the receipt; \`release_authorized=false\`.
5. Service and existing historical tasks, other project enrollment and release ledger remain unchanged apart from the narrowly approved local action source upgrade.

The installer does **not** manufacture or rewrite owner-intake/owner-release ledger approvals. Owner authorizes an exact frozen brief + quality criteria and its content hash as a distinct governance step. A general installation request does not waive existing Matrix project admission checks.

## Local source tests (no Dell required)

\`\`\`sh
cd brain/dev-toolyard/game_toolkit
python3 -m unittest -v test_game_toolkit_runner.py test_deploy_game_toolkit.py
\`\`\`

Checks include foreign projects, manifest path traversal, symlink paths, dependency tampering, missing Bubblewrap, no general shells, no host/home mounts, no implicit publication, staged controller patch compilation, old actions preserved, admissions extended, correct registry enrollment, and required exact controller SHA.

## Dell deployment procedure — DO NOT RUN UNTIL HOST ONLINE

The owner-authorized Dell connection must be fresh and provide exact current preflight evidence. Use the *development lane*, but the authorized install updates the local Matrix service; document and secure a full rollback.

1. Verify \`linux_host_status("dell-linux")\` online, paired, fresh development lane. Record clock and worker identity.
2. Read-only fingerprint and policy check:
   \`\`\`sh
   D=/var/lib/generic-linux-automator-exec/matrix-controller
   sha256sum "$D/controller.py" "$D/project_registry_v1.json" "$D/quality_admission.py"
   python3 "$D/controller.py" status
   systemctl --user is-active bhm-autonomy-controller.service
   \`\`\`
3. Pin this GitHub source branch's **full commit SHA**, review exact diff, copy the four new integration source/test/README files into an **isolated release staging directory** (not the game's source or original toolkit). Compare content SHA to GitHub before execution. Never execute unreviewed code from a random mutable branch.
4. Run independent \`unittest\` tests, followed by preflight:
   \`\`\`sh
   python3 deploy_game_toolkit.py preflight --expected-controller-sha256 <actual_64_hex_SHA_FROM_STEP_2>
   \`\`\`
   Preflight is read-only and stops if the live controller differs from the 0.2.2 expected structure, service is not active, QA fails or a new runner path collides.
5. Only after a completed successful preflight:
   \`\`\`sh
   python3 deploy_game_toolkit.py apply --expected-controller-sha256 <same_SHA>
   \`\`\`
   Installer backs up only the four touched Matrix files under \`matrix-controller/release-backups/\`, pauses/restarts **only** \`bhm-autonomy-controller.service\`, applies the protected registry/source, runs controller selftest, verifies controller version, owner admission policy and restarts. Rolls back installed files and service on a failure. No root permission, host network or game deploy changes.
6. After activation read \`controller.py status\` -> \`0.2.3-shaadi-toolkit-governed\` and \`game_toolkit: owner_admitted_fixed_offline_qa\`; \`project_registry.py check shaadi_aunty_dodge game_toolkit shaadi_toolkit_verify_v1\` must pass.
7. **Before submitting a live task**, separately record frozen quality contracts and owner intake ledger approval for each intended manifest; the code intentionally fails closed without them. Then submit and tick one benign manifest in staging first, inspect task \`show\` receipt and verify technical-only/owner-review-pending, and run negative tests (wrong project/manifest, missing record, compromised lock).
8. Collect runtime proof for Node/Chrome, MPFB import in no-network Bubblewrap, CC0 archive and optional GLTF CLI. A HEAD/HTTP status or mere registration is not evidence that a recipe executed correctly.

## Security/compatibility limits

- Running through native Generic Linux SSH gives the owner separate machine-administration access; **this does not mean the Matrix model brain gains arbitrary SSH capabilities**.
- Heavy Three.js library and Theatre Studio are **NOT** inserted into the current G3 game engine. Theatre Studio is AGPL-3.0-only; review obligations before distributing its code.
- MPFB2 is GPL-3.0-or-later; verify exported-asset/license terms separately. Kenney Food Kit is CC0 from original \`License.txt\`.
- No deployment to Cloudflare, game GitHub \`web/dev\`, \`web/test\` or \`web/production\`.
- The current v1.0.3 testing remains Claude's independent work; the Matrix adapter cannot merge or invalidate it.
- No background retry is scheduled. Dell was offline when this branch was written; do not claim \`DELL_LIVE_VERIFIED\` until fresh terminal receipts exist.

## Suggested owner-facing status conventions

- \`TOOLKIT_INSTALLED\`: YES — the prior authenticated Dell install and 13/13 smoke completed.
- \`ADAPTER_SOURCE_COMMITTED\`: YES after the new GitHub source commits.
- \`ADAPTER_LOCAL_UNIT_TESTED\`: PENDING independent CI/host tests.
- \`MATRIX_CONTROLLER_REGISTERED\`: NO until Dell reachable and guarded apply succeeds.
- \`ADMISSION_CONTRACTS_APPROVED\`: NO until exact project/manifest owner records supplied.
- \`GAME_V1.0.3_CHANGED\`: NO.
- \`PUBLIC_RELEASE_AUTHORIZED\`: NO.

## 25 October 2026 — live Dell activation and independent certification update

The earlier "offline/source staged only" language above describes the *initial* attempt; this section supersedes its runtime-status assertions.

- Authenticated Dell development lane online. Live controller pre-install file SHA256 `e7bbc99658ae1978e7c804fa763de993195a126f43558d238ab2b70269e688f9`; prior version `0.2.2-global-intake-governed`.
- Initial preflight correctly **failed closed**: the ephemeral staged selftest did not include its unchanged `quality_gate.py` dependency. The installer now copies that existing dependency into the **throwaway test directory only**, not the controller. Retest: 24/24 source unit tests and guarded preflight **PASS**.
- Guarded `apply` on Dell completed, old controller backed up at `/var/lib/generic-linux-automator-exec/matrix-controller/release-backups/shaadi-game-toolkit-20261025T114833Z`. Active user service and controller readback: `0.2.3-shaadi-toolkit-governed`; new `game_toolkit` action exposed; all original quality/release gates still enabled. Owner-intake and release ledgers **not modified**.
- Negative live controller submission cases correctly denied: missing owner intake, foreign project and unknown manifest. Direct owner-scoped runner: pinned verification **PASS**, 13/13 isolated authoring tool checks **PASS**, Kenney CC0 provenance inventory **PASS**, glTF Transform CLI `4.5.1` **PASS**.
- MPFB **initial recipe false positive caught**: the first import-only marker printed even after Blender logged an add-on registration exception because its logs lived in a read-only sandbox tree. This is a **certification defect**, not accepted as success. The runner now overlays **only the existing MPFB log directory with disposable sandbox tmpfs**, actually checks Blender's enabled add-on registry, and rejects any Blender registration exception or traceback. Dell retest: real `MPFB_REGISTERED_OK 4.5.15 LTS` with no stderr, **PASS**. A mocked false-positive/registration-error is now a negative regression test. Complete source suite **26/26 PASS**.
- Runner-only rollback backup: `/var/lib/generic-linux-automator-exec/matrix-controller/release-backups/shaadi-game-toolkit-mpfb-runner-20261025`. Installed corrected runner SHA256 `0b53bc8d43defa50b0fea4cd60cf6d0ad24b8c22aefda1d5ddc80492b5e5e5eb`.
- **Important boundary:** These recipe executions were owner-scoped direct technical QA, **not** a controller-admitted `game_toolkit` task. The live Matrix submit/dispatch path still requires a separately frozen owner-approved brief, exact quality contract and intake approval record; no approval URL or signature was invented. Therefore label it `CONTROLLER_REGISTERED=YES`, `RUNNER_5_RECIPES_TECHNICALLY_QA=YES`, `MATRIX_END_TO_END_OWNER_INTAKE=NOT_CERTIFIED`.
- This tool integration does **not** modify or deploy the game's G3 source. Dell drafted a separate data-only Sharma Aunty encounter module in private Shaadi draft PR [#414](https://github.com/KaranZi/shaadi-aunty-dodge/pull/414); runtime wiring, full browser Gate 1 and actual Android Gate 2 remain pending. No owner-approved public release.
