import importlib.util,json,os,sqlite3,tempfile,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import manager_governance_v3 as g

class GovernanceV3Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name)
  d=sqlite3.connect(self.root/"tasks.sqlite3")
  d.execute("""create table tasks(
    id text,project text,action text,status text,qa_level text,
    updated text,attempts int,remote_job text,error text,created text)""")
  d.execute("insert into tasks values(?,?,?,?,?,?,?,?,?,?)",(
   "aa","shaadi_aunty_dodge","game_toolkit","completed","synthetic",
   "2026-10-25T00:00:00+00:00",1,None,"","2026-10-25T00:00:00+00:00"))
  d.commit();d.close()
  self.qa=self.root/"qa.json"
  self.qa.write_text(json.dumps({"creative_qa":"FAIL_NOT_REFERENCE_MATCH","owner_approval":False,
   "release_allowed":False,"candidates":{"character":{"passed":5,"total":9},
   "wedding":{"passed":3,"total":6}}}))
 def test_initial_event_then_dedupe(self):
  a=g.reconcile(self.root,self.qa)
  self.assertEqual(a["new_events"],1)
  self.assertFalse(a["release_authorized"])
  self.assertEqual(a["shaadi_aunty"]["character"]["passed"],5)
  b=g.reconcile(self.root,self.qa)
  self.assertEqual(b["new_events"],0)
  self.assertEqual(b["event_head"],a["event_head"])
  self.assertEqual(len((self.root/"manager-governance-v3/events.jsonl").read_text().splitlines()),1)
 def test_stall_and_fail_to_review_event(self):
  g.reconcile(self.root,self.qa)
  d=sqlite3.connect(self.root/"tasks.sqlite3")
  d.execute("update tasks set status='delegated' where id='aa'");d.commit();d.close()
  a=g.reconcile(self.root,self.qa)
  self.assertEqual(a["new_events"],1)
  self.assertEqual(a["risk_count"],1)
  self.assertEqual(a["risks"][0]["next"],"inspect_stalled_job_before_retry")
  d=sqlite3.connect(self.root/"tasks.sqlite3")
  d.execute("update tasks set status='needs_review',error='failed',updated='2026-10-26T00:00:00+00:00' where id='aa'")
  d.commit();d.close()
  b=g.reconcile(self.root,self.qa)
  self.assertEqual(b["new_events"],1)
  self.assertFalse(b["auto_retry_uncertain"])
 def test_owner_approval_string_never_self_certifies(self):
  self.qa.write_text(json.dumps({"creative_qa":"PASS","owner_approval":True,"release_allowed":True,
   "candidates":{"character":{"passed":9,"total":9},"wedding":{"passed":6,"total":6}}}))
  s=g.reconcile(self.root,self.qa)["shaadi_aunty"]
  self.assertFalse(s["release_authorized"])
  self.assertFalse(s["visual_certified"])
 def test_evidence_change_generates_event(self):
  g.reconcile(self.root,self.qa)
  self.qa.write_text(self.qa.read_text()+" ")
  a=g.reconcile(self.root,self.qa)
  self.assertEqual(a["new_events"],1)
 def test_symlinks_and_missing_evidence_fail_closed(self):
  missing=g.reconcile(self.root,self.root/"nonexistent.json")
  self.assertFalse(missing["shaadi_aunty"]["visual_certified"])
  other=self.root/"safe.json";other.write_text("{}")
  evil=self.root/"symlink.json";evil.symlink_to(other)
  self.assertEqual(g.art_status(evil)["state"],"evidence_missing")
 def test_no_database_mutation(self):
  db=self.root/"tasks.sqlite3"
  orig=db.read_bytes()
  g.reconcile(self.root,self.qa)
  self.assertEqual(db.read_bytes(),orig)
 def test_report_and_private_state(self):
  g.reconcile(self.root,self.qa)
  self.assertEqual(g.report(self.root)["version"],g.VERSION)
  p=self.root/"manager-governance-v3"
  self.assertEqual(p.stat().st_mode&0o777,0o700)
  self.assertEqual((p/"latest.json").stat().st_mode&0o777,0o600)
 def test_event_chain_verifies(self):
  g.reconcile(self.root,self.qa)
  lines=(self.root/"manager-governance-v3/events.jsonl").read_text().splitlines()
  h="0"*64
  for line in lines:
   e=json.loads(line)
   self.assertEqual(e["previous"],h)
   self.assertEqual(e["sha256"],g.digest(g.wire({"previous":h,"event":e["event"]})))
   h=e["sha256"]
if __name__=="__main__":unittest.main()
