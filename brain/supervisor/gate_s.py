#!/usr/bin/env python3
"""Gate S experimental reasoning supervisor. Proposal-only; no executor integration.

The model may suggest work, but only hard-coded capabilities can ever be routed.
No imports from the certified v6 controller and no live service modifications.
"""
import argparse
import json
import re
import sys
import urllib.request

ROUTES = {
    "research": "approved_public_research_reader",
    "design": "offline_architecture_proposal",
    "coding": "enrolled_dev_sandbox_proposal",
    "qa": "independent_bubblewrap_test",
    "security": "fixed_policy_security_review",
    "review": "human_review_queue",
}
ID_PATTERN = re.compile(r"s[1-6]$")
MODEL = "qwen3:4b-instruct"
API = "http://127.0.0.1:11434/api/generate"
MAX_STEPS = 6

class SupervisorError(ValueError):
    pass

def _text(value, length):
    return isinstance(value, str) and 3 <= len(value.strip()) <= length and not any(ord(c) < 32 for c in value)

def validate_plan(raw):
    """Strict, capability-limited proposal; rejects ambiguous model output."""
    if not isinstance(raw, dict) or set(raw) != {"summary", "steps"}:
        raise SupervisorError("plan_schema")
    if not _text(raw["summary"], 280):
        raise SupervisorError("summary_invalid")
    steps = raw["steps"]
    if not isinstance(steps, list) or not 4 <= len(steps) <= MAX_STEPS:
        raise SupervisorError("step_count")
    seen = {}
    validated = []
    for i, step in enumerate(steps, start=1):
        if not isinstance(step, dict) or set(step) != {"id", "role", "objective", "depends_on"}:
            raise SupervisorError("step_schema")
        sid = step["id"]
        if not isinstance(sid, str) or not ID_PATTERN.fullmatch(sid) or sid != "s" + str(i):
            raise SupervisorError("step_identity")
        role = step["role"]
        if not isinstance(role, str) or role not in ROUTES:
            raise SupervisorError("role_not_enrolled")
        if not _text(step["objective"], 300):
            raise SupervisorError("objective_invalid")
        deps = step["depends_on"]
        if not isinstance(deps, list) or len(deps) != len(set(map(str, deps))):
            raise SupervisorError("dependencies_invalid")
        if i == 1 and deps:
            raise SupervisorError("first_step_has_dependency")
        if i > 1 and not deps:
            raise SupervisorError("unconnected_step")
        if any(not isinstance(d, str) or d not in seen for d in deps):
            raise SupervisorError("unknown_or_forward_dependency")
        seen[sid] = role
        validated.append(dict(id=sid, role=role, objective=step["objective"].strip(), depends_on=list(deps)))
    roles = [x["role"] for x in validated]
    if roles[-1] != "review" or roles.count("review") != 1:
        raise SupervisorError("review_must_be_last")
    if roles.count("qa") != 1 or roles.count("security") != 1:
        raise SupervisorError("missing_quality_or_security_gate")
    qa_i = roles.index("qa")
    sec_i = roles.index("security")
    if not 0 < qa_i < sec_i < len(roles) - 1:
        raise SupervisorError("quality_gate_order")
    if any(role == "coding" for role in roles[qa_i + 1:]):
        raise SupervisorError("coding_after_qa")
    if "coding" in roles[:qa_i] and not any(seen[d] == "coding" for d in validated[qa_i]["depends_on"]):
        raise SupervisorError("qa_must_depend_on_code")
    if "s" + str(qa_i + 1) not in validated[sec_i]["depends_on"]:
        raise SupervisorError("security_must_depend_on_qa")
    if "s" + str(sec_i + 1) not in validated[-1]["depends_on"]:
        raise SupervisorError("review_must_depend_on_security")
    return {"summary": raw["summary"].strip(), "steps": validated}

def route_preview(raw):
    """Preview trusted worker types. NEVER dispatch or execute from here."""
    proposal = validate_plan(raw)
    return {
        "mode": "proposal_only",
        "execute": False,
        "push": False,
        "publish": False,
        "model_controls_permissions": False,
        "summary": proposal["summary"],
        "work_order": [
            {"id": s["id"], "role": s["role"], "worker": ROUTES[s["role"]],
             "objective": s["objective"], "depends_on": s["depends_on"]}
            for s in proposal["steps"]
        ],
        "approval": "separate_owner_and_independent_QA_required",
    }

def assess_receipt(receipt, retries=0):
    """Independent deterministic response to worker evidence, no blind replay."""
    if not isinstance(receipt, dict) or not isinstance(retries, int) or retries < 0:
        return "escalate_invalid_evidence"
    status = receipt.get("status")
    if status in ("security_denied", "policy_denied", "source_mismatch"):
        return "escalate_security"
    if status in ("running", "queued"):
        return "await_receipt"
    if status == "passed":
        return "human_review" if receipt.get("qa_passed") is True and receipt.get("security_passed") is True else "escalate_missing_verification"
    if status in ("qa_failed", "worker_timeout") and retries < 1 and receipt.get("approved_scope") is True:
        return "propose_replan_only"
    if status in ("qa_failed", "worker_timeout"):
        return "escalate_retry_budget"
    return "escalate_unknown_or_unverified"

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None

def local_model_proposal(goal):
    """Local-only reasoning. A network-disabled QA workcell NEVER calls this."""
    if not _text(goal, 350) or len(goal.encode("utf-8")) > 600:
        raise SupervisorError("public_goal_invalid")
    schema = {
        "type": "object",
        "required": ["summary", "steps"],
        "additionalProperties": False,
        "properties": {
            "summary": {"type": "string"},
            "steps": {"type": "array", "minItems": 4, "maxItems": 6,
              "items": {"type": "object", "required": ["id","role","objective","depends_on"],
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "role": {"type": "string", "enum": list(ROUTES)},
                    "objective": {"type": "string"},
                    "depends_on": {"type": "array", "items": {"type": "string"}}
                }
            }}
        }
    }
    prompt = (
        "You are a planning-only software development supervisor. Never execute, request secrets, publish, or spend. "
        "Return a small sequential work plan of EXACTLY five steps, roles in order: research, coding, qa, security, review. "
        "IDs s1-s5; s1 depends_on []; every later step depends_on only the directly previous ID. "
        "The QA step must check code generated by coding. Review requires prior security clearance. "
        "Keep each objective brief and specific. Model output is a PROPOSAL, not permission. "
        "Public, non-sensitive task: " + goal
    )
    body = {
        "model": MODEL, "stream": False, "keep_alive": "0",
        "format": schema, "prompt": prompt,
        "options": {"temperature": 0, "num_ctx": 2048, "num_predict": 520, "num_thread": 4}
    }
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    req = urllib.request.Request(API, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with opener.open(req, timeout=115) as r:
            if r.status != 200:
                raise SupervisorError("ollama_status")
            payload = r.read(34000)
        env = json.loads(payload)
        if env.get("model") not in (MODEL, MODEL + ":latest"):
            raise SupervisorError("model_identity")
        return validate_plan(json.loads(env["response"]))
    except (TimeoutError, urllib.error.URLError) as exc:
        raise SupervisorError("model_transport_unavailable") from exc
    except (KeyError, ValueError, TypeError) as exc:
        raise SupervisorError("model_response_invalid") from exc

def main():
    parser = argparse.ArgumentParser(description="Nonproduction Gate S planning smoke")
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if not args.smoke:
        parser.error("only --smoke (fixed public benchmark) is supported")
    try:
        proposal = local_model_proposal("Build a public Python expense parser with strict unit tests in an isolated sandbox.")
        print(json.dumps(route_preview(proposal), sort_keys=True))
    except SupervisorError as exc:
        print(json.dumps({"status": "needs_review", "reason": str(exc), "executed": False}))
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
