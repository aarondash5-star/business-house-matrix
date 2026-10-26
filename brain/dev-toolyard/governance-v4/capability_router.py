#!/usr/bin/env python3
"""Deterministic, scoped Dev Yard v4 worker-fit routing decision.

No job dispatch. Presence of a tool or heartbeats alone is never proof that a
worker can implement a feature. Every declared capability must have actual
smoke evidence, scoped tool rights, and a healthy bound runner.
"""
from __future__ import annotations
import json,re
from datetime import datetime,timezone
SAFE=re.compile(r"^[a-z][a-z0-9_-]{1,63}$")
class RouteDenied(ValueError):pass

def choose(task,workers):
    if not isinstance(task,dict) or not isinstance(workers,list):
        raise RouteDenied("invalid_task_or_workers")
    project=task.get("project"); manifest=task.get("manifest")
    if not all(isinstance(x,str) and SAFE.fullmatch(x) for x in (project,manifest)):
        raise RouteDenied("scoped_project_manifest_required")
    base={"project":project,"manifest":manifest,"status":"blocked","worker":None,
          "automatically_dispatched":False,"production_authorized":False,
          "owner_approval_preserved":True,"reason":"no_capable_worker"}
    required=task.get("required_capabilities")
    if not isinstance(required,list) or not required or len(required)>30 or any(not isinstance(x,str) or not SAFE.fullmatch(x) for x in required):
        return base | {"reason":"critical_capabilities_missing"}
    if task.get("max_new_spend")!=0:
        return base | {"reason":"no_new_spend_without_approval"}
    if task.get("owner_scoped_intake") is not True or task.get("brief_pinned") is not True:
        return base | {"reason":"intake_or_brief_unverified"}
    if task.get("action") not in ("dev_project_build","sandbox_qa","repair_known_issue"):
        return base | {"reason":"unknown_or_unbounded_action"}
    candidates=[]
    for w in workers:
        if not isinstance(w,dict) or w.get("project")!=project or w.get("ready") is not True:
            continue
        if w.get("workspace_isolated") is not True or w.get("heartbeat_age_seconds",1e9)>60:
            continue
        if w.get("lane") not in ("development","operations") or w.get("arbitrary_shell") is True:
            continue
        if w.get("new_spend_required") is True or w.get("pending_job") is True:
            continue
        caps=w.get("capabilities",{})
        if not isinstance(caps,dict): continue
        if not all(caps.get(c)=={"probe":"passed","feature_smoke":"passed","project":project} for c in required):
            continue
        if task["action"] not in w.get("approved_actions",[]):continue
        if not isinstance(w.get("worker_id"),str) or not SAFE.fullmatch(w["worker_id"]):continue
        candidates.append(w)
    if len(candidates)==0:return base
    candidates.sort(key=lambda w:(w.get("heartbeat_age_seconds",99),w["worker_id"]))
    return base | {"status":"worker_fit_verified","reason":"needs_explicit_controller_dispatch",
                   "worker":candidates[0]["worker_id"],
                   "lane":candidates[0]["lane"],
                   "capabilities":required}

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("task")
    p.add_argument("workers")
    args=p.parse_args()
    from pathlib import Path
    if any(Path(x).is_symlink() or Path(x).stat().st_size>30000 for x in (args.task,args.workers)):
        raise SystemExit("invalid manifest")
    print(json.dumps(choose(json.load(open(args.task)),json.load(open(args.workers))),indent=2))
if __name__=="__main__":main()
