import json,tempfile,unittest,sys
from unittest import mock
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import yard_auto_adapter_v1 as yard

class Tests(unittest.TestCase):
 def test_existing_13_actions_inherit(self):
    for action in yard.ACTION_PROFILES:
      with self.subTest(action=action):
        r=yard.inherit('delulu_tech',action,'v2')
        self.assertTrue(r['automatically_attached'])
        self.assertFalse(r['production_authorized'])
        self.assertTrue(r['mandatory_checks'])
 def test_unknown_actions_denied(self):
    with self.assertRaises(yard.AdapterDenied):yard.inherit('delulu_tech','arbitrary_shell','v2')
 def test_unknown_tool_quarantined(self):
    with mock.patch.object(yard,'discover',return_value={
        'vercel':{'binary':'/usr/bin/echo','sha256':'f'*64}}):
      report=yard.reconcile(prober=lambda n,d:(True,'pass'))
    self.assertEqual(report['tools']['vercel']['state'],'quarantined_needs_certification')
    self.assertFalse(report['tools']['vercel']['production_live'])
 def test_builtin_auto_qa_only(self):
    with mock.patch.object(yard,'discover',return_value={
        'python3':{'binary':'/usr/bin/python3','sha256':'a'*64}}):
      report=yard.reconcile(prober=lambda n,d:(True,'tested'))
    self.assertEqual(report['tools']['python3']['operations'],['probe_version'])
    self.assertFalse(report['tools']['python3']['unbounded_execution_permitted'])
 def test_admission_refuses_arbitrary_operation(self):
    with self.assertRaisesRegex(yard.AdapterDenied,'operation_not_certified'):
      yard.preflight('python3','run_any_command')
 def test_changed_binary_denied(self):
    x=yard.discover()
    if 'python3' not in x: self.skipTest('python not on PATH')
    report=yard.reconcile(prober=lambda n,d:(True,'test_only'))
    with tempfile.TemporaryDirectory() as t:
      db=Path(t)/'registry.json';yard.save(report,db)
      with self.assertRaisesRegex(yard.AdapterDenied,'binary_changed'):
        yard.preflight('python3','probe_version',db,
          which=lambda n:'/usr/bin/git')
 def test_missing_tool_not_approved(self):
    with tempfile.TemporaryDirectory() as t:
      db=Path(t)/'registry.json';yard.save(yard.reconcile(prober=lambda n,d:(True,'test')),db)
      with self.assertRaises(yard.AdapterDenied):
        yard.preflight('ghost_cli','probe_version',db)
 def test_secure_registry_and_readback(self):
    with tempfile.TemporaryDirectory() as t:
      db=Path(t)/'reg.json'
      v=yard.reconcile(prober=lambda n,d:(True,'test'))
      yard.save(v,db)
      self.assertEqual(db.stat().st_mode&0o777,0o600)
      self.assertTrue(yard.load(db))
 def test_no_automatic_production(self):
    r=yard.reconcile(prober=lambda n,d:(True,'test'))
    self.assertFalse(r['automatic_live'])
    self.assertFalse(r['direct_ssh_intercepted'])
    self.assertTrue(all(not x.get('production_live') for x in r['tools'].values()))
 def test_scaffolds_and_syntax_only_admission(self):
    with tempfile.TemporaryDirectory() as t:
      registry=Path(t)/"db.json"
      source=Path(yard.HERE)/"yard_auto_adapter_v1.py"
      name="yard-yard_auto_adapter_v1"
      with mock.patch.object(yard,"discover",return_value={
          name:{"binary":str(source),"sha256":yard.sha(source),
                "inventory":"direct_script_unreviewed"}}):
        report=yard.reconcile()
      self.assertEqual(report["tools"][name]["operations"],["syntax_probe"])
      self.assertFalse(report["tools"][name]["production_live"])
      yard.save(report,registry)
      detail=json.loads((Path(t)/"yard-adapter-manifests-v1"/(name+".json")).read_text())
      self.assertEqual(detail["verified_operations"],["syntax_probe"])
      self.assertFalse(detail["arbitrary_exec"])
      self.assertEqual(yard.preflight(name,"syntax_probe",registry)["sha256"],yard.sha(source))
if __name__=="__main__":unittest.main(verbosity=2)
