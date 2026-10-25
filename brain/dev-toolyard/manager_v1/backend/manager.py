"""Project-scoped Matrix Dev Yard Manager. Never publishes or self-approves."""
import hashlib,re
from typing import TypedDict
SHA=re.compile(r"^[0-9a-f]{64}$")
IDENT=re.compile(r"^[a-z][a-z0-9_-]{1,39}$")
NEEDS=("requirement_id","source_quote_or_pointer","nonnegotiable","measurable_acceptance","evidence_type","validator")
GEOMETRY=("folds","backfaces","self_occlusion","shading","parallax","geometry_normals")
BMAD_ROLES=("analyst","product_manager","architect","developer","qa")
class GovernanceError(ValueError):pass
def frozen_brief(source,expected_sha):
 if not isinstance(source,bytes) or not SHA.fullmatch(expected_sha) or hashlib.sha256(source).hexdigest()!=expected_sha:raise GovernanceError("frozen_source_drift")
 return source.decode("utf-8")
def scope(requirements,source_sha):
 if not SHA.fullmatch(source_sha) or not isinstance(requirements,list) or not requirements:raise GovernanceError("frozen_scope_missing")
 seen=set()
 for r in requirements:
  if not isinstance(r,dict) or any(k not in r for k in NEEDS):raise GovernanceError("critical_traceability_missing")
  ident=r["requirement_id"]
  if not isinstance(ident,str) or ident in seen or not re.fullmatch(r"[A-Z]+-R[0-9]{2,3}",ident):raise GovernanceError("duplicate_requirement")
  seen.add(ident)
  if r["nonnegotiable"] is not True or any(not isinstance(r[k],str) or len(r[k].strip())<10 for k in NEEDS if k not in ("requirement_id","nonnegotiable")):raise GovernanceError("critical_requirement_weakened")
 return {"status":"scoped","requirements":requirements,"source_sha256":source_sha,"critical_coverage":1.0}
def plan(scoped,project,manifest):
 if scoped.get("status")!="scoped" or scoped.get("critical_coverage")!=1.0:raise GovernanceError("unscoped_work_denied")
 if not all(isinstance(x,str) and IDENT.fullmatch(x) for x in (project,manifest)):raise GovernanceError("invalid_project_manifest")
 return {"status":"ready_for_toolyard","project":project,"manifest":manifest,"action":"dev_project_build","dispatch_authorized":False,"release_authorized":False,"requirement_ids":[x["requirement_id"] for x in scoped["requirements"]]}
def spec_payload(scoped):
 if scoped.get("status")!="scoped":raise GovernanceError("spec_without_frozen_scope")
 return {"source_sha256":scoped["source_sha256"],"spec":"\n".join(x["requirement_id"]+": "+x["source_quote_or_pointer"]+" | PASS: "+x["measurable_acceptance"] for x in scoped["requirements"]),"state":"draft_pending_review"}
def bmad_roles(scoped):
 if scoped.get("status")!="scoped":raise GovernanceError("bmad_without_scope")
 return {"roles":list(BAD_ROLES) if False else list(BMAD_ROLES),"owner_fingerprint":scoped["source_sha256"],"agents_may_self_approve":False}
def review_fold_evidence(evidence,developer="developer"):
 missing=[k for k in GEOMETRY if evidence.get(k) is not True]
 if missing:return {"status":"independent_qa_failed","reason":"real_folds_missing","missing":missing,"release_authorized":False}
 if evidence.get("reviewer_type")!="independent_human" or evidence.get("reviewer_id") in (None,"",developer):return {"status":"independent_qa_failed","reason":"independent_review_missing","release_authorized":False}
 if not all(isinstance(evidence.get(k),str) and SHA.fullmatch(evidence[k]) for k in ("actual_frames_sha256","geometry_trace_sha256")):return {"status":"independent_qa_failed","reason":"authentic_frames_missing","release_authorized":False}
 return {"status":"owner_review_pending","owner_accepted":False,"release_authorized":False}
class State(TypedDict,total=False):
 requirements:list
 source_sha256:str
 project:str
 manifest:str
 result:dict
 error:str
def manager_graph():
 from langgraph.graph import StateGraph,START,END
 def interpret(state):
  try:return {"result":scope(state["requirements"],state["source_sha256"])}
  except (GovernanceError,KeyError) as exc:return {"result":{"status":"independent_qa_failed"},"error":str(exc)}
 def dispatch_plan(state):
  if state.get("error"):return {}
  return {"result":plan(state["result"],state["project"],state["manifest"])}
 def hold(state):return {"result":{**state.get("result",{}),"dispatch_authorized":False,"release_authorized":False}}
 g=StateGraph(State)
 for name,fn in (("interpret",interpret),("plan",dispatch_plan),("hold",hold)):g.add_node(name,fn)
 g.add_edge(START,"interpret")
 g.add_conditional_edges("interpret",lambda s:"hold" if s.get("error") else "plan")
 g.add_edge("plan","hold");g.add_edge("hold",END)
 return g.compile()
