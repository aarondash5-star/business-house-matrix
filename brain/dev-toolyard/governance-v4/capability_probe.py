#!/usr/bin/env python3
"""Evidence-grade, exact-operation *read-only* capability version probes.

No model invocation, arbitrary tool execution, tool auto-admission or billing.
A version probe establishes identity only; actual feature-level smoke evidence
and independent QA must be separately collected by the governed task.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

OPS={
 "python3":("--version",),
 "node":("--version",),
 "npm":("--version",),
 "git":("--version",),
 "ffmpeg":("-version",),
 "blender":("--version",),
 "google-chrome":("--version",),
}
ROOTS=("/usr/bin/","/usr/local/bin/","/opt/")
MAX_BINARY=250_000_000

def probe(name,which=shutil.which):
    result={"name":name,"status":"quarantined","version_probe_passed":False,
            "feature_compatibility_verified":False,"method_used":False,
            "production_enabled":False,"approved_operations":[]}
    if name not in OPS:return result | {"reason":"unknown_tool"}
    path=which(name)
    if not path:return result | {"reason":"binary_missing"}
    p=Path(path)
    if p.is_symlink() and not any(str(p).startswith(root) for root in ROOTS):
        return result | {"reason":"binary_symlink_requires_review"}
    try:
        real=p.resolve(strict=True)
        if not any(str(real).startswith(root) for root in ROOTS) or not real.is_file() or real.stat().st_size>MAX_BINARY:
            return result | {"reason":"untrusted_or_oversized_binary"}
        h=hashlib.sha256()
        with real.open("rb") as fd:
            for part in iter(lambda:fd.read(1<<20),b""):h.update(part)
        with tempfile.TemporaryDirectory(prefix="yard-capability-probe-") as home:
            env={"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":home,"LC_ALL":"C"}
            pr=subprocess.run([str(real),*OPS[name]],cwd="/",env=env,stdin=subprocess.DEVNULL,
                capture_output=True,text=True,timeout=8)
        output=(pr.stdout+pr.stderr).strip()[:800]
        if pr.returncode!=0 or not output:
            return result | {"reason":"version_probe_failed","exit_code":pr.returncode}
        return result | {"status":"identified_qa_only","version_probe_passed":True,
          "binary":str(real),"sha256":h.hexdigest(),"version_text":output,
          "operation":"version_probe_only","exit_code":pr.returncode}
    except (OSError,subprocess.TimeoutExpired,UnicodeError) as e:
        return result | {"reason":type(e).__name__}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("names",nargs="*",default=["python3","node","git"])
    args=p.parse_args()
    print(json.dumps([probe(name) for name in args.names],indent=2))
if __name__=="__main__":main()
