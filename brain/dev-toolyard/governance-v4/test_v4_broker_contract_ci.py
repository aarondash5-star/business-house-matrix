"""Repository-CI-only broker contract tests using synthetic data.

No live host, private key, signers, actual release approval, or production
controller may be accessed here. Real SSH Ed25519 acceptance and detached
V1.3/V1.4 source tests remain mandatory independent release gates.
"""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import v4_internal_release_broker as broker


class SyntheticBrokerContractTests(unittest.TestCase):
    def setUp(self):
        self.root=tempfile.TemporaryDirectory()
        self.addCleanup(self.root.cleanup)
        base=Path(self.root.name)
        self.live=base/"matrix-controller"
        self.source=base/"governance-v4"
        self.journal=base/"journal"
        for d in (self.live,self.source,self.journal):
            d.mkdir(mode=0o700)
        self.approval_file=base/"owner-approval.json"
        self.signature=base/"owner-approval.json.sig"
        self.trust=base/"allowed_signers"
        self.paths=broker.BrokerPaths(self.live,self.source,self.approval_file,
                                      self.signature,self.trust,self.journal)
        self.gate="bb0339f48add0537771dec2b2e4898258bfd4bd7758e1648a62f10130a2ee3e3"
        self.approval={
            "schema":1,"host":"dell-linux","project":"matrix_dev_manager",
            "manifest":"matrix_v4_controller_v14","action":"internal_component_release",
            "source_commit":broker.REVIEWED_SOURCE_SHA,
            "adapter_sha256":broker.V4_ADAPTER_SHA,
            "guard_sha256":broker.V4_GUARD_SHA,
            "v14_gate_sha256":self.gate,
            "qa_receipts":list(broker.QA_RECEIPTS),
            "release_id":"v4-controller-20261026-aabbccddeeff",
            "expires_utc":(datetime.now(timezone.utc)+timedelta(minutes=15)).isoformat(),
            "production":False,"spend":False,"max_activations":1,
        }
        self.write()
        self.mock_source={"manifest":{"new_source_hashes":{
            "yard_execution_guard_v13.py":self.gate}}}

    def write(self):
        self.approval_file.write_bytes(broker._canonical(self.approval))
        self.approval_file.chmod(0o600)

    def assess_synthetic(self):
        with mock.patch.object(broker,"source_review",return_value=self.mock_source):
            with mock.patch.object(broker,"verify_signature",return_value=True):
                return broker.assess(self.paths)

    def test_exact_contract_only_in_synthetic_positive(self):
        x=self.assess_synthetic()
        self.assertTrue(x["source_bound"])
        self.assertFalse(x["production"])
        self.assertFalse(x["spend"])
        self.assertEqual(x["source_bindings"],21)

    def test_real_signature_missing_fail_closed(self):
        with mock.patch.object(broker,"source_review",return_value=self.mock_source):
            with self.assertRaises(broker.BrokerDenied):
                broker.assess(self.paths)
        self.assertEqual(list(self.journal.iterdir()),[])

    def test_wrong_host_denied(self):
        self.approval["host"]="mac-linux";self.write()
        with self.assertRaisesRegex(broker.BrokerDenied,"approval_scope_denied"):
            self.assess_synthetic()

    def test_other_project_denied(self):
        self.approval["project"]="andaz";self.write()
        with self.assertRaisesRegex(broker.BrokerDenied,"approval_scope_denied"):
            self.assess_synthetic()

    def test_broad_action_denied(self):
        self.approval["action"]="shell";self.write()
        with self.assertRaisesRegex(broker.BrokerDenied,"approval_scope_denied"):
            self.assess_synthetic()

    def test_production_flag_denied(self):
        self.approval["production"]=True;self.write()
        with self.assertRaisesRegex(broker.BrokerDenied,"approval_scope_denied"):
            self.assess_synthetic()

    def test_spending_flag_denied(self):
        self.approval["spend"]=True;self.write()
        with self.assertRaisesRegex(broker.BrokerDenied,"approval_scope_denied"):
            self.assess_synthetic()

    def test_multiple_activations_denied(self):
        self.approval["max_activations"]=2;self.write()
        with self.assertRaisesRegex(broker.BrokerDenied,"approval_scope_denied"):
            self.assess_synthetic()

    def test_expired_approval_denied(self):
        self.approval["expires_utc"]=(datetime.now(timezone.utc)-timedelta(minutes=1)).isoformat()
        self.write()
        with self.assertRaisesRegex(broker.BrokerDenied,"release_expired_or_unbounded"):
            self.assess_synthetic()

    def test_uncanonical_approval_denied(self):
        self.approval_file.write_text(json.dumps(self.approval,indent=2))
        with self.assertRaisesRegex(broker.BrokerDenied,"approval_not_canonical"):
            self.assess_synthetic()

    def test_mismatched_v14_gate_denied(self):
        self.approval["v14_gate_sha256"]="a"*64;self.write()
        with self.assertRaisesRegex(broker.BrokerDenied,"approval_candidate_gate_mismatch"):
            self.assess_synthetic()

    def test_duplicate_release_id_blocked(self):
        self.assertTrue(broker.ensure_replay_free(self.paths,self.approval["release_id"]))
        (self.journal/(self.approval["release_id"]+".reserved")).write_text("reserved")
        with self.assertRaisesRegex(broker.BrokerDenied,"single_use_release_already_claimed"):
            broker.ensure_replay_free(self.paths,self.approval["release_id"])

    def test_no_arbitrary_command(self):
        with self.assertRaisesRegex(broker.BrokerDenied,"invalid_fixed_action"):
            broker.assess(self.paths,mode="arbitrary_exec")

    def test_uncontrolled_signer_file_denied(self):
        self.trust.write_text("matrix-v4-release-owner ssh-ed25519 AAAA\n")
        self.trust.chmod(0o600)
        if self.trust.stat().st_uid != 0:
            with self.assertRaisesRegex(broker.BrokerDenied,"trust_store_not_independently_owned"):
                broker._trust_store(self.trust)

    def test_stage_requires_real_owner_signature(self):
        with mock.patch.object(broker,"source_review",return_value=self.mock_source):
            with self.assertRaises(broker.BrokerDenied):
                broker.stage_signed_release(self.paths)
        self.assertEqual(list(self.journal.iterdir()),[])


if __name__=="__main__":
    unittest.main()
