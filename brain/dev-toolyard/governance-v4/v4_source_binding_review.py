"""Pure V4 source-binding release review (NOT a host installer).

It prepares the exact set of source-integrity bindings required before the
shared controller can even be considered for a governed upgrade. This module
does not write files, restart services, sign approvals, dispatch workers,
change root permissions or grant production authority.
"""
from __future__ import annotations
import ast
import hashlib
import json
from typing import Any

OLD_ADAPTER_SHA = "16f54c4ae1d97699786b649e84c94df2abb673b0682a20045d55399399217b79"
V4_ADAPTER_SHA = "116f435279bbe7e0cc8281ab513e319926b846ab6ae25752bccc3fc6746fb773"
V4_GUARD_SHA = "90f0a62cc6cfaf1458f0684363ffb9288c900ba0ade707908da0877447249e30"
V13_GATE_SHA = "7a989c6b484a13a4fdf349d698a6a1bf9e8d9b1afa9684508606bc08c036283e"
V13 = "yard-execution-enforcement-v1.3.0-20261026"
V14 = "yard-execution-enforcement-v1.4.0-20261026"
GUARD_FILE = "yard_execution_guard_v13.py"
LEDGER_V13 = "yard_exec_bindings_v13.json"
LEDGER_V14 = "yard_exec_bindings_v14.json"

class ReleaseDenied(ValueError):
    pass

def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()

def demand(actual: bytes, expected: str, reason: str):
    if not isinstance(actual, bytes) or digest(actual) != expected:
        raise ReleaseDenied(reason)

def render_candidate(original_gate: bytes, original_adapter: bytes,
                     reviewed_adapter: bytes, reviewed_guard: bytes,
                     pinned_ledger: dict[str, Any]) -> dict[str, Any]:
    """Return bytes and a release manifest only after all existing pins check."""
    for payload, expected, reason in (
        (original_gate, V13_GATE_SHA, "gate_source_drift"),
        (original_adapter, OLD_ADAPTER_SHA, "old_adapter_drift"),
        (reviewed_adapter, V4_ADAPTER_SHA, "v4_adapter_drift"),
        (reviewed_guard, V4_GUARD_SHA, "new_guard_drift"),
    ):
        demand(payload, expected, reason)
    if not isinstance(pinned_ledger, dict) or set(pinned_ledger) != {
        "version", "production_live", "external_paths_certified", "bindings"
    }:
        raise ReleaseDenied("invalid_existing_ledger")
    old = pinned_ledger["bindings"]
    if (pinned_ledger["version"] != V13 or
        pinned_ledger["production_live"] is not False or
        pinned_ledger["external_paths_certified"] is not False or
        not isinstance(old, dict) or
        old.get("yard_auto_adapter_v1.py") != OLD_ADAPTER_SHA):
        raise ReleaseDenied("untrusted_existing_policy")
    if "adapter_guard_v4.py" in old or LEDGER_V14 in old:
        raise ReleaseDenied("unexpected_previous_upgrade")
    if len(old) != 20 or any(not isinstance(k, str) or
                            not isinstance(v, str) or len(v) != 64
                            for k, v in old.items()):
        raise ReleaseDenied("unexpected_binding_scope")
    text = original_gate.decode("utf-8")
    old_core = ("CORE=['quality_admission.py','quality_gate.py','project_registry.py',"
                "'toolyard_qa_standard_v1.py','yard_auto_adapter_v1.py']")
    new_core = old_core[:-1] + ",'adapter_guard_v4.py']"
    old_lines = (
        ("LEDGER=ROOT/'yard_exec_bindings_v13.json'",
         "LEDGER=ROOT/'yard_exec_bindings_v14.json'"),
        ("VERSION='yard-execution-enforcement-v1.3.0-20261026'",
         "VERSION='yard-execution-enforcement-v1.4.0-20261026'"),
        (old_core, new_core),
    )
    for before, after in old_lines:
        if text.count(before) != 1:
            raise ReleaseDenied("unreviewed_gate_source_layout")
        text = text.replace(before, after, 1)
    ast.parse(text, filename=GUARD_FILE)
    result = dict(old)
    result["yard_auto_adapter_v1.py"] = V4_ADAPTER_SHA
    result["adapter_guard_v4.py"] = V4_GUARD_SHA
    policy = {"version":V14, "production_live":False,
              "external_paths_certified":False,"bindings":result}
    old_policy = {"version":V13,"production_live":False,
                  "external_paths_certified":False,"bindings":dict(old)}
    return {
        "review_only":True,
        "authorization":"owner_signed_release_action_missing",
        "effective_host_changes":False,
        "source": {
          "yard_auto_adapter_v1.py":reviewed_adapter,
          "adapter_guard_v4.py":reviewed_guard,
          GUARD_FILE:text.encode("utf-8"),
        },
        "candidate_ledger":policy,
        "rollback_pins":{
          "yard_auto_adapter_v1.py":OLD_ADAPTER_SHA,
          GUARD_FILE:V13_GATE_SHA,
          LEDGER_V13:digest(json.dumps(old_policy,sort_keys=True).encode("utf-8")),
        },
        "manifest":{
          "schema":1,
          "project":"matrix_dev_manager",
          "phase":"v4_review_only",
          "shared_controller_promotion":False,
          "new_source_hashes":{
             "yard_auto_adapter_v1.py":V4_ADAPTER_SHA,
             "adapter_guard_v4.py":V4_GUARD_SHA,
             GUARD_FILE:digest(text.encode("utf-8")),
          },
          "enforcement_policy_version":V14,
          "source_binding_count":len(result),
          "production":False,"spend":False,
          "pending_gates":[
            "signed_release_broker",
            "exclusive_queue_lease",
            "trusted_offline_qa",
            "atomic_backup_swap",
            "negative_canary",
            "tested_rollback",
            "owner_review",
          ],
        },
    }

def inspect_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    """An inert candidate cannot authorize itself even with passing tests."""
    if candidate.get("review_only") is not True or candidate.get("authorization") != "owner_signed_release_action_missing":
        raise ReleaseDenied("candidate_authority_violation")
    policy = candidate["candidate_ledger"]
    if (policy.get("version")!=V14 or policy.get("production_live") is not False or
        policy.get("external_paths_certified") is not False or
        policy["bindings"].get("adapter_guard_v4.py") != V4_GUARD_SHA):
        raise ReleaseDenied("candidate_policy_drift")
    for name, source in candidate["source"].items():
        if name not in candidate["manifest"]["new_source_hashes"]:
            raise ReleaseDenied("unlisted_source")
        if digest(source)!=candidate["manifest"]["new_source_hashes"][name]:
            raise ReleaseDenied("source_integrity_drift")
    return {"passed":True,"mode":"source_review_only",
            "production_authorized":False,
            "host_write_authorized":False,
            "bound_sources":len(policy["bindings"])}
