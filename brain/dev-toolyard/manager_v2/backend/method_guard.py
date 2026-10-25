"""Execution provenance and capability fit. A logo alpha mask is never 3D folding."""
from pathlib import Path
import hashlib,json,re
class MethodDenied(ValueError):pass
SHA=re.compile(r"^[0-9a-f]{64}$")
OFFICIAL={"bmad":"bmad-method@6.12.4","langgraph":"langgraph==1.2.17",
          "spec_kit":"specify-cli==1.2.3"}
def file_sha(path):
 p=Path(path)
 if not p.is_file() or p.is_symlink():raise MethodDenied("source_not_real_file")
 return hashlib.sha256(p.read_bytes()).hexdigest()
def check_stack(workspace):
 w=Path(workspace)
 refs={"bmad":w/"_bmad/_config/manifest.yaml",
       "spec_kit":w/".integrations/spec-workspace/.specify/integrations/speckit.manifest.json",
       "langgraph":w/".integrations/pip-freeze.lock"}
 for p in refs.values():
  if not p.is_file() or p.is_symlink():raise MethodDenied("stack_not_installed")
 skills=w/".claude/skills"
 required=["bmad-agent-analyst","bmad-agent-pm","bmad-agent-architect","bmad-agent-dev"]
 missing=[x for x in required if not (skills/x).is_dir()]
 if missing:raise MethodDenied("bmad_skills_missing:"+",".join(missing))
 if "langgraph==" not in refs["langgraph"].read_text() or "specify-cli==" not in refs["langgraph"].read_text():
  raise MethodDenied("dependency_lock_missing")
 return {"status":"installed_and_pinned","versions":OFFICIAL,
         "artifact_sha256":{k:file_sha(v) for k,v in refs.items()},
         "bmad_roles":required,"code_execution_verified":False}
def verify_method_receipt(receipt,workspace,source_path):
 """Worker receipts have real observed local files; never claim independent semantics."""
 if not isinstance(receipt,dict) or set(receipt)!={"method_id","tool","version","source_sha256","execution_receipt_path","execution_receipt_sha256","verified_artifact_path","verified_artifact_sha256","stage"}:
  raise MethodDenied("method_receipt_bad_schema")
 if receipt["stage"]!="private_dev" or receipt["tool"] not in OFFICIAL or receipt["version"]!=OFFICIAL[receipt["tool"]]:
  raise MethodDenied("unapproved_tool_version_or_stage")
 if not SHA.fullmatch(str(receipt["execution_receipt_sha256"])) or not SHA.fullmatch(str(receipt["source_sha256"])):
  raise MethodDenied("missing_method_provenance")
 if file_sha(source_path)!=receipt["source_sha256"]:raise MethodDenied("source_changed")
 w=Path(workspace).resolve()
 exec_receipt=(w/receipt["execution_receipt_path"]).resolve()
 if not exec_receipt.is_relative_to(w) or file_sha(exec_receipt)!=receipt["execution_receipt_sha256"]:
  raise MethodDenied("execution_receipt_unverifiable")
 target=(w/receipt["verified_artifact_path"]).resolve()
 if not target.is_relative_to(w) or file_sha(target)!=receipt["verified_artifact_sha256"]:
  raise MethodDenied("untrusted_artifact")
 return {"status":"method_evidence_present","method_id":receipt["method_id"],"actual_artifact_sha256":receipt["verified_artifact_sha256"],"semantic_approval":False}
def inspect_fold_candidate(renderer_source,video_path):
 """Deterministic rejection of the documented alpha-mask shortcut; not positive proof of 3D."""
 src=Path(renderer_source); vid=Path(video_path)
 if not src.is_file() or not vid.is_file() or src.is_symlink() or vid.is_symlink():
  raise MethodDenied("real_renderer_media_missing")
 s=src.read_text()
 banned=("alpha_from_svg(","a*reveal","reveal=smooth","GaussianBlur")
 if sum(t in s for t in banned)>=3 and "vertex" not in s and "mesh" not in s:
  return {"status":"negative_fixture_rejected","reason":"svg_mask_reveal_without_geometry",
          "renderer_sha256":file_sha(src),"media_sha256":file_sha(vid),"geometry_verified":False}
 return {"status":"requires_independent_geometry_review","renderer_sha256":file_sha(src),
         "media_sha256":file_sha(vid),"geometry_verified":False}
