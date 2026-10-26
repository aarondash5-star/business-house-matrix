"""Offline release transaction simulator: interruption, restoration and pin denial."""
import unittest

from v4_in_memory_release_transaction import (
    ModelDenied,OLD_NAMES,ORDER,NEW_NAMES,digest,simulate
)

class InMemoryRollbackTests(unittest.TestCase):
    def setUp(self):
        self.old={name:("V1.3-original-"+name).encode() for name in OLD_NAMES}
        self.candidate={name:("V1.4-reviewed-"+name).encode() for name in NEW_NAMES}
        self.old_pins={k:digest(v) for k,v in self.old.items()}
        self.candidate_pins={k:digest(v) for k,v in self.candidate.items()}

    def run_model(self,fail_after=None,**changes):
        opts=dict(old=self.old,candidate=self.candidate,
                  old_pins=self.old_pins,candidate_pins=self.candidate_pins,
                  fail_after=fail_after)
        opts.update(changes)
        return simulate(**opts)

    def test_four_file_source_only_apply(self):
        r=self.run_model()
        self.assertEqual(r.outcome,"SIMULATED_APPLY_SUCCESS")
        self.assertEqual(r.staged,ORDER)
        self.assertTrue(r.applied_state_pins_verified)
        self.assertFalse(r.signing_verified)
        self.assertFalse(r.deployed)
        self.assertFalse(r.service_restarted)
        self.assertTrue(r.simulation_only)

    def test_original_guard_must_be_final_write(self):
        self.assertEqual(ORDER[-1],"yard_execution_guard_v13.py")
        self.assertLess(ORDER.index("adapter_guard_v4.py"),ORDER.index("yard_execution_guard_v13.py"))
        self.assertLess(ORDER.index("yard_exec_bindings_v14.json"),ORDER.index("yard_execution_guard_v13.py"))

    def test_faults_after_every_phase_restore_all_originals(self):
        for i in range(5):
            with self.subTest(fault_after=i):
                r=self.run_model(fail_after=i)
                self.assertEqual(r.outcome,"SIMULATED_ROLLBACK_SUCCESS")
                self.assertTrue(r.old_state_identical)
                self.assertEqual(set(r.restored),OLD_NAMES)
                self.assertFalse(r.deployed)
                self.assertFalse(r.signing_verified)

    def test_wrong_adapter_sha_denied(self):
        bad=dict(self.old_pins);bad["yard_auto_adapter_v1.py"]="0"*64
        with self.assertRaisesRegex(ModelDenied,"old_hash_drift"):
            self.run_model(old_pins=bad)

    def test_wrong_new_gate_sha_denied(self):
        bad=dict(self.candidate_pins);bad["yard_execution_guard_v13.py"]="f"*64
        with self.assertRaisesRegex(ModelDenied,"candidate_hash_drift"):
            self.run_model(candidate_pins=bad)

    def test_missing_old_original_denied(self):
        bad=dict(self.old);bad.pop("yard_exec_bindings_v13.json")
        with self.assertRaisesRegex(ModelDenied,"unexpected_old_file_set"):
            self.run_model(old=bad)

    def test_unlisted_new_file_denied(self):
        bad=dict(self.candidate);bad["shell_runner.sh"]=b"malicious"
        with self.assertRaisesRegex(ModelDenied,"unexpected_candidate_file_set"):
            self.run_model(candidate=bad)

    def test_nonbytes_payload_denied(self):
        bad=dict(self.candidate);bad["adapter_guard_v4.py"]="untrusted string"
        with self.assertRaisesRegex(ModelDenied,"invalid_candidate_data"):
            self.run_model(candidate=bad)

    def test_empty_candidate_denied(self):
        bad=dict(self.candidate);bad["adapter_guard_v4.py"]=b""
        with self.assertRaisesRegex(ModelDenied,"invalid_candidate_data"):
            self.run_model(candidate=bad)

    def test_oversized_candidate_denied(self):
        bad=dict(self.candidate);bad["adapter_guard_v4.py"]=b"x"*2000001
        with self.assertRaisesRegex(ModelDenied,"invalid_candidate_data"):
            self.run_model(candidate=bad)

    def test_bad_fault_step_denied(self):
        for value in (-1,5,True,"2",1.5):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ModelDenied,"invalid_fault_step"):
                    self.run_model(fail_after=value)

    def test_inputs_are_not_mutated(self):
        before_old=dict(self.old);before_new=dict(self.candidate)
        self.run_model()
        self.run_model(fail_after=4)
        self.assertEqual(self.old,before_old)
        self.assertEqual(self.candidate,before_new)

if __name__=="__main__":
    unittest.main()
