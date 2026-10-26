#!/usr/bin/env python3
"""Bounded deterministic follow-up advisor for an already-authorized Yard job.

Can only prepare a reviewable work item. Never launches a model, shell, SSH,
CI, worker, deployment, publication, spend or cross-project replay.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ALLOWED_FAILURES={
    "python_asyncio_taskgroup_cancel": {
        "repair_action":"repair_known_issue",
        "recipe":"python_asyncio_TaskGroup_has_no_cancel",
        "requires_original_failed_test":True,
    },
    "ui_design_fidelity": {
        "repair_action":"dev_project_build",
        "recipe":"bounded_design_revision_after_independent_review",
        "requires_owner_design_review":True,
    }
}
UNSAFE_STATUS={"running","queued","dispatching","delegated","unknown","expired","stale_running","outcome_unknown"}
class RepairDenied(ValueError): pass

def decide(entry:dict)->dict:
    """Emit one bounded approval-gated action proposal. No side effects."""
    if not isinstance(entry,dict) or entry.get("schema_version")!=1:
        raise RepairDenied("invalid_failure_record")
    for k in ("project","manifest","task_id"):
        if not isinstance(entry.get(k),str) or not re.fullmatch(r"[a-z][a-z0-9_-]{1,63}",entry[k]):
            raise RepairDenied("project_manifest_task_required")
    result={"project":entry["project"],"manifest":entry["manifest"],"task_id":entry["task_id"],
            "status":"needs_review","executable":False,"owner_approved":False,
            "release_authorized":False,"auto_publish":False,"auto_retry_uncertain":False}
    if entry.get("task_status") in UNSAFE_STATUS:
        return result | {"reason":"uncertain_or_in_flight_task_never_replay"}
    if entry.get("task_status")!="tests_failed":
        return result | {"reason":"original_failure_not_verified"}
    if entry.get("attempts",0) not in (0,1):
        return result | {"reason":"bounded_retry_limit_reached"}
    if not entry.get("source_sha256") or not re.fullmatch("[0-9a-f]{64}",entry["source_sha256"]):
        return result | {"reason":"unverified_source_hash"}
    failure=ALLOWED_FAILURES.get(entry.get("failure_code"))
    if not failure:
        return result | {"reason":"unrecognized_failure_requires_owner"}
    if not entry.get("independent_failure_receipt",False):
        return result | {"reason":"independent_failure_evidence_missing"}
    if failure.get("requires_owner_design_review") and not entry.get("owner_design_change_approved",False):
        return result | {"reason":"owner_design_change_required"}
    if entry.get("owner_intake_signed") is not True:
        return result | {"reason":"owner_scoped_intake_required"}
    return result | {"status":"approved_recipe_candidate","reason":"propose_exact_governed_action",
                     "next_action":failure["repair_action"],"recipe":failure["recipe"],
                     "attempt":entry["attempts"]+1,
                     "dispatch_requires_owner_gated_controller":True,
                     "executable":False}
def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("record",type=Path)
    args=p.parse_args()
    if args.record.is_symlink() or not args.record.is_file() or args.record.stat().st_size>12000:
        raise SystemExit("invalid failure record")
    try:
        item=json.loads(args.record.read_text())
        print(json.dumps(decide(item),indent=2))
    except (OSError,ValueError,TypeError) as err:
        print(json.dumps({"status":"needs_review","reason":str(err),"auto_publish":False}))
        raise SystemExit(2)
if __name__=="__main__":main()
