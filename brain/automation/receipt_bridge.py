#!/usr/bin/env python3
"""Read-only bridge: translate a trusted local job receipt into task_events.
Intended to run on systemd PathChanged, never launches or repairs jobs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import task_events as events

SOURCE_NAMES={"progress.json","receipt.json","result.json","task-status.json"}

def observe(db,source: Path,task_id: str,run_id: str,owner_url: str,
            idle_seconds=1800, success_kind="approval_required"):
    events.valid_id(task_id)
    events.valid_id(run_id)
    owner_url=events.safe_link(owner_url)
    if success_kind not in {"completed","approval_required"}:
        raise events.EventError("invalid_success_kind")
    source=source.expanduser().absolute()
    if source.is_symlink() or source.name not in SOURCE_NAMES or not source.is_file():
        raise events.EventError("unsupported_receipt_source")
    if not source.resolve().is_relative_to(Path.home().resolve()):
        raise events.EventError("source_outside_owner_home")
    if source.stat().st_size>100_000:
        raise events.EventError("source_size_limit")
    raw=source.read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    state=json.loads(raw)
    if not isinstance(state,dict):
        raise events.EventError("receipt_not_object")
    e_state=state.get("state") or state.get("status")
    if e_state not in {"running","queued","completed","complete","failed",
                       "blocked","incomplete","needs_revision","needs_review"}:
        raise events.EventError("unknown_receipt_state")
    stage=str(state.get("current_phase") or state.get("stage") or e_state)[:200]
    if not db.execute("SELECT 1 FROM runs WHERE run_id=?",(run_id,)).fetchone():
        events.register(db,run_id,task_id,stage=stage,idle_seconds=idle_seconds)
    db.execute("""CREATE TABLE IF NOT EXISTS receipt_digests
         (run_id TEXT PRIMARY KEY, digest TEXT NOT NULL)""")
    old=db.execute("SELECT digest FROM receipt_digests WHERE run_id=?",(run_id,)).fetchone()
    if old and old["digest"]==digest:
        return {"status":"unchanged","run_id":run_id,"source_state":e_state}
    db.execute("INSERT OR REPLACE INTO receipt_digests(run_id,digest) VALUES(?,?)",(run_id,digest))
    current=db.execute("SELECT status FROM runs WHERE run_id=?",(run_id,)).fetchone()["status"]
    if current in events.FINAL:
        return {"status":"previous_terminal","run_id":run_id}
    if e_state in ("running","queued"):
        response=events.heartbeat(db,run_id,stage)
        return {"status":"progress_observed",**response}
    if e_state in ("completed","complete"):
        phases=state.get("phases")
        # Do not report a success for a superficially completed multi-pass plan
        # when its phase receipts are missing or invalid.
        if phases is not None and (not isinstance(phases,list) or
             len(phases)!=state.get("phase_total") or
             not all(isinstance(p,dict) and p.get("status")=="completed" for p in phases)):
            kind="blocked"
            summary="Terminal receipt reports completed, but phase QA receipts are incomplete"
        else:
            kind=success_kind
            summary="Task receipt completed; evidence and independent quality review required"
    else:
        kind="failed" if e_state=="failed" else "blocked"
        summary="Task entered "+str(e_state)+" at "+stage+"; inspect linked log and unblock"
    response=events.emit(db,run_id,kind,stage,summary,owner_url)
    return {"status":"event_created","event":response}

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--source",required=True)
    a.add_argument("--task-id",required=True)
    a.add_argument("--run-id",required=True)
    a.add_argument("--evidence-url",required=True)
    a.add_argument("--idle-seconds",type=int,default=1800)
    a.add_argument("--success-kind",choices=["approval_required","completed"],default="approval_required")
    a.add_argument("--database",default=str(events.DEFAULT_DB))
    x=a.parse_args()
    with events.connect(Path(x.database).expanduser()) as db:
        data=observe(db,Path(x.source),x.task_id,x.run_id,x.evidence_url,
                     x.idle_seconds,x.success_kind)
        db.commit()
    print(json.dumps(data,sort_keys=True))
if __name__=="__main__":
    try:main()
    except (OSError,sqlite3.Error,ValueError) as ex:
        print(json.dumps({"status":"blocked","reason":str(ex)}))
        sys.exit(2)
