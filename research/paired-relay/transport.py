#!/usr/bin/env python3
"""Permanent paired-device, E2E sealed SearXNG relay. Never accepts arbitrary commands."""
import argparse, base64, hashlib, json, os, re, sqlite3, subprocess, sys, time, uuid
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from nacl.signing import SigningKey, VerifyKey
from nacl.public import PrivateKey, PublicKey, SealedBox
from nacl.exceptions import BadSignatureError, CryptoError

VERSION="bhm-research-v1"
ENDPOINT="https://saczglesalubroyaucqe.supabase.co/functions/v1/bhm-research-relay"
HOME=Path("/var/lib/generic-linux-automator-exec/matrix-research-transport")
SEARCH=Path("/var/lib/generic-linux-automator-exec/matrix-searxng/local_search.py")
HOSTS={"mac-linux","dell-linux"}

def b64(x): return base64.urlsafe_b64encode(bytes(x)).decode().rstrip("=")
def raw(s): return base64.urlsafe_b64decode(s+"="*((-len(s))%4))
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True)
def secret_write(path,data):
    path=Path(path)
    if path.exists(): raise RuntimeError("Refusing to overwrite private state")
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,"w") as f:
        f.write(canon(data)+"\n");f.flush();os.fsync(f.fileno())
def get(name): return json.loads((HOME/name).read_text())
def own():
    d=get("identity.json")
    if d["host_id"] not in HOSTS:raise RuntimeError("Invalid device identity")
    return d,SigningKey(raw(d["signing_private"])),PrivateKey(raw(d["box_private"]))
def peer():
    d=get("peer.json")
    if d["host_id"] not in HOSTS:raise RuntimeError("Invalid trusted host")
    return d
def msg(*a):return "|".join(str(x) for x in (VERSION,*a)).encode()
def sig(sk,*parts):return b64(sk.sign(msg(*parts)).signature)
def verify(vk,signature,*parts):
    try: VerifyKey(raw(vk)).verify(msg(*parts),raw(signature));return True
    except (BadSignatureError,ValueError,TypeError):return False
def fingerprint(pub):return hashlib.sha256(raw(pub)).hexdigest()[:24]
def init(host):
    if host not in HOSTS:raise ValueError("Not an approved machine")
    HOME.mkdir(mode=0o700,parents=True,exist_ok=True)
    os.chmod(HOME,0o700)
    p=HOME/"identity.json"
    if not p.exists():
        s=SigningKey.generate();b=PrivateKey.generate()
        secret_write(p,{"host_id":host,"signing_private":b64(s.encode()),"box_private":b64(b.encode())})
    d,s,b=own()
    if d["host_id"]!=host:raise RuntimeError("Existing identity belongs to other host; no replacement")
    return {"host_id":host,"verify_key":b64(s.verify_key.encode()),"box_key":b64(b.public_key.encode()),"fingerprint":fingerprint(b64(s.verify_key.encode()))}
def trust(host,key,box):
    if host not in HOSTS or len(raw(key))!=32 or len(raw(box))!=32:raise ValueError("Bad peer identity")
    d,_,_=own()
    if d["host_id"]==host:raise ValueError("Self trust prohibited")
    p=HOME/"peer.json"
    payload={"host_id":host,"verify_key":key,"box_key":box,"fingerprint":fingerprint(key)}
    if p.exists():
        if get("peer.json")!=payload:raise RuntimeError("Peer key changed; explicit revocation and repinning needed")
        return {"state":"existing",**payload}
    secret_write(p,payload)
    return {"state":"paired",**payload}
def http(path,body=None,timeout=15):
    if path not in ("/submit","/status","/poll","/finish","/health"):raise RuntimeError("Untrusted endpoint")
    data=None if body is None else canon(body).encode()
    req=Request(ENDPOINT+path,data=data,headers={"Accept":"application/json","Content-Type":"application/json","User-Agent":"BHM-Research/1"},method="GET" if data is None else "POST")
    try:
        with urlopen(req,timeout=timeout) as r:
            out=json.loads(r.read(180000))
            if not isinstance(out,dict):raise RuntimeError("Malformed gateway response")
            return out
    except HTTPError as e:raise RuntimeError("Research relay HTTP "+str(e.code)) from None
    except (URLError,TimeoutError) as e:raise RuntimeError("Research relay unavailable: "+type(e).__name__) from None
def validate_query(q):
    if not isinstance(q,str) or not 2<=len(q.strip())<=180 or any(ord(c)<32 for c in q):raise ValueError("Invalid public research query")
    if re.search(r"\b[\w.+-]+@[\w.-]+\.[a-z]{2,}\b|\b(?:\+?\d[\s-]?){10,}\b|\b(api.?key|bearer|password|private.?key|guest.?data|customer.?list)\b",q,re.I):
        raise ValueError("Private data not allowed in search")
    return q.strip()
def envelope(obj,boxkey):
    return b64(SealedBox(PublicKey(raw(boxkey))).encrypt(canon(obj).encode()))
def open_box(box,private):
    data=SealedBox(private).decrypt(raw(box))
    if len(data)>120000:raise ValueError("Excessive encrypted message")
    return json.loads(data)
def local_db():
    p=HOME/"client.sqlite3";d=sqlite3.connect(p,timeout=10)
    d.execute("CREATE TABLE IF NOT EXISTS requests (digest text PRIMARY KEY,id text UNIQUE NOT NULL,box text NOT NULL,expires integer NOT NULL)")
    d.commit();os.chmod(p,0o600);return d
def status(jobid,sk):
    ts=int(time.time());nonce=str(uuid.uuid4())
    return http("/status",{"host":"mac-linux","id":jobid,"ts":ts,"nonce":nonce,"sig":sig(sk,"status","mac-linux",jobid,ts,nonce)})
def search(q,seconds=55):
    ownid,sk,private=own();target=peer()
    if ownid["host_id"]!="mac-linux" or target["host_id"]!="dell-linux":raise RuntimeError("Wrong research caller pairing")
    q=validate_query(q);digest=hashlib.sha256(q.encode()).hexdigest()
    db=local_db();now=int(time.time())
    x=db.execute("SELECT id,box,expires FROM requests WHERE digest=?",(digest,)).fetchone()
    if x and x[2]>now+20:jobid,boxed,expires=x
    else:
        jobid=str(uuid.uuid4());expires=now+175
        boxed=envelope({"v":1,"id":jobid,"q":q,"limit":5},target["box_key"])
        db.execute("INSERT OR REPLACE INTO requests(digest,id,box,expires) VALUES(?,?,?,?)",(digest,jobid,boxed,expires));db.commit()
    db.close()
    response=http("/submit",{"host":"mac-linux","id":jobid,"box":boxed,"expires":expires,"sig":sig(sk,"submit","mac-linux",jobid,expires,boxed)})
    if response.get("id")!=jobid:raise RuntimeError("Mismatched relay receipt")
    deadline=time.monotonic()+max(1,min(75,seconds))
    while time.monotonic()<deadline:
        r=status(jobid,sk)
        if r.get("state")=="completed":
            obj=open_box(r["box"],private)
            if obj.get("id")!=jobid or not isinstance(obj.get("payload"),dict):raise RuntimeError("Mismatched sealed response")
            payload=obj["payload"]
            if not verify(target["verify_key"],obj.get("signature",""),"receipt","dell-linux",jobid,canon(payload)):
                raise RuntimeError("Untrusted Dell result signature")
            if not payload.get("ok"):raise RuntimeError("Dell research failed: "+str(payload.get("error","unknown"))[:90])
            data=payload.get("result",{})
            if data.get("provider")!="self-hosted-searxng" or data.get("node")!="dell-linux":raise RuntimeError("Unexpected research provider")
            import urllib.parse,ipaddress
            res=[]
            for item in data.get("results",[])[:6]:
                url=str(item.get("url",""))[:700];p=urllib.parse.urlsplit(url)
                if p.scheme!="https" or not p.hostname:continue
                try:ipaddress.ip_address(p.hostname);continue
                except ValueError:pass
                res.append({"title":str(item.get("title",""))[:180],"url":url,"snippet":str(item.get("snippet",""))[:700],"engine":str(item.get("engine",""))[:60]})
            return {"provider":"searxng","mode":"self_hosted_encrypted_paired_relay","query":q,"results":res,"citations_required":True,"untrusted_external_content":True,"paid_fallback":False,"publish_approval":False,"request_id":jobid,"device_peer_verified":True}
        if r.get("expired"):raise RuntimeError("Research request expired; inspect prior receipt "+jobid)
        time.sleep(3)
    raise RuntimeError("Research pending; durable request "+jobid+"; no duplicate submission")
def pending_path():return HOME/"pending.json"
def send_finish(job,sk,box):
    ts=int(time.time());nonce=str(uuid.uuid4())
    r=http("/finish",{"host":"dell-linux","id":job["id"],"claim":job["claim"],"box":box,"ts":ts,"nonce":nonce,
                      "sig":sig(sk,"finish","dell-linux",job["id"],job["claim"],ts,nonce,box)})
    if not r.get("ok"):raise RuntimeError("Relay did not accept Dell receipt")
def process_job(job,sk,target,private):
    if not isinstance(job,dict) or not all(k in job for k in ("id","claim","box")):raise RuntimeError("Invalid claimed research request")
    state=pending_path()
    if not state.exists():secret_write(state,job)
    data=get("pending.json")
    if data.get("id")!=job["id"] or data.get("claim")!=job["claim"]:raise RuntimeError("Unresolved previous receipt, refusing second job")
    if "response_box" not in data:
        try:
            item=open_box(data["box"],private)
            if item.get("id")!=data["id"] or int(item.get("limit",0))!=5:raise ValueError("Malformed research envelope")
            q=validate_query(item.get("q"))
            # Only the preexisting Dell-local SearXNG CLI is executable; no shell, web crawling or stock downloads.
            result=subprocess.run([sys.executable,str(SEARCH),q,"--limit","5"],capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=43)
            if result.returncode:raise RuntimeError("Dell SearXNG unavailable")
            response=json.loads(result.stdout[:60000])
            if response.get("provider")!="self-hosted-searxng":raise RuntimeError("Unexpected provider")
            payload={"ok":True,"result":response}
        except Exception as e:
            payload={"ok":False,"error":type(e).__name__}
        signed={"id":data["id"],"payload":payload,"signature":sig(sk,"receipt","dell-linux",data["id"],canon(payload))}
        data["response_box"]=envelope(signed,target["box_key"])
        temp=state.with_suffix(".tmp")
        secret_write(temp,data);temp.replace(state);os.chmod(state,0o600)
    send_finish(data,sk,data["response_box"])
    state.unlink()
    return {"id":data["id"],"completed":True}
def poll_once():
    d,sk,private=own();p=peer()
    if d["host_id"]!="dell-linux" or p["host_id"]!="mac-linux":raise RuntimeError("Wrong research worker pairing")
    pend=pending_path()
    if pend.exists():
        j=get("pending.json");return process_job(j,sk,p,private)
    ts=int(time.time());nonce=str(uuid.uuid4())
    r=http("/poll",{"host":"dell-linux","ts":ts,"nonce":nonce,"sig":sig(sk,"poll","dell-linux",ts,nonce)})
    if r.get("job"):return process_job(r["job"],sk,p,private)
    return {"state":"idle"}
def serve():
    delay=8
    while True:
        try:
            v=poll_once()
            if v.get("completed"):print("research receipt completed",v["id"],flush=True)
            delay=8
        except Exception as e:
            print("research relay retry",type(e).__name__,flush=True)
            delay=min(50,max(delay*2,12))
        time.sleep(delay)
def selftest():
    d,s,b=own()
    blob=envelope({"hello":"research"},b64(b.public_key.encode()))
    assert open_box(blob,b)=={"hello":"research"}
    token=sig(s,"probe",d["host_id"],"123")
    assert verify(b64(s.verify_key.encode()),token,"probe",d["host_id"],"123")
    assert not verify(b64(s.verify_key.encode()),token,"probe",d["host_id"],"456")
    for sample in ("password abc","alice@example.com"):
        try:validate_query(sample)
        except ValueError:pass
        else:raise AssertionError("Private query accepted")
    return {"passed":True,"tests":["sealed payload roundtrip","Ed25519 valid signature","signature tampering rejected","private query denied"],"host_id":d["host_id"]}
def main():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("init");a.add_argument("--host",choices=sorted(HOSTS),required=True)
    a=sub.add_parser("trust");a.add_argument("--host",choices=sorted(HOSTS),required=True);a.add_argument("--verify-key",required=True);a.add_argument("--box-key",required=True)
    a=sub.add_parser("search");a.add_argument("query");a.add_argument("--timeout",type=int,default=55)
    sub.add_parser("identity");sub.add_parser("selftest");sub.add_parser("poll-once");sub.add_parser("serve");sub.add_parser("health")
    args=p.parse_args()
    if args.cmd=="init":result=init(args.host)
    elif args.cmd=="identity":
        d,s,b=own();result={"host_id":d["host_id"],"verify_key":b64(s.verify_key.encode()),"box_key":b64(b.public_key.encode()),"fingerprint":fingerprint(b64(s.verify_key.encode())),"trusted_peer":peer()["fingerprint"] if (HOME/"peer.json").exists() else None}
    elif args.cmd=="trust":result=trust(args.host,args.verify_key,args.box_key)
    elif args.cmd=="selftest":result=selftest()
    elif args.cmd=="health":result=http("/health")
    elif args.cmd=="poll-once":result=poll_once()
    elif args.cmd=="serve":serve();return
    else:result=search(args.query,args.timeout)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
