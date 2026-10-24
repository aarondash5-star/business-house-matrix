"""Guarded QA governor runtime install.

Target: current Dell v0.2.0-multiproject controller.
Never changes project enrollment, SSH permissions, production URLs or old receipts.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime,timezone

HERE=Path(__file__).resolve().parent
TARGET=Path("/var/lib/generic-linux-automator-exec/matrix-controller")
CONTROLLER="controller.py"
NEW="quality_gate.py"
SERVICE="bhm-autonomy-controller.service"
OLD_SHA="6938aedb960b1cb7e890f57658333b90e34e25498aca6a9e2d71c2064a602208"
GATED=('website_stage','dev_project_build','dev_general_build','dev_scoped_build','pine_chat_stage','video_preview')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replace_once(src,old,new):
    if src.count(old)!=1:
        raise RuntimeError("controller_source_pattern_drift:"+str(src.count(old)))
    return src.replace(old,new,1)

def patch(src):
    # Every build completion is a technical receipt only. Owner quality review
    # remains an explicit and separate gate.
    src=replace_once(src,
'''def receipt(d,job_id,state,output=None,error=None,qa="unverified",remote=None):
    d.execute''',
'''def receipt(d,job_id,state,output=None,error=None,qa="unverified",remote=None):
    if state=="completed" and isinstance(output,dict):
        row=d.execute("SELECT project,action,brief FROM tasks WHERE id=?",(job_id,)).fetchone()
        if row is not None and row["action"] in '''+repr(GATED)+''':
            from quality_gate import annotate
            output=annotate(row["project"],row["brief"],output)
    d.execute''')
    src=replace_once(src,
'''    d.close()
    return {"controller_version":"0.2.0-multiproject","host":"dell-linux",
      "capabilities":{k:v["mode"] for k,v in ALLOWED.items()},
      "counts":groups,"evolution_outcomes":feedback,
      "tasks":[dict(r) for r in all_],"paid":False,"auto_publish":False,''',
'''    d.close()
    tasks=[]
    for r in all_:
        item=dict(r)
        if item["action"] in '''+repr(GATED)+''':
            item["quality_gate_status"]="technical_only_or_legacy_unassessed"
            item["release_authorized"]=False
        tasks.append(item)
    return {"controller_version":"0.2.1-quality-governed","host":"dell-linux",
      "capabilities":{k:v["mode"] for k,v in ALLOWED.items()},
      "quality_policy":{"build_success_is_design_approval":False,
                        "owner_review_required":True,"auto_promotion":False},
      "counts":groups,"evolution_outcomes":feedback,
      "tasks":tasks,"paid":False,"auto_publish":False,''')
    src=replace_once(src,
'''    if val.get("output"):
        try:val["output"]=json.loads(val["output"])
        except ValueError:pass
    return val''',
'''    if val.get("output"):
        try:val["output"]=json.loads(val["output"])
        except ValueError:pass
    if val["action"] in '''+repr(GATED)+''' and val["status"]=="completed" and isinstance(val.get("output"),dict):
        if "quality_gate" not in val["output"]:
            from quality_gate import annotate
            val["output"]=annotate(val["project"],val["brief"],val["output"])
            val["output"]["quality_gate"]["retrospective"]=True
    return val''')
    return src

def _run(cmd,timeout=40):
    x=subprocess.run(cmd,capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=timeout)
    if x.returncode:
        raise RuntimeError("command_failed:"+" ".join(cmd[:4])+":"+(x.stderr or x.stdout)[-900:])
    return x.stdout.strip()

def preflight():
    if TARGET.is_symlink() or sha(TARGET/CONTROLLER)!=OLD_SHA:
        raise RuntimeError("controller_changed_since_review")
    if (TARGET/NEW).exists():
        raise RuntimeError("quality_gate_already_present_or_conflicting")
    if not os.access(TARGET,os.W_OK):
        raise RuntimeError("runtime_not_writable")
    if not (HERE/NEW).is_file() or not (HERE/"test_quality_gate.py").is_file():
        raise RuntimeError("missing_release_source")
    with tempfile.TemporaryDirectory(prefix="matrix-quality-preflight-") as temp:
        d=Path(temp)
        (d/CONTROLLER).write_text(patch((TARGET/CONTROLLER).read_text()))
        shutil.copy2(HERE/NEW,d/NEW)
        for name in (CONTROLLER,NEW):
            compile((d/name).read_text(),str(d/name),"exec")
        _run([sys.executable,str(HERE/"test_quality_gate.py")],timeout=40)
        _run([sys.executable,str(d/CONTROLLER),"selftest"],timeout=40)
        # Simulate real completed build receipt without touching owner data.
        script='''import json,sqlite3,sys
sys.path.insert(0,sys.argv[1])
import controller
controller.HOME=__import__("pathlib").Path(sys.argv[2]);controller.DB=controller.HOME/"qa.sqlite3"
d=controller.connect()
d.execute("INSERT INTO tasks(id,idempotency,project,action,department,brief,status,created,updated) VALUES(?,?,?,?,?,?,?,?,?)",
("smoke","smokequalitygate","smoke_project","website_stage","Development","site_v1","queued","now","now"))
d.commit()
controller.receipt(d,"smoke","completed",{"qa_passed":True},None,"private_static_preview_qa")
x=controller.show("smoke")["output"]
assert x["technical_only"] is True and x["design_complete"] is False and x["release_approved"] is False
assert x["quality_gate"]["status"]=="requirements_missing"
print(json.dumps({"quality_gate":x["quality_gate"]["status"],"release_approved":x["release_approved"]}))
'''
        _run([sys.executable,"-c",script,str(d),str(d)],timeout=20)
    return {"qa_regression_passed":True,"controller_selftest_passed":True,
            "new_receipt_gated":True,"existing_moksha_function_unchanged":True,
            "expected_controller_sha256":OLD_SHA,"new_version":"0.2.1-quality-governed"}

def _service(action):
    return _run(["systemctl","--user",action,SERVICE],timeout=25)

def _copy(src,dest,mode=0o600):
    tmp=dest.with_name(dest.name+".qa-gate.tmp")
    if tmp.exists():raise RuntimeError("temporary_file_conflict")
    shutil.copyfile(src,tmp)
    tmp.chmod(mode)
    os.replace(tmp,dest)

def apply():
    proof=preflight()
    was_active=_run(["systemctl","--user","is-active",SERVICE])=="active"
    if not was_active:raise RuntimeError("service_not_active_no_blind_start")
    backup=TARGET/"release-backups"/("quality-gate-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    backup.mkdir(parents=True,mode=0o700,exist_ok=False)
    shutil.copy2(TARGET/CONTROLLER,backup/CONTROLLER)
    (backup/"preflight.json").write_text(json.dumps(proof,indent=2))
    try:
        _service("stop")
        _copy(HERE/NEW,TARGET/NEW)
        out=backup/"controller.new"
        out.write_text(patch((backup/CONTROLLER).read_text()))
        _copy(out,TARGET/CONTROLLER,0o700)
        _run([sys.executable,str(TARGET/CONTROLLER),"selftest"],timeout=35)
        _service("start")
        time.sleep(2)
        if _run(["systemctl","--user","is-active",SERVICE])!="active":
            raise RuntimeError("service_activation_failed")
        response=json.loads(_run([sys.executable,str(TARGET/CONTROLLER),"status"]))
        if response.get("controller_version")!="0.2.1-quality-governed" or response.get("quality_policy",{}).get("owner_review_required") is not True:
            raise RuntimeError("post_install_receipt_wrong")
        return {"status":"production_quality_governor_active","controller_version":response["controller_version"],
                "backup":str(backup),"service_active":True,"tests":proof,
                "public_site_changed":False,"permissions_changed":False,
                "historic_tasks_mutated":False}
    except BaseException:
        _copy(backup/CONTROLLER,TARGET/CONTROLLER,0o700)
        p=TARGET/NEW
        if p.exists() and not p.is_symlink():p.unlink()
        try:_service("start")
        except Exception:pass
        raise

if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("command",choices=("preflight","apply"))
    args=a.parse_args()
    try:print(json.dumps(preflight() if args.command=="preflight" else apply(),indent=2))
    except Exception as e:
        print(json.dumps({"status":"blocked_or_rolled_back","error":type(e).__name__,"reason":str(e)[:1000]}))
        sys.exit(1)
