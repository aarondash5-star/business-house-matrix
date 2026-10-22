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
 "dev_docs_fetch":{"department":"Development","mode":"governed_external_mcp_read_only"},
 "dev_proposal":{"department":"Development","mode":"proposal_only"},
 "dev_scoped_build":{"department":"Development","mode":"synthetic_model_sandbox_review_only"},
 "dev_general_build":{"department":"Development","mode":"manifest_enrolled_sandbox_review_only"},
 "website_stage":{"department":"Development","mode":"private_static_staging_only"},
 "pine_chat_stage":{"department":"Development","mode":"private_synthetic_chat_staging_only"},
 "sandbox_qa":{"department":"QA/QC","mode":"isolated_test_execution"},
 "repair_known_issue":{"department":"EVOLUTION","mode":"bounded_verified_autorepair"},
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
    if action=="website_stage" and (project!="moksha_overhaul" or brief.strip()!="moksha_overhaul_v1"):
        raise ValueError("Website staging has no approved project/manifest scope")
    if action=="pine_chat_stage" and (project!="pine_mcp_chat" or brief.strip()!="pine_chat_v1"):
        raise ValueError("Pine chat staging has no approved project/manifest scope")
    if action=="dev_scoped_build" and (project!="pine_mcp_chat" or brief.strip()!="dev_matrix_synthetic_release_v1"):
        raise ValueError("Scoped coding project/manifest not enrolled")
    if action=="dev_general_build" and (project!="matrix_dev" or brief.strip()!="matrix-dev-dashboard-v2"):
        raise ValueError("General coding project/manifest not enrolled")
    if action=="dev_docs_fetch":
        verify=subprocess.run(
            [sys.executable,str(HOME/"mcp_tool_router.py"),"validate",brief],
            stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=15)
        if verify.returncode or json.loads(verify.stdout).get("valid") is not True:
            raise ValueError("Dev documentation URL rejected by MCP policy")
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
                  result.get("source_lookup_available") is not None and
                  result.get("mcp_docs_attached") is True)
        state="completed" if j["status"]=="review_passed" and verified else "needs_review"
        payload={"source":"dell_dev_brain","remote_job":remote,"remote_status":j["status"],
                 "proposal_only":True,"tests_executed":False,
                 "repository_changed":False,
                 "source_lookup_available":result.get("source_lookup_available",False),
                 "mcp_docs_attached":result.get("mcp_docs_attached",False),
                 "mcp_source_url":result.get("mcp_source_url"),
                 "artifacts":list((DEVBRAIN/"artifacts"/remote).glob("*.md")) and
                     sorted(p.name for p in (DEVBRAIN/"artifacts"/remote).glob("*")) or []}
        receipt(d,t["id"],state,payload,None if verified else "Incomplete Dev receipt",qa)
        return {"id":t["id"],"status":state,"qa_level":qa}
    receipt(d,t["id"],"needs_review",{"remote_status":j["status"]},
            "Remote Dev job did not reach approved outcome; no blind replay","unverified")
    return {"id":t["id"],"status":"needs_review"}

def poll_scoped_build(d,t):
    task="dev_matrix_synthetic_release_v1"
    unit="matrix-dev-autonomy-release-v1-20261022.service"
    receipt_path=HOME/"autonomous-code-state"/task/"receipt.json"
    if receipt_path.is_file():
        payload=json.loads(receipt_path.read_text())
        review=payload.get("review") or {}
        qa=payload.get("qa") or {}
        sandbox=payload.get("sandbox") or {}
        expected={"frontend/dev-autonomy-validated-v1.html","tests/test_dev_autonomy_validated_v1.py"}
        sha=review.get("commit")
        safe=(payload.get("task")==task and payload.get("project")=="pine_mcp_chat"
              and payload.get("status")=="verified_local_review"
              and payload.get("published") is False and review.get("published") is False
              and qa.get("passed") is True and qa.get("tests_executed") is True
              and set(review.get("files") or [])==expected
              and isinstance(payload.get("source_governor_sha256"),str)
              and re.fullmatch(r"[a-f0-9]{64}",payload.get("source_governor_sha256")) is not None
              and isinstance(payload.get("attempts"),list) and 1<=len(payload.get("attempts"))<=2
              and isinstance(sha,str) and re.fullmatch(r"[a-f0-9]{40}",sha)
              and all(sandbox.get(k) is True for k in
                ("home_hidden","private_hidden","foreign_project_hidden","net_blocked","workspace_writable")))
        repo=HOME/"autonomous-code-state"/"reviews"/task
        if safe:
            v=subprocess.run(["git","-C",str(repo),"rev-parse","HEAD"],
                             capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=8)
            safe=v.returncode==0 and v.stdout.strip()==sha
        state="completed" if safe else "needs_review"
        receipt(d,t["id"],state,{"model_generated":True,"sandbox_qa":qa,
            "local_commit":sha if safe else None,"published":False},
            None if safe else "Scoped coding receipt did not pass independent contract",
            "synthetic_model_sandbox_review_qa" if safe else "unverified")
        return {"id":t["id"],"status":state,"qa_level":"synthetic_model_sandbox_review_qa" if safe else "unverified"}
    active=subprocess.run(["systemctl","--user","is-active",unit],
                          capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=8)
    if active.stdout.strip()=="active":
        return {"id":t["id"],"status":"delegated","stage":"isolated_model_coding"}
    receipt(d,t["id"],"needs_review",None,
            "Scoped build service inactive without terminal artifact; do not replay","unverified")
    return {"id":t["id"],"status":"needs_review"}

def poll_general_build(d,t):
    task="matrix-dev-dashboard-v2"
    unit="matrix-general-dev-dispatch-v2-20261022.service"
    parent=HOME/"release-stage-general-dev-20261022"/"runs"/task
    receipt_path=parent/"receipt.json"
    if receipt_path.is_file():
        payload=json.loads(receipt_path.read_text())
        qa=payload.get("qa") or {}
        review=payload.get("review") or {}
        expected={"frontend/dev-release-dashboard.html"}
        sha=review.get("commit")
        safe=(payload.get("task")==task and payload.get("project")=="matrix_dev"
              and payload.get("base_sha")=="f4ad954ef19f9791a042d9f95d737c528c655334"
              and payload.get("status")=="verified_local_review"
              and payload.get("published") is False
              and payload.get("model_tools") is False and payload.get("paid") is False
              and qa.get("qa_passed") is True and qa.get("tests_executed") is True
              and set(review.get("files") or [])==expected
              and review.get("published") is False and review.get("pushed") is False
              and isinstance(sha,str) and re.fullmatch(r"[a-f0-9]{40}",sha) is not None)
        if safe:
            # Never follow a model-supplied review path. Use the enrolled exact path.
            repo=parent/"local-review"
            v=subprocess.run(["git","-C",str(repo),"rev-parse","HEAD"],
                             capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=8)
            safe=v.returncode==0 and v.stdout.strip()==sha
        state="completed" if safe else "needs_review"
        receipt(d,t["id"],state,{"local_commit":sha if safe else None,
                "independent_qa":qa if safe else None,"published":False},
                None if safe else "Unverified general Dev receipt",
                "manifest_enrolled_sandbox_qa" if safe else "unverified")
        return {"id":t["id"],"status":state}
    active=subprocess.run(["systemctl","--user","is-active",unit],
                    capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=8)
    if active.stdout.strip()=="active":
        return {"id":t["id"],"status":"delegated","stage":"offline_model_coding"}
    receipt(d,t["id"],"needs_review",None,
            "No terminal agent receipt; do not replay an uncertain task","unverified")
    return {"id":t["id"],"status":"needs_review"}


def tick():
    d=connect()
    pending=d.execute("SELECT * FROM tasks WHERE status='delegated' ORDER BY created LIMIT 1").fetchone()
    ready=d.execute("SELECT id FROM tasks WHERE status='queued' ORDER BY created LIMIT 1").fetchone()
    # Do not let an unrelated slow remote Dev proposal block a short local safe task.
    # Finish the bounded queued work, then resume polling delegated tasks.
    if pending and not ready:
        try:
            if pending["action"]=="dev_scoped_build":result=poll_scoped_build(d,pending)
            elif pending["action"]=="dev_general_build":result=poll_general_build(d,pending)
            else:result=poll_dev(d,pending)
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
        elif t["action"]=="dev_docs_fetch":
            proc=subprocess.run(
                [sys.executable,str(HOME/"mcp_tool_router.py"),"fetch",t["brief"]],
                stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=75)
            if proc.returncode:
                raise RuntimeError("Governed MCP document fetch failed; no automatic replay")
            data=json.loads(proc.stdout)
            if (data.get("provider")!="external-mcp" or
                    data.get("tool_slot")!="mcp-fetch-docs" or
                    data.get("writes_performed") is not False or not data.get("text")):
                raise RuntimeError("Governed MCP result contract failed")
            receipt(d,t["id"],"completed",data,None,"external_mcp_retrieval_only")
            out={"id":t["id"],"status":"completed",
                 "source":data.get("url"),"chars":data.get("content_chars"),
                 "quota_event_id":data.get("quota_event_id"),
                 "qa_level":"external_mcp_retrieval_only"}
        elif t["action"]=="sandbox_qa":
            batch=t["brief"]
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,47}",batch):
                raise ValueError("Sandbox batch must be a safe identifier")
            runner=HOME/"sandbox.py"
            result=subprocess.run([sys.executable,str(runner),"run",batch],
                                  stdin=subprocess.DEVNULL,capture_output=True,text=True,
                                  timeout=60)
            if result.returncode:
                raise RuntimeError("Sandbox runner rejected batch or execution failed")
            data=json.loads(result.stdout)
            state="completed" if data.get("qa_passed") is True and data.get("tests_executed") is True else "needs_review"
            receipt(d,t["id"],state,data,None if state=="completed" else "Isolated tests did not pass",
                    "executed_isolated_unit_tests")
            out={"id":t["id"],"status":state,"qa_level":"executed_isolated_unit_tests"}
            # Safe self-repair only for one exact, reproduced defect in isolated staging.
            if (state=="needs_review" and "has no attribute 'cancel'" in str(data.get("output_tail",""))
                  and "TaskGroup" in str(data.get("output_tail","")) and not batch.endswith("-fixed")):
                auto_key="auto-repair-"+batch
                follow=submit(t["project"],"repair_known_issue",batch,idempotency=auto_key)
                out["safe_repair_queued"]=follow["id"]
        elif t["action"]=="repair_known_issue":
            batch=t["brief"]
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,40}",batch):
                raise ValueError("Approved short failed batch ID required")
            result=subprocess.run(
                [sys.executable,str(HOME/"repair.py"),batch,"--attempt","1"],
                stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=65)
            if result.returncode:
                raise RuntimeError("No safe verified automated repair for this defect")
            data=json.loads(result.stdout)
            state="completed" if data.get("new_qc")=="tests_passed" else "needs_review"
            receipt(d,t["id"],state,data,None if state=="completed" else "Rule-based correction failed independent tests",
                    "executed_isolated_unit_tests")
            out={"id":t["id"],"status":state,"qa_level":"executed_isolated_unit_tests"}
        elif t["action"]=="website_stage":
            result=subprocess.run([sys.executable,str(HOME/"site_staging.py"),"build",t["project"],t["brief"]],
                capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=45)
            if result.returncode:
                raise RuntimeError("Private staging build rejected: "+(result.stderr or "")[-180:])
            data=json.loads(result.stdout)
            if (data.get("state")!="private_preview_ready" or data.get("publication") is not False
                or data.get("spend") is not False or data.get("qa_passed") is not True
                or data.get("nonindexed") is not True or data.get("external_services") is not False):
                raise RuntimeError("Private staging contract failed")
            receipt(d,t["id"],"completed",data,None,"private_static_preview_qa")
            out={"id":t["id"],"status":"completed","qa_level":"private_static_preview_qa",
                 "pages":data["pages"],"local_path":data["local_path"]}
        elif t["action"]=="pine_chat_stage":
            proc=subprocess.run([sys.executable,str(HOME/"pine_chat_stage.py"),"build",t["project"],t["brief"]],
                capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=30)
            if proc.returncode:raise RuntimeError("Pine synthetic stage rejected or unavailable")
            data=json.loads(proc.stdout)
            if (data.get("state")!="private_preview_ready" or data.get("project")!="pine_mcp_chat"
                or data.get("manifest")!="pine_chat_v1" or data.get("qa_passed") is not True
                or data.get("publication") is not False or data.get("nonindexed") is not True
                or data.get("external_services") is not False or data.get("mock_mcp") is not True
                or data.get("live_pine_access") is not False or data.get("model_autonomy") is not False):
                raise RuntimeError("Pine synthetic staging result contract failed")
            receipt(d,t["id"],"completed",data,None,"private_synthetic_chat_preview_qa")
            out={"id":t["id"],"status":"completed","qa_level":"private_synthetic_chat_preview_qa",
                 "sha256":data["sha256"],"path":data["local_path"]}
        elif t["action"]=="dev_general_build":
            unit="matrix-general-dev-dispatch-v2-20261022"
            script=HOME/"release-stage-general-dev-20261022"/"repo"/"brain"/"dev-operator"/"agent_loop.py"
            target=HOME/"release-stage-general-dev-20261022"/"runs"/"matrix-dev-dashboard-v2"
            if not script.is_file() or target.exists():
                raise RuntimeError("General Dev task source missing or already attempted")
            proc=subprocess.run(
                ["systemd-run","--user","--unit="+unit,
                 "--property=RuntimeMaxSec=420","--property=MemoryMax=1400M",
                 "/usr/bin/python3",str(script),"matrix-dev-dashboard-v2"],
                capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=15)
            if proc.returncode:
                raise RuntimeError("General Dev agent launch rejected; no retry")
            d.execute("UPDATE tasks SET status='delegated',remote_job=?,updated=? WHERE id=?",
                      (unit+".service",now(),t["id"]))
            d.commit()
            out={"id":t["id"],"status":"delegated","unit":unit+".service"}
        elif t["action"]=="dev_scoped_build":
            unit="matrix-dev-autonomy-release-v1-20261022"
            script=HOME/"dev_autonomy_task_v4.py"
            target=HOME/"autonomous-code-state"/"dev_matrix_synthetic_release_v1"
            if not script.is_file() or target.exists():
                raise RuntimeError("Enrolled code source missing or already attempted; no replay")
            proc=subprocess.run(
                ["systemd-run","--user","--unit="+unit,
                 "--property=RuntimeMaxSec=300","--property=MemoryMax=1400M",
                 "/usr/bin/python3",str(script),"dev_matrix_synthetic_release_v1"],
                capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=15)
            if proc.returncode:
                raise RuntimeError("Scoped code service launch rejected; no retry")
            d.execute("UPDATE tasks SET status='delegated',remote_job=?,updated=? WHERE id=?",
                      (unit+".service",now(),t["id"]))
            d.commit()
            out={"id":t["id"],"status":"delegated","unit":unit+".service"}
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
      "allow_shell_injection":False,"sandbox_execution":True}

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
            try:submit("unapproved","website_stage","moksha_overhaul_v1")
            except ValueError:pass
            else:raise AssertionError("Unapproved staging project accepted")
            try:submit("pine_private","pine_chat_stage","pine_chat_v1")
            except ValueError:pass
            else:raise AssertionError("Foreign Pine staging project accepted")
            try:submit("pine_mcp_chat","pine_chat_stage","invalid_manifest")
            except ValueError:pass
            else:raise AssertionError("Invalid Pine manifest accepted")
            pine=submit("pine_mcp_chat","pine_chat_stage","pine_chat_v1",idempotency="test-pine-chat-stage-20261022")
            pine_duplicate=submit("pine_mcp_chat","pine_chat_stage","pine_chat_v1",idempotency="test-pine-chat-stage-20261022")
            assert pine["status"]=="queued" and pine_duplicate["id"]==pine["id"]
            try:submit("private_foreign","dev_general_build","matrix-dev-dashboard-v2")
            except ValueError:pass
            else:raise AssertionError("Cross-project Dev Operator scope accepted")
            try:submit("matrix_dev","dev_general_build","unknown_manifest")
            except ValueError:pass
            else:raise AssertionError("Unknown General Dev manifest accepted")
            try:submit("pine_private","dev_scoped_build","dev_matrix_synthetic_release_v1")
            except ValueError:pass
            else:raise AssertionError("Cross-tenant code action accepted")
            try:submit("pine_mcp_chat","dev_scoped_build","arbitrary")
            except ValueError:pass
            else:raise AssertionError("Arbitrary coding manifest accepted")
            smoke=submit("pine_mcp_chat","dev_scoped_build","dev_matrix_synthetic_release_v1",idempotency="test-pine-dev-autonomy-20261022")
            assert smoke["status"]=="queued"
            staged=submit("moksha_overhaul","website_stage","moksha_overhaul_v1",idempotency="test-staging-route-20261022")
            duplicate=submit("moksha_overhaul","website_stage","moksha_overhaul_v1",idempotency="test-staging-route-20261022")
            assert staged["status"]=="queued" and duplicate["id"]==staged["id"]
            assert status()["counts"]=={"queued":4,"blocked":1}
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
