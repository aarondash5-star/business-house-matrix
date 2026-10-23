#!/usr/bin/env python3
"""Signed Dell event outbox sender -> Moksha's VERIFIED private booking Telegram DM.

Requires deliberate owner activation of matching WordPress fixed-function relay,
and BHM_PRIVATE_TELEGRAM_ENABLE=1 for outbound delivery. Never uses Engagement
Core community publisher or the wrong Primary group.
The Ed25519 private key stays on the emitting worker and never enters WordPress.
"""
from __future__ import annotations
import argparse
import base64
import json
import os
from pathlib import Path
import sqlite3
import sys
import time
import urllib.request
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from task_events import DEFAULT_DB, EventError, NoRedirect, connect

ENDPOINT="https://mokshagoa.com/wp-json/bhm-private-events/v1/notify"
KEY_PATH=Path.home()/".local/state/business-house-matrix/private_telegram_ed25519.pem"
PROJECT_KEY_ID="dell-bhm-20261023"
TYPES=frozenset(("completed","failed","blocked","stalled","resumed","approval_required","escalation"))

def private_key(path=KEY_PATH):
    path=Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_uid!=os.getuid() or path.stat().st_mode&0o077:
        raise EventError("private_notification_key_missing_or_unprotected")
    k=serialization.load_pem_private_key(path.read_bytes(),password=None)
    if not isinstance(k,Ed25519PrivateKey):
        raise EventError("wrong_notification_key_type")
    return k

def validated_body(payload):
    if payload.get("schema")!=1 or payload.get("kind") not in TYPES:
        raise EventError("unsupported_notification_schema")
    event_id=payload.get("event_id")
    if not isinstance(event_id,str) or len(event_id)!=64 or any(c not in "0123456789abcdef" for c in event_id):
        raise EventError("invalid_event_id")
    if not isinstance(payload.get("summary"),str) or not 4<=len(payload["summary"])<=420:
        raise EventError("notification_summary_invalid")
    return json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf8")

def sign_request(body, event_id, timestamp, key):
    canonical=("bhm-private-relay-v1\n"+str(timestamp)+"\n"+event_id+"\n").encode()+body
    sig=base64.b64encode(key.sign(canonical)).decode()
    return {
        "Content-Type":"application/json",
        "Accept":"application/json",
        "X-Matrix-Timestamp":str(timestamp),
        "X-Matrix-Event-ID":event_id,
        "X-Matrix-Signature":sig,
        "X-Matrix-Key-Id":PROJECT_KEY_ID,
        "User-Agent":"BHM-Private-Notify/1.0",
    }

def pending(db):
    return db.execute("SELECT seq,event_id,payload FROM events WHERE sent=0 ORDER BY seq LIMIT 1").fetchone()

def dispatch_once(db, key, *, enabled=False, opener=None, now=None):
    row=pending(db)
    if row is None:return {"status":"no_pending_events"}
    data=json.loads(row["payload"])
    body=validated_body(data)
    if not enabled:
        return {"status":"disabled_until_wordpress_relay_active","queued_event_id":row["event_id"],
                "outbound_network_requests":0}
    stamp=int(time.time()) if now is None else int(now)
    if stamp<=0:raise EventError("bad_clock")
    headers=sign_request(body,row["event_id"],stamp,key)
    # SQLite reservation before sending prevents duplicate dispatch after a timeout.
    db.execute("BEGIN IMMEDIATE")
    changed=db.execute("UPDATE events SET sent=2 WHERE seq=? AND sent=0",(row["seq"],)).rowcount
    if changed!=1:
        db.rollback()
        return {"status":"another_dispatcher_claimed"}
    db.commit()
    request=urllib.request.Request(ENDPOINT,method="POST",data=body,headers=headers)
    client=opener or urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
    try:
        with client.open(request,timeout=20) as response:
            if response.status!=200:
                return {"status":"delivery_uncertain_no_retry","event_id":row["event_id"]}
            receipt=json.loads(response.read(10000))
    except (OSError,ValueError,TimeoutError):
        return {"status":"delivery_uncertain_no_retry","event_id":row["event_id"]}
    if (not isinstance(receipt,dict) or receipt.get("ok") is not True or
            receipt.get("status")!="delivered" or
            receipt.get("recipient")!="verified_private_booking_chat" or
            receipt.get("event_id")!=row["event_id"] or
            not isinstance(receipt.get("message_id"),int) or receipt["message_id"]<=0):
        return {"status":"delivery_uncertain_no_retry","event_id":row["event_id"]}
    db.execute("CREATE TABLE IF NOT EXISTS private_notification_receipts (event_id TEXT PRIMARY KEY, telegram_message_id INTEGER NOT NULL, at_unix INTEGER NOT NULL)")
    db.execute("INSERT INTO private_notification_receipts VALUES(?,?,?)",(row["event_id"],receipt["message_id"],stamp))
    db.execute("UPDATE events SET sent=1 WHERE seq=? AND sent=2",(row["seq"],))
    db.commit()
    return {"status":"delivered_confirmed","event_id":row["event_id"],
            "telegram_message_id":receipt["message_id"],"recipient":"verified_private_booking_chat"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("command",choices=["status","dispatch"])
    p.add_argument("--database",default=str(DEFAULT_DB))
    args=p.parse_args()
    with connect(Path(args.database).expanduser()) as db:
        if args.command=="status":
            ans={"queued":db.execute("SELECT count(*) FROM events WHERE sent=0").fetchone()[0],
                "sent":db.execute("SELECT count(*) FROM events WHERE sent=1").fetchone()[0],
                "uncertain":db.execute("SELECT count(*) FROM events WHERE sent=2").fetchone()[0],
                "runtime_enabled":os.environ.get("BHM_PRIVATE_TELEGRAM_ENABLE")=="1"}
        else:
            enabled=os.environ.get("BHM_PRIVATE_TELEGRAM_ENABLE")=="1"
            key=private_key() if enabled else None
            ans=dispatch_once(db,key,enabled=enabled)
    print(json.dumps(ans,sort_keys=True))
if __name__=="__main__":
    try:main()
    except (EventError,OSError,sqlite3.Error) as e:
        print(json.dumps({"status":"blocked","reason":str(e)}))
        sys.exit(2)
