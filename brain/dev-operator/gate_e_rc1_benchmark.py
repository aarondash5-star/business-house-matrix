#!/usr/bin/env python3
"""RC1 public-source model benchmark launcher. Never touches certified v6.

Runs only the two independently owner-enrolled, immutable, non-sensitive
benchmarks; offline local model; no Git push, deployment, private mounts,
dynamic shell, or automatic retry. One terminal receipt per unique task.
"""
import json
import time
from pathlib import Path
import sys

import gate_e_operator as operator
import gate_e_runtime as gate

MATRIX=Path.home()/"matrix-gate-e-rc1-model-20261023"
SOURCE=MATRIX/"repo"
RUNS=MATRIX/"runs"
ALLOWED={"gate-e-rc1-node","gate-e-rc1-python","gate-e-rc1-node-json"}

def main(name):
    if name not in ALLOWED:
        raise gate.GateError("benchmark_not_owner_approved")
    if not operator.MODEL.is_file():
        raise gate.GateError("model_missing")
    record=operator.approve_task(name)
    if record["manifest"]["repository"]!="aarondash5-star/business-house-matrix":
        raise gate.GateError("source_scope_mismatch")
    if record["manifest"]["base_sha"]!="fbcea95fd22218aabc5a03be48811b23aa15cc66":
        raise gate.GateError("base_sha_mismatch")
    RUNS.mkdir(parents=True,exist_ok=True,mode=0o700)
    if (RUNS/name).exists():
        raise gate.GateError("completed_or_ambiguous_task_not_replayed")
    cancel=RUNS/name/"owner-cancel-requested"
    def limited_local_model(prompt,attempt):
        remaining=getattr(limited_local_model,"gate_e_deadline",time.monotonic()+110)-time.monotonic()
        if remaining<=0:
            raise gate.GateError("job_time_budget_exceeded")
        outcome=gate.bounded([sys.executable,"-B",str(Path(__file__).with_name("gate_e_rc1_ollama.py"))],
                             cwd=Path(__file__).resolve().parent,
                             input_text=prompt,timeout=min(105,remaining),
                             cancel_file=cancel,max_output=35000,
                             isolated_env={"PATH":"/usr/bin:/bin","HOME":"/empty",
                                           "PYTHONDONTWRITEBYTECODE":"1"})
        if outcome["code"]!=0:
            raise gate.GateError("local_structured_model_failed")
        return json.loads(outcome["stdout"])
    record=gate.exact_run(record,SOURCE,RUNS,name,
                          limited_local_model,cancel_file=cancel)
    print(json.dumps(record,sort_keys=True))
    if record["status"]!="verified_local_review":
        raise gate.GateError("benchmark_not_verified")

if __name__=="__main__":
    if len(sys.argv)!=2:
        print('{"status":"blocked","reason":"one_approved_task_required"}')
        sys.exit(2)
    try:main(sys.argv[1])
    except Exception as exc:
        print(json.dumps({"status":"blocked","reason":type(exc).__name__}))
        sys.exit(2)
