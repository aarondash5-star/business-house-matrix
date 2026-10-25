# Engagement Core CRM — G1 Mobile Design Worker: Frozen Intake Brief

**Project:** `engagement_core_crm`
**Action:** `dev_project_build` (project-isolated reviewed_patch_v1 only)
**Manifest:** `crm_wireframe_g1_v1`
**Quality profile:** `creative_web`
**Owner source:** https://github.com/karanzing1992/engagement-core/issues/75
**Canonical specification:** https://github.com/karanzing1992/engagement-core/blob/main/docs/ENGAGEMENT_CORE_CRM_V1_MOBILE_WIREFRAME_DEVYARD_BRIEF_20261026.md
**Pinned canonical commit:** `2fe3db659a003322adf06e3a12ab51ae90366fac`
**Wireframe source branch:** `karanzing1992/engagement-core:feat/eccrm-mobile-wireframes-g1-20261026`
**Baseline working UI:** `feat/eccrm-tabler-ux-20261025`, Draft PR #74.

## Explicit owner direction (26 Oct 2026)

- "Document this and send the execution to the dev tool yard"
- "Do it also check the yard docs for continuos works and art directors for quality"

These authorize the **G0/G1 wireframe design task and scoped project enrollment**. They do not authorize CRM functional coding, live messaging, real customer data, external channel credentials, installing paid tools or a production release.

## Owner's mandatory G0/G1 design outcomes

1. Preserve Tabler 1.7.0 (MIT) and the working WordPress CRM. No generic grey WordPress admin screens, no placeholder-only navigation and no broken touch UX.
2. Produce 15 distinct, editable screens: S01 Inbox, S02 Conversation, S03 Customer 360°, S04 Pipeline, S05 Deal Detail, S06 Tasks, S07 Channels, S08 AI Assistant, S09 Automation Builder, S10 Campaigns, S11 Calendar, S12 Reports, S13 Team, S14 Integrations, S15 System & Data.
3. Every screen must expose **normal, empty, loading, error and permission-denied** design states, with appropriate user recovery and accessibility affordances.
4. Complete primary navigation and two clickable flows: Inbox → Conversation → Customer 360° and Pipeline → Deal Detail → Task.
5. Mobile-first: 320/360/375/390/414px; 768/800px tablet; 1024/1440px desktop. Zero page overflow, visible focus, 44px touch targets where possible, safe-area navigation and drag-free operation alternatives.
6. Every control must have demonstrable behavior or explicit "design only/unavailable" feedback. Never fabricate provider connectivity, AI responses, send success or database persistence.
7. Include design-system tokens, source licensing, information architecture, backend/API ownership mapping and requirements traceability. Retain existing CRM 27/27 UI and 16/16 backend baseline.
8. Browser screenshot and interaction evidence is necessary. Independent visual/art direction must review composition, legibility, contrast, fidelity to brief, phone ergonomics, complete flows, and deviations. Automated checks cannot self-certify creative excellence.
9. Maintain bounded, project-scoped status monitoring using existing Manager V3. The existing Shaadi-specific 30-minute art director has **no CRM authority** and is blocked on its local vision model; do not share Shaadi state, data, timers or approval.
10. Owner approval remains mandatory for final G1 creative acceptance. No G2+ implementation, PR merge, live publishing or external customer channel activation without separate approval.

## Sandbox and task boundaries

Scope is an isolated reviewed-patch workspace only: `frontend/`, `backend/`, `tests/`, `docs/`. No production WordPress file writes, no external network from Bubblewrap worker, no root/sudo changes, no foreign repo/host paths. All output synthetic. The verified browser test and source branch may be imported as **reviewed inputs**, not as unrelated unverified commands.

Maintain fail-closed cross-project rules. A missing or hash-drifted owner approval record stops controller `dev_project_build`; never self-sign the acceptance ledger. The owner review record must identify the **exact contract SHA** before a governed build is dispatched. This admission proposal itself is not production authorization.

## Quality director and continuous-work rules

- Existing Manager V3 performs event/status observation only; no autonomous new creative iterations.
- A CRM-specific design director may examine actual Playwright screenshots with a verified local/free model or human review, but must report *advisory* defects and cannot approve itself.
- If the approved model is unavailable, return `vision_review_unavailable` and preserve a screenshot pack for owner review. Do not infer PASS.
- Any continuous worker is project-scoped, bounded by one G1 design-only task and a deterministic stop at owner review; no arbitrary worker recurrence, spend, publication or cross-project process reuse.
- The owner must approve any widened privilege, billing, remote integrations or broader persistent automation separately.

**Release designation:** `DESIGN_BUILD_ONLY / USER_VISUAL_ACCEPTANCE_PENDING / PRODUCTION_NO_GO`.
