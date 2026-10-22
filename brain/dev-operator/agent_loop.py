#!/usr/bin/env python3
"""Bounded, offline, policy-enrolled coding task runner. No model-selected host tools."""
import importlib.util
import json
import re
from pathlib import Path
import subprocess
import sys
import time

HERE=Path(__file__).resolve().parent
HOME=Path.home()/"matrix-controller"
SOURCE=HOME/"release-stage-general-dev-20261022"/"repo"
RUNS=HOME/"release-stage-general-dev-20261022"/"runs"
MODEL=Path.home()/".local/bin/matrix-pi-local"
REPOSITORY="aarondash5-star/business-house-matrix"
ATTEMPTS=3

def load(name):
    spec=importlib.util.spec_from_file_location("dev_"+name,HERE/(name+".py"))
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module
    spec.loader.exec_module(module);return module

def git(argv,cwd):
    p=subprocess.run(["/usr/bin/git","-c","core.hooksPath=/dev/null",*argv],
                     cwd=str(cwd),capture_output=True,text=True,input="",timeout=20,
                     env={"PATH":"/usr/bin:/bin","HOME":str(Path.home()),
                          "GIT_TERMINAL_PROMPT":"0","GIT_CONFIG_NOSYSTEM":"1",
                          "GIT_CONFIG_GLOBAL":"/dev/null"})
    if p.returncode:raise RuntimeError("git_operation_failed")
    return p.stdout.strip()

def inference(prompt, single_html_path=None):
    args=[str(MODEL),"--no-tools","--no-mcp","--no-extensions","--no-skills",
        "--no-prompt-templates","--no-context-files","--no-session",
        "--no-approve","--offline","--model","qwen3:4b-instruct","--thinking","off",
        "--system-prompt","Output only exact JSON. No markdown.","--print",prompt]
    p=subprocess.run(args,input="",capture_output=True,text=True,timeout=110,
        env={"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":str(Path.home()),
             "PI_TELEMETRY":"0","PI_SKIP_VERSION_CHECK":"1",
             "OLLAMA_HOST":"http://127.0.0.1:11434"})
    if p.returncode or len(p.stdout)>72000:raise RuntimeError("model_output_unavailable")
    raw=p.stdout.strip();fence=chr(96)*3
    if raw.startswith(fence):raw=raw.partition("\n")[2].rsplit(fence,1)[0].strip()
    if single_html_path is not None:
        return parse_single_html(raw,single_html_path)
    try:return json.loads(raw)
    except ValueError:
        a,z=raw.find("{"),raw.rfind("}")
        if a>=0 and z>a:return json.loads(raw[a:z+1])
        raise ValueError("model_schema_invalid")

def parse_single_html(text,allowed_path):
    """Single-file HTML output: no fragile JSON escaping or model-selected path."""
    if not allowed_path.endswith(".html"):
        raise ValueError("single_file_html_scope")
    m=re.search(r"(?is)<!doctype\\s+html.*?</html\\s*>",text)
    if not m:
        raise ValueError("complete_html_document_missing")
    html=m.group(0)
    if len(html.encode("utf-8"))>32000:
        raise ValueError("html_output_too_large")
    if re.search(r"(?is)<script\\b|<iframe\\b|https?://|\\b(?:fetch|xmlhttprequest)\\s*\\(",html):
        raise ValueError("unreviewed_active_content")
    return {"summary":"Generated offline static developer preview",
            "files":[{"path":allowed_path,"content":html}]}

def local_review(workspace,files,target):
    target.mkdir(mode=0o700)
    git(["init","-q"],target)
    for name in files:
        src=workspace/name;dst=target/name
        dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_bytes(src.read_bytes())
    git(["add","--",*files],target)
    p=subprocess.run(["/usr/bin/git","-c","core.hooksPath=/dev/null",
        "-c","user.name=Matrix Dev Review",
        "-c","user.email=dev-review@example.invalid",
        "commit","-q","-m","review: verified local agent code"],cwd=str(target),
        capture_output=True,text=True,timeout=15,
        env={"PATH":"/usr/bin:/bin","HOME":str(Path.home()),"GIT_CONFIG_NOSYSTEM":"1",
             "GIT_CONFIG_GLOBAL":"/dev/null"})
    if p.returncode:raise RuntimeError("review_commit_failure")
    sha=git(["rev-parse","HEAD"],target)
    if set(git(["ls-files"],target).splitlines())!=set(files):
        raise RuntimeError("review_file_set_mismatch")
    return {"commit":sha,"files":files,"path":str(target),
            "published":False,"pushed":False}

def run(task):
    policy=load("protocol");cell=load("workcell_runner")
    path=HERE/"enrollments"/(task+".json")
    if not path.is_file() or path.is_symlink():raise ValueError("unapproved_task")
    spec=json.loads(path.read_text())
    if set(spec)!={"manifest","goal"} or not isinstance(spec["goal"],str):
        raise ValueError("enrollment_schema_invalid")
    if not 12<=len(spec["goal"])<=800:raise ValueError("goal_size_invalid")
    scope=policy.enroll(spec["manifest"])
    if scope.repository!=REPOSITORY:raise ValueError("repository_not_enrolled")
    if git(["remote","get-url","origin"],SOURCE)!="https://github.com/"+scope.repository+".git":
        raise RuntimeError("source_repo_mismatch")
    git(["cat-file","-e",scope.base_sha+"^{commit}"],SOURCE)
    RUNS.mkdir(mode=0o700,parents=True,exist_ok=True)
    root=RUNS/task
    if root.exists():raise RuntimeError("already_attempted_no_replay")
    root.mkdir(mode=0o700)
    ws=root/"workspace";ws.mkdir(mode=0o700)
    record={"task":task,"project":scope.project,"base_sha":scope.base_sha,
            "published":False,"model_tools":False,"paid":False,
            "status":"blocked","attempts":[]}
    try:
        check=cell.doctor(ws)
        if check["passed"] is not True:raise RuntimeError("sandbox_probe_failed")
        record["sandbox"]=check["probe"]
        allowed=[x for x in scope.files if not x.startswith("tests/")]
        single_html=(len(allowed)==1 and allowed[0].endswith(".html"))
        if single_html:
            prompt=("Build this original, offline public developer prototype: "+spec["goal"]
                    +"\nReturn only one COMPLETE HTML5 document, starting with <!doctype html> "
                    +"and ending with </html>. Do NOT use JSON, markdown or explanations. "
                    +"Include <html lang='en'>, viewport meta and <main>. "
                    +"Use self-contained responsive inline CSS, no JavaScript, external URLs, "
                    +"CDNs, dependencies, credential values, accounts, browser storage or forms. "
                    +"Keep the page under 2500 characters.")
        else:
            prompt=("Implement this public prototype: "+spec["goal"]
                    +"\nReturn ONLY compact JSON with exactly summary and files; "
                    +"files elements contain path and content strings. "
                    +"Use approved paths only: "+", ".join(allowed)
                    +". Keep code short and offline; no credentials or external endpoints.")
        for index in range(1,ATTEMPTS+1):
            try:
                proposed=inference(prompt,allowed[0] if single_html else None)
                checked=policy.validate_proposal(scope,proposed)
                changed=[f["path"] for f in checked["files"]]
                outcome=cell.isolated(ws,"apply",
                       {"paths":list(scope.files),"files":proposed["files"]})
                if set(outcome.get("written",[]))!=set(changed):
                    raise RuntimeError("sandbox_written_paths_mismatch")
                qa=cell.isolated(ws,"qa",
                         {"paths":list(scope.files),"test_profile":scope.test_profile})
                record["attempts"].append({"attempt":index,"validated":True,
                                            "qa_passed":qa["qa_passed"]})
                if qa["qa_passed"] is True and qa["tests_executed"] is True:
                    review=local_review(ws,changed,root/"local-review")
                    record.update(status="verified_local_review",qa=qa,review=review,
                                  review_sha256=checked["review_sha256"])
                    break
                prompt += "\nIndependent tests failed; repair within same files: "+json.dumps(qa)[-700:]
            except Exception as exc:
                record["attempts"].append({"attempt":index,"validated":False,
                                           "error_type":type(exc).__name__})
                if index==ATTEMPTS:raise
                prompt += ("\nReturn one complete raw HTML document only." if single_html else "\nReturn exact JSON schema and approved paths.")
        if record["status"]!="verified_local_review":raise RuntimeError("qa_retry_exhausted")
    except Exception as exc:
        record["error"]={"type":type(exc).__name__,"message":str(exc)[:120]}
    record["completed_utc"]=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime())
    (root/"receipt.json").write_text(json.dumps(record,indent=2))
    return record

if __name__=="__main__":
    if len(sys.argv)!=2 or not re.fullmatch(r"[a-z][a-z0-9_-]{3,55}",sys.argv[1]):
        print(json.dumps({"status":"blocked","reason":"unapproved_task"}));sys.exit(2)
    try:
        record=run(sys.argv[1])
        print(json.dumps({"status":record["status"],"task":record["task"],
               "local_commit":(record.get("review") or {}).get("commit"),
               "attempts":record.get("attempts"),"error":record.get("error")}))
        sys.exit(0 if record["status"]=="verified_local_review" else 2)
    except Exception as exc:
        print(json.dumps({"status":"blocked","error_type":type(exc).__name__}))
        sys.exit(2)
