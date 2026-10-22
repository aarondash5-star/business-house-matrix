# Business House Matrix — Mac research evidence primary cutover

**Date:** 23 October 2026 IST.  
**Decision:** **MAC LOCAL EVIDENCE PRIMARY — LIVE / VERIFIED.** Existing signed Dell discovery remains subordinate and rollback is preserved. **Not** Stage B signed-extraction certification.

## Scope / implementation

The user explicitly approved Mac execution after requesting Mac as primary. Standard Generic SSH Mac tools, previously denied by platform checks, were accepted and returned terminal receipts in this turn. No connector exception or alternate Supabase enqueue was used.

**Live Mac brain:** `/opt/business-house-matrix/marketing/brain` (owner account `generic-auto-exec`, Linux host `KARAN`). Selectively promoted four source files from existing branch `feat/marketing-research-engine-20261022`, pinned at **`0f61caf249823c1a7a63712c0f4597b0bbbd6238`**:
- `research_engine.py` (original guarded extractor/evidence/FTS engine, not auto-enabled);
- `research_entities.py` (deterministic classifications, anti-fabrication);
- `research_mac_local.py` (strict read-only immutable SQLite snapshot packets);
- `research_mac_primary_bridge.py` promoted as the live `research_market_bridge.py` (existing Brain `research_market` import unchanged).

Prior live `research_market_bridge.py` preserved at `research_market_bridge.py.pre-mac-primary-20261023` and copied to `research_market_dell_bridge.py` for existing signed Mac→Dell discovery only. The live task router continues to use the established `research_market_bridge.market()` import without changing `brain.py`. New bridge returns Mac-local evidence/report in the existing v1.3 report format and delegates only existing `moksha_arambol` signed public discovery to Dell. For Andaz, local evidence is available but fresh public research continues in the separate existing `research_brief`/unified signed search path. Stage B exact-page extraction and publish/spend remain OFF.

Private Mac database: `~/.local/share/bhm-research/evidence.sqlite3`, mode 0600, local directory private. Dell original source `~/bhm-research-expansion-20261022/private-evidence.sqlite3` retained, with separate consistent SQLite backup `private-evidence.migration-20261023.sqlite3`. **No private evidence was committed to GitHub.** Backup compressed to 7,104 bytes, transferred through authenticated existing Dell/Mac SSH connector tool calls without exposing archive contents in response, verified at Mac by compressed and uncompressed SHA256 and SQLite quick_check, then atomically installed. Existing Supabase relay, OAuth and worker pairing were not modified.

## Receipts, terminal exit codes and QA

| Receipt / proof | Result |
|---|---|
| Mac fixed authenticated `linux_probe` `893e24cb-9e36-4b61-b3a0-a6f50dbef475` | Exit 0; host `KARAN`, `generic-auto-exec`, Linux |
| Mac resource preflight `a5a0e5d4-7956-4271-8f79-a26831e90bf1` | Mac Python 3.12.3 / 6.1Gi available; nonzero only because expected pre-migration paths absent |
| Dell engine/source/service preflight `a898e6b6-e3f9-45d6-9f67-06ac6247f484` | Exit 0, 4 existing research user services active; Dell private evidence source 90,112 bytes |
| Mac staging Git clone + initial offline QA `4facbc35-4373-46a6-b218-1a7394489dc4` | Exit 0; 73/73 tests |
| Mac isolated venv with pinned free OSS Trafilatura 2.3.1 `1d92c2b4-1adc-4e0d-b3c2-933bedcdfcf6` | Exit 0, pinned lock installation complete; no global Python packages |
| Dell SQLite consistent backup `2c45f6b8-4494-4fef-be10-1dbca7f7bbe4` | Exit 0, `PRAGMA quick_check=ok`, size 90,112; SHA256 `2096c353c0b0e10f0659b23b14719ce679b4a90b068406e7c14fe98552ff7711` |
| Dell snapshot gzip `bd4556d3-c9e5-4560-8a9a-9986450f9fe5` | Exit 0, size 7,104 bytes; compressed SHA256 `e807ea5bbf7b2f8ef526f84388021e77e210f333e61b86f40106fabd31523b74` |
| Mac authenticated two-part archive receipts `f320fdb5-d84f-4f1f-a288-6f9f3bcd1c42`, `c4022158-93b5-4b35-bb46-c063ee8ce10a` | Both exit 0; exactly 9,472 encoded bytes reconstructed, no archive emitted to user |
| Mac snapshot decode, digest and SQLite check `9eade7da-7cf0-4c0f-aa7e-790209b31a62` | Exit 0; exact SHA256; `quick_check=ok`; 5 source records, 0 claims, 12 review-queue entries |
| New Mac-primary bridge + existing tests `613851f7-eda1-4a1d-8d71-631691017f93` | Exit 0, **80/80 tests** |
| Mac selective live cutover `546da83b-14ee-4eeb-b3d9-f0545a26763d` | Exit 0, live local Andaz packet produced; 5 source rows, no price/publish approval; atomic old bridge backup |
| Mac→Dell signed subordinate search live `6a91ff1a-19d2-4ce8-9783-ebf7c8818af1` | Exit 0, `primary=mac-linux`, `signed_device_pair_verified=true`, `signed_dell_discovery`, **3 discovery queries**, publish false, price approval false, Stage B false |
| Post-cutover Mac health `24f7680c-fb18-4f54-bb04-7c7cf5c8bed3` | Exit 0; active Marketing queue timer; 6.1Gi available RAM, load avg 0.07/0.13/0.09; Mac DB hash exact; live Andaz Mac packet passes |

**Live bridge SHA256:** `93580f6b17344fb8a73c2b5e50709f9b6be75c929fcc049ed9d65f5c34f1f081`.  
**Original bridge backup SHA256:** `e2c0b5c80ca4de6c06b9f19059cb5b455ae5e6a939bfd077633f459b2fba2682`.  
**Mac/Dell evidence DB SHA256:** `2096c353c0b0e10f0659b23b14719ce679b4a90b068406e7c14fe98552ff7711`.

## Live architectural boundaries

- **Mac primary:** Marketing Brain Supervisor v2 and research local evidence-memory/packet computation; `research_market` bridge primary host is `mac-linux`. No consumer query changes required for existing `moksha_arambol` market task.
- **Dell supporting worker:** original `bhm-searxng`, `bhm-research-relay`, `bhm-marketing-research-api`, `bhm-autonomy-controller` remain intact, and live signed discovery test succeeded. Dell source database unchanged.
- **Mac isolation:** Pinned private development checkout `~/bhm-mac-research-stage-20261023`, private DB in dedicated local store, new source files mode 0600. No system-wide Python packages, root, sudoers, new daemon ports, SSH keys or permissions changes.
- **Mac extractor library available, crawling disabled:** Do not infer Stage B site permissions. No new source URL grants, competitor robots/terms authorization, credentialed booking or unattended monitoring. `research_extract` remains separately gated; users should not be told Stage B completed.
- **Business output remains conservative:** `verified_competitors=[]`, `pricing_table=[]`, no auto-approved claim or publication.

## Rollback

The live bridge is a file-level switch. If Mac evidence fails, restore the original Mac bridge **through approved Mac user-level execution**:
1. Verify the immutable backup path and checksum, and preserve current diagnostic receipts.
2. Atomically copy `/opt/business-house-matrix/marketing/brain/research_market_bridge.py.pre-mac-primary-20261023` back to `research_market_bridge.py` (the backup is not to be deleted). Verify SHA256 = `e2c0b5c80ca4de6c06b9f19059cb5b455ae5e6a939bfd077633f459b2fba2682`.
3. Run a bounded `research_market` signed Dell test and restore the routing policy to Dell primary only after verification. Existing Dell services already remain running.
4. Keep both private evidence databases and historical audit receipts. Do not delete or overwrite either database in rollback.

## Outstanding unrelated security and product gates

Security [Issue #14](https://github.com/aarondash5-star/business-house-matrix/issues/14) concerned approval for a **new Mac fixed-function Stage B attestation operation**; this has NOT been deployed or approved merely because the normal Mac fixed probe now passes. Stage B additionally requires verified robots/terms for exactly `happypandahostel.com` and `thepeacehostel.in`, source and human reviewer identities, and signed negative live extraction tests.

Draft [PR #4](https://github.com/aarondash5-star/business-house-matrix/pull/4) remains **unmerged**. Selective live Mac primary installation from its pinned commit is separately recorded here. No publication, advertising spend, production website, booking/PMS, root, permission, or live Supabase gateway changes.

**Scope-certified:** Mac research evidence primary + existing signed Dell search support.  
**Not certified:** Stage B automated source extraction or verified Andaz competitor prices.
