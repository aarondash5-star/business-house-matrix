#!/usr/bin/env python3
"""Autonomous bounded art direction: vision critique -> allowlisted Blender edit
-> new frames/GLB -> mechanical receipts. NEVER self-certify artistic quality.
"""
import fcntl,hashlib,json,os,subprocess,sys,time,uuid
from pathlib import Path
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
BASE=Path.home()/"shaadi-quality-v1-art-20261025/projects/shaadi-aunty-dodge/art/quality-v1"
WIP=BASE/"iterations/20261026-art-worker-v1"
ROOT=BASE/"iterations/20261026-ai-art-director-v1"
LTS=BASE/"tools/run_blender_4_5_lts.sh"
ORIGINAL=WIP/"sharma_aunty_art_rig_wip_v1.blend"
PIN="SAD-VISUAL-QUALITY-V1"
PROFILES=("glasses","jasmine","zari")
MODEL="qwen3-vl:2b-instruct"
ROOT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(HERE))
from ai_art_vision import model_ready,review
def utc():return datetime.now(timezone.utc).isoformat(timespec='seconds')
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for c in iter(lambda:f.read(1024*1024),b""):h.update(c)
 return h.hexdigest()
def atomic(path,obj):
 temp=path.with_name(path.name+".tmp")
 temp.write_text(json.dumps(obj,indent=2)+"\n")
 os.chmod(temp,0o600);os.replace(temp,path)
def load():
 p=ROOT/"cycle_state.json"
 if p.is_file() and not p.is_symlink():return json.loads(p.read_text())
 return {"version":"art-director-v1","source":str(ORIGINAL),
         "source_sha":sha(ORIGINAL),
         "done_profiles":[],"completed_cycles":0,
         "unresolved":"mature_face_sculpt_and_high_fidelity_sari",
         "state":"enrolled","last_attempt":None,"failures":0,
         "owner_approved":False,"quality_pass":False,
         "release_authorized":False}
def save(state):
 state.update({"updated_utc":utc(),"owner_approved":False,"quality_pass":False,
               "release_authorized":False})
 atomic(ROOT/"cycle_state.json",state)
 atomic(HERE/"director_status.json",{k:state.get(k) for k in
         ("version","state","updated_utc","completed_cycles","done_profiles",
          "unresolved","failures","owner_approved","quality_pass","release_authorized")})
def run(cmd,env,folder,name,timeout=90):
 with (folder/name).open("wb") as log:
  p=subprocess.run(cmd,cwd=str(folder),env=env,stdout=log,
    stderr=subprocess.STDOUT,timeout=timeout,stdin=subprocess.DEVNULL)
 if p.returncode:raise RuntimeError(name+"_exit_"+str(p.returncode))
def choose(critic,used):
 k=str(critic.get("highest_priority","")).lower()
 ideal={"glasses":"glasses","hair":"jasmine","sari":"zari"}.get(k)
 if not ideal:raise RuntimeError("vision_priority_not_allowlisted")
 if ideal in used:raise RuntimeError("vision_priority_already_exhausted")
 return ideal
def verify_enrollment():
 manifest=HERE/"ai_director_enrollment.json"
 if not manifest.is_file() or manifest.is_symlink():
  raise RuntimeError("art_director_not_enrolled")
 x=json.loads(manifest.read_text())
 if (x.get("project")!="shaadi_aunty_dodge" or
     x.get("quality_pin")!=PIN or
     x.get("review_only") is not True or
     x.get("release_authorized") is not False or
     x.get("model")!=MODEL):
  raise RuntimeError("art_director_admission_failed")
 for name,expected in x.get("pinned_scripts",{}).items():
  if name not in ("director_loop.py","ai_art_refine.py",
                  "ai_art_vision.py","render_study.py","export_verify.py"):
   raise RuntimeError("unapproved_script_in_manifest")
  if not (HERE/name).is_file() or sha(HERE/name)!=expected:
   raise RuntimeError("script_integrity_mismatch:"+name)
 if len(x.get("pinned_scripts",{}))!=5:
  raise RuntimeError("missing_script_pins")
 if ORIGINAL.is_symlink() or ROOT.is_symlink() or BASE.is_symlink():
  raise RuntimeError("unsafe_art_symlink")
 return x

def main():
 verify_enrollment()
 fd=os.open(ROOT/"director.lock",os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
 try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
 except BlockingIOError:
  print("DIRECTOR_BUSY");return 2
 try:
  s=load()
  if s["state"]=="running":
   s["state"]="needs_review_uncertain_prior_run";save(s)
   print("DIRECTOR_PREVIOUS_RUN_UNCERTAIN");return 3
  if s["state"]=="needs_review_uncertain_prior_run":
   print("DIRECTOR_AWAITING_RECOVERY");return 3
  if not ORIGINAL.is_file() or s["source_sha"]!=sha(Path(s["source"])):
   s["state"]="blocked_art_source_integrity";save(s);return 4
  if s["completed_cycles"]>=len(PROFILES):
   s["state"]="needs_independent_creative_review";save(s)
   print("DIRECTOR_REVIEW_STOP_AT_3");return 0
  if not model_ready():
   s["state"]="waiting_for_local_vision_model";save(s)
   print("DIRECTOR_VISION_NOT_READY");return 0
  cycle=s["completed_cycles"]+1
  dest=ROOT/("cycle-%02d"%cycle)
  if dest.exists() and any(dest.iterdir()):
   s["state"]="needs_review_existing_output";save(s);return 5
  dest.mkdir(mode=0o700)
  source=Path(s["source"])
  # Model is advisory: inspection of render never supplies executable code.
  photo=(WIP/"neutral_front.png" if cycle==1 else
        ROOT/("cycle-%02d"%(cycle-1))/"neutral_front.png")
  if not photo.is_file():
   s["state"]="blocked_missing_visual_evidence";save(s);return 6
  s["last_attempt"]=utc();s["state"]="running";save(s)
  try:
   available=[k for k,v in (("glasses","glasses"),("hair","jasmine"),("sari","zari")) if v not in s["done_profiles"]]
   critique=review(photo,cycle,timeout=270,allowed=available)
   atomic(dest/"vision_critique.json",critique)
   profile=choose(critique,s["done_profiles"])
   if not profile:raise RuntimeError("no_admissible_revision")
   input_sha=sha(source)
   env=dict(os.environ,ART_REVISION_PROFILE=profile,
     ART_CYCLE_DIR=str(dest),ART_SOURCE_SHA=input_sha,SHAADI_ART_OUTPUT=str(dest))
   run([str(LTS),str(source),"--python",str(HERE/"ai_art_refine.py")],
       env,dest,"revision_blender.log",timeout=100)
   receipt=json.loads((dest/"revision_receipt.json").read_text())
   out=Path(receipt["out_blend"])
   if not out.is_file() or receipt["out_sha256"]!=sha(out):
    raise RuntimeError("revision_receipt_hash_mismatch")
   run([str(LTS),str(out),"--python",str(HERE/"render_study.py")],
       env,dest,"render_blender.log",timeout=100)
   run([str(LTS),str(out),"--python",str(HERE/"export_verify.py")],
       env,dest,"export_blender.log",timeout=100)
   e=json.loads((dest/"export_qa.json").read_text())
   if not (e["actions_complete"] and e["morphs_complete"]):
    raise RuntimeError("core_gltf_contract_failed")
   s["source"]=str(out);s["source_sha"]=sha(out)
   s["done_profiles"].append(profile);s["completed_cycles"]+=1
   s["state"]="candidate_needs_visual_review"
   s["failures"]=0
   s["last_receipt"]=str(dest/"revision_receipt.json")
   s["unresolved"]="feature_film_mature_face_sculpt_fabric_fidelity_owner_visual_comparison"
   save(s)
   print("AI_ART_DIRECTOR_CYCLE_OK",cycle,profile,s["source_sha"],flush=True)
   return 0
  except Exception as exc:
   s["failures"]+=1;s["state"]="needs_review_cycle_failed"
   s["failure_reason"]=type(exc).__name__+":"+str(exc)[:160]
   save(s)
   print("AI_ART_DIRECTOR_CYCLE_FAIL",s["failure_reason"],flush=True)
   return 8
 finally:
  fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
if __name__=="__main__":raise SystemExit(main())
