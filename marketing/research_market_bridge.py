#!/usr/bin/env python3
"""Mac Marketing Brain → Dell public research packet via trusted signed relay.

Imports existing transport's device identity and cryptography; no private key
export, no new gateway endpoint, no edits to the Mac signed transport.
"""
import argparse
import hashlib
import importlib.util
import json
import sqlite3
import time
import uuid
from pathlib import Path

SOURCE=Path("/var/lib/generic-linux-automator-exec/matrix-research-transport/transport.py")
TOPICS=frozenset(("moksha_arambol",))
ENGINES=frozenset(("searxng","duckduckgo"))

def runtime():
    spec=importlib.util.spec_from_file_location("bhm_existing_paired_research",SOURCE)
    if spec is None or spec.loader is None:raise RuntimeError("Existing paired transport unavailable")
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

def market(topic="moksha_arambol",source_engine="duckduckgo",seconds=108):
    if topic not in TOPICS or source_engine not in ENGINES:
        raise ValueError("public_research_scope_not_granted")
    t=runtime()
    ownid,sk,private=t.own()
    target=t.peer()
    if ownid["host_id"]!="mac-linux" or target["host_id"]!="dell-linux":
        raise RuntimeError("incorrect_paired_research_identity")
    digest="market-v2-"+hashlib.sha256((topic+"|"+source_engine).encode()).hexdigest()
    db=t.local_db();now=int(time.time())
    existing=db.execute("SELECT id,box,expires FROM requests WHERE digest=?",(digest,)).fetchone()
    if existing and existing[2]>now+20:
        jobid,boxed,expires=existing
    else:
        jobid=str(uuid.uuid4());expires=now+175
        boxed=t.envelope({"v":2,"id":jobid,"op":"research_market","topic":topic,
                           "source_engine":source_engine,"limit":5},target["box_key"])
        db.execute("INSERT OR REPLACE INTO requests(digest,id,box,expires) VALUES(?,?,?,?)",
                   (digest,jobid,boxed,expires))
        db.commit()
    db.close()
    accepted=t.http("/submit",{"host":"mac-linux","id":jobid,"box":boxed,"expires":expires,
                                "sig":t.sig(sk,"submit","mac-linux",jobid,expires,boxed)})
    if accepted.get("id")!=jobid:raise RuntimeError("market_relay_receipt_mismatch")
    deadline=time.monotonic()+max(15,min(125,int(seconds)))
    while time.monotonic()<deadline:
        receipt=t.status(jobid,sk)
        if receipt.get("state")=="completed":
            obj=t.open_box(receipt["box"],private)
            if obj.get("id")!=jobid or not isinstance(obj.get("payload"),dict):
                raise RuntimeError("incorrect_signed_report_envelope")
            payload=obj["payload"]
            if not t.verify(target["verify_key"],obj.get("signature",""),
                            "receipt","dell-linux",jobid,t.canon(payload)):
                raise RuntimeError("invalid_Dell_receipt_signature")
            if not payload.get("ok"):
                raise RuntimeError("Dell research unavailable:"+str(payload.get("error","unknown"))[:75])
            result=payload.get("result",{})
            if (result.get("node")!="dell-linux" or result.get("provider")!="bhm-local-research-api"):
                raise RuntimeError("untrusted_research_provider")
            report=result.get("report",{})
            if (report.get("schema")!="business_house_matrix.marketing_research.v1.3"
                or report.get("topic")!=topic
                or report.get("requested_engine")!=source_engine
                or report.get("publish_approval") is not False
                or report.get("approved_for_design_claims") is not False):
                raise RuntimeError("unsafe_market_packet")
            return {"provider":"bhm_encrypted_signed_research_api_v2",
                    "signed_device_pair_verified":True,"request_id":jobid,
                    "source_engine":source_engine,"report":report,
                    "paid_fallback":False,"publish_approval":False}
        if receipt.get("expired"):
            raise RuntimeError("market_request_expired_"+jobid)
        time.sleep(3)
    raise RuntimeError("market_request_pending_"+jobid)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--topic",choices=sorted(TOPICS),default="moksha_arambol")
    p.add_argument("--engine",choices=sorted(ENGINES),default="duckduckgo")
    args=p.parse_args()
    try:
        r=market(args.topic,args.engine)
        report=r["report"]
        print(json.dumps({"status":"ok","provider":r["provider"],
                          "signed_device_pair_verified":r["signed_device_pair_verified"],
                          "request_id":r["request_id"],"source_engine":r["source_engine"],
                          "source_count":report["source_count"],
                          "provider_leads":len(report["unverified_leads"]),
                          "discovery_queries":[{"status":x.get("status"),"count":len(x.get("sources",[])),
                                               "fallback_used":x.get("fallback_used",False)}
                                               for x in report.get("discovery_queries",[])],
                          "design_ready":report["ready_for_design_copy"],
                          "publish":report["publish_approval"]},ensure_ascii=False,indent=2))
    except (RuntimeError,ValueError) as exc:
        print(json.dumps({"status":"error","reason":str(exc)[:150]}))
        raise SystemExit(2)
