import json,os,tempfile,unittest
from pathlib import Path
from unittest import mock
import yard_execution_guard_v13 as guard
import yard_auto_adapter_v1 as yard

class AdversarialV13(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for name in ('quality.py','manager.py','target.py'):
            (self.root/name).write_text('value=1\n')
        self.bindings={name:guard.digest(self.root/name) for name in ('quality.py','manager.py','target.py')}
        self.ledger=self.root/'ledger.json'
        self.ledger.write_text(json.dumps({'version':guard.VERSION,
            'production_live':False,'external_paths_certified':False,'bindings':self.bindings}))
        self.ledger.chmod(0o600)
        self.patches=[
         mock.patch.object(guard,'ROOT',self.root),
         mock.patch.object(guard,'ACTIVE',{'sandbox_qa':['target.py'],'research_search':['target.py']}),
         mock.patch.object(guard,'CORE',['quality.py']),
         mock.patch.object(guard,'MANAGER','manager.py')]
        for p in self.patches:
            p.start();self.addCleanup(p.stop)
    def test_good_bound_route_not_a_release(self):
        result=guard.preflight('matrix_dev','sandbox_qa','qa_v1',self.ledger)
        self.assertTrue(result['source_bound'])
        self.assertFalse(result['production_authorized'])
        self.assertFalse(result['unmanaged_ssh_or_connectors_certified'])
    def test_unknown_action_quarantined(self):
        with self.assertRaises(guard.ExecutionDenied):
            guard.preflight('matrix_dev','arbitrary_shell','qa_v1',self.ledger)
    def test_default_blocked_route_remains_denied(self):
        with self.assertRaises(guard.ExecutionDenied):
            guard.preflight('matrix_dev','video_preview','qa_v1',self.ledger)
    def test_source_drift_fail_closed(self):
        (self.root/'target.py').write_text('value=2\n')
        with self.assertRaisesRegex(guard.ExecutionDenied,'hash_drift'):
            guard.preflight('matrix_dev','sandbox_qa','qa_v1',self.ledger)
    def test_manager_import_guard_hash(self):
        self.assertTrue(guard.manager_preflight(self.ledger))
        (self.root/'manager.py').write_text('changed\n')
        with self.assertRaises(guard.ExecutionDenied):
            guard.manager_preflight(self.ledger)
    def test_ledger_cannot_grant_production(self):
        data=json.loads(self.ledger.read_text());data['production_live']=True
        self.ledger.write_text(json.dumps(data))
        with self.assertRaises(guard.ExecutionDenied):
            guard.preflight('matrix_dev','sandbox_qa','qa_v1',self.ledger)
    def test_unreviewed_binding_rejected(self):
        data=json.loads(self.ledger.read_text());del data['bindings']['target.py']
        self.ledger.write_text(json.dumps(data))
        with self.assertRaises(guard.ExecutionDenied):
            guard.preflight('matrix_dev','sandbox_qa','qa_v1',self.ledger)
    def test_auto_reconcile_drift_is_not_reacceptance(self):
        old={'python3':{'sha256':'0'*64,'state':'accepted_qa_probe_only',
                        'operations':['probe_version'],'production_live':False}}
        with mock.patch.object(yard,'discover',return_value={
            'python3':{'binary':'/usr/bin/python3','sha256':'f'*64}}):
            r=yard.reconcile(old=old,prober=lambda *a:(True,'passed'))
            self.assertEqual(r['tools']['python3']['state'],'quarantined_source_drift')
            self.assertEqual(r['tools']['python3']['operations'],[])
            rr=yard.reconcile(old=r['tools'],prober=lambda *a:(True,'passed'))
            self.assertEqual(rr['tools']['python3']['operations'],[])
if __name__=='__main__':unittest.main()
