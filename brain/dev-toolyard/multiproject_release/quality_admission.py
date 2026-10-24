"""Mandatory owner-scoped intake and release gates for every Tool Yard project.

No model can approve its own creative requirements. This module is read-only:
operator approvals must be recorded through separately controlled owner actions.
"""
from __future__ import annotations
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import re
import stat

ROOT=Path(__file__).resolve().parent
RUN_ACTIONS=frozenset(("website_stage","dev_project_build","dev_general_build",
                        "dev_scoped_build","pine_chat_stage","video_preview",
                        "repair_known_issue"))
PLATFORMS=frozenset(("vercel","cloudflare","wordpress","github_pages","other"))
ENVIRONMENTS=frozenset(("preview","staging","production"))
HEX64=re.compile(r"^[0-9a-f]{64}$")
SLUG=re.compile(r"^[a-z][a-z0-9_-]{1,39}$")

class AdmissionDenied(ValueError):pass

def _file(path:Path,limit:int=65536)->bytes:
    if path.is_symlink() or not path.is_file():raise AdmissionDenied("protected_record_missing")
    st=path.stat()
    if st.st_size<1 or st.st_size>limit or st.st_mode & (stat.S_IWGRP|stat.S_IWOTH):
        raise AdmissionDenied("protected_record_unsafe")
    if any(a.is_symlink() for a in (path.parent,path.parent.parent)):
        raise AdmissionDenied("protected_path_symlink")
    return path.read_bytes()

def _json(path:Path):
    try:return json.loads(_file(path))
    except (TypeError,UnicodeError,json.JSONDecodeError) as e:raise AdmissionDenied("invalid_record_json") from e

def _validate_identity(project,manifest):
    if not isinstance(project,str) or not SLUG.fullmatch(project) or not isinstance(manifest,str) or not SLUG.fullmatch(manifest):
        raise AdmissionDenied("project_manifest_invalid")

def _entries(path:Path,field):
    doc=_json(path)
    if not isinstance(doc,dict) or set(doc)!={"schema_version",field} or doc["schema_version"]!=1 or not isinstance(doc[field],list) or len(doc[field])>200:
        raise AdmissionDenied("approval_ledger_invalid")
    return doc[field]

def _contract(project,manifest,root):
    from quality_gate import evaluate,PROFILES
    base=Path(root)/"quality-inbox"/project/manifest
    path=base/"quality-contract.json"
    content=_file(path)
    c=_json(path)
    brief_bytes=_file(base/"brief.md",limit=250000)
    brief_sha=hashlib.sha256(brief_bytes).hexdigest()
    contract_sha=hashlib.sha256(content).hexdigest()
    if (not isinstance(c,dict) or c.get("project")!=project or c.get("manifest")!=manifest or
        c.get("brief_sha256")!=brief_sha or c.get("profile") not in PROFILES):
        raise AdmissionDenied("brief_or_contract_not_pinned")
    check=evaluate(project,manifest,root)
    if check.get("status") not in ("evidence_missing","evidence_ready_for_owner_review","evidence_not_passed","independent_review_missing","visual_observation_missing"):
        raise AdmissionDenied("quality_contract_invalid:"+str(check.get("status")))
    return c,contract_sha,brief_sha,check

def intake_check(project,action,manifest,root=ROOT):
    """Hard stop at submit AND dispatch, including previously queued work."""
    if action not in RUN_ACTIONS:
        return {"required":False,"status":"read_only_or_nonbuild"}
    _validate_identity(project,manifest)
    c,sha,brief_sha,_=_contract(project,manifest,root)
    entries=_entries(Path(root)/"owner-intake-approvals-v1.json","approvals")
    found=[]
    for x in entries:
        if not isinstance(x,dict) or set(x)!={"project","manifest","profile","contract_sha256","brief_sha256","approval_ref","approved_by"}:
            raise AdmissionDenied("approval_ledger_record_invalid")
        if (x["project"],x["manifest"])==(project,manifest):found.append(x)
    if len(found)!=1:raise AdmissionDenied("owner_intake_approval_missing_or_ambiguous")
    x=found[0]
    if (x["profile"]!=c["profile"] or x["contract_sha256"]!=sha or x["brief_sha256"]!=brief_sha or
        x["approved_by"]!="owner" or not isinstance(x["approval_ref"],str) or not x["approval_ref"].startswith("https://") or len(x["approval_ref"])<20):
        raise AdmissionDenied("owner_intake_approval_drift")
    return {"required":True,"status":"approved_intake","profile":c["profile"],
            "contract_sha256":sha,"brief_sha256":brief_sha,"release_authorized":False}

def release_check(project,manifest,platform,environment,artifact_sha256,root=ROOT):
    """Preflight only. Does NOT publish. Actual deployment wrapper must use this."""
    _validate_identity(project,manifest)
    if platform not in PLATFORMS or environment not in ENVIRONMENTS or not isinstance(artifact_sha256,str) or not HEX64.fullmatch(artifact_sha256):
        raise AdmissionDenied("invalid_release_target_or_artifact_hash")
    approval=intake_check(project,"website_stage",manifest,root)
    from quality_gate import evaluate
    state=evaluate(project,manifest,root)
    if state["status"]!="evidence_ready_for_owner_review":
        raise AdmissionDenied("independent_quality_evidence_not_ready")
    base=Path(root)/"quality-inbox"/project/manifest
    evidence_sha=hashlib.sha256(_file(base/"evidence.json")).hexdigest()
    entries=_entries(Path(root)/"owner-release-approvals-v1.json","approvals")
    matched=[]
    for x in entries:
        if not isinstance(x,dict) or set(x)!={"project","manifest","contract_sha256","evidence_sha256","artifact_sha256","platform","environment","expires_utc","approval_ref","approved_by"}:
            raise AdmissionDenied("release_ledger_invalid_entry")
        if x["project"]==project and x["manifest"]==manifest and x["platform"]==platform and x["environment"]==environment:
            matched.append(x)
    if len(matched)!=1:raise AdmissionDenied("explicit_owner_release_approval_missing")
    x=matched[0]
    try:expiry=datetime.fromisoformat(x["expires_utc"].replace("Z","+00:00"))
    except (AttributeError,ValueError) as err:raise AdmissionDenied("release_approval_expiry_invalid") from err
    if expiry.tzinfo is None or expiry<=datetime.now(timezone.utc):raise AdmissionDenied("release_approval_expired")
    if (x["contract_sha256"]!=approval["contract_sha256"] or x["evidence_sha256"]!=evidence_sha or
        x["artifact_sha256"]!=artifact_sha256 or x["approved_by"]!="owner" or
        not isinstance(x["approval_ref"],str) or not x["approval_ref"].startswith("https://")):
        raise AdmissionDenied("release_artifact_or_approval_drift")
    return {"status":"preflight_authorized","project":project,"manifest":manifest,
            "platform":platform,"environment":environment,"artifact_sha256":artifact_sha256,
            "authorization_type":"owner_managed_record","published":False}

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("command",choices=("intake","release-check"))
    p.add_argument("project");p.add_argument("manifest")
    p.add_argument("--action",default="website_stage")
    p.add_argument("--platform",default="vercel")
    p.add_argument("--environment",default="preview")
    p.add_argument("--artifact-sha256",default="")
    a=p.parse_args()
    value=intake_check(a.project,a.action,a.manifest) if a.command=="intake" else release_check(a.project,a.manifest,a.platform,a.environment,a.artifact_sha256)
    print(json.dumps(value,indent=2))
if __name__=="__main__":main()
