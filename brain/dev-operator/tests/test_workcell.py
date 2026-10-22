import importlib.util
from pathlib import Path
import tempfile
import unittest
import sys

HERE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("workcell_runner",HERE/"workcell_runner.py")
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)

class WorkcellSmoke(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="dev-matrix-workcell-")
        self.addCleanup(self.temp.cleanup)
        self.dir=Path(self.temp.name)
        self.assertTrue(mod.doctor(self.dir)["passed"])
    def test_isolated_semantic_html_and_apply(self):
        files=[{"path":"frontend/index.html","content":'<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width"></head><body><main>Welcome</main></body></html>'}]
        result=mod.isolated(self.dir,"apply",{"paths":["frontend/index.html"],"files":files})
        self.assertEqual(result["written"],["frontend/index.html"])
        qa=mod.isolated(self.dir,"qa",{"paths":["frontend/index.html"],"test_profile":"static-html"})
        self.assertTrue(qa["qa_passed"])
        self.assertTrue(qa["tests_executed"])
    def test_missing_landmark_fails(self):
        mod.isolated(self.dir,"apply",{"paths":["a.html"],"files":[
            {"path":"a.html","content":"<html><body>missing main and viewport</body></html>"}]})
        q=mod.isolated(self.dir,"qa",{"paths":["a.html"],"test_profile":"static-html"})
        self.assertFalse(q["qa_passed"])
    def test_independent_python_syntax(self):
        mod.isolated(self.dir,"apply",{"paths":["pkg.py"],"files":[
            {"path":"pkg.py","content":"def add(a,b): return a+b\n"}]})
        with self.assertRaises(mod.IsolationError):
            # No false PASS for missing HTML despite valid Python.
            mod.isolated(self.dir,"qa",{"paths":["pkg.py"],"test_profile":"static-html"})
    def test_cross_path_rejected(self):
        with self.assertRaises(mod.IsolationError):
            mod.isolated(self.dir,"apply",{"paths":["a.py"],"files":[
                {"path":"../../another/a.py","content":"print(1)"}]})
    def test_hidden_file_rejected(self):
        with self.assertRaises(mod.IsolationError):
            mod.isolated(self.dir,"apply",{"paths":[".env"],"files":[
                {"path":".env","content":"private"}]})
    def test_test_file_mutation_denied(self):
        with self.assertRaises(mod.IsolationError):
            mod.isolated(self.dir,"apply",{"paths":["tests/test_app.py"],"files":[
                {"path":"tests/test_app.py","content":"assert True"}]})
    def test_unenrolled_action_denied(self):
        with self.assertRaises(mod.IsolationError):
            mod.isolated(self.dir,"shell",{})
    def test_unsupported_node_qa_fails_closed(self):
        (self.dir/"main.js").write_text("console.log('sample')")
        with self.assertRaises(mod.IsolationError):
            mod.isolated(self.dir,"qa",{"paths":["main.js"],"test_profile":"node-test"})

if __name__=="__main__":unittest.main()
