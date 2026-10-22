#!/usr/bin/env python3
"""Exact-match, reversible Mac Marketing Brain research_market task patch."""
import argparse,os,shutil
from pathlib import Path
FILE=Path("/opt/business-house-matrix/marketing/brain/brain.py")
BACKUP=Path(str(FILE)+".pre-market-v2-20261022")
MARKER="# BHM_MARKET_V2_20261022"
def build(content):
    if MARKER in content:raise ValueError("already_applied")
    a='"research_brief", "reel_pilot"}'
    if content.count(a)!=1:raise ValueError("task_registry_changed")
    content=content.replace(a,'"research_brief", "research_market", "reel_pilot"}')
    a='''    if task == "research_brief":
        if not isinstance(payload.get("topic"), str)'''
    if content.count(a)!=1:raise ValueError("validation_contract_changed")
    b='''    # BHM_MARKET_V2_20261022
    if task == "research_market":
        if set(payload)-{"topic","source_engine"}:
            raise ValueError("Unexpected research_market fields")
        if payload.get("topic","moksha_arambol")!="moksha_arambol":
            raise ValueError("Topic not granted")
        if payload.get("source_engine","duckduckgo") not in ("duckduckgo","searxng"):
            raise ValueError("Research source not granted")
'''
    content=content.replace(a,b+a)
    a='''    if task == "research_search":
        import searxng_research'''
    if content.count(a)!=1:raise ValueError("execution_contract_changed")
    content=content.replace(a,'''    if task == "research_market":
        import research_market_bridge
        return research_market_bridge.market(payload.get("topic","moksha_arambol"),
                                             payload.get("source_engine","duckduckgo"))
'''+a)
    compile(content,str(FILE),"exec")
    return content
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--apply",action="store_true")
    p.add_argument("--rollback",action="store_true")
    a=p.parse_args()
    if a.apply and a.rollback:raise ValueError("conflicting_modes")
    if a.rollback:
        if not BACKUP.is_file():raise ValueError("missing_backup")
        s=BACKUP.read_text();compile(s,str(FILE),"exec")
        tmp=Path(str(FILE)+".v2-tmp");tmp.write_text(s);os.chmod(tmp,0o600);os.replace(tmp,FILE)
        print({"state":"rolled_back"});return
    s=build(FILE.read_text())
    if a.apply:
        if BACKUP.exists():raise ValueError("backup_exists")
        shutil.copy2(FILE,BACKUP)
        tmp=Path(str(FILE)+".v2-tmp");tmp.write_text(s);os.chmod(tmp,0o600);os.replace(tmp,FILE)
    print({"state":"applied" if a.apply else "preflight_passed","added_task":"research_market",
           "old_tasks_preserved":True,"signed_relay_reused":True})
if __name__=="__main__":main()
