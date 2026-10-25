# Dell Dev Tool Yard — Universal Default-Attachment & Auto-Adapter Rule (V1.2)

**Effective:** 2026-10-26 (implementation activated on Dell host 2026-10-25 19:08 UTC)  
**Status:** DEPLOYED AND QA-VERIFIED for controller-mediated tasks and bounded local tool admission. **Not** a license for unrestricted CLI execution or automatic public production release.  
**Policy module:** `yard_auto_adapter_v1.py` SHA-256 `bd68decf7ce0f19ef8713dca1fd1c8491779ade794b63fc652d26fc070fbf9d7`.  
**Controller:** `controller.py` SHA-256 `1a3285a0d39d4bf4875b90aadf9ed0c0363e525efe0ab112c90caa53a757a2d4`.

## Rule adopted

**Every existing/new registered Dell Tool Yard action inherits Universal QA Standard V1 by default** at controller task admission, and the same binding appears in its completion receipt. If its action or project/manifest is unrecognized, deny rather than run without governance.

**Tools missing adapters enter automatic bounded onboarding:** discovery → classified QA profile → generated per-tool manifest → safe version probe or parse-only syntax check → **QA-only yard inventory admission**, or quarantine if unsafe/unrecognized/changed. Production/live execution is a separate project-specific release procedure. There is no wildcard shell or automatic authorization for newly discovered code.

The default is **`inherit_or_quarantine`**, not `auto_execute`.

## What is actually installed

- **All 13 original controller action types** use `yard_auto_adapter_v1.inherit(project, action, manifest)` at admission; the universal quality receipt continues to record mandatory checks, source/project scoping, human review and release status without granting them.
- Dell runtime auto-reconciles the tool registry on `controller.py tick` **when the controller is running/ticked**, at most every 300 seconds or when the `managed-tools` directory changes. This is a bounded scheduled-on-use process, **not** a claim that a separate 24/7 watcher is running.
- Recognized CLI templates: `python3`, `node`, `npm`, `npx`, `git`, `gh`, `blender`, `ffmpeg`, `google-chrome`, `podman`. These receive SHA-pinned `probe_version` only.
- Local script templates: `.py` via Python AST parse; `.js/.mjs` via Node `--check`; `.sh` via Bash `-n`. **Parsing is not execution** and does not certify integration/performance/correctness.
- Discovery locations: direct central Yard controller scripts; approved `managed-tools` root; first-level scripts in Dell workspaces with prefixes `matrix-`, `threejs-`, `shaadi-`, `delulu-`, `wp-manager-`, `eccrm-`, `andaz-`, `moksha-`, and their immediate `src`, `scripts` and `tools` subfolders. No recursive dependency harvesting; no credentials/keys or arbitrary filesystem scans.
- Each discoverable tool gets a SHA-pinned restricted adapter manifest under `/var/lib/generic-linux-automator-exec/matrix-controller/yard-adapter-manifests-v1/`. The registry `yard_tool_adapters_v1.json` is owner-private.
- The tool adapter preflight checks the **current** binary SHA and scope. Different binary, unsupported operation, missing tool, unauthorized path or unreviewed template is denied.
- No permission changes, spend, hosting/publication, root/SSH escalation, automatic pull-request merge or production Go Live enabled.

## Verified Dell inventory

After V1.2 activation:

| Check | Result |
|---|---|
| Inventoried bounded tool entrypoints | **83** |
| QA-only admissions after reviewed version/syntax checks | **83** |
| Per-tool generated adapter manifests | **83** |
| Full functional adapters newly certified by this rollout | **0** (not claimed) |
| Production Go Live authorizations | **0** |
| Independent rootless/no-network adversarial QA | **6/6 passed**, batch `yard-auto-adapter-v12-independent-20261026` |
| Existing controller tests | PASS |
| Existing standard + adapter tests | PASS |

**Important:** “83 admitted” means **only** a bounded QA probe or syntax validation was accepted. These 83 tools are **not** approved to perform their entire workload. The existing controller actions, project contracts, independent reviewer and owner-release policies continue to govern real execution.

The rootless QA used a read-only Podman sandbox with no network. It rejected unknown actions, fake model approval, automatic production claims and arbitrary unknown-tool execution. Rootless QA source fingerprint: `c7c34dce445b670ddd0dbdabb56bfc63d368c4f67cb8e3a51cac34336fc39b9a`.

## Admission and Go Live lifecycle

1. **Discovery:** a new tool enters a scoped Yard directory or receives an owner-reviewed controller registration. The default policy attaches automatically when the controller evaluates the entrypoint.
2. **Scaffold and checks:** a bounded adapter manifest is produced with project/source identity, SHA, QA profile and permitted operations. If the safe template can parse/version-check it, the **QA-only** operation is admitted; otherwise it remains quarantined.
3. **Functional adapter:** project-specific developers must implement narrowly scoped, fixed-function operations and certify them under the original project manifest and negative tests. Generic syntax/version probes **cannot** grant real tool operation.
4. **Independent QA:** verify artifact/output, real-world UI or code behavior, attack/denial paths, privacy, performance, fallback, owner scope, recovery and supply independently controlled evidence.
5. **Go Live:** request exact target/environment approval and run existing `quality_admission.release_check` with genuine independent QA, artifact hash and owner release approval. **Never** treat `qa_probe_accepted` as an owner-release token.
6. **Changes:** changed binary SHA triggers a new probe and revised manifest. Until reapproved, previously certified operation checks fail. Missing tools are quarantined.

## Coverage not overstated

This policy **does not intercept direct/unmediated SSH shell commands**, arbitrary processes launched outside the controller, remote SaaS connectors, tools outside curated Yard scan paths, or tools buried deep in dependency trees. It does not magically make all APIs or providers compliant. For genuinely universal execution enforcement, install independently reviewed fixed-function adapters at each external execution gateway rather than weakening policy or adding unrestricted shell transport.

**The 83 entries represent the currently discovered scoped Yard inventory, not every executable installed on the computer.**

## How to verify and maintain

```bash
cd /var/lib/generic-linux-automator-exec/matrix-controller
python3 controller.py selftest
python3 -m unittest -q test_yard_auto_adapter_v1 test_toolyard_qa_standard_v1
python3 yard_auto_adapter_v1.py status
python3 yard_auto_adapter_v1.py reconcile
python3 yard_auto_adapter_v1.py check python3 probe_version
python3 controller.py status
```

Current runtime quality source: `toolyard_qa_standard_v1.py`. Existing universal process: [Universal QA Standard V1](./QA_UNIVERSAL_STANDARD_V1_20261025.md) and [Dell rollout](./DELL_COVERAGE_AND_ROLLOUT_20261025.md).

Owner-private rollback receipts remain on Dell:
- `matrix-controller/release-backups/yard-auto-adapter-v1-20261026/PROMOTION_ROLLBACK_RECEIPT_FINAL.json` (controller update; preserves delegated remote tasks)
- `matrix-controller/release-backups/yard-auto-adapter-v11-20261026/PROMOTION_ROLLBACK_RECEIPT.json`
- `matrix-controller/release-backups/yard-auto-adapter-v12-20261026/PROMOTION_AND_ROLLBACK_RECEIPT.json`

The first controller promotion backed out after a receipt parser bug; the subsequent verified atomic promotion succeeded. The first V1.1 parser status-key bug was also safely rolled back before its corrected promotion. **Do not suppress those failed attempts from the audit trail.**

## Future acceptance requirement

The universal quality baseline is mandatory for **all newly controller-registered tools**. Tool yard maintainers must not mark a tool `functional_certified` or `production_live` without exact independent evidence, supported method/version, owner approval, and a working rollback. A version string, AST parse, LLM review or fake reviewer signature is never sufficient.
