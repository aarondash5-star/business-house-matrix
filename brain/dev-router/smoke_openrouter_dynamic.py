"""Public demand-routing smoke: automatic classification, qualification, and isolated QA."""
import hashlib,json,pathlib,resource,subprocess,sys,tempfile
r=pathlib.Path.home()/'.local/share/matrix-dev-router'
prompt='Calculate parity. Return only Python source, no markdown: def is_even(n) returning a boolean for even integer n.'
checks='from answer import is_even\nassert is_even(2) is True\nassert is_even(3) is False\nassert is_even(0) is True\nassert is_even(-2) is True\nassert is_even(-3) is False\nassert is_even(100) is True'
p=subprocess.run([sys.executable,str(r/'matrix-route.py'),'run','--profile','auto','--public-input','--slot','openrouter-code','--no-fallback',prompt],capture_output=True,text=True,timeout=112)
trace=[x for x in p.stdout.splitlines() if x.startswith(('ROUTE ','OPENROUTER_MODEL ','OPENROUTER_DEMAND_QUALIFICATION '))]
receipt=r/'openrouter-dynamic-live.receipt.json'
if p.returncode:
 result={'status':'DYNAMIC_API_FAIL','exit':p.returncode,'trace':trace,'error':p.stderr[:200]}
 receipt.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));sys.exit(1)
d=json.loads(p.stdout.strip().splitlines()[-1]);source=d['text'].strip()
assert any('DEMAND_PROFILE reasoning' in x for x in trace),'automatic profile not used'
assert (d.get('usage') or {}).get('cost')==0,'zero cost receipt required'
if source.startswith('```') and source.endswith('```'):source='\n'.join(source.splitlines()[1:-1])
def limits():
 resource.setrlimit(resource.RLIMIT_CPU,(3,3));resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024));resource.setrlimit(resource.RLIMIT_FSIZE,(65536,65536))
with tempfile.TemporaryDirectory(prefix='matrix-demand-live-') as tmp:
 pathlib.Path(tmp,'answer.py').write_text(source)
 args=['/usr/bin/bwrap','--clearenv','--setenv','PATH','/usr/bin:/bin','--unshare-all','--die-with-parent','--new-session','--ro-bind','/usr','/usr','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/work','--ro-bind',tmp,'/work','--chdir','/work','/usr/bin/python3','-I','-S','-c',"import sys;sys.path.insert(0,'/work');\n"+checks]
 q=subprocess.run(args,capture_output=True,text=True,timeout=10,preexec_fn=limits)
 result={'status':'DYNAMIC_QA_PASS' if q.returncode==0 else 'DYNAMIC_QA_FAIL','model':d['model'],'usage':d.get('usage'),'trace':trace,'assertions':6,'qa_exit':q.returncode,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'sandbox':'bubblewrap-no-network-clearenv'}
 receipt.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));sys.exit(q.returncode)
