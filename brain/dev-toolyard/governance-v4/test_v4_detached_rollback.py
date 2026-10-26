"""Detached V4->V1.3 rollback rehearsal. Never imports or writes host controller."""
import importlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from v4_source_binding_review import render_candidate, inspect_candidate, OLD_ADAPTER_SHA, V13, digest

@unittest.skipUnless(os.environ.get("V4_RELEASE_FIXTURE_DIR"), "requires owner-scoped fixture")
class RollbackRehearsal(unittest.TestCase):
    def setUp(self):
        self.fx=Path(os.environ["V4_RELEASE_FIXTURE_DIR"])
        self.old_guard=(self.fx/"gate_v13.py").read_bytes()
        self.old_adapter=(self.fx/"adapter_v1.py").read_bytes()
        self.old_ledger=(self.fx/"ledger_v13.json").read_bytes()
        self.candidate=render_candidate(
            self.old_guard,self.old_adapter,
            (self.fx/"adapter_v4.py").read_bytes(),
            (self.fx/"guard_v4.py").read_bytes(),
            json.loads(self.old_ledger))
        inspect_candidate(self.candidate)
        self.d=tempfile.TemporaryDirectory()
        self.addCleanup(self.d.cleanup)
        self.root=Path(self.d.name)
        for name in ("quality_admission.py","quality_gate.py","project_registry.py",
                     "toolyard_qa_standard_v1.py","manager_governance_v3.py",
                     "reviewed_patch_runner.py"):
            shutil.copyfile(self.fx/name,self.root/name)
        self._sys_path=list(sys.path)
        sys.path.insert(0,str(self.root))
        self.addCleanup(self.cleanup)
        self.promote_detached()

    def cleanup(self):
        self.purge_modules()
        sys.path[:]=self._sys_path

    def purge_modules(self):
        for m in ("yard_execution_guard_v13","yard_auto_adapter_v1",
                  "adapter_guard_v4","toolyard_qa_standard_v1"):
            sys.modules.pop(m,None)
        importlib.invalidate_caches()

    def promote_detached(self):
        for name,content in self.candidate["source"].items():
            (self.root/name).write_bytes(content)
        ledger=self.root/"yard_exec_bindings_v14.json"
        ledger.write_text(json.dumps(self.candidate["candidate_ledger"],sort_keys=True))
        ledger.chmod(0o600)

    def revert_detached(self):
        (self.root/"yard_execution_guard_v13.py").write_bytes(self.old_guard)
        (self.root/"yard_auto_adapter_v1.py").write_bytes(self.old_adapter)
        (self.root/"yard_exec_bindings_v13.json").write_bytes(self.old_ledger)
        (self.root/"yard_exec_bindings_v13.json").chmod(0o600)
        (self.root/"yard_exec_bindings_v14.json").unlink()
        (self.root/"adapter_guard_v4.py").unlink()
        self.purge_modules()

    def test_exact_reversal_restores_original_hashes(self):
        self.revert_detached()
        self.assertEqual(digest((self.root/"yard_auto_adapter_v1.py").read_bytes()),OLD_ADAPTER_SHA)
        self.assertEqual((self.root/"yard_execution_guard_v13.py").read_bytes(),self.old_guard)
        self.assertEqual((self.root/"yard_exec_bindings_v13.json").read_bytes(),self.old_ledger)
        self.assertFalse((self.root/"adapter_guard_v4.py").exists())
        self.assertFalse((self.root/"yard_exec_bindings_v14.json").exists())

    def test_old_v13_manager_gate_passes_after_reversal(self):
        self.revert_detached()
        guard=importlib.import_module("yard_execution_guard_v13")
        self.assertTrue(guard.manager_preflight())
        self.assertEqual(guard.read_ledger()["version"],V13)

    def test_old_v13_build_admission_is_still_source_bound(self):
        self.revert_detached()
        gate=importlib.import_module("yard_execution_guard_v13")
        report=gate.preflight("matrix_dev_manager","dev_project_build","matrix_lane_driver_v1")
        self.assertTrue(report["source_bound"])
        self.assertFalse(report["production_authorized"])
        with self.assertRaises(gate.ExecutionDenied):
            gate.preflight("matrix_dev_manager","arbitrary_shell","unreviewed")

    def test_v14_binding_cannot_pass_with_removed_guard(self):
        (self.root/"adapter_guard_v4.py").unlink()
        self.purge_modules()
        gate=importlib.import_module("yard_execution_guard_v13")
        with self.assertRaises(gate.ExecutionDenied):
            gate.manager_preflight()

    def test_v14_cannot_read_without_ledger(self):
        (self.root/"yard_exec_bindings_v14.json").unlink()
        self.purge_modules()
        gate=importlib.import_module("yard_execution_guard_v13")
        with self.assertRaises((gate.ExecutionDenied,OSError)):
            gate.manager_preflight()

if __name__ == "__main__":
    unittest.main()
