#!/usr/bin/env python3
"""Narrow, audited autonomous correction for proven TaskGroup.cancel() bug.

No model self-approval: every candidate re-runs independent unit tests in the
networkless sandbox. Unknown failures remain NEEDS_REVIEW; no guesswork.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import sys
import uuid
import sandbox

ROOT=Path(__file__).resolve().parent

def repair(batch,attempt=1):
    if attempt not in (1,2):raise ValueError("No more than two bounded correction attempts")
    src,meta=sandbox.check(batch)
    old=sandbox.RECEIPTS/(batch+".json")
    if not old.is_file():raise RuntimeError("Original isolated QA receipt missing")
    fail=json.loads(old.read_text())
    text=str(fail.get("output_tail",""))
    if (fail.get("status")!="tests_failed" or
            "TaskGroup" not in text or
            "has no attribute 'cancel'" not in text):
        raise RuntimeError("Not an approved, reproduced TaskGroup.cancel defect")
    file=src/"candidate.py"
    if not file.is_file():raise RuntimeError("Only candidate.py supported")
    candidate=file.read_text()
    if candidate.count("await tg.cancel()")!=1 or candidate.count("tg.create_task(work())")!=1:
        raise RuntimeError("Automated correction not safely applicable to this source")
    # Exact known source form; unknown variable names / structures must escalate.
    m=re.search(r"(?m)^([ \t]+)for _ in range\(3\):$",candidate)
    n=re.search(r"(?m)^([ \t]+)await tg\.cancel\(\)[^\n]*$",candidate)
    if not m or not n or len(n.group(1))!=len(m.group(1)):
        raise RuntimeError("Expected task structure not present; human or AI review required")
    indent=m.group(1)
    corrected=candidate.replace(m.group(0),
         indent+"tasks = []\n"+m.group(0),1)
    corrected=corrected.replace("tg.create_task(work())","tasks.append(tg.create_task(work()))",1)
    corrected=re.sub(r"(?m)^([ \t]+)await tg\.cancel\(\)[^\n]*$",
                     indent+"for task in tasks: task.cancel()",corrected,count=1)
    if corrected==candidate or "tg.cancel()" in corrected:
        raise RuntimeError("Correction did not safely apply")
    base=batch+"-fixed"+("" if attempt==1 else str(attempt))
    batchname=base[:47]
    sandbox.check(batch)
    target=sandbox.INBOX/batchname
    if target.exists():
        raise RuntimeError("Previously staged repair; no overwrite")
    target.mkdir(mode=0o755,parents=True)
    target.chmod(0o755)  # Explicit: umask 0077 would hide mounted test files from nobody in container.
    (target/"candidate.py").write_text(corrected)
    shutil.copy2(src/"test_candidate.py",target/"test_candidate.py")
    for p in target.iterdir():p.chmod(0o644)
    qa=sandbox.run(batchname)
    event={"original_batch":batch,"fixed_batch":batchname,
           "repair_rule":"python_asyncio_TaskGroup_has_no_cancel",
           "original_qc":"tests_failed","new_qc":qa["status"],
           "tests_reexecuted":True,"source_changed_in_isolated_staging":True,
           "repository_modified":False,"production_modified":False,
           "automatic_publishing":False,"requires_human_review":not bool(qa["qa_passed"]),
           "new_source_sha256":qa.get("source_sha256")}
    evidence=ROOT/"repair-receipts"
    evidence.mkdir(mode=0o700,parents=True,exist_ok=True)
    p=evidence/(batch+"-attempt-"+str(attempt)+".json")
    if p.exists():raise RuntimeError("Repair audit entry already exists")
    p.write_text(json.dumps(event,indent=2));p.chmod(0o600)
    return event

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("batch")
    a.add_argument("--attempt",type=int,default=1)
    x=a.parse_args()
    try:print(json.dumps(repair(x.batch,x.attempt),indent=2))
    except (RuntimeError,ValueError,OSError) as e:
        print("REPAIR_REQUIRES_REVIEW",type(e).__name__,str(e)[:160],file=sys.stderr)
        sys.exit(2)
