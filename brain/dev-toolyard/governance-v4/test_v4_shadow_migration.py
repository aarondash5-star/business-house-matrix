"""Run as isolated rootless QA with V4_RELEASE_FIXTURE_DIR set.

Tests detached V1.4 source-binding migration against actual pinned Dell
V1.3 controller dependency files, without writing to shared controller.
"""
import importlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from v4_source_binding_review import render_candidate, inspect_candidate, ReleaseDenied

@unittest.skipUnless(os.getenv("V4_RELEASE_FIXTURE_DIR"), "pinned local fixture required")
class DetachedRuntimeMigration(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/"controller"
        self.root.mkdir(mode=0o700)
        fixture=Path(os.environ["V4_RELEASE_FIXTURE_DIR"])
        old=json.loads((fixture/"ledger_v13.json").read_text())
        self.result=render_candidate(
           (fixture/"gate_v13.py").read_bytes(),
           (fixture/"adapter_v1.py").read_bytes(),
           (fixture/"adapter_v4.py").read_bytes(),
           (fixture/"guard_v4.py").read_bytes(), old)
        inspect_candidate(self.result)
        for name in ("quality_admission.py","quality_gate.py","project_registry.py",
                     "toolyard_qa_standard_v1.py","manager_governance_v3.py",
                     "reviewed_patch_runner.py"):
            shutil.copyfile(fixture/name,self.root/name)
        for name, source in self.result["source"].items():
            (self.root/name).write_bytes(source)
        ledger=self.root/"yard_exec_bindings_v14.json"
        ledger.write_text(json.dumps(self.result["candidate_ledger"],sort_keys=True))
        ledger.chmod(0o600)
        self._prevpath=list(sys.path)
        sys.path.insert(0,str(self.root))
        for module in ("yard_execution_guard_v13", "yard_auto_adapter_v1", "adapter_guard_v4",
                       "toolyard_qa_standard_v1"):
            sys.modules.pop(module,None)
        self.guard=importlib.import_module("yard_execution_guard_v13")
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        for module in ("yard_execution_guard_v13","yard_auto_adapter_v1","adapter_guard_v4",
                       "toolyard_qa_standard_v1"):
            sys.modules.pop(module,None)
        sys.path[:]=self._prevpath

    def test_exact_new_binding_count(self):
        self.assertEqual(len(self.guard.read_ledger()["bindings"]),21)

    def test_manager_preflight_true(self):
        self.assertTrue(self.guard.manager_preflight())

    def test_v4_dependency_pinned(self):
        self.assertTrue(self.guard.verify_sources(["adapter_guard_v4.py"]))

    def test_dev_build_scoped_preflight(self):
        out=self.guard.preflight("matrix_dev_manager","dev_project_build","matrix_lane_driver_v1")
        self.assertEqual(out["rule"],self.guard.VERSION)
        self.assertTrue(out["source_bound"])
        self.assertFalse(out["production_authorized"])

    def test_arbitrary_unenrolled_action_denied(self):
        with self.assertRaises(self.guard.ExecutionDenied):
            self.guard.preflight("matrix_dev_manager","arbitrary_shell","matrix_lane_driver_v1")

    def test_modified_v4_guard_denied(self):
        f=self.root/"adapter_guard_v4.py"
        f.write_bytes(f.read_bytes()+b"\n# unauthorized change")
        with self.assertRaisesRegex(self.guard.ExecutionDenied,"execution_source_hash_drift"):
            self.guard.manager_preflight()

    def test_changed_adapter_denied(self):
        f=self.root/"yard_auto_adapter_v1.py"
        f.write_bytes(f.read_bytes()+b"\n# unauthorized change")
        with self.assertRaisesRegex(self.guard.ExecutionDenied,"execution_source_hash_drift"):
            self.guard.manager_preflight()

    def test_no_prod_flag(self):
        policy=self.guard.read_ledger()
        self.assertIs(policy["production_live"],False)
        self.assertIs(policy["external_paths_certified"],False)

    def test_production_escalation_denied(self):
        f=self.root/"yard_exec_bindings_v14.json"
        policy=json.loads(f.read_text());policy["production_live"]=True
        f.write_text(json.dumps(policy));f.chmod(0o600)
        with self.assertRaises(self.guard.ExecutionDenied):
            self.guard.manager_preflight()

    def test_external_access_escalation_denied(self):
        f=self.root/"yard_exec_bindings_v14.json"
        policy=json.loads(f.read_text());policy["external_paths_certified"]=True
        f.write_text(json.dumps(policy));f.chmod(0o600)
        with self.assertRaises(self.guard.ExecutionDenied):
            self.guard.manager_preflight()

    def test_live_controller_not_in_fixture(self):
        self.assertNotIn("controller.py",list(x.name for x in self.root.iterdir()))
        self.assertFalse((self.root/"controller.db").exists())

if __name__=="__main__":
    unittest.main()
