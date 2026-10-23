#!/usr/bin/env python3
"""Isolated Gate S v3: local Ollama multi-pass, resumable, streaming PLAN ONLY.

No project tools/credentials/worker dispatch. No live changes. This is a
cognitive planning experiment, not a new execution authority or v6 adapter.
Each phase receives a verified public-only brief, can run for several minutes,
streams partial tokens to stage-local files, and is bounded by a total budget.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.request

MODEL = "qwen3:4b-instruct"
URL = "http://127.0.0.1:11434/api/generate"
PHASES = [
 ("01-audit-research", "CURRENT STATE & EVIDENCE", "Audit source of truth, live WordPress/PMS integration (do not claim inspection), booking paths, real guest journeys, justified competitor/OTA evidence, source/claim register, measurable baseline and critical unknowns."),
 ("02-ux-content", "MOBILE UX & AUTHENTIC CONTENT", "Design sitemap, conversion-first navigation and page-by-page mobile wireframes, STAY CONNECT PLAY RESET storytelling, room cards, hero/CTAs, real photo provenance, copy and accessibility; preserve Andaz vs Moksha brand boundary."),
 ("03-engineering-booking", "PRIVATE IMPLEMENTATION & PMS BOOKING", "Specify private staging, backup/rollback, architecture constraints, bed/room inventory/date-specific rates, returning guest, WhatsApp handoff, consent/tracking, SEO/canonicals/structured data, privacy-aware IDs, safe delivery modules."),
 ("04-qa-security", "INDEPENDENT QA, SECURITY & ROLLBACK", "Design independent mobile viewport/browser QA, booking synthetic-fixture and negative tests, truthful inventory, accessibility/performance/SEO, data security, threats, regression coverage, staging-only rollback drill."),
 ("05-red-team-signoff", "CRITIQUE, DEPENDENCIES & FINAL OWNER GATES", "Critique gaps and optimistic assumptions from phases 1-4. Create a risk register, phase priorities, dependency/parallelism decisions, measurable no-go conditions, blocked unknowns, and an owner review checklist; explicitly state what has NOT been done.")
]
RULES = (
 "You are the autonomous LOCAL planning brain for the independent Dev Matrix, NOT a code runner. "
 "No shell commands, credentials, live site access, spending, publishing, installation, integrations or claims of completed research. "
 "Do NOT invent current page URLs, pricing, PMS API schema, exact conversion figures, kitchen availability, or site inspection. "
 "All actions are PROPOSALS pending approval. Facts not verified must become specific verification tasks. "
 "Choose your OWN work packages, no five-step linear template; describe safe parallelism. "
 "Each substantive work package needs: ROLE, OBJECTIVE, EVIDENCE INPUTS, DELIVERABLE, "
 "MEASURABLE ACCEPTANCE TEST, DEPENDENCIES and P0/P1/P2 PRIORITY. "
 "Use Markdown headings and short rich paragraphs; do not use JSON or code fences. "
 "Be specific to Andaz, not generic website advice. Keep 3-4 substantive work packages per phase, with 80-120 words per package. "
 "each with genuine implementation detail, Avoid lengthy preambles, repeated disclaimers or decorative headings; use compact work-package sections with all required fields. Demand 100% accurate inventory/availability at every booking acceptance test. Flag unknowns and blockers explicitly."
)
CONTEXT=(
 "Andaz Vibe Stay - Arambol, Goa; STAY CONNECT PLAY RESET. Hostel has dorms, private rooms, "
 "pool and social experiences; Moksha Wellness is a PARTNER, not the hostel. "
 "Prior direction: mobile-first booking-first, avoid palm cliches/generic hostels/oversized hero widget. "
 "Use only authentic, licensed Andaz photography or clearly labeled private staging placeholders. "
 "Existing custom WordPress/PMS with booking/room inventory and WhatsApp handoff must remain intact. "
 "Repeat-guest and ID/country-code collection can involve PII, so require owner-verified privacy. "
 "Kitchen/cafe operational status is NOT confirmed; do not advertise it. "
 "Rates, room inventory, OTA competitors, tracking and booking outcomes must be verified. "
 "Private staging and owner approval only, no live modifications. "
 "Do not assume availability of production SSH, credentials or site admin."
)
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):return None
def atomic_json(file, data):
 tmp=file.with_name(file.name+".tmp")
 tmp.write_text(json.dumps(data,indent=2,sort_keys=True))
 tmp.replace(file)
def stage_request(stage_name,stage_title,focus,previous,keep_alive):
 intro=(
  "Deliver a rigorous SELF-DIRECTED software project PLAN as an independent thinking supervisor. "
  +RULES+"\nREAL PROJECT BRIEF: "+CONTEXT+"\n"
  "CURRENT PHASE "+stage_title+". SPECIFIC OUTCOMES: "+focus+"\n"
  "Previously identified risks/needs to integrate: "+previous[-1600:]+"\n"
  "Write the real proposals for this phase now; no template-only outline."
 )
 return {"model":MODEL,"prompt":intro,"stream":True,"keep_alive":keep_alive,
         "options":{"temperature":0.2,"num_ctx":4096,"num_predict":1400,
                    "num_thread":4,"repeat_penalty":1.04}}
def generate(req, stage_file, metrics_file, timeout=540):
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
 http=urllib.request.Request(URL,data=json.dumps(req).encode("utf8"),
     headers={"Content-Type":"application/json"},method="POST")
 start=time.monotonic(); fragments=[]; last=None
 # Append incrementally, preserving partial responses across timeouts.
 with opener.open(http,timeout=timeout) as conn, open(stage_file,"w",encoding="utf8",buffering=1) as sink:
  if conn.status!=200:raise RuntimeError("ollama_http_error")
  for line in conn:
   if time.monotonic()-start>timeout:raise TimeoutError("phase_timeout")
   if not line.strip():continue
   event=json.loads(line)
   if event.get("model") not in (MODEL,MODEL+":latest"):raise RuntimeError("unexpected_model")
   if event.get("error"):raise RuntimeError("ollama_model_error")
   part=event.get("response","")
   if part:
    if not isinstance(part,str):raise RuntimeError("invalid_stream")
    fragments.append(part);sink.write(part)
   if event.get("done") is True:
    last=event
    break
 if last is None:raise RuntimeError("incomplete_stream")
 elapsed=round(time.monotonic()-start,2)
 values={"wall_s":elapsed,"tokens":last.get("eval_count"),"prompt_tokens":last.get("prompt_eval_count"),
    "load_s":round(last.get("load_duration",0)/1e9,3),
    "generation_s":round(last.get("eval_duration",0)/1e9,3),
    "prefill_s":round(last.get("prompt_eval_duration",0)/1e9,3),
    "done_reason":last.get("done_reason"),"chars":len("".join(fragments))}
 atomic_json(metrics_file,values)
 return values
def main():
 p=argparse.ArgumentParser();p.add_argument("--out",required=True)
 p.add_argument("--max-phases",type=int,default=5);args=p.parse_args()
 out=Path(args.out).resolve()
 if not out.is_dir() or out.is_symlink():raise SystemExit("isolated output directory required")
 if not 1<=args.max_phases<=5:raise SystemExit("phase range")
 receipt=out/"progress.json"
 if receipt.exists():raise SystemExit("do not overwrite existing run")
 status={"mode":"proposal_only","model":MODEL,"started_unix":time.time(),
   "execute":False,"publish":False,"spend":False,"change_permissions":False,
   "phase_total":args.max_phases,"phases":[],"state":"running","brief_sha256":hashlib.sha256(CONTEXT.encode()).hexdigest()}
 atomic_json(receipt,status)
 previous="None. Explicitly identify unknowns; do not claim access to the website."
 started=time.monotonic()
 for index,(name,title,focus) in enumerate(PHASES[:args.max_phases],start=1):
  stage=out/(name+".md"); metrics=out/(name+".json")
  status["current_phase"]=name
  atomic_json(receipt,status)
  try:
   r=stage_request(name,title,focus,previous,"0" if index==args.max_phases else "20m")
   detail=generate(r,stage,metrics)
   text=stage.read_text()
   if len(text)<350:raise RuntimeError("insufficient_planning_detail")
   accepted=detail["done_reason"]=="stop"
   status["phases"].append({"name":name,"status":"completed" if accepted else "truncated",
      **detail})
   previous=text[-1500:]
   atomic_json(receipt,status)
   if not accepted:status["state"]="incomplete";break
  except Exception as exc:
   status["phases"].append({"name":name,"status":"failed",
     "error_type":type(exc).__name__,"error":str(exc)[:160]})
   status["state"]="incomplete";atomic_json(receipt,status);break
  if time.monotonic()-started>2100:
   status["state"]="incomplete";status["reason"]="total_budget";break
 else:status["state"]="completed"
 status["finished_unix"]=time.time()
 status["elapsed_s"]=round(time.monotonic()-started,2)
 atomic_json(receipt,status)
 summary=["# Andaz Vibe Stay - Local Dev Supervisor Planning Run",
  "**Proposal only. No research/site inspection was executed; evidence checks remain open.**",
  "**Model:** "+MODEL,"**Status:** "+status["state"],
  "**Owner approval and v6 security gates remain mandatory.**"]
 for name,title,_ in PHASES[:args.max_phases]:
  f=out/(name+".md")
  if f.exists():summary+=["\n## "+title+"\n",f.read_text()]
 (out/"andaz_local_plan.md").write_text("\n\n".join(summary))
 print(json.dumps({"state":status["state"],"phases":status["phases"],
                  "elapsed_s":status["elapsed_s"],"output":str(out/"andaz_local_plan.md")}))
 return 0 if status["state"]=="completed" else 2
if __name__=="__main__":raise SystemExit(main())
