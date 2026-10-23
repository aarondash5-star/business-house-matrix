"""Review local planning evidence without mistaking keywords for certification."""
import pathlib,sys,tempfile,json,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"benchmarks"/"gate_s"))
import review_local_plan_v3 as qa
GOOD=("Andaz mobile responsive dorm private rooms PMS booking WhatsApp "
 "verified real photo ownership Moksha SEO accessibility keyboard rollback "
 "independent QA security owner approval unknowns. DELIVERABLE: verified audit evidence. "
 "ACCEPTANCE: source-to-claim checklist with risk register. ")*4
class QA(unittest.TestCase):
 def temp_run(self):
  t=tempfile.TemporaryDirectory()
  root=pathlib.Path(t.name)
  for item in qa.STAGES:(root/(item+".md")).write_text(GOOD)
  (root/"progress.json").write_text(json.dumps({"state":"completed",
       "phases":[{"status":"completed"}]*5}))
  return t,root
 def test_complete_structure_detected(self):
  tmp,root=self.temp_run()
  with tmp:self.assertEqual(qa.analyze(root)["decision"],"REVIEW_READY")
 def test_incomplete_run_rejected(self):
  tmp,root=self.temp_run()
  with tmp:
   (root/"progress.json").write_text(json.dumps({"state":"running","phases":[]}))
   self.assertIn("model_run_not_complete",qa.analyze(root)["issues"])
 def test_missing_stage_rejected(self):
  tmp,root=self.temp_run()
  with tmp:
   (root/(qa.STAGES[3]+".md")).unlink()
   self.assertIn("missing_or_short_phase:"+qa.STAGES[3],qa.analyze(root)["issues"])
 def test_suspicious_consistency_threshold_rejected(self):
  tmp,root=self.temp_run()
  with tmp:
   target=root/(qa.STAGES[0]+".md")
   target.write_text(GOOD+" at least 90% of room availability and pricing data must be consistent")
   self.assertTrue(qa.analyze(root)["critical_patterns"]["unjustified_booking_consistency_below_100pct"])
 def test_no_claimed_live_inspection(self):
  tmp,root=self.temp_run()
  with tmp:
   (root/(qa.STAGES[1]+".md")).write_text(GOOD+" We have inspected the live WordPress site.")
   self.assertTrue(qa.analyze(root)["critical_patterns"]["fake_completed_live_inspection"])
if __name__=="__main__":unittest.main()
