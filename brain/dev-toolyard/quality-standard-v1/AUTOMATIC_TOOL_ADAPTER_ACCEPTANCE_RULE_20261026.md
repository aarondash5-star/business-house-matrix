# Dell Tool Yard — Automatic Adapter Admission and Go-Live Rule

**Effective:** 2026-10-26 IST. **Controller integration:** `yard_auto_adapter_v1.py` v1.2.0 and `toolyard_qa_standard_v1.py`. **Decision:** Every discovered tool inherits the universal quality requirement. No tool without a certifiable adapter and scoped evidence may execute via the governed yard. A tool's successful installation is not operational approval.

## Default lifecycle
1. **DISCOVER:** Inventory executables and scripts under trusted Dell locations. Resolve paths, reject symlinks/untrusted roots, calculate SHA-256 and assign a conservative profile. Newly found or changed binaries default to quarantine, not production.
2. **AUTO-ATTACH:** Generate a per-tool manifest carrying the QA profile and mandatory tests. Record exact binary identity, source SHA and tool/operation scope.
3. **BUILD THE BOUNDED ADAPTER:** Only fixed-function operations; no arbitrary arguments, shell/root privilege, hidden network effects, production writes or security-policy bypass. Version/syntax probes may run only in temporary isolated environments. Add purpose-specific adapters for real work after independent review.
4. **ADAPTER CERTIFICATION:** Confirm source/license integrity, admission identity, negative action-denial tests, isolated tests, test artifacts, rollback, project/manifests and per-operation allowlist. Reject mutated binaries until re-reviewed.
5. **ACCEPT TO TOOL YARD:** Explicitly mark the *tested operation* accepted. A `probe_version` or `syntax_probe` admission only allows the probe; it is NOT approval to build, publish, invoke arbitrary CLI or access customer data.
6. **GO-LIVE GATE:** Separately bind an enrolled project, frozen requirements, independent QA and actual owner release authorization. Only an exact approved operation/artifact may be promoted. Record rollback evidence. Tool installation and quality score do not confer go-live.

## Verified current coverage (2026-10-26)
- Central Dell controller: **13 action types**, each inherits `toolyard-qa-v1`.
- Auto adapter registry: **83 discovered tools/scripts**, **83 QA-probe-only accepted**, **0 quarantined at last reconciliation**. QA-probe-only means **NOT general operational certification**. Newly discovered and changed tools must repeat admission. This inventory is not a proof that all scripts are safe to execute.
- `test_yard_auto_adapter_v1.py`: **10/10 PASS**, including changed-binary denial, unknown tool denial, no automatic production, automatic QA inheritance and scaffold/syntax-only checks.
- Live fixed-function preflight: Python and ffmpeg `probe_version` accepted; deliberately unapproved ffmpeg `unrestricted_exec` correctly rejected with `AdapterDenied: operation_not_certified`.
- Registry: `matrix-controller/yard_tool_adapters_v1.json`. Generated per-tool manifests: `matrix-controller/yard-adapter-manifests-v1/`.
- Existing owner-intake, independent QA and release gates remain mandatory. Never bypass them; no direct SSH interception has been claimed.

## Work required for full operational admission
For each of the 83 entries, add explicit supported operations only when the project actually needs them. Examples:
- Blender: inspect/validate an approved .blend and sampled frames in a sandbox; separate owner approval for rendering changes.
- ffmpeg: fixed media probe with input allowlist; generation/transcode requires new bounded adapter, source fidelity and QA.
- Chrome/Playwright: preapproved URLs/domains and screenshot/interaction tests with privacy controls and browser evidence.
- Python/Node/npm: project-manifest-scoped tests/builds with dependency SHA, isolated environment and negative security tests.
- Git/GitHub/Vercel: read-only inspection first; merging and publishing require independent release and owner authorization.
- Project scripts: syntax validation is not functional review. Bind exact project/manifest, test behavior and forbid foreign-project dispatch.
Tool families may share QA templates, but each operation must be explicitly certified.

## Commands on Dell
```bash
cd /var/lib/generic-linux-automator-exec/matrix-controller
python3 -m unittest -v test_yard_auto_adapter_v1
python3 yard_auto_adapter_v1.py status
python3 yard_auto_adapter_v1.py check ffmpeg probe_version
# Intentionally denied:
python3 yard_auto_adapter_v1.py check ffmpeg unrestricted_exec
python3 controller.py selftest
```

## Safety and accuracy
- The auto-attachment and registry are **active for the governed controller**. This cannot automatically intercept someone running `ffmpeg`, `node` or `git` directly from an unrestricted SSH terminal; they must use the governed Tool Yard route or obtain a separately enforced gateway.
- Do not set tools to `live` merely because their version or syntax probe passed. The per-tool registry currently records `production_live=false` and `owner_approved=false`.
- Record capabilities and checks before enabling fixed-function operational adapters. A full yard-wide runtime interception or automatic tool adapter generator that safely enables all operations is **not yet certified**.
- No changes to production websites, security ACLs, external providers or owner release records by this rule.
