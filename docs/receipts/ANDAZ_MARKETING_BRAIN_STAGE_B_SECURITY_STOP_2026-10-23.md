# Business House Matrix — Andaz Marketing Brain Stage B security stop
**Date:** 2026-10-23 IST (worker heartbeat 2026-10-22 19:58 UTC). **Scope:** User-approved bounded Stage B only, exact first-party pilot URLs:
1. `https://www.happypandahostel.com/`
2. `https://thepeacehostel.in/`

**Terminal decision: STOP / DENIED BY CONNECTOR SECURITY GATE. No activation, no bypass.**
This is a documented partial review, **not** a Stage B test or deployment pass.

## Approval boundary and sources
- [Latest canonical Andaz handover](../handoffs/MARKETING_BRAIN_ANDAZ_FINAL_HANDOVER_2026-10-23.md).
- [Stage A implementation with terminal QA and proposed Stage B](ANDAZ_MARKETING_BRAIN_STAGE_A_ISOLATED_IMPLEMENTATION_2026-10-23.md).
- [Prior source-extraction security review](ANDAZ_SIGNED_EXTRACTION_SECURITY_REVIEW_2026-10-23.md).
- Existing unmerged draft PR #4 branch `feat/marketing-research-engine-20261022`: `marketing/research_transport_ops.py`, `marketing/research_transport_patch.py`, `marketing/andaz_stagea_evidence.py`.
- User specifically required: exact two public URLs; robots/terms/security review; existing trusted identities and preflights; run bounded extraction/negative QA **only if all gates pass**, and **stop if any connector security gate denies activation**. No additional URLs, authenticated booking, root, publishing, spending, merge, production site or permission changes.

## Confirmed during this attempt
1. **GitHub source-of-truth read:** canonical handover and Stage A full receipt re-read from `main`; exact staged `research_transport_ops.py` and `research_transport_patch.py` read from the draft branch. Stage A is prior offline design only, not proof of signed live extraction.
2. **Both existing workers paired and online:** `mac-linux` heartbeat: online, paired, age 1 second, three lane timestamps; `dell-linux` heartbeat: online, paired, age 0 seconds, three lane timestamps; checked 2026-10-22 approximately 19:58:12 UTC. Heartbeat alone does **not** certify live transport internals.
3. **Static signed transport review:** proposed paired Ed25519/encrypted v2 `extract_granted_url` path and exact-page `grant()` checks exist in GitHub but were previously **not activated**. Published staged grant set remains `https://mokshagoa.com/` and `https://www.w3.org/WAI/fundamentals/accessibility-intro/` only. **Neither Stage B pilot URL appears in those grants**. Planned patch would alter live relay files and adapter; requires both permission checks and reversible source fingerprint/backup validation before any application.
4. **External public policy review attempted:** read-only web tool `open` for `https://www.happypandahostel.com/robots.txt` and `https://thepeacehostel.in/robots.txt` returned inaccessible/internal errors. Therefore robots directives/crawl delay and current site terms **were not verified**; this is **not** evidence that either site allows crawling. A public indexed homepage result for The Peace establishes a public page but **not** extraction authorization or suitability for automated access.

## Exact connector-denial evidence
- Attempted **owner-scoped, read-only Generic SSH development-lane** preflight against existing Dell: host identity, four existing user-service statuses, staged patch/transport paths, activation marker, backup filenames, Stage A source hash.
- Attempted analogous **owner-scoped, read-only Generic SSH development-lane** preflight against existing Mac: queue timer, LangGraph v2 marker, current extract adapter, transport/backup filenames, Stage A hash and publish/spend flags.
- **Both tool calls were denied before worker submission** with the connector error: `This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.`
- **No queued host command, terminal receipt or exit code exists for those denied calls.** They must NOT be counted as executed or passing preflight.
- **Explicit safety stop obeyed.** No disguised/split/rephrased repeat through another SSH lane, terminal, browser, raw host access, local shell, external operator or alternative tool. No additional fetch/extraction attempted after denial.

## Gate scorecard
| Stage B requirement | Result | Evidence/next action |
|---|---|---|
| Read handover, Stage A and staged patch | **PASS** | GitHub reads in this turn |
| Mac/Dell paired host heartbeats | **PASS heartbeat only** | Both online/paired, three lanes |
| Exact-two-source constraint | **LIMIT DEFINED; not deployed** | URLs listed above, existing grants unchanged |
| First-party robots and usage-terms review | **INCOMPLETE** | Both `robots.txt` reads inaccessible; cannot infer allow |
| Authenticated reviewer/source identities | **BLOCKED / NOT ENROLLED** | Stage A identities are synthetic offline keys; no authorized active identity enrollment proven |
| Live relay/patch source-fingerprint and rollback preflight | **DENIED** | Both Generic SSH development preflight commands blocked by connector safety checks |
| Extend exact-page grant or activate v2 signed operation | **NOT ATTEMPTED** | Fail-closed; no permissions or production services modified |
| Real signed extraction and negative security smoke | **NOT ATTEMPTED** | All prerequisite gates did not pass |
| Publication, spend, merge, root, prod-site modifications | **NONE** | User limits respected |

## What remains before Stage B can be revisited
1. Obtain **an explicitly permitted, security-reviewed path for read-only transport fingerprint, service, and backup preflight** using the existing authorized connector controls. An owner action may be needed to resolve the connector's denial. **Do not evade safety controls**; retry only after legitimate connector permission/safety resolution.
2. Confirm target-domain `robots.txt`, crawling restrictions and applicable terms for the **exact** two pages; fail closed if unavailable or disallowed. A web search result is not substitute evidence.
3. Enrollment of a **real, identity-vetted human reviewer** and authorized source-signing identity/key governance through existing approved mechanisms. Do not relabel test keys or operational host identity as a vetted human. Check revocation, key custody, proof of authorization and review audit.
4. Verify deployed source fingerprints, exact grants, backup/rollback, idempotency/replay, TLS/SSRF/redirect controls and denied URL behavior before any signed transport patch. Respect any renewed connector denial.
5. Only after all preceding gates pass, perform one bounded approved public retrieval at a time, prove signed source identity and nonpromotion to verified facts, and record terminal worker receipts. No OTA checkout/authentication or extended grants.

**Status:** Stage A offline QA remains historically green. **Stage B blocked at security and source-policy gates.** No active signed extractor pilot, no verified hotel prices, no customer-facing claim certification. Draft PR #4 remains intended to stay unmerged and Issue #5 open. No modifications to the Marketing Brain, Dell/Mac services, keys, source permissions, publishing, spending, root or production websites were executed.
