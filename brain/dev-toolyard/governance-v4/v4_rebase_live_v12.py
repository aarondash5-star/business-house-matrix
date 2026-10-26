"""Pure Dell live V1.2 adapter -> V4 registry-guard candidate rebase.

NO filesystem writes, service restarts, owner signature, approval mutation,
deploy instruction, privilege changes, or host activation.

Reconstruct the live V1.2 source from the original reviewed V4 source only
if the SHA exactly matches the observed current host source. This allows CI
to prove that this patch is a transformation of the *actual* live adapter
rather than silently downgrading to the stale V1.1 adapter.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

PREVIOUS_REVIEWED_V4_SHA = "116f435279bbe7e0cc8281ab513e319926b846ab6ae25752bccc3fc6746fb773"
CURRENT_LIVE_ADAPTER_SHA = "adad20add5e247c515c48d8e2d0c61f2b91e2238d489ed8b4c2e674c845d1abe"
CURRENT_LEDGER_SHA = "9c084832984c1471a22079cc606daccd0a49b78c942ddfee0800a800176c43a9"
CURRENT_GUARD_SHA = "7a989c6b484a13a4fdf349d698a6a1bf9e8d9b1afa9684508606bc08c036283e"
REVIEWED_V4_GUARD_SHA = "90f0a62cc6cfaf1458f0684363ffb9288c900ba0ade707908da0877447249e30"
V13 = "yard-execution-enforcement-v1.3.0-20261026"
V14 = "yard-execution-enforcement-v1.4.0-20261027"
REBASED_ADAPTER_VERSION = "yard-auto-adapter-v1.2.2-v4-bounded-20261027"
REBASED_ADAPTER_SHA = "2ea43e8953c59726f510b6db9a8d0127a64efd7acb0fb824db5c70cb130a8837"
REBASED_ENFORCEMENT_SHA = "664d4681747282561755dd34201210ce19306e15beeb506c8c02a024bf7ae644"
REBASED_LEDGER_CANONICAL_SHA = "81edd213acfd4c66359d1a217a62c392c283358e972a7ea87b4948687fc5012f"

class RebaseDenied(ValueError):
    pass

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def exactly(text: str, before: str, after: str, label: str) -> str:
    if text.count(before) != 1:
        raise RebaseDenied("unexpected_source_layout:" + label)
    return text.replace(before, after, 1)

_REVIEWED_LOAD = '''def load(path=REGISTRY):
    """Load a bounded QA-only inventory; fail closed on malformed privileges."""
    from adapter_guard_v4 import checked_registry, AdapterRegistryDenied
    try:
        return checked_registry(path)
    except AdapterRegistryDenied as exc:
        raise AdapterDenied(str(exc)) from exc
'''

_LIVE_LOAD = '''def load(path=REGISTRY):
    p=Path(path)
    if p.is_symlink():raise AdapterDenied("registry_symlink")
    if not p.exists():return {}
    if not p.is_file() or p.stat().st_size>REGISTRY_MAX_BYTES:raise AdapterDenied("registry_invalid")
    d=json.loads(p.read_text())
    if d.get("schema")!=1 or not isinstance(d.get("tools"),dict):
        raise AdapterDenied("schema_invalid")
    if len(d["tools"])>REGISTRY_MAX_TOOLS:raise AdapterDenied("registry_too_many_tools")
    return d["tools"]
'''

_LIVE_SAVE_PREFIX = '''def save(d,path=REGISTRY):
    if d.get("schema")!=1 or not isinstance(d.get("tools"),dict):
        raise AdapterDenied("schema_invalid")
    if len(d["tools"])>REGISTRY_MAX_TOOLS:raise AdapterDenied("registry_too_many_tools")
    if len((json.dumps(d,sort_keys=True,indent=2)+"\\n").encode("utf-8"))>REGISTRY_MAX_BYTES:
        raise AdapterDenied("registry_too_large")
    p=Path(path)
'''

_REVIEWED_SAVE_PREFIX = '''def save(d,path=REGISTRY):
    p=Path(path)
'''

_REVIEWED_TMP_GUARD = '''    from adapter_guard_v4 import checked_registry, AdapterRegistryDenied
    try:
        checked_registry(tmp)
    except AdapterRegistryDenied as exc:
        tmp.unlink(missing_ok=True)
        raise AdapterDenied("registry_save_bound_rejected") from exc
'''

_REBASED_LOAD = '''def load(path=REGISTRY):
    """Keep V1.2 hard limits and require the independently pinned V4 guard."""
    p=Path(path)
    if p.is_symlink():raise AdapterDenied("registry_symlink")
    if not p.exists():return {}
    if not p.is_file() or p.stat().st_size>REGISTRY_MAX_BYTES:raise AdapterDenied("registry_invalid")
    from adapter_guard_v4 import checked_registry, AdapterRegistryDenied
    try:
        tools=checked_registry(p)
    except AdapterRegistryDenied as exc:
        raise AdapterDenied(str(exc)) from exc
    if len(tools)>REGISTRY_MAX_TOOLS:raise AdapterDenied("registry_too_many_tools")
    return tools
'''

def reconstruct_live_unchanged(reviewed_v4: bytes) -> bytes:
    """Rebuild current *actual* V1.2 source by reversing precise V4 deltas."""
    if sha(reviewed_v4) != PREVIOUS_REVIEWED_V4_SHA:
        raise RebaseDenied("reviewed_v4_digest_drift")
    s = reviewed_v4.decode("utf-8")
    s = exactly(s,
        'VERSION="yard-auto-adapter-v1.2.1-bounded-20261026"\n',
        'VERSION="yard-auto-adapter-v1.2.0-20261026"\n'
        'REGISTRY_MAX_BYTES=1_048_576\nREGISTRY_MAX_TOOLS=512\n',
        "version_and_original_limits")
    s = exactly(s, _REVIEWED_LOAD, _LIVE_LOAD, "original_load")
    s = exactly(s, _REVIEWED_SAVE_PREFIX, _LIVE_SAVE_PREFIX, "original_save_limit")
    s = exactly(s, _REVIEWED_TMP_GUARD, "", "remove_review_only_tmp_guard")
    ast.parse(s,filename="reconstructed_actual_live_adapter_v12.py")
    result=s.encode("utf-8")
    if sha(result) != CURRENT_LIVE_ADAPTER_SHA:
        raise RebaseDenied("reconstructed_source_does_not_match_actual_host")
    return result

def rebase_current_live(live_bytes: bytes) -> bytes:
    if sha(live_bytes) != CURRENT_LIVE_ADAPTER_SHA:
        raise RebaseDenied("live_v12_adapter_drift")
    s=live_bytes.decode("utf-8")
    s=exactly(s,
        'VERSION="yard-auto-adapter-v1.2.0-20261026"\n',
        'VERSION="'+REBASED_ADAPTER_VERSION+'"\n', "new_version")
    s=exactly(s,_LIVE_LOAD,_REBASED_LOAD,"new_v4_load_guard")
    needle='''        json.dump(d,f,sort_keys=True,indent=2);f.write("\\n");f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)
'''
    replace='''        json.dump(d,f,sort_keys=True,indent=2);f.write("\\n");f.flush();os.fsync(f.fileno())
'''+_REVIEWED_TMP_GUARD+'''    os.replace(tmp,p)
'''
    s=exactly(s,needle,replace,"new_v4_save_guard")
    ast.parse(s,filename="yard_auto_adapter_v12_rebased_v14.py")
    return s.encode("utf-8")

def render_guard_and_ledger(original_guard: bytes, ledger_bytes: bytes,
                            rebased_adapter: bytes, v4_guard: bytes) -> dict:
    """Source-only seven-field policy; no host operation or release admission."""
    if sha(original_guard)!=CURRENT_GUARD_SHA:
        raise RebaseDenied("live_guard_digest_drift")
    if sha(ledger_bytes)!=CURRENT_LEDGER_SHA:
        raise RebaseDenied("live_ledger_digest_drift")
    if sha(v4_guard)!=REVIEWED_V4_GUARD_SHA:
        raise RebaseDenied("reviewed_v4_guard_digest_drift")
    if sha(rebased_adapter)!=REBASED_ADAPTER_SHA:
        raise RebaseDenied("rebased_v14_adapter_digest_drift")
    try:
        ledger=json.loads(ledger_bytes)
    except (ValueError,UnicodeError) as exc:
        raise RebaseDenied("invalid_ledger") from exc
    expected_fields={"version","production_live","external_paths_certified","bindings",
                     "actions_bound","independent_human_review","review"}
    if not isinstance(ledger,dict) or set(ledger)!=expected_fields:
        raise RebaseDenied("unreviewed_ledger_schema")
    if not isinstance(ledger["bindings"],dict) or len(ledger["bindings"])!=20:
        raise RebaseDenied("unreviewed_binding_count")
    expected_metadata={"version":V13,"production_live":False,
                       "external_paths_certified":False,
                       "actions_bound":11,
                       "independent_human_review":False,
                       "review":"technical_hash_and_syntax_only"}
    for key,required in expected_metadata.items():
        if type(ledger[key]) is not type(required) or ledger[key]!=required:
            raise RebaseDenied("unreviewed_ledger_policy:"+key)
    if ledger["bindings"].get("yard_auto_adapter_v1.py")!=CURRENT_LIVE_ADAPTER_SHA:
        raise RebaseDenied("live_adapter_not_pinned")
    if "adapter_guard_v4.py" in ledger["bindings"]:
        raise RebaseDenied("upgrade_already_installed")
    gate=original_guard.decode("utf-8")
    old_core="CORE=['quality_admission.py','quality_gate.py','project_registry.py','toolyard_qa_standard_v1.py','yard_auto_adapter_v1.py']"
    new_core=old_core[:-1]+",'adapter_guard_v4.py']"
    gate=exactly(gate,"LEDGER=ROOT/'yard_exec_bindings_v13.json'",
                 "LEDGER=ROOT/'yard_exec_bindings_v14.json'","ledger_location")
    gate=exactly(gate,"VERSION='yard-execution-enforcement-v1.3.0-20261026'",
                 "VERSION='"+V14+"'","enforcement_version")
    gate=exactly(gate,old_core,new_core,"guard_core_modules")
    ast.parse(gate,filename="yard_execution_guard_v14.py")
    if sha(gate.encode("utf-8"))!=REBASED_ENFORCEMENT_SHA:
        raise RebaseDenied("rebased_v14_enforcement_digest_drift")
    new_ledger={**ledger,"version":V14,"bindings":{
        **ledger["bindings"],
        "yard_auto_adapter_v1.py":sha(rebased_adapter),
        "adapter_guard_v4.py":REVIEWED_V4_GUARD_SHA,
    }}
    ledger_canonical=(json.dumps(new_ledger,sort_keys=True,separators=(",",":"))+"\n").encode("utf-8")
    if sha(ledger_canonical)!=REBASED_LEDGER_CANONICAL_SHA:
        raise RebaseDenied("rebased_v14_ledger_digest_drift")
    return {
        "mode":"SOURCE_REBASE_ONLY",
        "host":"dell-linux",
        "project":"matrix_dev_manager",
        "production":False,
        "spend":False,
        "owner_release_present":False,
        "controller_mutated":False,
        "release_authorized":False,
        "source":{
            "yard_auto_adapter_v1.py":rebased_adapter,
            "adapter_guard_v4.py":v4_guard,
            "yard_execution_guard_v13.py":gate.encode("utf-8"),
        },
        "ledger":new_ledger,
        "source_pins":{
            "current_live_adapter_sha256":CURRENT_LIVE_ADAPTER_SHA,
            "current_live_binding_ledger_sha256":CURRENT_LEDGER_SHA,
            "rebased_adapter_sha256":sha(rebased_adapter),
            "v4_guard_sha256":REVIEWED_V4_GUARD_SHA,
            "v14_enforcement_sha256":sha(gate.encode("utf-8")),
            "rebased_binding_count":len(new_ledger["bindings"]),
        }
    }
