#!/usr/bin/env python3
"""Guarded add-only Matrix 0.2.2 -> game-toolkit capability upgrade.

Not a game release. Every action is project/manifest allowlisted and must
pass the existing owner-pinned quality intake gate at submit *and* dispatch.
No arbitrary commands, changes to G3, SSH privileges or external publishing.
"""
from __future__ import annotations
from datetime import datetime, timezone
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

HERE = Path(__file__).resolve().parent
TARGET = Path("/var/lib/generic-linux-automator-exec/matrix-controller")
SERVICE = "bhm-autonomy-controller.service"
PROJECT = "shaadi_aunty_dodge"
ACTION = "game_toolkit"
ENGINE = "fixed_shaadi_recipe_v1"
RECIPES = (
    "shaadi_toolkit_verify_v1",
    "shaadi_toolkit_smoke_v1",
    "shaadi_mpfb_verify_v1",
    "shaadi_kenney_inventory_v1",
    "shaadi_gltf_cli_v1",
)
MANAGED = ("controller.py", "project_registry.py", "project_registry_v1.json",
           "quality_admission.py")
NEW = "game_toolkit_runner.py"

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise RuntimeError("source_pattern_drift_" + old[:70].replace("\n", "_"))
    return source.replace(old, new, 1)

def controller_patch(src: str) -> str:
    src = replace_once(src,
        ' "dev_project_build":{"department":"Development","mode":"manifest_enrolled_isolated_reviewed_patch_qa"},',
        ' "dev_project_build":{"department":"Development","mode":"manifest_enrolled_isolated_reviewed_patch_qa"},\n'
        ' "game_toolkit":{"department":"Development","mode":"owner_admitted_fixed_offline_qa"},')
    src = replace_once(src,
        '    if action=="dev_docs_fetch":',
        '    if action=="game_toolkit":\n'
        '        from project_registry import enroll_check\n'
        '        enroll_check(project,"game_toolkit",brief.strip())\n'
        '    if action=="dev_docs_fetch":')
    branch = '''        elif t["action"]=="game_toolkit":
            from project_registry import enroll_check
            from quality_gate import annotate
            project,manifest=t["project"],t["brief"]
            enroll_check(project,"game_toolkit",manifest)
            runner=HOME/"game_toolkit_runner.py"
            cmd=[sys.executable,str(runner),"run",project,manifest]
            run=subprocess.run(cmd,stdin=subprocess.DEVNULL,capture_output=True,
                               text=True,timeout=115)
            payload=json.loads(run.stdout) if run.stdout.strip() else {
                "technical_only":True,"published":False,"spent":False,
                "game_repository_modified":False,"qa_passed":False,
                "error":"isolated_tool_runner_rejected"}
            if run.returncode:
                payload["qa_passed"]=False
                payload["error"]="toolkit_runner_failed"
                payload["stderr_tail"]=run.stderr[-500:]
            good=(run.returncode==0 and payload.get("qa_passed") is True
                  and payload.get("published") is False
                  and payload.get("game_repository_modified") is False
                  and payload.get("technical_only") is True)
            payload=annotate(project,manifest,payload,HOME)
            receipt(d,t["id"],"completed" if good else "needs_review",payload,
                    None if good else "Game toolkit isolated QA failed or was denied",
                    "game_toolkit_technical_qa" if good else "unverified")
            out={"id":t["id"],"status":"completed" if good else "needs_review",
                 "qa_level":"game_toolkit_technical_qa" if good else "unverified",
                 "release_authorized":False}
'''
    src = replace_once(src,
        '        elif t["action"]=="dev_general_build":',
        branch + '        elif t["action"]=="dev_general_build":')
    src = replace_once(src,
        '"controller_version":"0.2.2-global-intake-governed"',
        '"controller_version":"0.2.3-shaadi-toolkit-governed"')
    return src

def registry_patch(src: str) -> str:
    return replace_once(src, '    "dev_project_build": {"reviewed_patch_v1"},',
        '    "dev_project_build": {"reviewed_patch_v1"},\n'
        '    "game_toolkit": {"fixed_shaadi_recipe_v1"},')

def admission_patch(src: str) -> str:
    return replace_once(src, '                        "repair_known_issue"))',
        '                        "repair_known_issue","game_toolkit"))')

def registry_json_patch(src: str) -> str:
    obj = json.loads(src)
    if set(obj) != {"schema_version", "projects"} or obj["schema_version"] != 1:
        raise RuntimeError("registry_schema_drift")
    if not isinstance(obj["projects"], list) or any(p.get("project") == PROJECT for p in obj["projects"]):
        raise RuntimeError("shaadi_registry_record_conflict")
    obj["projects"].append({"project": PROJECT, "approved": True,
                            "actions": {ACTION: {r: ENGINE for r in RECIPES}}})
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"

def staged_versions(src: Path) -> dict[str, bytes]:
    data = {name: (src/name).read_bytes() for name in MANAGED}
    if any((src/name).is_symlink() for name in MANAGED):
        raise RuntimeError("protected_runtime_source_symlink")
    staged = {
        "controller.py": controller_patch(data["controller.py"].decode()).encode(),
        "project_registry.py": registry_patch(data["project_registry.py"].decode()).encode(),
        "quality_admission.py": admission_patch(data["quality_admission.py"].decode()).encode(),
        "project_registry_v1.json": registry_json_patch(data["project_registry_v1.json"].decode()).encode(),
        NEW: (HERE / "game_toolkit_runner.py").read_bytes(),
    }
    for name, raw in staged.items():
        if name.endswith(".py"):
            compile(raw.decode(), name, "exec")
    return staged

def run(cmd, timeout=40) -> str:
    completed = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True,
                               text=True, timeout=timeout)
    if completed.returncode:
        raise RuntimeError("verification_command_failed_" + str(cmd[:3]) +
                           ":" + (completed.stderr or completed.stdout)[-600:])
    return completed.stdout.strip()

def preflight(expected_sha: str, target: Path = TARGET) -> dict:
    if (not isinstance(expected_sha, str) or len(expected_sha) != 64 or
            not all(ch in "0123456789abcdef" for ch in expected_sha)):
        raise RuntimeError("exact_controller_sha256_required")
    if target.is_symlink() or not target.is_dir():
        raise RuntimeError("runtime_target_missing_or_symlink")
    for name in (*MANAGED,):
        p = target/name
        if p.is_symlink() or not p.is_file():
            raise RuntimeError("protected_runtime_file_missing")
    if sha((target/"controller.py").read_bytes()) != expected_sha:
        raise RuntimeError("live_controller_hash_drift")
    if (target/NEW).exists():
        raise RuntimeError("existing_game_toolkit_runner_conflict")
    src = (target/"controller.py").read_text()
    if "0.2.2-global-intake-governed" not in src or "prebuild_owner_admission_required" not in src:
        raise RuntimeError("mandatory_owner_governance_missing")
    staged = staged_versions(target)
    if TARGET == target and run(["systemctl","--user","is-active",SERVICE]) != "active":
        raise RuntimeError("controller_service_not_active")
    with tempfile.TemporaryDirectory(prefix="shaadi-toolkit-release-preflight-") as temp:
        folder = Path(temp)
        for name, raw in staged.items():
            p = folder / name
            p.write_bytes(raw)
            p.chmod(0o600)
        # The unchanged quality_gate is a required dependency for the
        # staged controller's admission-negative selftest. Copy only to the
        # disposable preflight sandbox; never install/overwrite it.
        qg=target/"quality_gate.py"
        if qg.is_symlink() or not qg.is_file():
            raise RuntimeError("quality_gate_preflight_dependency_missing")
        (folder/"quality_gate.py").write_bytes(qg.read_bytes())
        run([sys.executable,str(folder/"project_registry.py"),
             "check",PROJECT,ACTION,RECIPES[0]])
        run([sys.executable,str(folder/"controller.py"),"selftest"],timeout=55)
        run([sys.executable,str(HERE/"test_game_toolkit_runner.py")],timeout=50)
    return {"status":"preflight_passed","old_controller_sha256":expected_sha,
            "planned_runtime_version":"0.2.3-shaadi-toolkit-governed",
            "source_shas":{key:sha(value) for key,value in staged.items()},
            "existing_project_registry_preserved":True,
            "owner_intake_gate_preserved":True, "publication":False}

def atomic_write(dst: Path, raw: bytes, mode: int) -> None:
    temp = dst.with_name(dst.name + ".game-toolkit-next")
    if temp.exists() or dst.is_symlink():
        raise RuntimeError("unsafe_existing_temp_or_symlink")
    fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,mode)
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(temp,mode)
        os.replace(temp,dst)
    finally:
        if temp.exists(): temp.unlink()

def apply(expected_sha: str) -> dict:
    report=preflight(expected_sha)
    staged=staged_versions(TARGET)
    backup=TARGET/"release-backups"/("shaadi-game-toolkit-"+datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    backup.mkdir(mode=0o700,parents=True,exist_ok=False)
    for name in MANAGED:
        shutil.copy2(TARGET/name,backup/name)
    (backup/"preflight.json").write_text(json.dumps(report,indent=2))
    created=False
    stopped=False
    try:
        run(["systemctl","--user","stop",SERVICE],timeout=30)
        stopped=True
        for name,raw in staged.items():
            atomic_write(TARGET/name,raw,0o700 if name=="controller.py" else 0o600)
            if name==NEW:created=True
        run([sys.executable,str(TARGET/"controller.py"),"selftest"],timeout=55)
        run([sys.executable,str(TARGET/"project_registry.py"),
             "check",PROJECT,ACTION,RECIPES[0]],timeout=15)
        run(["systemctl","--user","start",SERVICE],timeout=35)
        time.sleep(2)
        if run(["systemctl","--user","is-active",SERVICE])!="active":
            raise RuntimeError("service_failed_to_restart")
        stat=json.loads(run([sys.executable,str(TARGET/"controller.py"),"status"],timeout=20))
        if stat.get("controller_version")!="0.2.3-shaadi-toolkit-governed" or "game_toolkit" not in stat.get("capabilities",{}):
            raise RuntimeError("game_toolkit_action_not_advertised")
        if stat.get("quality_policy",{}).get("prebuild_owner_admission_required") is not True:
            raise RuntimeError("owner_intake_regressed")
        # Owner-approved quality contracts and an owner-maintained ledger are
        # NOT created by this installer; only the owner can approve their hashes.
        return {"status":"local_matrix_action_registered",
                "service_active":True, "version":stat["controller_version"],
                "toolkit_action":"game_toolkit","backup":str(backup),
                "owner_intake_ledger_mutated":False,
                "game_repo_modified":False, "production_published":False,
                "project_manifest_enrollment":list(RECIPES),
                "first_task_requires_owner_pinned_quality_contract":True}
    except BaseException:
        for name in MANAGED:
            try:atomic_write(TARGET/name,(backup/name).read_bytes(),
                             0o700 if name=="controller.py" else 0o600)
            except Exception:pass
        if created and (TARGET/NEW).is_file() and not (TARGET/NEW).is_symlink():
            (TARGET/NEW).unlink()
        if stopped:
            try:run(["systemctl","--user","start",SERVICE],timeout=35)
            except Exception:pass
        raise

def main():
    p=argparse.ArgumentParser()
    p.add_argument("command",choices=("preflight","apply"))
    p.add_argument("--expected-controller-sha256",required=True)
    args=p.parse_args()
    try:
        result=preflight(args.expected_controller_sha256) if args.command=="preflight" else apply(args.expected_controller_sha256)
        print(json.dumps(result,indent=2))
    except Exception as err:
        print(json.dumps({"status":"BLOCKED_OR_ROLLED_BACK","error":type(err).__name__,
                          "reason":str(err)[:600],"production_published":False}))
        sys.exit(2)

if __name__=="__main__":
    main()
