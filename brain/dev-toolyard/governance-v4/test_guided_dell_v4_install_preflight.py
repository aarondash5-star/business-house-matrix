"""Read-only installer gate regressions. No host modifications or secrets."""
import importlib.util
import os
from pathlib import Path
import stat
import tempfile
import unittest

import guided_dell_v4_install_preflight as m

class GuidedPreflightTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home=Path(tmp.name)
        self.live=self.home/"matrix-controller"
        self.live.mkdir()
        self.trust=self.home/"etc"/"matrix-internal-release"/"allowed_signers"

    def test_missing_everything_blocks_and_never_installs(self):
        r=m.assess(self.home,"karan-Inspiron-5379",True,self.trust)
        self.assertFalse(r["ready_to_install"])
        self.assertFalse(r["release_authorized"])
        self.assertFalse(r["live_controller_changed"])
        self.assertFalse(r["credentials_requested"])
        self.assertFalse(r["privilege_changed"])
        self.assertIn("owner_signer_trust_valid",r["blockers"])
        self.assertIn("host_activation_runner_certified",r["blockers"])

    def test_host_is_strict(self):
        r=m.assess(self.home,"KARAN",True,self.trust)
        self.assertIn("exact_host",r["blockers"])

    def test_service_required(self):
        r=m.assess(self.home,"karan-Inspiron-5379",False,self.trust)
        self.assertIn("controller_service_active",r["blockers"])

    def test_hash_drift_detected(self):
        (self.live/"yard_auto_adapter_v1.py").write_text("new adapter")
        r=m.assess(self.home,"karan-Inspiron-5379",True,self.trust)
        self.assertFalse(r["checks"]["source_yard_auto_adapter_v1.py"])
        self.assertFalse(r["ready_to_install"])

    def test_symlink_live_dir_denied(self):
        self.live.rmdir()
        (self.home/"original").mkdir()
        self.live.symlink_to(self.home/"original",target_is_directory=True)
        r=m.assess(self.home,"karan-Inspiron-5379",True,self.trust)
        self.assertIn("controller_dir_not_symlink",r["blockers"])

    def test_symlink_source_denied(self):
        (self.live/"controller.py").symlink_to(__file__)
        self.assertIsNone(m.sha(self.live/"controller.py"))

    def test_user_written_signer_untrusted(self):
        self.trust.parent.mkdir(parents=True)
        self.trust.write_text("matrix-v4-release-owner ssh-ed25519 AAAA\n")
        if os.geteuid()!=0:
            self.assertFalse(m.trust_is_independent(self.trust))
        else:
            # Root-running CI fixture still fails if directory mode is unsafe.
            self.trust.parent.chmod(0o777)
            self.assertFalse(m.trust_is_independent(self.trust))

    def test_approval_file_presence_is_not_signature(self):
        d=self.home/".matrix-release-authorizations"
        d.mkdir(mode=0o700)
        for name in m.RELEASE_FILES:
            (d/name).write_text("FAKE")
            (d/name).chmod(0o600)
        r=m.assess(self.home,"karan-Inspiron-5379",True,self.trust)
        self.assertTrue(r["checks"]["owner_v4-owner-release.json_present"])
        self.assertFalse(r["checks"]["owner_signature_verified"])
        self.assertFalse(r["ready_to_install"])

    def test_never_activates_from_cli(self):
        self.assertEqual(m.main(["preflight"]),3)
        with self.assertRaises(SystemExit):
            m.main(["activate"])

if __name__=="__main__":
    unittest.main()
