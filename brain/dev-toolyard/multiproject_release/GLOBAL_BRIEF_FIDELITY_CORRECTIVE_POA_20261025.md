# Business House Matrix — Global Brief-Fidelity Corrective Plan of Action

**Prepared:** 2026-10-25  
**Status:** **DOCUMENTED / PROPOSED — NOT IMPLEMENTED OR CERTIFIED**  
**Priority:** P0 for the global Dev Tool Yard  
**Owner decision:** All development must use the project-scoped Dev Tool Yard. Preserve working code, authorizations, backups, previous builds and project boundaries.

## Executive decision

Prevent any developer, AI agent, QA worker or tool from **silently weakening the approved brief**, substituting easier implementations that do not meet mandatory outcomes, or presenting technically valid output as design/product acceptance.

**Hard rule:** An approved non-negotiable requirement can only be (a) satisfied with linked evidence, (b) explicitly rejected and returned for rework, or (c) changed by a separate owner-approved, versioned change request. There is no autonomous “close enough” state for critical features.

## Root-cause incident: Delulu Tech logo animation

- Approved intent: physically plausible/impossible **folding, twisting, dimensional ribbon**, front/back surfaces, geometry crossings, material light response, shadows, and final lock to the frozen Impossible Ribbon SVG.
- Built: Python-based 2D progressive SVG reveal with mask, white/violet/lime overlays. This produced a valid 4-second animation and passed codec/color/playback QA but **contained no modeled folds, backfaces, self-occlusion, physical shading or camera parallax**.
- Governance gap: having a Gaming Dev Toolkit installed was confused with actually using a suitable geometry renderer; technical QA was promoted as creative QA; independent visual inspection never gated presentation.
- Owner rejected the work as “vanilla” and without folds. The prior logo render **must be classified creatively rejected** and retained as a **known-bad negative regression fixture**.
- Exact approved final brand source SVG SHA-256: `d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368`.
- Scope boundary: existing V2 homepage and sign-in protected Vercel review remain unchanged until separately approved; no new logo/full-motion publication as part of this POA.

## Existing state and exact limitations

- Dell controller was verified in conversation as **`0.2.2-global-intake-governed`**: project enrollment, owner-pinned brief/contract intake at submission and dispatch, separate owner release preflight, quality evidence records, retrospective technical-only classification. This is a **baseline**, not proof the new controls below exist.
- Dell Gaming Dev Toolkit exists but is **not fully enrolled as a governed autonomous render action**. Its installation is not an execution receipt.
- `quality_gate.py` reviews category/evidence presence and requires independent human review; it does **not yet validate feature-level semantic conformity**.
- External Vercel/Cloudflare/WordPress/GitHub publishing routes can still be accessed outside the Tool Yard's release preflight and are **not centrally intercepted**.
- This POA is **planning/documentation only**; no permission, deployment, controller or website change is authorized by the document.

## Target global lifecycle — mandatory gated chain

```text
Super Brain: frozen owner brief
  GATE 1: signed/versioned requirement traceability matrix (RTM)
Dev/Gaming Brain: capability-fit plan and project-specific tooling
  GATE 2: method/tool fidelity & substitution authorization
Dev Tool Yard: isolated implementation + intermediate artifact checkpoints
  GATE 3: evidence-to-requirement independent QA (visual/functional/negative)
Owner: see actual output and accept, reject or approve a change
  GATE 4: artifact/target/time-bound release authorization
Deployment: actual remote verification + rollback receipt
```

Build status vocabulary is distinct and enforced: **proposed / technically completed / evidence pending / independent QA failed / independent QA passed / owner accepted / release authorized / released**. “Completed” may only refer to the exact stage being measured; never claim design or release readiness because a renderer exited 0.

## Phase 1 — Requirements Fidelity Engine (P0)

Introduce a mandatory RTM and immutable source fingerprint per project/task/manifest:
- `requirement_id`, `source_quote_or_pointer`, `owner_decision_ref`, `criticality`, `nonnegotiable`, `measurable_acceptance`, `evidence_type`, `validator`, `stage`, `status`, `artifact_sha256`.
- Explicit “must do”, “must not do”, allowed substitutions, disallowed shortcuts, visual/UX intent, dimensionality and desired user outcome.
- Store the **exact original owner's words** and meaning along with an implementation-level interpretation; do not replace the original requirement with a shorter proxy.
- Admission rejects missing, conflicting, ambiguous or non-testable critical requirements, unapproved changes and source-hash drift.
- A change request is a separate versioned item requiring owner approval and recalculation of dependent manifests/tests.

**Exit gate:** 100% of critical requirements trace from frozen source to measurable tests with a unique pass/fail criterion and an approval authority; none silently removed.

## Phase 2 — Capability Fit & Implementation Fidelity Gate (P0)

Each development/gaming execution manifest declares:
- exact `requirement_ids`, required algorithms/capabilities and forbidden substitutes;
- specific agent, runtime lane, actual executable/dependency versions and isolated workspace;
- method-level preflight proofs and capability smoke tests, not merely presence of installed libraries;
- expected checkpoints, failure exits, max runtime/thermal controls, source and output hashes.
- Any developer-requested convenience substitution must be blocked until the owner accepts a documented change.

**Delulu test:** 2D mask + color sweep is formally **noncompliant** with “visible physically modeled folding ribbon,” even if 120 frames and correct palette pass. For actual fold method, require animated geometry normals/hinges/occlusion backed by rendered frames.

**Exit gate:** The planned method is capable of meeting every critical requirement, and the specific execution used that method; passing installed-library checks alone is insufficient.

## Phase 3 — Independent Product / Design QA Brain (P0)

Independent evaluator cannot approve its own development receipts. Separate identities, roles and writable directories for developer, evidence collector, independent QA and owner approvals.

- Execute functional and negative tests for software; actual Playwright browser states for websites and applications; actual sampled video frames and playback for media/games; accessibility/performance/security where applicable.
- Every mandatory criterion must be tied to `requirement_id` and original approved evidence, plus a tool/version/time stamp, artifact hash and observation.
- Require real visual material for visual claims. A **text-only LLM critique is not visual QA**, and a test file that exists is not necessarily evidence its critical motion or behavior is visible.
- Validate evidence origin/integrity, reject fake screenshots, made-up scores, self-graded passes, stale frame sheets, wrong viewports and cross-project re-use.
- Do not use model disagreement as an excuse for auto-approving. Independent human review + owner acceptance remain separate where specified.
- Require defect severity, repro steps, owners and retest receipts.

**Exit gate:** All critical `requirement_ids` independently pass **semantic acceptance**; zero P0/P1 blockers; failed/untested cases are explicitly not sign-off.

## Phase 4 — Global Governor & Release Boundaries (P0)

Upgrade existing `0.2.2` in a versioned feature branch with a guarded installer, exact runtime SHA pin, isolated preflight, regression tests, rollback and readback verification:
- gate at task intake, dispatch, intermediate design checkpoint, claim creation and release;
- owner approvals stored outside developer write access and bound to exact brief/contract/implementation/artifact hashes and expiry;
- no ability for a worker to relabel failure as owner approval;
- centralize Vercel, Cloudflare, WordPress, GitHub Pages and other supported **publishing** paths through a separately authorized mediation layer. Prevent credential bypass where technically controllable, and record explicit coverage gaps elsewhere. Do not claim global protection while external routes remain outside the gate;
- prevent requested `preview` deployments unexpectedly returned as `production` from silently proceeding as correct environment. Preserve sign-in protection and rollback.

**Exit gate:** Withheld/expired/wrong-environment approval stops all governed promotion routes, and connector coverage is measured and honestly reported.

## Phase 5 — Adversarial Regression & Cross-Project Certification (P0)

Maintain synthetic **known-bad and known-good** fixtures across web, UI/UX, animation/game, mobile, backend, automation and media:
1. Original Delulu 2D masked render must be **rejected against the physical-fold brief**, despite correct duration/logo/color/playback.
2. Genuine fold geometry with matching actual images may advance to **owner review**, not autonomously to “approved”.
3. Missing/simplified must-have feature is rejected.
4. Falsified screenshot, stale artifact, wrong hash, wrong manifest, cross-project data, self-signed owner approval, expired release record or target drift is rejected.
5. Installed but unused toolchain is not recorded as executed.
6. Existing compliant website builds remain admissible; no retroactive destruction of task records.
7. All protected production apps, sites, source repos and device root policies remain unchanged.
8. External publishing bypass attempts are rejected on routes under policy control and explicitly logged as uncovered otherwise.

**Exit gate:** 100% of required known-bad critical-feature fixtures are rejected, all required known-good fixtures pass the correct **stage**, controlled rollbacks pass, and owner approves gradual deployment.

## Proposed implementation order and evidence

| Sequence | Work product | Required acceptance receipt |
|---|---|---|
| 1 | RTM schema + owner-approved frozen-brief import | Missing critical feature fails prebuild intake |
| 2 | Implementation method/capability checker | Wrong algorithm or unused game lane fails |
| 3 | Independent QA executor + evidence checker | Real outputs pass/fail requirement-by-requirement |
| 4 | Controller/approval isolation + publish adapter coverage | Unauthorized release paths reject; rollback works |
| 5 | Multi-project adversarial suite | Legacy Delulu animation fails creatively; honest certified matrix |

Estimated effort **3.5–7 engineering days** (rough planning only, not scheduling). No background execution implied.

## Handover and operational directives

- Treat this document as the **corrective POA source of truth**; reference existing `GLOBAL_ENFORCEMENT_V022.md` and `QUALITY_RELEASE_STANDARD.md` as baseline, and `projects/delulu-tech/docs/MOTION_REJECTION_AND_IMPOSSIBLE_FOLD_V2_20261025.md` as the negative test example.
- Start by **auditing actual controller/runtime, task schemas, permission boundaries, gaming lane and release connectors before modifying**.
- Use Dell Dev Tool Yard for all code and tests; document with Git branch, PR, exact receipts and registry entry. Preserve prior branches and previous user-approved website designs.
- Execute phased fixes only on explicit continuation request. Never claim any of these new phases is implemented merely because this document exists.
- After permanent correction is independently certified, return to Delulu's owner-approved **Impossible Origami** direction with five review keyframes before full render, private staging only; final public publication separately authorized.

**Document-only checkpoint as of 2026-10-25:** No implementation of these phases or deployment is claimed.
