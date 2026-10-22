#!/usr/bin/env python3
"""Guarded, reversible registration of one Brain-owned research_report task."""
from pathlib import Path
import argparse,os,shutil
FILE=Path("/opt/business-house-matrix/marketing/brain/brain.py")
PRE=Path(str(FILE)+".pre-marketing-report-orchestrator-20261022")
MARK="# BHM_MARKETING_REPORT_OWNER_20261022"
def transform(s):
    if MARK in s:return s
    a='"research_market", "reel_pilot"'
    if s.count(a)!=1:raise ValueError("brain_task_registry_mismatch")
    s=s.replace(a,'"research_market", "research_report", "reel_pilot"')
    a='''    if task == "research_market":
        if set(payload)-{"topic","source_engine"}:'''
    if s.count(a)!=1:raise ValueError("brain_validation_hunk_mismatch")
    s=s.replace(a,'''    # BHM_MARKETING_REPORT_OWNER_20261022
    if task == "research_report":
        if set(payload)!={"business"} or payload.get("business") not in ("andaz_arambol","moksha_arambol"):
            raise ValueError("Unregistered business or report field")
'''+a)
    a='''    if task == "research_market":
        import research_market_bridge'''
    if s.count(a)!=1:raise ValueError("brain_execution_hunk_mismatch")
    s=s.replace(a,'''    if task == "research_report":
        import marketing_report_orchestrator
        if cfg.get("publish_enabled") or cfg.get("spend_enabled"):
            raise RuntimeError("research_report_requires_readonly_mode")
        return marketing_report_orchestrator.run(payload["business"])
'''+a)
    compile(s,str(FILE),"exec")
    return s
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--apply",action="store_true")
    p.add_argument("--rollback",action="store_true")
    a=p.parse_args()
    if a.apply and a.rollback:raise ValueError("conflicting_modes")
    if a.rollback:
        if not PRE.is_file():raise ValueError("rollback_not_available")
        s=PRE.read_text();compile(s,str(FILE),"exec")
        t=FILE.with_suffix(".rollback.tmp");t.write_text(s);os.chmod(t,0o600);os.replace(t,FILE)
        print({"status":"rolled_back"});return
    orig=FILE.read_text()
    new=transform(orig)
    if a.apply and new!=orig:
        if PRE.exists():raise ValueError("preexisting_rollback_backup")
        shutil.copy2(FILE,PRE)
        t=FILE.with_suffix(".report.tmp");t.write_text(new)
        os.chmod(t,0o600);os.replace(t,FILE)
    print({"status":"applied" if a.apply else "preflight_ok",
           "registered":"research_report","existing_jobs_preserved":True})
if __name__=="__main__":main()
