# Self-hosted SearXNG research — deployment and handoff

**Date:** 2026-10-21 (Asia/Kolkata)  
**Scope:** Independent Business House AI Matrix / Marketing research. No changes to Moksha Master.

## Decision
- **Tavily deprecated:** no active model- or research-tool route uses Tavily; previous Tavily source, quota ledger and old tests were archived on Mac for rollback/audit rather than erased.
- **Replacement:** SearXNG, official upstream **AGPL-3.0-or-later**, using a version-pinned GHCR OCI container on Dell. No inference credits or API key are required by the local SearXNG service.
- **Upstream note:** SearXNG is metasearch. External search engines may still rate-limit, challenge, reject or return stale results. Read-only retrieval is not automatic claim verification.

## Verified Dell deployment
- Host: \`dell-linux\` (Dell Inspiron Linux), service identity \`generic-auto-exec\`.
- Pinned image: \`ghcr.io/searxng/searxng:2026.10.19-81371861f\`. Source: https://github.com/searxng/searxng/pkgs/container/searxng . License: GNU AGPL-3.0-or-later.
- Rootless Podman with dedicated subordinate UID/GID range \`200000:65536\`, Ubuntu packages \`uidmap\` and \`slirp4netns\` installed after diagnosing host setup gaps.
- Engine only on **\`127.0.0.1:18889\`** (container 8080) with 512 MiB memory and 1 CPU limits. Private config generated locally with noncommitted random secret under \`/var/lib/generic-linux-automator-exec/matrix-searxng/config/settings.yml\`.
- Official SearXNG JSON API enabled in private \`settings.yml\` (not enabled by default in upstream). Source: https://docs.searxng.org/dev/search_api.html .
- Verified live native Dell JSON query for \`sauna wellness\` returned **42 results**; two upstream engines reported errors. Later local CLI search for \`sauna ice bath wellness Goa\` returned relevant results, including Moksha Wellness's public homepage and Goa listing pages.
- Rootless user service \`bhm-searxng.service\` is **enabled and active**, with account lingering enabled for boot persistence.
- Private LAN gateway: \`/var/lib/generic-linux-automator-exec/matrix-searxng/gateway.py\`, system service \`bhm-searxng-gateway.service\` **enabled and active**, bound to \`192.168.0.103:18888\`; fixed source IP allowlist for Mac \`192.168.0.106\` and systemd inbound/outbound IP protection. Never route this gateway to the WAN or publicly forward port 18888.
- Local Dell read-only command:
  \`\`\`bash
  python3 /var/lib/generic-linux-automator-exec/matrix-searxng/local_search.py 'sauna ice bath wellness Goa' --limit 4
  \`\`\`
- Last measured resource usage: approximately **122.6 MB / 536.9 MB** container memory; ~1.8% reported CPU during sample. The existing generic Linux SSH automator remains active.

## Mac Marketing Brain switch
- Canonical repo: \`marketing/mac-brain/searxng_research.py\`, \`marketing/mac-brain/brain.py\`, \`marketing/mac-brain/router.py\`, \`marketing/mac-brain/provider-policy.template.json\`.
- Live Mac: \`/opt/business-house-matrix/marketing/brain/\`. \`brain.py\` routes \`research_search\` to the SearXNG module; \`research_extract\` safely refuses requests pending a separately reviewed local Trafilatura content extractor, rather than calling the previous Tavily Extract.
- Operational model policy \`tool_connections\` now holds only \`searxng-search\` (\`provider=searxng\`, \`self_hosted=true\`, license reviewed, no paid fallback). **Tavily was removed from this active list.**
- For safety, Mac \`searxng-search\` remains **\`enabled=false\`** until real private connectivity to the Dell is restored.
- The Mac client pins Dell's LAN address, rejects secrets/personal-data patterns in queries, requires public HTTPS result URLs, labels source snippets untrusted, and enforces 3 requests/minute and 100/day. Its policy permits only known endpoints; no arbitrary URL.
- Both Groq models remain enabled and authenticated; Cloudflare/OpenRouter/Gemini remain disabled. \`publish_enabled=false\`, \`spend_enabled=false\`, \`local_inference_enabled=false\` and \`render_enabled=false\`.
- **24 Mac synthetic regression tests passed**: 8 router + 4 Brain + 6 Reel Studio + 6 SearXNG client. Dell live engine and CLI were tested separately.

## Remaining blocker — Wi-Fi device isolation
- Mac address at verification: \`192.168.0.106/24\`, Dell: \`192.168.0.103/24\`. Both are on \`192.168.0.0/24\`.
- Mac \`ip neigh show 192.168.0.103\` showed **FAILED**; Mac TCP to Dell port 22 and 18888 returned **no route to host**. Reciprocal Dell-to-Mac ping also failed.
- This occurs **before** the SearXNG gateway can accept the connection. It is consistent with router guest/client/AP isolation (or another layer-2 network partition), not a defect in SearXNG or the Mac adapter. Both hosts have UFW inactive, and rootless engine localhost is healthy.
- Required for autonomous Mac-to-Dell search: enable peer-to-peer device connectivity on a trusted private SSID / VLAN, or supply a separately authorized private relay such as WireGuard over a reachable endpoint. Do **not** circumvent by exposing SearXNG publicly.
- Once network works, verify Mac \`curl --fail http://192.168.0.103:18888/health\` and an actual JSON search. Only **then** set \`searxng-search.enabled=true\` through the reviewed router policy; retain rate caps.
- The two DHCP addresses are not pinned: reserve them in the router or revise both endpoint allowlist and gateway binding if the leases change.

## Operator checks
\`\`\`bash
# Dell, authenticated via generic SSH Linux, service user
systemctl --user is-active bhm-searxng.service
systemctl --user is-enabled bhm-searxng.service
sudo -n systemctl is-active bhm-searxng-gateway.service
podman ps --filter name=bhm-searxng
python3 /var/lib/generic-linux-automator-exec/matrix-searxng/local_search.py 'Goa wellness retreats' --limit 5

# Mac, authenticated service user
B=/opt/business-house-matrix/marketing/brain
python3 "$B/router.py" validate
python3 "$B/router.py" status
python3 "$B/searxng_research.py" status
python3 "$B/test_router.py"
python3 "$B/test_searxng_research.py"
python3 "$B/brain.py" status
\`\`\`

## Rollback
- Dell: \`systemctl --user disable --now bhm-searxng.service\`; \`sudo -n systemctl disable --now bhm-searxng-gateway.service\`; preserve the container image and private config for audit until approved cleanup. Do not remove Podman mappings blindly—they may be reused.
- Mac: take private policy backups before changing anything; existing snapshots \`router.py.pre-searxng-20261021\`, \`brain.py.pre-searxng-20261021\`, \`provider-policy.json.pre-searxng-20261021\`. Old Tavily source and SQLite ledger retained as \`*.deprecated-tavily-*.\`
- Don't re-enable Tavily without a new explicit decision.
- Never alter the generic Linux SSH bridge, Dell Matrix Dev Brain, Moksha Master or root security settings as part of rollback.
