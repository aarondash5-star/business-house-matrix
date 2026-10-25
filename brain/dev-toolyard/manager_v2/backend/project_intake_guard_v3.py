"""Scope router for a new Delulu folding task. Prior V2 is not an approval for physical origami."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path("/var/lib/generic-linux-automator-exec/matrix-controller")
class ProjectScopeDenied(ValueError):pass
SHA=re.compile(r"^[a-f0-9]{64}$")
NAME=re.compile(r"^[a-z][a-z0-9_]{2,39}$")
def digest(raw):return hashlib.sha256(raw).hexdigest()
def read_project_contract(project,manifest,root=ROOT):
 if not all(isinstance(x,str) and NAME.fullmatch(x) for x in (project,manifest)):raise ProjectScopeDenied("invalid_project")
 base=Path(root)/"quality-inbox"/project/manifest
 if base.is_symlink() or not base.is_dir():raise ProjectScopeDenied("no_enrolled_project")
 files=[base/"brief.md",base/"quality-contract.json"]
 if any(not f.is_file() or f.is_symlink() or f.stat().st_mode&0o022 for f in files):raise ProjectScopeDenied("unsafe_contract")
 bref,raw=(x.read_bytes() for x in files)
 c=json.loads(raw)
 if c.get("project")!=project or c.get("manifest")!=manifest or c.get("brief_sha256")!=digest(bref):raise ProjectScopeDenied("contract_drift")
 if not isinstance(c.get("criteria"),list) or not c["criteria"]:raise ProjectScopeDenied("no_criteria")
 return {"project":project,"manifest":manifest,"brief":bref.decode(),"contract":c,"brief_sha256":digest(bref),"contract_sha256":digest(raw),"release_authorized":False}
def verify_owner_intake(project,manifest,action,expected_sha,root=ROOT):
 item=read_project_contract(project,manifest,root)
 if not SHA.fullmatch(expected_sha) or item["contract_sha256"]!=expected_sha:raise ProjectScopeDenied("contract_not_frozen")
 p=subprocess.run([sys.executable,str(Path(root)/"quality_admission.py"),"intake",project,manifest,"--action",action],capture_output=True,text=True,timeout=18)
 if p.returncode:raise ProjectScopeDenied("existing_controller_admission_denied")
 v=json.loads(p.stdout)
 if v.get("status")!="approved_intake" or v.get("contract_sha256")!=expected_sha or v.get("release_authorized") is not False:raise ProjectScopeDenied("approval_drift")
 return item
def require_actual_folds(item,change_ref):
 if not isinstance(change_ref,str) or not change_ref.startswith("https://github.com/"):raise ProjectScopeDenied("versioned_owner_change_ref_required")
 b=item["brief"].lower()
 accepts=[str(x.get("acceptance","")).lower() for x in item["contract"]["criteria"]]
 mandatory=("actual 3d mesh","front and back surfaces","self-occlusion","five review keyframes","frozen svg sha")
 if not all(s in b and any(s in a for a in accepts) for s in mandatory):
  raise ProjectScopeDenied("outdated_creative_contract_no_physical_folds")
 if "no production publish" not in b:raise ProjectScopeDenied("release_scope_not_private")
 return {"status":"project_scope_verified","project":item["project"],"manifest":item["manifest"],
         "requirements_covered":len(item["contract"]["criteria"]),"brief_sha256":item["brief_sha256"],"contract_sha256":item["contract_sha256"],
         "change_ref":change_ref,"release_authorized":False}
def propose_only(item):
 return {"status":"project_only_draft","project":item["project"],"requirements":[x["id"] for x in item["contract"]["criteria"]],
         "method":"blender actual mesh deforming fold, not SVG alpha reveal","auto_dispatch":False,"auto_release":False}
