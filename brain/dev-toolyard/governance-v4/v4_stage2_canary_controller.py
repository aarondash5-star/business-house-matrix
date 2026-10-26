#!/usr/bin/env python3
"""V4 Stage 2: one-shot, nonproduction synthetic probe controller.

Ingress: owner-authenticated Generic SSH development lane ONLY.
No listener, worker delegation, package installation, model, key or publish route.
Never import this module into the protected live Matrix controller.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import time

import adapter_guard_v4 as guard
import yard_auto_adapter_v1 as adapter

PROJECT = "matrix_dev_manager"
MANIFEST = "v4_stage2_single_probe"
ACTION = "probe_version"
TOOL = "python3"
TASK_ID = "v4-stage2-canary-20261026"
SNAPSHOT_BYTES = 80005
SNAPSHOT_SHA256 = "76cd6bcdf3c947012a1b83e551cef4e4ed206aa0ba6975fd876715631e325dc8"
EXPECTED_GUARD_SHA = "90f0a62cc6cfaf1458f0684363ffb9288c900ba0ade707908da0877447249e30"
EXPECTED_ADAPTER_SHA = "116f435279bbe7e0cc8281ab513e319926b846ab6ae25752bccc3fc6746fb773"
SOURCE = Path("/app")
STATE = Path("/state")
SNAPSHOT = SOURCE / "registry-snapshot.json"

class AdmissionDenied(ValueError):
    pass

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def admission(project=PROJECT, manifest=MANIFEST, action=ACTION, tool=TOOL,
              production=False, spend=False):
    if (project, manifest, action, tool, production, spend) != (
        PROJECT, MANIFEST, ACTION, TOOL, False, False):
        raise AdmissionDenied("fixed_scope_denied")
    return {"project":PROJECT,"manifest":MANIFEST,"action":ACTION,
            "tool":TOOL,"production":False,"spend":False}

def secure_setup():
    if os.geteuid() == 0:
        raise AdmissionDenied("container_root_denied")
    if any((SOURCE / p).is_symlink() for p in
           ("adapter_guard_v4.py","yard_auto_adapter_v1.py","registry-snapshot.json")):
        raise AdmissionDenied("source_symlink_denied")
    if sha(SOURCE/"adapter_guard_v4.py") != EXPECTED_GUARD_SHA:
        raise AdmissionDenied("guard_source_changed")
    if sha(SOURCE/"yard_auto_adapter_v1.py") != EXPECTED_ADAPTER_SHA:
        raise AdmissionDenied("adapter_source_changed")
    if sha(SNAPSHOT) != SNAPSHOT_SHA256 or SNAPSHOT.stat().st_size != SNAPSHOT_BYTES:
        raise AdmissionDenied("original_registry_snapshot_changed")
    snap = guard.summary(SNAPSHOT)
    if (snap["count"],snap["size"],snap["production_live"],
        snap["automatic_release"],snap["qa_probe_only"]) != (91,80005,False,False,True):
        raise AdmissionDenied("v4_registry_scope_denied")
    if not STATE.is_dir() or STATE.is_symlink():
        raise AdmissionDenied("dedicated_state_missing")
    # No other imported controller state paths or host gateway journal.
    admission()
    return snap

def store():
    p=STATE/"stage2-canary.sqlite3"
    if p.is_symlink() or (p.exists() and not p.is_file()):
        raise AdmissionDenied("unsafe_state")
    db=sqlite3.connect(str(p),timeout=5,isolation_level=None)
    db.row_factory=sqlite3.Row
    db.execute("PRAGMA busy_timeout=5000")
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("""CREATE TABLE IF NOT EXISTS jobs(
       task_id TEXT PRIMARY KEY, project TEXT NOT NULL, manifest TEXT NOT NULL,
       action TEXT NOT NULL, status TEXT NOT NULL, attempts INTEGER NOT NULL,
       receipt_json TEXT, updated_utc INTEGER NOT NULL)""")
    p.chmod(0o600)
    return db

def register_once(db):
    db.execute("BEGIN IMMEDIATE")
    try:
        prior=db.execute("SELECT * FROM jobs WHERE task_id=?",(TASK_ID,)).fetchone()
        if prior:
            row=dict(prior)
            if any(row[k] != v for k,v in
                   (("project",PROJECT),("manifest",MANIFEST),("action",ACTION))):
                raise AdmissionDenied("existing_task_conflict")
            if row["status"]=="completed":
                receipt=json.loads(row["receipt_json"])
                if receipt["status"]!="completed" or receipt["task_id"]!=TASK_ID:
                    raise AdmissionDenied("receipt_corrupt")
                db.execute("COMMIT")
                return ("deduplicated",receipt)
            raise AdmissionDenied("uncertain_or_pending_do_not_replay")
        db.execute("INSERT INTO jobs VALUES(?,?,?,?,?,?,?,?)",
                   (TASK_ID,PROJECT,MANIFEST,ACTION,"reserved",1,None,int(time.time())))
        db.execute("COMMIT")
        return ("reserved",None)
    except BaseException:
        db.execute("ROLLBACK")
        raise

def isolate_probe():
    # Registry derived solely from the actual restricted container executable.
    import shutil
    name=shutil.which("python3")
    if name is None:
        raise AdmissionDenied("python_probe_unavailable")
    p=Path(name).resolve(strict=True)
    if not str(p).startswith("/usr/local/bin/"):
        raise AdmissionDenied("unapproved_container_binary")
    registry={
      "schema":1,"rule":"v4-stage2-single-tool",
      "automatic_live":False,"direct_ssh_intercepted":False,
      "tools":{TOOL:{"binary":str(p),"sha256":adapter.sha(p),
        "state":"accepted_qa_probe_only","operations":["probe_version"],
        "production_live":False,"unbounded_execution_permitted":False}}}
    registry_file=STATE/"v4-stage2-probe-registry.json"
    if registry_file.exists():
        raise AdmissionDenied("registry_reuse_denied")
    adapter.save(registry,registry_file)  # only private /state is writable
    tool=adapter.preflight(TOOL,ACTION,registry_file)
    if tool["production_live"] or tool["unbounded_execution_permitted"]:
        raise AdmissionDenied("unexpected_exec_grant")
    allowed, reason=adapter.probe(TOOL,tool)  # actually runs fixed python3 --version
    if not allowed or reason!="version_probe_pass":
        raise AdmissionDenied("real_probe_failed:"+str(reason))
    return {
      "task_id":TASK_ID,"project":PROJECT,"manifest":MANIFEST,
      "status":"completed","actual_operation":"python3 --version",
      "controller":"separate_v4_rootless_one_shot",
      "tool_source_sha256":tool["sha256"],"snapshot_sha256":SNAPSHOT_SHA256,
      "independent_registry_total":91,"qa_only":True,
      "production":False,"spend":False,"network":False,
      "attempts":1,"receipt_kind":"actual_fixed_probe_no_model_no_worker"
    }

def run():
    secure_setup()
    db=store()
    try:
        result,old=register_once(db)
        if result=="deduplicated":
            print(json.dumps({"reused":True,"receipt":old},sort_keys=True))
            return
        try:
            receipt=isolate_probe()
        except Exception:
            # Never replay uncertain actions after the reservation.
            db.execute("UPDATE jobs SET status='blocked',updated_utc=? WHERE task_id=?",
                       (int(time.time()),TASK_ID))
            raise
        db.execute("BEGIN IMMEDIATE")
        try:
            count=db.execute("UPDATE jobs SET status='completed',receipt_json=?,updated_utc=? "
                             "WHERE task_id=? AND status='reserved' AND attempts=1",
                             (json.dumps(receipt,sort_keys=True),int(time.time()),TASK_ID)).rowcount
            if count!=1:raise AdmissionDenied("state_changed_during_probe")
            db.execute("COMMIT")
        except BaseException:
            db.execute("ROLLBACK")
            raise
        print(json.dumps({"reused":False,"receipt":receipt},sort_keys=True))
    finally:
        db.close()

if __name__ == "__main__":
    try:
        if len(sys.argv)!=2 or sys.argv[1]!="execute-exactly-once":
            raise AdmissionDenied("fixed_action_required")
        run()
    except (AdmissionDenied, OSError, sqlite3.Error) as e:
        print(json.dumps({"status":"blocked","error":type(e).__name__,
                          "reason":str(e)[:120],"production":False}),file=sys.stderr)
        sys.exit(2)
