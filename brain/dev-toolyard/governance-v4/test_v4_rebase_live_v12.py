"""Adversarial and backwards-compatibility tests for live Dell V1.2 -> V4 rebase."""
from pathlib import Path
import ast
import json
import os
import tempfile
import types
import unittest
from unittest import mock

from v4_rebase_live_v12 import (
    RebaseDenied,reconstruct_live_unchanged,rebase_current_live,
    sha,PREVIOUS_REVIEWED_V4_SHA,CURRENT_LIVE_ADAPTER_SHA,
    REBASED_ADAPTER_VERSION,render_guard_and_ledger
)

HERE=Path(__file__).resolve().parent
ORIGINAL=HERE/"yard_auto_adapter_v1_patched.py"

class RebaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old_v4=ORIGINAL.read_bytes()
        cls.actual=reconstruct_live_unchanged(cls.old_v4)
        cls.rebased=rebase_current_live(cls.actual)

    def test_legacy_review_exact_pin(self):
        self.assertEqual(sha(self.old_v4),PREVIOUS_REVIEWED_V4_SHA)

    def test_reconstructed_v12_matches_real_dell_sha(self):
        self.assertEqual(sha(self.actual),CURRENT_LIVE_ADAPTER_SHA)
        self.assertNotEqual(sha(self.old_v4),sha(self.rebased))

    def test_rebase_is_pure_and_compiles(self):
        self.assertNotEqual(self.actual,self.rebased)
        ast.parse(self.rebased)
        self.assertIn(REBASED_ADAPTER_VERSION.encode(),self.rebased)

    def test_original_live_capacity_preserved(self):
        for marker in (b"REGISTRY_MAX_BYTES=1_048_576",b"REGISTRY_MAX_TOOLS=512",
                       b"if len(d[\"tools\"])>REGISTRY_MAX_TOOLS:",
                       b"if len((json.dumps(d,sort_keys=True,indent=2)"):
            self.assertIn(marker,self.rebased)
        self.assertEqual(self.rebased.count(b"checked_registry("),2)

    def test_v4_guard_in_load_and_save(self):
        t=ast.parse(self.rebased)
        functions={n.name:n for n in t.body if isinstance(n,ast.FunctionDef)}
        self.assertIn("load",functions)
        self.assertIn("save",functions)
        load=ast.get_source_segment(self.rebased.decode(),functions["load"])
        save=ast.get_source_segment(self.rebased.decode(),functions["save"])
        self.assertIn("from adapter_guard_v4 import",load)
        self.assertIn("from adapter_guard_v4 import",save)
        self.assertIn("checked_registry(p)",load)
        self.assertIn("checked_registry(tmp)",save)

    def test_refuse_reviewed_source_drift(self):
        with self.assertRaisesRegex(RebaseDenied,"reviewed_v4_digest_drift"):
            reconstruct_live_unchanged(self.old_v4+b"#corruption")

    def test_refuse_host_source_drift(self):
        with self.assertRaisesRegex(RebaseDenied,"live_v12_adapter_drift"):
            rebase_current_live(self.actual+b"#changed")

    def test_rebased_preserves_guard_deny_flags(self):
        s=self.rebased.decode()
        for f in ('"production_authorized":False','"owner_release":False',
                  '"arbitrary_exec":False','"automatic_live":False'):
            self.assertIn(f,s)

    def test_old_unreviewed_ledger_denied_before_mutation(self):
        with self.assertRaisesRegex(RebaseDenied,"live_guard_digest_drift"):
            render_guard_and_ledger(b"not-guard",b"not-ledger",self.rebased,b"not-v4")

    def test_missing_reviewed_guard_denied(self):
        from v4_rebase_live_v12 import CURRENT_GUARD_SHA
        with mock.patch("v4_rebase_live_v12.CURRENT_GUARD_SHA",sha(b"test-control-guard")):
            with self.assertRaisesRegex(RebaseDenied,"live_ledger_digest_drift"):
                render_guard_and_ledger(b"test-control-guard",b"corrupt",self.rebased,b"guard")


@unittest.skipUnless(os.environ.get("V4_CURRENT_LIVE_FIXTURE_DIR"),
                     "Requires independent read-only actual Dell V1.2 gate and ledger fixture")
class SourceAndLedgerReadOnlyFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path(os.environ["V4_CURRENT_LIVE_FIXTURE_DIR"])
        cls.guard=(root/"yard_execution_guard_v13.py").read_bytes()
        cls.ledger=(root/"yard_exec_bindings_v13.json").read_bytes()
        cls.reviewed_guard=(HERE/"adapter_guard.py").read_bytes()
        cls.rebased=rebase_current_live(reconstruct_live_unchanged(ORIGINAL.read_bytes()))

    def test_reviewed_real_ledger_and_guard(self):
        x=render_guard_and_ledger(self.guard,self.ledger,self.rebased,self.reviewed_guard)
        self.assertEqual(x["mode"],"SOURCE_REBASE_ONLY")
        self.assertEqual(x["source_pins"]["rebased_binding_count"],21)
        self.assertFalse(x["release_authorized"])
        self.assertFalse(x["controller_mutated"])
        self.assertEqual(x["ledger"]["bindings"]["yard_auto_adapter_v1.py"],sha(self.rebased))
        self.assertIn("adapter_guard_v4.py",x["ledger"]["bindings"])

if __name__=="__main__":
    unittest.main()
