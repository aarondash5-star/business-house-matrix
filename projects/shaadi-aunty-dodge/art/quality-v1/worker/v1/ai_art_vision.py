#!/usr/bin/env python3
"""Local-only multimodal art-direction review. Advisory, never production authority."""
import base64,hashlib,json,os,time,urllib.request
from pathlib import Path
from datetime import datetime,timezone
BASE=Path.home()/"shaadi-quality-v1-art-20261025/projects/shaadi-aunty-dodge/art/quality-v1"
ART=BASE/"iterations/20261026-art-worker-v1"
ROOT=BASE/"iterations/20261026-ai-art-director-v1"
MODEL="qwen3-vl:2b-instruct"
PIN="SAD-VISUAL-QUALITY-V1"
# Grounded in the actual, owner-pinned turnaround reference. This is not a
# substitute for image-to-image comparison against the original reference PNG.
REFERENCE={
 "character":"Warm, authoritative, stocky middle-aged Indian Sharma Aunty, semi-realistic feature-film stylization",
 "face":"Expressive large brown eyes, rounded mature cheeks, defined warm confident smile, expressive brow, red circular bindi",
 "glasses":"Thin but substantial black/brown tortoiseshell oval/rounded-rectangular eyewear with visible bridge and temple arms",
 "hair":"Dark swept-up bun with layered jasmine flower garland and side wisps",
 "costume":"Deep raspberry silk sari with orange-saffron pallu, intricate antique-gold zari jacquard motifs and detailed pleated drape; magenta short-sleeve fitted blouse with gold-embroidered sleeves",
 "ornaments":"Golden dangling jhumka earrings, necklace medallion, black-bead mangalsutra, stacked gold/burgundy bangles, sandals, embroidered handbag",
 "silhouette":"Full-body rounded adult woman with compact center of gravity, full hips, visible distinct silk pleats, hand confidently on hip",
 "never_assume":"No score or approval without independent owner visual review; only an observed candidate description is possible."
}
def utc():return datetime.now(timezone.utc).isoformat(timespec="seconds")
def http_json(url,body=None,timeout=20):
 raw=None if body is None else json.dumps(body).encode()
 req=urllib.request.Request(url,data=raw,headers={"Content-Type":"application/json"} if raw else {})
 with urllib.request.urlopen(req,timeout=timeout) as f:return json.loads(f.read())
def model_ready():
 try:
  tags=http_json("http://127.0.0.1:11434/api/tags",timeout=6)
  return any(x.get("name")==MODEL for x in tags.get("models",[]))
 except Exception:return False
def parse_vision_report(raw,allowed):
 try:report=json.loads(raw.strip())
 except (ValueError,TypeError) as exc:raise RuntimeError("invalid_vision_json") from exc
 if not isinstance(report,dict):raise RuntimeError("vision_report_not_object")
 if report.get("highest_priority") not in allowed:raise RuntimeError("vision_priority_unavailable")
 if not isinstance(report.get("three_critical_defects"),list) or len(report["three_critical_defects"])!=3:
  raise RuntimeError("vision_defect_count_invalid")
 for k in ("visible","specific_modelling_instruction"):
  if not isinstance(report.get(k),str) or len(report[k].strip())<8:
   raise RuntimeError("vision_report_missing_"+k)
 return report

def review(image,cycle,timeout=240,allowed=None):
 allowed=list(allowed or ("glasses","hair","sari"))
 if not allowed or any(a not in ("glasses","hair","sari") for a in allowed):
  raise RuntimeError("vision_allowed_set_invalid")
 if not image.is_file() or image.is_symlink():raise ValueError("missing_image")
 if not model_ready():raise RuntimeError("vision_model_not_installed")
 # Give full image (Ollama image encoding is base64). Only local loopback.
 data=base64.b64encode(image.read_bytes()).decode()
 prompt=("You are an art director. Inspect this actual 3D Blender character "
  "render, NOT an ideal reference. Judge material/model details based only "
  "on visible evidence and compare to this textual target: "
  +json.dumps(REFERENCE,ensure_ascii=False)+
  ". State missing or wrong visual details concisely. "
  "Return JSON object with keys visible, three_critical_defects, "
  "highest_priority (exactly one of the available allowed edits: "+",".join(allowed)+"), "
  "specific_modelling_instruction, confidence. "
  "Describe face and fabric defects even if none of the allowed edits can fix them. "
  "Three critical defects must be three short strings. Only choose an allowed edit. "
  "No claims of independent quality passing or owner approval.")
 result=http_json("http://127.0.0.1:11434/api/generate",
   {"model":MODEL,"prompt":prompt,"images":[data],"stream":False,
    "format":{"type":"object","properties":{
     "visible":{"type":"string"},
     "three_critical_defects":{"type":"array","items":{"type":"string"},"minItems":3,"maxItems":3},
     "highest_priority":{"type":"string","enum":allowed},
     "specific_modelling_instruction":{"type":"string"},
     "confidence":{"type":"string"}},
     "required":["visible","three_critical_defects","highest_priority","specific_modelling_instruction","confidence"],
     "additionalProperties":False},
    "options":{"num_predict":420,"temperature":0.1,"num_ctx":3072},
    "keep_alive":"1m"},timeout)
 raw=result.get("response","")
 report=parse_vision_report(raw,allowed)
 report.update({"model":MODEL,"image_sha256":hashlib.sha256(image.read_bytes()).hexdigest(),
  "cycle":cycle,"timestamp_utc":utc(),"pin":PIN,
  "reference_images_loaded":False, "owner_approved":False,
  "quality_certified":False,"release_authorized":False})
 return report
if __name__=="__main__":
 import sys
 cycle=int(sys.argv[2]) if len(sys.argv)>2 else 0
 img=Path(sys.argv[1])
 ROOT.mkdir(parents=True,exist_ok=True)
 if not model_ready():
  out={"state":"vision_model_not_ready","model":MODEL,"cycle":cycle,
       "timestamp_utc":utc(),"release_authorized":False}
 else:
  try:
   out={"state":"review_complete","review":review(img,cycle)}
  except Exception as exc:
   out={"state":"vision_review_failed","reason":type(exc).__name__,
       "cycle":cycle,"timestamp_utc":utc(),"release_authorized":False}
 outpath=ROOT/("vision_cycle_%02d.json"%cycle)
 outpath.write_text(json.dumps(out,indent=2))
 print("AI_ART_VISION_RECEIPT",json.dumps(out)[:950],flush=True)
