#!/usr/bin/env python3
"""Standalone, deny-by-default Bubblewrap verifier for reviewed source patches."""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import uuid

BASE=Path.home()/".local/share/matrix-code-executor"
WORKER=Path(__file__).with_name("sandbox_worker.py")
ALLOWED=frozenset({"pine_mcp_chat"})

def workspace(project):
    if project not in ALLOWED: raise ValueError("project_not_enrolled")
    BASE.mkdir(mode=0o700,parents=True,exist_ok=True)
    BASE.chmod(0o700)
    path=BASE/project
    if path.is_symlink(): raise ValueError("symlink_denied")
    path.mkdir(mode=0o700,exist_ok=True)
    if path.resolve().parent!=BASE.resolve(): raise ValueError("workspace_escape")
    return path

def set_limits():
    resource.setrlimit(resource.RLIMIT_CPU,(30,30))
    resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))

def isolated(project,action,payload=None):
    directory=workspace(project)
    cmd=["/usr/bin/bwrap","--unshare-all","--new-session","--die-with-parent",
         "--ro-bind","/usr","/usr","--ro-bind","/bin","/bin",
         "--ro-bind","/lib","/lib","--ro-bind","/lib64","/lib64",
         "--dev","/dev","--proc","/proc","--tmpfs","/tmp",
         "--bind",str(directory),"/workspace",
         "--ro-bind",str(WORKER),"/worker.py",
         "--dir","/empty","--chdir","/workspace",
         "/usr/bin/python3","/worker.py",action]
    p=subprocess.run(cmd,input=json.dumps(payload or {}),capture_output=True,text=True,
                     env={"PATH":"/usr/bin:/usr/local/bin:/bin","HOME":"/empty","LANG":"C.UTF-8"},
                     timeout=45,preexec_fn=set_limits)
    if p.returncode:raise RuntimeError("isolated_operation_failed:"+(p.stderr or "")[-500:])
    return json.loads(p.stdout)

def check(project):
    info=isolated(project,"probe")
    checks=("home_hidden","private_hidden","foreign_project_hidden",
            "net_blocked","workspace_writable")
    return {"passed":all(info.get(k) is True for k in checks),"detail":info}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("action",choices=("doctor","inventory","apply","test"))
    parser.add_argument("--project",default="pine_mcp_chat")
    parser.add_argument("--patch")
    args=parser.parse_args()
    if args.action=="doctor":out=check(args.project)
    elif args.action=="inventory":out=isolated(args.project,"inventory")
    elif args.action=="test":out=isolated(args.project,"test")
    else:
        if not check(args.project)["passed"]: raise RuntimeError("security_gate_failed")
        file=Path(args.patch or "")
        if not file.is_file() or file.is_symlink() or file.stat().st_size>330000:
            raise ValueError("reviewed_patch_file_required")
        out=isolated(args.project,"apply",json.loads(file.read_text()))
    out["action"]=args.action
    out["project"]=args.project
    print(json.dumps(out))
    if args.action=="doctor" and not out["passed"]:sys.exit(2)
if __name__=="__main__":
    try:main()
    except Exception as e:
        print(json.dumps({"status":"blocked","error":type(e).__name__,
                          "reason":str(e)[:500]}))
        sys.exit(1)
