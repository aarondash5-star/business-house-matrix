import pathlib,subprocess,sys,json,tempfile,resource
r=pathlib.Path.home()/'.local/share/matrix-dev-router';slot=sys.argv[1]
fixtures={
 'groq-oss120':('Return only Python source, no markdown: def add(a,b) returning their sum.','from answer import add\nassert add(2,3)==5\nassert add(-1,1)==0\nassert add(0,0)==0\nassert add(-2,-4)==-6\nassert add(1.5,2)==3.5\nassert add(10,-3)==7'),
 'groq-qwen-primary':('Return only Python source, no markdown: def clamp(x, low, high) bounding x inclusively. Assume low <= high.','from answer import clamp\nassert clamp(2,0,4)==2\nassert clamp(-1,0,4)==0\nassert clamp(9,0,4)==4\nassert clamp(0,0,4)==0\nassert clamp(4,0,4)==4\nassert clamp(3,2,2)==2'),
 'groq-oss20':('Return only Python source, no markdown: def is_even(n) returning a boolean for even integer n.','from answer import is_even\nassert is_even(2) is True\nassert is_even(3) is False\nassert is_even(0) is True\nassert is_even(-2) is True\nassert is_even(-3) is False\nassert is_even(100) is True')}
prompt,checks=fixtures[slot]
p=subprocess.run([sys.executable,str(r/'matrix-route.py'),'run','--public-input','--slot',slot,'--no-fallback',prompt],capture_output=True,text=True,timeout=40)
if p.returncode:print(json.dumps({'slot':slot,'status':'API_FAIL','detail':p.stderr[:200]}));sys.exit(1)
d=json.loads(p.stdout.strip().splitlines()[-1]);source=d['text'].strip()
if source.startswith('```') and source.endswith('```'):source='\n'.join(source.splitlines()[1:-1])
def limits():
 resource.setrlimit(resource.RLIMIT_CPU,(3,3));resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024));resource.setrlimit(resource.RLIMIT_FSIZE,(65536,65536))
with tempfile.TemporaryDirectory(prefix='matrix-groq-qa-') as tmp:
 pathlib.Path(tmp,'answer.py').write_text(source)
 args=['/usr/bin/bwrap','--unshare-all','--die-with-parent','--new-session','--ro-bind','/usr','/usr','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/work','--ro-bind',tmp,'/work','--chdir','/work','/usr/bin/python3','-I','-S','-c',"import sys;sys.path.insert(0,'/work');\n"+checks]
 q=subprocess.run(args,capture_output=True,text=True,timeout=10,preexec_fn=limits)
 result={'slot':slot,'model':d['model'],'status':'QA_PASS' if q.returncode==0 else 'QA_FAIL','assertions':6,'sandbox':'bubblewrap-no-network','usage':d.get('usage'),'qa_exit':q.returncode}
 if q.returncode:result['error']=q.stderr[-500:]
 print(json.dumps(result));pathlib.Path(__file__).with_name(slot+'.receipt.json').write_text(json.dumps(result,indent=2)+'\n');sys.exit(q.returncode)
