#!/usr/bin/env python3
"""Rootless, container-isolated test runner for staged Python candidates.

A job MUST have test_*.py unit tests. Syntax-only or model-written review is
never treated as QA success. No host code exec, no network, no writes, no sudo.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid

ROOT=Path("/var/lib/generic-linux-automator-exec/matrix-controller")
INBOX=ROOT/"sandbox-inbox"
RECEIPTS=ROOT/"sandbox-receipts"
IMAGE="docker.io/library/python:3.12-alpine"
MAX_FILES=12
MAX_TOTAL=256000
CMD_TIMEOUT=48

def check(batch):
    if not isinstance(batch,str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,47}",batch):
        raise ValueError("Safe sandbox batch ID required")
    src=INBOX/batch
    if not src.is_dir() or src.is_symlink():
        raise ValueError("No approved test batch directory")
    allfiles=list(src.iterdir())
    if not allfiles or len(allfiles)>MAX_FILES:
        raise ValueError("Batch needs 1-12 Python files")
    total=0; tests=0
    for f in allfiles:
        if not f.is_file() or f.is_symlink() or f.suffix!=".py" or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{0,70}\.py",f.name):
            raise ValueError("Only regular Python source/test files allowed")
        total+=f.stat().st_size
        if f.name.startswith("test_"): tests+=1
    if not tests:raise ValueError("Independent test_*.py required")
    if total>MAX_TOTAL or total<20:
        raise ValueError("Source batch total size out of bounds")
    return src,{"files":len(allfiles),"test_files":tests,"total_bytes":total}

def run(batch):
    src,meta=check(batch)
    RECEIPTS.mkdir(mode=0o700,parents=True,exist_ok=True)
    # The full source batch fingerprint makes replay safe without duplicate execution.
    h=hashlib.sha256()
    for f in sorted(src.iterdir()):
        h.update(f.name.encode("utf-8"));h.update(f.read_bytes())
    digest=h.hexdigest()
    dest=RECEIPTS/(batch+".json")
    if dest.exists():
        cached=json.loads(dest.read_text())
        if cached.get("source_sha256")==digest:
            return {**cached,"idempotent_receipt_reused":True}
        raise ValueError("QA receipt exists for changed source; use new batch ID")
    name="bhm-qa-"+uuid.uuid4().hex[:12]
    cmd=[
      "/usr/bin/podman","run","--rm","--name",name,
      "--pull=never","--network=none","--read-only",
      "--cap-drop=all","--security-opt=no-new-privileges",
      "--pids-limit=64","--memory=268435456","--cpus=0.75",
      "--tmpfs=/tmp:rw,noexec,nosuid,size=32m,mode=1777",
      "-v",str(src)+":/workspace:ro",
      "--workdir=/workspace","--user=65534:65534",
      IMAGE,"python","-m","unittest","discover",
      "-s","/workspace","-p","test_*.py","-v"
    ]
    started=time.monotonic()
    try:
        r=subprocess.run(cmd,stdin=subprocess.DEVNULL,capture_output=True,text=True,
                         timeout=CMD_TIMEOUT)
        output=(r.stdout+"\n"+r.stderr)[-10000:]
        tests_observed=bool(re.search(r"Ran [1-9][0-9]* test",output))
        qa_ok=(r.returncode==0 and tests_observed and
               ("OK" in output) and "FAILED" not in output)
        status="tests_passed" if qa_ok else "tests_failed"
    except subprocess.TimeoutExpired:
        subprocess.run(["/usr/bin/podman","rm","-f",name],
                       stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=15)
        status="timeout";output="Sandbox exceeded 48 second timeout and was stopped"
        qa_ok=False
    result={"batch_id":batch,"status":status,"qa_passed":qa_ok,
            "mode":"rootless_podman_no_network_read_only",
            "files":meta["files"],"test_files":meta["test_files"],
            "source_sha256":digest,
            "elapsed_seconds":round(time.monotonic()-started,2),
            "output_tail":output[:10000],
            "tests_executed":True,"source_modified":False,
            "repository_changed":False,"publish_allowed":False,
            "paid_access":False}
    temp=RECEIPTS/(batch+".next")
    if dest.exists():raise ValueError("Concurrent QA result exists; preserve immutable receipt")
    with temp.open("x") as f:
        json.dump(result,f,indent=2);f.flush();os.fsync(f.fileno())
    temp.chmod(0o600);temp.replace(dest)
    return result

def selftest():
    for bad in ("../../", "/tmp", "", "bad batch", "a"*55):
        try:check(bad)
        except ValueError:pass
        else:raise AssertionError("Unsafe path allowed")
    return {"passed":True,"test":"batch path safety","scope":"no code executed"}

def main():
    parser=argparse.ArgumentParser()
    subs=parser.add_subparsers(dest="op",required=True)
    r=subs.add_parser("run");r.add_argument("batch")
    subs.add_parser("selftest")
    a=parser.parse_args()
    val=run(a.batch) if a.op=="run" else selftest()
    print(json.dumps(val,indent=2))
if __name__=="__main__":
    try:main()
    except (RuntimeError,ValueError,OSError) as e:
        print("QA_ERROR",type(e).__name__,str(e)[:180],file=sys.stderr)
        sys.exit(2)
