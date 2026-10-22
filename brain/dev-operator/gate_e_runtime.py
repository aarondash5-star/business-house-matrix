"""Gate E candidate: immutable-source, owner-enrolled multi-file Dev workflow.

Separate from the live v6 controller. No remote publishing, root, network for
test workcells, dependency installs, or model-chosen shell operations.
"""
from dataclasses import dataclass
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import re
import resource
import shutil
import signal
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
MAX_CONTEXT_BYTES = 200_000
MAX_CONTEXT_FILES = 16
MAX_ATTEMPTS = 3
TIME_BUDGET = 240
NODE = Path("/usr/bin/node")
BWRAP = Path("/usr/bin/bwrap")

class GateError(RuntimeError):
    pass

class Cancelled(GateError):
    pass

def load(name):
    spec=importlib.util.spec_from_file_location("gate_e_"+name,HERE/(name+".py"))
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module

def check_cancel(cancel_file):
    if cancel_file and Path(cancel_file).is_file():
        raise Cancelled("owner_cancellation_requested")

def bounded(cmd, *, cwd, timeout=30, input_text=None, cancel_file=None, isolated_env=None):
    """Fixed-argv subprocess with process-group termination on timeout/cancel."""
    env=isolated_env or {"PATH":"/usr/bin:/bin","HOME":"/empty",
                         "LANG":"C.UTF-8","PYTHONDONTWRITEBYTECODE":"1"}
    proc=subprocess.Popen(cmd,cwd=str(cwd),stdin=subprocess.PIPE if input_text is not None else subprocess.DEVNULL,
                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                          start_new_session=True,env=env)
    payload=input_text
    start=time.monotonic()
    try:
        while True:
            check_cancel(cancel_file)
            try:
                out,err=proc.communicate(input=payload,timeout=0.35)
                return {"code":proc.returncode,"stdout":out[-2000:],"stderr":err[-2000:]}
            except subprocess.TimeoutExpired:
                # communicate may retain internal input state after timeout.
                payload=None
                if time.monotonic()-start>timeout:
                    raise GateError("execution_timeout")
    except (Cancelled,GateError,BaseException):
        if proc.poll() is None:
            try: os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError: pass
        try:proc.communicate(timeout=3)
        except Exception:pass
        raise

def git(repo,*args):
    p=subprocess.run(["/usr/bin/git","-c","core.hooksPath=/dev/null",*args],
                     cwd=str(repo),stdin=subprocess.DEVNULL,capture_output=True,
                     timeout=18,env={"PATH":"/usr/bin:/bin","HOME":"/empty",
                                    "GIT_CONFIG_NOSYSTEM":"1","GIT_CONFIG_GLOBAL":"/dev/null",
                                    "GIT_TERMINAL_PROMPT":"0"})
    if p.returncode:raise GateError("immutable_git_lookup_failed")
    return p.stdout

@dataclass(frozen=True)
class Enrollment:
    scope: object
    goal: str
    context: tuple
    tests: tuple
    writable: tuple

def enrollment(record):
    p=load("protocol")
    if not isinstance(record,dict) or set(record)!={"manifest","goal","context","tests"}:
        raise GateError("enrollment_schema")
    scope=p.enroll(record["manifest"])
    goal=record["goal"]
    if not isinstance(goal,str) or not 15<=len(goal)<=800:
        raise GateError("goal_bounds")
    context=record["context"];tests=record["tests"]
    if not isinstance(context,list) or not isinstance(tests,list) or not 1<=len(tests)<=8:
        raise GateError("context_or_tests_schema")
    context=tuple(p.path(x) for x in context)
    tests=tuple(p.path(x) for x in tests)
    if len(context)>MAX_CONTEXT_FILES or len(set(context))!=len(context) or len(set(tests))!=len(tests):
        raise GateError("duplicate_or_excessive_context")
    if not all(x.startswith("tests/") for x in tests):
        raise GateError("trusted_tests_only")
    if not set(tests).issubset(scope.files):
        raise GateError("tests_not_enrolled")
    writable=tuple(x for x in scope.files if x not in tests)
    if not writable or any("tests" in Path(x).parts for x in writable):
        raise GateError("test_source_write_denied")
    if scope.test_profile not in ("python-unittest","node-test"):
        raise GateError("language_profile_not_certified")
    if set(writable).intersection(context):
        raise GateError("read_only_context_conflict")
    return Enrollment(scope,goal,context,tests,writable)

def source_verify(source,enrolled):
    src=Path(source)
    if src.is_symlink() or not src.is_dir() or not src.is_absolute():
        raise GateError("source_checkout_untrusted")
    expected="https://github.com/"+enrolled.scope.repository+".git"
    if git(src,"remote","get-url","origin").decode().strip()!=expected:
        raise GateError("repository_identity_mismatch")
    if git(src,"rev-parse",enrolled.scope.base_sha+"^{commit}").decode().strip()!=enrolled.scope.base_sha:
        raise GateError("immutable_base_not_present")

def read_blob(src,sha,name,missing_ok=False):
    # ls-tree exact path, never recursively check out a model-chosen directory.
    line=git(src,"ls-tree",sha,"--",name).decode("utf-8")
    if not line.strip() and missing_ok:return None
    if not line.strip():raise GateError("baseline_file_missing")
    fields=line.split("\t",1)
    if len(fields)!=2 or fields[1].strip()!=name:
        raise GateError("baseline_path_mismatch")
    mode,typ,_=fields[0].split()
    if mode not in ("100644","100755") or typ!="blob":
        raise GateError("baseline_symlink_or_submodule_denied")
    raw=git(src,"show",sha+":"+name)
    if len(raw)>65000 or b"\x00" in raw:raise GateError("source_binary_or_large")
    try:raw.decode("utf-8")
    except UnicodeDecodeError:raise GateError("non_utf8_baseline")
    return raw

def seed_workspace(src,scope,ws):
    names=set(scope.context+scope.tests+scope.writable)
    if len(names)>MAX_CONTEXT_FILES+16:raise GateError("source_count_exceeded")
    contents={};total=0
    for name in sorted(names):
        raw=read_blob(src,scope.scope.base_sha,name,missing_ok=name in scope.writable)
        if raw is None:continue
        total+=len(raw)
        if total>MAX_CONTEXT_BYTES:raise GateError("source_context_too_large")
        contents[name]=raw
    for name,raw in contents.items():
        target=ws/name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(raw)
    return contents

def node_qa(ws,tests,writable,cancel_file=None):
    if not BWRAP.is_file() or not NODE.is_file():
        raise GateError("node_runtime_missing")
    if not tests or not all(t.endswith((".test.js",".test.mjs")) for t in tests):
        raise GateError("node_tests_not_enrolled")
    flags=["--unshare-all","--new-session","--die-with-parent",
           "--ro-bind","/usr","/usr","--ro-bind","/bin","/bin",
           "--ro-bind","/lib","/lib","--ro-bind","/lib64","/lib64",
           "--dev","/dev","--proc","/proc","--tmpfs","/tmp",
           "--bind",str(ws),"/workspace","--dir","/empty",
           "--chdir","/workspace"]
    checks=[]
    for name in writable:
        if name.endswith((".js",".mjs")) and (ws/name).is_file():
            r=bounded([str(BWRAP),*flags,str(NODE),"--check",name],
                      cwd=ws,timeout=20,cancel_file=cancel_file)
            checks.append({"type":"node_syntax","file":name,"passed":r["code"]==0,
                           "diagnostic":r["stderr"][-300:]})
    r=bounded([str(BWRAP),*flags,str(NODE),"--test","--test-concurrency=1",*tests],
              cwd=ws,timeout=30,cancel_file=cancel_file)
    checks.append({"type":"node_test","passed":r["code"]==0,
                   "diagnostic":(r["stdout"]+r["stderr"])[-600:]})
    return {"qa_passed":all(c["passed"] for c in checks),
            "tests_executed":True,"checks":checks}

def exact_run(record,source,stage,task,proposer,*,cancel_file=None):
    """Trusted operator passes approved enrollment and proposer callback.

    An autonomous proposer is allowed JSON file content ONLY. It never
    chooses repository, commands, tests, mounts, base SHA, or review target.
    """
    if not re.fullmatch(r"[a-z][a-z0-9_-]{4,55}",task):
        raise GateError("task_id_invalid")
    scope=enrollment(record)
    source_verify(source,scope)
    parent=Path(stage)
    if not parent.is_absolute() or parent.is_symlink() or not parent.is_dir():
        raise GateError("stage_dir_not_trusted")
    root=parent/task
    root.mkdir(mode=0o700)  # duplicate task is fail-closed: never replay.
    ws=root/"workspace"
    ws.mkdir(mode=0o700)
    result={"task":task,"repository":scope.scope.repository,
            "base_sha":scope.scope.base_sha,"profile":scope.scope.test_profile,
            "published":False,"pushed":False,"status":"needs_review",
            "attempts":[]}
    start=time.monotonic()
    try:
        seed_workspace(source,scope,ws)
        sandbox=load("workcell_runner")
        doctor=sandbox.doctor(ws)
        if not doctor["passed"]:raise GateError("sandbox_probe_failed")
        result["sandbox"]=doctor["probe"]
        context={}
        for name in scope.context+scope.tests+scope.writable:
            file=ws/name
            if file.is_file():
                context[name]=file.read_text(encoding="utf-8")[:9000]
        prompt=("Goal: "+scope.goal+"\n"
                "Return only JSON {\"summary\":\"...\",\"files\":[{\"path\":\"...\",\"content\":\"...\"}]}.\n"
                "Allowed edits: "+", ".join(scope.writable)+"\n"
                "No new files elsewhere; no credentials, network, installs, dynamic shell or deployment.\n"
                "Trusted immutable baseline context: "+json.dumps(context,ensure_ascii=False)[:18000])
        policy=load("protocol")
        for index in range(1,MAX_ATTEMPTS+1):
            check_cancel(cancel_file)
            if time.monotonic()-start>TIME_BUDGET:raise GateError("job_time_budget_exceeded")
            try:
                raw=proposer(prompt,index)
                if isinstance(raw,str):raw=json.loads(raw)
                checked=policy.validate_proposal(scope.scope,raw)
                changed=[f["path"] for f in checked["files"]]
                if not set(changed).issubset(scope.writable):raise GateError("writable_scope_violation")
                applied=sandbox.isolated(ws,"apply",
                                         {"paths":list(scope.scope.files),"files":raw["files"]})
                if set(applied["written"])!=set(changed):raise GateError("sandbox_patch_mismatch")
                if scope.scope.test_profile=="python-unittest":
                    qa=sandbox.isolated(ws,"qa",
                                        {"paths":list(scope.scope.files),"test_profile":"python-unittest"})
                else:qa=node_qa(ws,scope.tests,scope.writable,cancel_file=cancel_file)
                result["attempts"].append({"attempt":index,"qa_passed":qa["qa_passed"]})
                if qa["qa_passed"]:
                    review=load("agent_loop").local_review(ws,changed,root/"local-review")
                    result.update(status="verified_local_review",qa=qa,review=review,
                                  proposal_hash=checked["review_sha256"])
                    break
                prompt+="\nIndependent QA failed (repair in approved files only): "+json.dumps(qa)[-650:]
            except Cancelled:raise
            except Exception as exc:
                result["attempts"].append({"attempt":index,"error_type":type(exc).__name__})
                prompt+="\nProposal rejected. Retry with exact JSON and enrolled paths only."
        if result["status"]!="verified_local_review":result["error"]="attempt_budget_exhausted"
    except Cancelled:
        result.update(status="cancelled_verified",error="owner_cancelled")
    except Exception as exc:
        result["error"]=type(exc).__name__
    finally:
        result["finished_utc"]=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
        # Stable, atomic receipt. Incomplete runs remain needs_review.
        temp=root/"receipt.json.tmp"
        temp.write_text(json.dumps(result,indent=2))
        temp.replace(root/"receipt.json")
    return result
