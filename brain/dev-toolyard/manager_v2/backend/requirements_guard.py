"""Immutable RTM and owner intent verification; never take a coverage percentage on trust."""
from pathlib import Path
import hashlib,json,re,stat

class ScopeDenied(ValueError): pass
HEX=re.compile(r"^[a-f0-9]{64}$")
ID=re.compile(r"^mgr_r(0[1-9]|1[0-2])$")
REQUIRED={"schema_version","project","manifest","profile","criteria","brief_sha256"}

def protected_bytes(p,limit=250000):
 p=Path(p)
 if p.is_symlink() or not p.is_file() or any(a.is_symlink() for a in (p.parent,p.parent.parent)):
  raise ScopeDenied("unsafe_missing_record")
 s=p.stat()
 if not 0<s.st_size<=limit or s.st_mode & (stat.S_IWGRP|stat.S_IWOTH):
  raise ScopeDenied("unsafe_record_permissions")
 return p.read_bytes()
def sha(value): return hashlib.sha256(value).hexdigest()
def load_frozen(base):
 base=Path(base)
 b=protected_bytes(base/"brief.md")
 raw=protected_bytes(base/"quality-contract.json",65536)
 c=json.loads(raw)
 if set(c)!=REQUIRED or sha(b)!=c["brief_sha256"]:
  raise ScopeDenied("brief_contract_drift")
 if c["project"]!="matrix_dev_manager" or c["profile"]!="automation" or not isinstance(c["criteria"],list):
  raise ScopeDenied("foreign_contract")
 ids=[x["id"] for x in c["criteria"]]
 if len(ids)!=12 or set(ids)!={f"mgr_r{i:02d}" for i in range(1,13)} or len(ids)!=len(set(ids)):
  raise ScopeDenied("frozen_contract_missing_critical_ids")
 return b.decode("utf-8"),c,sha(raw)
def verify_rtm(base,records,expected_contract_sha):
 brief,c,contract_sha=load_frozen(base)
 if contract_sha!=expected_contract_sha or not HEX.fullmatch(expected_contract_sha):
  raise ScopeDenied("contract_sha_drift")
 if not isinstance(records,list) or len(records)!=12:
  raise ScopeDenied("critical_coverage_incomplete")
 expected={x["id"]:x for x in c["criteria"]}
 seen=set()
 for r in records:
  if not isinstance(r,dict) or set(r)!={"requirement_id","source_quote","nonnegotiable","measurable_acceptance","evidence_type","validator","method_id"}:
   raise ScopeDenied("malformed_requirement")
  ident=r["requirement_id"]
  if ident not in expected or ident in seen:raise ScopeDenied("unknown_or_duplicate_requirement")
  seen.add(ident)
  if r["nonnegotiable"] is not True or r["measurable_acceptance"]!=expected[ident]["acceptance"]:
   raise ScopeDenied("critical_requirement_mutated")
  quote=r["source_quote"]
  if not isinstance(quote,str) or len(quote)<10 or quote not in brief:
   raise ScopeDenied("source_quote_not_in_frozen_brief")
  for k in ("evidence_type","validator","method_id"):
   if not isinstance(r[k],str) or len(r[k].strip())<8:raise ScopeDenied("unverifiable_requirement")
 if seen!=set(expected):raise ScopeDenied("critical_requirement_missing")
 return {"status":"rtm_complete","coverage":len(seen),"source_sha256":c["brief_sha256"],
         "contract_sha256":contract_sha,"requirements":sorted(seen),"release_authorized":False}
def build_rtm_from_frozen(base,method_id="reviewed_dell_toolyard"):
 """Produce a draft for owner/QA review; no auto approval or evidence fabrication."""
 brief,c,_=load_frozen(base)
 lines=brief.splitlines()
 rows={}
 for line in lines:
  for i in range(1,13):
   ident=f"MGR-R{i:02d}"
   if ident in line and "|" in line and ident not in rows:rows[ident]=line.strip()
 if len(rows)!=12:raise ScopeDenied("source_has_no_full_rtm")
 return [{"requirement_id":x["id"],"source_quote":rows[x["id"].upper().replace("_","-")],
          "nonnegotiable":True,"measurable_acceptance":x["acceptance"],
          "evidence_type":"real hash pinned independently reviewed file",
          "validator":"independent authenticated QA plus owner","method_id":method_id} for x in c["criteria"]]
