import unittest,tempfile,pathlib,importlib.util,json,io,contextlib,sqlite3,socket
from unittest.mock import patch,MagicMock
spec=importlib.util.spec_from_file_location('route',pathlib.Path(__file__).with_name('matrix-route.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class T(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);p=pathlib.Path(self.tmp.name)
  m.DB=p/'quota.db';m.VAULT=p/'vault';m.VAULT.mkdir();f=m.secret_path('groq-qwen-primary');f.write_text('synthetic-not-a-live-credential');f.chmod(0o600)
  self.s={'id':'groq-oss20','model':'openai/gpt-oss-20b','provider':'groq','credential_ref':'groq-qwen-primary'}
  self.policy=patch.object(m,'read_policy',return_value={'groq_free_plan_owner_confirmed':True});self.policy.start();self.addCleanup(self.policy.stop)
 def api(self,payload=None,error=None):
  obj=MagicMock();obj.open.return_value.__enter__.return_value.read.return_value=json.dumps(payload or {'model':self.s['model'],'choices':[{'message':{'content':'def add(a,b): return a+b'},'finish_reason':'stop'}],'usage':{'total_tokens':25}}).encode()
  if error:obj.open.side_effect=error
  return patch.object(m.urllib.request,'build_opener',return_value=obj)
 def test_private_denied(self):
  with self.assertRaisesRegex(RuntimeError,'PUBLIC_TEXT'):m.groq_text(self.s,'public')
 def test_tools_denied(self):
  with self.assertRaisesRegex(RuntimeError,'NO_TOOLS'):m.groq_text(self.s,'public',True,True)
 def test_missing_key(self):
  m.secret_path('groq-qwen-primary').unlink()
  with self.assertRaisesRegex(RuntimeError,'NO_SECURE'):m.groq_text(self.s,'public',False,True)
 def test_permissions(self):
  m.secret_path('groq-qwen-primary').chmod(0o644)
  with self.assertRaisesRegex(RuntimeError,'NO_SECURE'):m.groq_text(self.s,'public',False,True)
 def test_prompt_limit(self):
  with self.assertRaisesRegex(RuntimeError,'2048'):m.groq_text(self.s,'x'*2049,False,True)
 def test_attestation(self):
  m.read_policy.return_value={}
  with self.assertRaisesRegex(RuntimeError,'ATTESTATION'):m.groq_text(self.s,'public',False,True)
 def test_real_payload_bounds(self):
  with self.api() as op,contextlib.redirect_stdout(io.StringIO()):self.assertEqual(m.groq_text(self.s,'public',False,True),0)
  req=op.return_value.open.call_args.args[0];d=json.loads(req.data);self.assertEqual(d['max_completion_tokens'],1024);self.assertNotIn('tools',d);self.assertTrue(req.get_header('User-agent').startswith('BusinessHouseMatrixDev/'));self.assertEqual(req.full_url,'https://api.groq.com/openai/v1/chat/completions');self.assertEqual(op.return_value.open.call_args.kwargs['timeout'],15)
 def test_timeout(self):
  with self.api(error=socket.timeout()),contextlib.redirect_stderr(io.StringIO()):self.assertEqual(m.groq_text(self.s,'public',False,True),1)
 def test_incomplete(self):
  d={'choices':[{'message':{'content':'partial'},'finish_reason':'length'}]}
  with self.api(d),self.assertRaisesRegex(RuntimeError,'INCOMPLETE'):m.groq_text(self.s,'public',False,True)
 def test_shared_quota(self):
  with self.api(),contextlib.redirect_stdout(io.StringIO()):
   m.groq_text(self.s,'x'*2048,False,True);m.groq_text(self.s,'x'*2048,False,True)
   with self.assertRaisesRegex(RuntimeError,'TOKEN_BUDGET'):m.groq_text(self.s,'x'*2048,False,True)
 def test_redirect_denied(self):
  with self.api() as op,contextlib.redirect_stdout(io.StringIO()):m.groq_text(self.s,'public',False,True)
  handler=op.call_args.args[0]
  with self.assertRaisesRegex(RuntimeError,'REDIRECT'):handler.redirect_request(None,None,None,None,None,None)
if __name__=='__main__':unittest.main(verbosity=1)
