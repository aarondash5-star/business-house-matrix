"""Adversarial and backwards-compatibility tests for live Dell V1.2 -> V4 rebase."""
from pathlib import Path
import ast
import json
import os
import sys
import types
import tempfile
import types
import unittest
from unittest import mock

from v4_rebase_live_v12 import (
    RebaseDenied,reconstruct_live_unchanged,rebase_current_live,
    sha,PREVIOUS_REVIEWED_V4_SHA,CURRENT_LIVE_ADAPTER_SHA,
    REBASED_ADAPTER_VERSION,REBASED_ADAPTER_SHA,render_guard_and_ledger
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

    def test_frozen_file_matches_exact_rebased_sha(self):
        frozen=(HERE/"yard_auto_adapter_v12_rebased_v14.py").read_bytes()
        self.assertEqual(sha(self.rebased),REBASED_ADAPTER_SHA)
        self.assertEqual(sha(frozen),REBASED_ADAPTER_SHA)
        self.assertEqual(frozen,self.rebased)

    def adapter(self, dirname):
        qa=types.ModuleType("toolyard_qa_standard_v1")
        qa.VERSION="test-qa-v1"
        qa.ACTION_PROFILES={}
        qa.REQUIREMENTS={}
        guarded=types.ModuleType("adapter_guard_v4")
        code=(HERE/"adapter_guard.py").read_text()
        exec(compile(code,str(HERE/"adapter_guard.py"),"exec"),guarded.__dict__)
        modules={"toolyard_qa_standard_v1":qa,"adapter_guard_v4":guarded}
        with mock.patch.dict(sys.modules,modules):
            scope={"__name__":"adapter_test_only","__file__":str(dirname/"yard_auto_adapter_v1.py")}
            exec(compile(self.rebased,str(dirname/"yard_auto_adapter_v1.py"),"exec"),scope)
            return scope,modules

    def test_guarded_load_and_save_with_real_v4_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);scope,modules=self.adapter(root)
            f=root/"registry.json"
            tools={"test-qa":{"operations":["probe_version"],"state":"accepted_qa_probe_only",
                              "production_live":False,"unbounded_execution_permitted":False}}
            payload={"schema":1,"tools":tools}
            f.write_text(json.dumps(payload))
            f.chmod(0o600)
            with mock.patch.dict(sys.modules,modules):
                self.assertEqual(scope["load"](f),tools)
                self.assertEqual(scope["save"](payload,f),f)
                self.assertEqual(scope["load"](f),tools)
                self.assertTrue((root/"yard-adapter-manifests-v1"/"test-qa.json").is_file())

    def test_invalid_registry_operations_fail_both_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);scope,modules=self.adapter(root)
            f=root/"registry.json";payload={"schema":1,"tools":{
                "test-qa":{"operations":["root_shell"],"state":"accepted_qa_probe_only"}}}
            f.write_text(json.dumps(payload));f.chmod(0o600)
            with mock.patch.dict(sys.modules,modules):
                with self.assertRaisesRegex(scope["AdapterDenied"],"registry_untrusted_operations"):
                    scope["load"](f)
                with self.assertRaisesRegex(scope["AdapterDenied"],"registry_save_bound_rejected"):
                    scope["save"](payload,root/"new-registry.json")
            self.assertFalse((root/"new-registry.json").exists())

    def test_513_tools_denied_preserving_v12_ceiling(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);scope,modules=self.adapter(root)
            f=root/"registry.json"
            tools={"qa-tool-"+str(i):{"operations":[],"state":"accepted_qa_probe_only"} for i in range(513)}
            p={"schema":1,"tools":tools}
            f.write_text(json.dumps(p));f.chmod(0o600)
            with mock.patch.dict(sys.modules,modules):
                with self.assertRaisesRegex(scope["AdapterDenied"],"registry_too_many_tools"):
                    scope["load"](f)
                with self.assertRaisesRegex(scope["AdapterDenied"],"registry_too_many_tools"):
                    scope["save"](p,root/"new-registry.json")

    def test_mutable_registry_is_denied(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);scope,modules=self.adapter(root)
            f=root/"registry.json";f.write_text(json.dumps({"schema":1,"tools":{}}))
            f.chmod(0o666)
            with mock.patch.dict(sys.modules,modules):
                with self.assertRaisesRegex(scope["AdapterDenied"],"registry_mutable"):
                    scope["load"](f)

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
