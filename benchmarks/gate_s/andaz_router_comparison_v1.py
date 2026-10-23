#!/usr/bin/env python3
"""Gate S model comparison: exact public prompts via existing free-only router.

Three fixed context-rich plan slices, identical for both model slots.
No model tools, commands, credentials, production changes or automated replay.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROUTER=Path.home()/".local/share/matrix-dev-router/matrix-route.py"
OUT=Path.home()/"matrix-gate-s-andaz-comparison-20261023"
SLOTS={"local":"local-qwen","north":"openrouter-code","oss120":"groq-oss120"}
PHASES={
 "discovery":"Audit real website WordPress/PMS and booking journey, dated Arambol competitive evidence, mobile STAY-CONNECT-PLAY-RESET information architecture/wireframes and real photo rights.",
 "build":"Plan isolated WordPress staging/backups, room/dorm UI, PMS inventory/WhatsApp booking/return guests, content SEO/canonical/schema, consent analytics and rollback.",
 "verify":"Independent mobile booking/availability regression with synthetic fixtures, a11y, Core Web Vitals/SEO, photo authenticity, ID/PII security, failure paths, rollback and owner review."
}
CONTEXT=("Andaz Vibe Stay - Arambol, Goa hostel: dorm/private rooms, pool/social "
 "experiences and Moksha wellness partner. Real property photography, mobile "
 "booking-first STAY-CONNECT-PLAY-RESET; preserve existing WordPress/PMS and "
 "WhatsApp booking. Do not invent prices, availability, inspection findings "
 "or claim unverified kitchen/cafe is operating. Private staging only.")
def question(phase):
 s=("You are a senior autonomous Dev Matrix planning supervisor. Produce a "
  "specific, implementable deep plan for this ONE phase; NOT a generic outline. "
  "No website inspected; mark unknowns, no model tools, changes, spend or publish. "
  "PUBLIC PROJECT: "+CONTEXT+" PHASE: "+PHASES[phase]+" "
  "Return ONLY JSON: "+'{"phase":"'+phase+'","tasks":[{"role":"research|design|development|qa|security|review",'
  '"objective":"specific work","deliverable":"verifiable artifact",'
  '"acceptance":"measurable independent criterion",'
  '"dependencies":"prior evidence or work"}],"risks":["..."],"unknowns":["..."]}. '
  "Choose 3-5 detailed work packages with objective, deliverable, acceptance, "
  "dependencies, genuine risks and unknowns. This is a plan, not executed work.")
 if len(s.encode())>2048:raise ValueError("router prompt limit")
 return s
def extract(stdout):
 for line in reversed(stdout.splitlines()):
  try: p=json.loads(line)
  except json.JSONDecodeError:continue
  if isinstance(p,dict) and isinstance(p.get("text"),str):
   return {"provider_response_model":p.get("model"),"usage":p.get("usage"),"text":p["text"],"tools_enabled":p.get("tools_enabled")}
 return None
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--slot",choices=SLOTS,required=True)
 parser.add_argument("--phase",choices=PHASES,required=True)
 o=parser.parse_args()
 if not ROUTER.is_file() or not OUT.is_dir():raise SystemExit("trusted_router_or_staging_missing")
 dst=OUT/(o.slot+"-"+o.phase+".json")
 if dst.exists():raise SystemExit("no_ambiguous_replay")
 q=question(o.phase)
 argv=[sys.executable,"-B",str(ROUTER),"run","--profile","reasoning","--public-input",
       "--no-fallback","--slot",SLOTS[o.slot],q]
 receipt={"slot":o.slot,"phase":o.phase,"prompt_sha256":hashlib.sha256(q.encode()).hexdigest(),
    "prompt_bytes":len(q.encode()),"model_slot":SLOTS[o.slot],
    "status":"needs_review","production_changed":False,
    "no_tools":True,"paid_inference_allowed":False,"started_unix":time.time()}
 start=time.monotonic()
 try:
  p=subprocess.run(argv,capture_output=True,text=True,timeout=115,
      env={"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":str(Path.home()),"LANG":"C.UTF-8"})
  receipt["router_exit"]=p.returncode
  receipt["router_diagnostic"]=p.stderr[-800:]
  x=extract(p.stdout)
  if p.returncode==0 and x and x["tools_enabled"] is False:
   receipt.update(x)
   try:
    raw=x["text"].strip()
    if raw.startswith(chr(96)*3):
     raw=raw.partition("\n")[2].rsplit(chr(96)*3,1)[0].strip()
    plan=json.loads(raw)
    assert isinstance(plan,dict) and plan.get("phase")==o.phase
    assert isinstance(plan.get("tasks"),list) and 2<=len(plan["tasks"])<=7
    assert isinstance(plan.get("risks"),list) and isinstance(plan.get("unknowns"),list)
    for t in plan["tasks"]:
     assert isinstance(t,dict)
     for k in ("role","objective","deliverable","acceptance","dependencies"):
      assert isinstance(t.get(k),str) and len(t[k])>4
     assert t["role"] in ("research","design","development","qa","security","review")
    receipt["plan"]=plan
    receipt["status"]="valid_plan"
   except (AssertionError,ValueError,TypeError) as exc:
    receipt.update(status="invalid_model_plan",parse_error=type(exc).__name__)
  else:receipt["status"]="router_failed_or_denied"
 except subprocess.TimeoutExpired:receipt["status"]="model_timeout"
 finally:
  receipt["duration_s"]=round(time.monotonic()-start,3)
  dst.write_text(json.dumps(receipt,indent=2))
  print(json.dumps({"status":receipt["status"],"slot":o.slot,"phase":o.phase,
       "duration_s":receipt["duration_s"],"model":receipt.get("provider_response_model"),
       "router_exit":receipt.get("router_exit"),"prompt_sha256":receipt["prompt_sha256"]}))
 return 0 if receipt["status"]=="valid_plan" else 2
if __name__=="__main__":sys.exit(main())
