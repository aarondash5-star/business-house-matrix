"""Independent offline regression for universal Dev candidate, no external accounts."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"brain"/"dev-operator"))
import universal_dev_dispatch as dut


class DevGateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.work=self.root/"andaz-task-v1"
        self.work.mkdir()
        self.git("init","-q")
        self.git("remote","add","origin","https://github.com/demo-owner/demo-site.git")
        (self.work/"app.py").write_text("VALUE=1\n")
        (self.work/"test_app.py").write_text("assert True\n")
        self.git("add","-A")
        self.git("-c","user.name=Test","-c","user.email=fixture@example.invalid",
                 "commit","-qm","fixture")
        self.sha=self.git("rev-parse","HEAD")
        self.request=dict(schema=1,task_id="andaz-task-v1",project="andaz_static",
            repository="demo-owner/demo-site",base_sha=self.sha,
            objective="Modify application source and validate the independent acceptance test.",
            model="qwen3:4b-instruct",
            image="docker.io/library/python@sha256:"+"a"*64,
            test_command="python3 -B test_app.py",approval_ref="approved-gate-test",
            max_steps=4,max_seconds=180,
            trusted_tests={"test_app.py":hashlib.sha256(
                (self.work/"test_app.py").read_bytes()).hexdigest()})
        self.key=b"unit-test-fixture-signing-key-32-bytes-minimum"
        self.signature=dut.sign_owner(self.request,self.key)

    def git(self,*args):
        env={"PATH":"/usr/bin:/bin","HOME":str(self.root),
             "GIT_CONFIG_NOSYSTEM":"1","GIT_CONFIG_GLOBAL":"/dev/null",
             "GIT_TERMINAL_PROMPT":"0"}
        result=subprocess.run(["/usr/bin/git","-c","core.hooksPath=/dev/null",*args],
                              cwd=self.work,env=env,capture_output=True,text=True,timeout=15)
        if result.returncode:
            raise AssertionError(result.stderr)
        return result.stdout.strip()

    def denies(self, func):
        with self.assertRaises(dut.Denied):
            func()

    def test_owner_signed_dynamic_project(self):
        self.assertEqual(dut.validate_request(self.request,self.signature,self.key),
                         self.request)
        changed=dict(self.request,project="different_project")
        self.denies(lambda:dut.validate_request(changed,self.signature,self.key))
        self.denies(lambda:dut.validate_request(self.request,"f"*64,self.key))

    def test_bad_repositories_blocked(self):
        for name in ("../private","org/..","./repo","org/.hidden","org/foo..bar"):
            with self.subTest(name=name):
                request=dict(self.request,repository=name)
                self.denies(lambda:dut.validate_request(
                    request,dut.sign_owner(request,self.key),self.key))

    def test_pinned_container_image_and_test_identity(self):
        q=dict(self.request,image="python:latest")
        self.denies(lambda:dut.validate_request(q,dut.sign_owner(q,self.key),self.key))
        q=dict(self.request,trusted_tests={})
        self.denies(lambda:dut.validate_request(q,dut.sign_owner(q,self.key),self.key))

    def test_guest_isolation_and_readonly_git_metadata(self):
        args=dut.podman_argv("/usr/bin/podman",self.request["image"],
                            self.work,"python3 -B test_app.py")
        self.assertIn("--network=none",args)
        self.assertIn("--cap-drop=all",args)
        self.assertIn("--security-opt=no-new-privileges",args)
        self.assertTrue(any("/workspace/.git:ro" in v for v in args))
        self.assertIn("--read-only",args)

    def test_clean_repo_cannot_falsely_finish(self):
        dut.validate_source(self.work,self.sha,self.request["repository"])
        self.denies(lambda:dut.verified_source_changes(self.work,self.request))

    def test_real_source_edit_has_sha_fingerprint(self):
        (self.work/"app.py").write_text("VALUE=2\n")
        proof=dut.verified_source_changes(self.work,self.request)
        self.assertEqual(proof["changed_files"],["app.py"])
        self.assertEqual(len(proof["change_sha256"]),64)

    def test_new_file_is_reviewable(self):
        (self.work/"new.py").write_text("print('new')\n")
        proof=dut.verified_source_changes(self.work,self.request)
        self.assertIn("new.py",proof["changed_files"])

    def test_trusted_tests_cannot_be_changed(self):
        (self.work/"app.py").write_text("VALUE=2\n")
        (self.work/"test_app.py").write_text("assert False\n")
        self.denies(lambda:dut.verified_source_changes(self.work,self.request))

    def test_baseline_and_origin_tampering_denied(self):
        (self.work/"app.py").write_text("VALUE=2\n")
        self.git("remote","set-url","origin","https://github.com/other/unsafe.git")
        self.denies(lambda:dut.verified_source_changes(self.work,self.request))
        self.git("remote","set-url","origin",
                 "https://github.com/demo-owner/demo-site.git")
        self.git("add","-A")
        self.git("-c","user.name=Test","-c","user.email=fixture@example.invalid",
                 "commit","-qm","modified")
        self.denies(lambda:dut.verified_source_changes(self.work,self.request))

    def test_symlink_source_denied(self):
        (self.work/"pointer.py").symlink_to(self.work/"app.py")
        self.denies(lambda:dut.verified_source_changes(self.work,self.request))

    def test_ledger_idempotency_and_crash_quarantine(self):
        ledger=dut.JobLedger(self.root/"ledger.sqlite")
        self.assertEqual(ledger.submit(self.request,self.signature,self.key)["state"],"queued")
        self.assertTrue(ledger.submit(self.request,self.signature,self.key)["deduplicated"])
        ledger.claim(self.request["task_id"])
        self.denies(lambda:ledger.claim(self.request["task_id"]))
        self.assertEqual(ledger.quarantine_orphaned(),1)
        self.assertEqual(ledger.status(self.request["task_id"])["state"],"needs_review")

    def test_mock_lifecycle_requires_actual_edit_and_passed_qa(self):
        class Model:
            def __init__(self,name):self.called=0
            def next_action(self,request,history):
                self.called+=1
                if self.called==1:return {"action":"command","command":"edit app.py"}
                return {"action":"finish","summary":"changed app.py"}
        class Backend:
            def __init__(self,work):self.work=work
            def execute(self,image,command,timeout,read_only=False):
                if not read_only:(self.work/"app.py").write_text("VALUE=2\n")
                return dut.Outcome(0,"test pass","")
        ledger=dut.JobLedger(self.root/"lifecycle.sqlite")
        ledger.submit(self.request,self.signature,self.key)
        result=dut.execute_job(ledger,self.request["task_id"],self.key,
            workspace_root=self.root,model_factory=Model,backend_factory=Backend)
        self.assertEqual(result["state"],"review_ready")
        self.assertIn("app.py",result["receipt"]["source_changes"]["changed_files"])

    def test_noop_model_action_must_not_pass(self):
        class Model:
            def __init__(self,name):self.called=0
            def next_action(self,request,history):
                self.called+=1
                if self.called==1:return {"action":"command","command":"true"}
                return {"action":"finish","summary":"finished without edits"}
        class Noop:
            def __init__(self,work):pass
            def execute(self,*args,**kwargs):return dut.Outcome(0,"pass","")
        ledger=dut.JobLedger(self.root/"noop.sqlite")
        ledger.submit(self.request,self.signature,self.key)
        result=dut.execute_job(ledger,self.request["task_id"],self.key,
            workspace_root=self.root,model_factory=Model,backend_factory=Noop)
        self.assertEqual(result["state"],"needs_review")
        self.assertIn("no_source_changes",result["receipt"]["reason"])


    def test_verified_qa_auto_completes_without_model_finish(self):
        class NeverFinish:
            def __init__(self,name):
                self.called=0
            def next_action(self,request,history):
                self.called+=1
                return {"action":"command","command":"edit app.py"}
        class Backend:
            def __init__(self,work):
                self.work=work
            def execute(self,image,command,timeout,read_only=False):
                if not read_only:
                    (self.work/"app.py").write_text("VALUE=2\\n")
                return dut.Outcome(0,"QA PASS","")
        ledger=dut.JobLedger(self.root/"auto-verified.sqlite")
        ledger.submit(self.request,self.signature,self.key)
        result=dut.execute_job(ledger,self.request["task_id"],self.key,
                workspace_root=self.root,model_factory=NeverFinish,backend_factory=Backend)
        self.assertEqual(result["state"],"review_ready")
        self.assertEqual(result["steps"],1)
        self.assertEqual(result["receipt"]["qa_exit"],0)
        self.assertIn("app.py",result["receipt"]["source_changes"]["changed_files"])

    def test_failed_independent_qa_does_not_auto_complete(self):
        class NeverFinish:
            def __init__(self,name): pass
            def next_action(self,request,history):
                return {"action":"command","command":"edit app.py"}
        class BadQA:
            def __init__(self,work): self.work=work
            def execute(self,image,command,timeout,read_only=False):
                if not read_only:(self.work/"app.py").write_text("VALUE=2\\n")
                return dut.Outcome(1 if read_only else 0,"","independent test failed")
        ledger=dut.JobLedger(self.root/"badqa.sqlite")
        ledger.submit(self.request,self.signature,self.key)
        result=dut.execute_job(ledger,self.request["task_id"],self.key,
            workspace_root=self.root,model_factory=NeverFinish,backend_factory=BadQA)
        self.assertEqual(result["state"],"needs_review")


if __name__=="__main__":
    unittest.main()
