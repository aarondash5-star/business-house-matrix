# Autonomous Matrix MVP — implementation and acceptance checkpoint
Date: 2026-10-21. Project: independent Business House AI Matrix, NOT linked to Moksha Master.

## Verified working now

| Service / capability | Live verification | Limit |
| --- | --- | --- |
| Dell self-hosted SearXNG | Rootless Podman, HTTP only on 127.0.0.1:18889, actual public search results returned | External engines can throttle; no LAN or public gateway |
| Dell local LangGraph Dev Brain | Brain service running; SearXNG-researched Dev proposal reached `review_passed` with 5 saved artifacts | Model's textual PASS did **not** prove code works |
| Central Brain dispatcher | `bhm-autonomy-controller.service` enabled/active, SQLite task queue, idempotency, department routing, outcomes ledger | Locally routes public research, proposal-only Dev, QA; does NOT yet reach Mac |
| Central actual research | 5 public sources returned, task receipt completed; no paid API | Source discovery is not independent verification |
| Dev job reconciliation | Existing completed Dev job imported with no duplicate model run | Imported job marked `proposal_review_only` |
| Sandboxed executed QA | Rootless nonroot Python 3.12 Alpine Podman container, no network, read-only, memory/PID/CPU limits | Only separately staged Python files with independent tests; no production writes |
| Genuine code defect found | Earlier model proposal called nonexistent `TaskGroup.cancel()`. Independent Python unit test failed despite previous model `review_passed` | Proves text-only model QA can produce false positives |
| Narrow correction rule | Specific identified TaskGroup bug corrected in isolated staging; Python unit test subsequently passed | A single known defect, not generic self-healing code generation |
| Mac Groq | `groq-creative-oss120` and `groq-copy-qwen` eligible; new creative brief job with Trends opt-in completed in ~1.2 s | Creative text only; not a rendered video |
| Google Trends | Public India RSS ingested 10 items; 6 offline tests pass; Mac Brain `trends_insight` completed; refresh cron every 6 hours | National trending headlines and relative index; cannot infer Goa-specific search demand, fonts or colors |
| Reel Studio | Existing renderer/preflight/preview QA code retained; negative/guard tests pass | `render_enabled=false` until sustainable Mac thermal and real approved footage |
| SSH bridge | Both Mac/Dell workers online, no root/sudo permission changes | Bridge access from GPT does not equal autonomous direct Mac-Dell traffic |
| EVOLUTION ledger | Central outcomes categorized with strict QA grades; failed results retained | Rule-based feedback only, no autonomous model fine-tuning |

## Durable paths and code

- Central source: `brain/mvp-controller/controller.py`
- Executed unit-test runner: `brain/mvp-controller/sandbox.py`
- Narrow verified correction rule: `brain/mvp-controller/repair.py`
- Dell central runtime directory: `/var/lib/generic-linux-automator-exec/matrix-controller`
- Dell service: `systemctl --user is-active bhm-autonomy-controller.service` (rootless, memory bounded)
- Dell local Dev Brain: `sudo matrix-brain doctor`; research: `sudo matrix-brain research-search 'Python official docs'`
- Mac Brain: `/opt/business-house-matrix/marketing/brain/brain.py` and `trends.py`
- Detailed reusable SearXNG: [deployment](RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md), [contract](REUSABLE-RESEARCH-CONTRACT.md), [skill](../skills/selfhosted-searxng-research/SKILL.md).

Safe CLI usage on Dell (authenticated service account):

```bash
D=/var/lib/generic-linux-automator-exec/matrix-controller
P=/var/lib/generic-linux-automator-exec/.local/share/matrix-dev-brain/venv/bin/python
"$P" "$D/controller.py" status
"$P" "$D/controller.py" selftest
"$P" "$D/controller.py" submit pilot research_search 'Python LangGraph official docs' --key unique-safe-query-id
"$P" "$D/controller.py" submit pilot dev_proposal 'Propose validated Python code' --research-query 'Python official docs type validation'
"$P" "$D/controller.py" submit pilot sandbox_qa approved-test-batch
python3 "$D/sandbox.py" selftest
systemctl --user is-active bhm-autonomy-controller.service
```

No arbitrary executable arguments are accepted by these routes. Queued, running, unknown, blocked, review-needed and completed states are distinct. If external Dev dispatch has an ambiguous receipt, controller must **not replay** it blindly.

## What remains NOT fully functioning

1. **Secure cross-machine link:** Dell `andaz` and Mac `Andaz` are separate Wi-Fi networks with overlapping 192.168.0.0/24 addresses and non-working ARP/peer routes. Mac SearXNG policy remains OFF; Dell HTTP gateway disabled. Need an owner-approved private shared LAN or authenticated overlay. Never expose SearXNG to the public Internet or alter Wi-Fi remotely without safe recovery.
2. **Production-safe video pipeline:** Mac CPU previously approached 90°C. User `generic-auto-exec` PipeWire/WirePlumber was unnecessarily running during SSH sessions; it was stopped and locally masked for that service user only. Spot-check sensors improved to ~65–76°C but fan/desktop load vary. This is NOT a sustained render success. Real footage, original logo, music rights, 9:16 render, timed captions and technical/brand QA still need an end-to-end acceptance receipt.
3. **Dev automatic coding:** The initial LangGraph Dev Brain remains proposal-only. The central sandbox truly executes staged unit tests, but has not been certified to take arbitrary generated multi-file code, create sufficiently independent tests, correct arbitrary errors and safely deliver a repository change. No merge/publish rights granted.
4. **Central user interface:** User selected Open WebUI; however official releases from v0.6.6 include a branding-restriction condition that is not standard OSI-approved open-source. The Matrix policy requires OSI-licensed components. Older BSD-3 v0.6.5 is unmaintained and must undergo security review; do not silently install a current non-OSI build or deprecated LibreChat. Central CLI remains usable.
5. **Full 9-department architecture:** Concept, Development, QA/QC and limited EVOLUTION run some pilot workflows. Design, Sales, Accounts and Support and full interdepartmental coordination remain staged. Payment/publishing and customer data require explicit policy approvals.
6. **General retry and recovery:** A limited, known bug correction is not a guarantee of unconstrained autonomy; unknown failures escalate and are never retried indefinitely.
7. **End-to-end acceptance:** Must verify a fresh goal reaching its real finished deliverable, QA, remediation and a reboot/network fault recovery; no fabricated success.

## Privacy, license and approval controls

Open-source SearXNG (AGPL-3.0-or-later), existing LangGraph, Python, SQLite and Podman are reused. The local Python sandbox pulls the official Python 3.12 Alpine image. No paid plan or unverified proprietary model route is switched on. Neither GitHub, model-generated text, nor controller status grants the right to edit production, expose credentials, change root/sudo privileges, post to user channels or spend money. Project-specific data stays isolated. User's exact-host permission-change approval rule remains in force. Mac service-user audio masks can be undone through:

```bash
systemctl --user unmask wireplumber.service pipewire.service pipewire-pulse.service pipewire.socket pipewire-pulse.socket
```

This affects the automation service account, NOT the desktop owner's interactive audio services. Re-enable selected audio units if a future voice project requires them.

## Acceptance definition and next actions

- A fully autonomous MVP is **not** achieved until central coordinator can securely delegate to both machines, execute approved development and marketing tools, run independent tests, correct bounded faults, and deliver a real video/code artifact without repeated intervention.
- Immediate gates: cross-network secure path; thermal-safe Mac reel; source-grounded creative→edit→QA; actually tested code results; safe frontend licensing and access; outage/reboot resilience.
- Verify each step with completed tool receipts and asset checks. A pending, queued, failed or blocked tool call is never described as done.


## Verified unattended failure → EVOLUTION correction, 2026-10-21

- Controller task `c54a717f-f0bb-486b-85e9-cb986800fc52` autonomously ran independent Python 3.12 QA against extracted model source and found `TaskGroup` has no `cancel()` method. Saved failed QA receipt; it did **not** accept earlier model review PASS as correctness.
- Controller automatically enqueued EVOLUTION repair task `999d4a42-18bf-4e0f-8fef-8527d256b61e`. Rootless user service executed a **bounded, exact known rule**, staged separate corrected source, reran isolated unit tests without network/host writes, and finalized the repair as `completed` with QA level `executed_isolated_unit_tests`.
- Verified both 0600 receipts: `/var/lib/generic-linux-automator-exec/matrix-controller/repair-receipts/auto-repair-pilot-20261021-attempt-1.json` and `sandbox-receipts/auto-repair-pilot-20261021-fixed.json`. This is a genuine **unattended** repair-and-retest loop for this one recognized defect, *not* arbitrary freeform AI self-repair.
- Earlier manual fixed-batch test also passed after correcting container mount permissions; the failed attempts remain in the ledger, not deleted. SearXNG, Dev Brain, dispatcher, and Generic SSH services remained active.


## Plugin skill publication — 2026-10-21
- Private connected `generic-linux-ssh-mcp` plugin updated to **v0.1.19**, release `pluginrel_6ad8d710c0c88191968891ff74a5e2ff`, with new portable `skills/matrix-autonomous-mvp/SKILL.md` and existing `skills/selfhosted-searxng-research/SKILL.md` preserved. Post-update plugin readback verified both skills and the original onboarding skill.
- Reuse: [private SSH plugin](https://chatgpt.com/plugins/plugins_6ad64adab5e481918832cd516e779009) and [repository Matrix autonomy skill](../skills/matrix-autonomous-mvp/SKILL.md). Publishing a skill does NOT create a new MCP tool or grant other projects access to private data or privileged machine actions.
- **Network checkpoint:** Dell sees only lower-case `andaz` Wi-Fi in its radio scan; the stored `Andaz` profile has not been switched remotely. Neither router nor root permissions have been changed. Mac-to-Dell routing remains blocked, and the private LAN gateway remains OFF.
