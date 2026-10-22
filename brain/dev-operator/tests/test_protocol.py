import importlib.util
from pathlib import Path
import unittest

SOURCE=Path(__file__).resolve().parents[1]/"protocol.py"
spec=importlib.util.spec_from_file_location("dev_operator_protocol",SOURCE)
m=importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name]=m
spec.loader.exec_module(m)

def sample():
    return {
        "project":"matrix_dev","repository":"aarondash5-star/business-house-matrix",
        "base_sha":"1"*40,"files":["frontend/index.html","frontend/app.js",
                                       "tests/test_ui.py"],"test_profile":"static-html",
        "write_enabled":True}
class PolicyTests(unittest.TestCase):
    def test_enroll_valid(self):
        v=m.enroll(sample())
        self.assertEqual(len(v.files),3)
        self.assertTrue(v.write_enabled)
    def test_enroll_requires_approval(self):
        data=sample();data["write_enabled"]=False
        with self.assertRaisesRegex(m.PolicyError,"not_enrolled"):
            m.enroll(data)
    def test_reject_unpinned_branch(self):
        data=sample();data["base_sha"]="main"
        with self.assertRaisesRegex(m.PolicyError,"unpinned"):
            m.enroll(data)
    def test_reject_unknown_tools(self):
        data=sample();data["shell"]="run-anything"
        with self.assertRaisesRegex(m.PolicyError,"schema"):
            m.enroll(data)
    def test_reject_cross_project_path(self):
        for value in ("../private/file.py","/etc/config.py",".ssh/id_rsa",
                      "frontend/.env","frontend//src.py","frontend/hello.sh"):
            with self.subTest(value=value):
                data=sample();data["files"]=[value]
                with self.assertRaises(m.PolicyError):m.enroll(data)
    def test_reject_duplicate(self):
        data=sample();data["files"]=["a.py","a.py"]
        with self.assertRaisesRegex(m.PolicyError,"duplicate"):
            m.enroll(data)
    def test_reject_tests_unenrolled(self):
        data=sample();data["test_profile"]="sudo-test"
        with self.assertRaisesRegex(m.PolicyError,"profile"):
            m.enroll(data)
    def test_model_patch_receipt(self):
        manifest=m.enroll(sample())
        good={"summary":"Responsive demo",
              "files":[{"path":"frontend/index.html","content":"<!doctype html><main>Test</main>"}]}
        r=m.validate_proposal(manifest,good)
        self.assertEqual(r["status"],"needs_independent_qa")
        self.assertFalse(r["published"])
        self.assertFalse(r["remote_write"])
        self.assertEqual(len(r["review_sha256"]),64)
    def test_model_cannot_select_repo_or_baseline(self):
        manifest=m.enroll(sample())
        for field in ("repository","base_sha","test_profile","command","mcp"):
            with self.subTest(field=field),self.assertRaisesRegex(m.PolicyError,"schema"):
                m.validate_proposal(manifest,{"summary":"x","files":[
                    {"path":"frontend/index.html","content":"X"}],field:"bad"})
    def test_model_cannot_escape_paths(self):
        manifest=m.enroll(sample())
        for value in ("../../private/a.py","backend/server.py","frontend/index.html/../app.js"):
            with self.subTest(value=value),self.assertRaises(m.PolicyError):
                m.validate_proposal(manifest,{"summary":"x","files":[{"path":value,"content":"ok"}]})
    def test_duplicate_edit_denied(self):
        manifest=m.enroll(sample())
        with self.assertRaises(m.PolicyError):
            m.validate_proposal(manifest,{"summary":"x","files":[
                {"path":"frontend/app.js","content":"A"},
                {"path":"frontend/app.js","content":"B"}]})
    def test_large_source_denied(self):
        manifest=m.enroll(sample())
        with self.assertRaisesRegex(m.PolicyError,"size"):
            m.validate_proposal(manifest,{"summary":"x","files":[
                {"path":"frontend/app.js","content":"a"*33000}]})
    def test_no_secret_literals(self):
        manifest=m.enroll(sample())
        with self.assertRaisesRegex(m.PolicyError,"credential"):
            m.validate_proposal(manifest,{"summary":"x","files":[
                {"path":"frontend/app.js","content":"password='realsecretphrase123456'"}]})

if __name__=="__main__":unittest.main()
