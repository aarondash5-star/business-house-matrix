#!/usr/bin/env python3
"""Run exactly one bounded LOCAL model against immutable Andaz prompt.
Never dispatch, publish, push or connect to PMS/WordPress.
"""
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"brain"/"supervisor"))
from gate_s_v2 import PlanError, propose_local, plan_prompt

BRIEF = ROOT/"benchmarks"/"gate_s"/"andaz_website_deep_brief_20261023.md"
def main():
    if len(sys.argv)!=2:
        raise SystemExit("usage: run_andaz_deep_eval.py <owner-created-disposable-output-folder>")
    out=pathlib.Path(sys.argv[1]).resolve()
    if not out.is_dir() or out.is_symlink():
        raise SystemExit("output must be an existing authorized directory")
    brief=BRIEF.read_text(encoding="utf-8")
    result={"task":"Andaz private staging website planning","source":"real_local_model",
            "model":"qwen3:4b-instruct","status":"needs_review",
            "executed":False,"published":False,"pushed":False,"spent":False}
    start=time.monotonic()
    try:
        answer=propose_local(brief,timeout=190)
        result.update(status="valid_structured_plan",latency_s=answer["latency_s"],
                      completion_tokens=answer["completion_tokens"],plan=answer["output"]["plan"])
    except Exception as e:
        result.update(error_type=type(e).__name__,error=str(e)[:300])
    finally:
        result["elapsed_s"]=round(time.monotonic()-start,2)
        (out/"qwen4b-deep-eval.json").write_text(json.dumps(result,indent=2))
        print(json.dumps({k:v for k,v in result.items() if k!="plan"}))
    return 0 if result["status"]=="valid_structured_plan" else 2
if __name__=="__main__":sys.exit(main())
