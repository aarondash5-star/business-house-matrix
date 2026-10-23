#!/usr/bin/env python3
"""Gate E RC1 candidate queue. Local-only, owner-enrolled, at-most-once dispatch.

No live service hooks, no Git push/publish, no automatic retry after an
uncertain result. Unknown crash state blocks other jobs until reconciled.
"""
import argparse
import json
import os
from pathlib import Path
import sqlite3
import sys
import time

import gate_e_operator as operator
import gate_e_runtime as gate

HERE=Path(__file__).resolve().parent
BASE=Path.home()/"matrix-gate-e-stage-20261022"
DB=BASE/"rc1-queue.sqlite3"
STATES=("queued","running","orphaned_needs_review",
        "verified_local_review","cancelled_verified","needs_review")

def connect(db=DB):
    file=Path(db)
    file.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    if file.is_symlink():
        raise gate.GateError("queue_symlink_denied")
    con=sqlite3.connect(file,timeout=10,isolation_level=None)
    con.row_factory=sqlite3.Row
    con.execute("PRAGMA busy_timeout=10000")
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("""CREATE TABLE IF NOT EXISTS jobs (
        task TEXT PRIMARY KEY, idem TEXT UNIQUE NOT NULL,
        status TEXT NOT NULL, created_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL, receipt_status TEXT)""")
    if file.is_file():os.chmod(file,0o600)
    return con

def enqueue(con,task,idem):
    operator.approve_task(task)
    if not isinstance(idem,str) or not 8<=len(idem)<=96 or not all(
            x.isascii() and (x.isalnum() or x in "-_.:") for x in idem):
        raise gate.GateError("idempotency_key_invalid")
    if (operator.RUNS/task).exists():
        raise gate.GateError("previous_run_must_not_replay")
    now=int(time.time())
    con.execute("BEGIN IMMEDIATE")
    try:
        existing=con.execute("SELECT * FROM jobs WHERE idem=? OR task=?",
                             (idem,task)).fetchone()
        if existing:
            if existing["task"]!=task or existing["idem"]!=idem:
                raise gate.GateError("task_or_key_already_registered")
            con.execute("COMMIT")
            return {"task":task,"status":existing["status"],"deduplicated":True}
        con.execute("""INSERT INTO jobs(task,idem,status,created_at,updated_at)
                       VALUES (?,?,'queued',?,?)""",(task,idem,now,now))
        con.execute("COMMIT")
        return {"task":task,"status":"queued","deduplicated":False}
    except BaseException:
        con.execute("ROLLBACK")
        raise

def claim(con):
    con.execute("BEGIN IMMEDIATE")
    try:
        blocked=con.execute("""SELECT count(*) AS n FROM jobs
                               WHERE status IN ('running','orphaned_needs_review')""").fetchone()["n"]
        if blocked:
            con.execute("COMMIT")
            return None
        row=con.execute("SELECT task FROM jobs WHERE status='queued' ORDER BY created_at,task LIMIT 1").fetchone()
        if not row:
            con.execute("COMMIT")
            return None
        task=row["task"]
        con.execute("UPDATE jobs SET status='running',updated_at=? WHERE task=?",
                    (int(time.time()),task))
        con.execute("COMMIT")
        return task
    except BaseException:
        con.execute("ROLLBACK")
        raise

def set_status(con,task,status,receipt=None):
    if status not in STATES:
        raise gate.GateError("invalid_queue_state")
    con.execute("UPDATE jobs SET status=?,updated_at=?,receipt_status=? WHERE task=?",
                (status,int(time.time()),receipt,task))

def reconcile(con):
    """After a restart, never replay running jobs. Block until reviewed."""
    con.execute("BEGIN IMMEDIATE")
    try:
        rows=con.execute("SELECT task FROM jobs WHERE status='running'").fetchall()
        for row in rows:
            set_status(con,row["task"],"orphaned_needs_review")
        con.execute("COMMIT")
        return {"orphaned_for_review":[x["task"] for x in rows]}
    except BaseException:
        con.execute("ROLLBACK")
        raise

def dispatch_once(con):
    task=claim(con)
    if task is None:
        return {"status":"idle_or_blocked"}
    try:
        # Operator re-validates manifest and per-host capacity lock.
        # No model-supplied shell command or non-enrolled repository.
        outcome=gate.bounded([sys.executable,"-B",str(HERE/"gate_e_operator.py"),task,"run"],
                             cwd=HERE,timeout=390,max_output=32000)
        path=operator.RUNS/task/"receipt.json"
        if path.is_file() and path.stat().st_size<160000:
            receipt=json.loads(path.read_text(encoding="utf-8"))
            status=receipt.get("status")
            if receipt.get("task")==task and status in (
                    "verified_local_review","cancelled_verified"):
                if status=="verified_local_review" and outcome["code"]!=0:
                    status="needs_review"
            else:
                status="needs_review"
        else:
            status="needs_review"
    except BaseException:
        status="needs_review"
    set_status(con,task,status,status)
    return {"task":task,"status":status,"published":False,
            "pushed":False,"automatically_retried":False}

def status(con):
    return [dict(row) for row in con.execute(
        "SELECT task,idem,status,updated_at,receipt_status FROM jobs ORDER BY created_at,task")]

def main(argv=None):
    ap=argparse.ArgumentParser()
    subs=ap.add_subparsers(dest="action",required=True)
    sub=subs.add_parser("enqueue")
    sub.add_argument("task")
    sub.add_argument("--idem",required=True)
    subs.add_parser("once")
    subs.add_parser("reconcile")
    subs.add_parser("status")
    sub=subs.add_parser("cancel")
    sub.add_argument("task")
    args=ap.parse_args(argv)
    with connect() as con:
        if args.action=="enqueue":
            result=enqueue(con,args.task,args.idem)
        elif args.action=="once":
            result=dispatch_once(con)
        elif args.action=="reconcile":
            result=reconcile(con)
        elif args.action=="status":
            result={"jobs":status(con)}
        elif args.action=="cancel":
            if not con.execute("SELECT 1 FROM jobs WHERE task=?",(args.task,)).fetchone():
                raise gate.GateError("unregistered_task")
            result=operator.main(["gate_e_operator.py",args.task,"cancel"])
    print(json.dumps(result,sort_keys=True))
    return result

if __name__=="__main__":
    try:main()
    except Exception as exc:
        print(json.dumps({"status":"blocked","error_type":type(exc).__name__}))
        sys.exit(2)
