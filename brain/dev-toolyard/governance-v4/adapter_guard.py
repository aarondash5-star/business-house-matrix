#!/usr/bin/env python3
"""Bounded, read-only, backward compatible loader for Dell v1 tool inventory.

Fixes the known 80,005-byte vs 80,000-byte outage WITHOUT granting new
execution, publication, sudo privileges, cross-project tools or auto-admission.
"""
from __future__ import annotations
import json
import os
import re
import stat
from pathlib import Path

MAX_REGISTRY_BYTES=524288
MAX_TOOLS=1200
MAX_ENTRY_BYTES=8192
NAME=re.compile(r"^[a-z][a-z0-9_-]{1,39}$")
class AdapterRegistryDenied(ValueError):pass

def checked_registry(path: Path) -> dict:
    p=Path(path)
    if p.is_symlink() or not p.is_file():raise AdapterRegistryDenied("registry_missing_or_symlink")
    s=p.stat()
    if not stat.S_ISREG(s.st_mode) or s.st_size<10 or s.st_size>MAX_REGISTRY_BYTES:
        raise AdapterRegistryDenied("registry_invalid")
    if s.st_mode & (stat.S_IWGRP|stat.S_IWOTH):
        raise AdapterRegistryDenied("registry_mutable")
    if s.st_nlink!=1:raise AdapterRegistryDenied("registry_hardlink_denied")
    try:
        record=json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError,UnicodeError) as e:
        raise AdapterRegistryDenied("registry_parse_invalid") from e
    if not isinstance(record,dict) or record.get("schema")!=1 or not isinstance(record.get("tools"),dict):
        raise AdapterRegistryDenied("registry_schema_invalid")
    if len(record["tools"])>MAX_TOOLS:raise AdapterRegistryDenied("registry_tools_exceeded")
    for name,value in record["tools"].items():
        if not isinstance(name,str) or not NAME.fullmatch(name):
            raise AdapterRegistryDenied("registry_tool_name_invalid")
        if not isinstance(value,dict) or len(json.dumps(value,ensure_ascii=False).encode())>MAX_ENTRY_BYTES:
            raise AdapterRegistryDenied("registry_tool_entry_invalid")
        operations=value.get("operations",[])
        if not isinstance(operations,list) or any(o not in ("probe_version","syntax_probe") for o in operations):
            raise AdapterRegistryDenied("registry_untrusted_operations")
        if value.get("production_live") is True or value.get("unbounded_execution_permitted") is True:
            raise AdapterRegistryDenied("registry_privilege_escalation")
    return record["tools"]

def summary(path:Path):
    tools=checked_registry(path)
    return {"rule":"yard-adapter-bound-v4","state":"validated","size":Path(path).stat().st_size,
            "count":len(tools),"qa_probe_only":True,
            "production_live":False,"automatic_release":False,
            "quarantined":sum(x.get("state")!="accepted_qa_probe_only" for x in tools.values())}

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("registry",type=Path)
    a=p.parse_args()
    try:print(json.dumps(summary(a.registry),indent=2))
    except (AdapterRegistryDenied,OSError) as e:
        print(json.dumps({"state":"denied","reason":str(e),"production_live":False}))
        raise SystemExit(2)
