#!/usr/bin/env python3
"""Owner-scoped persistent art queue. Fixed Blender/OpenCode recipes only.
Does not alter controller approvals, publish, merge or assert aesthetic success.
"""
import argparse,hashlib,json,os,sqlite3,subprocess,sys,uuid,fcntl
from contextlib import contextmanager
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=Path.home()/"shaadi-quality-v1-art-20261025/projects/shaadi-aunty-dodge/art/quality-v1"
OUTPUT=ROOT/"iterations/20261026-art-worker-v1"
DB=HERE/"jobs.sqlite3"
STEPS=("render_study","opencode_art_critique","foundation_inventory")
BLENDER=ROOT/"tools/run_blender_4_5_lts.sh"
ASSET=OUTPUT/"sharma_aunty_art_rig_wip_v1.blend"
GATE="SAD-VISUAL-QUALITY-V1"
def stamp():return datetime.now(timezone.utc).isoformat(timespec='seconds')
def sha(p):
 with p.open('rb') as f:
  h=hashlib.sha256()
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True)
 tmp=p.with_suffix(p.suffix+".tmp")
 tmp.write_text(json.dumps(x,indent=2)+"\n")
 os.chmod(tmp,0o600);os.replace(tmp,p)
@contextmanager
def lock():
 HERE.mkdir(parents=True,exist_ok=True)
 fd=os.open(HERE/"worker.lock",os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
 try:
  fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
  yield
 finally:fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
def connect():
 d=sqlite3.connect(DB,timeout=10);d.row_factory=sqlite3.Row
 d.execute("PRAGMA journal_mode=WAL")
 d.execute("""CREATE TABLE IF NOT EXISTS jobs
 (id TEXT PRIMARY KEY,step TEXT UNIQUE NOT NULL,status TEXT NOT NULL,
 created TEXT NOT NULL,updated TEXT NOT NULL,attempts INTEGER DEFAULT 0,
 input_sha TEXT,output_sha TEXT,error TEXT DEFAULT '')""")
 d.commit();os.chmod(DB,0o600);return d
def assert_scope():
 if ROOT.is_symlink() or OUTPUT.is_symlink():raise RuntimeError("art_path_symlink")
 if not BLENDER.is_file() or not ASSET.is_file():raise RuntimeError("missing_pinned_blender_or_asset")
 if (HERE/"worker_enrollment.json").is_symlink():raise RuntimeError("enrollment_symlink")
 e=json.loads((HERE/"worker_enrollment.json").read_text())
 if e.get("project")!="shaadi_aunty_dodge" or e.get("gate")!=GATE or e.get("production_merge") is not False:
  raise RuntimeError("unauthorized_enrollment")
 if e.get("source_sha256")!=sha(ASSET):raise RuntimeError("unapproved_art_source_drift")
 for name in ("render_study.py","character_art_pass.py","foundation_inventory.py"):
  if e["scripts"].get(name)!=sha(HERE/name):raise RuntimeError("pinned_worker_recipe_drift")
 return e
def enroll():
 e={"project":"shaadi_aunty_dodge","scope":"isolated_review_only",
    "gate":GATE,"approved_request":"Owner: enroll art worker and restart character rebuild",
    "source_sha256":sha(ASSET),
    "scripts":{x:sha(HERE/x) for x in ("render_study.py","character_art_pass.py","foundation_inventory.py")},
    "production_merge":False,"paid_apis":False,
    "visual_approval":False,"at":stamp()}
 write(HERE/"worker_enrollment.json",e)
 return e
def seed():
 assert_scope()
 d=connect()
 for step in STEPS:
  d.execute("INSERT OR IGNORE INTO jobs VALUES (?,?,?,?,?,?,?,?,?)",
            (str(uuid.uuid4()),step,"queued",stamp(),stamp(),0,sha(ASSET),None,""))
 d.commit();d.close();return status()
def status():
 d=connect();j=[dict(x) for x in d.execute("SELECT * FROM jobs ORDER BY created,step")];d.close()
 obj={"worker":"shaadi-art-v1","gate":GATE,"polled":stamp(),
     "worker_enrolled":(HERE/"worker_enrollment.json").is_file(),
     "jobs":j,"jobs_count":len(j),
     "art_source":str(ASSET),"release_authorized":False,
     "visual_certified":False,"auto_qa_approval":False,
     "model_role":"advisory_only","owner_review_required":True}
 write(HERE/"latest.json",obj)
 return obj
def run_step(step):
 if step=="render_study":
  env=dict(os.environ,SHAADI_ART_OUTPUT=str(OUTPUT))
  cmd=[str(BLENDER),str(ASSET),"--python",str(HERE/"render_study.py")]
  name="render_study.log";timeout=120
 elif step=="foundation_inventory":
  cmd=[sys.executable,str(HERE/"foundation_inventory.py")]
  env=dict(os.environ);name="foundation_inventory.log";timeout=35
 elif step=="opencode_art_critique":
  # Run model only for an advisory design brief: output never becomes executable code.
  folder=OUTPUT/"opencode-review";folder.mkdir(exist_ok=True)
  prompt=("Review an Indian wedding game character art task conceptually. Current "
   "semi-realistic Sharma Aunty prototype uses Blender and fails pinned visual gate. "
   "Prioritize 6 concrete sculpt, glasses, mature face, sari drape, jewelry and "
   "authentic mandap changes. Give an ordered concise design critique only. "
   "Never claim approval or request paid assets. Do not use tools or edit files.")
  cmd=["/usr/bin/timeout","75","/usr/local/bin/opencode","run","--agent","plan",
       "-m","ollama/qwen3:4b-instruct",prompt]
  env=dict(os.environ);name="opencode_review.log";timeout=85
 else:raise RuntimeError("recipe_not_allowlisted")
 p=OUTPUT/name
 with p.open("wb") as f:
  r=subprocess.run(cmd,cwd=str(OUTPUT),env=env,stdout=f,stderr=subprocess.STDOUT,
       stdin=subprocess.DEVNULL,timeout=timeout,check=False)
 if r.returncode!=0:raise RuntimeError("fixed_recipe_failed_exit_"+str(r.returncode))
 if step=="foundation_inventory":
  j=json.loads((OUTPUT/"foundation_inventory.json").read_text())
  if j.get("assets_inspected",0)<1:raise RuntimeError("inventory_empty")
 elif step=="render_study":
  j=json.loads((OUTPUT/"render_study_receipt.json").read_text())
  if set(j.get("views",{}))!={"neutral_front","three_quarter","facial_smile","facial_blink"}:
   raise RuntimeError("incomplete_image_evidence")
 else:
  if p.stat().st_size<50:raise RuntimeError("review_output_empty")
 return sha(p)
def tick():
 with lock():
  assert_scope();d=connect()
  # Never auto-replay a job of ambiguous state.
  for row in d.execute("SELECT id FROM jobs WHERE status='running'").fetchall():
   d.execute("UPDATE jobs SET status='needs_review',error='uncertain_previous_dispatch',updated=? WHERE id=?",(stamp(),row["id"]))
  row=d.execute("SELECT * FROM jobs WHERE status='queued' ORDER BY CASE step WHEN 'render_study' THEN 0 ELSE 1 END, created LIMIT 1").fetchone()
  if not row:
   d.commit();d.close();return status()
  d.execute("UPDATE jobs SET status='running',attempts=attempts+1,updated=? WHERE id=?",(stamp(),row["id"]))
  d.commit()
  try:
   result=run_step(row["step"])
   d.execute("UPDATE jobs SET status='completed',output_sha=?,updated=? WHERE id=?",(result,stamp(),row["id"]))
  except Exception as e:
   d.execute("UPDATE jobs SET status='needs_review',error=?,updated=? WHERE id=?",(str(e)[:170],stamp(),row["id"]))
  d.commit();d.close()
  return status()
if __name__=="__main__":
 a=argparse.ArgumentParser()
 a.add_argument("action",choices=("enroll","seed","tick","status"))
 arg=a.parse_args().action
 if arg=="enroll":print(json.dumps(enroll(),indent=2))
 elif arg=="seed":print(json.dumps(seed(),indent=2))
 elif arg=="tick":print(json.dumps(tick(),indent=2))
 else:print(json.dumps(status(),indent=2))
