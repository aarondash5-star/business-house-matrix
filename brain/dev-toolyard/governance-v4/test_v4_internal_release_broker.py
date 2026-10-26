"""V4 internal-release broker tests. Synthetic approvals only; never edits live host."""
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

import v4_internal_release_broker as b

@unittest.skipUnless(os.environ.get("V4_RELEASE_FIXTURE_DIR"),"review fixture required")
class BrokerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root=Path(self.tmp.name)
        self.live=root/"matrix-controller"
        self.src=root/"governance-v4"
        self.journal=root/"journal"
        for d in (self.live,self.src,self.journal):
            d.mkdir(mode=0o700)
        fx=Path(os.environ["V4_RELEASE_FIXTURE_DIR"])
        for frm,to in (
            ("gate_v13.py",self.live/"yard_execution_guard_v13.py"),
            ("adapter_v1.py",self.live/"yard_auto_adapter_v1.py"),
            ("ledger_v13.json",self.live/"yard_exec_bindings_v13.json"),
            ("adapter_v4.py",self.src/"yard_auto_adapter_v1_patched.py"),
            ("guard_v4.py",self.src/"adapter_guard.py"),
        ):
            to.write_bytes((fx/frm).read_bytes())
            to.chmod(0o600)
        reviewed=b.source_review(self.live,self.src)
        self.approval={
            "schema":1, "host":b.HOST, "project":b.PROJECT,
            "manifest":b.MANIFEST, "action":b.ACTION,
            "source_commit":b.REVIEWED_SOURCE_SHA,
            "adapter_sha256":b.V4_ADAPTER_SHA, "guard_sha256":b.V4_GUARD_SHA,
            "v14_gate_sha256":reviewed["manifest"]["new_source_hashes"]["yard_execution_guard_v13.py"],
            "qa_receipts":list(b.QA_RECEIPTS),
            "release_id":"v4-controller-20261026-abcdefabcdef",
            "expires_utc":(datetime.now(timezone.utc)+timedelta(minutes=20)).isoformat(),
            "production":False,"spend":False,"max_activations":1,
        }
        self.doc=root/"owner-release.json"
        self.sig=root/"owner-release.sig"
        self.signers=root/"allowed_signers"
        self.sig.write_bytes(b"synthetic")
        self.sig.chmod(0o600)
        self.signers.write_text("no independently installed owner key\n")
        self.signers.chmod(0o600)
        self.paths=b.BrokerPaths(self.live,self.src,self.doc,self.sig,self.signers,self.journal)
        self.save()

    def save(self):
        self.doc.write_bytes(b._canonical(self.approval))
        self.doc.chmod(0o600)

    def assess(self):
        with mock.patch.object(b, "verify_signature", return_value=True):
            return b.assess(self.paths)

    def test_candidate_has_exact_21_source_pins(self):
        r=b.source_review(self.live,self.src)
        self.assertEqual(len(r["candidate_ledger"]["bindings"]),21)

    def test_verified_scope_positive_synthetic_only(self):
        q=self.assess()
        self.assertTrue(q["source_bound"])
        self.assertTrue(q["authenticated_owner_release"])
        self.assertFalse(q["production"])
        self.assertFalse(q["spend"])

    def test_no_owner_signature_fails_closed(self):
        with self.assertRaises(b.BrokerDenied):
            b.assess(self.paths)

    def test_missing_trust_root_denied(self):
        with self.assertRaises(b.BrokerDenied):
            b._trust_store(self.signers)

    def test_forged_project_denied(self):
        self.approval["project"]="pine_engineer"
        self.save()
        with self.assertRaisesRegex(b.BrokerDenied,"approval_scope_denied"):
            self.assess()

    def test_forged_host_denied(self):
        self.approval["host"]="mac-linux"
        self.save()
        with self.assertRaises(b.BrokerDenied):
            self.assess()

    def test_arbitrary_action_denied(self):
        self.approval["action"]="arbitrary_shell"
        self.save()
        with self.assertRaises(b.BrokerDenied):
            self.assess()

    def test_increase_activations_denied(self):
        self.approval["max_activations"]=2
        self.save()
        with self.assertRaises(b.BrokerDenied):
            self.assess()

    def test_release_permission_denied(self):
        self.approval["production"]=True
        self.save()
        with self.assertRaises(b.BrokerDenied):
            self.assess()

    def test_spending_denied(self):
        self.approval["spend"]=True
        self.save()
        with self.assertRaises(b.BrokerDenied):
            self.assess()

    def test_expired_approval_denied(self):
        self.approval["expires_utc"]=(datetime.now(timezone.utc)-timedelta(seconds=5)).isoformat()
        self.save()
        with self.assertRaises(b.BrokerDenied):
            self.assess()

    def test_qa_evidence_change_denied(self):
        self.approval["qa_receipts"]=[b.QA_RECEIPTS[0]]
        self.save()
        with self.assertRaises(b.BrokerDenied):
            self.assess()

    def test_source_guard_drift_denied(self):
        p=self.src/"adapter_guard.py"
        p.write_bytes(p.read_bytes()+b"\n# tampered")
        with self.assertRaises(b.ReleaseDenied):
            self.assess()

    def test_incorrect_v14_gate_hash_denied(self):
        self.approval["v14_gate_sha256"]="f"*64
        self.save()
        with self.assertRaises(b.BrokerDenied):
            self.assess()

    def test_noncanonical_json_denied(self):
        self.doc.write_text(json.dumps(self.approval,indent=2))
        with self.assertRaisesRegex(b.BrokerDenied,"approval_not_canonical"):
            self.assess()

    def test_cross_project_controller_directory_denied(self):
        wrong=b.BrokerPaths(self.live.parent/"andaz-controller",self.src,
                            self.doc,self.sig,self.signers,self.journal)
        with self.assertRaises(b.BrokerDenied):
            with mock.patch.object(b, "verify_signature", return_value=True):
                b.assess(wrong)

    def test_private_journal_requires_no_replay(self):
        self.assertTrue(b.ensure_replay_free(self.paths,self.approval["release_id"]))
        (self.journal/(self.approval["release_id"]+".reserved")).write_text("reserved")
        with self.assertRaises(b.BrokerDenied):
            b.ensure_replay_free(self.paths,self.approval["release_id"])

    def test_disabled_cli_command_scope(self):
        with self.assertRaisesRegex(b.BrokerDenied,"invalid_fixed_action"):
            b.assess(self.paths,mode="arbitrary_exec")

    def test_status_never_issues_authorization(self):
        s=b.status(self.live,self.src)
        self.assertEqual(s["candidate"],"pinned")
        self.assertIs(s["live_promotion"],False)
        self.assertIs(s["dispatch"],False)

    def test_signature_verifier_rejects_unsigned_data(self):
        with self.assertRaises(b.BrokerDenied):
            b.verify_signature(b._canonical(self.approval),self.sig,self.signers)

    def test_signed_fixture_can_stage_exact_backup_without_live_writes(self):
        original=(self.live/"yard_auto_adapter_v1.py").read_bytes()
        gate=(self.live/"yard_execution_guard_v13.py").read_bytes()
        with mock.patch.object(b, "verify_signature", return_value=True):
            result=b.stage_signed_release(self.paths)
        self.assertEqual(result["status"],"candidate_staged")
        self.assertFalse(result["host_write_authorized"])
        self.assertEqual((self.live/"yard_auto_adapter_v1.py").read_bytes(),original)
        self.assertEqual((self.live/"yard_execution_guard_v13.py").read_bytes(),gate)
        staged=self.journal/(self.approval["release_id"]+".candidate")
        self.assertEqual((staged/"v13-yard_auto_adapter_v1.py").read_bytes(),original)
        self.assertEqual((staged/"v13-yard_execution_guard_v13.py").read_bytes(),gate)
        self.assertEqual((staged/"v14-yard_auto_adapter_v1.py").read_bytes(),
                         (self.src/"yard_auto_adapter_v1_patched.py").read_bytes())
        self.assertTrue((self.journal/(self.approval["release_id"]+".reserved")).exists())
        self.assertTrue((staged/"stage-audit.json").is_file())
        self.assertFalse((self.live/"yard_exec_bindings_v14.json").exists())

    def test_staged_release_cannot_replay(self):
        with mock.patch.object(b,"verify_signature",return_value=True):
            b.stage_signed_release(self.paths)
            with self.assertRaisesRegex(b.BrokerDenied,"single_use_release_already_claimed"):
                b.stage_signed_release(self.paths)

    def test_stage_never_uses_unverified_signer(self):
        with self.assertRaises(b.BrokerDenied):
            b.stage_signed_release(self.paths)
        self.assertFalse(any(self.journal.iterdir()))

    def test_stage_fails_closed_if_live_old_source_modified(self):
        path=self.live/"yard_auto_adapter_v1.py"
        path.write_bytes(path.read_bytes()+b"#drift")
        with mock.patch.object(b,"verify_signature",return_value=True):
            with self.assertRaises(b.ReleaseDenied):
                b.stage_signed_release(self.paths)
        self.assertFalse(any(self.journal.iterdir()))

if __name__=="__main__":
    unittest.main()
