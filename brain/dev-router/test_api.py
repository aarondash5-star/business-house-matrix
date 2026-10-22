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
class N(T):
 def test_development_gate(self):
  self.s.update(id='nvidia-oss20',provider='nvidia',model='openai/gpt-oss-20b')
  with self.assertRaisesRegex(RuntimeError,'DEVELOPMENT_TEST'):m.nvidia_text(self.s,'public',False,True)
 def test_nvidia_payload(self):
  self.s.update(id='nvidia-oss20',provider='nvidia',model='openai/gpt-oss-20b');m.read_policy.return_value={'nvidia_free_development_owner_confirmed':True}
  with self.api() as op,contextlib.redirect_stdout(io.StringIO()):self.assertEqual(m.nvidia_text(self.s,'public',False,True,True),0)
  req=op.return_value.open.call_args.args[0];body=json.loads(req.data);self.assertIn('max_tokens',body);self.assertNotIn('max_completion_tokens',body);self.assertEqual(req.full_url,'https://integrate.api.nvidia.com/v1/chat/completions');self.assertEqual(op.return_value.open.call_args.kwargs['timeout'],45)
 def test_license_gate(self):
  self.s.update(provider='nvidia',model='nvidia/nemotron-3-ultra-550b-a55b',license_review_required=True)
  with self.assertRaisesRegex(RuntimeError,'LICENSE_GATE'):m.nvidia_text(self.s,'public',False,True,True)
class O(unittest.TestCase):
 api=T.api
 def setUp(self):
  T.setUp(self)
  self.s.update(id='openrouter-code',provider='openrouter',model='cohere/north-mini-code:free')
  m.read_policy.return_value={'openrouter_free_only_owner_confirmed':True,'groq_free_plan_owner_confirmed':True}
 def test_paid_model_rejected_before_network_or_budget(self):
  self.s['model']='cohere/north-mini-code'
  with self.api() as op,self.assertRaisesRegex(RuntimeError,'MODEL_DENIED'):m.openrouter_text(self.s,'public',False,True)
  op.assert_not_called();self.assertFalse(m.DB.exists())
 def test_private_and_tools_rejected_before_network(self):
  with self.api() as op:
   with self.assertRaisesRegex(RuntimeError,'PUBLIC_TEXT'):m.openrouter_text(self.s,'private')
   with self.assertRaisesRegex(RuntimeError,'NO_TOOLS'):m.openrouter_text(self.s,'public',True,True)
  op.assert_not_called();self.assertFalse(m.DB.exists())
 def test_free_price_privacy_and_deadline_contract(self):
  with self.api() as op,contextlib.redirect_stdout(io.StringIO()):self.assertEqual(m.openrouter_text(self.s,'public',False,True),0)
  req=op.return_value.open.call_args.args[0];body=json.loads(req.data)
  self.assertEqual(req.full_url,'https://openrouter.ai/api/v1/chat/completions')
  self.assertEqual(body['model'],'cohere/north-mini-code:free')
  self.assertEqual(body['provider'],{'data_collection':'deny','max_price':{'prompt':0,'completion':0}})
  self.assertEqual(body['max_tokens'],1024);self.assertEqual(body['plugins'],[])
  for k in ('tools','models','route','reasoning_effort','max_completion_tokens'):self.assertNotIn(k,body)
  self.assertEqual(op.return_value.open.call_args.kwargs['timeout'],30)
 def test_symlink_key_rejected(self):
  p=m.secret_path('groq-qwen-primary');p.rename(p.with_suffix('.other'));p.symlink_to(p.with_suffix('.other'))
  with self.api() as op,self.assertRaisesRegex(RuntimeError,'NO_SECURE'):m.openrouter_text(self.s,'public',False,True)
  op.assert_not_called()
 def test_oversized_response_rejected(self):
  with self.api() as op:
   op.return_value.open.return_value.__enter__.return_value.read.return_value=b'x'*65537
   with self.assertRaisesRegex(RuntimeError,'TOO_LARGE'):m.openrouter_text(self.s,'public',False,True)
 def test_unexpected_model_and_nonzero_cost_rejected(self):
  for model,cost,err in [('other/model',0,'UNEXPECTED_MODEL'),('cohere/north-mini-code',0.01,'UNEXPECTED_COST')]:
   data={'model':model,'choices':[{'message':{'content':'source'},'finish_reason':'stop'}],'usage':{'cost':cost}}
   with self.api(data),self.assertRaisesRegex(RuntimeError,err):m.openrouter_text(self.s,'public',False,True)
 def test_budget_is_separate_from_groq(self):
  c=m.conn();c.execute('CREATE TABLE token_reservations(ts INTEGER,budget INTEGER)');c.execute('INSERT INTO token_reservations VALUES(?,80000)',(m.now(),));c.close()
  with self.api(),contextlib.redirect_stdout(io.StringIO()):self.assertEqual(m.openrouter_text(self.s,'public',False,True),0)
  c=m.conn();self.assertEqual(c.execute('SELECT sum(budget) FROM token_reservations').fetchone()[0],80000)
  self.assertGreater(c.execute('SELECT sum(budget) FROM openrouter_token_reservations').fetchone()[0],0);c.close()
 def test_429_is_sanitized_without_echoing_provider_body(self):
  error=m.urllib.error.HTTPError('https://openrouter.ai/api/v1/chat/completions',429,'synthetic-private-body',{},None)
  out=io.StringIO()
  with self.api(error=error),contextlib.redirect_stderr(out):self.assertEqual(m.openrouter_text(self.s,'public',False,True),1)
  self.assertEqual(out.getvalue(),'OPENROUTER_HTTP_429\n')
 def test_key_check_only_prints_allowlisted_metadata(self):
  data={'data':{'label':'synthetic-sensitive-label','free_model_daily_requests':{'remaining':7,'unexpected':'synthetic-private'},'is_management_key':False}}
  out=io.StringIO()
  with self.api(data) as op,contextlib.redirect_stdout(out):m.verify_openrouter(self.s)
  self.assertEqual(op.return_value.open.call_args.args[0].full_url,'https://openrouter.ai/api/v1/key')
  self.assertNotIn('synthetic-',out.getvalue());self.assertEqual(json.loads(out.getvalue())['free_model_daily_requests'],{'remaining':7})
 def test_cli_private_route_rejects_before_reservation(self):
  m.read_policy.return_value={'connections':[self.s]}
  with patch.object(m.sys,'argv',['matrix-route.py','run','--slot',self.s['id'],'private']),self.assertRaisesRegex(RuntimeError,'PUBLIC_INPUT'):
   m.main()
  c=m.conn();self.assertEqual(c.execute('SELECT count(*) FROM events').fetchone()[0],0);c.close()
 def test_http200_error_envelope_is_sanitized(self):
  out=io.StringIO()
  with self.api({'error':{'code':503,'message':'synthetic-private-body'}}),contextlib.redirect_stderr(out):self.assertEqual(m.openrouter_text(self.s,'public',False,True),1)
  self.assertEqual(out.getvalue(),'OPENROUTER_API_ERROR_503\n')
 def test_http200_rate_limit_sets_account_cooldown(self):
  with self.api({'error':{'code':429,'message':'synthetic-private-body'}}),contextlib.redirect_stderr(io.StringIO()):self.assertEqual(m.openrouter_text(self.s,'public',False,True),1)
  c=m.conn();until=c.execute('SELECT until_epoch FROM cooldowns WHERE slot=?',(self.s['id'],)).fetchone()[0];c.close()
  self.assertGreaterEqual(until,m.now()+895)
 def test_missing_choices_is_safe_provider_failure(self):
  for data in ({'choices':[]},{'unexpected':'synthetic-private-body'}):
   out=io.StringIO()
   with self.api(data),contextlib.redirect_stderr(out):self.assertEqual(m.openrouter_text(self.s,'public',False,True),1)
   self.assertEqual(out.getvalue(),'OPENROUTER_INVALID_COMPLETION_ENVELOPE\n')
if __name__=='__main__':unittest.main(verbosity=1)


