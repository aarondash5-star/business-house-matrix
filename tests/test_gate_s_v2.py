"""Gate S v2 plan richness and policy tests."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"brain"/"supervisor"))
import gate_s_v2 as s

def valid_plan(n=12):
    roles=["research","research","design","design","development","development",
           "development","qa","qa","security","qa","review"]
    if n>12:roles=roles[:-1]+["development"]*(n-12)+["review"]
    tasks=[]
    for i,role in enumerate(roles,1):
        tasks.append({"id":f"T{i}","milestone":"M1" if i<7 else "M2",
          "role":role,"objective":f"Complete specific Andaz planning work package {i}",
          "deliverables":[f"Reviewed measurable artifact for package {i}"],
          "acceptance":[f"Independent QA confirms work package {i}"],
          "depends_on":[] if i==1 else [f"T{i-1}"],"priority":"P0"})
    return {"project":"Andaz mobile website rework",
       "strategy":"Research the real website; plan booking-first staging; verify SEO, accessibility and rollback.",
       "assumptions":["Photos must be verified"],
       "risks":["Inventory data might be stale","SEO redirects might break"],
       "milestones":[{"id":"M1","name":"Research and staging","outcome":"Verified baseline and design"},
                    {"id":"M2","name":"Independent QA and review","outcome":"Reviewed evidence"}],
       "tasks":tasks,"approval":"owner_review_before_execution"}

class TestGateSV2(unittest.TestCase):
    def fails(self,p):
        with self.assertRaises(s.PlanError):s.preview(p)
    def test_twelve_tasks(self):self.assertEqual(len(s.preview(valid_plan())["plan"]["tasks"]),12)
    def test_twenty_tasks(self):self.assertEqual(len(s.preview(valid_plan(20))["plan"]["tasks"]),20)
    def test_no_side_effects(self):
        x=s.preview(valid_plan())
        self.assertTrue(x["owner_approval_required"])
        for key in ("execute","push","publish","spend","privilege_change","model_controls_permissions"):
            self.assertFalse(x[key])
    def test_all_roles(self):self.assertEqual({t["role"] for t in valid_plan()["tasks"]},s.ROLES)
    def test_no_automatic_approval(self):
        x=valid_plan();x["approval"]="auto";self.fails(x)
    def test_no_extra_root_fields(self):
        x=valid_plan();x["run_tool"]="extra";self.fails(x)
    def test_no_extra_task_fields(self):
        x=valid_plan();x["tasks"][4]["run_tool"]="extra";self.fails(x)
    def test_only_enrolled_roles(self):
        x=valid_plan();x["tasks"][4]["role"]="superuser";self.fails(x)
    def test_deliverables_required(self):
        x=valid_plan();x["tasks"][5]["deliverables"]=[];self.fails(x)
    def test_acceptance_required(self):
        x=valid_plan();x["tasks"][5]["acceptance"]=[];self.fails(x)
    def test_review_must_be_last(self):
        x=valid_plan();x["tasks"][-1]["role"]="development";self.fails(x)
    def test_security_required(self):
        x=valid_plan();x["tasks"][9]["role"]="development";self.fails(x)
    def test_forward_dependency_denied(self):
        x=valid_plan();x["tasks"][1]["depends_on"]=["T9"];self.fails(x)
    def test_unknown_dependency_denied(self):
        x=valid_plan();x["tasks"][3]["depends_on"]=["T80"];self.fails(x)
    def test_duplicate_id_denied(self):
        x=valid_plan();x["tasks"][3]["id"]="T2";self.fails(x)
    def test_review_needs_verification_dependency(self):
        x=valid_plan();x["tasks"][-1]["depends_on"]=["T2"];self.fails(x)
    def test_parallel_work_allowed(self):
        x=valid_plan();x["tasks"][3]["depends_on"]=["T1"]
        self.assertEqual(len(s.validate(x)["tasks"]),12)
    def test_long_context_not_truncated_to_350_chars(self):
        self.assertIn("Mandatory owner brief:",s.plan_prompt("Andaz needs mobile-first staging. "*100))
    def test_long_context_bounded(self):
        with self.assertRaises(s.PlanError):s.plan_prompt("a"*13000)
    def test_unapproved_model_denied(self):
        with self.assertRaises(s.PlanError):s.propose_local("Andaz needs a private staging website. "*5,model="other")
if __name__=="__main__":unittest.main()
