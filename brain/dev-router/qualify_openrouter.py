"""Qualify one reviewed free model using a fixed public fixture and shared quotas."""
import argparse, contextlib, hashlib, importlib.util, io, json, pathlib, resource, subprocess, sys, tempfile, time
import openrouter_pool as pool
BASE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('matrix_route',BASE/'matrix-route.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
PROMPT='Return only Python source, no markdown: def clamp(x, low, high) bounding x inclusively. Assume low <= high.'
CHECKS='from answer import clamp\nassert clamp(2,0,4)==2\nassert clamp(-1,0,4)==0\nassert clamp(9,0,4)==4\nassert clamp(0,0,4)==0\nassert clamp(4,0,4)==4\nassert clamp(3,2,2)==2'

def limits():
    resource.setrlimit(resource.RLIMIT_CPU,(3,3))
    resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,256*1024*1024))
    resource.setrlimit(resource.RLIMIT_FSIZE,(65536,65536))

def main(model):
    if model not in pool.registry(BASE): raise RuntimeError('MODEL_LICENSE_NOT_REVIEWED')
    current=pool.catalog(BASE)['models'].get(model)
    if not current: raise RuntimeError('MODEL_NOT_FREE_OR_AVAILABLE')
    if current['canonical_slug']!=pool.registry(BASE)[model].get('canonical_slug'):raise RuntimeError('MODEL_LICENSE_REVISION_REVIEW_REQUIRED')
    p=m.read_policy();c=m.conn();eid=None;passed=False;started=time.monotonic();error=None
    c.execute('BEGIN IMMEDIATE')
    try:
        row=next(x for x in m.candidates(p,'coding',c) if x[0]['id']=='openrouter-code')
        if not row[1]: raise RuntimeError('SHARED_QUOTA_OR_SLOT_UNAVAILABLE')
        s=dict(row[0],model=model)
        c.execute('INSERT INTO events(slot,ts,outcome) VALUES(?,?,?)',('openrouter-code',m.now(),'qualification_reserved'))
        eid=c.execute('SELECT last_insert_rowid()').fetchone()[0];c.commit()
    except: c.rollback();c.close();raise
    try:
        out=io.StringIO()
        with contextlib.redirect_stdout(out): code=m.openrouter_text(s,PROMPT,False,True)
        if code: raise RuntimeError('QUALIFICATION_API_FAILED')
        d=json.loads(out.getvalue().strip());source=d['text'].strip()
        if (d.get('usage') or {}).get('cost')!=0: raise RuntimeError('ZERO_COST_RECEIPT_REQUIRED')
        if source.startswith('```') and source.endswith('```'):source='\n'.join(source.splitlines()[1:-1])
        with tempfile.TemporaryDirectory(prefix='matrix-openrouter-qualification-') as tmp:
            pathlib.Path(tmp,'answer.py').write_text(source)
            args=['/usr/bin/bwrap','--clearenv','--setenv','PATH','/usr/bin:/bin','--unshare-all','--die-with-parent','--new-session','--ro-bind','/usr','/usr','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/work','--ro-bind',tmp,'/work','--chdir','/work','/usr/bin/python3','-I','-S','-c',"import sys;sys.path.insert(0,'/work');\n"+CHECKS]
            q=subprocess.run(args,capture_output=True,text=True,timeout=10,preexec_fn=limits)
            passed=q.returncode==0
        result={'model':model,'status':'QA_PASS' if passed else 'QA_FAIL','assertions':6,'sandbox':'bubblewrap-no-network-clearenv','usage':d.get('usage'),'source_sha256':hashlib.sha256(source.encode()).hexdigest()}
    except (OSError,ValueError,RuntimeError,KeyError,TypeError,subprocess.TimeoutExpired) as exc:
        error=type(exc).__name__;result={'model':model,'status':'QA_FAIL','error_type':error}
    finally:
        c.execute('UPDATE events SET outcome=? WHERE id=?',('qualification_ok' if passed else 'qualification_failed',eid));c.close()
    result['latency_ms']=round((time.monotonic()-started)*1000)
    evidence=BASE/('openrouter-qualification-'+model.replace('/','_').replace(':','_')+'-'+str(time.time_ns())+'.json')
    evidence.write_text(json.dumps(result,indent=2)+'\n');evidence.chmod(0o600)
    pool.mark_qa(BASE,m.DB,model,passed,evidence.name,result['latency_ms'])
    print(json.dumps(result));return 0 if passed else 1

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--model',required=True);args=parser.parse_args()
    try:sys.exit(main(args.model))
    except (OSError,ValueError,RuntimeError,StopIteration) as exc:
        print(json.dumps({'status':'QUALIFICATION_DEFERRED','error_type':type(exc).__name__}));sys.exit(2)
