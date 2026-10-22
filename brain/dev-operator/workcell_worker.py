"""Unprivileged source patch and independent QA inside a Bubblewrap capsule.

This is executed as /worker.py after the caller has unshared all namespaces and
exposed only /workspace as writable. No LLM, remote Git or host tools run here.
"""
from html.parser import HTMLParser
from static_html_policy import validate_static_html, StaticHTMLViolation
import ast
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path("/workspace")

class SemanticHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags=set()
        self.viewport=False
    def handle_starttag(self,tag,attrs):
        self.tags.add(tag)
        if tag=="meta" and dict(attrs).get("name")=="viewport":
            self.viewport=True

def relpath(name):
    if not isinstance(name,str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_./-]{0,139}",name):
        raise ValueError("path_syntax_denied")
    parts=Path(name).parts
    if name.startswith(".") or ".." in parts or any(p.startswith(".") for p in parts):
        raise ValueError("path_escape")
    target=ROOT.joinpath(*parts)
    for part in [target]+list(target.parents):
        if part.exists() and part.is_symlink():
            raise ValueError("symlink_denied")
        if part==ROOT:break
    if not target.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("outside_capsule")
    return target

def probe():
    # Network namespace is removed. These files must not exist inside capsule.
    outside_home=not Path("/home").exists() and not Path("/root").exists()
    foreign_hidden=not Path("/var/lib/generic-linux-automator-exec").exists()
    network_hidden=not Path("/run/systemd").exists()
    test=ROOT/".probe-write"
    test.write_text("ok")
    can_write=test.read_text()=="ok"
    test.unlink()
    return {"home_hidden":outside_home,"foreign_project_hidden":foreign_hidden,
            "host_service_hidden":network_hidden,"workspace_writable":can_write,
            "net_namespace":True}

def apply(data):
    paths=data["paths"]
    files=data["files"]
    if not isinstance(paths,list) or not isinstance(files,list) or len(files)>8:
        raise ValueError("apply_schema")
    enrolled=set(paths)
    if len(enrolled)!=len(paths):raise ValueError("duplicate_enrollment")
    written=[]
    for item in files:
        name=item["path"]
        if name not in enrolled or name.startswith("tests/"):
            raise ValueError("path_not_enrolled_for_write")
        target=relpath(name)
        raw=item["content"]
        if not isinstance(raw,str) or len(raw.encode("utf-8"))>32000:
            raise ValueError("source_size")
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(raw,encoding="utf-8")
        written.append(name)
    return {"written":written,"test_executed":False}

def independent_qa(data):
    paths=data["paths"]
    profile=data["test_profile"]
    if not isinstance(paths,list) or profile not in ("static-html","python-unittest","node-test"):
        raise ValueError("qa_profile_denied")
    files=[relpath(name) for name in paths]
    existing=[p for p in files if p.exists() and p.is_file() and "tests" not in p.parts]
    if not existing:raise ValueError("no_source_for_qa")
    checks=[]
    for file in existing:
        suffix=file.suffix
        src=file.read_text(encoding="utf-8")
        if suffix==".py":
            ast.parse(src,filename=str(file))
            checks.append({"type":"python_syntax","file":str(file.relative_to(ROOT)),"passed":True})
        if suffix==".html":
            parser=SemanticHTML();parser.feed(src)
            try:
                validate_static_html(src)
                ok=True
            except StaticHTMLViolation:
                ok=False
            checks.append({"type":"html_semantics_and_active_content","file":str(file.relative_to(ROOT)),"passed":ok})
    if profile=="python-unittest":
        tests=ROOT/"tests"
        if not tests.is_dir():
            raise ValueError("independent_tests_missing")
        result=subprocess.run(["/usr/bin/python3","-m","unittest","discover","-s","tests"],
                              capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=18,
                              cwd=str(ROOT),env={"PATH":"/usr/bin:/bin","HOME":"/empty"})
        checks.append({"type":"unittest","passed":result.returncode==0,
                       "result":result.stderr[-600:]})
    elif profile=="static-html":
        if not any(c["type"]=="html_semantics" for c in checks):
            raise ValueError("html_source_missing")
    else:
        # Node runtime is not pre-certified in this capsule; never claim QA success.
        raise ValueError("node_profile_not_certified")
    return {"qa_passed":len(checks)>0 and all(c["passed"] for c in checks),
            "tests_executed":True,"checks":checks}

def main():
    action=sys.argv[1]
    data=json.loads(sys.stdin.read(75000) or "{}")
    if action=="probe":out=probe()
    elif action=="apply":out=apply(data)
    elif action=="qa":out=independent_qa(data)
    else:raise ValueError("unknown_action")
    print(json.dumps(out))

if __name__=="__main__":
    try:main()
    except Exception as exc:
        print(json.dumps({"status":"blocked","error":type(exc).__name__,
                          "reason":str(exc)[:160]}),file=sys.stderr)
        sys.exit(2)
