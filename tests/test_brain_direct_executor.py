"""Direct Brain coding capability regression tests; all fake-model/offline, no workers."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"brain"/"dev-brain"))
import direct_executor as d

def manifest():
    return {"schema":1,"task_id":"andaz-static-stage1","mode":"brain_direct_only",
       "workers_allowed":False,"model":"qwen3:4b-instruct","max_steps":8,
       "editable":["site/","docs/"],
       "tests":[["python3","-B","-m","unittest","discover","-s","verification","-p","test_static_site.py","-v"]],
       "publish":False,"merge":False,"spend":False,"permissions":False,
       "brief":"Build a pure static Andaz website with an independent booking enquiry UI and no WordPress dependency. Test the latest revision before declaring success."}

class TestDirectExecutor(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)/"brain-direct"
        self.root.mkdir()
        self.workspace=self.root/"andaz-static-stage1"
        self.workspace.mkdir()
        (self.workspace/"index.html").write_text("Andaz baseline")
        self.patch=patch.object(d,"ROOT",self.root)
        self.patch.start()
        self.m=manifest()
    def tearDown(self):
        self.patch.stop();self.tmp.cleanup()

    def test_manifest_accepts_brain_only(self):
        self.assertEqual(d.validate(self.m)["mode"],"brain_direct_only")
    def test_worker_mode_refused(self):
        m=manifest();m["workers_allowed"]=True
        with self.assertRaises(d.GateError):d.validate(m)
    def test_production_right_refused(self):
        m=manifest();m["publish"]=True
        with self.assertRaises(d.GateError):d.validate(m)
    def test_inline_code_runner_refused(self):
        m=manifest();m["tests"]=[["python3","-c","print(1)"]]
        with self.assertRaises(d.GateError):d.validate(m)
    def test_model_cannot_edit_root_index(self):
        with self.assertRaises(d.GateError):d.put(self.workspace,"index.html","overwritten",self.m)
        self.assertEqual((self.workspace/"index.html").read_text(),"Andaz baseline")
    def test_model_cannot_escape_scope(self):
        for name in ("../secret.js","../../repo/site/index.html","wordpress/plugins/test.js",".github/deploy.yml","site/../admin.js"):
            with self.subTest(path=name):
                with self.assertRaises(d.GateError):d.put(self.workspace,name,"x",self.m)
    def test_symlink_path_blocked(self):
        (self.workspace/"site").symlink_to(Path(self.tmp.name),target_is_directory=True)
        with self.assertRaises(d.GateError):d.put(self.workspace,"site/page.html","x",self.m)
    def test_source_edit_digest(self):
        r=d.put(self.workspace,"site/index.html","<html>Andaz</html>",self.m)
        self.assertEqual(len(r["sha256"]),64)
        self.assertIn("Andaz",d.read(self.workspace,"site/index.html",self.m)["text"])
    def test_full_run_with_fake_model_and_fake_tests(self):
        sequence=iter([
         {"action":"read","path":"index.html"},
         {"action":"write","path":"site/index.html","content":"<html>Andaz</html>"},
         {"action":"test"},
         {"action":"finish","summary":"Static pages created and independently tested."}
        ])
        calls=[]
        def agent(m,history):
            calls.append("model")
            return next(sequence)
        tests=[]
        def tester(workspace,commands):
            tests.append(commands)
            return {"passed":True,"evidence":[{"exit":0}],"isolated":True}
        result=d.run(self.workspace,self.m,agent=agent,tester=tester)
        self.assertEqual(result["status"],"review_ready")
        self.assertFalse(result["worker_invoked"])
        self.assertFalse(result["published"])
        self.assertEqual(len(tests),1)
        self.assertEqual(result["revision"],1)
        self.assertEqual(result["last_tested_revision"],1)
    def test_finish_without_test_never_claims_success(self):
        self.m["max_steps"]=5
        actions=iter([
         {"action":"write","path":"site/index.html","content":"<html>test</html>"},
         {"action":"finish","summary":"Fake pass without running any test"},
         {"action":"finish","summary":"Fake pass without running any test"},
         {"action":"finish","summary":"Fake pass without running any test"},
         {"action":"finish","summary":"Fake pass without running any test"},
        ])
        x=d.run(self.workspace,self.m,agent=lambda m,h:next(actions),
                tester=lambda w,c:{"passed":False})
        self.assertEqual(x["status"],"blocked")
    def test_generated_code_requires_real_sandbox(self):
        with patch.object(d.shutil,"which",return_value=None):
            with self.assertRaisesRegex(d.GateError,"bubblewrap_missing"):
                d.sandbox(self.workspace,self.m["tests"])
    def test_invalid_action_cannot_run_shell(self):
        self.m["max_steps"]=5
        x=d.run(self.workspace,self.m,agent=lambda m,h:{"action":"shell","cmd":"rm -rf /"},
                tester=lambda w,c:{"passed":False})
        self.assertEqual(x["status"],"blocked")
        self.assertEqual(x["revision"],0)
    def test_cannot_repeat_completed_workspace(self):
        (self.workspace/".brain-run.json").write_text('{"status":"review_ready"}')
        with self.assertRaisesRegex(d.GateError,"repeat_run_requires_owner_review"):
            d.run(self.workspace,self.m,agent=lambda m,h:{"action":"list"})
if __name__=="__main__":unittest.main()
