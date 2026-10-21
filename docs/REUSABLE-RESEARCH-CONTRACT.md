# Reusable Research Provider Contract v1 — SearXNG

**Current implementation status:** Dell-hosted, SSH-accessed **read-only public search** operational; Mac's network adapter staged but disabled; no external HTTP exposure.  
**Designed for:** Independent Business House AI Matrix departments and other owner-authorized projects that opt in to shared *retrieval capability*, **not** shared business data or privileges.  
**Companion portable skill:** [selfhosted-searxng-research/SKILL.md](../skills/selfhosted-searxng-research/SKILL.md).  
**Canonical operator state:** [SearXNG deployment](RESEARCH-SEARXNG-DEPLOYMENT-2026-10-21.md).

## Design choices

1. **Golden Rule 0 (reuse):** Reuse existing rootless Podman SearXNG container, existing Generic Linux SSH bridge, Python standard library and current single-project job queues; do not introduce paid SaaS, another browser/search service or a global unrestricted shell service.
2. **Open-source core:** SearXNG is AGPL-3.0-or-later. Check full obligations if network services/code are modified and offered publicly; document exact upstream image/version, and preserve notices. Do not construe a free *hosted search engine* as open-source just because SearXNG queries it.
3. **No public ports:** Dell-local engine \`127.0.0.1:18889\`. LAN relay was shut down after confirmed divergent SSIDs/gateways. No automatic cross-router access. The Generic Linux SSH tool is the supported secure human-supervised pathway for other ChatGPT projects that are expressly authorized.
4. **No data mixing:** The search tool can search public keywords from several projects, but may never automatically receive unrelated private project prompts, documents, customer data or previous search logs. Queue, SQLite state and output for each caller stay within the caller's own project. Cross-project source links can be reused but not user-specific search histories without permission.
5. **Fail closed on governance:** Input 2–180 characters; no credentials, phone numbers, customer emails, private or unpublished material. Explicit research query only; no LLM-initiated arbitrary tool execution. Source snippets remain untrusted. No arbitrary URL fetching or uncontrolled site crawling.
6. **Spend and rights:** Self-hosting costs no API fees; upstream search engines can throttle. No paid fallback, publishing, user impersonation or unknown-license datasets. All material must be verified against source-specific content/license restrictions before reuse in marketing assets or training.
7. **Safety/reliability:** Bound results to 1–10, timeout remote execution, use service quotas, search-safe URL filtering and read-only execution; never retry unknown SSH outcomes or regenerate an identical mutating job without inspecting the receipt. Thermal and active CPU-heavy job state affect scheduling.

## Public-only call envelope (application interface)

Input (project-specific wrapper; the Dell CLI currently consumes only \`query\` and \`limit\`):

\`\`\`json
{
  "version": "1",
  "project_id": "project-specific-audit-label",
  "query": "Python 3.12 TaskGroup official documentation",
  "limit": 5
}
\`\`\`

Output (actual deployed CLI structure; field \`project_id\` is **not** currently emitted):

\`\`\`json
{
  "provider": "self-hosted-searxng",
  "node": "dell-linux",
  "results": [
    {
      "title": "Public documentation title",
      "url": "https://example.org/docs",
      "snippet": "Bounded public search snippet.",
      "engine": "duckduckgo"
    }
  ],
  "result_count": 1,
  "source_attribution_required": true,
  "untrusted_external_content": true,
  "automatic_publication": false
}
\`\`\`

**Warning:** These structures illustrate *shape*, not a specific real source or live result. Query-result ranking, \`engine\` availability and index freshness depend on SearXNG's public upstream engines. Do not assert search results constitute consensus or independent verification. For a caller-agnostic software contract use [JSON Schema](../research/contracts/searxng-search-response-v1.schema.json).

## Supported invocation patterns

**Owner ChatGPT Generic Linux SSH plugin / any approved project:**
\`\`\`bash
python3 /var/lib/generic-linux-automator-exec/matrix-searxng/local_search.py 'bounded public query' --limit 5
\`\`\`
Invoke through the authenticated \`dell-linux\` bridge and poll the returned task ID to \`completed\` + exit zero before consuming JSON. Shell-quote all user strings safely, do not embed credentials. This bridge grants *no new permissions* through documentation.

**Dell Matrix Dev Brain:**
\`\`\`bash
sudo matrix-brain research-search 'Python asyncio official docs'
sudo matrix-brain submit 'Draft a clear design proposal' \
  --profile fast --research-query 'LangGraph Python StateGraph documentation'
\`\`\`
The \`--research-query\` parameter is optional, explicitly public, and used as evidence to inform plan/develop/QA stages. The model does not get a freeform browsing tool. All output remains proposal-only; no tests or repository edits implied.

**Mac Marketing Brain:** Runtime \`searxng_research.py\` and research queue task are installed but \`searxng-search.enabled=false\` while two different Wi-Fi networks use overlapping \`192.168.0.0/24\` addresses and cannot reach each other. No SearXNG HTTP relay is active. Research on Dell through a separate authorized SSH operation is possible, but do not pretend it is already a continuous Mac-to-Dell network integration.

**Other projects:** Reuse the portable skill in the ChatGPT private Generic Linux SSH plugin or install a local adapter bound to an explicitly approved service endpoint. Limit project scopes, queries, trusted domains, timeout and record retention separately. Reuse **capability** only; never copy model keys, project databases, Master Registry entries, sensitive session data or cookies.

## Verification and maintenance

- Dell: \`systemctl --user is-active bhm-searxng.service\`; search CLI smoke; \`sudo matrix-brain selftest\`; \`sudo matrix-brain list\`.
- Current Dell Dev 4-node research-assisted real job was submitted as ID \`cad4904e-7aec-4678-ad71-d170ad2c4841\`; at latest observation it was still in QA review and had no final receipt. Later users must check its final state before claiming it passed.
- Mac: router validation, negative tests and approval flags; stay disabled until authenticated, private cross-network transport is fixed and separately verified.
- Generic SSH plugin status is independent of SearXNG status. Its underlying auth, rate limits, and root/sudo privileges cannot be silently changed by another project just because the search adapter is reusable.
- Rollback: stop only the relevant integration after auditing in-flight jobs. Preserve backup \`brain.py.pre-searxng-20261021\`, saved SearXNG image/settings, and bounded historical receipts. Do not restore Tavily automatically.
- Update source → integration tests → host deploy → readback → plugin skill → versioned docs. Distinguish \`DOC_SAVED\`, \`PLUGIN_RELEASE_UPDATED\`, \`DELL_LIVE_VERIFIED\`, \`MAC_LIVE_DISABLED\`, and \`OTHER_PROJECT_ADOPTION_PENDING\`.

## MVP next blockers

1. Securely connect Mac to Dell by using a common approved private LAN or explicitly approved authenticated overlay, without changing SSIDs remotely and cutting the owner off.
2. Activate Mac read-only SearXNG policy after a real JSON search from Mac. Check address reservation and host identity rather than relying on mutable private DHCP IP alone.
3. Add a separate reviewed open-source content extractor (Trafilatura) only if needed, with SSRF defense, public-domain allowlists, controlled retries and source licensing checks.
4. Add project-specific relevance/ranking and feedback/evaluation; never confuse national Google Trends search spikes with actual Goa-specific demand.
