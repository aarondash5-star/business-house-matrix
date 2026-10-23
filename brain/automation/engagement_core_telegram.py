#!/usr/bin/env python3
"""Send event receipts only to enrolled verified Primary group through Engagement Core REST.

Reuses existing GREC WordPress bot; sends ONLY to the owner-approved Primary group.
Requires exact Primary destination and a preexisting
scoped GREC key in an owner-private 0600 local file. No automatic retry of uncertain sends.
"""
import argparse
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import urllib.error
import urllib.request

from task_events import connect, EventError, DEFAULT_DB, NoRedirect

STATUS_URL="https://mokshagoa.com/wp-json/engagement-core/v1/telegram/status"
PUBLISH_URL="https://mokshagoa.com/wp-json/engagement-core/v1/telegram/publish"
TARGET="primary"
EXPECTED_GROUP_ID="-1001827799147"
class DeliveryError(EventError):pass

def load_config(environ=os.environ):
    path=environ.get("MATRIX_GREC_KEY_FILE","")
    chat=environ.get("MATRIX_OWNER_TG_GROUP_ID","")
    if not path or chat!=EXPECTED_GROUP_ID:
        raise DeliveryError("OWNER_PRIMARY_GROUP_NOT_APPROVED")
    p=Path(path).expanduser()
    if not p.is_absolute() or p.is_symlink() or not p.is_file():
        raise DeliveryError("APPROVED_SCOPED_KEY_FILE_MISSING")
    if p.stat().st_mode & 0o077 or p.stat().st_uid!=os.getuid():
        raise DeliveryError("SCOPED_KEY_FILE_PERMISSIONS_UNSAFE")
    key=p.read_text().strip()
    if len(key)<24 or "\n" in key:
        raise DeliveryError("SCOPED_KEY_MISSING")
    return {"chat_id":chat,"key":key}

def allow_target(status,chat_id):
    if not isinstance(status,dict) or status.get("connected") is not True:
        raise DeliveryError("ENGAGEMENT_CORE_NOT_CONNECTED")
    options=status.get("destinations")
    if not isinstance(options,list):
        raise DeliveryError("DESTINATION_PREFLIGHT_FAILED")
    matches=[d for d in options if isinstance(d,dict) and d.get("key")==TARGET
            and d.get("enabled") is True and d.get("level")=="primary" and str(d.get("chat_id"))==EXPECTED_GROUP_ID==chat_id]
    if len(matches)!=1:
        raise DeliveryError("PRIMARY_GROUP_TARGET_NOT_VERIFIED")
    return True

def _http(request,opener=None):
    opener=opener or urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    with opener.open(request,timeout=12) as response:
        body=response.read(40000)
        if response.status!=200:
            raise DeliveryError("ENGAGEMENT_CORE_UNEXPECTED_STATUS")
    try:return json.loads(body)
    except ValueError as exc:raise DeliveryError("ENGAGEMENT_CORE_INVALID_JSON") from exc

def preflight(config,opener=None):
    request=urllib.request.Request(STATUS_URL,method="GET",headers={
        "X-GREC-Publish-Key":config["key"],"Accept":"application/json"})
    status=_http(request,opener=opener)
    allow_target(status,config["chat_id"])
    return status

def render(payload):
    if not isinstance(payload,dict) or payload.get("kind") not in {
        "completed","failed","blocked","escalation","stalled","approval_required","resumed"}:
        raise DeliveryError("INVALID_EVENT_KIND")
    summary=str(payload.get("summary",""))[:350]
    if re.search(r"(?i)(api[_ -]?key|bearer|password|secret)\s*[:=]",summary):
        raise DeliveryError("SENSITIVE_SUMMARY_BLOCKED")
    def esc(s):
        return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    text=("Business House Matrix - "+str(payload["kind"]).upper()+
      "\nTask: "+esc(str(payload.get("task_id",""))[:80])+
      "\nStage: "+esc(str(payload.get("stage",""))[:120])+
      "\n"+esc(summary))
    link=str(payload.get("evidence_url",""))
    if link:
        if not link.startswith("https://") or len(link)>700:
            raise DeliveryError("INVALID_EVIDENCE_LINK")
        text+="\nEvidence: "+esc(link)
    if payload.get("requires_owner_attention") is True:
        text+="\nAction: review evidence and unblock."
    if len(text)>1200:
        raise DeliveryError("NOTIFICATION_TOO_LONG")
    return text

def accepted_delivery(response,chat_id):
    if not isinstance(response,dict) or response.get("ok") is not True or response.get("failed"):
        return False
    sent=response.get("sent")
    if not isinstance(sent,list) or len(sent)!=1 or not isinstance(sent[0],dict):
        return False
    r=sent[0]
    ids=r.get("message_ids")
    return (r.get("key")==TARGET and str(r.get("chat_id"))==chat_id and
      isinstance(ids,list) and any(isinstance(n,int) and n>0 for n in ids))

def send_once(db,config,opener=None):
    preflight(config,opener=opener)
    db.execute("BEGIN IMMEDIATE")
    row=db.execute("SELECT seq,event_id,payload FROM events WHERE sent=0 ORDER BY seq LIMIT 1").fetchone()
    if row is None:
        db.commit()
        return {"status":"no_pending_events"}
    data=json.loads(row["payload"])
    message=render(data)
    # Reserve before network write to prevent accidental retries after a timeout.
    db.execute("UPDATE events SET sent=2 WHERE seq=? AND sent=0",(row["seq"],))
    db.commit()
    request=urllib.request.Request(PUBLISH_URL,method="POST",data=json.dumps({
        "text":message,"targets":[TARGET]}).encode(),headers={
        "Content-Type":"application/json","X-GREC-Publish-Key":config["key"],
        "X-Matrix-Event-ID":row["event_id"],"Accept":"application/json"})
    try:
        result=_http(request,opener=opener)
        if not accepted_delivery(result,config["chat_id"]):
            return {"status":"delivery_uncertain_manual_reconcile","event_id":row["event_id"]}
    except (OSError,ValueError):
        return {"status":"delivery_uncertain_manual_reconcile","event_id":row["event_id"]}
    db.execute("UPDATE events SET sent=1 WHERE seq=? AND sent=2",(row["seq"],))
    db.commit()
    return {"status":"delivered_confirmed","event_id":row["event_id"],
        "telegram_message_id":result["sent"][0]["message_ids"][0],
        "destination_key":TARGET}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--database",default=str(DEFAULT_DB))
    p.add_argument("action",choices=["preflight","dispatch","status"])
    args=p.parse_args()
    with connect(Path(args.database).expanduser()) as db:
        if args.action=="status":
            output={"queued":db.execute("SELECT count(*) FROM events WHERE sent=0").fetchone()[0],
                "delivered":db.execute("SELECT count(*) FROM events WHERE sent=1").fetchone()[0],
                "uncertain":db.execute("SELECT count(*) FROM events WHERE sent=2").fetchone()[0]}
        else:
            config=load_config()
            if args.action=="preflight":
                preflight(config)
                output={"status":"primary_group_verified","destination_key":TARGET}
            else:output=send_once(db,config)
    print(json.dumps(output,sort_keys=True))
if __name__=="__main__":
    try:main()
    except (OSError,sqlite3.Error,ValueError) as exc:
        print(json.dumps({"status":"blocked","reason":str(exc) if str(exc) in (
           "OWNER_PRIVATE_DESTINATION_NOT_ENROLLED","APPROVED_SCOPED_KEY_FILE_MISSING",
           "SCOPED_KEY_FILE_PERMISSIONS_UNSAFE","SCOPED_KEY_MISSING",
           "PRIMARY_GROUP_TARGET_NOT_VERIFIED","ENGAGEMENT_CORE_NOT_CONNECTED")
           else type(exc).__name__}))
        sys.exit(2)
