# AI Art Direction — Autonomous Workflow & Quality SOP (V1)
**Project:** Shaadi Aunty's Dodge • **Updated:** 2026-10-26 • **Status:** non-production, review-only  
**Canonical quality gate:** `SAD-VISUAL-QUALITY-V1` (pinned; **not passed**)

## Purpose and scope
This SOP describes the operational lifecycle added to the existing Dell Matrix Dev Tool Yard. It establishes reproducible Blender artwork, locally assisted visual critique, restricted revision recipes, persistent task state, QA evidence, supervision, and explicit release control. It is **not** a claim of feature-film quality or of unrestricted self-improving AI. The art director has a **bounded maximum of three pre-authorized revision profiles**, after which independent assessment is required. Its real image-review loop is unverified until the local vision model runs successfully.

This is **Sharma Aunty first**. Wedding mandap improvements are a separately enrolled later phase. The game engine remains **Three.js**; Blender 4.5.15 LTS is the isolated authoring tool, with MPFB2. Neither Godot nor a substitute game engine is authorized.

## Actual architecture and boundaries

```text
Owner & pinned V1 artistic references
   |  explicit project scope, no quality-waiver
   v
Dell Matrix Manager v0.2.4 / governance-v3
   |  registry and existing admission/release policies unchanged
   +-- Fixed art worker (2-minute timer, SQLite jobs, fail closed)
   |     -> editable Blender rig + GLB clip/morph checks
   |     -> front / 3-quarter / expression QA renders + hashes
   |     -> foundation/license inventory, manual review of failures
   |
   +-- AI Art Director V1 (30-minute timer, independent unit)
         -> local Ollama VLM inspects actual rendered image
         -> JSON critique / highest defect / confidence
         -> picks ONLY glasses, jasmine or zari recipe
         -> fixed Blender Python applies reversible derivative edit
         -> new .blend / fresh renders / GLB / checksums
         -> stop after 3 recipes or on any unsafe/uncertain result
   |
   +-- read-only manager-governance-v3 supervisor snapshots/events
         -> ChatGPT hourly supervisory check, or user-initiated
         -> owner visual approval ONLY after independent artistic QA
```

**Manager V3 observes the art worker and director; it does not invent tasks or confer permission to merge.** The external ChatGPT hourly automation is distinct from systemd and cannot be treated as a continuous running process. The fixed worker continues to poll after jobs are exhausted; polling by itself is **not** continuous modelling.

## Roles and permissions
| Component | Can do | Cannot do |
|---|---|---|
| Owner | Approve scope; approve exact art assets; authorize production merge | Delegation never implies final approval |
| Manager V3 | Read SQLite/state, flag stale/failed work, publish append-only local events and current receipts | Re-run uncertain jobs, change owner approval, certify artistry or publish |
| Art worker V1 | Execute owner-enrolled pinned Blender scripts; store output/QA; inventory assets | Run arbitrary model-generated shell; silently retry a failed job |
| AI art director V1 | Local vision critique of actual renders; choose among 3 fixed scripts; make derived Blender candidates | Generate and execute new arbitrary code; add paid providers; loop indefinitely |
| Independent QA | Verify actual visual likeness, source/licences, deformation, clips and measured mobile performance | Replace owner sign-off |
| ChatGPT supervisor | Hourly/on-demand inspection; bounded authorized recovery and prioritization | Direct webhook injection into this same chat; independent artistic sign-off |

## Immutable visual acceptance target
Three user-pinned source images, **owner reference bytes not yet verified on Dell**:
- Sharma Aunty character turnaround SHA-256 `936b282ebcb1fb9ca5ef47b0ed1b3b471191bb654aa4c2f6925a469dbb667d3b`
- Sharma Aunty grand mandap SHA-256 `6802cc9c839fcb6be65da162eed9b4ea9028b938bac4007155597bb412e9760a`
- Wedding runway SHA-256 `5ccb9756a43706f19bd208fdebe3723a252d86e91473771c04510145db2bfd5d`

Art direction: stylized/semi-realistic mature Indian woman; recognizable expressive face, eyes/brows, tortoiseshell spectacles, red bindi, jasmine bun, authentic silhouette, detailed constructed magenta/saffron/gold silk sari with embroidered zari and draped deformable pallu, jewellery, and intricate Indian wedding venue. **A technical skeleton, morphology check or AI description is not visual likeness evidence.**

At the time of this SOP, the independent legacy structural results are **character 5/9, venue 3/6**. The new WIP does export four named clips (`Idle`, `Walk`, `Question`, `DodgeReaction`) and three named morphs (`Blink`, `Smile`, `JawOpen`), but artistic acceptance and actual mobile gameplay performance are **unverified**.

## End-to-end process and state transition
1. **Intake & authorization:** Require explicit owner task, scoped project branch, immutable reference hashes, source provenance, permitted no-cost/local compute, tool admission, no-production boundaries. Persist hash-pinned scripts in `ai_director_enrollment.json`.
2. **Inventory and modelling baseline:** Verify licensed foundations before reuse, retain all prior .blend files, baseline SHA-256, GLB import/export, bone weights and render. Missing or ambiguous commercial licences are a stop condition for final use.
3. **Model readiness:** Confirm Ollama exposes `qwen3-vl:2b-instruct` in `/api/tags`; a running pull does not count. If absent, the director emits `waiting_for_local_vision_model` and does **not** claim a reviewed cycle.
4. **Image critique:** Feed the actual current render to the local vision model. For V1, it compares the photo with a *textual description* of the pinned target, **not** actual reference pixels; report image hash, model, defects and uncertainty. Correct before claiming comparative art QA.
5. **Restricted revision:** The director selects exactly one unused allowlisted profile (`glasses`, `jasmine`, `zari`). Inputs/scripts must match SHA pins. No AI-generated commands are executed. It writes only a new staged editable .blend, leaving previous files intact.
6. **Build and test:** Render fresh neutral front, three-quarter, smile and blink evidence; export GLB; check real GLB JSON for 4 clips and 3 morphs; produce file hashes, exit codes, logs and machine-readable receipt.
7. **Decision:** If tests fail, record a review-blocker; if technical checks pass, mark candidate **needs visual review**. Do not infer improved likeness from counts, size, brightness or model confidence. After 3 allowlisted revisions, stop with `needs_independent_creative_review`.
8. **Human/independent acceptance:** Check actual side-by-side reference images, anatomy, drape, hands, expression, jewellery, mesh/rig deformation and 9:16 framing; independently test game-ready GLB in Three.js and measured Android FPS. Require an explicit owner receipt for exact candidate SHA(s).
9. **Release gate:** Only after independent QA and owner sign-off may a separate authorized production workflow consider merge/deployment. This workflow does **not** approve, merge, deploy or spend.

## State machines
**Fixed art jobs (SQLite)**: `queued -> running -> completed` OR `running -> needs_review` on error/uncertainty. No implicit retries from `needs_review`. Current known jobs: `render_study=completed`, `foundation_inventory=completed`, `opencode_art_critique=needs_review` (timeout exit 124). Additional jobs require bounded separate admission.

**AI director**: `enrolled -> waiting_for_local_vision_model -> running -> candidate_needs_visual_review` (repeat for at most three profiles) -> `needs_independent_creative_review`. Failure alternatives: `blocked_art_source_integrity`, `blocked_missing_visual_evidence`, `needs_review_cycle_failed`, `needs_review_existing_output`, `needs_review_uncertain_prior_run`. Running interrupted without a receipt must not be blindly replayed. **States do not equal artistic grades.**

## Cadence and evidence
- `bhm-shaadi-art-worker.timer`: ~2-minute **queue polling**, not a modelling guarantee.
- `bhm-shaadi-ai-art-director.timer`: **30-minute fallback local cycle**; not a ChatGPT reminder. Only progresses if Ollama model and all guard conditions are satisfied.
- Manager controller: ~20-second observation tick, with local `manager-governance-v3/latest.json`, `events.jsonl` and worker/director summaries.
- ChatGPT `Sharma Aunty Manager Review`: hourly conditional supervisory review; may retrieve events and selectively alert on genuine improvement/blockers.

Evidence required each cycle: model ID, actual image/input SHA, chosen recipe and script SHA, source/output .blend SHA, PNG SHA and camera identity, GLB SHA, action/morph verification, errors, QA decision, and owner-approval status. Store local full binary evidence; commit only appropriate code/docs and approved shareable thumbnails to isolated Git branch.

## Global invariants
- Read-only governance observations and append-only local events do **not** independently prove remote attestation or visual quality.
- Never write `certified=true`, bypass the asset manifest, or self-generate the owner's approval receipt.
- No Cline/Prefect installation, production branch merge, unrestricted tool execution, payment, external media publication, or cross-project worker enrollment from this SOP.
- Failed quality pin remains failed until both independent evidence and owner visual approval exist.
- Detailed triage, exact paths and rollback: [Operator Runbook](./AI_ART_DIRECTOR_OPERATIONS_RUNBOOK_20261026.md).

## Operational correction: vision decision schema V2 (verified 2026-10-26)
The first real local Qwen3-VL image inference and bounded Blender edit **completed**. It produced a spectacles derivative (editable SHA-256 `1cbf7767bc5289e16fadb1af201baf1a40a9a36fd08d43a5d0bd7a9c89b51f88`), four review renders and a glTF export (`25b40673c2691b3c2ba5707e5eb7cb7dfba613f238d70047cdfd64957b29b251`) containing all required named actions/morphs. **Artistic QA still FAILS.**

Independent validation found the first model response was **truncated / nonparseable JSON**. The old selector then picked `glasses` as its default unused recipe. This means the model did evaluate the candidate, but the recipe choice was a bounded deterministic fallback, **not a validated model decision**.

To prevent this from recurring, the director now:
- Requests schema-constrained JSON using the local Ollama `format` contract.
- Requires three defects and a valid, non-empty modelling instruction, plus an available `glasses`/`hair`/`sari` priority.
- Rejects malformed, disallowed or already-consumed priorities; **no fallback recipe** and no blind retry.
- Sends the list of remaining permitted profiles to the model; a failed structured response remains an explicit review blocker.
- Maintains original source hashes, script SHA pins, max three allowed profiles, local review-only scope and explicit owner approvals.

The patch passes eight dedicated director contract tests; Manager regression suite passed 27 tests. The **next strict-schema cycle** was running at 02:48 IST and must not be called complete without its own terminal receipt. Visual target reference image bytes remain absent from Dell. This paragraph supersedes the earlier statement that no cycles have yet completed, but does **not** supersede the artist-quality gate.
