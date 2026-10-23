#!/usr/bin/env python3
"""Gate S v2: evidence-first development planning, separate from certified v6.

No tool execution, no model-selected commands, no publish/push or privileged actions.
The supervisor may *propose* arbitrary-length staged work within a bounded JSON
contract, but never changes permissions or dispatches a worker.
"""
import json
import re
import time
import urllib.request

ROLES = frozenset(("research", "design", "development", "qa", "security", "review"))
MODEL_LOCAL = "qwen3:4b-instruct"
LOCAL_URL = "http://127.0.0.1:11434/api/generate"
MAX_BRIEF_BYTES = 12000

class PlanError(ValueError):
    pass

def clean_text(value, max_len=2000):
    return isinstance(value, str) and 3 <= len(value.strip()) <= max_len and "\x00" not in value

def text_list(value, minimum=1, maximum=12):
    return (isinstance(value, list) and minimum <= len(value) <= maximum and
            all(clean_text(item, 1500) for item in value))

def validate(proposal):
    """Validate the work-order structure and hard security gates, NOT its intelligence."""
    expected = {"project", "strategy", "assumptions", "risks", "milestones", "tasks", "approval"}
    if not isinstance(proposal, dict) or set(proposal) != expected:
        raise PlanError("schema")
    if not clean_text(proposal["project"], 250) or not clean_text(proposal["strategy"], 8000):
        raise PlanError("project_or_strategy")
    if not text_list(proposal["assumptions"], 0, 30):
        raise PlanError("assumptions")
    if not text_list(proposal["risks"], 2, 30):
        raise PlanError("risks")
    if proposal["approval"] != "owner_review_before_execution":
        raise PlanError("approval")
    milestones = proposal["milestones"]
    if not isinstance(milestones, list) or not 2 <= len(milestones) <= 14:
        raise PlanError("milestones")
    milestone_ids = set()
    for m in milestones:
        if not isinstance(m, dict) or set(m) != {"id", "name", "outcome"}:
            raise PlanError("milestone_schema")
        if not isinstance(m["id"], str) or not re.fullmatch(r"M[1-9][0-9]?", m["id"]) or m["id"] in milestone_ids:
            raise PlanError("milestone_identity")
        if not clean_text(m["name"], 200) or not clean_text(m["outcome"], 1500):
            raise PlanError("milestone_text")
        milestone_ids.add(m["id"])
    tasks = proposal["tasks"]
    if not isinstance(tasks, list) or not 6 <= len(tasks) <= 30:
        raise PlanError("task_count")
    seen = set()
    seen_roles = set()
    for task in tasks:
        if not isinstance(task, dict) or set(task) != {
            "id", "milestone", "role", "objective", "deliverables",
            "acceptance", "depends_on", "priority"
        }:
            raise PlanError("task_schema")
        ident = task["id"]
        if not isinstance(ident, str) or not re.fullmatch(r"T[1-9][0-9]?", ident) or ident in seen:
            raise PlanError("task_identity")
        if task["milestone"] not in milestone_ids or task["role"] not in ROLES:
            raise PlanError("role_or_milestone")
        if not clean_text(task["objective"], 1500):
            raise PlanError("objective")
        if not text_list(task["deliverables"], 1, 10) or not text_list(task["acceptance"], 1, 10):
            raise PlanError("missing_deliverables_or_acceptance")
        if task["priority"] not in ("P0", "P1", "P2"):
            raise PlanError("priority")
        deps = task["depends_on"]
        if not isinstance(deps, list) or any(not isinstance(x, str) for x in deps) or len(deps) != len(set(deps)):
            raise PlanError("dependencies")
        if any(dep not in seen for dep in deps):
            raise PlanError("forward_or_unenrolled_dependency")
        seen.add(ident)
        seen_roles.add(task["role"])
    if not {"research", "design", "development", "qa", "security", "review"}.issubset(seen_roles):
        raise PlanError("missing_department")
    if tasks[-1]["role"] != "review":
        raise PlanError("final_review")
    review_deps = tasks[-1]["depends_on"]
    if not review_deps or not any(t["id"] in review_deps and t["role"] in ("qa", "security") for t in tasks[:-1]):
        raise PlanError("final_review_dependency")
    return proposal

def preview(proposal):
    plan = validate(proposal)
    return {"mode": "proposal_only", "execute": False, "push": False,
            "publish": False, "spend": False, "privilege_change": False,
            "model_controls_permissions": False,
            "owner_approval_required": True, "plan": plan}

def plan_prompt(brief):
    if not isinstance(brief, str) or len(brief.encode("utf-8")) > MAX_BRIEF_BYTES or len(brief.strip()) < 80:
        raise PlanError("brief_bounds")
    return (
        "You are an expert technical program manager and software architect. "
        "Prepare a rigorous, specific, actionable PRIVATE STAGING development plan. "
        "Determine the number, order, dependencies, and safe parallelism of tasks yourself. "
        "Cover research and evidence, website/current-state audit, information architecture, UX/UI wireframes, "
        "content and real assets, existing integrations and data, implementation sequencing, "
        "mobile QA, accessibility, performance, SEO, booking journeys, privacy/security, rollback, "
        "risks, exact deliverables, measurable acceptance criteria, and explicit unknowns. "
        "Do not invent prices, existing system capabilities, source inspection, completed research or business facts. "
        "Mark unavailable evidence as audit/verification tasks. Avoid generic boilerplate. "
        "This is a PROPOSAL ONLY. No commands, live changes, merging, publishing or spending. "
        "Return JSON with EXACT root keys: project (string), strategy (detailed string), "
        "assumptions (array of strings), risks (array of strings), milestones (2-14 objects with id M1 etc, name, outcome), "
        "tasks (6-30 objects with id T1 etc, milestone M#, role research|design|development|qa|security|review, "
        "objective, deliverables [strings], acceptance [strings], depends_on [prior T#], priority P0|P1|P2), "
        "approval equal owner_review_before_execution. "
        "Use as many tasks as needed; make the outcome implementable, not a five-step summary. "
        "Mandatory owner brief:\n"+brief
    )

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def propose_local(brief, timeout=190, model=MODEL_LOCAL):
    """Pure local Ollama inference. No staging writes or tool dispatch."""
    if model != MODEL_LOCAL:
        raise PlanError("unapproved_local_model")
    req = {
        "model": model, "stream": False, "keep_alive": "0",
        "format": "json",
        "prompt": plan_prompt(brief),
        "options": {"temperature": 0.15, "num_ctx": 6144,
                    "num_predict": 2800, "num_thread": 4}
    }
    client = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    http = urllib.request.Request(LOCAL_URL, data=json.dumps(req).encode("utf-8"),
                                  headers={"Content-Type": "application/json"}, method="POST")
    start = time.monotonic()
    with client.open(http, timeout=timeout) as resp:
        if resp.status != 200:
            raise PlanError("model_http_status")
        body = resp.read(180001)
        if len(body) > 180000:
            raise PlanError("model_output_limit")
    envelope = json.loads(body)
    if envelope.get("model") not in (model, model+":latest"):
        raise PlanError("model_identity")
    raw = envelope.get("response")
    if not isinstance(raw, str):
        raise PlanError("model_response")
    plan = validate(json.loads(raw))
    return {"model": model, "latency_s": round(time.monotonic()-start, 2),
            "completion_tokens": envelope.get("eval_count"), "output": preview(plan)}
