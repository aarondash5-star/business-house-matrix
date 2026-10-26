"""Purely in-memory Dell V4 file-transaction and restoration model.

This is intentionally NOT a host activation runner. It has no disk writes,
network, shell, sudo, systemd, signing, credentials, or file path arguments.
It models exact four-file apply ordering and original-three-file restoration
under injected interruptions before authorizing an independent real host runner.
"""
from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from typing import Mapping

OLD_NAMES = frozenset(("yard_auto_adapter_v1.py",
                       "yard_execution_guard_v13.py",
                       "yard_exec_bindings_v13.json"))
ORDER = ("yard_auto_adapter_v1.py", "adapter_guard_v4.py",
         "yard_exec_bindings_v14.json", "yard_execution_guard_v13.py")
NEW_NAMES = frozenset(ORDER)

class ModelDenied(ValueError): pass

@dataclass(frozen=True)
class TransactionReceipt:
    outcome: str
    staged: tuple[str,...]
    restored: tuple[str,...]
    old_state_identical: bool
    applied_state_pins_verified: bool
    simulation_only: bool = True
    signing_verified: bool = False
    service_restarted: bool = False
    deployed: bool = False

def digest(data:bytes)->str:
    return sha256(data).hexdigest()

def _validate(d:Mapping[str,bytes], allowed:frozenset[str], pins:Mapping[str,str], kind:str):
    if set(d)!=allowed or set(pins)!=allowed:
        raise ModelDenied("unexpected_"+kind+"_file_set")
    for name in allowed:
        blob=d[name]
        if type(blob) is not bytes or len(blob)==0 or len(blob)>2_000_000:
            raise ModelDenied("invalid_"+kind+"_data")
        if digest(blob)!=pins[name]:
            raise ModelDenied(kind+"_hash_drift:"+name)

def simulate(old:Mapping[str,bytes], candidate:Mapping[str,bytes],
             old_pins:Mapping[str,str], candidate_pins:Mapping[str,str],
             fail_after:int|None=None)->TransactionReceipt:
    """In-memory only; model every interrupted transition and full restoration."""
    _validate(old,OLD_NAMES,old_pins,"old")
    _validate(candidate,NEW_NAMES,candidate_pins,"candidate")
    if fail_after is not None and (type(fail_after) is not int or not 0<=fail_after<=4):
        raise ModelDenied("invalid_fault_step")
    fs=dict(old)  # synthetic isolated live dictionary, never real files
    backup=dict(fs)
    applied:list[str]=[]
    try:
        if fail_after == 0:
            raise RuntimeError("synthetic_interrupt_before_first_write")
        for i,name in enumerate(ORDER,1):
            fs[name]=candidate[name]
            applied.append(name)
            if fail_after == i:
                raise RuntimeError("synthetic_interrupt_after_"+str(i))
        if set(fs)!=(OLD_NAMES|{"adapter_guard_v4.py","yard_exec_bindings_v14.json"}):
            raise ModelDenied("unexpected_post_apply_files")
        for name in ORDER:
            if digest(fs[name])!=candidate_pins[name]:
                raise ModelDenied("post_apply_drift:"+name)
        if digest(backup["yard_exec_bindings_v13.json"]) != old_pins["yard_exec_bindings_v13.json"]:
            raise ModelDenied("rollback_original_ledger_changed")
        return TransactionReceipt("SIMULATED_APPLY_SUCCESS",tuple(applied),(),
                                  old_state_identical=False,applied_state_pins_verified=True)
    except RuntimeError:
        # No file is deleted from a physical host; restoration occurs in memory.
        for name in list(fs):
            if name not in OLD_NAMES:
                fs.pop(name)
        for name in OLD_NAMES:
            fs[name]=backup[name]
        if fs!=backup:
            raise ModelDenied("simulation_rollback_integrity_failed")
        return TransactionReceipt("SIMULATED_ROLLBACK_SUCCESS",tuple(applied),
                                  tuple(sorted(OLD_NAMES)),old_state_identical=True,
                                  applied_state_pins_verified=False)
