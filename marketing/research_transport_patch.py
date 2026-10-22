#!/usr/bin/env python3
"""One-time source-exact, reversible patch to the previously paired transport.
Owner-scoped, no identity/key edits. --check writes nothing.
"""
import argparse
import hashlib
import os
from pathlib import Path
import shutil

ROOT=Path("/var/lib/generic-linux-automator-exec")
TRANSPORT=ROOT/"matrix-research-transport/transport.py"
MAC_ADAPTER=Path("/opt/business-house-matrix/marketing/brain/searxng_research.py")
MARKER="# BHM_EXACT_EXTRACT_GATE_20261022"
STAMP=".pre-exact-extract-gate-20261022"

CLIENT= r'''
# BHM_EXACT_EXTRACT_GATE_20261022
def extract_granted_url(url,seconds=70):
    import importlib.util
    from pathlib import Path
    path=HOME/"research_transport_ops.py"
    spec=importlib.util.spec_from_file_location("bhm_exact_grant",path)
    if spec is None or spec.loader is None:raise RuntimeError("Exact-page grant missing")
    ops=importlib.util.module_from_spec(spec);spec.loader.exec_module(ops)
    url=ops.grant(url)
    ownid,sk,private=own();target=peer()
    if ownid["host_id"]!="mac-linux" or target["host_id"]!="dell-linux":
        raise RuntimeError("Wrong extract caller pairing")
    digest="exact-extract-"+hashlib.sha256(url.encode()).hexdigest()
    db=local_db();timestamp=int(time.time())
    row=db.execute("SELECT id,box,expires FROM requests WHERE digest=?",(digest,)).fetchone()
    if row and row[2]>timestamp+20:
        jobid,boxed,expires=row
    else:
        jobid=str(uuid.uuid4());expires=timestamp+175
        boxed=envelope({"v":2,"op":"extract_granted_url","id":jobid,"url":url,"limit":5},target["box_key"])
        db.execute("INSERT OR REPLACE INTO requests(digest,id,box,expires) VALUES(?,?,?,?)",
                   (digest,jobid,boxed,expires));db.commit()
    db.close()
    response=http("/submit",{"host":"mac-linux","id":jobid,"box":boxed,"expires":expires,
                              "sig":sig(sk,"submit","mac-linux",jobid,expires,boxed)})
    if response.get("id")!=jobid:raise RuntimeError("Mismatched extract submit receipt")
    deadline=time.monotonic()+max(1,min(75,seconds))
    while time.monotonic()<deadline:
        r=status(jobid,sk)
        if r.get("state")=="completed":
            obj=open_box(r["box"],private)
            if obj.get("id")!=jobid or not isinstance(obj.get("payload"),dict):
                raise RuntimeError("Invalid sealed extract envelope")
            payload=obj["payload"]
            if not verify(target["verify_key"],obj.get("signature",""),
                          "receipt","dell-linux",jobid,canon(payload)):
                raise RuntimeError("Untrusted Dell extract receipt signature")
            if not payload.get("ok"):
                raise RuntimeError("Extract unavailable: "+str(payload.get("error","unknown"))[:80])
            result=payload.get("result",{})
            if (result.get("provider")!="bhm-exact-page-extractor"
                or result.get("node")!="dell-linux" or result.get("page",{}).get("source_url")!=url):
                raise RuntimeError("Unexpected extraction source identity")
            page=result["page"]
            if page.get("status") not in ("needs_review","unavailable"):
                raise RuntimeError("Untrusted page status")
            return {"provider":"bhm-exact-page-extractor",
                    "mode":"self_hosted_encrypted_paired_relay","request_id":jobid,
                    "device_peer_verified":True,"page":page,
                    "facts_verified":False,"paid_fallback":False,
                    "publish_approval":False}
        if r.get("expired"):raise RuntimeError("Exact page request expired: "+jobid)
        time.sleep(3)
    raise RuntimeError("Exact page research pending: "+jobid)
'''

OLD_WORKER='''            item=open_box(data["box"],private)
            if item.get("id")!=data["id"] or int(item.get("limit",0))!=5:raise ValueError("Malformed research envelope")
            q=validate_query(item.get("q"))
            # Only the preexisting Dell-local SearXNG CLI is executable; no shell, web crawling or stock downloads.
            result=subprocess.run([sys.executable,str(SEARCH),q,"--limit","5"],capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=43)
            if result.returncode:raise RuntimeError("Dell SearXNG unavailable")
            response=json.loads(result.stdout[:60000])
            if response.get("provider")!="self-hosted-searxng":raise RuntimeError("Unexpected provider")
            payload={"ok":True,"result":response}
'''

NEW_WORKER='''            item=open_box(data["box"],private)
            if item.get("id")!=data["id"] or int(item.get("limit",0))!=5:
                raise ValueError("Malformed research envelope")
            if item.get("v")==2 and item.get("op")=="extract_granted_url":
                import importlib.util
                op_path=HOME/"research_transport_ops.py"
                spec=importlib.util.spec_from_file_location("bhm_exact_grant",op_path)
                if spec is None or spec.loader is None:raise RuntimeError("Missing extractor policy")
                ops=importlib.util.module_from_spec(spec);spec.loader.exec_module(ops)
                payload={"ok":True,"result":ops.execute(ops.grant(item.get("url")))}
            elif item.get("v")==1 and set(item)=={"v","id","q","limit"}:
                q=validate_query(item.get("q"))
                # Preserve existing strict search-only execution contract.
                result=subprocess.run([sys.executable,str(SEARCH),q,"--limit","5"],
                                      capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=43)
                if result.returncode:raise RuntimeError("Dell SearXNG unavailable")
                response=json.loads(result.stdout[:60000])
                if response.get("provider")!="self-hosted-searxng":raise RuntimeError("Unexpected provider")
                payload={"ok":True,"result":response}
            else:
                raise ValueError("Unsupported authenticated research operation")
'''

OLD_MAC='''def extract(url):
    raise RuntimeError("Tavily Extract deprecated. No arbitrary URL fetching. Add a reviewed local Trafilatura extractor later.")
'''
NEW_MAC='''def extract(url):
    # Exact public-page grants are enforced independently on Mac and Dell.
    import importlib.util
    module_path=Path("/var/lib/generic-linux-automator-exec/matrix-research-transport/transport.py")
    spec=importlib.util.spec_from_file_location("bhm_paired_research",module_path)
    if spec is None or spec.loader is None:raise RuntimeError("Approved paired research runtime missing")
    paired=importlib.util.module_from_spec(spec);spec.loader.exec_module(paired)
    return paired.extract_granted_url(url)
'''

def patch(s,host):
    if MARKER in s:
        raise RuntimeError("already_applied")
    if host=="dell":
        if s.count(OLD_WORKER)!=1:raise RuntimeError("worker_signature_changed")
        return s.replace(OLD_WORKER,NEW_WORKER+ "\n            "+MARKER+"\n")
    if s.count("def pending_path():")!=1:
        raise RuntimeError("client_signature_changed")
    return s.replace("def pending_path():",CLIENT+"\ndef pending_path():")
def patch_mac_adapter(s):
    if s.count(OLD_MAC)!=1:
        raise RuntimeError("mac_adapter_signature_changed")
    return s.replace(OLD_MAC,NEW_MAC)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--host",choices=("dell","mac"),required=True)
    p.add_argument("--apply",action="store_true")
    a=p.parse_args()
    files=[(TRANSPORT,patch)]
    if a.host=="mac":files.append((MAC_ADAPTER,None))
    updates=[]
    for path,method in files:
        original=path.read_text()
        new=patch(original,a.host) if method else patch_mac_adapter(original)
        compile(new,str(path),"exec")
        updates.append((path,original,new))
    if a.apply:
        for path,original,new in updates:
            backup=Path(str(path)+STAMP)
            if backup.exists():
                raise RuntimeError("backup_exists_refuse_to_overwrite")
        for path,original,new in updates:
            backup=Path(str(path)+STAMP)
            shutil.copy2(path,backup)
            temp=Path(str(path)+".exact-gate.tmp")
            temp.write_text(new)
            os.chmod(temp,path.stat().st_mode & 0o777)
            os.replace(temp,path)
    print({"host":a.host,"mode":"applied" if a.apply else "check_only",
           "files":len(updates),"source_matches":len(updates),
           "backup_suffix":STAMP})
if __name__=="__main__":main()
