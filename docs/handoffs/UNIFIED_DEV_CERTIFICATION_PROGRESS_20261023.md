# Dev Matrix universal-runtime certification — remaining gates, 23 October 2026

**Decision: PARTIAL CERTIFICATION; FULL UNIFIED RELEASE NO-GO.**  
**Owner instruction:** "Certify whats left".  
**Development candidate SHA:** `2d885b6fb8cf8f43792de74e1f93b2931ca36eae` on branch `feat/dev-universal-dynamic-intake-20261023`.  
**Canonical independent controller v6 hash:** `b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e`.

## New verified achievements

| Gate | Result | Receipts |
| --- | --- | --- |
| Rootless Podman standalone container launches offline | **PASS** | `b2b54bc3-ce0f-4678-a282-0304412d79f9` exit 0 |
| Root cause of stuck workcell | **IDENTIFIED**: `--userns=keep-id` triggered expensive ID-mapped layer copy; timed out. Normal rootless namespace worked with actual source volume; no root privilege granted | `df98e590-eb6a-4db3-8eb3-90253a6c535d` observed timeout; `5513e698-38ab-4cd2-b79e-38a03b22a5cf` successful |
| Fixed runtime and static regression | **PASS 13/13** after removing keep-id | `06648121-01c2-4293-a189-d2666a2c181c` exit 0 |
| Real rootless guest file edit + Git metadata denial + independent test | **PASS**: model workcell updated isolated `app.py`, verified SHA fingerprint; `.git/config` write failed with read-only FS; independent Python acceptance PASS | `559a9ba8-f751-4e37-b1c1-80ed5cae9f65` exit 0 |
| Actual model-driven two-file Python | **PASS** on an isolated synthetic repository: `qwen3:4b-instruct` changed `calc.py` and `invoice.py`, independent trusted acceptance passed; exact change hash `ebb0b0a20f10e4c9db9c5a3f69fe1d37929112f97151c9a84d251305d62106fe`; 52.92 s; `review_ready`, `qa_exit=0`, `pushed=false`, `published=false` | `84a4c2d4-6fe7-48f7-8eaf-a1c83e76dbf8` exit 0 |
| Automatic independent QA-based completion | **PASS**: source diff + immutable tests required, not model self-assertion; rejects no-change and failing tests; 15/15 unit checks | `d64a201e-9be3-4676-a233-078bf65dec39` exit 0 |
| Real guest cross-project isolation, offline network denial, read-only QA | **PASS** in disposable guest; synthetic sibling-project marker inaccessible, outbound socket denied `Network unreachable`, read-only test phase denied write | `89b05f55-1953-4203-9da8-aad8de58f3e0` exit 0 |
| Durable timeout cleanup | **PASS 17/17** unit tests, including fail-closed cleanup refusal; actual `sleep 30` guest timed out at 3 s with `workcell_timeout_stopped` and zero remaining candidate containers. Scoped unique-name `podman rm -f --ignore`; existing SearXNG untouched | `d6c2c639-6b54-416d-8935-26039ba1407d`, `09afde9e-3338-4e2b-8423-a6e548677c3c`, exit 0 |
| Final host continuity | **PASS**: Dell SSH online, certified v6 active/checksum unchanged, legacy proposal Brain stopped, no unified service, no orphan candidate guest, existing SearXNG alive | `88e88f69-33ec-45e8-a471-6d9f1c40eaaa` exit 0 |

## Real external Andaz project — not certified

Verified the actual public `karanzing1992/andaz-vibe-stay` repository at pinned main SHA `21de8351238f9292e270a7635cbac7a08dd55c63`. A model-scoped, **unpublished** accessibility improvement was tested in isolated checkouts (skip navigation to main content and focus CSS). **Neither attempt passed QA:**

- `2b76783f-508e-4d64-a733-55d084ed0e8e`: timed out before producing the first development action; source unchanged.
- `b1469114-bb04-406d-9179-aa69e782e548`: after successful Qwen warm-up (`7b6acbc1-3825-4d65-8a65-f4b4e4ead603`, 28.93 s), model generated only untracked `temp.html`, failed to modify `index.html`, reached step budget and correctly returned `needs_review`. No branch push, publication or live change.

Additional earlier synthetic Python attempt `efae2667-551f-4cb6-b907-428cc864f596` modified two modules but hit total timeout prior to QA; separate `622e320f-3e33-4fe7-b775-ad3fe0f852fb` changed two modules but hit step budget. These unsuccessful jobs were **not** replayed; a new task `84a4c2d4...` succeeded after independent auto-finalization change.

**Model/throughput observation:** Local Ollama endpoint was running; model cold start and inconsistent reasoning on a large real HTML file are still material to general autonomous development. A brief model probe timed out for both Qwen/Granite (`d4c5276a-2c9b-4126-b485-181f775d714e`). Qwen subsequently successfully prewarmed. These observations do not certify a robust external-project controller.

## Remaining non-negotiable release gates

1. **Real external-project autonomous model patch:** produce an actual diff in the owner-approved Andaz `index.html`, verify the external origin/commit, accessibility/booking UI QA and real source-change fingerprint. Do not claim success from synthetic Python.
2. **Authenticated universal Brain CLI and worker intake:** currently **not deployed**, with previous CLI/bootstrap request denied by platform tool safeguards. User approval is recorded but cannot bypass the connector/security owner. Resolve via legitimate fixed-purpose review; do not reroute a denied privileged action.
3. **Independent Mac review:** Mac paired but offline/stale (26,363 seconds at final `2026-10-23T11:20:04Z` heartbeat). Need verified cross-host peer evaluation or an expressly approved equivalent.
4. **Project-scoped GitHub PR identity + hosted CI** on exact source: neither has independently certified pass; no autonomous merges, public publishing, production writes or spending.
5. **Canary integration and rollback:** no unified Brain service created or connected to v6, no automatic task-worker ingress, no cross-system receipt propagation, no time-bounded Dell canary and rollback drill. Production v6 SHA remains protected.
6. **Controller reliability:** benchmark Qwen model warm/cold behavior, suitable stronger controller model and evidence-backed repair loops for larger external projects. Prevent near-timeout partial edits from being reported as completed.

## Owner-facing conclusion

**Certified:** isolated real tool execution, positive source editing, independent trusted QA, two-file Qwen autonomous Python success, signed dynamic intake unit checks, deny-by-default isolation, timeout cleanup and current v6 continuity on Dell.

**Not certified or deployed:** unified control plane/CLI, real Andaz model-generated external-project change, Mac peer signoff, GitHub restricted write identity, rollout canary and rollback. **NO-GO** for full autonomous unified Dev Brain release and for switching from certified v6. No permission/security denial was bypassed.

**Next actions:** Review fixed-purpose CLI ingress through connector/security owner, restore Mac, improve external-project model planning/reasoning and run verified Andaz edit+QA, independently audit code/CI and project-scoped write identity, then canary and rollback beside v6. Preserve every failure receipt as non-pass evidence.
