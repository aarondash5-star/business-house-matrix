#!/usr/bin/env python3
"""Read-only competitor digest monitoring; target grants require human approval.
Dry-run is default. No autonomous alerts, publishing or campaign actions.
"""
import datetime as dt
import json
import sqlite3
from pathlib import Path
from urllib.parse import urlsplit
import research_engine as engine

RECHECK_HOURS=24
BACKOFF_HOURS=(1,4,12,24)

def validate_targets(config,grants):
    if not isinstance(config,dict) or not isinstance(config.get("targets"),list):
        raise ValueError("invalid_target_config")
    if len(config["targets"])>12:
        raise ValueError("too_many_targets")
    seen=set()
    targets=[]
    for target in config["targets"]:
        if not isinstance(target,dict) or not target.get("reviewed_by_owner"):
            raise ValueError("owner_review_required")
        url=engine.validate_url(target.get("url"),grants)
        if url in seen:continue
        seen.add(url)
        if target.get("role")!="confirmed_provider":
            raise ValueError("confirmed_provider_only")
        targets.append(url)
    return targets

def monitor_once(db,config,grants,fetcher=engine.fetch_extract,dry_run=True):
    targets=validate_targets(config,grants)
    result={"mode":"dry_run" if dry_run else "read_only_monitor",
            "scheduled":False,"checked":[],"manual_review_required":True,
            "automatic_notifications":False,"publish_approval":False,"spend_approval":False}
    for url in targets:
        host=urlsplit(url).hostname
        recent=db.execute("SELECT observed_utc,outcome FROM crawl_attempt WHERE url=? ORDER BY id DESC LIMIT 1",(url,)).fetchone()
        if recent:
            try:
                age=(dt.datetime.now(dt.timezone.utc)-dt.datetime.fromisoformat(recent[0])).total_seconds()
                if age<RECHECK_HOURS*3600:
                    result["checked"].append({"url":url,"status":"deferred_cooldown"})
                    continue
            except ValueError:
                pass
        if dry_run:
            result["checked"].append({"url":url,"status":"planned"})
            continue
        page=fetcher(url,grants,db)
        if page.get("status")!="needs_review":
            result["checked"].append({"url":url,"status":"unavailable","reason":page.get("reason","unknown")})
            continue
        state=engine.save_evidence(db,page)
        result["checked"].append({"url":url,"status":state["change"],
             "review_required":state["change"]=="content_changed_unverified"})
    return result

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--targets",required=True)
    p.add_argument("--db",required=True)
    p.add_argument("--grants",required=True)
    p.add_argument("--execute",action="store_true",help="Read-only approved target checks; no alerts")
    a=p.parse_args()
    config=json.loads(Path(a.targets).read_text())
    grants={x.strip().lower() for x in a.grants.split(",") if x.strip()}
    db=engine.connect(a.db)
    try:print(json.dumps(monitor_once(db,config,grants,dry_run=not a.execute),indent=2))
    finally:db.close()
if __name__=="__main__":main()
