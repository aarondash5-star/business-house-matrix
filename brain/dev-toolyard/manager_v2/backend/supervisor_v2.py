"""Checkpointed BHM manager. All actionable work remains behind the live Tool Yard."""
import json,os,sqlite3,subprocess,sys
from pathlib import Path
from typing import TypedDict
os.environ.setdefault("LANGGRAPH_STRICT_MSGPACK","true")
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.sqlite import SqliteSaver
from requirements_guard import ScopeDenied,verify_rtm,build_rtm_from_frozen
from method_guard import MethodDenied,check_stack
from evidence_guard import EvidenceDenied,verify_review,TRUST_FILE
ROOT=Path("/var/lib/generic-linux-automator-exec/matrix-controller")
PROJECT="matrix_dev_manager"
class StageError(ValueError):pass
class State(TypedDict,total=False):
 project:str
 manifest:str
 base:str
 workspace:str
 contract_sha256:str
 status:str
 requirements:dict
 methods:dict
 signed_qa:dict
 evidence_root:str
 developer_identity:str
 approved_dispatch:bool
 receipt:dict
 error:str
def graph_builder():
 def scope_stage(state):
  try:
   r=build_rtm_from_frozen(state["base"])
   v=verify_rtm(state["base"],r,state["contract_sha256"])
   return {"requirements":v,"status":"scope_verified"}
  except (KeyError,ScopeDenied) as exc:
   return {"status":"blocked","error":str(exc)}
 def method_stage(state):
  if state.get("status")!="scope_verified":return {}
  try:return {"methods":check_stack(state["workspace"]),"status":"methods_checked"}
  except (KeyError,MethodDenied) as exc:return {"status":"blocked","error":str(exc)}
 def qa_stage(state):
  if state.get("status")=="blocked":return {}
  signed=state.get("signed_qa")
  if not isinstance(signed,dict):
   return {"status":"blocked_independent_qa","approved_dispatch":False}
  try:
   v=verify_review(signed,TRUST_FILE,state["evidence_root"],
      state["requirements"]["source_sha256"],state["developer_identity"],
      state["project"],state["manifest"],state["requirements"]["contract_sha256"])
  except (EvidenceDenied,KeyError) as err:
   return {"status":"blocked_independent_qa","approved_dispatch":False,"error":str(err)}
  if v["status"]!="owner_review_pending":
   return {"status":"blocked_independent_qa","approved_dispatch":False}
  return {"status":"pending_owner_dispatch","approved_dispatch":False}
 def handoff(state):
  # Even authenticated QA cannot sign an owner dispatch or publication approval.
  return {"status":"blocked_owner_dispatch","approved_dispatch":False}
 g=StateGraph(State)
 for name,fn in (("scope",scope_stage),("methods",method_stage),("qa_gate",qa_stage),("handoff",handoff)):
  g.add_node(name,fn)
 g.add_edge(START,"scope");g.add_edge("scope","methods");g.add_edge("methods","qa_gate")
 g.add_edge("qa_gate","handoff");g.add_edge("handoff",END)
 return g
class DurableManager:
 def __init__(self,db):
  self.db=Path(db)
  if self.db.exists() and self.db.is_symlink():raise StageError("symlink_database_denied")
  self.db.parent.mkdir(parents=True,exist_ok=True)
  self.conn=sqlite3.connect(str(self.db),check_same_thread=False)
  self.saver=SqliteSaver(self.conn)
  self.graph=graph_builder().compile(checkpointer=self.saver,interrupt_before=["handoff"])
 def config(self,thread_id):
  if not isinstance(thread_id,str) or len(thread_id)<8 or len(thread_id)>96 or not all(x.isalnum() or x in "_-" for x in thread_id):
   raise StageError("bad_thread_id")
  return {"configurable":{"thread_id":thread_id}}
 def start(self,thread_id,payload):
  cfg=self.config(thread_id)
  if self.graph.get_state(cfg).values:raise StageError("thread_already_started")
  return self.graph.invoke(payload,cfg)
 def inspect(self,thread_id):
  snap=self.graph.get_state(self.config(thread_id))
  return {"values":snap.values,"next":list(snap.next),"exists":bool(snap.values)}
 def resume(self,thread_id):
  # The graph itself never submits to controller or bypasses owner decisions.
  return self.graph.invoke(None,self.config(thread_id))
 def close(self):self.conn.close()
def controller_intake_check(project,manifest):
 if project!=PROJECT:raise StageError("foreign_project_denied")
 cmd=[sys.executable,str(ROOT/"quality_admission.py"),"intake",project,manifest,"--action","dev_project_build"]
 p=subprocess.run(cmd,capture_output=True,text=True,stdin=subprocess.DEVNULL,timeout=15)
 if p.returncode:raise StageError("live_owner_intake_denied")
 obj=json.loads(p.stdout)
 if obj.get("status")!="approved_intake" or obj.get("release_authorized") is not False:
  raise StageError("live_controller_intake_not_safe")
 return obj
def prepare_handoff_only(project,manifest,verified_qa,owner_dispatch_permission=False):
 """Project-scoped proposal, never a privileged shell fallback."""
 intake=controller_intake_check(project,manifest)
 if verified_qa.get("status")!="owner_review_pending":
  raise StageError("independent_qa_not_verified")
 if owner_dispatch_permission is not True:
  return {"status":"awaiting_separate_owner_dispatch_decision","controller_intake":intake["status"],"submitted":False}
 return {"status":"owner_dispatch_decision_required_outside_manager","submitted":False,
         "controller_command":["python3",str(ROOT/"controller.py"),"submit",project,"dev_project_build",manifest]}
