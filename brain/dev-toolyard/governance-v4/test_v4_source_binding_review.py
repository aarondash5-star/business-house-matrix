"""Adversarial tests for V4 shared promotion candidate. No host mutation.

Set V4_RELEASE_FIXTURE_DIR to a private read-only fixture containing copies of:
gate_v13.py, adapter_v1.py, adapter_v4.py, guard_v4.py, ledger_v13.json.
"""
import json
import os
from pathlib import Path
import unittest
from copy import deepcopy

from v4_source_binding_review import (
    ReleaseDenied, render_candidate, inspect_candidate,
    V13, V14, OLD_ADAPTER_SHA, V4_ADAPTER_SHA, V4_GUARD_SHA, digest
)


@unittest.skipUnless(os.environ.get("V4_RELEASE_FIXTURE_DIR"), "pinned local fixture required")
class ReleaseReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(os.environ["V4_RELEASE_FIXTURE_DIR"])
        cls.gate=(root/"gate_v13.py").read_bytes()
        cls.old=(root/"adapter_v1.py").read_bytes()
        cls.new=(root/"adapter_v4.py").read_bytes()
        cls.guard=(root/"guard_v4.py").read_bytes()
        cls.ledger=json.loads((root/"ledger_v13.json").read_text())

    def candidate(self, **values):
        kwargs={"original_gate":self.gate,"original_adapter":self.old,
                "reviewed_adapter":self.new,"reviewed_guard":self.guard,
                "pinned_ledger":deepcopy(self.ledger)}
        kwargs.update(values)
        return render_candidate(**kwargs)

    def test_real_source_candidate_passes(self):
        result=inspect_candidate(self.candidate())
        self.assertEqual(result["bound_sources"],21)
        self.assertFalse(result["host_write_authorized"])

    def test_pins_are_exact(self):
        self.assertEqual(digest(self.old),OLD_ADAPTER_SHA)
        self.assertEqual(digest(self.new),V4_ADAPTER_SHA)
        self.assertEqual(digest(self.guard),V4_GUARD_SHA)

    def test_bind_guard_new_source(self):
        candidate=self.candidate()
        self.assertEqual(candidate["candidate_ledger"]["bindings"]["adapter_guard_v4.py"],V4_GUARD_SHA)
        self.assertEqual(candidate["candidate_ledger"]["bindings"]["yard_auto_adapter_v1.py"],V4_ADAPTER_SHA)
        self.assertEqual(candidate["candidate_ledger"]["version"],V14)

    def test_nonproduction_no_dispatch(self):
        candidate=self.candidate()
        self.assertEqual(candidate["authorization"],"owner_signed_release_action_missing")
        self.assertFalse(candidate["manifest"]["shared_controller_promotion"])
        self.assertFalse(candidate["manifest"]["production"])
        self.assertFalse(candidate["manifest"]["spend"])
        self.assertEqual(candidate["manifest"]["phase"],"v4_review_only")

    def test_rollback_original_preserved(self):
        candidate=self.candidate()
        self.assertEqual(candidate["rollback_pins"]["yard_auto_adapter_v1.py"],OLD_ADAPTER_SHA)
        self.assertEqual(candidate["rollback_pins"]["yard_execution_guard_v13.py"],
                         digest(self.gate))
        self.assertEqual(self.ledger["version"],V13)

    def test_gate_update_is_only_expected_items(self):
        candidate=self.candidate()
        source=candidate["source"]["yard_execution_guard_v13.py"].decode()
        self.assertIn("adapter_guard_v4.py",source)
        self.assertIn("yard_exec_bindings_v14.json",source)
        self.assertIn(V14,source)
        self.assertEqual(source.count("adapter_guard_v4.py"),1)

    def test_controller_guard_source_drift_denied(self):
        with self.assertRaisesRegex(ReleaseDenied,"gate_source_drift"):
            self.candidate(original_gate=self.gate+b"\n# drift")

    def test_old_adapter_source_drift_denied(self):
        with self.assertRaisesRegex(ReleaseDenied,"old_adapter_drift"):
            self.candidate(original_adapter=self.old+b"\n")

    def test_new_adapter_source_drift_denied(self):
        with self.assertRaisesRegex(ReleaseDenied,"v4_adapter_drift"):
            self.candidate(reviewed_adapter=self.new+b"\n")

    def test_v4_guard_source_drift_denied(self):
        with self.assertRaisesRegex(ReleaseDenied,"new_guard_drift"):
            self.candidate(reviewed_guard=self.guard+b"\n")

    def test_production_toggle_denied(self):
        d=deepcopy(self.ledger);d["production_live"]=True
        with self.assertRaisesRegex(ReleaseDenied,"untrusted_existing_policy"):
            self.candidate(pinned_ledger=d)

    def test_external_tools_toggle_denied(self):
        d=deepcopy(self.ledger);d["external_paths_certified"]=True
        with self.assertRaisesRegex(ReleaseDenied,"untrusted_existing_policy"):
            self.candidate(pinned_ledger=d)

    def test_source_sha_drift_denied(self):
        d=deepcopy(self.ledger)
        d["bindings"]["yard_auto_adapter_v1.py"]="0"*64
        with self.assertRaisesRegex(ReleaseDenied,"untrusted_existing_policy"):
            self.candidate(pinned_ledger=d)

    def test_extra_binding_denied(self):
        d=deepcopy(self.ledger);d["bindings"]["new_unreviewed_worker.py"]="a"*64
        with self.assertRaisesRegex(ReleaseDenied,"unexpected_binding_scope"):
            self.candidate(pinned_ledger=d)

    def test_candidate_does_not_self_authorize(self):
        d=self.candidate()
        d["authorization"]="auto-approved"
        with self.assertRaisesRegex(ReleaseDenied,"candidate_authority_violation"):
            inspect_candidate(d)

    def test_candidate_tampering_denied(self):
        d=self.candidate()
        d["source"]["yard_auto_adapter_v1.py"]+=b"#tamper\n"
        with self.assertRaisesRegex(ReleaseDenied,"source_integrity_drift"):
            inspect_candidate(d)


if __name__=="__main__":
    unittest.main()
