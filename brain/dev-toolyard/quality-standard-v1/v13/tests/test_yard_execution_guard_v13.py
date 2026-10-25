import json,hashlib,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import yard_execution_guard_v13 as g

class GuardSmoke(unittest.TestCase):
    def fixture(self):
        d=tempfile.TemporaryDirectory()
        data={'version':g.VERSION,'production_live':False,
              'external_paths_certified':False,
              'bindings':{x:g.digest(g.ROOT/x) for x in set(g.CORE+[g.MANAGER]+[p for xs in g.ACTIVE.values() for p in xs])}}
        f=Path(d.name)/'policy.json'
        f.write_text(json.dumps(data));f.chmod(0o600)
        self.addCleanup(d.cleanup)
        return f
    def test_action_coverage(self):
        from yard_auto_adapter_v1 import ACTION_PROFILES
        self.assertEqual(set(ACTION_PROFILES),set(g.ACTIVE)|{'marketing_draft','video_preview'})
    def test_controller_action_routes(self):
        f=self.fixture()
        for action in g.ACTIVE:
            with self.subTest(action=action):
                report=g.preflight('matrix_dev',action,'frozen_brief_v1',f)
                self.assertTrue(report['source_bound'])
                self.assertFalse(report['production_authorized'])
    def test_blocked_actions_remain_blocked(self):
        f=self.fixture()
        for a in ('marketing_draft','video_preview'):
            with self.assertRaises(g.ExecutionDenied):g.preflight('matrix_dev',a,'frozen_brief_v1',f)
    def test_unknown_action_denied(self):
        with self.assertRaises(g.ExecutionDenied):
            g.preflight('matrix_dev','arbitrary_shell','v1',self.fixture())
    def test_source_drift_denied(self):
        f=self.fixture();data=json.loads(f.read_text())
        data['bindings']['sandbox.py']='0'*64
        f.write_text(json.dumps(data))
        with self.assertRaisesRegex(g.ExecutionDenied,'hash_drift'):
            g.preflight('matrix_dev','sandbox_qa','batch_v1',f)
    def test_missing_source_binding_denied(self):
        f=self.fixture();data=json.loads(f.read_text())
        del data['bindings']['sandbox.py'];f.write_text(json.dumps(data))
        with self.assertRaises(g.ExecutionDenied):g.preflight('matrix_dev','sandbox_qa','b',f)
    def test_insecure_ledger_denied(self):
        f=self.fixture();f.chmod(0o666)
        with self.assertRaises(g.ExecutionDenied):g.manager_preflight(f)
    def test_manager_fails_closed_on_hash_drift(self):
        f=self.fixture();data=json.loads(f.read_text())
        data['bindings'][g.MANAGER]='0'*64;f.write_text(json.dumps(data))
        with self.assertRaisesRegex(g.ExecutionDenied,'hash_drift'):g.manager_preflight(f)
    def test_runtime_does_not_auto_authorize_production(self):
        f=self.fixture();data=json.loads(f.read_text());data['production_live']=True
        f.write_text(json.dumps(data))
        with self.assertRaises(g.ExecutionDenied):g.preflight('matrix_dev','sandbox_qa','b',f)
if __name__=='__main__':unittest.main(verbosity=2)
