"""Owner-local Matrix Manager supervisor. OBSERVATION ONLY: never dispatch,
retry, release, spend, publish or approve. Event receipts for hourly review."""
import argparse
from contextlib import contextmanager
from datetime import datetime,timezone
import fcntl,hashlib,json,os,sqlite3,tempfile
from pathlib import Path

VERSION="manager-governance-v3"
GATE="SAD-VISUAL-QUALITY-V1"
ART=Path("/var/lib/generic-linux-automator-exec/shaadi-quality-v1-art-20261025/projects/shaadi-aunty-dodge/art/quality-v1/evidence/qa_independent_structural.json")
ALERTS={"needs_review","blocked","failed"}
RUNNING={"queued","dispatching","delegated"}
def now():return datetime.now(timezone.utc).isoformat(timespec="seconds")
def wire(x):return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def digest(x):return hashlib.sha256(x).hexdigest()
def read(p):
 if p.is_symlink():raise ValueError("symlink_denied")
 with p.open() as f:return json.load(f)
def atomic(p,x):
 fd,tmp=tempfile.mkstemp(dir=p.parent,prefix=".gov-")
 try:
  with os.fdopen(fd,"wb") as f:
   f.write(wire(x)+b"\n");f.flush();os.fsync(f.fileno())
  os.chmod(tmp,0o600);os.replace(tmp,p)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
@contextmanager
def locked(folder):
 p=folder/"lock"
 if p.is_symlink():raise ValueError("lock_symlink")
 fd=os.open(p,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
 try:
  fcntl.flock(fd,fcntl.LOCK_EX)
  yield
 finally:
  fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
def rows(root):
 p=Path(root)/"tasks.sqlite3"
 if p.is_symlink():raise ValueError("db_symlink")
 d=sqlite3.connect(p.as_uri()+"?mode=ro",uri=True,timeout=4)
 d.row_factory=sqlite3.Row
 try:
  d.execute("PRAGMA query_only=ON")
  n=d.execute("select count(*) from tasks").fetchone()[0]
  if n>1000:raise ValueError("too_many_tasks")
  return [dict(r) for r in d.execute(
   "select id,project,action,status,qa_level,updated,attempts,remote_job,error from tasks order by created")]
 finally:d.close()
def art_status(p=ART):
 result={"quality_gate":GATE,"release_authorized":False,"visual_certified":False,"state":"evidence_missing"}
 if not p.is_file() or p.is_symlink():return result
 try:
  q=read(p)
  c=q["candidates"]
  result.update({"state":"owner_and_independent_visual_review_required",
   "creative_qa":str(q.get("creative_qa","unknown")),
   "character":{k:c["character"].get(k) for k in ("passed","total")},
   "wedding":{k:c["wedding"].get(k) for k in ("passed","total")},
   "evidence_sha256":digest(p.read_bytes())})
 except (OSError,ValueError,TypeError,KeyError):result["state"]="evidence_invalid"
 return result
def age(s):
 try:
  t=datetime.fromisoformat(s.replace("Z","+00:00"))
  return max(0,int((datetime.now(timezone.utc)-t).total_seconds()))
 except (TypeError,ValueError,AttributeError):return 0
def summarize(tasks,art):
 counts={};risks=[]
 for t in tasks:
  state=t["status"];counts[state]=counts.get(state,0)+1
  if state in ALERTS:risks.append({"task_id":t["id"],"project":t["project"],
    "status":state,"next":"review_or_recover_only_after_receipt_audit"})
  elif state in RUNNING and age(t["updated"])>=1800:
   risks.append({"task_id":t["id"],"project":t["project"],"status":state,
    "age_seconds":age(t["updated"]),"next":"inspect_stalled_job_before_retry"})
 return {"version":VERSION,"snapshot_utc":now(),"total":len(tasks),"counts":counts,
  "risk_count":len(risks),"risks":risks[:50],"shaadi_aunty":art,
  "owner_review_required":True,"release_authorized":False,
  "auto_qa_approval":False,"auto_retry_uncertain":False,
  "auto_promotion":False,"unmanaged_external_tools_certified":False}
def event(folder,x,head):
 h=digest(wire({"previous":head,"event":x}))
 p=folder/"events.jsonl"
 if p.is_symlink():raise ValueError("event_symlink")
 fd=os.open(p,os.O_APPEND|os.O_CREAT|os.O_WRONLY|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,"ab") as f:
  f.write(wire({"previous":head,"event":x,"sha256":h})+b"\n")
  f.flush();os.fsync(f.fileno())
 return h
def reconcile(root,qa_path=ART):
 folder=Path(root)/"manager-governance-v3"
 if folder.is_symlink():raise ValueError("directory_symlink")
 folder.mkdir(parents=True,exist_ok=True,mode=0o700);folder.chmod(0o700)
 with locked(folder):
  index=folder/"index.json"
  old=read(index) if index.exists() else {"fingerprints":{},"head":"0"*64}
  tasks=rows(root);art=art_status(Path(qa_path));out=summarize(tasks,art)
  fingerprints={t["id"]:digest(wire(t)) for t in tasks}
  changed=[t for t in tasks if old["fingerprints"].get(t["id"])!=fingerprints[t["id"]]]
  if not old["fingerprints"]:
   updates=[{"type":"baseline","tasks":len(tasks),"at":now()}]
  else:
   updates=[{"type":"task_change","id":t["id"],"project":t["project"],
     "status":t["status"],"review":t["status"] in ALERTS,"at":now()}
    for t in changed]
  if old.get("art_hash")!=art.get("evidence_sha256") and old["fingerprints"]:
   updates.append({"type":"art_evidence_change","gate":GATE,"at":now(),"approved":False})
  head=old["head"]
  for x in updates:head=event(folder,x,head)
  out.update({"new_events":len(updates),"event_head":head})
  atomic(folder/"latest.json",out)
  atomic(index,{"fingerprints":fingerprints,"head":head,
    "art_hash":art.get("evidence_sha256"),"at":now()})
  return out
def report(root):
 p=Path(root)/"manager-governance-v3/latest.json"
 return read(p) if p.exists() else {"version":VERSION,"state":"not_initialized","release_authorized":False}
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("command",choices=("reconcile","report"))
 ap.add_argument("--root",default=str(Path(__file__).resolve().parent))
 a=ap.parse_args()
 print(json.dumps(reconcile(a.root) if a.command=="reconcile" else report(a.root),indent=2))
