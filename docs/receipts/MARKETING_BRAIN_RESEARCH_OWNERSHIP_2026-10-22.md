# Marketing Brain → Research Worker Ownership Release

**Date:** 2026-10-22, 21:20 IST (approx). **Project:** independent Business House Matrix.
**Observed live status:** Mac Marketing Brain queue **29 completed**, systemd polling remains active; Dell paired encrypted read-only search reused.

## Root cause
The Mac Marketing Brain was a durable task dispatcher and API router, not a supervising research agent. The existing generic `research_brief` task produced five Andaz OTA sources but no final analytical report. Dell's research worker only searched/extracted. Previous assistant turns orchestrated report preparation manually because no Brain-owned report composer/QA stage existed.

## Narrow Brain-owned autonomy deployed

- Added Mac module `marketing_report_orchestrator.py` from `marketing/marketing_report_orchestrator.py` in `main`.
- Registered guarded `research_report` in the **existing** Mac `brain.py` via reversible `marketing/brain_report_task_patch.py`, preserving all previous task types and worker scheduling.
- Mission input: `{"business":"andaz_arambol"}` or `{"business":"moksha_arambol"}`; unknown projects, extra fields, publishing/spending flags prohibited.
- Brain now internally selects predefined business-specific public research queries, calls existing **Mac→Dell signed SearXNG research worker** for each, classifies first-party listings vs independent leads, builds a private Markdown+JSON analytical evidence review draft with executive overview, candidate comparison, uncertain prices, target-segment hypotheses, booking/SEO/seasonal research gaps, suggestions, citations and explicit quality/escalation flags.
- Does **not** install unknown new software, execute arbitrary remote code, bypass CAPTCHA, verify uncorroborated competitor prices or claim rights to publish. This is bounded workflow autonomy, not self-programming general AI.

## Tests and receipt

- Compiler, exact-hunk patch preflight and offline mocked two-source QA contract **PASS**.
- Live task `research_report` for Andaz enqueued with idempotency `bhm-andaz-brain-owned-orchestration-20261022` and UUID `def570d8-8fef-40c5-acff-689ac797f779`.
- Existing Mac **autonomous systemd timer** picked up the queued task; `brain.py status` showed `running`, then `completed` on **attempt 1**, error null, at `2026-10-22T15:49:26Z`.
- Three signed live research queries returned **15** distinct source leads; **10** non-owner source leads, **5** Andaz owner-related booking listings. Example external candidate pages Happy Panda Hostel and Dreamcatcher House & Hostel on Hostelworld/Booking.com. Independent source leads **are not equivalent to ten verified competitors**.
- Private report generated: `/opt/business-house-matrix/marketing/brain/reports/private/andaz_arambol-research-report.md`, JSON adjacent; Markdown 6,120 bytes. Private owner-only directory, **not public Github**.
- QA `REVIEW_REQUIRED`: 0 independently verified sources/prices, `approved_for_customer_facing_use=false`, `publish_allowed=false`, `spend_allowed=false`.
- Existing `research_market`, `research_brief`, `reel_pilot` and raw research search task paths remain intact. No new service, cron or timer created.

## What is *still* missing for a self-managing Marketing Brain
1. A model-driven planning and replanning loop which reads QA failures and commissions new research jobs automatically, beyond the narrow fixed query plans implemented here.
2. Source-verification worker capable of corroborating current facts/price against independent official pages and escalating conflicts to owner.
3. A robust full-length, model-assisted marketing report synthesizer; current report has meaningful sections, citations and research process recommendations but explicitly **does not assert competitive facts or pricing**.
4. Design/media specialist delegation, Mac thermal-safe previews, feedback-driven EVOLUTION, cross-department dispatch and independent evaluation.
5. Full reboot/network-outage recovery certification. No production publishing or spending permission granted.

## Rollback
Mac: `cd /opt/business-house-matrix/marketing/brain && python3 brain_report_task_patch.py --rollback`, after ensuring `research_report` jobs are terminal. Dated original `brain.py.pre-marketing-report-orchestrator-20261022` backup retained. Leave the existing systemd worker, Dell SearXNG, relay and separate business functions operating.

**Next autonomous milestone:** add limited report QA → follow-up research → independent evidence corroboration → long-form synthesis, then test one Andaz run with actual verified competitor identities and pricing. Keep review gate.
