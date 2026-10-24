"""Production rollout of reviewed multi-project Matrix controller overlay.

Refuses unknown runtime versions. Preserves the prior controller, runner and
user service state; never changes sudo, root, secrets or external publishing.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

TARGET = Path("/var/lib/generic-linux-automator-exec/matrix-controller")
HERE = Path(__file__).resolve().parent
EXPECTED = {
    "controller.py": "b1ed132245b1bac5fb0cd66b16f1632e457bdeffaea9ac3b300b5cb7b1b9209e",
    "reviewed_patch_runner.py": "11850510131d9d2c624e8771cd9d568d7ee973c476f8750a43af6c969f894681",
}
NEW = ("project_registry.py", "project_registry_v1.json", "project_static_stage.py")
SERVICE = "bhm-autonomy-controller.service"

def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError("source_pattern_mismatch_" + label + "_" + str(count))
    return text.replace(old, new, 1)

def patched_controller(text: str) -> str:
    text = replace_once(text,
        ' "dev_general_build":{"department":"Development","mode":"manifest_enrolled_sandbox_review_only"},',
        ' "dev_general_build":{"department":"Development","mode":"manifest_enrolled_sandbox_review_only"},\n'
        ' "dev_project_build":{"department":"Development","mode":"manifest_enrolled_isolated_reviewed_patch_qa"},',
        "allowed_action")
    text = replace_once(text,
        '    if action=="website_stage" and (project!="moksha_overhaul" or brief.strip()!="moksha_overhaul_v1"):\n'
        '        raise ValueError("Website staging has no approved project/manifest scope")',
        '    if action=="website_stage":\n'
        '        from project_registry import enroll_check\n'
        '        enroll_check(project,"website_stage",brief.strip())\n'
        '    if action=="dev_project_build":\n'
        '        from project_registry import enroll_check\n'
        '        enroll_check(project,"dev_project_build",brief.strip())',
        "submit_guards")
    text = replace_once(text,
        '            result=subprocess.run([sys.executable,str(HOME/"site_staging.py"),"build",t["project"],t["brief"]],\n'
        '                capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=45)',
        '            from project_registry import website_command\n'
        '            result=subprocess.run(website_command(HOME,t["project"],t["brief"]),\n'
        '                capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=45)',
        "website_runner")
    dev_branch = '''        elif t["action"]=="dev_project_build":
            from project_registry import fixed_patch_path
            project,manifest=t["project"],t["brief"]
            patch_path=fixed_patch_path(HOME,project,manifest)
            runner=HOME/"reviewed_patch_runner.py"
            def toolyard(action,extra=()):
                cmd=[sys.executable,str(runner),action,"--project",project,*extra]
                run=subprocess.run(cmd,capture_output=True,text=True,
                        stdin=subprocess.DEVNULL,timeout=65)
                if run.returncode:
                    raise RuntimeError("Isolated Tool Yard "+action+" rejected: "+(run.stderr or run.stdout)[-220:])
                return json.loads(run.stdout)
            doctor=toolyard("doctor")
            if doctor.get("passed") is not True:
                raise RuntimeError("Tool Yard sandbox isolation gate failed")
            applied=toolyard("apply",("--patch",str(patch_path)))
            qa=toolyard("test")
            good=qa.get("passed") is True and qa.get("tests_executed") is True
            result_data={"project":project,"manifest":manifest,
                         "sandbox":doctor.get("detail",{}),
                         "written":applied.get("written",[]),
                         "independent_qa":qa,"published":False,"spent":False}
            receipt(d,t["id"],"completed" if good else "needs_review",result_data,
                    None if good else "Isolated project tests did not pass",
                    "project_isolated_executed_qa" if good else "unverified")
            out={"id":t["id"],"status":"completed" if good else "needs_review",
                 "qa_level":"project_isolated_executed_qa" if good else "unverified"}
'''
    text = replace_once(text,
        '        elif t["action"]=="dev_general_build":\n',
        dev_branch + '        elif t["action"]=="dev_general_build":\n',
        "generic_dev_pipeline")
    text = replace_once(text,
        '"controller_version":"0.1.0"',
        '"controller_version":"0.2.0-multiproject"',
        "version")
    return text

def patched_runner(text: str) -> str:
    text=replace_once(text,
        'ALLOWED=frozenset({"pine_mcp_chat"})',
        'from project_registry import patch_allowed',
        "runner_allowlist")
    text=replace_once(text,
        '    if project not in ALLOWED: raise ValueError("project_not_enrolled")',
        '    if not patch_allowed(project): raise ValueError("project_not_enrolled")',
        "runner_workspace")
    return text

def preflight() -> dict:
    for name,expected in EXPECTED.items():
        p=TARGET/name
        if p.is_symlink() or not p.is_file() or digest(p.read_bytes())!=expected:
            raise RuntimeError("live_source_drift_" + name)
        if not os.access(p,os.W_OK):
            raise RuntimeError("source_not_writable_" + name)
    if not os.access(TARGET,os.W_OK):
        raise RuntimeError("controller_directory_not_writable")
    for name in NEW:
        p=HERE/name
        if p.is_symlink() or not p.is_file():
            raise RuntimeError("release_file_missing_" + name)
        if (TARGET/name).exists():
            raise RuntimeError("unexpected_prior_release_" + name)
    db=TARGET/"tasks.sqlite3"
    con=sqlite3.connect(f"file:{db}?mode=ro",uri=True,timeout=3)
    active=con.execute("SELECT count(*) FROM tasks WHERE status='dispatching'").fetchone()[0]
    con.close()
    if active:
        raise RuntimeError("controller_has_active_dispatches")
    control=patched_controller((TARGET/"controller.py").read_text())
    runner=patched_runner((TARGET/"reviewed_patch_runner.py").read_text())
    from pathlib import Path as P
    with tempfile.TemporaryDirectory(prefix="multi-project-qa-") as d:
        stage=P(d)
        for name,content in (("controller.py",control),("reviewed_patch_runner.py",runner)):
            (stage/name).write_text(content,encoding="utf-8")
        for name in NEW:
            shutil.copyfile(HERE/name,stage/name)
        for name in ("controller.py","reviewed_patch_runner.py","project_registry.py","project_static_stage.py"):
            compile((stage/name).read_text(),str(stage/name),"exec")
        stage_registry=stage/"project_registry.py"
        sys.path.insert(0,str(stage))
        try:
            import project_registry as r
            assert r.enroll_check("moksha_overhaul","website_stage","moksha_overhaul_v1",stage/"project_registry_v1.json")=="legacy_moksha"
            assert r.enroll_check("delulu_tech","website_stage","delulu_homepage_v1",stage/"project_registry_v1.json")=="static_v1"
            assert r.enroll_check("andaz_website","dev_project_build","andaz_homepage_v1",stage/"project_registry_v1.json")=="reviewed_patch_v1"
            assert r.patch_allowed("pine_mcp_chat",stage/"project_registry_v1.json")
            for proj,action,manifest in (
                ("unknown_project","website_stage","delulu_homepage_v1"),
                ("delulu_tech","website_stage","moksha_overhaul_v1"),
                ("../secret","website_stage","delulu_homepage_v1"),
            ):
                try: r.enroll_check(proj,action,manifest,stage/"project_registry_v1.json")
                except r.EnrollmentError: pass
                else: raise RuntimeError("negative_project_gate_failed")
        finally:
            sys.path.remove(str(stage))
            sys.modules.pop("project_registry",None)
        test=subprocess.run([sys.executable,str(stage/"controller.py"),"selftest"],
                            capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=30)
        if test.returncode:
            raise RuntimeError("controller_selftest_failed:"+test.stderr[-500:]+test.stdout[-300:])
    return {"source_pinned":True,"compilation_passed":True,
            "multi_project_positive_and_negative_tests":True,
            "legacy_controller_selftest":True,"old_version":EXPECTED,
            "new_files":list(NEW),"publish":False,"spend":False}

def service(action):
    result=subprocess.run(["systemctl","--user",action,SERVICE],
                          capture_output=True,text=True,timeout=20)
    if result.returncode:
        raise RuntimeError("controller_service_"+action+"_failed:"+(result.stderr or "")[-200:])

def active():
    result=subprocess.run(["systemctl","--user","is-active",SERVICE],
                          capture_output=True,text=True,timeout=10)
    return result.returncode==0 and result.stdout.strip()=="active"

def atomic_copy(src: Path, dest: Path, mode=0o600):
    temp=dest.with_name(dest.name+".multi-release-temp")
    if temp.exists():
        raise RuntimeError("temporary_install_conflict")
    shutil.copyfile(src,temp,follow_symlinks=False)
    temp.chmod(mode)
    os.replace(temp,dest)

def deploy():
    result=preflight()
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup=TARGET/"release-backups"/("multiproject-"+stamp)
    backup.mkdir(mode=0o700,parents=True,exist_ok=False)
    for name in EXPECTED:
        shutil.copyfile(TARGET/name,backup/name)
    (backup/"manifest.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    had_active=active()
    try:
        if had_active:
            service("stop")
        for name in NEW:
            atomic_copy(HERE/name,TARGET/name,0o600)
        for name,transform in (("controller.py",patched_controller),
                               ("reviewed_patch_runner.py",patched_runner)):
            text=transform((backup/name).read_text())
            staged=backup/(name+".new")
            staged.write_text(text,encoding="utf-8")
            atomic_copy(staged,TARGET/name,0o700 if name=="controller.py" else 0o600)
        check=subprocess.run([sys.executable,str(TARGET/"controller.py"),"selftest"],
                             capture_output=True,text=True,timeout=30)
        if check.returncode:
            raise RuntimeError("live_controller_selftest_failed")
        verify=subprocess.run([sys.executable,str(TARGET/"project_registry.py"),"status"],
                              capture_output=True,text=True,timeout=10)
        if verify.returncode:
            raise RuntimeError("registry_runtime_rejected")
        if had_active:
            service("start")
            time.sleep(2)
            if not active():
                raise RuntimeError("controller_not_active_after_upgrade")
        return {"status":"production_controller_upgraded","backup":str(backup),
                "controller_active":active(),"registry":json.loads(verify.stdout),
                "selftest":True,"publish":False,"spend":False}
    except BaseException:
        for name in EXPECTED:
            atomic_copy(backup/name,TARGET/name,0o700 if name=="controller.py" else 0o600)
        for name in NEW:
            p=TARGET/name
            if p.is_file() and not p.is_symlink():
                p.unlink()
        if had_active:
            try: service("start")
            except Exception: pass
        raise

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("command",choices=("preflight","apply"))
    args=p.parse_args()
    try:
        print(json.dumps(preflight() if args.command=="preflight" else deploy(),indent=2))
    except Exception as exc:
        print(json.dumps({"status":"blocked_or_rolled_back","reason":type(exc).__name__,
                          "detail":str(exc)[:600]}))
        sys.exit(1)
