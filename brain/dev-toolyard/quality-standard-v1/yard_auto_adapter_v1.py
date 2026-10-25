"""Bounded automatic Dell Tool Yard adapter enrollment, not release authority."""
from __future__ import annotations
import ast,hashlib,json,os,re,shutil,subprocess,tempfile
from pathlib import Path
from datetime import datetime,timezone
from toolyard_qa_standard_v1 import VERSION as QAVER,ACTION_PROFILES,REQUIREMENTS
VERSION="yard-auto-adapter-v1.2.0-20261026"
HERE=Path(__file__).resolve().parent
REGISTRY=HERE/"yard_tool_adapters_v1.json"
TEMPLATES={"python3":("functional_app","--version"),"node":("functional_app","--version"),
"npm":("functional_app","--version"),"git":("automation","--version"),
"blender":("interactive_media","--version"),"ffmpeg":("media","-version"),
"google-chrome":("creative_web","--version"),"podman":("verification","--version"),
"npx":("functional_app","--version"),"gh":("automation","--version")}
UNREVIEWED=("vercel","pytest")
ROOTS=("/usr/bin/","/usr/local/bin/","/opt/")
class AdapterDenied(ValueError):pass
def sha(p):
    p=Path(p)
    if not p.is_file() or p.stat().st_size>250_000_000:raise AdapterDenied("bad_binary")
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(1<<20),b""):h.update(c)
    return h.hexdigest()
def safe(name,path):
    if not re.fullmatch(r"[a-z][a-z0-9_-]{1,39}",name):raise AdapterDenied("bad_name")
    p=Path(path).resolve(strict=True)
    if not any(str(p).startswith(x) for x in ROOTS):raise AdapterDenied("untrusted_binary_location")
    if not p.is_file():raise AdapterDenied("not_a_file")
    return p
def inherit(project,action,manifest):
    if action not in ACTION_PROFILES:raise AdapterDenied("unknown_action_quarantined")
    if not project or not manifest:raise AdapterDenied("project_manifest_required")
    kind=ACTION_PROFILES[action]
    return {"rule":VERSION,"quality_policy":QAVER,"project":project,
      "action":action,"manifest":manifest,"profile":kind,
      "mandatory_checks":list(REQUIREMENTS[kind]),
      "automatically_attached":True,"production_authorized":False}
def discover(which=shutil.which):
    found={}
    for name in (*TEMPLATES,*UNREVIEWED):
        p=which(name)
        if p:
            try:
                real=safe(name,p)
                found[name]={"binary":str(real),"sha256":sha(real)}
            except (OSError,AdapterDenied):
                found[name]={"error":"untrusted_binary"}
    # New local yard scripts are auto-inventoried with the QA rule attached,
    # but no executable operation is certified until a reviewed adapter exists.
    for parent in (HERE, HERE.parent/"managed-tools"):
        if not parent.is_dir() or parent.is_symlink(): continue
        for script in sorted(parent.iterdir()):
            if script.is_symlink() or not script.is_file() or script.suffix not in (".py",".mjs",".js",".sh"):
                continue
            if script.stat().st_size>1000000: continue
            key="yard-"+re.sub(r"[^a-z0-9_-]","-",script.stem.lower())[:33]
            if key in found: continue
            found[key]={"binary":str(script.resolve()),"sha256":sha(script),
                       "inventory":"direct_script_unreviewed"}
    roots=("matrix-","threejs-","shaadi-","delulu-","wp-manager-","eccrm-","andaz-","moksha-")
    for workspace in sorted(HERE.parent.iterdir()):
        if workspace==HERE or workspace.is_symlink() or not workspace.is_dir() or not workspace.name.startswith(roots):
            continue
        for directory in (workspace,workspace/"src",workspace/"scripts",workspace/"tools"):
            if not directory.is_dir() or directory.is_symlink():continue
            for item in sorted(directory.iterdir()):
                if item.is_symlink() or not item.is_file() or item.suffix not in (".py",".js",".mjs",".sh"):
                    continue
                if item.stat().st_size>1_000_000:continue
                short=re.sub(r"[^a-z0-9_-]","-",item.stem.lower())[:10]
                token=hashlib.sha256(str(item).encode()).hexdigest()[:7]
                key="yard-"+workspace.name[:10]+"-"+short+"-"+token
                found.setdefault(key,{"binary":str(item.resolve()),"sha256":sha(item),
                                      "inventory":"yard_workspace_script"})
    return found
def probe(name,entry):
    if name not in TEMPLATES:return False,"no_reviewed_template"
    args=[entry["binary"],TEMPLATES[name][1]]
    try:
        with tempfile.TemporaryDirectory(prefix="yard-probe-") as home:
            env={"PATH":"/usr/local/bin:/usr/bin:/bin","LANG":"C",
                 "LC_ALL":"C","HOME":home,"XDG_RUNTIME_DIR":home}
            r=subprocess.run(args,cwd="/",env=env,capture_output=True,text=True,
                             stdin=subprocess.DEVNULL,timeout=10)
        ok=(r.returncode==0 and bool((r.stdout+r.stderr).strip()))
        return ok,"version_probe_pass" if ok else "version_probe_failed"
    except (OSError,subprocess.TimeoutExpired) as e:return False,type(e).__name__
def syntax_probe(entry):
    """Safely syntax-check a local script; never import or execute it."""
    f=Path(entry["binary"])
    try:
        if f.suffix==".py":
            ast.parse(f.read_text(encoding="utf-8"),filename=str(f))
            return True,"python_ast_syntax_pass"
        if f.suffix in (".mjs",".js",".sh"):
            exe="node" if f.suffix in (".mjs",".js") else "bash"
            args=[exe,"--check",str(f)] if exe=="node" else [exe,"-n",str(f)]
            with tempfile.TemporaryDirectory(prefix="yard-syntax-") as temp:
                env={"PATH":"/usr/local/bin:/usr/bin:/bin","LANG":"C","HOME":temp}
                v=subprocess.run(args,stdin=subprocess.DEVNULL,capture_output=True,
                    text=True,cwd="/",env=env,timeout=8)
            return v.returncode==0,"syntax_only_pass" if v.returncode==0 else "syntax_error"
    except (OSError,UnicodeError,SyntaxError,subprocess.TimeoutExpired) as err:
        return False,type(err).__name__
    return False,"no_syntax_template"
def script_profile(name):
    if any(w in name for w in ("site","web","html","browser")):return "creative_web"
    if any(w in name for w in ("game","three","blend","motion","anim")):return "interactive_media"
    if any(w in name for w in ("video","reel","media")):return "media"
    if any(w in name for w in ("research","search","fetch")):return "retrieval"
    if any(w in name for w in ("marketing","content")):return "marketing"
    return "automation"
def reconcile(old=None,which=shutil.which,prober=probe):
    old=old or {};now=discover(which);items={}
    for name,entry in now.items():
        if "error" in entry:
            items[name]={"state":"quarantined_invalid_binary","operations":[]};continue
        known=name in TEMPLATES
        safe_script=name.startswith("yard-") and entry.get("inventory") in ("direct_script_unreviewed","yard_workspace_script")
        passing,reason=(prober(name,entry) if known else
          syntax_probe(entry) if safe_script else (False,"adapter_needed"))
        profile=TEMPLATES[name][0] if known else script_profile(name) if safe_script else None
        items[name]={**entry,"profile":profile,"quality_policy":QAVER,"rule":VERSION,
          "required_checks":list(REQUIREMENTS[profile]) if profile else [],
           "adapter_template":"exact_version_probe" if known else
              "read_only_syntax_probe" if safe_script else "none",
          "state":"accepted_qa_probe_only" if passing else "quarantined_needs_certification",
          "proof":reason,"operations":[("probe_version" if known else "syntax_probe")] if passing else [],
          "owner_approved":False,"production_live":False,
          "unbounded_execution_permitted":False}
    for name,entry in old.items():
        if name not in now:items[name]={**entry,"state":"quarantined_binary_missing",
                                        "operations":[],"production_live":False}
    return {"schema":1,"rule":VERSION,"default":"inherit_or_quarantine",
            "updated_at":datetime.now(timezone.utc).isoformat(),"tools":items,
            "automatic_live":False,"direct_ssh_intercepted":False}
def load(path=REGISTRY):
    p=Path(path)
    if p.is_symlink():raise AdapterDenied("registry_symlink")
    if not p.exists():return {}
    if not p.is_file() or p.stat().st_size>80000:raise AdapterDenied("registry_invalid")
    d=json.loads(p.read_text())
    if d.get("schema")!=1 or not isinstance(d.get("tools"),dict):
        raise AdapterDenied("schema_invalid")
    return d["tools"]
def save(d,path=REGISTRY):
    p=Path(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.is_symlink():raise AdapterDenied("registry_symlink")
    tmp=p.with_suffix(".tmp")
    if tmp.exists():raise AdapterDenied("registry_update_in_progress")
    with tmp.open("x") as f:
        os.fchmod(f.fileno(),0o600)
        json.dump(d,f,sort_keys=True,indent=2);f.write("\n");f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)
    # Generate per-tool bounded adapter manifests for the full discovered yard.
    # Manifests are metadata, not executable wrappers or permission grants.
    manifest_dir=p.parent/"yard-adapter-manifests-v1"
    if manifest_dir.is_symlink():raise AdapterDenied("manifest_dir_symlink")
    manifest_dir.mkdir(mode=0o700,exist_ok=True)
    for name,item in d["tools"].items():
        if not re.fullmatch(r"[a-z][a-z0-9_-]{1,39}",name):continue
        manifest={"schema":1,"name":name,"rule":VERSION,"quality_policy":QAVER,
          "profile":item.get("profile"),"source_sha256":item.get("sha256"),
          "checks":item.get("required_checks",[]),
          "bounded_adapter":item.get("adapter_template","none"),
          "verified_operations":item.get("operations",[]),
          "admission":item.get("state"),"arbitrary_exec":False,
          "owner_release":False,"production_go_live":False}
        out=manifest_dir/(name+".json")
        if out.is_symlink():raise AdapterDenied("manifest_symlink")
        draft=out.with_suffix(".tmp")
        if draft.exists():raise AdapterDenied("manifest_write_collision")
        with draft.open("x") as m:
            os.fchmod(m.fileno(),0o600);json.dump(manifest,m,sort_keys=True,indent=2)
            m.write("\n")
        os.replace(draft,out)
    return p
def preflight(name,op,registry=REGISTRY,which=shutil.which):
    if op not in ("probe_version","syntax_probe"):raise AdapterDenied("operation_not_certified")
    x=load(registry).get(name)
    if not x or x.get("state")!="accepted_qa_probe_only":
        raise AdapterDenied("tool_not_admitted")
    if op not in x.get("operations",[]):raise AdapterDenied("no_certified_operation")
    if op=="syntax_probe":
        binary=Path(x["binary"]).resolve(strict=True)
        parent=binary.parent
        direct=parent in (HERE,HERE.parent/"managed-tools")
        workspace=parent if parent.parent==HERE.parent else parent.parent
        scoped=(workspace.parent==HERE.parent and
          workspace.name.startswith(("matrix-","threejs-","shaadi-","delulu-",
                                     "wp-manager-","eccrm-","andaz-","moksha-")) and
          parent in (workspace,workspace/"src",workspace/"scripts",workspace/"tools"))
        if Path(x["binary"]).is_symlink() or not (direct or scoped):
            raise AdapterDenied("script_scope_denied")
    else:
        p=which(name)
        if not p:raise AdapterDenied("tool_missing")
        binary=safe(name,p)
    if str(binary)!=x.get("binary") or sha(binary)!=x.get("sha256"):
        raise AdapterDenied("binary_changed_quarantined")
    return x
def state(registry=REGISTRY):
    items=load(registry)
    return {"rule":VERSION,"total":len(items),
       "qa_probe_accepted":sum(x.get("state")=="accepted_qa_probe_only" for x in items.values()),
       "quarantined":sum(x.get("state")!="accepted_qa_probe_only" for x in items.values()),
       "tools":{name:{"state":r.get("state"),"profile":r.get("profile"),
                       "operations":r.get("operations",[])} for name,r in sorted(items.items())},
       "controller_inheritance_actions":len(ACTION_PROFILES),
       "direct_ssh_intercepted":False,"production_go_live":False}
def reconcile_if_due(interval_seconds=300, registry=REGISTRY):
    """Called by the common controller tick, never a shell profile hook."""
    target=Path(registry)
    if target.is_symlink():raise AdapterDenied("registry_symlink")
    managed=HERE.parent/"managed-tools"
    due=not target.exists()
    if not due:
        age=max(0,__import__("time").time()-target.stat().st_mtime)
        due=age>=interval_seconds
        if managed.is_dir() and managed.stat().st_mtime>target.stat().st_mtime:
            due=True
    if not due:return {"reconciled":False,"reason":"not_due"}
    updated=reconcile(load(registry))
    save(updated,registry)
    return {"reconciled":True,"total":len(updated["tools"]),
       "accepted_qa_probe_only":sum(x.get("state")=="accepted_qa_probe_only" for x in updated["tools"].values()),
       "quarantined":sum(x.get("state")!="accepted_qa_probe_only" for x in updated["tools"].values()),
       "production_go_live":False}
def main():
    import argparse
    ap=argparse.ArgumentParser(description="Dell governed tool adapter inventory")
    subs=ap.add_subparsers(dest="cmd",required=True)
    for name in ("discover","reconcile","status"):subs.add_parser(name)
    c=subs.add_parser("check");c.add_argument("name");c.add_argument("operation")
    args=ap.parse_args()
    if args.cmd=="discover":v=discover()
    elif args.cmd=="reconcile":
        saved=reconcile(load());save(saved)
        v={"result":"reconciled","rule":VERSION,**state()}
    elif args.cmd=="status":v=state()
    else:
        x=preflight(args.name,args.operation)
        v={"accepted":True,"operation":args.operation,"binary_sha256":x["sha256"],
           "scope":"QA-probe-only","go_live":False}
    print(json.dumps(v,indent=2))
if __name__=="__main__":main()
