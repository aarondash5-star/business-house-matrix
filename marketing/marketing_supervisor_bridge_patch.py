#!/usr/bin/env python3
"""Opt-in reversible Brain research_report integration of isolated LangGraph venv.

Does not create a new worker or modify any device identity, bridge or credentials.
"""
from pathlib import Path
import argparse
import os
import shutil

ROOT=Path("/opt/business-house-matrix/marketing/brain")
FILE=ROOT/"marketing_report_orchestrator.py"
BACKUP=FILE.with_name(FILE.name+".pre-langgraph-supervisor-20261022")
MARK="# BHM_LANGGRAPH_SUPERVISOR_V2_20261022"
EXTENSION='''
# BHM_LANGGRAPH_SUPERVISOR_V2_20261022
# The original v1 report builder remains available as _legacy_report_run
# for independent rollback; Brain sends only allowlisted business slugs.
_legacy_report_run = run
def run(business):
    import json
    import subprocess
    from pathlib import Path
    if business not in BUSINESSES:
        raise ValueError("business_not_registered")
    py = BASE / ".venv-supervisor" / "bin" / "python"
    script = BASE / "marketing_supervisor_langgraph.py"
    if not py.is_file() or not script.is_file():
        raise RuntimeError("reviewed_supervisor_runtime_unavailable")
    result = subprocess.run([str(py), str(script), "--business", business],
        capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=135,
        check=True, cwd=str(BASE))
    if len(result.stdout)>12000:
        raise RuntimeError("oversized_supervisor_receipt")
    data = json.loads(result.stdout.strip())
    if (data.get("mode")!="brain_owned_langgraph_supervisor_v2"
        or data.get("business")!=business
        or data.get("state") not in ("REVIEW_REQUIRED","INSUFFICIENT_EVIDENCE")
        or data.get("qa_passed") is not True
        or data.get("publish") is not False or data.get("spend") is not False):
        raise RuntimeError("unsafe_supervisor_receipt")
    expected = (OUTPUT / (business+"-supervisor-report.md")).resolve()
    if str(expected)!=str(Path(data.get("report_path","")).resolve()) or not expected.is_file():
        raise RuntimeError("invalid_supervisor_report_path")
    return data
'''
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--apply",action="store_true")
    p.add_argument("--rollback",action="store_true")
    args=p.parse_args()
    if args.apply and args.rollback:raise ValueError("conflicting_modes")
    if args.rollback:
        if not BACKUP.is_file():raise ValueError("rollback_backup_missing")
        original=BACKUP.read_text()
        compile(original,str(FILE),"exec")
        tmp=FILE.with_suffix(".rollback.tmp")
        tmp.write_text(original);os.chmod(tmp,0o600);os.replace(tmp,FILE)
        print({"result":"rolled_back"});return
    original=FILE.read_text()
    if MARK in original:
        print({"result":"already_installed"});return
    if original.count("def run(business):")!=1 or "def report_from_evidence" not in original:
        raise RuntimeError("v1_contract_changed")
    revised=original+"\n"+EXTENSION
    compile(revised,str(FILE),"exec")
    if args.apply:
        if BACKUP.exists():raise RuntimeError("backup_exists")
        shutil.copy2(FILE,BACKUP)
        tmp=FILE.with_suffix(".supervisor.tmp")
        tmp.write_text(revised);os.chmod(tmp,0o600);os.replace(tmp,FILE)
    print({"result":"installed" if args.apply else "preflight_ok",
           "old_tasks_preserved":True,"no_extra_worker":True})
if __name__=="__main__":main()
