"""Real temporary filesystem recovery tests; NEVER tests live controller changes."""
import tempfile
from pathlib import Path
import unittest

from v4_fixed_host_rollback_rehearsal import (
    RehearsalDenied,ORIGINAL,CANDIDATE,digest,rehearse,write_atomic
)

class TestFixedHostRehearsal(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p=Path(self.tmp.name)
        self.live=p/"controller-fixture";self.live.mkdir()
        self.staged=p/"signed-candidate-fixture";self.staged.mkdir()
        self.backup=p/"private-backups";self.backup.mkdir()
        self.orig={n:("v13-original-"+n).encode() for n in ORIGINAL}
        self.next={n:("v14-candidate-"+n).encode() for n in CANDIDATE}
        self.old_pins={n:digest(b) for n,b in self.orig.items()}
        self.new_pins={n:digest(b) for n,b in self.next.items()}
        for n,b in self.orig.items():
            (self.live/n).write_bytes(b);(self.live/n).chmod(0o600)
        for n,b in self.next.items():
            (self.staged/n).write_bytes(b);(self.staged/n).chmod(0o600)
    def run_rehearsal(self,**x):
        args=dict(target=self.live,staged=self.staged,backup=self.backup,
                  old_pins=self.old_pins,new_pins=self.new_pins)
        args.update(x);return rehearse(**args)

    def test_all_successful_replacements_are_temp_only(self):
        r=self.run_rehearsal()
        self.assertEqual(r.status,"TEMP_FILES_REPLACED")
        self.assertEqual(r.applied,CANDIDATE)
        for name,data in self.next.items():self.assertEqual((self.live/name).read_bytes(),data)
        for name,data in self.orig.items():self.assertEqual((self.backup/name).read_bytes(),data)
        self.assertFalse(r.authenticated_release)
        self.assertFalse(r.live_controller_touched)
        self.assertFalse(r.systemd_touched)

    def test_each_failure_restores_all_originals(self):
        for fail in range(5):
            with self.subTest(fault_after=fail):
                with tempfile.TemporaryDirectory() as d:
                    sub=Path(d);t=sub/"live";t.mkdir();s=sub/"stage";s.mkdir();b=sub/"backup";b.mkdir()
                    for name,data in self.orig.items(): (t/name).write_bytes(data);(t/name).chmod(0o600)
                    for name,data in self.next.items(): (s/name).write_bytes(data);(s/name).chmod(0o600)
                    r=rehearse(t,s,b,self.old_pins,self.new_pins,fault_after=fail)
                    self.assertEqual(r.status,"TEMP_FILES_RESTORED")
                    self.assertTrue(r.restored_verified)
                    self.assertEqual({p.name for p in t.iterdir()},set(ORIGINAL))
                    for name,data in self.orig.items():
                        self.assertEqual((t/name).read_bytes(),data)
                        self.assertEqual((b/name).read_bytes(),data)
                    self.assertFalse(r.live_controller_touched)

    def test_source_sha_mismatch_fail_before_backup(self):
        p=self.live/ORIGINAL[0];p.write_bytes(b"unexpected live");p.chmod(0o600)
        with self.assertRaisesRegex(RehearsalDenied,"file_sha_drift"):
            self.run_rehearsal()
        self.assertEqual(list(self.backup.iterdir()),[])

    def test_candidate_sha_mismatch_denied(self):
        p=self.staged/CANDIDATE[1];p.write_bytes(b"unexpected");p.chmod(0o600)
        with self.assertRaisesRegex(RehearsalDenied,"file_sha_drift"):
            self.run_rehearsal()

    def test_symlink_candidate_denied(self):
        p=self.staged/CANDIDATE[1];p.unlink();p.symlink_to(self.live/ORIGINAL[0])
        with self.assertRaisesRegex(RehearsalDenied,"missing_or_symlink"):
            self.run_rehearsal()

    def test_untrusted_permissions_denied(self):
        p=self.live/ORIGINAL[0];p.chmod(0o666)
        with self.assertRaisesRegex(RehearsalDenied,"file_metadata_denied"):
            self.run_rehearsal()

    def test_second_attempt_denied_with_retained_backup(self):
        self.run_rehearsal()
        with self.assertRaisesRegex(RehearsalDenied,"backup_dir_must_be_empty"):
            self.run_rehearsal()

    def test_unlisted_manifest_denied(self):
        bad=dict(self.new_pins);bad["shell.sh"]="0"*64
        with self.assertRaisesRegex(RehearsalDenied,"unexpected_manifest_paths"):
            self.run_rehearsal(new_pins=bad)

    def test_boolean_fault_not_valid(self):
        with self.assertRaisesRegex(RehearsalDenied,"invalid_injected_fault"):
            self.run_rehearsal(fault_after=True)

    def test_live_controller_path_denied(self):
        with self.assertRaises(RehearsalDenied):
            self.run_rehearsal(target=Path("/var/lib/generic-linux-automator-exec/matrix-controller"))

if __name__=="__main__":
    unittest.main()
