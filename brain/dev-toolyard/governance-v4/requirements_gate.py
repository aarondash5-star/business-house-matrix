#!/usr/bin/env python3
"""Dev Tool Yard v4: bounded requirements→method→execution→independent-QA gate.

Data-only evaluation. No shell dispatch, model calls, approvals, site changes,
auto-merges or release permissions. Source and evidence must be independently pinned.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import stat
from pathlib import Path, PurePosixPath

SAFE = re.compile(r"^[a-z][a-z0-9_-]{1,63}$")
SHA = re.compile(r"^[0-9a-f]{64}$")
MAX_RECORD = 196608
MAX_ARTIFACT = 8_000_000
STAGES = ("intake", "capability", "execution", "independent_qa", "owner_review")
DENY = {"production", "published", "released", "merged", "owner_approved"}
VALID_TERMINAL = {"completed", "failed", "needs_review", "unknown"}
class GateDenied(ValueError):
    pass

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def safe_component(value):
    if not isinstance(value, str) or not SAFE.fullmatch(value):
        raise GateDenied("invalid_scoped_identifier")
    return value

def safe_relative(path: str) -> Path:
    if not isinstance(path,str) or len(path)>180 or "\\" in path:
        raise GateDenied("unsafe_path")
    p=PurePosixPath(path)
    if p.is_absolute() or any(q in ("", ".", "..") for q in p.parts):
        raise GateDenied("path_escape")
    if any(not re.fullmatch(r"[A-Za-z0-9_.-]+",q) for q in p.parts):
        raise GateDenied("unsafe_path")
    return Path(*p.parts)

def load(path: Path):
    if path.is_symlink() or not path.is_file():
        raise GateDenied("unsafe_record")
    s=path.stat()
    if not stat.S_ISREG(s.st_mode) or s.st_size<2 or s.st_size>MAX_RECORD:
        raise GateDenied("invalid_record_size")
    if s.st_mode & (stat.S_IWGRP|stat.S_IWOTH):
        raise GateDenied("mutable_record")
    try:
        o=json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeError,json.JSONDecodeError) as e:
        raise GateDenied("unreadable_record") from e
    if not isinstance(o,dict):
        raise GateDenied("record_must_be_object")
    return o

def artifact_digest(root: Path, name: str) -> str:
    rel=safe_relative(name)
    base=(root/"artifacts").resolve(strict=True)
    t=base/rel
    if t.is_symlink() or any(x.is_symlink() for x in t.parents if x != base.parent):
        raise GateDenied("artifact_symlink")
    path=t.resolve(strict=True)
    if not path.is_relative_to(base) or not path.is_file() or path.stat().st_size>MAX_ARTIFACT:
        raise GateDenied("artifact_scope_or_size")
    return sha(path.read_bytes())

def identity_check(a, b):
    if not isinstance(a,str) or not isinstance(b,str) or not a.strip() or a==b:
        raise GateDenied("independent_identity_required")

def evaluate(root: Path, manifest: dict) -> dict:
    """Return stage-specific blockers and no release claims. Fail-closed on malformed input."""
    root=Path(root).resolve(strict=True)
    if not isinstance(manifest,dict) or manifest.get("schema_version")!=1:
        raise GateDenied("unsupported_manifest_schema")
    project=safe_component(manifest.get("project"))
    task=safe_component(manifest.get("task_id"))
    result={"policy":"yard-requirements-gate-v4","project":project,"task_id":task,
            "stage":"intake","status":"blocked","blockers":[],
            "requirements_verified":0,"requirements_total":0,
            "capabilities_verified":0,"method_fit_verified":False,
            "technical_tests_verified":False,"independent_qa_verified":False,
            "owner_accepted":False,"release_authorized":False,
            "production_published":False,"repair_automatically_executed":False}
    def blocked(stage, *what):
        result.update(stage=stage,status="blocked",blockers=list(what))
        return result
    source=manifest.get("source",{})
    if not isinstance(source,dict) or set(source)!={"path","sha256"}:
        return blocked("intake","immutable_brief_required")
    if not isinstance(source["sha256"],str) or not SHA.fullmatch(source["sha256"]):
        return blocked("intake","bad_brief_digest")
    try:
        path=root/safe_relative(source["path"])
        if path.is_symlink() or not path.is_file() or path.resolve(strict=True).parent != root:
            return blocked("intake","source_outside_task")
        if sha(path.read_bytes())!=source["sha256"]:
            return blocked("intake","brief_source_hash_drift")
    except (OSError,GateDenied):
        return blocked("intake","brief_unavailable")
    brief_text=path.read_text(encoding="utf-8",errors="replace")
    reqs=manifest.get("requirements")
    if not isinstance(reqs,list) or not (1<=len(reqs)<=200):
        return blocked("intake","requirements_matrix_missing")
    ids=set(); all_ids=set()
    for r in reqs:
        if not isinstance(r,dict) or set(r)!={"id","source_quote","acceptance","nonnegotiable","capability_id","forbidden_substitutes","evidence_type"}:
            return blocked("intake","requirement_fields_missing")
        try:
            rid=safe_component(r["id"])
            cap=safe_component(r["capability_id"])
        except GateDenied:
            return blocked("intake","requirement_identifier_invalid")
        if rid in ids or r["nonnegotiable"] is not True or not isinstance(r["source_quote"],str) or len(r["source_quote"].strip())<8:
            return blocked("intake","weakened_or_duplicate_requirement")
        if r["source_quote"].strip() not in brief_text:
            return blocked("intake","critical_quote_not_in_original_brief")
        if not isinstance(r["acceptance"],str) or len(r["acceptance"].strip())<15:
            return blocked("intake","acceptance_not_testable")
        if not isinstance(r["evidence_type"],str) or r["evidence_type"] not in ("functional","visual","security","performance","negative","source"):
            return blocked("intake","evidence_type_missing")
        if not isinstance(r["forbidden_substitutes"],list) or any(not isinstance(x,str) or len(x)<3 for x in r["forbidden_substitutes"]):
            return blocked("intake","substitution_policy_missing")
        ids.add(rid);all_ids.add(cap)
    result["requirements_total"]=result["requirements_verified"]=len(ids)
    caps=manifest.get("capabilities")
    if not isinstance(caps,list) or not (1<=len(caps)<=64):
        return blocked("capability","capability_inventory_required")
    bycap={}
    for c in caps:
        if not isinstance(c,dict) or set(c)!={"id","version","license","probe","probe_artifact","probe_sha256","approved_operations"}:
            return blocked("capability","capability_schema_invalid")
        try: cid=safe_component(c["id"])
        except GateDenied: return blocked("capability","capability_id_invalid")
        if cid in bycap or not c["version"] or not c["license"] or c["probe"] is not True:
            return blocked("capability","capability_not_verified")
        if not SHA.fullmatch(str(c["probe_sha256"])) or not isinstance(c["approved_operations"],list) or not c["approved_operations"]:
            return blocked("capability","capability_probe_or_ops_missing")
        try:
            if artifact_digest(root,c["probe_artifact"])!=c["probe_sha256"]:
                return blocked("capability","capability_probe_artifact_drift")
        except (OSError,GateDenied):
            return blocked("capability","capability_probe_missing")
        bycap[cid]=c
    if not all_ids.issubset(bycap):
        return blocked("capability","required_capability_missing")
    methods=manifest.get("methods")
    if not isinstance(methods,list) or len(methods)!=len(ids):
        return blocked("capability","method_per_requirement_required")
    covered=set()
    for m in methods:
        if not isinstance(m,dict) or set(m)!={"requirement_id","capability_id","operation","implementation_method","method_proof","method_proof_sha256"}:
            return blocked("capability","method_fields_missing")
        if m["requirement_id"] not in ids or m["requirement_id"] in covered:
            return blocked("capability","duplicate_or_missing_method")
        r=next(x for x in reqs if x["id"]==m["requirement_id"])
        if m["capability_id"]!=r["capability_id"]:
            return blocked("capability","wrong_capability_for_requirement")
        if m["operation"] not in bycap[m["capability_id"]]["approved_operations"]:
            return blocked("capability","unapproved_tool_operation")
        if not isinstance(m["implementation_method"],str) or len(m["implementation_method"])<8:
            return blocked("capability","method_missing")
        if any(word.lower() in m["implementation_method"].lower() for word in r["forbidden_substitutes"]):
            return blocked("capability","forbidden_implementation_substitution")
        try:
            if artifact_digest(root,m["method_proof"])!=m["method_proof_sha256"]:
                return blocked("capability","method_proof_drift")
        except (OSError,GateDenied):
            return blocked("capability","method_proof_missing")
        covered.add(m["requirement_id"])
    result["capabilities_verified"]=len(bycap)
    result["method_fit_verified"]=True
    execution=manifest.get("execution",{})
    if not isinstance(execution,dict) or set(execution)!={"state","exit_code","source_sha256","artifacts","tests","worker_id","receipt_artifact","receipt_sha256"}:
        return blocked("execution","terminal_execution_receipt_required")
    if execution["state"]!="completed" or execution["exit_code"]!=0 or not SHA.fullmatch(str(execution["source_sha256"])):
        return blocked("execution","execution_not_terminal_success")
    if not isinstance(execution["artifacts"],list) or not execution["artifacts"] or not isinstance(execution["tests"],list) or not execution["tests"]:
        return blocked("execution","real_artifacts_and_tests_required")
    if not isinstance(execution["worker_id"],str) or not execution["worker_id"].strip():
        return blocked("execution","worker_identity_missing")
    try:
        if artifact_digest(root,execution["receipt_artifact"])!=execution["receipt_sha256"]:
            return blocked("execution","receipt_drift")
        for a in execution["artifacts"]:
            if not isinstance(a,dict) or set(a)!={"path","sha256"} or artifact_digest(root,a["path"])!=a["sha256"]:
                return blocked("execution","source_artifact_drift")
    except (OSError,GateDenied,KeyError,TypeError):
        return blocked("execution","receipt_or_artifact_missing")
    found=set()
    for t in execution["tests"]:
        if not isinstance(t,dict) or set(t)!={"requirement_id","status","evidence_path","sha256"} or t["requirement_id"] not in ids or t["requirement_id"] in found:
            return blocked("execution","test_traceability_missing")
        if t["status"]!="passed":return blocked("execution","tests_failed")
        try:
            if artifact_digest(root,t["evidence_path"])!=t["sha256"]:return blocked("execution","test_receipt_drift")
        except (OSError,GateDenied):return blocked("execution","test_evidence_missing")
        found.add(t["requirement_id"])
    if found!=ids: return blocked("execution","mandatory_test_coverage_incomplete")
    result["technical_tests_verified"]=True
    qa=manifest.get("independent_qa",{})
    if not isinstance(qa,dict) or set(qa)!={"reviewer_id","producer_id","results","review_receipt","review_sha256"}:
        return blocked("independent_qa","independent_review_missing")
    try:identity_check(qa["reviewer_id"],qa["producer_id"])
    except GateDenied:return blocked("independent_qa","self_review_rejected")
    if qa["producer_id"]!=execution["worker_id"]:
        return blocked("independent_qa","producer_identity_mismatch")
    try:
        if artifact_digest(root,qa["review_receipt"])!=qa["review_sha256"]:
            return blocked("independent_qa","review_artifact_drift")
    except (OSError,GateDenied):
        return blocked("independent_qa","independent_review_receipt_missing")
    if not isinstance(qa["results"],list) or len(qa["results"])!=len(ids):
        return blocked("independent_qa","independent_qa_coverage_missing")
    reviewed=set()
    for row in qa["results"]:
        if not isinstance(row,dict) or set(row)!={"requirement_id","status","observed_artifact","sha256"} or row["requirement_id"] not in ids or row["requirement_id"] in reviewed:
            return blocked("independent_qa","qa_trace_invalid")
        if row["status"]!="passed":return blocked("independent_qa","independent_semantic_qa_failed")
        try:
            if artifact_digest(root,row["observed_artifact"])!=row["sha256"]:
                return blocked("independent_qa","observed_evidence_drift")
        except (OSError,GateDenied):
            return blocked("independent_qa","observed_artifact_missing")
        reviewed.add(row["requirement_id"])
    result["independent_qa_verified"]=True
    return result | {"stage":"owner_review","status":"ready_for_owner_review","blockers":["separate_owner_acceptance_required"],
                     "owner_accepted":False,"release_authorized":False}

def main():
    p=argparse.ArgumentParser(description="Fail-closed Dev Yard v4 delivery fidelity checker")
    p.add_argument("root",type=Path,help="Single isolated task evidence root")
    p.add_argument("manifest",type=Path,help="Manifest JSON under that task root")
    a=p.parse_args()
    try:
        root=a.root.resolve(strict=True)
        mf=a.manifest.resolve(strict=True)
        if mf.parent!=root:raise GateDenied("manifest_must_be_in_task_root")
        result=evaluate(root,load(mf))
        print(json.dumps(result,indent=2))
        raise SystemExit(0 if result["status"]=="ready_for_owner_review" else 2)
    except (GateDenied,OSError,TypeError,KeyError) as e:
        print(json.dumps({"status":"blocked","error":str(e),"owner_accepted":False,"release_authorized":False}))
        raise SystemExit(2)
if __name__=="__main__":main()
