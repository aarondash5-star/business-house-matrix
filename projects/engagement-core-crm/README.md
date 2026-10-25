# Dell Dev Tool Yard — CRM G1 Design Enrollment (source + local staged record)

**Owner workstream:** Engagement Core CRM (`karanzing1992/engagement-core`)  
**Yard system:** `aarondash5-star/business-house-matrix` / existing Dell `matrix-controller`  
**Gate:** `engagement_core_crm / dev_project_build / crm_wireframe_g1_v1 / reviewed_patch_v1`  
**Only authorized outcome:** editable mobile-first **G1 design prototypes and QA**, no CRM backend / production code.

## Source and actual local status

- Full G1 brief: [Engagement Core specification](https://github.com/karanzing1992/engagement-core/blob/main/docs/ENGAGEMENT_CORE_CRM_V1_MOBILE_WIREFRAME_DEVYARD_BRIEF_20261026.md)
- Existing prototype: [G1 Wireframes](https://github.com/karanzing1992/engagement-core/tree/feat/eccrm-mobile-wireframes-g1-20261026/design/eccrm-g1)
- Git issue: [engagement-core#75](https://github.com/karanzing1992/engagement-core/issues/75)
- Local frozen brief SHA-256: `c1743553515178b9c7cb9c2608aca12ca6f7c23a15ba625cf2fec9ad2b4cefe1`
- Exact quality contract SHA-256: `9afe3098449fc5d3bd38ad15ecd9e8d1e8db3b3dce3b58969d451e3fa4743251`
- Project-scoped live registry entry added with approved exact manifest and `reviewed_patch_v1`; previous registry backup under `matrix-controller/release-backups/eccrm-enroll-20261025T212609Z/`.
- **Owner-intake approval ledger untouched.** Thus `quality_admission.py intake engagement_core_crm crm_wireframe_g1_v1 --action dev_project_build` **fails closed with** `owner_intake_approval_missing_or_ambiguous`. This is intentional. The user's "Do it" authorizes scoped design and enrollment but is **not evidence of separately signing an exact generated contract SHA**.

## Verify and finalize admission without bypass

1. Review **exact** `quality/brief.md` and `quality/quality-contract.json` in this PR.
2. Separately record owner approval of **contract SHA `9afe3098...`** through the existing owner-controlled intake mechanism (do not have the worker/model synthesize `approved_by:owner`).
3. Validate source hash match, previously enrolled registry, and current owner ledger. Create a **reviewed patch manifest** with only the pinned G1 design files and isolated tests; read current workspace/inventory; prevent overwriting other project outputs.
4. Dispatch via controller `dev_project_build`, watch durable task receipt; refuse task if ledger or hash differs.
5. Browser-test actual mobile/desktop artifacts, perform independent visual critique, preserve G1 owner approval gate. Never auto-merge or publish.

**Do not route the G1 CRM task through any existing `shaadi_aunty_dodge`, `delulu_tech`, `andaz_website` or other manifest.** That would cross tenant/source and QA boundaries.

## Continuous-work + art-direction investigation

Verified installed Manager V3: `bhm-autonomy-controller.service` runs its 20-second dispatch/observation loop and writes local read-only summaries/events. Per `matrix-controller/docs/MANAGER_GOVERNANCE_V3_20261026.md`, **continuous observation is NOT creative iteration**; actual workers require separately enrolled bounded tasks.

Existing `bhm-shaadi-ai-art-director.timer` is 30-minute, Shaadi-only; current `director_status.json` says `waiting_for_local_vision_model`, zero completed cycles. **Do not reuse it for CRM**.

Recommended G1 integration: use existing Manager V3 for task status/event receipts; add an isolated CRM art-direction acceptance checklist bound to actual Playwright captures and prototype hash. Once a verified visual reviewer/local permissively usable vision model is available, schedule *bounded* project-specific review against the frozen quality contract; stop at owner acceptance. No new generic shell, credentials, video worker or parallel periodic orchestrator.

## QA and controls

G1 interactive source on Dell, isolated git worktree, Chrome Playwright **253/253 route/state/navigation/viewport checks**; screenshot pack and QA JSON available only in project-local QA directory. This is **technical interactive prototype QA**, not independent visual acceptance or backend integration.

Manager V3 controller selftest passed after enrollment; negative test cross-project manifest denial passed. The full targeted unittest selection is still being reconciled; do not treat a piped/partial unittest command as a pass.

**Scope:** No external providers, paid APIs, real CRM customer data, WordPress migration, live publish, new root policy, Ashwakaal account/data sharing or producer-artworker cross-project execution.
