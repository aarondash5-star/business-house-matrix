# Business House Matrix Marketing Brain — Andaz Stage A isolated implementation and QA
**Date:** 23 October 2026 IST (worker terminal UTC dates 22 October).  
**Scope:** User-approved Stage A only: isolated signed reviewer evidence, date-specific OTA checkout contract, source-to-claim QA, stale legacy fixture correction and offline regressions.  
**Disposition:** **STAGE A ISOLATED IMPLEMENTATION PASS**. **Stage B signed extractor activation NOT AUTHORIZED**. No real Andaz competitor/price facts certified.

## Sources, implementation branch, and protection
- Source of truth: [Andaz handover](../handoffs/MARKETING_BRAIN_ANDAZ_FINAL_HANDOVER_2026-10-23.md), [Andaz pricing QA](ANDAZ_COMPETITOR_PRICING_QA_2026-10-23.md), and [extraction threat review](ANDAZ_SIGNED_EXTRACTION_SECURITY_REVIEW_2026-10-23.md).
- Stage A code committed to existing unmerged draft PR #4 branch **\`feat/marketing-research-engine-20261022\`**:
  - [\`marketing/andaz_stagea_evidence.py\`](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/marketing/andaz_stagea_evidence.py)
  - [\`marketing/test_andaz_stagea_evidence.py\`](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/marketing/test_andaz_stagea_evidence.py)
  - [\`marketing/patches/andaz_stagea_legacy_fixture.patch\`](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/marketing/patches/andaz_stagea_legacy_fixture.patch).
- No code merged, services reloaded, scheduler added, model tools expanded, source permissions granted, private keys created for production, credentials changed, production website edited, publishing enabled or ad spend.
- Current staged code is not wired into the live Mac v2 relay, marketing orchestrator, original queue, Dell user services, or customer-facing system.

## Implemented in existing isolated host workspaces
- Dell: \`$HOME/bhm-research-expansion-20261022/andaz_stagea_evidence.py\` and \`test_andaz_stagea_evidence.py\`. Mac: \`$HOME/bhm-gsc-multidim-stage-20261022/\` with the same two files; no new service or active timer.
- Both hosts' final **source SHA256**: \`2d056d307cc75e243a33946970454846ec932fdea91e3320da5ea8a7fb0d3e9e\`. Both hosts' final **test SHA256**: \`e7cc4c1bef7e2fdf039a74e795a31ed08f473fd6dfbf6fd77e38cfc7c172efda\`.
- Existing OSI-open-source \`cryptography\` Ed25519 (system Python 41.0.7) reused; no package installation. Keys are **ephemeral offline test fixture only**; no real reviewer enrolled.
- \`source_receipt\`: verifies a trusted issuer's Ed25519 signature, source digest, exact source URL/entity against a *caller-provided trusted pinned registry*, source role/origin, timezone and freshness. Source snippets stay untrusted.
- \`verified_claim\`: requires two signed receipts with distinct pinned origin IDs, at least one first-party source, direct quote present in each receipt, material claim value present in quoted text, same entity, bound claim digest and receipt IDs, active reviewer with configured Ed25519 verification key and role \`human_qa\`, and signed time-bounded approval. Output deliberately says \`cryptographically_reviewed\`, \`publish_allowed=false\`. Free-form reviewer name and unverified URL list no longer count as QA evidence.
- **Extra safety fix discovered during QA:** generic \`checkout_rate\` claims are explicitly rejected by \`verified_claim\`; hotel prices cannot be promoted via the generic entity-claim mechanism.
- \`validate_checkout\`: typed future check-in/checkout, observation freshness, dorm one adult/one bed versus private two adults/one room, AC class, product, live available final-review-before-payment status, INR, base/tax/fee/total exact arithmetic, cancellations, payment terms, inclusions, source receipt ID. Output **always** \`needs_review\`, never booking/reservation/price certification.
- \`comparable_quotes\`: rejects fewer than five distinct properties or inconsistent dates/product/occupancy/AC. Output stays \`requires_independent_checkout_review\` and denies publishing.
- Source and rate provenance/authentication remain separate; these schema functions do **not** retrieve accommodation pages, prove availability, verify supplier checkout source receipts, sign in to OTAs, or certify semantic truth by themselves.

## Regression and debug trail (real terminal receipts)
| Host/workspace | Test | Terminal receipt | Result |
|---|---|---|---|
| Dell isolated Stage A | Final 23 cryptographic/security/checkout cases | \`abbf8f11-89b5-4f76-83a3-7ee7af5f806f\` | **23/23 PASS**, exit 0 |
| Mac isolated Stage A | Same 23 tests | \`74b4f59b-8ad5-405c-966c-587d95555818\` | **23/23 PASS**, exit 0 |
| Dell existing isolated extractor/entities/monitor | 63 regression tests (pre-existing suite) | \`36dd5351-fba7-4b1f-a5ed-ec3d08e8fdb9\` | **63/63 PASS**, exit 0 |
| Mac active Supervisor v2 (read-only test) | 7 regression tests | \`48907716-3863-41da-9480-6d4d592b8e68\` | **7/7 PASS**, exit 0 |
| Mac isolated GSC schema | 11 regression tests | \`48907716-3863-41da-9480-6d4d592b8e68\` | **11/11 PASS**, exit 0 |
| Mac isolated *patched copy* legacy research | 12 regression tests | \`54543437-24b3-4cd2-9d5b-3a1a5516f623\` (also \`48907716-3863-41da-9480-6d4d592b8e68\`) | **12/12 PASS**, exit 0 |

- Legacy patch changes only one assertion: an irrelevant/weak search fixture must be \`insufficient_evidence\`, not \`observed\`. Live \`/opt/business-house-matrix/marketing/brain/test_unified_research.py\` was **not modified**; existing unpatched live fixture remains 11/12 until a separately reviewed code rollout.
- An intermediate strengthened 23-case rerun initially had **22 pass / one expected-error-order mismatch**: changed claim value failed source support validation before reaching reviewer binding. Corrected only its negative test input to \`Panda Hostel\` (supported by both snippets but digest differs), then **23/23 PASS on each host**. No quality gate was weakened.
- No network calls were needed by new Stage A test cases; synthetic dates, signed proof fixtures and local deterministic contract checks only. Full signed Mac→Dell end-to-end extraction is **not** tested or activated by these results.

## Still open / cannot certify
1. **Identity/key enrollment**: \`reviewer-01\` and signed sources in tests are disposable local keys. Actual reviewer identity, role, key custody, revocation, authorized origin registry and signed source provenance require separate reviewed policy and explicit approval. A key signature verifies key possession, not independent real-world human identity.
2. **Transport permission**: draft PR #4 signed \`extract_granted_url\` extension is not activated. Its exact-page grant currently covers only \`https://mokshagoa.com/\` and a W3C page. No Andaz/OTA/source expansion, no connector-safety bypass and no source-to-claim extraction receipt.
3. **Price proof**: Stage A validates rate records structurally but does NOT validate actual live checkout evidence against signed source receipts; 0/5 same-date competitor prices certified, no real availability/cancellation/taxes established.
4. **Competitor research**: Mac Brain retains 2 detected competitor lead names, 0 claim-certified competitors; operator-side shortlist of 6 is discovery only. Human-labeled 10-case accuracy gate, owner property inventory/policies, real Andaz GSC/conversions, 429/cold-boot/soak remain open.
5. **Live regression patch**: corrected only as isolated fixture; requires separate reviewed deployment to live test tree, preserving actual stricter classification.
6. **Editorial**: Reviewer sign-off, Marketing→Design→Dev delivery, site publication and spend all explicitly DENIED.

## Stage B — proposal for SEPARATE approval (DO NOT EXECUTE YET)
**Goal:** a bounded signed public-page extraction proof without broadening permissions by implication.

1. Security owner confirms reviewer key enrollment/revocation and trusted issuer registry; validates code branch against deployed source fingerprints and existing backups; reviews robots, lawful page access, exact origin and rate limits.
2. Propose only **two first-party pilot exact URLs**, if owner/security/robots permit: \`https://www.happypandahostel.com/\` and \`https://thepeacehostel.in/\`. They are candidate grants, **not currently authorized**. No new OTA URLs, login, protected checkout, credentials, or unrestricted model URL fetching.
3. After **separate explicit authorization**, stage signed typed \`extract_granted_url\` through the existing Mac↔Dell paired transport; preserve search envelope and rollback. Revalidate source SHA, TLS/SSRF, redirects, robots, expiry/replay, unknown URL denial, requester/host identity, signed receipts, 512 KB cap and no automatic fact promotion.
4. Run one approved source retrieval at a time and offline negative controls. If integration security denies staging again, stop—never bypass. Record terminal receipts, restore rollback if required, and ask for human audit.
5. Independently certify 3+ competitor identities, 5 date-matched INR checkout quotes and 10 labeled topical cases >=80% only after further provider permission/QA review. **No automatic publication or spending** even if Stage B succeeds.

**Status for owner:** Stage A isolated implementation/code and offline QA complete. **Await Stage B security/activation decision.** PR #4 remains draft/unmerged; Issue #5 remains open.
