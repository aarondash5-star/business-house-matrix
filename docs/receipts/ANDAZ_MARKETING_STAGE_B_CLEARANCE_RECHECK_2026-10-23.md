# Andaz Marketing Brain — Stage B clearance recheck and fail-closed result

**Date:** 2026-10-23 IST; heartbeat/preflight 2026-10-22 ~20:04 UTC.
**Authority:** User stated "Clearance granted", following earlier explicit approval of Stage B for only two exact public-page candidates. This was treated as authority to re-attempt the *previously denied read-only connector preflight* through its normal controls, **not** as the ability to override the connector's own security decisions.

**Disposition: PARTIAL READ-ONLY PREFLIGHT; MAC CONNECTOR SAFETY DENIAL; EXTRACTION NOT ACTIVATED.**

## Fixed authorized scope
- `https://www.happypandahostel.com/`
- `https://thepeacehostel.in/`
No other website, booking session, credential access, production service changes, broad URL permissions, publishing, spending, root, merge or source grants.

## Evidence and receipts
1. Re-read [canonical handover](../handoffs/MARKETING_BRAIN_ANDAZ_FINAL_HANDOVER_2026-10-23.md), [Stage A](ANDAZ_MARKETING_BRAIN_STAGE_A_ISOLATED_IMPLEMENTATION_2026-10-23.md), existing [Stage B denial](ANDAZ_MARKETING_BRAIN_STAGE_B_SECURITY_STOP_2026-10-23.md), and staged `marketing/research_transport_ops.py` + `marketing/research_transport_patch.py` on unmerged draft PR #4. Staged code still names only Moksha/W3C exact-page grants; neither pilot URL was added.
2. Authenticated Generic SSH read-only heartbeat: `mac-linux` online/paired, age 2 seconds, 3 lane timestamps; `dell-linux` online/paired, age 1 second, 3 lane timestamps. Time approximately 20:04:40 UTC.
3. **Dell** read-only development lane preflight accepted. Task `3d58e1b6-df42-4513-a4c1-043ea3513178` reached **completed, exit 0**, four user units ACTIVE (`bhm-searxng`, `bhm-research-relay`, `bhm-marketing-research-api`, `bhm-autonomy-controller`), and source paths exist: `matrix-research-transport/transport.py` (owner-only mode 0600), `bhm-research-expansion-20261022/research_engine.py`. This is existence/service preflight **only**, not signature verification, backups certification or approval to deploy.
4. **Mac** read-only development lane preflight rejected *before task submission* with explicit connector result: `This tool call was blocked by OpenAI's safety checks. Please double check what you are sending.` No Mac job UUID or terminal receipt was generated. **No control-lane, other SSH, browser, shell, or split-command retry was attempted.** Thus the hard gate remains DENIED.
5. Separate public web review successfully read both first-party *homepage content* and Happy Panda's [guest policies](https://www.happypandahostel.com/policies/). Happy Panda's published policies concern guests, check-in/cancellation; they do not grant automated crawling permission. The Peace homepage is public and describes accommodation, facilities, check-in, but not crawling permission. Direct `robots.txt` reads on **both** candidate domains returned inaccessible/internal tool errors; no reliable robots permissions, crawl-delay or site-specific automated-access terms could be established. The appropriate verdict is **UNKNOWN/NOT CLEARED**, not allow-by-default.
6. Authentic *human reviewer* identity and production source-signing identity enrollment, custody and revocation checks were **not completed**. Stage A's ephemeral signed test proofs do not constitute production enrollment.
7. No signed Mac→Dell v2 `extract_granted_url` end-to-end source receipt, no denied-URL negative live smoke, no source hash/pinned backup attestation, no activated source grant, no prospect or pricing claim verified. All past offline tests remain historical; none were presented as live Stage B tests.

## Gate disposition
| Gate | Status | Notes |
|---|---|---|
| User scope and approval | APPROVED, EXACT TWO ONLY | Approval does not override connector safety |
| Mac/Dell heartbeat | PASS | Both paired/online |
| Dell read-only service/paths | PASS | Terminal receipt `3d58e1b6-df42-4513-a4c1-043ea3513178`, exit 0 |
| Mac read-only transport preflight | **DENIED** | Security policy blocked before execution |
| Both exact domains' robots/terms | **UNKNOWN** | Public homepages readable; robots inaccessible |
| Real reviewer/source signing enrollment | **NOT COMPLETED** | Stage A proofs synthetic only |
| Restore-point, source hash, keyed receipt end-to-end proof | **NOT TESTED** | Security-denied prerequisites |
| Exact-page signed extraction and negative smoke | **NOT RUN** | Fail-closed |
| Publishing, spending, merge, root, expanded permissions, production site/services | **NO CHANGE** | Preserved |

## Next authorized action
- Clear the Mac connector restriction through legitimate security/connector administration and obtain an unblocked normal preflight receipt. **Do not circumvent the denial.**
- Confirm the *two exact* hostnames' `robots.txt`, site-specific terms and permitted page fetch timing via an approved safe path, or obtain direct written access authorization. If unavailable, fail closed.
- Vet and enroll a real human reviewer/source-signing identity with audit trail and revocation, not synthetic keys.
- Only after **all** conditions succeed should a reviewed fingerprint/backups check and strictly bounded source extraction/negative controls be reconsidered; preserve signed search transport and return unverified evidence only.

**Final: USER CLEARANCE NOTED; PLATFORM CONNECTOR CLEARANCE NOT CONFIRMED. STAGE B REMAINS BLOCKED.**
