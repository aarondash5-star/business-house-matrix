#!/usr/bin/env python3
"""Event-driven Business House Matrix task completion / stall / escalation inbox.

Run as the unprivileged Dell/Mac owner; never grants tool authorization.
Posts to a separately approved HTTPS endpoint only when the OWNER configures
a pinned host and signing key. Without that, durable events remain queued.
No automatic ChatGPT-conversation message injection is claimed.
"""
from __future__ import annotations
import argparse
import hashlib
import hmac
import ipaddress
import json
import os
from pathlib import Path
import re
import socket
import sqlite3
import sys
import time
import urllib.parse
import urllib.request

ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{1,119}$")
KINDS = {"completed", "failed", "blocked", "escalation", "stalled", "resumed", "approval_required"}
FINAL = {"completed", "failed", "blocked", "approval_required"}
BASE = Path.home() / ".local/state/business-house-matrix"
DEFAULT_DB = BASE / "task-events.sqlite3"
MAX_DETAIL = 550
MAX_URL = 700

class EventError(ValueError):
    pass

def valid_id(value: str):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise EventError("invalid_identifier")
    return value

def safe_text(value: str):
    if not isinstance(value, str) or len(value) > MAX_DETAIL or any(ord(c)<32 and c not in "\n\t" for c in value):
        raise EventError("invalid_detail")
    return value.strip()

def safe_link(value: str):
    if not value:
        return ""
    if not isinstance(value,str) or len(value)>MAX_URL:
        raise EventError("invalid_evidence_link")
    p=urllib.parse.urlsplit(value)
    if p.scheme!="https" or not p.hostname or p.username or p.password or p.fragment:
        raise EventError("evidence_link_must_be_https")
    return value

def connect(path: Path):
    if path.is_symlink():
        raise EventError("symlink_database_denied")
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    if path.exists() and not path.is_file():
        raise EventError("database_not_regular_file")
    con=sqlite3.connect(str(path),timeout=12)
    con.row_factory=sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA busy_timeout=10000")
    con.execute("""CREATE TABLE IF NOT EXISTS runs(
        run_id TEXT PRIMARY KEY, task_id TEXT NOT NULL, status TEXT NOT NULL,
        stage TEXT NOT NULL, last_update INTEGER NOT NULL,
        idle_seconds INTEGER NOT NULL,
        stall_count INTEGER NOT NULL DEFAULT 0)""")
    con.execute("""CREATE TABLE IF NOT EXISTS events(
        seq INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT NOT NULL UNIQUE,
        run_id TEXT NOT NULL, task_id TEXT NOT NULL, kind TEXT NOT NULL,
        severity TEXT NOT NULL, payload TEXT NOT NULL, 
        sent INTEGER NOT NULL DEFAULT 0, created_unix INTEGER NOT NULL)""")
    con.commit()
    os.chmod(path,0o600)
    return con

def event_id(run_id,kind,stage,detail):
    return hashlib.sha256((run_id+"\n"+kind+"\n"+stage+"\n"+detail).encode()).hexdigest()

def _write_event(db,run_id,task_id,kind,stage,detail="",url="",severity=None,now=None):
    if kind not in KINDS:
        raise EventError("unknown_event")
    if now is None:now=int(time.time())
    severity=severity or ("info" if kind in {"completed","resumed"} else "warning" if kind=="approval_required" else "critical")
    if severity not in ("info","warning","critical"):
        raise EventError("invalid_severity")
    detail=safe_text(detail)
    url=safe_link(url)
    identity=event_id(run_id,kind,stage,detail)
    payload={"schema":1,"event_id":identity,"task_id":task_id,"run_id":run_id,
        "kind":kind,"severity":severity,"stage":stage,"summary":detail,
        "evidence_url":url,"timestamp":now, "requires_owner_attention":kind in
        ("failed","blocked","escalation","stalled","approval_required")}
    db.execute("""INSERT OR IGNORE INTO events
       (event_id,run_id,task_id,kind,severity,payload,created_unix)
       VALUES(?,?,?,?,?,?,?)""",(identity,run_id,task_id,kind,severity,json.dumps(payload,sort_keys=True),now))
    return payload

def register(db,run_id,task_id,stage="assigned",idle_seconds=1800,now=None):
    valid_id(run_id);valid_id(task_id);safe_text(stage)
    if not 300<=idle_seconds<=86400:
        raise EventError("watchdog_threshold_out_of_bounds")
    now=int(time.time()) if now is None else now
    existing=db.execute("SELECT * FROM runs WHERE run_id=?",(run_id,)).fetchone()
    if existing:
        if existing["task_id"]!=task_id:raise EventError("run_id_conflict")
        return {"run_id":run_id,"state":"existing","stage":existing["stage"]}
    db.execute("INSERT INTO runs(run_id,task_id,status,stage,last_update,idle_seconds) VALUES(?,?,?,?,?,?)",
               (run_id,task_id,"running",stage,now,idle_seconds))
    return {"run_id":run_id,"state":"registered","stage":stage}

def heartbeat(db,run_id,stage,now=None):
    valid_id(run_id);safe_text(stage)
    now=int(time.time()) if now is None else now
    r=db.execute("SELECT * FROM runs WHERE run_id=?",(run_id,)).fetchone()
    if not r:raise EventError("unknown_run")
    if r["status"] in FINAL:
        raise EventError("terminal_run_cannot_resume")
    if r["status"]=="stalled":
        _write_event(db,run_id,r["task_id"],"resumed",stage,"Worker heartbeat resumed",now=now)
    db.execute("UPDATE runs SET status='running',stage=?,last_update=?,stall_count=0 WHERE run_id=?",
               (stage,now,run_id))
    return {"run_id":run_id,"stage":stage,"status":"running"}

def emit(db,run_id,kind,stage,detail,url="",now=None):
    valid_id(run_id);safe_text(stage)
    now=int(time.time()) if now is None else now
    if kind not in KINDS - {"stalled","resumed"}:raise EventError("use_watchdog_for_stall")
    r=db.execute("SELECT * FROM runs WHERE run_id=?",(run_id,)).fetchone()
    if not r:raise EventError("unknown_run")
    if r["status"] in FINAL:
        raise EventError("terminal_run_already_recorded")
    e=_write_event(db,run_id,r["task_id"],kind,stage,detail,url,now=now)
    next_state=kind if kind in FINAL else r["status"]
    db.execute("UPDATE runs SET status=?,stage=?,last_update=? WHERE run_id=?",
               (next_state,stage,now,run_id))
    return e

def watchdog(db,now=None):
    now=int(time.time()) if now is None else now
    events=[]
    for r in db.execute("SELECT * FROM runs WHERE status IN ('running','stalled')").fetchall():
        duration=now-r["last_update"]
        if duration>=r["idle_seconds"] and r["status"]=="running":
            e=_write_event(db,r["run_id"],r["task_id"],"stalled",r["stage"],
                 "No verified worker progress for "+str(duration)+" seconds",now=now)
            db.execute("UPDATE runs SET status='stalled',stall_count=1 WHERE run_id=?",(r["run_id"],))
            events.append(e)
        elif duration>=r["idle_seconds"]*2 and r["status"]=="stalled" and r["stall_count"]==1:
            e=_write_event(db,r["run_id"],r["task_id"],"escalation",r["stage"],
                 "Stalled for at least twice the configured threshold; investigate worker and receipts",
                 now=now)
            db.execute("UPDATE runs SET stall_count=2 WHERE run_id=?",(r["run_id"],))
            events.append(e)
    return events

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def approved_endpoint(environ):
    url=environ.get("MATRIX_TASK_NOTIFY_WEBHOOK","").strip()
    secret=environ.get("MATRIX_TASK_NOTIFY_SECRET","")
    hosts={h.strip().lower() for h in environ.get("MATRIX_TASK_NOTIFY_HOSTS","").split(",") if h.strip()}
    if not url:return None
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.port not in (None,443) or p.username or p.password or p.fragment:
        raise EventError("unsafe_webhook_url")
    if not p.hostname or p.hostname.lower() not in hosts or not secret or len(secret)<24:
        raise EventError("webhook_unapproved_or_unsigned")
    try:
        infos=socket.getaddrinfo(p.hostname,443,type=socket.SOCK_STREAM)
    except OSError as exc:
        raise EventError("webhook_dns_unavailable") from exc
    if not infos:raise EventError("webhook_dns_empty")
    for info in infos:
        ip=ipaddress.ip_address(info[4][0])
        if not ip.is_global:raise EventError("webhook_nonpublic_address")
    return (url,secret)

def dispatch(db,environ=os.environ,limit=10):
    config=approved_endpoint(environ)
    if config is None:
        return {"status":"queued_no_approved_delivery_endpoint","delivered":0,
                "pending":db.execute("SELECT COUNT(*) FROM events WHERE sent=0").fetchone()[0]}
    if not 1<=limit<=25:raise EventError("dispatch_limit")
    url,secret=config
    delivered=0
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    rows=db.execute("SELECT * FROM events WHERE sent=0 ORDER BY seq LIMIT ?",(limit,)).fetchall()
    for row in rows:
        content=row["payload"].encode("utf-8")
        signature=hmac.new(secret.encode(),content,hashlib.sha256).hexdigest()
        req=urllib.request.Request(url,data=content,method="POST",headers={
          "Content-Type":"application/json",
          "X-Matrix-Event-ID":row["event_id"],
          "X-Matrix-Signature":"sha256="+signature,
          "User-Agent":"BusinessHouseMatrix-EventRouter/1.0"})
        try:
            with opener.open(req,timeout=12) as response:
                if response.status not in (200,201,202,204):
                    break
        except (OSError,TimeoutError):
            break
        db.execute("UPDATE events SET sent=1 WHERE event_id=?",(row["event_id"],))
        db.commit()
        delivered+=1
    return {"status":"dispatched" if delivered else "delivery_failed_or_no_events",
            "delivered":delivered,"pending":db.execute("SELECT COUNT(*) FROM events WHERE sent=0").fetchone()[0]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--database",default=str(DEFAULT_DB))
    sub=p.add_subparsers(dest="cmd",required=True)
    def ident(name):
        q=sub.add_parser(name);q.add_argument("--run-id",required=True);return q
    q=ident("register");q.add_argument("--task-id",required=True);q.add_argument("--stage",default="assigned")
    q.add_argument("--idle-seconds",type=int,default=1800)
    q=ident("heartbeat");q.add_argument("--stage",required=True)
    for kind in ("completed","failed","blocked","approval_required","escalation"):
        q=ident(kind);q.add_argument("--stage",required=True);q.add_argument("--detail",required=True)
        q.add_argument("--evidence-url",default="")
    sub.add_parser("watchdog");sub.add_parser("dispatch");sub.add_parser("status")
    args=p.parse_args()
    with connect(Path(args.database).expanduser()) as db:
        if args.cmd=="register":
            ans=register(db,args.run_id,args.task_id,args.stage,args.idle_seconds)
        elif args.cmd=="heartbeat":ans=heartbeat(db,args.run_id,args.stage)
        elif args.cmd in KINDS-{"stalled","resumed"}:
            ans=emit(db,args.run_id,args.cmd,args.stage,args.detail,args.evidence_url)
        elif args.cmd=="watchdog":ans={"events":watchdog(db)}
        elif args.cmd=="dispatch":ans=dispatch(db)
        else:
            ans={"runs":[dict(r) for r in db.execute("SELECT * FROM runs ORDER BY last_update DESC LIMIT 30")],
                 "pending_events":[json.loads(r[0]) for r in db.execute(
                 "SELECT payload FROM events WHERE sent=0 ORDER BY seq DESC LIMIT 15")]}
        db.commit()
    print(json.dumps(ans,sort_keys=True))
if __name__=="__main__":
    try:main()
    except (EventError,sqlite3.Error,OSError) as ex:
        print(json.dumps({"status":"blocked","reason":str(ex)}))
        sys.exit(2)
