#!/usr/bin/env python3
"""Owner-scope Bubblewrap workcell. Runs only fixed worker operations.

The model cannot supply commands or change process/mount flags. This file does
not provide Git push, SSH, dependency installs, provider APIs or deployments.
"""
import json
import os
import signal
import time
from pathlib import Path
import resource
import subprocess
import sys

WORKER=Path(__file__).with_name("workcell_worker.py")
STATIC_POLICY=WORKER.with_name("static_html_policy.py")
BWRAP=Path("/usr/bin/bwrap")
MAX_INPUT=70000

class IsolationError(RuntimeError):
    pass

def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(25,25))
    resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))
    resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))
    resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))

def isolated(workspace,action,request=None,*,cancel_file=None,timeout=40,deadline=None):
    if action not in ("probe","apply","qa"):
        raise IsolationError("action_not_enrolled")
    ws=Path(workspace)
    if ws.is_symlink() or not ws.is_dir() or not ws.is_absolute():
        raise IsolationError("workspace_not_trusted")
    if (not WORKER.is_file() or WORKER.is_symlink() or
            not STATIC_POLICY.is_file() or STATIC_POLICY.is_symlink() or
            not BWRAP.is_file()):
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
         "--ro-bind",str(STATIC_POLICY),"/static_html_policy.py",
         "--dir","/empty","--chdir","/workspace",
         "/usr/bin/python3","/worker.py",action]
    # Cancellation also applies mid-QA, not only between model attempts.
    if not 0 < timeout <= 40:
        raise IsolationError("worker_timeout_invalid")
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,text=True,start_new_session=True,
                       env={"HOME":"/empty","PATH":"/usr/bin:/bin","LANG":"C.UTF-8"},
                       preexec_fn=limits)
    start=time.monotonic()
    payload=blob
    try:
        while True:
            if cancel_file and Path(cancel_file).is_file():
                raise IsolationError("worker_cancelled")
            remaining=timeout-(time.monotonic()-start)
            if deadline is not None:
                remaining=min(remaining,deadline-time.monotonic())
            if remaining<=0:
                raise IsolationError("worker_deadline_exceeded")
            try:
                stdout,stderr=p.communicate(input=payload,timeout=min(.25,remaining))
                if len(stdout.encode("utf-8"))>70000 or len(stderr.encode("utf-8"))>70000:
                    raise IsolationError("worker_output_limit")
                if p.returncode:
                    raise IsolationError("isolated_"+action+"_failed:"+stderr[-180:])
                try:return json.loads(stdout)
                except json.JSONDecodeError:raise IsolationError("worker_response_invalid")
            except subprocess.TimeoutExpired as partial:
                payload=None
                if len(partial.stdout or b"")>70000 or len(partial.stderr or b"")>70000:
                    raise IsolationError("worker_output_limit")
    except BaseException:
        if p.poll() is None:
            try:os.killpg(p.pid,signal.SIGKILL)
            except ProcessLookupError:pass
        try:p.communicate(timeout=3)
        except Exception:pass
        raise

def doctor(workspace):
    result=isolated(workspace,"probe")
    needed=("home_hidden","foreign_project_hidden","host_service_hidden",
            "workspace_writable","net_namespace")
    return {"passed":all(result.get(name) is True for name in needed),
            "probe":result}

if __name__=="__main__":
    # Never accept untrusted workspace/path inputs from CLI as active capabilities.
    print(json.dumps({"status":"review_only","reason":"Use a trusted controller-enrolled manifest to invoke the workcell"}))
