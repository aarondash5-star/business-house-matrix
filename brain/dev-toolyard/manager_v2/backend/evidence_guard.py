"""Authenticated independent QA verification. Private signing keys never live here."""
import base64,hashlib,json,re,os,stat
from datetime import datetime,timezone,timedelta
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
class EvidenceDenied(ValueError):pass
SHA=re.compile(r"^[0-9a-f]{64}$")
TRUST_FILE=Path("/etc/business-house-matrix/independent-qa-trust-v1.json")
REQUIRED_GEOMETRY={"folds","backfaces","self_occlusion","shading","parallax","geometry_normals"}
def sha(path):
 p=Path(path)
 if p.is_symlink() or not p.is_file():raise EvidenceDenied("missing_real_artifact")
 return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(d):return json.dumps(d,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def verify_review(signed,trust_store,evidence_root,source_sha,developer_identity,project,manifest,contract_sha):
 """Trust store must be provisioned independently outside dev writable directories."""
 p=Path(trust_store)
 if p.absolute()!=TRUST_FILE or p.is_symlink() or not p.is_file():
  raise EvidenceDenied("trusted_owner_managed_key_store_required")
 if p.stat().st_uid!=0 or p.stat().st_mode & (stat.S_IWGRP|stat.S_IWOTH):
  raise EvidenceDenied("reviewer_trust_store_not_independent")
 trusted=json.loads(p.read_text())
 if not isinstance(trusted,dict) or trusted.get("schema_version")!=1 or not isinstance(trusted.get("reviewers"),dict):
  raise EvidenceDenied("invalid_trust_store")
 if not isinstance(signed,dict) or set(signed)!={"payload","key_id","signature"}:
  raise EvidenceDenied("malformed_attestation")
 body=signed["payload"]
 if not isinstance(body,dict) or set(body)!={"reviewer_id","source_sha256","contract_sha256","project","manifest","artifacts","observations","decision","review_time_utc"}:
  raise EvidenceDenied("malformed_attested_payload")
 key_id=signed["key_id"]; reviewer=body["reviewer_id"]
 entry=trusted["reviewers"].get(key_id)
 if not isinstance(entry,dict) or entry.get("identity")!=reviewer or entry.get("role")!="independent_qa":
  raise EvidenceDenied("independent_reviewer_not_enrolled")
 if (reviewer==developer_identity or body["source_sha256"]!=source_sha or
     body["project"]!=project or body["manifest"]!=manifest or
     body["contract_sha256"]!=contract_sha or not SHA.fullmatch(source_sha) or not SHA.fullmatch(contract_sha)):
  raise EvidenceDenied("reviewer_or_source_drift")
 try:
  key=Ed25519PublicKey.from_public_bytes(base64.b64decode(entry["public_key_b64"],validate=True))
  key.verify(base64.b64decode(signed["signature"],validate=True),canonical(body))
 except (InvalidSignature,ValueError,TypeError,KeyError) as err:
  raise EvidenceDenied("signature_invalid") from err
 artifacts=body["artifacts"]
 if not isinstance(artifacts,dict) or set(artifacts)!={"frames","geometry","renderer"}:
  raise EvidenceDenied("required_artifacts_missing")
 root=Path(evidence_root).resolve()
 for name,item in artifacts.items():
  if not isinstance(item,dict) or set(item)!={"path","sha256"} or not isinstance(item["path"],str) or not SHA.fullmatch(str(item["sha256"])):
   raise EvidenceDenied("bad_artifact_reference")
  target=(root/item["path"]).resolve()
  if not target.is_relative_to(root) or sha(target)!=item["sha256"]:
   raise EvidenceDenied("forged_or_missing_artifact")
 observations=body["observations"]
 if not isinstance(observations,dict) or set(observations)!=REQUIRED_GEOMETRY:
  raise EvidenceDenied("geometry_observations_incomplete")
 try:
  reviewed=datetime.fromisoformat(body["review_time_utc"].replace("Z","+00:00"))
 except (TypeError,ValueError,AttributeError) as err:
  raise EvidenceDenied("review_timestamp_invalid") from err
 if reviewed.tzinfo is None or reviewed>datetime.now(timezone.utc)+timedelta(minutes=5):
  raise EvidenceDenied("review_timestamp_not_trusted")
 if not all(observations[k] is True for k in REQUIRED_GEOMETRY) or body["decision"]!="qa_pass":
  return {"status":"independent_qa_failed","release_authorized":False,"reason":"physical_geometry_or_review_rejected"}
 return {"status":"owner_review_pending","qa_identity":reviewer,"observed_real_files":True,
         "release_authorized":False,"owner_accepted":False}
