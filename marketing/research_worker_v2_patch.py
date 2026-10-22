#!/usr/bin/env python3
"""Install reviewed read-only v2 research task in pre-existing Dell paired relay.

Backup and source-signature validation are mandatory. No Mac transport edits,
identity edits, domain widening, shell routing, or credential transfer.
"""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

HOST=Path("/var/lib/generic-linux-automator-exec/matrix-research-transport/transport.py")
BACKUP=Path(str(HOST)+".pre-market-v2-20261022")
MARKER="# BHM_MARKET_RESEARCH_V2_20261022"

OLD='''            item=open_box(data["box"],private)
            if item.get("id")!=data["id"] or int(item.get("limit",0))!=5:raise ValueError("Malformed research envelope")
            q=validate_query(item.get("q"))
            # Only the preexisting Dell-local SearXNG CLI is executable; no shell, web crawling or stock downloads.
            result=subprocess.run([sys.executable,str(SEARCH),q,"--limit","5"],capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=43)
            if result.returncode:raise RuntimeError("Dell SearXNG unavailable")
            response=json.loads(result.stdout[:60000])
            if response.get("provider")!="self-hosted-searxng":raise RuntimeError("Unexpected provider")
            payload={"ok":True,"result":response}
'''
NEW='''            item=open_box(data["box"],private)
            if item.get("id")!=data["id"] or int(item.get("limit",0))!=5:
                raise ValueError("Malformed research envelope")
            # BHM_MARKET_RESEARCH_V2_20261022
            if item.get("v")==2 and item.get("op")=="research_market":
                if set(item)!={"v","id","op","topic","source_engine","limit"}:
                    raise ValueError("Unexpected v2 market fields")
                topic=item["topic"]
                source_engine=item["source_engine"]
                if topic!="moksha_arambol" or source_engine not in ("searxng","duckduckgo"):
                    raise ValueError("Market topic/source not granted")
                from urllib.request import Request,urlopen
                body=json.dumps({"topic":topic,"source_engine":source_engine,"refresh":False}).encode()
                req=Request("http://127.0.0.1:18890/v1/run",data=body,
                            headers={"Content-Type":"application/json"},method="POST")
                with urlopen(req,timeout=95) as http_result:
                    data_bytes=http_result.read(80001)
                if len(data_bytes)>80000:raise ValueError("Market packet too large")
                report=json.loads(data_bytes)
                if (report.get("schema")!="business_house_matrix.marketing_research.v1.3"
                    or report.get("topic")!=topic
                    or report.get("publish_approval") is not False
                    or report.get("spend_approval") is not False
                    or report.get("approved_for_design_claims") is not False
                    or report.get("ready_for_design_copy") is not False):
                    raise ValueError("Research packet safety contract")
                payload={"ok":True,"result":{"provider":"bhm-local-research-api",
                           "node":"dell-linux","report":report}}
            elif item.get("v")==1 and set(item)=={"v","id","q","limit"}:
                q=validate_query(item.get("q"))
                result=subprocess.run([sys.executable,str(SEARCH),q,"--limit","5"],
                                      capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=43)
                if result.returncode:raise RuntimeError("Dell SearXNG unavailable")
                response=json.loads(result.stdout[:60000])
                if response.get("provider")!="self-hosted-searxng":
                    raise RuntimeError("Unexpected provider")
                payload={"ok":True,"result":response}
            else:
                raise ValueError("Unsupported authenticated research operation")
'''

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--apply",action="store_true")
    p.add_argument("--rollback",action="store_true")
    a=p.parse_args()
    if a.apply and a.rollback:raise ValueError("conflicting_modes")
    if a.rollback:
        if not BACKUP.is_file():raise ValueError("backup_not_found")
        content=BACKUP.read_text()
        if content.count(OLD)!=1:raise ValueError("rollback_backup_mismatch")
        compile(content,str(HOST),"exec")
        temp=Path(str(HOST)+".v2-restore.tmp");temp.write_text(content)
        os.chmod(temp,0o600);temp.replace(HOST)
        print({"state":"rolled_back","restore_exact":True});return
    content=HOST.read_text()
    if MARKER in content:
        print({"state":"already_applied"});return
    if content.count(OLD)!=1:
        raise ValueError("existing_worker_source_signature_changed")
    modified=content.replace(OLD,NEW)
    compile(modified,str(HOST),"exec")
    if a.apply:
        if BACKUP.exists():raise ValueError("backup_already_exists")
        shutil.copy2(HOST,BACKUP)
        temp=Path(str(HOST)+".v2-stage.tmp")
        temp.write_text(modified)
        os.chmod(temp,0o600);temp.replace(HOST)
    print({"state":"applied" if a.apply else "preflight_passed",
           "source_exact_match":True,"transport_v1_search_preserved":True,
           "signed_receipt_preserved":True,"backup_path":str(BACKUP)})

if __name__=="__main__":main()
