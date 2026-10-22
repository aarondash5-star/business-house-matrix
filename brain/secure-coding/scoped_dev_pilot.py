#!/usr/bin/env python3
"""Pine synthetic-only autonomous coding pilot. No SSH, repo push, cloud deploy or shell tools for model."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid

HERE=Path(__file__).resolve().parent
WORKSPACE_KEY="pine_mcp_chat"
WORK_IDS={
 "pine_ui_accessibility_node_retest_v1":(
  "Build a small standalone accessible mobile-first Pine Engineer CHAT DEMO "
  "with clear user and assistant messages, keyboard send and new-chat reset, "
  "and independent Python unittest checks. Synthetic only; no network or real MCP/trading."
 ),
 "pine_ui_accessibility_v1":(
  "Build a small standalone accessible mobile-first Pine Engineer CHAT DEMO "
  "with clear user and assistant messages, keyboard send and new-chat reset, "
  "and an independent Python unittest test of source markup/semantics. "
  "Only synthetic data; no external requests, account data, shell, real MCP or trading."
 )
}
BWRAP=HERE/"reviewed_patch_runner.py"
MODEL=Path.home()/".local/bin/matrix-pi-local"
STATE=HERE/"autonomous-code-state"
WORKSPACE=Path.home()/".local/share/matrix-code-executor/pine_mcp_chat"
ROOTS=("frontend/","backend/","tests/","docs/")
MAX_SOURCE=200000
BLOCKED=(r"\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(",
 r"\b(?:subprocess|os\.system|os\.popen)\s*\(",r"\b(?:eval|exec)\s*\(",
 r"\b(?:password|api[_-]?key|bearer|private.?key|service_role)\b",
 r"<script\b[^>]*\bsrc=", r"\bhttps?://", r"\b(?:localStorage|sessionStorage)\b")

def restricted_files(value):
    if not isinstance(value,dict):raise ValueError("bad_proposal")
    items=value.get("files")
    if not isinstance(items,list) or not 2<=len(items)<=12:raise ValueError("bad_file_count")
    have_test=False
    seen=set()
    total=0
    for item in items:
        if not isinstance(item,dict):raise ValueError("file_shape")
        path=item.get("path")
        txt=item.get("content")
        if not isinstance(path,str) or not path.startswith(ROOTS):raise ValueError("path_not_allowed")
        if path in seen or ".." in path or any(part.startswith(".") for part in path.split("/")):
            raise ValueError("unsafe_or_duplicate_path")
        if not isinstance(txt,str) or len(txt)<8:raise ValueError("empty_source")
        if path.endswith(".py") and path.startswith("tests/test_"):have_test=True
        if any(re.search(pattern,txt,re.I) for pattern in BLOCKED):raise ValueError("forbidden_source_pattern")
        total+=len(txt.encode())
        seen.add(path)
        if total>MAX_SOURCE:raise ValueError("too_large")
        existing=WORKSPACE/path
        if existing.exists() and not existing.is_symlink() and existing.is_file():
            item["expected_sha256"]=hashlib.sha256(existing.read_bytes()).hexdigest()
        else:item["expected_sha256"]=None
    if not have_test:raise ValueError("independent_test_required")
    return {"files":items}

def parse_model(output):
    text=output.strip()
    fence=chr(96)*3
    if text.startswith(fence):
        text=text.partition("\n")[2].rsplit(fence,1)[0]
    try:return json.loads(text)
    except json.JSONDecodeError:
        a=text.find("{"); b=text.rfind("}")
        if a<0 or b<a:raise ValueError("model_not_json")
        return json.loads(text[a:b+1])

def isolated(action,patch=None):
    args=[sys.executable,str(BWRAP),action,"--project",WORKSPACE_KEY]
    if patch:args.extend(["--patch",str(patch)])
    p=subprocess.run(args,capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=60)
    if p.returncode:raise RuntimeError("sandbox_gate_failed:"+(p.stdout+p.stderr)[-450:])
    return json.loads(p.stdout)

def propose(prompt,seconds=130):
    cmd=[str(MODEL),"--no-tools","--no-mcp","--no-extensions",
        "--no-skills","--no-context-files","--no-session","--offline","--print",prompt]
    env={"HOME":str(Path.home()),"PATH":"/usr/local/bin:/usr/bin:/bin",
         "PI_TELEMETRY":"0","PI_SKIP_VERSION_CHECK":"1",
         "OLLAMA_HOST":"http://127.0.0.1:11434"}
    p=subprocess.run(cmd,capture_output=True,text=True,stdin=subprocess.DEVNULL,
                     timeout=seconds,env=env,check=False)
    if p.returncode:raise RuntimeError("local_model_failed:"+str(p.returncode)+(p.stderr or "")[-250:])
    return restricted_files(parse_model(p.stdout))

def local_review(work_id,files,qa):
    review_root=STATE/"reviews"/work_id
    if review_root.exists():raise ValueError("review_artifact_exists")
    review_root.mkdir(mode=0o700,parents=True)
    for item in files:
        src=WORKSPACE/item["path"]
        if src.is_symlink() or not src.is_file():raise RuntimeError("staged_symlink_or_missing")
        content=src.read_bytes()
        if hashlib.sha256(content).hexdigest()!=item["sha256"]:raise RuntimeError("staged_sha_changed")
        target=review_root/item["path"]
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(content)
    env={"PATH":"/usr/bin:/bin","HOME":"/nonexistent",
         "GIT_CONFIG_NOSYSTEM":"1","GIT_CONFIG_GLOBAL":"/dev/null",
         "GIT_CONFIG_SYSTEM":"/dev/null"}
    cmds=[
      ["git","-c","core.hooksPath=/dev/null","init","--initial-branch=review",str(review_root)],
      ["git","-C",str(review_root),"-c","core.hooksPath=/dev/null","add","--"]+[x["path"] for x in files],
      ["git","-C",str(review_root),"-c","core.hooksPath=/dev/null",
       "-c","user.name=Dell Dev Matrix","-c","user.email=matrix-synthetic@localhost",
       "commit","-m","review(pine): offline synthetic coding pilot"]
    ]
    for cmd in cmds:
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=20,env=env)
        if p.returncode:raise RuntimeError("local_review_git_failed:"+p.stderr[-350:])
    p=subprocess.run(["git","-C",str(review_root),"rev-parse","HEAD"],
                     text=True,capture_output=True,timeout=8,env=env,check=True)
    return {"commit":p.stdout.strip(),"review_path":str(review_root),
            "files":[x["path"] for x in files],"published":False,"qa":qa}

def run(work_id):
    if work_id not in WORK_IDS:raise ValueError("work_id_not_enrolled")
    STATE.mkdir(mode=0o700,parents=True,exist_ok=True)
    state=STATE/work_id
    if state.is_symlink():raise ValueError("state_symlink_denied")
    if state.exists():raise ValueError("work_already_attempted_do_not_replay")
    state.mkdir(mode=0o700)
    attempts=[]
    def record(status,extra):
        result={"task":work_id,"project":WORKSPACE_KEY,"status":status,
           "attempts":attempts,"extra":extra,"created_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
           "autopublish":False,"spend":False,"private_pine_access":False}
        (state/"receipt.json").write_text(json.dumps(result,indent=2))
        return result
    try:
        health=isolated("doctor")
        if not health.get("passed"):raise RuntimeError("security_gate_failed")
        inv=isolated("inventory")
        failure=""
        for idx in range(2):
            prompt=(
             "Reply ONLY with JSON object {\"files\":[{\"path\":\"frontend/dev-pilot.html\","
             "\"content\":\"...\"},{\"path\":\"tests/test_dev_pilot.py\",\"content\":\"...\"}]}. "
             "Write complete functional public SYNTHETIC code only. Do not use source imports,"
             "network requests, credentials, real Pine/trading endpoints, browser storage, shell commands,"
             "or external libraries. Include test_* unittest methods in tests/test_dev_pilot.py."
             "Allowed dirs frontend/,backend/,tests/,docs/. Use minimal self-contained HTML/CSS/JS."
             " The task is "+WORK_IDS[work_id]+". Existing files (avoid overwriting): "+
             json.dumps(inv.get("files",[]))[:1600]+". Previous QA failure: "+failure[:500]
            )
            patch=propose(prompt)
            patchpath=state/("patch-%d.json"%(idx+1))
            patchpath.write_text(json.dumps(patch))
            changed=isolated("apply",patchpath)
            qa=isolated("test")
            a={"iteration":idx+1,"changed":changed.get("written",[]),"passed":qa.get("passed",False),
               "tests_executed":qa.get("tests_executed",False),"test_evidence":qa.get("runs",[])}
            attempts.append(a)
            if qa.get("passed") and qa.get("tests_executed"):
                result=local_review(work_id,changed["written"],qa)
                return record("verified_local_review",result)
            failure=json.dumps(qa)[-900:]
        return record("qa_needs_review",{"reason":"bounded_retries_exhausted"})
    except Exception as e:
        return record("blocked",{"error":type(e).__name__,"detail":str(e)[:450]})

def main():
    p=argparse.ArgumentParser()
    p.add_argument("action",choices=["doctor","status","run"])
    p.add_argument("work_id",choices=sorted(WORK_IDS))
    a=p.parse_args()
    if a.action=="doctor":
        print(json.dumps({"work_id":a.work_id,"sandbox":isolated("doctor"),"model":MODEL.is_file(),"workspaces":list(ROOTS)}))
    elif a.action=="status":
        receipt=STATE/a.work_id/"receipt.json"
        print(receipt.read_text() if receipt.exists() else json.dumps({"status":"not_run"}))
    else:print(json.dumps(run(a.work_id)))
if __name__=="__main__":
    try:main()
    except Exception as e:
        print(json.dumps({"status":"blocked","error":type(e).__name__,"detail":str(e)[:450]}))
        sys.exit(1)
