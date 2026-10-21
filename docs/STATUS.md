# Current Business House AI Matrix rollout status

**Matrix-wide baseline:** 2026-10-18; **Marketing checkpoint verified:** 2026-10-21

| Stage | State |
|---|---|
| Architecture | Approved: Open WebUI, LangGraph, Temporal, FastMCP/ContextForge, Ollama, PostgreSQL, EVOLUTION |
| GitHub migration | Complete: public `aarondash5-star/business-house-matrix`, original Git history preserved |
| CI / public-repository safety | Proposed in branch `ci/cloud-readiness-20261018`; verify PR checks before merging |
| Oracle Always Free | Target selected; tenancy, identity and capacity not yet verified |
| Google Cloud Run | Backup target selected; Matrix identity and free quota not yet verified |
| Open WebUI runtime | Not deployed |
| LangGraph | Starter simulation only; no live model or tools |
| Temporal / MCP | Planned, not connected |
| OpenClaw | Deferred until pilot acceptance |

Next exit gate: passing, reviewed GitHub validation checks. Next required external decision: which separately authorized cloud tenancy/project to use, and verify its actual free capacity before any deployment.


## Marketing Department — verified 2026-10-21

For accurate Marketing facts use **[current-state handoff](MARKETING-CURRENT-STATE-2026-10-21.md)**; chronological records appear in [Phase 1](MAC-MARKETING-PHASE1.md) and [API router](MAC-MARKETING-API-ROUTER.md).

- Mac Marketing Brain: isolated SQLite autonomous queue, cron runner and receipts functioning; **5 completed jobs** at verification.
- Groq: **GPT-OSS 120B and Qwen3.8 27B authenticated and live**, including end-to-end Marketing Brain job; **2 recorded local API requests**, shared conservative cap 40/day.
- **11 passing regression tests** (7 provider-router + 4 Brain) on Mac; Generic Linux SSH, cron and Ollama active.
- Tavily and Gemini **registered but disabled**; Gemini has proprietary licensing conflict with Matrix's open-source rule. Cloudflare/OpenRouter configured but disabled.
- No live video pipeline integration or ready-to-publish autonomous output yet; existing Reel Studio is present.
- Local creative inference disabled after ~90°C test; social publishing and spending disabled.
- Next stage: QA-gated Reel Studio integration using real footage, then Tavily research connector and controlled provider expansion.

The earlier Matrix-wide pilot status above remains independently tracked. No Open WebUI/Temporal/MCP production deployment is implied by Marketing's successful Groq pilot.


## Research engine change — 2026-10-21
- Tavily **deprecated**: removed from operational Mac research provider registry and Brain imports; old code/database archived locally.
- Dell self-hosted rootless **SearXNG live and boot-persistent**; native and Dell-local CLI search verified.
- Mac replacement client and task connection deployed, **disabled pending private reachability**. Wi-Fi hosts cannot ARP each other; Mac-to-Dell SSH and TCP failed before gateway. No public endpoint exposed.
- [Detailed rollout, safety, blocker, restart and rollback](RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md).


## SearXNG correction and Dell Dev expansion — 2026-10-21
- Dell SearXNG remains available at **localhost only** and starts at boot. LAN gateway was disabled as the network is two DIFFERENT SSIDs/routers (`andaz` vs `Andaz`) using overlapping `192.168.0.0/24` private ranges; do not claim Mac-to-Dell access works.
- **Dev Brain research integrated and tested:** `matrix-brain research-search`, optional public `--research-query` and evidence-containing LangGraph research node, with source receipts. Existing queue retained. No model-directed search, repository edit or paid API.
- Mac Marketing Brain SearXNG still disabled until trusted inter-network connectivity is established; Tavily remains retired.
- Full details: [Deployment and Dev integration](RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md).
