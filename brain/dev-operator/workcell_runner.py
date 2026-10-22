#!/usr/bin/env python3
"""Owner-scope Bubblewrap workcell. Runs only fixed worker operations.

The model cannot supply commands or change process/mount flags. This file does
not provide Git push, SSH, dependency installs, provider APIs or deployments.
"""
import json
from pathlib import Path
import resource
import subprocess
import sys

WORKER=Path(__file__).with_name("workcell_worker.py")
BWRAP=Path("/usr/bin/bwrap")
MAX_INPUT=70000

class IsolationError(RuntimeError):
    pass

def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(25,25))
    resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))

def isolated(workspace,action,request=None):
    if action not in ("probe","apply","qa"):
        raise IsolationError("action_not_enrolled")
    ws=Path(workspace)
    if ws.is_symlink() or not ws.is_dir() or not ws.is_absolute():
        raise IsolationError("workspace_not_trusted")
    if not WORKER.is_file() or WORKER.is_symlink() or not BWRAP.is_file():
        raise IsolationError("runner_dependency_missing")
    blob=json.dumps(request or {},separators=(",",":"))
    if len(blob.encode("utf-8"))>MAX_INPUT:
        raise IsolationError("request_too_large")
    cmd=[str(BWRAP),"--unshare-all","--new-session","--die-with-parent",
         "--ro-bind","/usr","/usr","--ro-bind","/bin","/bin",
         "--ro-bind","/lib","/lib","--ro-bind","/lib64","/lib64",
         "--dev","/dev","--proc","/proc","--tmpfs","/tmp",
         "--bind",str(ws),"/workspace",
         "--ro-bind",str(WORKER),"/worker.py",
         "--dir","/empty","--chdir","/workspace",
         "/usr/bin/python3","/worker.py",action]
    p=subprocess.run(cmd,input=blob,capture_output=True,text=True,
                     stdin=subprocess.PIPE,timeout=40,
                     env={"HOME":"/empty","PATH":"/usr/bin:/bin","LANG":"C.UTF-8"},
                     preexec_fn=limits)
    if p.returncode:
        raise IsolationError("isolated_"+action+"_failed:"+p.stderr[-180:])
    try: return json.loads(p.stdout)
    except json.JSONDecodeError:raise IsolationError("worker_response_invalid")

def doctor(workspace):
    result=isolated(workspace,"probe")
    needed=("home_hidden","foreign_project_hidden","host_service_hidden",
            "workspace_writable","net_namespace")
    return {"passed":all(result.get(name) is True for name in needed),
            "probe":result}

if __name__=="__main__":
    # Never accept untrusted workspace/path inputs from CLI as active capabilities.
    print(json.dumps({"status":"review_only","reason":"Use a trusted controller-enrolled manifest to invoke the workcell"}))
