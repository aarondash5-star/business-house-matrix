# Business House Matrix — Marketing Department Development Status and Takeover

**Checkpoint:** 2026-10-22, late evening IST  
**Project boundary:** Independent Business House Matrix, not Moksha Master. Moksha and Andaz are authorized research test subjects only.  
**Status:** Autonomous queue and source-gathering MVP **LIVE**. Complete research reports and autonomous finished creative production **NOT CERTIFIED**.  
**Primary live hosts:** `mac-linux` coordinator; `dell-linux` research and private staging.  
**Public repo safety:** No secrets, customer records, private analytics rows, staged images, SQLite databases or privileged tokens in GitHub.

## 1. Executive development scorecard

| Capability | Status | Verified evidence / important limitation |
| --- | --- | --- |
| Mac/Dell authenticated SSH workers | **LIVE** | Both online at this checkpoint; owner-scoped read-only probes completed |
| Marketing Brain Python/SQLite task queue | **LIVE** | `brain.py status --verbose`: **28 completed**, no queued/running jobs at check; no auto publication or spend |
| Autonomous worker/scheduler | **LIVE** | `bhm-marketing-queue-worker.timer` **enabled/active**; self-run research and deduplicated ping passed; user lingering enabled; no full cold reboot test |
| Marketing Brain task routing | **LIVE, LIMITED** | `research_search`, `research_brief`, `research_market`, hosted drafts and media preflight/review task interfaces; no end-to-end final marketing deliverable orchestrator |
| Mac–Dell research transport | **LIVE** | Existing device-paired sealed/signed v1 SearXNG route and narrow v2 market packet route tested, original route backward-compatible |
| SearXNG on Dell | **LIVE** | `bhm-searxng` active/enabled, local service only; public search can rate-limit |
| Dell research API | **LIVE** | `bhm-marketing-research-api` active/enabled, `127.0.0.1:18890`, HTTP health `ready` v1.3 |
| DuckDuckGo / Opera fallback | **FUNCTIONAL, UNSTABLE SOURCE** | DDG via SearXNG had results, intermittent CAPTCHA/unavailability; isolated public Opera fallback real smoke and synthetic-trigger fallback passed; no CAPTCHA bypass, shared credentialed tabs untouched |
| Trafilatura page extraction | **LIVE, GUARDED** | On Dell for exact approved public URLs; real pages collected, robots/TLS/IP/redirect checks, bounded excerpts. General arbitrary web extraction is deliberately unavailable |
| Research memory and change detection | **LIVE LOCAL** | Dell private 0600 SQLite FTS5; normalized visible-text hashing; five-page second live run returned 5/5 unchanged |
| Business entity / claim checks | **FUNCTIONAL, REVIEW-GATED** | Social/own-brand listings distinguished from provider leads; prices require manual corroboration, none automatically verified |
| Search Console ingestion | **PARTIAL** | Mac existing 99 property query rows, read-only. Separate isolated 12 authentic three-dimensional `query,page,date` rows; linked route caps at three dimensions; no verified country/device joint report |
| Google Trends | **LIVE RSS, LIMITED** | Mac 40 public national-news RSS observations; recurring Trends cron preserved; **zero genuine historical indexed series**; cannot infer localized Goa demand |
| Hosted Groq planning/copy models | **PREVIOUSLY LIVE, NOT RECHECKED THIS TURN** | GPT-OSS and Qwen Groq pilot previously returned receipts; provider availability, current rate budget and precise licenses should be rechecked before relying on them |
| Local models on Mac | **PAUSED** | Local inference disabled after high Mac temperatures; fresh sensor spot read 59°C is not sustained safe rendering proof |
| Real reel rendering | **NOT CERTIFIED** | Existing Reel Studio/bridge exists; thermal-guarded Mac finished preview and full brand/rights/technical QA pipeline have not passed acceptance |
| Private Moksha website staging | **BASELINE BUILT** | Existing Dell controller active; 9 local nonindexed static HTML pages; mobile 390×820 and desktop 1440×900 Firefox screenshot smoke; placeholders, no authenticated preview link or production deployment |
| Marketing→Design→Dev→QA linked autonomy | **NOT CERTIFIED** | Research packet and staging exist independently; no validated autonomous report→review→design brief→revision→finished preview |
| EVOLUTION continuous learning | **PARTIAL FOUNDATION** | Deterministic outcomes/corrections present in wider Matrix; no fully assessed feedback-driven marketing learning/retraining cycle |
| Social publishing / paid ads / production WordPress edits | **DISABLED** | Explicit gates preserved: `publish_enabled=false`, `spend_enabled=false`; no independent production permissions |
| Main Matrix central UI | **OUTSIDE MARKETING MVP / UNDEPLOYED** | Open WebUI pilot still not deployed per earlier Matrix status; broader nine-department rollout separate from Marketing queue reliability |

**Interpretation:** Source discovery and independent task execution exist. Report composition, fact-certification, creative production and finished end-to-end orchestration are the primary missing capabilities.

## 2. Live Andaz assignment — important outcome

Requested report subject: **Andaz Vibe Stay - Arambol, Goa**. Queue job:
`58b10808-367a-4899-aecc-6e5f76204480`.

Terminal receipt: **completed**, first attempt, **23.116 seconds**, `2026-10-22T15:34:46Z`; signed Mac→Dell SearXNG web mode **observed** with 5 source leads. The five cited domains/pages in its live receipt were:
- Goibibo — Andaz booking listing
- Agoda — Vibe Stay by Andaz listing
- MakeMyTrip — Andaz hostel listing
- Tripadvisor — Vibe Stay by Andaz reviews
- Booking.com — Vibe Stay by Andaz guest reviews

These are largely **first-party-property OTA/review listings**, not an independently verified **competitor set**. `trending_topics.status=no_relevant_observation`; `verified_property_performance.status=property_not_selected`. Most importantly, the result schema had **no** `executive_summary`, `competitor_table`, `pricing_analysis`, or `recommendations`. Therefore: **task execution SUCCESS; actual requested Andaz research report NOT DELIVERED**. The next agent must create a report-composition task using these attributed leads plus independently reviewed competitor sources, clear pricing/date/unit distinctions, audience segments, marketing conclusions and reviewer gate. Do not claim this assignment is a completed report.

## 3. Chronological development ledger

### 2026-10-21 — Department Brain and research infrastructure
1. Created/reused the Mac Marketing Brain: Python jobs/SQLite queue, deduplication and bounded retries, nonroot worker, result receipts; modular hosted inference via Groq; conservative provider policy.
2. Established Dell rootless SearXNG and reusable read-only public research discipline. Deprecated Tavily as the operational research provider. Added Google Trends official RSS refresh, existing per-property GSC read-only ingestion; distinguished RSS headlines from demand index.
3. Existing Reel Studio retained, but thermally guarded; original user assets stored privately; no unrestricted model/automatic publishing.
4. Central Dell autonomous controller and limited Dev QA already existed; no assumption that proposal-only output constitutes built code.

### 2026-10-22 — Transport, research quality and private site staging
5. Established existing Mac↔Dell signed/encrypted research relay across distinct private networks, preserving identity/signatures and per-request receipts. Original SearXNG v1 search continues to work.
6. Upgraded Mac `unified_research.py` to v1.1 relevance/limits QA: **17/17** quality tests; rejected irrelevant or misleading search and Trends/GSC inferences.
7. Autonomous Dell `website_stage` action compiled **nine** Moksha private static HTML pages; **7/7** staging tests, Firefox mobile/desktop smoke, no public server, no production changes. Full visual review, real photos, owner remote preview and creative handoff remain outstanding.
8. Expanded Dell research modules in protected PR #4: Trafilatura extraction, typed entity/source evidence, per-host bounded public crawl, SQLite/FTS5, claim review, monitor contract. After later fixes, **83/83** Dell test suite passed. Earlier Mac QA **17/17** and isolated GSC schema **11/11** also passed at respective prior checkpoints (do not combine these as a single current re-execution).
9. Deployed separate Dell **loopback-only** Research API v1.3, exact-topic market packet and guarded source refresh; preserved open-source architecture, no external paid fallback.
10. Integrated SearXNG DuckDuckGo, then a user-requested **isolated Opera** public-browser fallback. **Opera is proprietary**, an exception specifically requested by the owner to the general OSI-only Matrix policy. Browser use does not authorize credentials, purchases, CAPTCHA evasion, production access or site writes.
11. Extended the *existing* encrypted paired transport with exact `research_market` v2 route; Mac client verified Dell signed response. Existing v1 SearXNG backward-compatibility smoke passed.
12. Added `research_market` to the Mac Brain job contract. Real queue job `d0d30d26-dc6c-430b-a5bf-62d21928c3f4` completed first attempt, 5 source evidence records and 3 **unverified** local provider leads. No automatically certified prices.
13. Fixed transient-markup false positives with reader-visible content fingerprints; two real five-page rounds: initial migration changes then **5/5 unchanged**; corrected social/own-brand classification.
14. Permanent autonomy fix: replaced duplicate-prone opaque two-minute cron worker with **enabled/active** user-level systemd timer polling 40 seconds after previous completion; preserved original guarded `worker.sh`, `flock`, `recover`, backoff and queue receipts; increased bounded runtime to 160 seconds. Old cron worker removed only after success. Google Trends cron left intact. Real `research_market` auto task `b93df5b0-549f-4eda-af64-a65a4ec4c2c5` completed; timer restart and same-key duplicate enqueue/ping completion verified. Full host cold reboot NOT tested.
15. Andaz task `58b10808-367a-4899-aecc-6e5f76204480` completed by autonomous worker with five first-party OTA/review leads, **but no finished analytical report**. This is the latest decisive functional gap.
16. **Live check this document:** Mac queue 28 completed; timer enabled+active; Dell `bhm-searxng`, `bhm-research-relay`, `bhm-marketing-research-api` all active+enabled and `/health` ready; Dell central controller active; private staged `index.html` and a mobile screenshot exist; spot Mac temperature 59°C, local inference still disabled. GSC reports existing 99 query rows, RSS 40 and historical index 0.

## 4. What remains — prioritized executable checklist and exit criteria

### P0: Deliver validated marketing research **reports** rather than raw source packets
- [ ] **Research report composer:** Add a bounded `research_report` task (or reuse a working approved draft/profile) that takes **verified, cited leads** and outputs an executive summary, named competitor comparison, explicit price/currency/date/services table, audiences/segments, SEO, booking-channel positioning, actionable recommendations, limitations and unresolved questions. Test for nonempty complete sections. Avoid unreviewed claims.
- [ ] **Andaz full report:** Rerun or extend the specific Andaz assignment; distinguish its own OTA listings from independent Arambol hostel comparators. Include sources and reviewer-needed flags. Existing task completed only the evidence gathering stage.
- [ ] **Broader research scope:** Current `research_market` exact-topic signed v2 API is **Moksha-only**; Andaz used generic `research_brief`. Architect narrow per-business registry + owner-approved source manifests without arbitrary external fetch or runtime cross-business secret sharing.
- [ ] **Claim verification:** Resolve actual provider identity/operating status, official vs reseller prices, inclusions and contradictions with independent corroboration; implement human review receipts for promoted facts.
- [ ] **Benchmark:** Score at least 10 labeled real searches for named-provider precision, relevance and citations; current broad queries often rank own-brand social posts and generic directory pages.
- [ ] **GSC:** Reuse an authorized no-cost connector giving real `query,page,country,device,date` rows if available, otherwise leave country/device `unknown`. Never synthesize a 5D cross-tab from separate marginals or request paid upgrades automatically.

**Acceptance:** A real Andaz report and a real Moksha report each contain all sections with attributable citations, factual uncertainty and independent reviewed competitor evidence. A queue state of `completed` alone is insufficient.

### P1: Autonomous campaign execution and content production
- [ ] Link research evidence → brand strategy/concept → copy → Design → independent QA → owner review as one durable mission graph with stage receipts and safe retries.
- [ ] Mac Reel Studio: verify sustained thermals and media rights, automate selection/edit/captions/sound using authorized real images/footage, render a genuine **9:16 finished preview**; test FFprobe technical output plus factual/brand checks. Do not raise thermal cutoffs or re-enable heavy local inference by assumption.
- [ ] Moksha website private stage: replace placeholders with rights-verified real assets, generate reviewed responsive pages, complete multi-breakpoint visual and accessibility QA, and offer owner-authenticated private preview **without public WordPress publishing**.
- [ ] Build revision-feedback and EVOLUTION correction receipts: fixes to a report/creative remain auditable, reviewed and restricted; do not let model text self-certify QA.
- [ ] Revalidate live hosted Groq model/provider availability, OSI-license qualification, conservative quotas and cost policy before routine workloads; current provider evidence originates from prior checkpoints.

**Acceptance:** A single unattended research→creative→QA task yields a genuine usable preview/report requiring only owner editorial approval. No model-generated PASS alone.

### P2: Operational reliability and intelligence
- [ ] Certify full Mac/Dell cold reboot, SSH link interruption, service restart, provider timeout/429, queue recovery and non-duplicated idempotent reprocessing under fault-injected tests. Timer restarts have passed; whole-machine reboot has **not**.
- [ ] Add explicitly reviewed competitor URL manifests and bounded periodic monitors only after targets/source terms reviewed. Keep alert noise low with normalized fingerprints.
- [ ] Support campaign analytics, reliable conversions, source-specific GSC/Trends, attribution dashboards and experiment outcomes. No fabricated demand/search volume or return on ad spend.
- [ ] Modularize the pilot per business: Andaz, Moksha and future tenants each have isolated identities/source registries and policy. Do not assume Moksha assets, rooms, bookings or GSC property apply to Andaz.
- [ ] Connect Marketing into central Matrix coordination / controlled Dev support and future approved UI. Central Open WebUI and full nine-department integration are **not yet deployed/certified** under the Matrix-wide status.
- [ ] Merge [research engine draft PR #4](https://github.com/aarondash5-star/business-house-matrix/pull/4) only after review, reconcile source drift with deployed Dell/Mac modules and finalize source quality/CI/safety gates. Track [Issue #5](https://github.com/aarondash5-star/business-house-matrix/issues/5).

## 5. Safety and architecture constraints

- Business House Matrix remains independent from Moksha Master. Do not share customer/guest records, personal secrets or account exports to the public repository.
- Genuinely OSI-approved source and models required unless owner explicitly authorizes a named exception (Opera public-browser option requested; **do not generalize** exception to models or paid services).
- Remote source text is untrusted. Bounded public HTTPS-only research with real citations; robots/SSRF and signed transport controls stay in force.
- No unsolicited posts, ad payments, publication, booking edits, root/security configuration changes or protected logins.
- Local Mac models/rendering remain thermal-gated; a 59°C single sample is not sustained-load clearance.
- Never equate `completed` queue receipt with factually correct / fully authored/approved content.

## 6. Pointers, receipts and rollback

**Canonical repo:** [Business House Matrix](https://github.com/aarondash5-star/business-house-matrix).

- [Marketing AI handover Oct 21](MARKETING_AI_HANDOVER_2026-10-21.md)
- [Research engine upgrade plan/handover Oct 22](MARKETING_RESEARCH_ENGINE_EXPANSION_2026-10-22.md)
- [Live research API/Opera release evidence on PR branch](https://github.com/aarondash5-star/business-house-matrix/blob/feat/marketing-research-engine-20261022/docs/receipts/MARKETING_RESEARCH_API_LIVE_RELEASE_2026-10-22.md)
- [Permanent autonomous queue worker receipt](../receipts/MARKETING_AUTONOMOUS_QUEUE_PERMANENT_FIX_2026-10-22.md)
- [Moksha private staging status](../../tasks/moksha-website-overhaul/STATUS_2026-10-22.md)
- [Moksha private staging runbook](../dev/PRIVATE_SITE_STAGING_2026-10-22.md)
- [Research quality gate report](../receipts/MARKETING_RESEARCH_QUALITY_GATE_2026-10-22.md)
- [Research expansion draft PR #4](https://github.com/aarondash5-star/business-house-matrix/pull/4)
- [Open blockers Issue #5](https://github.com/aarondash5-star/business-house-matrix/issues/5)

**Useful nonsecret diagnostics:**

```bash
# Mac Marketing Brain (nonroot)
cd /opt/business-house-matrix/marketing/brain
python3 brain.py status --verbose
python3 unified_research.py status
systemctl --user is-active bhm-marketing-queue-worker.timer
systemctl --user list-timers --all --no-pager | grep bhm-marketing-queue-worker
python3 brain.py receipt 58b10808-367a-4899-aecc-6e5f76204480

# Dell (nonroot)
systemctl --user is-active bhm-searxng bhm-research-relay bhm-marketing-research-api bhm-autonomy-controller
curl --max-time 5 -fsS http://127.0.0.1:18890/health
```

**Backups and rollback:** Refer to the exact production runbooks/receipts before changing anything. Existing queue timer sources committed on `main`; prior cron saved in `~/.local/state/bhm-marketing-backups/crontab.before-systemd-worker-20261022`. Signed relay and Brain original scripts have dated rollback backups. Leave running services untouched unless repairing a verified issue.

## 7. Shortest next-chat takeover prompt

> Continue Business House Matrix **Marketing Department**, not Moksha Master. Read `docs/handoffs/MARKETING_MATRIX_STATUS_HANDOVER_2026-10-22.md` on main, then verify live Mac/Dell receipts. Priority: turn existing Andaz research job `58b10808-367a-4899-aecc-6e5f76204480` (completed, five OTA/review sources, **not a report**) into a complete cited competitor/market report via reusable evidence→report→QA tasks. Reuse working queue, signed research relay and no-publish/no-spend gates; avoid unnecessary infrastructure rebuilding. Document new receipts and remaining blockers.
