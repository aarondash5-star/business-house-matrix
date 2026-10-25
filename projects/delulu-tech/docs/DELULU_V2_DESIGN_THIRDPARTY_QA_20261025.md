# Delulu Tech V2 — Design QA & Independent Third-Party Audit
**Date:** 2026-10-25  
**Scope:** Vercel sign-in protected V2 `https://delulu-tech-v2-review.vercel.app`  
**Decision:** **NO-GO for design acceptance / public launch.** Technical prototype passes smoke tests. **Read-only audit; site unchanged.**

## Evidence and provenance

- Actual Vercel deployment: `dpl_CGPwahWyishGqKQNm51aQjum9AqU`, `READY`, no alias error; Vercel's API reported target **production** despite request `preview`. This is a separate V2 review project and no main brand domain was attached. SSO Protection confirmed enabled on **all** deployment types.
- The protected URL returns Vercel login to unauthenticated clients. We did **not** bypass authentication or claim to browser-test the private URL as a logged-in user. This review checks the Dell mirror of the *exact deployed asset hashes*, with Vercel's deployment file tree separately confirmed:
  - index.html SHA1 `b53e6ab3f2ee40ecd54a6e7f65a99d9130ba10da`
  - logo SVG SHA1 `40abdc9e28e93258a4c2595e3cb1767e90a674e8`, owner-frozen SHA256 `d100714ef9579af8e2e4b3385ad5984dec922e331888539077a66e5d4a1d6368`
  - landscape preview WebM SHA1 `ffecf7b9ccc706218d30035abc39f822dfc5de6d`
  - portrait preview WebM SHA1 `59be658490f99b254c2cca2ea0326f2c655437eb`.
- Dell independent QA evidence: `/var/lib/generic-linux-automator-exec/delulu-site-v2-20261025/projects/delulu-tech/staging/v2-vercel-review/qa-evidence/independent/`, including `audit.cjs`, `independent-qa.json`, actual screenshot captures and `framecheck/`.
- Accessibility scanner: external OSS **axe-core 4.10.3** browser-injected locally, with source integrity SHA256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`. Browser: Google Chrome via Playwright on Dell. The deployed files themselves were not changed.
- External language-model review: Groq-hosted Qwen 3.8 27B free-slot (Mac Marketing Brain). **Text-only, not image review, not independent human sign-off**. Two review prompts returned provisional 6.5/10 and 4/10, but the lower result incorrectly asserted the Vercel project was unprotected. That assertion is contradicted by Vercel's live SSO `all` configuration; do not quote 4/10 as a reliable objective score. Corroborated model objections are CTA dead-end, ARIA markup, absent visual sign-off. The reviewer tool capped output to 240 tokens and one long structured response was truncated.

## Confirmed technical passes

- Vercel READY / no alias error; sign-in required. No observed unauthorized public access.
- Original frozen logo SHA verified; correct ink, white, violet, volt palette; static end frame visible.
- No unexpected horizontal overflow or JavaScript page errors on desktop 1440x900, tablet 768x1024, mobile 390x844, small mobile 360x780 and reduced-motion mobile 390x844.
- Video is 4 seconds, 30 fps, 120 frames each in original masters; browser preview copies are VP9 WebM `960x540` landscape and `540x960` portrait. Do not mistake preview resolution for the high-res master resolution. No audio.
- Independent frame sample: both preview videos black at start, visible progressive white reveal by 0.6–1.2s, violet highlight around 1.6–1.8s, lime climax around 2.2–2.4s and stable white lockup from 2.6s onward. This verifies color/timing presence, not aesthetic sophistication or physical depth.
- Normal Chrome **viewport** capture shows desktop logo; apparent blank logo in **full-page** capture is a headless screenshot compositing artifact. This is not a confirmed product defect.
- Reduced-motion correctly suppresses video. Internal anchors valid; skip-motion functionality previously tested.

## Verified blockers

| Severity | Finding | Evidence / user impact | Required acceptance test |
|---|---|---|---|
| **P1** | Primary CTA is not meaningfully visible in first viewport | At 360×780 its top is y=833 (53px below fold); at 390×844 top y=840 (only 4px exposed); desktop 1440×900 y=882 (18px visible). Oversized hero pushes the user action below the fold. | CTA fully visible in initial viewport on 360×780, 390×844 and 1440×900 without diminishing approved logo motion. |
| **P1** | CTA promise has no completion path | Header **Get curious** links `#contact` but that section has no email, form, messaging or other contact mechanism; only **Back to the beginning**. This is a dead-end for a visitor expecting to contact the company. | Provide owner-approved real contact method or relabel/restructure navigation to remove a misleading conversion promise. Do not invent addresses or handles. |
| **P1** | Invalid ARIA markup | **axe-core 4.10.3**, `aria-prohibited-attr`, impact **serious** at `div#logo-motion` with `aria-label` but without valid semantic role; 1 violation at desktop/tablet/mobile/default. Reduced-motion returned zero violations for this rule. | Use valid semantic role or remove redundant aria-label in favor of descriptive SVG/img alternative; axe serious/critical violations zero. |
| **P2** | Animation-skip target undersized | Bounding box height **23px** across default viewports. 44px is recommended touch target; nominal WCAG 2.2 24px target criterion has spacing exceptions, so do not overstate a conformance failure without full analysis. | Aim for ≥44px comfortable touch target and visible focus. |
| **P2** | Mobile navigation target only 38px tall | Header Get curious bound `height=38` at 390 and 360 widths; below widely recommended 44px. | Enlarge target while preserving clean header. |
| **P2** | Brand story lacks concrete next step | Main content is a manifesto and 3 abstract cards (Imagine/Make/Play). No actual product, work, use case or validated capability. This may be acceptable for a private concept but does not yet constitute a complete, conversion-ready business website. | Owner approves intended audience, destination and real offerings. |
| **P1 process** | Vercel preview target mismatch | Deployment API target **production** despite explicit `preview` target; V2 is contained in separately named project and SSO protection is verified **all**. This is a workflow violation, **not** demonstrated security exposure. | Future deploys must verify returned target before promotion and use a true preview environment. |
| **Gate** | No independent human design / owner sign-off | Tool Yard quality gate `evidence_not_passed`: independent_review pending. | Review actual site in authenticated browser; approve visual evidence and corrected release artifact. |

## Independent reviewer reconciliation

External Groq/Qwen text reviews were informative but inconsistent; neither inspected screenshot or animation images. One generated a **false P0 security allegation** despite the explicitly supplied sign-in protection; that is discarded. The other classified the ARIA defect as P0, but the objective scanner calls it **serious** and the team assigns **P1**. The CTA dead-end and missing independent visual approval were valid, corroborated findings. The numeric model outputs are **not** release certifications.

## Verdict / next steps

**Design QA: CONDITIONAL FAIL. Third-party accessibility QA: FAIL (one serious axe violation). Functional/browser QA: PASS. Logo/color/animation timing: PASS technical verification; aesthetic sign-off pending. Remote authenticated end-to-end browser QA: NOT PERFORMED.**

Fix in this order through owner-approved Dell Dev Tool Yard: (1) hero first-screen composition and CTA visibility, (2) real owner-approved contact/CTA flow, (3) ARIA and touch targets, (4) updated browser/axe audits plus actual screenshot/time-series review, (5) owner sign-off, (6) target-verified Vercel preview re-deploy. Preserve V1/V2 artifacts and never auto-publish production.

This document records evidence only and makes **no site modifications**.
