"""Project-independent delivery-quality governor for Matrix Tool Yard.

Technical success is not artistic acceptance, product acceptance, or publication
authorization. This module never grants those permissions.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat

HERE = Path(__file__).resolve().parent
PROFILES = {
    "creative_web": {"brief_trace", "visual_sequence", "responsive", "accessibility", "independent_review"},
    "functional_app": {"brief_trace", "functional_tests", "security", "independent_review"},
    "automation": {"brief_trace", "negative_tests", "recovery", "independent_review"},
    "media": {"brief_trace", "sampled_frames", "asset_fidelity", "independent_review"},
    "documentation": {"brief_trace", "source_checks", "independent_review"},
}
SAFE = re.compile(r"^[a-z][a-z0-9_-]{1,39}$")
ARTIFACT_LIMIT = 32
MAX_FILE = 5_000_000

class QualityError(ValueError):
    pass

def _load(path: Path, max_bytes=65536):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > max_bytes:
        raise QualityError("missing_or_unsafe_json")
    if path.stat().st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        raise QualityError("world_or_group_writable_record")
    return json.loads(path.read_text(encoding="utf-8"))

def _safe_rel(name):
    if not isinstance(name, str) or len(name) > 180 or "\\" in name:
        raise QualityError("invalid_artifact_path")
    p = PurePosixPath(name)
    if p.is_absolute() or ".." in p.parts or "." in p.parts or not all(re.fullmatch("[a-zA-Z0-9_.-]+", x) for x in p.parts):
        raise QualityError("path_escape_denied")
    return p

def evaluate(project: str, manifest: str, root: Path=HERE) -> dict:
    """Inspect owner-scoped quality evidence. Never issue self-service signoff."""
    if not isinstance(project, str) or not SAFE.fullmatch(project) or not isinstance(manifest,str) or not SAFE.fullmatch(manifest):
        raise QualityError("invalid_project_manifest")
    base = Path(root)/"quality-inbox"/project/manifest
    out = {"policy_version": 1, "project": project, "manifest": manifest,
           "technical_build_may_complete": True, "design_verified": False,
           "owner_approved": False, "release_authorized": False,
           "claim_limit": "technical_prototype_only"}
    contract=base/"quality-contract.json"
    if not contract.is_file():
        return {**out, "status":"requirements_missing", "missing":["owner_approved_quality_contract"]}
    try:
        c=_load(contract)
        if set(c)!={"schema_version","project","manifest","profile","criteria","brief_sha256"} or c["schema_version"]!=1 or c["project"]!=project or c["manifest"]!=manifest:
            raise QualityError("quality_contract_mismatch")
        if c["profile"] not in PROFILES or not re.fullmatch(r"[a-f0-9]{64}",c["brief_sha256"]):
            raise QualityError("unknown_profile_or_brief")
        criteria=c["criteria"]
        if not isinstance(criteria,list) or not (1<=len(criteria)<=30):
            raise QualityError("invalid_criteria")
        by_kind={}
        for item in criteria:
            if not isinstance(item,dict) or set(item)!={"id","kind","acceptance","required"}:
                raise QualityError("invalid_criterion")
            kind=item["kind"]
            if kind not in PROFILES[c["profile"]] or item["required"] is not True or not isinstance(item["acceptance"],str) or not 12<=len(item["acceptance"])<=600:
                raise QualityError("invalid_criterion_content")
            if not isinstance(item["id"],str) or not SAFE.fullmatch(item["id"]) or item["id"] in by_kind:
                raise QualityError("duplicate_or_invalid_criterion")
            by_kind[item["id"]]=kind
        missing_kinds=sorted(PROFILES[c["profile"]]-set(by_kind.values()))
        if missing_kinds: return {**out,"status":"requirements_incomplete","missing":missing_kinds}
        evidence_path=base/"evidence.json"
        if not evidence_path.is_file():return {**out,"status":"evidence_missing","missing":list(by_kind)}
        evidence=_load(evidence_path)
        if not isinstance(evidence,dict) or set(evidence)!={"schema_version","brief_sha256","results"} or evidence["schema_version"]!=1 or evidence["brief_sha256"]!=c["brief_sha256"]:
            raise QualityError("evidence_brief_mismatch")
        results=evidence["results"]
        if not isinstance(results,list) or len(results)!=len(by_kind):
            raise QualityError("evidence_result_mismatch")
        found=set()
        for item in results:
            if not isinstance(item,dict) or set(item)!={"id","status","artifact","sha256","reviewer_type"}:
                raise QualityError("bad_evidence_entry")
            ident=item["id"]
            if ident not in by_kind or ident in found:raise QualityError("unknown_or_duplicate_criterion")
            found.add(ident)
            if item["status"]!="passed" or item["reviewer_type"] not in ("automated", "independent_human", "external_model"):
                return {**out,"status":"evidence_not_passed","missing":[ident]}
            if by_kind[ident]=="independent_review" and item["reviewer_type"]!="independent_human":
                return {**out,"status":"independent_review_missing","missing":[ident]}
            if by_kind[ident] in ("visual_sequence","sampled_frames","asset_fidelity") and item["reviewer_type"]=="external_model":
                return {**out,"status":"visual_observation_missing","missing":[ident]}
            rel=_safe_rel(item["artifact"])
            target=base/"artifacts"/Path(*rel.parts)
            if not target.is_file() or target.is_symlink() or target.stat().st_size>MAX_FILE or target.stat().st_size==0:
                raise QualityError("artifact_missing_or_unsafe")
            if any(parent.is_symlink() for parent in target.parents if parent != Path(root).parent):
                raise QualityError("artifact_symlink_denied")
            if not isinstance(item["sha256"],str) or not re.fullmatch(r"[a-f0-9]{64}",item["sha256"]) or hashlib.sha256(target.read_bytes()).hexdigest()!=item["sha256"]:
                raise QualityError("artifact_hash_mismatch")
        return {**out,"status":"evidence_ready_for_owner_review","missing":[],
                "claim_limit":"review_pending_not_design_approved"}
    except (ValueError,TypeError,KeyError) as err:
        return {**out,"status":"quality_contract_rejected","missing":[type(err).__name__+":"+str(err)[:90]]}

def annotate(project: str, manifest: str, technical: dict, root: Path=HERE) -> dict:
    result=dict(technical)
    result["quality_gate"]=evaluate(project,manifest,root)
    result["technical_only"]=True
    result["design_complete"]=False
    result["release_approved"]=False
    return result

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("action",choices=("check","profiles"))
    p.add_argument("project",nargs="?")
    p.add_argument("manifest",nargs="?")
    args=p.parse_args()
    if args.action=="profiles":print(json.dumps({k:sorted(v) for k,v in PROFILES.items()},indent=2))
    else:print(json.dumps(evaluate(args.project,args.manifest),indent=2))

if __name__=="__main__":
    main()
