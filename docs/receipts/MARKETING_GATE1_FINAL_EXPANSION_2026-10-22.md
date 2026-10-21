# Marketing Gate 1 — final expanded research acceptance

**2026-10-22 IST | Independent Business House AI Matrix**.

## Verdict

**CORE GATE 1: PASS (already certified 21 October).** Durable autonomous Mac–Dell private signed/encrypted SearXNG research, source URLs, quota, zero paid fallback, network interruption recovery, replay resistance, untrusted-content checks. Original immutable [certification](MARKETING_GATE1_CERTIFICATION_2026-10-21.md) remains authoritative.

**RESEARCH EXPANSION: PASS for live manual/orchestrated WordPress GSC→Mac transfer, autonomous Mac consumption, idempotent replay, and Google Trends cached research.** The remaining *separate* certification is a **future scheduled ChatGPT automation run**, which is now enabled but has not yet executed for the first time. Do not claim unattended daily GSC updates already observed.

## Fresh evidence

- Mac and Dell Generic SSH heartbeats ONLINE as of 2026-10-21 19:37 UTC.
- Mac `searxng_research.py status`: signed/encrypted paired relay enabled, `self_hosted=true`, `paid_fallback=false`, 3 used/100 per day; last outcome `ok`.
- Mac `trends.py status`: official RSS enabled, geos IN/GB/RU/US, 10 cached observations, zero fake historical index data, no paid trends API.
- Mac `router.py validate`: `valid:true,connections:5,paid:false`.
- Four protected Mac services `generic-linux-automator`, `cron`, `mbpfan`, `thermald` ACTIVE, `brain.py status` completed 15, publish/spend OFF, no Mac GSC OAuth token.
- Authentic WP Manager site `79e365b9-fdbb-42cc-82c4-78d7fb8d344f` is Moksha Wellness Goa. WP `gsc_status`: `connected=true,configured=true,scheduled=true`, `webmasters.readonly`, previous aggregate snapshot 155 clicks / 2448 impressions. Genuine `gsc_search` returns 50 query rows for 2026-09-20–2026-10-18 with Google provenance.
- Previously authenticated Matrix local store contains 50 real GSC records (batch `d08c6c7e079ba074df39ad0aeb588da3`); Mac's existing cron autonomously completed GSC research job `78369f74-4d48-4802-b006-3b54dd6da5ad`, first attempt, 10 matched GSC observations, no publishing.
- Identified and fixed existing per-batch duplicate import implementation which had `INSERT OR REPLACE` on the same batch hash. New implementation returns `unchanged` and preserves original `imported` timestamp and original observations for the same exact source/property/window/row digest; fails closed if a batch hash's provenance conflicts. Changes: `gsc_metrics.py` commit `2c148a53891dc902f633c69972d813f4bf487f2b`; regression test commit `f00938bb82c297af1bdc22bcd2a1c4fe0db2749f`. Source deployed on Mac from pinned immutable GitHub commit with private rollback backups; **50/50 tests PASS** (SSH `54052733-ab70-4503-8916-e1b726d2bde6`, exit 0).
- **Fresh real-source replay test:** re-read WP Manager's 50 real GSC rows and passed only metrics to the Mac importer via private Generic Linux SSH. Importer returned `status=unchanged`, original batch `d08c6c7e079ba074df39ad0aeb588da3`, same 50 rows, **1 batch**, original timestamp unchanged. SSH receipt `64693bf8-6930-45e7-9bef-9b33ffe7b7da` `completed/exit_code=0`.
- Daily **Matrix GSC Daily Sync** ChatGPT automation already created/enabled, ~08:00 IST, verifies WP Manager source/property/read-only scope and private SSH transfer of metrics only; **first task run has not occurred**. Strictly require a separate future receipt before certifying recurring scheduled runs.

## Security and limits

No Google OAuth or WP bridge token on Mac, no public search/GSC listener, no third-party paid search API, no customer/booking data, no Mac root permission or network changes, no publishing/spending, no rendering guard bypass, no automatic Moksha Master sync. The automation relies on connected account tools; if credentials, plugin session or services become unavailable, fail closed and flag the blocker. Tool `gsc_search` explicit date inputs currently fail its double-escaped regex; use provider-default settled dates until fixed.

**Gate 1 exit decision:** research infrastructure and data integrity VERIFIED; proceed to Gate 2 only with its existing thermal safety threshold and required original-media rights checks. The automatic scheduled *daily cross-system* refresh should be checked on its first future run, not retrospectively marked passed.
