#!/usr/bin/env python3
"""Bounded Gate E pilot dispatch. Never modifies the certified v6 controller.

Owner-approved manifest filenames only, no arbitrary CLI command, host mount,
new repository enrollment, remote Git push, production deployment or spending.
"""
import json
import os
from pathlib import Path
import re
import sys

import gate_e_runtime as gate

HERE=Path(__file__).resolve().parent
MATRIX=Path.home()/"matrix-gate-e-stage-20261022"
REPO=MATRIX/"repo"
RUNS=MATRIX/"runs"
MODEL=Path.home()/".local/bin/matrix-pi-local"
TASK=re.compile(r"^gate-e-[a-z][a-z0-9_-]{3,48}$")

def approve_task(name):
    if not TASK.fullmatch(name):
        raise gate.GateError("task_not_approved")
    manifest=HERE/"enrollments"/(name+".json")
    if not manifest.is_file() or manifest.is_symlink():
        raise gate.GateError("manifest_not_enrolled")
    return json.loads(manifest.read_text(encoding="utf-8"))

def proposer(cancel_file):
    if not MODEL.is_file() or MODEL.is_symlink():
        raise gate.GateError("offline_model_missing")
    def propose(prompt,attempt):
        args=[str(MODEL),"--no-tools","--no-mcp","--no-extensions",
              "--no-skills","--no-prompt-templates","--no-context-files",
              "--no-session","--no-approve","--offline",
              "--model","granite4:3b","--thinking","off",
              "--system-prompt",
              "Produce ONLY valid JSON with summary and files. No markdown or shell commands.",
              "--print",prompt]
        runtime_env={"PATH":"/usr/local/bin:/usr/bin:/bin",
            "HOME":str(Path.home()),"PI_TELEMETRY":"0",
            "PI_SKIP_VERSION_CHECK":"1",
            "OLLAMA_HOST":"http://127.0.0.1:11434",
            "PYTHONDONTWRITEBYTECODE":"1"}
        outcome=gate.bounded(args,cwd=HERE,timeout=108,cancel_file=cancel_file,
                             isolated_env=runtime_env,max_output=70000)
        if outcome["code"]!=0:
            raise gate.GateError("offline_model_failed")
        raw=outcome["stdout"].strip()
        fence=chr(96)*3
        if raw.startswith(fence):
            raw=raw.partition("\n")[2].rsplit(fence,1)[0].strip()
        try:return json.loads(raw)
        except (ValueError,TypeError):
            first,last=raw.find("{"),raw.rfind("}")
            if first>=0 and last>first:return json.loads(raw[first:last+1])
            raise gate.GateError("model_json_invalid")
    return propose

def main(argv):
    if len(argv) not in (2,3):
        raise gate.GateError("usage: gate_e_operator.py <approved-task> [run|status|cancel]")
    name=argv[1]
    record=approve_task(name)
    action=argv[2] if len(argv)==3 else "status"
    if action not in ("run","status","cancel"):
        raise gate.GateError("unknown_action")
    run=RUNS/name
    if action=="status":
        receipt=run/"receipt.json"
        if receipt.is_file():return json.loads(receipt.read_text())
        return {"task":name,"status":"not_started" if not run.exists() else "needs_review",
                "published":False}
    if action=="cancel":
        # Request only. Never claim cancellation until worker receipt attests it.
        if not run.is_dir():return {"task":name,"status":"not_started"}
        receipt=run/"receipt.json"
        if receipt.is_file():return json.loads(receipt.read_text())
        (run/"owner-cancel-requested").write_text("1",encoding="ascii")
        return {"task":name,"status":"cancel_requested"}
    RUNS.mkdir(parents=True,exist_ok=True,mode=0o700)
    cancel=RUNS/name/"owner-cancel-requested"
    return gate.exact_run(record,REPO,RUNS,name,proposer(cancel),cancel_file=cancel)

if __name__=="__main__":
    try:
        print(json.dumps(main(sys.argv),sort_keys=True))
    except Exception as exc:
        print(json.dumps({"status":"blocked","reason":type(exc).__name__}))
        sys.exit(2)
