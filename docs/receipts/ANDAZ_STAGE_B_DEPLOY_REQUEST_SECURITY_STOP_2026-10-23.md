# Business House Matrix — Stage B deployment request / certification gate decision

**Date:** 2026-10-23 IST.
**User request:** "Deploy and finish b" following earlier explicit instruction to stop upon a connector safety gate denial, and later authorization to use a secure Supabase handshake.

**Decision:** USER DEPLOYMENT AUTHORITY RECONFIRMED, but **RELEASE STOP**. No platform/connector security-owner authorization for Mac execution is recorded. Route substitution through Supabase cannot be used to carry a Mac operation the platform rejected.

## Current read-only observations
1. [Security Issue #14](https://github.com/aarondash5-star/business-house-matrix/issues/14) is open, no assignee and no recorded authorized security approval. Its comments are implementation/status requests, not a granted platform exception.
2. [Draft PR #4](https://github.com/aarondash5-star/business-house-matrix/pull/4) remains open, **draft**, **unmerged** and no assigned reviewers. The existing branch `feat/marketing-research-engine-20261022` contains all five expected preflight files:
   - `marketing/andaz_stageb_fixed_attestation.py`
   - `marketing/test_andaz_stageb_fixed_attestation.py` (14 offline cases)
   - `marketing/andaz_stageb_mac_collector.py`
   - `marketing/test_andaz_stageb_mac_collector.py` (14 offline cases)
   - `marketing/schemas/linux_mac_fixed_attestation_v1.json`.
   Source presence and test definitions checked via GitHub. Prior reports record **14/14 verifier + 14/14 collector local offline test passes**; **no new host-side tests or CI test receipts in this turn**.
3. Independently attempted site policy verification for exactly `https://www.happypandahostel.com/robots.txt` and `https://thepeacehostel.in/robots.txt`. Public web retrieval returned the tool's inaccessible/internal result for both. Local isolated curl DNS checks also failed (exit code **6**, cannot resolve either hostname in local container); **no robots decision can be inferred from these environmental failures**.
4. Read-only public first-party [Happy Panda policies](https://www.happypandahostel.com/policies/) concern guest bookings/cancellation and age rules, **not automated crawling permission**. Read-only public [The Peace homepage](https://thepeacehostel.in/) describes accommodation and services, but no confirmed site-specific automated-extraction permission. **Neither competitor site passed a robots/terms authorization gate.**
5. Latest *historically verified* Supabase transport state from preceding read-only receipt: project `saczglesalubroyaucqe`, active Generic SSH Edge version 7 (runtime v1.2.1), signed research relay Edge v2, both host heartbeat/registration and 43 stored completed relay jobs. This is not live attestation nor an exemption from the earlier **Mac fixed-function `linux_probe` pre-execution safety rejection**.
6. No verified new enrollment of human reviewer and source-signature production identities; no authorized Stage B live Mac attestation, no exact-page signed retrieval or negative live security smoke receipt.

## Mandatory release gates
| Gate | Result |
|---|---|
| User authorizes deployment | YES, subject to higher-priority platform/connector safety |
| Collector + verifier + typed schema code prepared | YES, review branch only |
| Offline 28-test local historical QA | PASS reported previously, no new live claim |
| Verified security-owner identity, signature and decision | **NO** |
| OpenAI platform safety clearance for Mac action | **NO**; existing fixed `linux_probe` previously denied |
| Production Mac-side fixed-function collector installed | **NO** |
| Approved additive Supabase MCP tool versioned rollout | **NO** |
| Exactly two source robots/terms clearances | **UNKNOWN / NOT PASSED** |
| Vetted real reviewer/source trust identities | **NOT ENROLLED** |
| Signed Mac↔Dell exact extraction and negative live tests | **NOT RUN** |
| Stage B certified and released | **NO / BLOCKED** |

## Next authorized release steps (once real decisions exist)
1. Obtain explicit action-specific clearance from the connector/platform security owner for a **typed, nonce-bound Mac read-only attestation**, not a generic Mac shell or indirect rejected operation. Request a trace/rule remediation for the former `linux_development_run` and existing `linux_probe` denials.
2. Review attestation schema and code, fix any security review findings, record pinned signing key provenance, file fingerprints, immutable release artifact hashes and rollback plans. Use the *existing* Supabase gateway only through its authenticated, formally registered tool; do not enqueue another path or mutate existing jobs.
3. Have source legal/robots policy verified for the two exact authorized competitor homepages or secure the site owner's written access permission; do not assume permission when DNS/tools fail.
4. Vet real reviewer and extractor identities, complete isolated negative security tests, then run bounded one-at-a-time signed exact-page Mac/Dell tests only if the approved connector action is available and passes all controls.
5. Record host task IDs, terminal exit codes, reviewer signoffs, all denied-URL negatives, QA, restore points; only then classify Stage B pass/fail. No unrestricted root, spending, publishing, unrelated URL expansion or production-site mutations.

**Changes in this turn:** documentation/review coordination only. No live Edge Function deployment, worker commands, Supabase direct job insertion, root/permissions alteration, new source grants, PR merge, site publishing or spend.

**Canonical handover:** [MARKETING_BRAIN_ANDAZ_FINAL_HANDOVER_2026-10-23.md](../handoffs/MARKETING_BRAIN_ANDAZ_FINAL_HANDOVER_2026-10-23.md).
