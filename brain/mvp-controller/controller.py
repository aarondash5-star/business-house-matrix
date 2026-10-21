#!/usr/bin/env python3
"""Independent Matrix MVP central dispatcher -- durable, least-privilege, local.

Only public research and proposal-only Dev execution are currently runnable.
Marketing/video/production routes are explicitly BLOCKED pending host/network/thermal readiness.
No model-selected shell commands, code execution, payments, publishing or paid APIs.
"""
import argparse
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
import uuid

HERE=Path(__file__).resolve().parent
HOME=Path(os.environ.get("BHM_AUTONOMY_HOME",HERE))
DB=HOME/"tasks.sqlite3"
DEVBRAIN=Path("/var/lib/generic-linux-automator-exec/.local/share/matrix-dev-brain")
DEV_DB=DEVBRAIN/"queue.sqlite3"
DELL_RESEARCH=Path("/var/lib/generic-linux-automator-exec/matrix-searxng/local_search.py")
ALLOWED={
 "research_search":{"department":"Concept","mode":"public_retrieval"},
 "dev_proposal":{"department":"Development","mode":"proposal_only"},
 "marketing_draft":{"department":"Marketing","mode":"blocked_until_private_route"},
 "video_preview":{"department":"Marketing","mode":"blocked_until_thermal_QA"},
}
TRANSIENT_ERRORS=("TimeoutError","HTTP 429","temporary unavailable")
BLOCKERS={
 "marketing_draft":"MKT_NETWORK: Mac and Dell are on different isolated Wi-Fi networks; no authenticated machine-to-machine relay",
 "video_preview":"VIDEO_THERMAL: Mac reel render is disabled pending safe thermal test, approved footage and independent QA",
}
MAX_BRIEF=2000
MAX_SEARCH=180

def now():return datetime.now(timezone.utc).isoformat(timespec="seconds")

def connect():
    HOME.mkdir(mode=0o700,parents=True,exist_ok=True)
    d=sqlite3.connect(DB,timeout=15)
    d.row_factory=sqlite3.Row
    d.execute("PRAGMA busy_timeout=15000")
    d.execute("PRAGMA journal_mode=WAL")
    d.execute("""CREATE TABLE IF NOT EXISTS tasks (
      id TEXT PRIMARY KEY, idempotency TEXT NOT NULL UNIQUE,
      project TEXT NOT NULL, action TEXT NOT NULL, department TEXT NOT NULL,
      brief TEXT NOT NULL, research_query TEXT NOT NULL DEFAULT '',
      status TEXT NOT NULL, remote_job TEXT, attempts INTEGER NOT NULL DEFAULT 0,
      created TEXT NOT NULL, updated TEXT NOT NULL, next_check INTEGER NOT NULL DEFAULT 0,
      output TEXT, error TEXT, qa_level TEXT NOT NULL DEFAULT 'unverified'
    )""")
    d.execute("""CREATE TABLE IF NOT EXISTS evolution (
        id INTEGER PRIMARY KEY, time TEXT NOT NULL, project TEXT NOT NULL,
        task TEXT NOT NULL, outcome TEXT NOT NULL, qa_level TEXT NOT NULL,
        note TEXT NOT NULL
    )""")
    d.commit();DB.chmod(0o600)
    return d

def validate_public(q):
    if not isinstance(q,str):raise ValueError("Public research must be text")
    if not q:return ""
    if not (2<=len(q.strip())<=MAX_SEARCH) or any(ord(c)<32 for c in q):
        raise ValueError("Public query must be 2-180 characters, no control characters")
    if re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",q) or re.search(r"\b(?:\+?\d[\s-]?){10,}\b",q):
        raise ValueError("Personal identifying contact data forbidden in public query")
    if re.search(r"\b(?:secret|password|api.?key|private.?key|bearer|guest.?data|customer.?list)\b",q,re.I):
        raise ValueError("Private information forbidden in research query")
    return q.strip()

def validate_project(value):
    if not isinstance(value,str) or not re.fullmatch(r"[a-z][a-z0-9_-]{1,31}",value):
        raise ValueError("Safe project id required")
    return value

def submit(project,action,brief,research_query="",idempotency=None):
    validate_project(project)
    if action not in ALLOWED:raise ValueError("Unknown allowlisted task action")
    if not isinstance(brief,str) or not 2<=len(brief.strip())<=MAX_BRIEF:
        raise ValueError("Brief must be 2-2000 characters")
    if action=="research_search" and not research_query:research_query=brief
    q=validate_public(research_query)
    idem=idempotency or str(uuid.uuid4())
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{7,95}",idem):
        raise ValueError("Idempotency value must be 8-96 safe characters")
    d=connect()
    found=d.execute("SELECT id,status FROM tasks WHERE idempotency=?",(idem,)).fetchone()
    if found:
        d.close();return {"id":found["id"],"status":found["status"],"deduplicated":True}
    ident=str(uuid.uuid4())
    status="blocked" if action in BLOCKERS else "queued"
    d.execute("""INSERT INTO tasks(id,idempotency,project,action,department,brief,
        research_query,status,created,updated,error)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
      (ident,idem,project,action,ALLOWED[action]["department"],brief.strip(),q,status,now(),now(),BLOCKERS.get(action)))
    d.commit();d.close()
    return {"id":ident,"status":status,"department":ALLOWED[action]["department"],"deduplicated":False}

def evolve(d,task,status,qa_level,note=""):
    d.execute("INSERT INTO evolution(time,project,task,outcome,qa_level,note) VALUES(?,?,?,?,?,?)",
              (now(),task["project"],task["action"],status,qa_level,note[:300]))

def receipt(d,job_id,state,output=None,error=None,qa="unverified",remote=None):
    d.execute("""UPDATE tasks SET status=?,updated=?,output=?,error=?,qa_level=?,
                 remote_job=COALESCE(?,remote_job) WHERE id=?""",
              (state,now(),json.dumps(output,ensure_ascii=False)[:30000] if output is not None else None,
               (error or "")[:300],qa,remote,job_id))
    if state in ("completed","needs_review","failed"):
        row=d.execute("SELECT * FROM tasks WHERE id=?",(job_id,)).fetchone()
        evolve(d,row,state,qa,error or "")
    d.commit()

def read_dev(job_id):
    if not re.fullmatch(r"[a-f0-9-]{36}",job_id):raise ValueError("Untrusted Dev job ID")
    if not DEV_DB.is_file():raise RuntimeError("Dev Brain database not present")
    d=sqlite3.connect(f"file:{DEV_DB}?mode=ro",uri=True,timeout=5)
    d.row_factory=sqlite3.Row
    row=d.execute("SELECT id,status,stage,error FROM jobs WHERE id=?",(job_id,)).fetchone()
    d.close()
    if not row:raise RuntimeError("Dev Job not found")
    return dict(row)

def poll_dev(d,t):
    remote=t["remote_job"]
    if not remote:
        # Dispatch wasn't acknowledged, never replay and risk duplicate work.
        d.execute("UPDATE tasks SET status='needs_review',error=?,updated=? WHERE id=?",
                  ("Dispatch receipt absent; audit target queue before any retry",now(),t["id"]))
        d.commit();return {"id":t["id"],"status":"needs_review"}
    j=read_dev(remote)
    if j["status"] in ("queued","running"):
        return {"id":t["id"],"status":"delegated","remote_stage":j["stage"]}
    if j["status"] in ("review_passed","needs_revision"):
        path=DEVBRAIN/"artifacts"/remote/"result.json"
        result=json.loads(path.read_text()) if path.is_file() else {}
        qa="proposal_review_only"
        verified=(result.get("tests_executed") is False and
                  result.get("repository_changed") is False and
                  result.get("source_lookup_available") is not None)
        state="completed" if j["status"]=="review_passed" and verified else "needs_review"
        payload={"source":"dell_dev_brain","remote_job":remote,"remote_status":j["status"],
                 "proposal_only":True,"tests_executed":False,
                 "repository_changed":False,
                 "source_lookup_available":result.get("source_lookup_available",False),
                 "artifacts":list((DEVBRAIN/"artifacts"/remote).glob("*.md")) and
                     sorted(p.name for p in (DEVBRAIN/"artifacts"/remote).glob("*")) or []}
        receipt(d,t["id"],state,payload,None if verified else "Incomplete Dev receipt",qa)
        return {"id":t["id"],"status":state,"qa_level":qa}
    receipt(d,t["id"],"needs_review",{"remote_status":j["status"]},
            "Remote Dev job did not reach approved outcome; no blind replay","unverified")
    return {"id":t["id"],"status":"needs_review"}

def tick():
    d=connect()
    pending=d.execute("SELECT * FROM tasks WHERE status='delegated' ORDER BY created LIMIT 1").fetchone()
    if pending:
        try:result=poll_dev(d,pending)
        except Exception as err:
            result={"id":pending["id"],"status":"uncertain","message":type(err).__name__}
        d.close();return result
    d.execute("BEGIN IMMEDIATE")
    t=d.execute("SELECT * FROM tasks WHERE status='queued' ORDER BY created LIMIT 1").fetchone()
    if not t:
        d.commit();d.close();return {"status":"idle"}
    d.execute("UPDATE tasks SET status='dispatching',attempts=attempts+1,updated=? WHERE id=?",
              (now(),t["id"]))
    d.commit()
    try:
        if t["action"]=="research_search":
            result=subprocess.run(
                [sys.executable,str(DELL_RESEARCH),t["research_query"],"--limit","5"],
                capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=40)
            if result.returncode:raise RuntimeError("Public research provider not available")
            data=json.loads(result.stdout)
            if data.get("provider")!="self-hosted-searxng":raise RuntimeError("Wrong research provider")
            receipt(d,t["id"],"completed",data,None,"retrieval_only")
            out={"id":t["id"],"status":"completed","results":len(data.get("results",[]))}
        elif t["action"]=="dev_proposal":
            sys.path.insert(0,str(DEVBRAIN))
            import brain
            remote=brain.enqueue(t["brief"],"fast",t["research_query"])
            d.execute("UPDATE tasks SET status='delegated',remote_job=?,updated=? WHERE id=?",
                      (remote,now(),t["id"]))
            d.commit()
            out={"id":t["id"],"status":"delegated","remote_job":remote}
        else:raise RuntimeError("Task route not enabled")
    except Exception as err:
        # Persistent/manual recovery to avoid duplicate delegation after crash.
        receipt(d,t["id"],"needs_review",None,type(err).__name__+": "+str(err)[:200],"unverified")
        out={"id":t["id"],"status":"needs_review","error":type(err).__name__}
    d.close();return out

def recover():
    d=connect()
    # There are no attempts to auto-replay external calls with ambiguous result.
    rows=d.execute("SELECT id FROM tasks WHERE status='dispatching'").fetchall()
    for t in rows:
        d.execute("UPDATE tasks SET status='needs_review',error=?,updated=? WHERE id=?",
                  ("Ambiguous dispatch state: audit target job before retry",now(),t["id"]))
    d.commit();d.close()
    return {"flagged_uncertain_dispatches":len(rows)}

def status(limit=12):
    d=connect()
    groups={r[0]:r[1] for r in d.execute("SELECT status,count(*) FROM tasks GROUP BY status")}
    all_=d.execute("SELECT id,project,action,department,status,qa_level,remote_job,error FROM tasks ORDER BY created DESC LIMIT ?",(limit,)).fetchall()
    feedback={r[0]:r[1] for r in d.execute("SELECT outcome,count(*) FROM evolution GROUP BY outcome")}
    d.close()
    return {"controller_version":"0.1.0","host":"dell-linux",
      "capabilities":{k:v["mode"] for k,v in ALLOWED.items()},
      "counts":groups,"evolution_outcomes":feedback,
      "tasks":[dict(r) for r in all_],"paid":False,"auto_publish":False,
      "allow_shell_injection":False,"sandbox_execution":False}

def show(job_id):
    d=connect()
    row=d.execute("SELECT * FROM tasks WHERE id=?",(job_id,)).fetchone()
    d.close()
    if not row:raise ValueError("Task not found")
    val=dict(row)
    if val.get("output"):
        try:val["output"]=json.loads(val["output"])
        except ValueError:pass
    return val

def attach_existing(project,remote_job):
    # Reconciles existing completed job; does not enqueue another expensive run.
    j=read_dev(remote_job)
    validate_project(project)
    idem="existing-"+remote_job
    d=connect()
    row=d.execute("SELECT id FROM tasks WHERE idempotency=?",(idem,)).fetchone()
    if row:
        ident=row["id"]
    else:
        ident=str(uuid.uuid4())
        d.execute("""INSERT INTO tasks
            (id,idempotency,project,action,department,brief,research_query,
            status,remote_job,created,updated)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
            (ident,idem,project,"dev_proposal","Development",
             "Retrospective verification of existing Dell Dev Brain proposal","",
             "delegated",remote_job,now(),now()))
        d.commit()
    row=d.execute("SELECT * FROM tasks WHERE id=?",(ident,)).fetchone()
    val=poll_dev(d,row)
    d.close();return val

def test():
    with tempfile.TemporaryDirectory(prefix="matrix-autonomy-test-") as name:
        global HOME,DB
        hold_home,hold_db=HOME,DB
        try:
            HOME=Path(name);DB=HOME/"test.sqlite3"
            a=submit("devpilot","research_search","Python TaskGroup official documentation",
                    "Python TaskGroup official documentation","smoke-research-20261021")
            b=submit("devpilot","research_search","Python TaskGroup official documentation",
                    "Python TaskGroup official documentation","smoke-research-20261021")
            c=submit("marketing","video_preview","Test a safe video draft")
            assert a["id"]==b["id"] and b["deduplicated"]
            assert c["status"]=="blocked"
            assert status()["counts"]=={"queued":1,"blocked":1}
            assert recover()["flagged_uncertain_dispatches"]==0
            try:submit("devpilot","research_search","contact", "email alice@example.com")
            except ValueError:pass
            else:raise AssertionError("Private text passed")
            return {"passed":True,"tests":["persistent queue","idempotency","blocked production route",
                                           "isolation","privacy validation","conservative recovery"]}
        finally:HOME,DB=hold_home,hold_db

def main():
    ap=argparse.ArgumentParser(description="Independent Matrix central orchestrator")
    sp=ap.add_subparsers(dest="command",required=True)
    add=sp.add_parser("submit")
    add.add_argument("project");add.add_argument("action",choices=sorted(ALLOWED))
    add.add_argument("brief")
    add.add_argument("--research-query",default="")
    add.add_argument("--key",default=None)
    sp.add_parser("tick");sp.add_parser("recover")
    sp.add_parser("status");sp.add_parser("selftest")
    attach=sp.add_parser("attach-existing")
    attach.add_argument("project");attach.add_argument("dev_job_id")
    showp=sp.add_parser("show");showp.add_argument("id")
    daemon=sp.add_parser("serve");daemon.add_argument("--interval",type=int,default=15)
    a=ap.parse_args()
    if a.command=="submit":v=submit(a.project,a.action,a.brief,a.research_query,a.key)
    elif a.command=="tick":v=tick()
    elif a.command=="recover":v=recover()
    elif a.command=="status":v=status()
    elif a.command=="show":v=show(a.id)
    elif a.command=="selftest":v=test()
    elif a.command=="attach-existing":v=attach_existing(a.project,a.dev_job_id)
    else:
        recover()
        while True:
            try:tick()
            except Exception as e:
                print("CONTROLLER_LOOP_ERROR",type(e).__name__,flush=True)
            time.sleep(max(10,min(120,a.interval)))
    print(json.dumps(v,indent=2,ensure_ascii=False,default=str))
if __name__=="__main__":
    main()
