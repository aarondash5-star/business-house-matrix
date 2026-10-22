#!/usr/bin/env python3
"""Matrix Dev preference/quota selector for the existing Pi harness (stdlib only)."""
import signal, socket
import argparse, datetime as dt, getpass, json, os, pathlib, sqlite3, subprocess, sys, time, urllib.request, urllib.error
BASE=pathlib.Path(__file__).resolve().parent
import openrouter_pool as pool
POLICY=BASE/"policy.json"
DB=BASE/"quota.sqlite3"
VAULT=BASE/"secrets"
ALLOWED={"groq":{"qwen/qwen3.8-27b","openai/gpt-oss-120b","openai/gpt-oss-20b"},
         "cloudflare-workers-ai":{"@cf/zai-org/glm-4.7-flash"},
         "nvidia":{"openai/gpt-oss-20b","nvidia/nemotron-3-ultra-550b-a55b"},
         "openrouter":{"cohere/north-mini-code:free"},
         "ollama":{"qwen3:4b-instruct","granite4:3b"}}
PI=pathlib.Path.home()/".local/share/matrix-pi-pilot/node_modules/.bin/pi"
PIHOME=BASE/"pi-home"
def now(): return int(time.time())
def read_policy():
 p=json.loads(POLICY.read_text())
 assert p["version"]==1 and p["paid_inference_allowed"] is False
 ids=set()
 for s in p["connections"]:
  assert s["id"] not in ids;ids.add(s["id"])
  assert s["provider"] in ALLOWED and (s["model"] in ALLOWED[s["provider"]] or (s["provider"]=="openrouter" and s["model"] in pool.registry(BASE)))
  assert s["max_daily_requests"] >= 0 and s["max_minute_requests"]>=0
  assert all(k in {"coding","reasoning","review","fast","private"} for k in s["preference"])
 for s in p["connections"]:
  ref=s.get("credential_ref")
  if ref is not None:
   targets=[x for x in p["connections"] if x["id"]==ref]
   assert len(targets)==1 and targets[0]["provider"]==s["provider"] and "credential_ref" not in targets[0]
 return p
def conn():
 c=sqlite3.connect(DB, timeout=20, isolation_level=None)
 c.execute("PRAGMA busy_timeout=20000")
 c.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, slot TEXT, ts INTEGER, outcome TEXT)")
 c.execute("CREATE TABLE IF NOT EXISTS cooldowns(slot TEXT PRIMARY KEY, until_epoch INTEGER)")
 return c
def secret_path(slot):
 assert slot.isascii() and all(x.isalnum() or x in "_-" for x in slot)
 return VAULT/(slot+".key")
def ready(s):
 if not s["enabled"]:return False,"disabled"
 if s["provider"]=="ollama":return True,"local"
 if s.get("license_review_required"):return False,"license_review_required"
 p=secret_path(s.get("credential_ref",s["id"]))
 if not p.is_file():return False,"no_credentials"
 if (p.stat().st_mode & 0o077)!=0:return False,"unsafe_secret_permissions"
 if s["provider"]=="cloudflare-workers-ai" and not s.get("account_id"):return False,"missing_account_id"
 return True,"authenticated_slot"
def candidates(policy, profile, c, reservation=False):
 ts=now();day=ts-ts%86400
 rows=[]
 for s in policy["connections"]:
  if profile not in s["preference"]:continue
  ok,reason=ready(s)
  group=s.get("quota_group",s["id"])
  members=[x["id"] for x in policy["connections"] if x.get("quota_group",x["id"])==group]
  q=",".join("?" for _ in members)
  dayuse=c.execute(f"SELECT count(*) FROM events WHERE slot IN ({q}) AND ts>=?",(*members,day)).fetchone()[0]
  minuse=c.execute(f"SELECT count(*) FROM events WHERE slot IN ({q}) AND ts>=?",(*members,ts-60)).fetchone()[0]
  cd=c.execute("SELECT until_epoch FROM cooldowns WHERE slot=?",(s["id"],)).fetchone()
  if ok and cd and cd[0]>ts: ok=False;reason="cooldown"
  if ok and s["provider"]!="ollama" and dayuse>=s["max_daily_requests"]:ok=False;reason="daily_quota"
  if ok and s["provider"]!="ollama" and minuse>=s["max_minute_requests"]:ok=False;reason="minute_quota"
  rows.append((s,ok,reason,dayuse,minuse))
 rows.sort(key=lambda x:(x[0]["preference"][profile],x[0]["id"]))
 return rows
def choice(policy,profile,c):
 rows=candidates(policy,profile,c)
 for s,ok,reason,_,_ in rows:
  if ok:return s
 raise RuntimeError("no permitted local or free provider available")
def save_policy(policy):
 backup=POLICY.with_suffix(".json.bak")
 if not backup.exists():
  backup.write_bytes(POLICY.read_bytes());backup.chmod(0o600)
 temp=POLICY.with_suffix(".json.tmp")
 if temp.exists():raise RuntimeError("stale temporary policy; do not overwrite")
 fd=os.open(temp,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
 with os.fdopen(fd,"w") as f:
  json.dump(policy,f,indent=2);f.write("\n");f.flush();os.fsync(f.fileno())
 os.replace(temp,POLICY)
def get_slot(policy,id):
 s=next((s for s in policy["connections"] if s["id"]==id),None)
 if not s:raise RuntimeError("unknown connection slot")
 return s
def _hosted_text(s,prompt,tools=False,public_input=False):
 provider=s["provider"]
 if provider not in {"groq","nvidia","openrouter"}:raise RuntimeError("PROVIDER_DENIED")
 if provider=="nvidia" and (s["model"]!="openai/gpt-oss-20b" or s.get("license_review_required")):raise RuntimeError("NVIDIA_MODEL_LICENSE_GATE")
 if not public_input or tools:raise RuntimeError("PUBLIC_TEXT_ONLY_NO_TOOLS_REQUIRED")
 if s["model"] not in ALLOWED[provider] and not (provider=="openrouter" and s["model"] in pool.registry(BASE)):raise RuntimeError("MODEL_DENIED")
 flag={"groq":"groq_free_plan_owner_confirmed","nvidia":"nvidia_free_development_owner_confirmed","openrouter":"openrouter_free_only_owner_confirmed"}[provider]
 if not read_policy().get(flag):raise RuntimeError("FREE_PLAN_ATTESTATION_REQUIRED")
 if not prompt or len(prompt.encode())>2048:raise RuntimeError("PUBLIC_PROMPT_MAX_2048_BYTES")
 sp=secret_path(s.get("credential_ref",s["id"]))
 if sp.is_symlink() or not sp.is_file() or sp.stat().st_mode&0o077:raise RuntimeError("NO_SECURE_CREDENTIAL")
 budget=len(prompt.encode())+1536
 table={"groq":"token_reservations","nvidia":"nvidia_token_reservations","openrouter":"openrouter_token_reservations"}[provider]
 c=conn();c.execute(f"CREATE TABLE IF NOT EXISTS {table}(ts INTEGER,budget INTEGER)")
 c.execute("BEGIN IMMEDIATE")
 try:
  ts=now();day=ts-ts%86400
  minute=c.execute(f"SELECT COALESCE(SUM(budget),0) FROM {table} WHERE ts>=?",(ts-60,)).fetchone()[0]
  daily=c.execute(f"SELECT COALESCE(SUM(budget),0) FROM {table} WHERE ts>=?",(day,)).fetchone()[0]
  if minute+budget>7600 or daily+budget>(80000 if provider=="groq" else 20000):raise RuntimeError("GROQ_SHARED_TOKEN_BUDGET")
  c.execute(f"INSERT INTO {table} VALUES(?,?)",(ts,budget));c.commit()
 except: c.rollback();raise
 finally:c.close()
 body={"model":s["model"],"messages":[{"role":"system","content":"Return only the requested public coding answer. No tools."},{"role":"user","content":prompt}],"max_completion_tokens":1024,"temperature":0.1,"stream":False,"reasoning_effort":"none" if s["model"].startswith("qwen/") else "low"}
 if provider=="nvidia":body["max_tokens"]=body.pop("max_completion_tokens")
 if provider=="openrouter":
  body["max_tokens"]=body.pop("max_completion_tokens");body.pop("reasoning_effort")
  body["provider"]={"data_collection":"deny","max_price":{"prompt":0,"completion":0}}
  body["plugins"]=[]
 class NoRedirect(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,*a,**kw):raise RuntimeError("PROVIDER_REDIRECT_DENIED")
 def deadline(*a):raise TimeoutError("GROQ_DEADLINE")
 old=signal.signal(signal.SIGALRM,deadline);signal.alarm({"groq":30,"nvidia":60,"openrouter":45}[provider])
 try:
  url={"groq":"https://api.groq.com/openai/v1/chat/completions","nvidia":"https://integrate.api.nvidia.com/v1/chat/completions","openrouter":"https://openrouter.ai/api/v1/chat/completions"}[provider]
  request=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+sp.read_text().strip(),"Content-Type":"application/json","User-Agent":"BusinessHouseMatrixDev/1.0 (+https://github.com/aarondash5-star/business-house-matrix)"})
  with urllib.request.build_opener(NoRedirect()).open(request,timeout={"groq":15,"nvidia":45,"openrouter":30}[provider]) as response:
   raw=response.read(65537)
   if len(raw)>65536:raise RuntimeError("PROVIDER_RESPONSE_TOO_LARGE")
   d=json.loads(raw)
  text=d["choices"][0]["message"].get("content")
  if not isinstance(text,str) or not text.strip() or len(text.encode())>8192:raise RuntimeError("INVALID_OR_TRUNCATED_PROVIDER_OUTPUT")
  if d["choices"][0].get("finish_reason")!="stop":raise RuntimeError("PROVIDER_OUTPUT_INCOMPLETE")
  if provider=="openrouter":
   aliases=pool.registry(BASE).get(s['model'],{}).get('response_models',[])
   if not aliases and s['model']=='cohere/north-mini-code:free':aliases=["cohere/north-mini-code","cohere/north-mini-code:free","cohere/north-mini-code-20260617:free","cohere/north-mini-code-20260617"]
   if d.get("model") not in aliases:raise RuntimeError("OPENROUTER_UNEXPECTED_MODEL")
   cost=(d.get("usage") or {}).get("cost")
   if cost is not None and (isinstance(cost,bool) or not isinstance(cost,(int,float)) or cost!=0):raise RuntimeError("OPENROUTER_UNEXPECTED_COST")
  print(json.dumps({"model":d.get("model"),"usage":d.get("usage"),"text":text,"tools_enabled":False}));return 0
 except urllib.error.HTTPError as exc:
  if provider=='openrouter' and exc.code==429:
   try:seconds=max(60,min(86400,int(exc.headers.get('Retry-After','900'))))
   except (ValueError,TypeError,AttributeError):seconds=900
   with conn() as rate_db:rate_db.execute('INSERT OR REPLACE INTO cooldowns(slot,until_epoch) VALUES(?,?)',(s['id'],now()+seconds))
  print(provider.upper()+"_HTTP_"+str(exc.code),file=sys.stderr);return 1
 except (OSError,TimeoutError,ValueError,KeyError,IndexError) as exc:
  print(provider.upper()+"_REQUEST_FAILED_"+type(exc).__name__,file=sys.stderr);return 1
 finally:signal.alarm(0);signal.signal(signal.SIGALRM,old)

def groq_text(s,prompt,tools=False,public_input=False):
 return _hosted_text(s,prompt,tools,public_input)
def nvidia_text(s,prompt,tools=False,public_input=False,development_test=False):
 if not development_test:raise RuntimeError("NVIDIA_DEVELOPMENT_TEST_CONFIRMATION_REQUIRED")
 return _hosted_text(s,prompt,tools,public_input)
def openrouter_text(s,prompt,tools=False,public_input=False):
 return _hosted_text(s,prompt,tools,public_input)
def launch(s,prompt,tools=False,public_input=False,development_test=False,profile='coding'):
 if s["provider"]=="openrouter":
  dynamic=False;model=None;started=time.monotonic()
  try:
   dynamic=read_policy().get('openrouter_demand_routing',False)
   if dynamic:
    if not public_input or tools:raise RuntimeError('PUBLIC_TEXT_ONLY_NO_TOOLS_REQUIRED')
    probe=pool.next_probe(BASE,DB,profile)
    if probe:
     # One fixed public QA fixture at most; never give unqualified models the task.
     q=subprocess.run([sys.executable,str(BASE/'qualify_openrouter.py'),'--model',probe],capture_output=True,text=True,timeout=70)
     print('OPENROUTER_DEMAND_QUALIFICATION',probe,'exit',q.returncode,flush=True)
    rate_db=conn()
    try:account_cd=rate_db.execute('SELECT until_epoch FROM cooldowns WHERE slot=?',(s['id'],)).fetchone()
    finally:rate_db.close()
    if account_cd and account_cd[0]>now():raise RuntimeError('OPENROUTER_ACCOUNT_COOLDOWN')
    model=pool.select(BASE,DB,profile);s=dict(s,model=model)
    print('OPENROUTER_MODEL',model,'DEMAND_PROFILE',profile,flush=True)
   started=time.monotonic()
   code=openrouter_text(s,prompt,tools,public_input)
  except (OSError,ValueError,RuntimeError,KeyError,TypeError,sqlite3.Error,subprocess.TimeoutExpired) as exc:
   print('OPENROUTER_POOL_FAILED_'+type(exc).__name__,file=sys.stderr);code=1
  if dynamic and model:pool.record(DB,model,code==0,(time.monotonic()-started)*1000)
  return code
 if s["provider"]=="nvidia":return nvidia_text(s,prompt,tools,public_input,development_test)
 if s["provider"]=="groq":return groq_text(s,prompt,tools,public_input)
 env=os.environ.copy()
 env["PI_CODING_AGENT_DIR"]=str(PIHOME)
 env["PI_OFFLINE"]="1"
 env["PI_TELEMETRY"]="0"
 env.pop("OPENROUTER_API_KEY",None)
 env.pop("ANTHROPIC_API_KEY",None)
 env.pop("OPENAI_API_KEY",None)
 env.pop("NVIDIA_API_KEY",None)
 if s["provider"]=="groq":
  env["GROQ_API_KEY"]=secret_path(s.get("credential_ref",s["id"])).read_text().strip()
 if s["provider"]=="nvidia":
  env["NVIDIA_API_KEY"]=secret_path(s.get("credential_ref",s["id"])).read_text().strip()
 if s["provider"]=="cloudflare-workers-ai":
  env["CLOUDFLARE_API_KEY"]=secret_path(s.get("credential_ref",s["id"])).read_text().strip()
  env["CLOUDFLARE_ACCOUNT_ID"]=s["account_id"]
 args=[str(PI),"--provider",s["provider"],"--model",s["model"],
       "--print","--no-session","--no-mcp","--no-extensions","--no-context-files","--no-approve"]
 if not tools:args+=["--no-tools"]
 args+=["--",prompt]
 return subprocess.run(args,env=env,check=False).returncode
def verify_provider(s):
 if s["provider"]=="openrouter":return verify_openrouter(s)
 if s["provider"]=="ollama":
  print("LOCAL_NO_EXTERNAL_TOKEN_REQUIRED",s["id"]);return
 sp=secret_path(s.get("credential_ref",s["id"]))
 if not sp.is_file() or sp.stat().st_mode&0o077:
  raise RuntimeError("NO_SECURE_CREDENTIAL: enroll from Dell terminal before verify")
 key=sp.read_text().strip()
 if s["provider"]=="nvidia":
  raise RuntimeError("NVIDIA public /models is not an authentication check; after Free-plan enrollment run a bounded model inference using run --slot nvidia-oss20 --no-fallback")
 if s["provider"]=="groq":
  url="https://api.groq.com/openai/v1/models"
 else:
  account=s.get("account_id","")
  if len(account)!=32 or any(x not in "0123456789abcdefABCDEF" for x in account):
   raise RuntimeError("Cloudflare Account ID missing/invalid")
  url=f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/models/search?search=glm-4.7-flash"
 request=urllib.request.Request(url,headers={"Authorization":"Bearer "+key,"User-Agent":"matrix-dev-credential-check/1.0"})
 try:
  with urllib.request.urlopen(request,timeout=15) as res:
   data=json.load(res)
 except urllib.error.HTTPError as exc:
  raise RuntimeError("PROVIDER_TOKEN_CHECK_HTTP_"+str(exc.code))
 except Exception as exc:
  raise RuntimeError("PROVIDER_TOKEN_CHECK_FAILED_"+type(exc).__name__)
 if s["provider"]=="groq":
  models={item.get("id") for item in data.get("data",[]) if isinstance(item,dict)}
  if s["model"] not in models:raise RuntimeError("CREDENTIAL_WORKS_BUT_MODEL_UNAVAILABLE")
 else:
  if not data.get("success") or not data.get("result"):
   raise RuntimeError("CLOUDFLARE_CREDENTIAL_OR_MODEL_PERMISSION_FAILED")
 print("PROVIDER_CREDENTIAL_PASS",s["id"],"PLAN_AND_BILLING_STILL_REQUIRE_ACCOUNT_VERIFICATION")
def verify_openrouter(s):
 sp=secret_path(s.get("credential_ref",s["id"]))
 if sp.is_symlink() or not sp.is_file() or sp.stat().st_mode&0o077:raise RuntimeError("NO_SECURE_CREDENTIAL")
 class NoRedirect(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,*a,**kw):raise RuntimeError("PROVIDER_REDIRECT_DENIED")
 def deadline(*a):raise TimeoutError("OPENROUTER_KEY_CHECK_DEADLINE")
 old=signal.signal(signal.SIGALRM,deadline);signal.alarm(30)
 try:
  req=urllib.request.Request("https://openrouter.ai/api/v1/key",headers={"Authorization":"Bearer "+sp.read_text().strip(),"User-Agent":"BusinessHouseMatrixDev/1.0 (+https://github.com/aarondash5-star/business-house-matrix)"})
  with urllib.request.build_opener(NoRedirect()).open(req,timeout=15) as res:
   raw=res.read(65537)
   if len(raw)>65536:raise RuntimeError("PROVIDER_RESPONSE_TOO_LARGE")
   data=json.loads(raw)["data"]
  if not isinstance(data,dict) or data.get("is_management_key") or data.get("is_provisioning_key"):raise RuntimeError("OPENROUTER_INFERENCE_KEY_REQUIRED")
  q=data.get("free_model_daily_requests") or {}
  if not isinstance(q,dict):raise RuntimeError("OPENROUTER_INVALID_QUOTA")
  safe_quota={k:v for k,v in q.items() if k in {"used","limit","remaining"} and type(v) is int and v>=0}
  print(json.dumps({"status":"OPENROUTER_CREDENTIAL_PASS","slot":s["id"],"free_model_daily_requests":safe_quota,"paid_routes_allowed":False,"inference_verified":False}))
 except urllib.error.HTTPError as exc:raise RuntimeError("OPENROUTER_KEY_CHECK_HTTP_"+str(exc.code))
 except (OSError,TimeoutError,ValueError,KeyError,TypeError) as exc:raise RuntimeError("OPENROUTER_KEY_CHECK_FAILED_"+type(exc).__name__)
 finally:signal.alarm(0);signal.signal(signal.SIGALRM,old)
def main():
 parser=argparse.ArgumentParser(description="Zero-paid Matrix Dev API selector")
 sub=parser.add_subparsers(dest="command",required=True)
 sub.add_parser("status");sub.add_parser("validate")
 discovery=sub.add_parser('openrouter-pool');discovery.add_argument('--refresh',action='store_true');discovery.add_argument('--profile',choices=['coding','review','reasoning','fast'],default='coding')
 verify=sub.add_parser("verify-provider");verify.add_argument("slot")
 manage=sub.add_parser("set");manage.add_argument("slot");manage.add_argument("--enabled",choices=["yes","no"]);manage.add_argument("--profile",choices=["coding","reasoning","review","fast","private"]);manage.add_argument("--rank",type=int);manage.add_argument("--daily",type=int);manage.add_argument("--rpm",type=int);manage.add_argument("--account-id")
 choose=sub.add_parser("choose");choose.add_argument("--profile",default="coding")
 run=sub.add_parser("run");run.add_argument("--profile",choices=['auto','coding','review','reasoning','fast','private'],default="auto");run.add_argument("--public-input",action="store_true");run.add_argument("--development-test",action="store_true");run.add_argument("--allow-tools",action="store_true");run.add_argument("--slot");run.add_argument("--no-fallback",action="store_true");run.add_argument("prompt")
 sim=sub.add_parser("simulate-429");sim.add_argument("slot");sim.add_argument("--seconds",type=int,default=3600)
 enroll=sub.add_parser("enroll");enroll.add_argument("slot");enroll.add_argument("--free-plan-confirmed",action="store_true")
 args=parser.parse_args();p=read_policy()
 c=conn()
 if args.command=='openrouter-pool':
  print(json.dumps({'models':pool.describe(BASE,DB,args.profile,args.refresh),'paid_routes_allowed':False,'idle_polling':False}));return
 if args.command=="set":
  s=get_slot(p,args.slot)
  if args.profile is not None:
   if args.rank is None or not 0<=args.rank<=1000:raise RuntimeError("rank must be 0..1000")
   s["preference"][args.profile]=args.rank
  elif args.rank is not None:raise RuntimeError("profile required with rank")
  if args.daily is not None:
   if s["provider"]=="ollama" or not 0<=args.daily<=1000:raise RuntimeError("invalid daily free quota")
   s["max_daily_requests"]=args.daily
  if args.rpm is not None:
   if s["provider"]=="ollama" or not 0<=args.rpm<=30:raise RuntimeError("invalid free requests/minute")
   s["max_minute_requests"]=args.rpm
  if args.account_id is not None:
   if s["provider"]!="cloudflare-workers-ai" or not args.account_id.isascii() or len(args.account_id)!=32 or not all(ch in "0123456789abcdefABCDEF" for ch in args.account_id):
    raise RuntimeError("Cloudflare account id must be 32 hex chars")
   s["account_id"]=args.account_id
  if args.enabled is not None:
   if args.enabled=="yes" and s.get("license_review_required"):
    raise RuntimeError("model license not OSI-verified; obtain explicit approval before enabling")
   if args.enabled=="yes" and s["provider"]!="ollama":
    sp=secret_path(s.get("credential_ref",s["id"]))
    if not sp.is_file() or (sp.stat().st_mode & 0o077):raise RuntimeError("valid secure slot credential required before enabling")
    if s["provider"]=="cloudflare-workers-ai" and not s.get("account_id"):raise RuntimeError("Cloudflare account_id required")
   s["enabled"]=args.enabled=="yes"
  save_policy(p)
  print("POLICY_UPDATED",args.slot,"enabled",s["enabled"],"preference",s["preference"]);return
 if args.command=="validate":
  print("PASS policy schema, zero-paid allowlist, distinct slots");return
 if args.command=="verify-provider":
  verify_provider(get_slot(p,args.slot));return
 if args.command=="enroll":
  s=next((s for s in p["connections"] if s["id"]==args.slot),None)
  if not s or s["provider"]=="ollama":raise RuntimeError("no external slot")
  if not args.free_plan_confirmed:raise RuntimeError("confirm vendor Free plan and zero paid billing first")
  if not sys.stdin.isatty():raise RuntimeError("enroll only from interactive Dell terminal")
  VAULT.mkdir(mode=0o700,exist_ok=True)
  value=getpass.getpass("Provider API key (hidden): ").strip()
  if not value or len(value)<12:raise RuntimeError("invalid key length")
  sp=secret_path(s.get("credential_ref",s["id"]))
  if sp.exists():raise RuntimeError("existing key: rotate explicitly instead of overwriting")
  fd=os.open(sp,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
  with os.fdopen(fd,"w") as f:f.write(value+"\n")
  print("KEY_SAVED securely. Enable the slot only after validation; not activated automatically.");return
 if args.command=="simulate-429":
  if not any(x["id"]==args.slot for x in p["connections"]):raise RuntimeError("unknown slot")
  if args.seconds<1 or args.seconds>86400:raise RuntimeError("cooldown must be 1..86400 seconds")
  c.execute("INSERT OR REPLACE INTO cooldowns(slot,until_epoch) VALUES(?,?)",(args.slot,now()+args.seconds))
  print("SIMULATED cooldown only",args.slot);return
 if args.command=="status":
  for s,ok,reason,dayuse,minuse in candidates(p,"coding",c):
   print(s["id"],"ready" if ok else reason,"model="+s["model"],"daily="+str(dayuse)+"/"+str(s["max_daily_requests"]),"minute="+str(minuse)+"/"+str(s["max_minute_requests"]))
  print("PAID_API=DENIED; vendor Free plan required");return
 if args.command=="choose":
  s=choice(p,args.profile,c)
  print("SELECT",s["id"],s["provider"]+"/"+s["model"]);return
 if args.command=="run":
  if args.profile=='auto':args.profile=pool.classify(args.prompt)
  if not args.development_test:
   if args.slot and get_slot(p,args.slot)["provider"]=="nvidia":raise RuntimeError("NVIDIA_DEVELOPMENT_TEST_CONFIRMATION_REQUIRED")
   for item in p["connections"]:
    if item["provider"]=="nvidia":item["enabled"]=False
  if not args.public_input:
   if args.slot and get_slot(p,args.slot)["provider"]!="ollama":raise RuntimeError("PUBLIC_INPUT_CONFIRMATION_REQUIRED")
   for item in p["connections"]:
    if item["provider"]!="ollama":item["enabled"]=False
  c.execute("BEGIN IMMEDIATE")
  try:
   if args.slot:
    rows=[row for row in candidates(p,args.profile,c) if row[0]["id"]==args.slot]
    if not rows:raise RuntimeError("slot not configured for requested profile")
    selected,eligible,reason,*_=rows[0]
    if not eligible:raise RuntimeError("slot unavailable: "+reason)
    s=selected
   else:
    s=choice(p,args.profile,c)
   c.execute("INSERT INTO events(slot,ts,outcome) VALUES(?,?,?)",(s["id"],now(),"reserved"))
   eid=c.execute("SELECT last_insert_rowid()").fetchone()[0]
   c.commit()
  except:
   c.rollback();raise
  attempts=0
  attempted=set()
  while True:
   attempts+=1;attempted.add(s["id"])
   print("ROUTE",s["id"],"PROFILE",args.profile,"ATTEMPT",attempts,flush=True)
   code=launch(s,args.prompt,args.allow_tools,args.public_input,args.development_test,args.profile)
   c.execute("UPDATE events SET outcome=? WHERE id=?",("ok" if code==0 else "failed",eid))
   if code==0:return
   if args.allow_tools or args.no_fallback:
    print("FAILED; automatic replay blocked" if args.allow_tools else "SLOT_TEST_FAILED; no fallback requested",file=sys.stderr)
    sys.exit(code)
   if not (s['provider']=='openrouter' and p.get('openrouter_demand_routing')):
    c.execute("INSERT OR REPLACE INTO cooldowns(slot,until_epoch) VALUES(?,?)",(s["id"],now()+900))
   c.execute("BEGIN IMMEDIATE")
   try:
    options=[x for x,ok,why,*_ in candidates(p,args.profile,c) if ok and x["id"] not in attempted]
    if not options:
     c.commit();print("NO_MORE_ZERO_COST_ROUTES",file=sys.stderr);sys.exit(code)
    s=options[0]
    c.execute("INSERT INTO events(slot,ts,outcome) VALUES(?,?,?)",(s["id"],now(),"reserved"))
    eid=c.execute("SELECT last_insert_rowid()").fetchone()[0]
    c.commit()
   except:
    c.rollback();raise
if __name__=="__main__":
 try:main()
 except (AssertionError,ValueError,RuntimeError,sqlite3.Error) as exc:
  print("ROUTER_ERROR",str(exc),file=sys.stderr);sys.exit(2)


