#!/usr/bin/env python3
"""Brain-direct development: model edits files, offline tests, revises and submits receipts.

No subordinate agents/workers. No shell tool, root, network test runner, git push,
production write, WordPress, guest data or permissions bypass. Standalone and
experimental; it does not modify the existing proposal-only service or v6.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import time
import urllib.request

ROOT = Path.home() / ".local/share/business-house-matrix/brain-direct"
MODEL_URL = "http://127.0.0.1:11434/api/generate"
EXT = {".html", ".css", ".js", ".cjs", ".mjs", ".json", ".svg", ".md", ".txt"}
BIN = {"node", "python3"}

class GateError(ValueError):
    pass

def validate(m):
    if not isinstance(m, dict) or m.get("schema") != 1:
        raise GateError("manifest_schema")
    if m.get("mode") != "brain_direct_only" or m.get("workers_allowed") is not False:
        raise GateError("worker_execution_not_authorized")
    if not isinstance(m.get("task_id"), str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{3,60}", m["task_id"]):
        raise GateError("task_id")
    if not isinstance(m.get("brief"), str) or not 80 <= len(m["brief"]) <= 9000:
        raise GateError("brief")
    prefixes = m.get("editable")
    if not isinstance(prefixes, list) or not prefixes or len(prefixes) > 8:
        raise GateError("editable_prefixes")
    if len(set(prefixes)) != len(prefixes) or any(not isinstance(p, str) or
            not re.fullmatch(r"[a-z][a-z0-9_-]{1,24}/", p) for p in prefixes):
        raise GateError("unsafe_editable_prefix")
    tests = m.get("tests")
    if not isinstance(tests, list) or not tests or len(tests) > 10:
        raise GateError("tests_required")
    if any(not isinstance(cmd, list) or len(cmd) < 2 or len(cmd) > 9 or
           cmd[0] not in BIN or
           any(not isinstance(x, str) or not re.fullmatch(r"[a-zA-Z0-9_.\-/]+", x) for x in cmd[1:])
           for cmd in tests):
        raise GateError("unsafe_test_command")
    if any(any(flag in cmd for flag in ("-c","-e","--eval","--require","--loader","--inspect","--import")) for cmd in tests):
        raise GateError("inline_test_execution_denied")
    if not isinstance(m.get("max_steps"), int) or not 5 <= m["max_steps"] <= 150:
        raise GateError("step_budget")
    if not isinstance(m.get("model"), str) or not re.fullmatch(r"[a-zA-Z0-9_:/.-]{2,75}", m["model"]):
        raise GateError("model")
    if m.get("publish") or m.get("merge") or m.get("spend") or m.get("permissions"):
        raise GateError("production_rights_denied")
    return m

def path_for(w, name, m, read_only=False):
    if name == "index.html" and read_only:
        return w / name
    if not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9_./-]{3,160}", name):
        raise GateError("invalid_path")
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts or any(x.startswith(".") for x in p.parts):
        raise GateError("path_escape")
    if p.suffix not in EXT or not any(name.startswith(prefix) for prefix in m["editable"]):
        raise GateError("scope_violation")
    c = w
    for part in p.parts:
        c = c / part
        if c.is_symlink():
            raise GateError("symlink_denied")
    if not c.resolve(strict=False).is_relative_to(w.resolve()):
        raise GateError("path_escape")
    return c

def put(w, name, content, m):
    p = path_for(w, name, m)
    if not isinstance(content, str) or not 1 <= len(content.encode()) <= 170000:
        raise GateError("bad_file_size")
    p.parent.mkdir(parents=True, exist_ok=True)
    temporary = p.with_name(p.name + ".candidate")
    if temporary.exists() or temporary.is_symlink():
        raise GateError("temporary_file_collision")
    with temporary.open("x", encoding="utf8") as f:
        f.write(content)
    temporary.replace(p)
    return {"file":name,"sha256":hashlib.sha256(content.encode()).hexdigest()}

def read(w, name, m):
    p=path_for(w, name, m, read_only=True)
    if p.is_symlink() or not p.is_file():
        raise GateError("file_not_found")
    with p.open("rb") as h:
        data=h.read(32001)
    return {"file":name,"text":data[:32000].decode("utf8","replace"),
            "truncated":len(data)>32000}

def sandbox(w, commands):
    bwrap=shutil.which("bwrap")
    if not bwrap:
        raise GateError("bubblewrap_missing_no_unsandboxed_fallback")
    prefix=[bwrap,"--die-with-parent","--new-session","--unshare-all"]
    for folder in ("/usr","/bin","/lib","/lib64"):
        if Path(folder).exists():
            prefix.extend(("--ro-bind",folder,folder))
    prefix+=["--proc","/proc","--dev","/dev","--tmpfs","/tmp",
             "--ro-bind",str(w),"/work","--chdir","/work",
             "--setenv","HOME","/tmp","--setenv","PATH","/usr/bin:/bin",
             "--setenv","CI","1","--"]
    evidence=[]
    for command in commands:
        try:
            p=subprocess.run(prefix+command,stdin=subprocess.DEVNULL,
                             text=True,capture_output=True,timeout=75,
                             env={"PATH":"/usr/bin:/bin","HOME":"/tmp"})
            entry={"argv":command,"exit":p.returncode,
                   "stdout":p.stdout[-1600:],"stderr":p.stderr[-1600:]}
        except subprocess.TimeoutExpired:
            entry={"argv":command,"exit":124,"stderr":"timeout"}
        evidence.append(entry)
        if entry["exit"]!=0:
            break
    return {"passed":len(evidence)==len(commands) and all(e["exit"]==0 for e in evidence),
            "isolated":True,"network":"disabled","evidence":evidence}

def model_action(m, history):
    instruction=("You are the Dev Matrix Brain author. Build a complete genuine static "
      "Andaz Vibe Stay website and booking UI. Own the implementation directly, "
      "without delegating to workers. Reply ONLY one JSON action: "
      '{"action":"list"} or {"action":"read","path":"index.html"} or '
      '{"action":"write","path":"site/index.html","content":"FULL FILE"} or '
      '{"action":"test"} or {"action":"finish","summary":"..."} . '
      "Write full real source files, include responsive design, booking states, "
      "date/guest validation and honest no-live-PMS enquiry fallback. "
      "Do not claim booking/payment confirmation or fake inventory. "
      "Use only permitted paths and run tests after final edits. "
      "Study test failures and revise. No shell, tools, remote workers or Git push.\n"
      "Brief: "+m["brief"]+"\nObservations: "+json.dumps(history[-7:])[-10000:])
    request=urllib.request.Request(MODEL_URL,
      json.dumps({"model":m["model"],"prompt":instruction,"stream":False,
                  "format":"json","options":{"temperature":0.1,"num_predict":12000}}).encode(),
      {"Content-Type":"application/json"})
    with urllib.request.urlopen(request,timeout=360) as response:
        if response.status!=200:
            raise GateError("model_status")
        data=response.read(850001)
    if len(data)>850000:
        raise GateError("model_response_too_large")
    env=json.loads(data)
    if env.get("model") not in (m["model"],m["model"]+":latest"):
        raise GateError("model_identity")
    action=json.loads(env.get("response",""))
    if not isinstance(action,dict):
        raise GateError("model_action_type")
    return action

def run(w,m,agent=model_action,tester=sandbox):
    w=w.resolve(strict=True)
    if not w.is_dir() or w.parent!=ROOT.expanduser().resolve() or w.name!=m["task_id"]:
        raise GateError("workspace_not_enrolled")
    state=w/".brain-run.json"
    log=w/".brain-events.jsonl"
    if state.exists() or log.exists():
        raise GateError("repeat_run_requires_owner_review")
    revision=0
    passed_at=-1
    history=[]
    def receipt(status,**details):
        result={"status":status,"task_id":m["task_id"],"revision":revision,
                "last_tested_revision":passed_at,"worker_invoked":False,
                "pushed":False,"published":False,**details}
        temporary=w/".brain-run.tmp"
        temporary.write_text(json.dumps(result,indent=2))
        temporary.replace(state)
        return result
    receipt("running")
    started=time.monotonic()
    for i in range(m["max_steps"]):
        if time.monotonic()-started>3*3600:
            return receipt("blocked",reason="time_budget")
        try:
            action=agent(m,history)
            kind=action.get("action")
            if kind=="list" and set(action)=={"action"}:
                files=[]
                for prefix in m["editable"]:
                    directory=w/prefix
                    if directory.is_dir():
                        files += [p.relative_to(w).as_posix() for p in directory.rglob("*")
                                  if p.is_file() and not p.is_symlink()]
                response={"files":sorted(files)[:80]+(["index.html"])}
            elif kind=="read" and set(action)=={"action","path"}:
                response=read(w,action["path"],m)
            elif kind=="write" and set(action)=={"action","path","content"}:
                response=put(w,action["path"],action["content"],m)
                revision+=1
                passed_at=-1
            elif kind=="test" and set(action)=={"action"}:
                response=tester(w,m["tests"])
                if response["passed"] is True:
                    passed_at=revision
            elif kind=="finish" and set(action)=={"action","summary"}:
                if revision>0 and passed_at==revision and isinstance(action["summary"],str):
                    return receipt("review_ready",steps=i+1,
                                   summary=action["summary"][:700],
                                   evidence="offline_tests_passed")
                response={"rejected":"no_passing_tests_at_current_revision"}
            else:
                response={"rejected":"unapproved_action"}
        except (ValueError,KeyError,TypeError,TimeoutError,OSError) as exc:
            response={"rejected":type(exc).__name__+":"+str(exc)[:140]}
        logitem={"step":i+1,"action":action.get("action") if "action" in locals() else "unknown",
                 "result":{k:v for k,v in response.items() if k!="text"}}
        with log.open("a") as f:
            f.write(json.dumps(logitem)+"\n")
        history.append(logitem)
        if i%5==4:
            receipt("running",steps=i+1)
    return receipt("blocked",reason="step_budget_exhausted",steps=m["max_steps"])

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("mode",choices=["run","status"])
    parser.add_argument("--manifest",required=True)
    args=parser.parse_args()
    m=validate(json.loads(Path(args.manifest).read_text()))
    w=ROOT.expanduser()/m["task_id"]
    if args.mode=="status":
        f=w/".brain-run.json"
        print(f.read_text() if f.exists() else json.dumps({"status":"not_started"}))
    else:
        print(json.dumps(run(w,m)))
if __name__=="__main__":
    try:
        main()
    except (GateError,OSError,ValueError) as exc:
        print(json.dumps({"status":"blocked","reason":str(exc),"workers_invoked":False}))
        sys.exit(2)
