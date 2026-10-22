"""Gate E candidate tests: real immutable Git baseline, isolated Python/Node QA.

No external network, credentials, or production repositories are used.
"""
import importlib.util
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("gate_e_runtime_under_test",ROOT/"gate_e_runtime.py")
gate=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=gate
spec.loader.exec_module(gate)

REPO="aarondash5-star/business-house-matrix"

class GateETests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="matrix-gate-e-")
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.repo=self.root/"repo"
        self.repo.mkdir()
        subprocess.run(["git","init","-q"],cwd=self.repo,check=True)
        subprocess.run(["git","remote","add","origin","https://github.com/"+REPO+".git"],
                       cwd=self.repo,check=True)
        (self.repo/"README.md").write_text("Public arithmetic QA exercise.")
        (self.repo/"src").mkdir()
        (self.repo/"tests").mkdir()
        self.stage=self.root/"stage"
        self.stage.mkdir()
    def commit(self):
        subprocess.run(["git","add","."],cwd=self.repo,check=True)
        subprocess.run(["git","-c","user.name=QA","-c","user.email=qa@example.invalid",
                        "commit","-q","-m","baseline"],cwd=self.repo,check=True)
        return subprocess.check_output(["git","rev-parse","HEAD"],cwd=self.repo,text=True).strip()
    def record(self,sha,profile,writable,tests):
        return {"manifest":{"project":"gate_e_qa","repository":REPO,"base_sha":sha,
                 "files":writable+tests,"test_profile":profile,"write_enabled":True},
                 "goal":"Repair arithmetic operation using only the approved source file.",
                 "context":["README.md"],"tests":tests}
    def python_case(self):
        (self.repo/"src"/"arithmetic.py").write_text("def add(a,b):\n    return a-b\n")
        (self.repo/"tests"/"test_arithmetic.py").write_text(
            "import unittest\nfrom src.arithmetic import add\n"
            "class Tests(unittest.TestCase):\n"
            " def test_sum(self):\n  self.assertEqual(add(2,3),5)\n")
        sha=self.commit()
        record=self.record(sha,"python-unittest",["src/arithmetic.py"],["tests/test_arithmetic.py"])
        return record
    def node_case(self):
        (self.repo/"src"/"arithmetic.js").write_text(
            "function add(a,b){return a-b};module.exports={add};\n")
        (self.repo/"tests"/"arithmetic.test.js").write_text(
            "const test=require('node:test');const assert=require('node:assert/strict');"
            "const {add}=require('../src/arithmetic');"
            "test('sum',()=>assert.equal(add(2,3),5));\n")
        sha=self.commit()
        return self.record(sha,"node-test",["src/arithmetic.js"],["tests/arithmetic.test.js"])
    def test_immutable_python_e2e_verified_local_only(self):
        record=self.python_case()
        result=gate.exact_run(record,self.repo,self.stage,"qa_python_e2e",
            lambda prompt,attempt:{"summary":"correct addition",
                 "files":[{"path":"src/arithmetic.py","content":"def add(a,b):\n    return a+b\n"}]})
        self.assertEqual(result["status"],"verified_local_review",result)
        self.assertTrue(result["qa"]["qa_passed"])
        self.assertFalse(result["published"])
        self.assertFalse(result["review"]["pushed"])
        self.assertTrue((self.stage/"qa_python_e2e"/"receipt.json").exists())
        self.assertIn("a-b",(self.repo/"src"/"arithmetic.py").read_text())
        self.assertEqual(result["review"]["files"],["src/arithmetic.py"])
    def test_immutable_node_e2e_verified_local_only(self):
        record=self.node_case()
        result=gate.exact_run(record,self.repo,self.stage,"qa_node_e2e",
            lambda prompt,attempt:{"summary":"correct JS addition",
                 "files":[{"path":"src/arithmetic.js",
                           "content":"function add(a,b){return a+b};module.exports={add};\n"}]})
        self.assertEqual(result["status"],"verified_local_review",result)
        self.assertTrue(any(c["type"]=="node_test" and c["passed"] for c in result["qa"]["checks"]))
        self.assertFalse(result["pushed"])
    def test_failing_model_repairs_within_three_attempts(self):
        record=self.python_case()
        proposals=[
            {"summary":"bad first","files":[{"path":"src/arithmetic.py","content":"def add(a,b):\n return a-b\n"}]},
            {"summary":"fixed","files":[{"path":"src/arithmetic.py","content":"def add(a,b):\n return a+b\n"}]},
        ]
        result=gate.exact_run(record,self.repo,self.stage,"qa_repair_loop",
                              lambda p,n:proposals[n-1])
        self.assertEqual(result["status"],"verified_local_review",result)
        self.assertEqual(len(result["attempts"]),2)
        self.assertFalse(result["attempts"][0]["qa_passed"])
    def test_tests_cannot_be_model_modified(self):
        record=self.python_case()
        result=gate.exact_run(record,self.repo,self.stage,"qa_test_write_deny",
            lambda p,n:{"summary":"attack","files":[{"path":"tests/test_arithmetic.py",
                                                      "content":"pass\n"}]})
        self.assertEqual(result["status"],"needs_review")
        self.assertLessEqual(len(result["attempts"]),3)
        self.assertFalse((self.stage/"qa_test_write_deny"/"local-review").exists())
    def test_cancel_before_model_invocation(self):
        record=self.python_case()
        marker=self.root/"cancel"
        marker.write_text("owner requested")
        result=gate.exact_run(record,self.repo,self.stage,"qa_cancel_check",
                              lambda p,n:self.fail("proposer must not run"),cancel_file=marker)
        self.assertEqual(result["status"],"cancelled_verified")
        self.assertFalse((self.stage/"qa_cancel_check"/"local-review").exists())
    def test_duplicate_task_is_not_replayed(self):
        record=self.python_case()
        first=gate.exact_run(record,self.repo,self.stage,"qa_no_replay",
            lambda p,n:{"summary":"fixed","files":[{"path":"src/arithmetic.py",
                                                     "content":"def add(a,b):return a+b\n"}]})
        self.assertEqual(first["status"],"verified_local_review",first)
        with self.assertRaises(FileExistsError):
            gate.exact_run(record,self.repo,self.stage,"qa_no_replay",lambda p,n:{})
    def test_foreign_origin_denied(self):
        record=self.python_case()
        subprocess.run(["git","remote","set-url","origin","https://github.com/other/private.git"],
                       cwd=self.repo,check=True)
        with self.assertRaises(gate.GateError):
            gate.exact_run(record,self.repo,self.stage,"qa_origin_denied",lambda p,n:{})
    def test_unpinned_sha_denied(self):
        record=self.python_case()
        record["manifest"]["base_sha"]="main"
        with self.assertRaises(ValueError):
            gate.enrollment(record)
    def test_missing_trusted_tests_denied(self):
        record=self.python_case()
        record["tests"]=[]
        with self.assertRaises(gate.GateError):
            gate.enrollment(record)
    def test_context_cannot_be_writable(self):
        record=self.python_case()
        record["context"]=["src/arithmetic.py"]
        with self.assertRaises(gate.GateError):
            gate.enrollment(record)
    def test_node_invalid_syntax_fails_closed(self):
        record=self.node_case()
        result=gate.exact_run(record,self.repo,self.stage,"qa_node_syntax_deny",
             lambda p,n:{"summary":"broken","files":[{"path":"src/arithmetic.js",
                                                         "content":"function add({ broken"}]})
        self.assertEqual(result["status"],"needs_review",result)
        self.assertFalse((self.stage/"qa_node_syntax_deny"/"local-review").exists())
    def test_baseline_symlink_denied(self):
        os.symlink("/etc/passwd",self.repo/"src"/"arithmetic.py")
        (self.repo/"tests"/"test_arithmetic.py").write_text("import unittest\n")
        sha=self.commit()
        record=self.record(sha,"python-unittest",["src/arithmetic.py"],["tests/test_arithmetic.py"])
        result=gate.exact_run(record,self.repo,self.stage,"qa_symlink_deny",lambda p,n:{})
        self.assertEqual(result["status"],"needs_review",result)
        self.assertEqual(result["error"],"GateError")
    def test_bounded_timeout_terminates_child(self):
        with self.assertRaises(gate.GateError):
            gate.bounded(["/usr/bin/python3","-c","import time;time.sleep(10)"],
                         cwd=self.root,timeout=.1)
    def test_cancelled_subprocess_is_terminated(self):
        flag=self.root/"cancel"
        flag.write_text("stop")
        with self.assertRaises(gate.Cancelled):
            gate.bounded(["/usr/bin/python3","-c","import time;time.sleep(10)"],
                         cwd=self.root,timeout=2,cancel_file=flag)
    def test_owner_cancellation_during_active_python_qa(self):
        # The immutable approved QA itself is intentionally slow so we
        # exercise cancellation after the sandboxed test subprocess starts.
        record=self.python_case()
        (self.repo/"tests"/"test_arithmetic.py").write_text(
            "import time\\ntime.sleep(5)\\nimport unittest\\n"
            "from src.arithmetic import add\\n"
            "class Tests(unittest.TestCase):\\n"
            " def test_sum(self): self.assertEqual(add(2,3),5)\\n".replace("\\\\n","\\n")
        )
        # Pin the modified trusted test baseline, not a model-generated test.
        sha=self.commit()
        record["manifest"]["base_sha"]=sha
        flag=self.root/"cancel-active-qa"
        timer=threading.Timer(1.3, lambda:flag.write_text("stop"))
        timer.daemon=True
        timer.start()
        self.addCleanup(timer.cancel)
        started=time.monotonic()
        result=gate.exact_run(record,self.repo,self.stage,"qa_cancel_live_worker",
            lambda prompt,attempt:{"summary":"fix","files":[
                {"path":"src/arithmetic.py","content":"def add(a,b): return a+b\\n"}]},
            cancel_file=flag)
        self.assertEqual(result["status"],"cancelled_verified",result)
        self.assertLess(time.monotonic()-started,5)
        self.assertFalse((self.stage/"qa_cancel_live_worker"/"local-review").exists())

    def test_global_budget_rejects_late_model_response(self):
        from unittest.mock import patch
        record=self.python_case()
        with patch.object(gate,"TIME_BUDGET",.15):
            result=gate.exact_run(record,self.repo,self.stage,"qa_time_budget",
                lambda prompt,attempt:(time.sleep(.3) or {"summary":"late","files":[
                    {"path":"src/arithmetic.py","content":"def add(a,b):return a+b\\n"}]}))
        self.assertEqual(result["status"],"needs_review",result)
        self.assertEqual(result["error"],"GateError")
        self.assertFalse((self.stage/"qa_time_budget"/"local-review").exists())

    def test_streaming_output_guard_fails_before_child_exit(self):
        with self.assertRaises(gate.GateError):
            gate.bounded(["/usr/bin/python3","-c",
                          "import sys,time;sys.stdout.write('x'*100000);sys.stdout.flush();time.sleep(9)"],
                         cwd=self.root,timeout=3,max_output=2000)

if __name__=="__main__":unittest.main()
