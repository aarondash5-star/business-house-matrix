#!/usr/bin/env python3
"""Run ONLY inside Bubblewrap /workspace; no network or host credentials."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import socket
import subprocess
import sys
import tempfile
import uuid

ROOT=Path("/workspace")
ALLOWED=("frontend","backend","tests","docs")

def path_checked(name):
    if not isinstance(name,str) or len(name)>180 or "\x00" in name:
        raise ValueError("bad_path")
    p=PurePosixPath(name)
    if (p.is_absolute() or len(p.parts)<2 or p.parts[0] not in ALLOWED or
        any(v in ("",".","..") or v.startswith(".") for v in p.parts) or
        p.suffix not in (".html",".css",".js",".json",".py",".md",".txt",".svg")):
        raise ValueError("outside_allowlist")
    cur=ROOT
    for component in p.parts:
        cur=cur/component
        if cur.is_symlink():
            raise ValueError("symlink_forbidden")
    return ROOT.joinpath(*p.parts)

def inventory():
    result=[]
    for d in ALLOWED:
        base=ROOT/d
        if base.is_symlink():
            raise ValueError("symlink_forbidden")
        if base.exists():
            for p in sorted(base.rglob("*")):
                if p.is_symlink():
                    raise ValueError("symlink_forbidden")
                if p.is_file():
                    if len(result)>=80:break
                    rel=p.relative_to(ROOT).as_posix()
                    if p.stat().st_size <= 500000:
                        result.append({"path":rel,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
                                       "size":p.stat().st_size})
    return {"files":result}

def apply_patch(data):
    files=data.get("files",[])
    if not isinstance(files,list) or not 1<=len(files)<=16:
        raise ValueError("file_count_denied")
    prepared=[]
    total=0
    seen=set()
    for item in files:
        if not isinstance(item,dict):
            raise ValueError("file_invalid")
        p=path_checked(item.get("path"))
        s=item.get("content")
        if not isinstance(s,str):
            raise ValueError("content_invalid")
        b=s.encode("utf-8")
        total+=len(b)
        if len(b)>100000 or total>300000 or p in seen:
            raise ValueError("content_exceeds_limit")
        seen.add(p)
        if p.exists():
            if not p.is_file() or item.get("expected_sha256")!=hashlib.sha256(p.read_bytes()).hexdigest():
                raise ValueError("stale_or_unapproved_overwrite")
        elif item.get("expected_sha256") not in (None,""):
            raise ValueError("new_file_sha_mismatch")
        prepared.append((p,b))
    out=[]
    for p,b in prepared:
        p.parent.mkdir(parents=True,exist_ok=True)
        if any((ROOT.joinpath(*p.relative_to(ROOT).parts[:i])).is_symlink()
               for i in range(1,len(p.relative_to(ROOT).parts))):
            raise ValueError("symlink_parent")
        tmp=p.parent/(".write-"+uuid.uuid4().hex)
        fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        try:
            with os.fdopen(fd,"wb") as f:
                f.write(b);f.flush();os.fsync(f.fileno())
            os.replace(tmp,p)
        finally:
            if tmp.exists():tmp.unlink()
        out.append({"path":p.relative_to(ROOT).as_posix(),"sha256":hashlib.sha256(b).hexdigest()})
    return {"written":out}

def probe():
    with tempfile.NamedTemporaryFile(dir=ROOT) as f:
        f.write(b"safe"); f.flush()
        can_write=Path(f.name).read_bytes()==b"safe"
    s=socket.socket()
    try:
        blocked=s.connect_ex(("1.1.1.1",53))!=0
    except OSError:
        blocked=True
    finally:s.close()
    return {"workspace_writable":can_write,
            "home_hidden":not Path("/home").exists(),
            "private_hidden":not Path("/var/lib/generic-linux-automator-exec/.ssh").exists(),
            "foreign_project_hidden":not Path("/var/lib/generic-linux-automator-exec/business-house-matrix").exists(),
            "net_blocked":blocked,
            "uid":os.getuid()}

def test():
    py=sorted((ROOT/"tests").glob("test_*.py")) if (ROOT/"tests").is_dir() else []
    js=sorted((ROOT/"tests").glob("*.test.js")) if (ROOT/"tests").is_dir() else []
    if not py and not js:
        return {"passed":False,"tests_executed":False,"error":"no_tests_found"}
    runs=[]
    if py:
        x=subprocess.run(["/usr/bin/python3","-m","unittest","discover","-s","tests","-p","test_*.py"],
                         cwd=ROOT,capture_output=True,text=True,timeout=35)
        runs.append({"kind":"python","exit":x.returncode,"output":(x.stdout+x.stderr)[-1400:]})
    if js:
        node=Path("/usr/bin/node")
        if not node.exists():
            return {"passed":False,"tests_executed":False,"error":"node_unavailable"}
        x=subprocess.run([str(node),"--test",*[str(p) for p in js]],cwd=ROOT,
                         capture_output=True,text=True,timeout=35)
        runs.append({"kind":"node","exit":x.returncode,"output":(x.stdout+x.stderr)[-1400:]})
    return {"passed":all(x["exit"]==0 for x in runs),
            "tests_executed":True,"runs":runs}

def main():
    action=sys.argv[1]
    if action=="probe":result=probe()
    elif action=="inventory":result=inventory()
    elif action=="apply":result=apply_patch(json.load(sys.stdin))
    elif action=="test":result=test()
    else:raise ValueError("unknown_action")
    print(json.dumps(result))

if __name__=="__main__":
    try:main()
    except Exception as e:
        print(json.dumps({"error":type(e).__name__,"reason":str(e)[:300]}),file=sys.stderr)
        sys.exit(2)
