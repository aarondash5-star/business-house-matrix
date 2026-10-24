"""Safe production v0.2.2 admission/release policy upgrade for Dell Matrix Tool Yard."""
from __future__ import annotations
import hashlib,json,os,shutil,subprocess,sys,tempfile,time
from datetime import datetime,timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
TARGET=Path("/var/lib/generic-linux-automator-exec/matrix-controller")
OLD_SHA="d2b46bef25a30cd0e40c74c192eb2b489c01a1378fc5048877c06bb7330a0742"
SERVICE="bhm-autonomy-controller.service"
EXTRAS=("quality_admission.py",)
LEDGERS=("owner-intake-approvals-v1.json","owner-release-approvals-v1.json")
CODE_ACTIONS=("website_stage","dev_project_build","dev_general_build","dev_scoped_build",
              "pine_chat_stage","video_preview","repair_known_issue")
def _sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def _sub(command,timeout=50):
    p=subprocess.run(command,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=timeout)
    if p.returncode:raise RuntimeError("test_or_service_command_failed:"+str(command[:4])+":"+(p.stderr or p.stdout)[-1000:])
    return p.stdout.strip()
def _once(code,old,new):
    if code.count(old)!=1:raise RuntimeError("runtime_patch_pattern_drift:"+repr(old[:90])+":"+str(code.count(old)))
    return code.replace(old,new,1)
def _patch(code):
    code=_once(code,
'''    ident=str(uuid.uuid4())
    status="blocked" if action in BLOCKERS else "queued"''',
'''    if action not in BLOCKERS:
        from quality_admission import intake_check
        intake_check(project,action,brief.strip(),HOME)
    ident=str(uuid.uuid4())
    status="blocked" if action in BLOCKERS else "queued"''')
    code=_once(code,
'''    d.execute("UPDATE tasks SET status='dispatching',attempts=attempts+1,updated=? WHERE id=?",
              (now(),t["id"]))''',
'''    try:
        from quality_admission import intake_check
        intake_check(t["project"],t["action"],t["brief"],HOME)
    except ValueError as err:
        receipt(d,t["id"],"needs_review",None,"Quality intake gate: "+str(err)[:170],"unverified")
        d.close()
        return {"id":t["id"],"status":"needs_review","quality_gate":"intake_denied"}
    d.execute("UPDATE tasks SET status='dispatching',attempts=attempts+1,updated=? WHERE id=?",
              (now(),t["id"]))''')
    code=_once(code,
'''      "quality_policy":{"build_success_is_design_approval":False,
                        "owner_review_required":True,"auto_promotion":False},''',
'''      "quality_policy":{"build_success_is_design_approval":False,
                        "owner_review_required":True,"auto_promotion":False,
                        "prebuild_owner_admission_required":True,
                        "dispatch_revalidates_admission":True,
                        "release_preflight_required":True,
                        "external_connectors_mediated":False},''')
    code=_once(code,'"controller_version":"0.2.1-quality-governed"','"controller_version":"0.2.2-global-intake-governed"')
    pos1=code.index("def test():")
    pos2=code.index("def main():",pos1)
    updated_test='''def test():
    """Old feature-preservation regression plus new mandatory intake fail-closed."""
    with tempfile.TemporaryDirectory(prefix="matrix-global-qa-test-") as name:
        global HOME,DB
        prior_home,prior_db=HOME,DB
        try:
            HOME=Path(name);DB=HOME/"test.sqlite3"
            a=submit("devpilot","research_search","Python TaskGroup official documentation",
                     "Python TaskGroup official documentation","smoke-research-v022")
            b=submit("devpilot","research_search","Python TaskGroup official documentation",
                     "Python TaskGroup official documentation","smoke-research-v022")
            assert a["id"]==b["id"] and b["deduplicated"]
            c=submit("marketing","video_preview","Blocked until thermal review")
            assert c["status"]=="blocked"
            try:submit("pine_mcp_chat","pine_chat_stage","pine_chat_v1")
            except ValueError:pass
            else:raise AssertionError("Unapproved new coding admission accepted")
            try:submit("moksha_overhaul","website_stage","moksha_overhaul_v1")
            except ValueError:pass
            else:raise AssertionError("Unapproved new Moksha staging accepted")
            try:submit("private_foreign","dev_general_build","matrix-dev-dashboard-v4")
            except ValueError:pass
            else:raise AssertionError("Cross-project build scope accepted")
            try:submit("devpilot","research_search","email contact","email alice@example.com")
            except ValueError:pass
            else:raise AssertionError("Private contact passed public validation")
            assert status()["counts"]=={"queued":1,"blocked":1}
            assert status()["quality_policy"]["prebuild_owner_admission_required"] is True
            assert recover()["flagged_uncertain_dispatches"]==0
            return {"passed":True,"tests":["read-only research", "idempotency",
                   "production route remains blocked","unapproved new build denied",
                   "project isolation","privacy validation","conservative recovery"]}
        finally:HOME,DB=prior_home,prior_db

'''
    code=code[:pos1]+updated_test+code[pos2:]
    return code
def _copy(src,dest,mode=0o600):
    tmp=dest.with_name(dest.name+".globalgate.tmp")
    if tmp.exists():raise RuntimeError("temporary_collision")
    shutil.copyfile(src,tmp)
    tmp.chmod(mode)
    os.replace(tmp,dest)
def preflight():
    if _sha(TARGET/"controller.py")!=OLD_SHA:raise RuntimeError("installed_controller_sha_changed")
    for x in (*EXTRAS,*LEDGERS):
        if (TARGET/x).exists():raise RuntimeError("runtime_file_conflict:"+x)
    if _sub(["systemctl","--user","is-active",SERVICE])!="active":raise RuntimeError("service_inactive")
    source=(HERE/"quality_admission.py")
    if not source.is_file():raise RuntimeError("new_policy_missing")
    _sub([sys.executable,str(HERE/"test_quality_admission.py")],timeout=30)
    _sub([sys.executable,str(HERE/"test_quality_gate.py")],timeout=30)
    with tempfile.TemporaryDirectory(prefix="matrix-global-intake-preflight-") as td:
        work=Path(td)
        (work/"controller.py").write_text(_patch((TARGET/"controller.py").read_text()))
        shutil.copy2(HERE/"quality_admission.py",work/"quality_admission.py")
        for fn in ("quality_gate.py","project_registry.py","project_registry_v1.json"):
            shutil.copy2(TARGET/fn,work/fn)
        for fn in ("controller.py","quality_admission.py"):
            compile((work/fn).read_text(),fn,"exec")
        _sub([sys.executable,str(work/"controller.py"),"selftest"],timeout=35)
    return {"status":"preflight_passed","old_controller_sha":OLD_SHA,
            "independent_regressions_passed":True,"owner_intake_before_submit":True,
            "owner_intake_before_dispatch":True,
            "release_preflight_is_a_deny_by_default_command":True,
            "external_provider_connectors_not_governed_yet":True}
def apply():
    pre=preflight()
    backup=TARGET/"release-backups"/("global-gates-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    backup.mkdir(parents=True,mode=0o700,exist_ok=False)
    shutil.copy2(TARGET/"controller.py",backup/"controller.py")
    (backup/"preflight.json").write_text(json.dumps(pre,indent=2))
    changed=[]
    try:
        _sub(["systemctl","--user","stop",SERVICE],timeout=25)
        for name in EXTRAS:
            _copy(HERE/name,TARGET/name);changed.append(name)
        for name in LEDGERS:
            p=TARGET/name
            p.write_text('{"schema_version":1,"approvals":[]}\n',encoding="utf-8")
            p.chmod(0o600);changed.append(name)
        candidate=backup/"controller.new"
        candidate.write_text(_patch((backup/"controller.py").read_text()))
        _copy(candidate,TARGET/"controller.py",0o700)
        _sub([sys.executable,str(TARGET/"controller.py"),"selftest"],timeout=35)
        _sub(["systemctl","--user","start",SERVICE],timeout=25)
        time.sleep(2)
        if _sub(["systemctl","--user","is-active",SERVICE])!="active":
            raise RuntimeError("service_inactive_after_restart")
        status=json.loads(_sub([sys.executable,str(TARGET/"controller.py"),"status"],timeout=15))
        if status.get("controller_version")!="0.2.2-global-intake-governed" or status.get("quality_policy",{}).get("prebuild_owner_admission_required") is not True:
            raise RuntimeError("postdeploy_state_mismatch")
        blocked=subprocess.run([sys.executable,str(TARGET/"quality_admission.py"),"release-check",
                    "delulu_tech","delulu_homepage_v1","--artifact-sha256","a"*64],
                    capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=15)
        if blocked.returncode==0:raise RuntimeError("release_check_fail_open")
        return {"status":"production_global_admission_active",
                "controller_version":status["controller_version"],
                "backup":str(backup),
                "service_active":True,"builds_require_pinned_owner_contract":True,
                "releases_require_separate_owner_record":True,
                "new_approvals_enrolled":0,"external_platform_routes_intercepted":False,
                "historical_tasks_mutated":False,"permissions_changed":False,
                "tests":pre}
    except BaseException:
        _copy(backup/"controller.py",TARGET/"controller.py",0o700)
        for name in reversed(changed):
            p=TARGET/name
            if p.exists() and not p.is_symlink():p.unlink()
        try:_sub(["systemctl","--user","start",SERVICE],timeout=25)
        except Exception:pass
        raise
if __name__=="__main__":
    import argparse
    a=argparse.ArgumentParser();a.add_argument("command",choices=("preflight","apply"))
    args=a.parse_args()
    try:print(json.dumps(preflight() if args.command=="preflight" else apply(),indent=2))
    except Exception as e:
        print(json.dumps({"status":"blocked_or_rolled_back","error":type(e).__name__,"message":str(e)[:1400]}))
        sys.exit(1)
