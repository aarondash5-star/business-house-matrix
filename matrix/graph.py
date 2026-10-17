"""A runnable LangGraph implementation of the recursive Business House Matrix.

The MVP executes a safe, deterministic *simulation*. Real tool calls, LLMs,
and cross-run learning need to be connected, authorized and tested separately.
"""
from __future__ import annotations

from typing import Any
from typing_extensions import TypedDict

from langgraph.graph import START, END, StateGraph
from langgraph.types import interrupt

from .config import DEPARTMENTS, DEPARTMENT_TOOL_SCOPES, SENSITIVE_ACTIONS, proposed_departments


class MatrixState(TypedDict, total=False):
    request: str
    requested_departments: list[str]
    task_type: str
    work_order: list[str]
    cursor: int
    department: str
    plan: list[str]
    attempts: dict[str, int]
    artifacts: list[dict[str, Any]]
    department_quality: dict[str, Any]
    integration_quality: dict[str, Any]
    feedback: list[dict[str, Any]]
    evolution: dict[str, Any]
    approval_required: bool
    approval_decision: dict[str, Any]
    max_retries: int
    force_fail_first: bool  # Test-only fault injection.
    status: str
    final: dict[str, Any]


def make_department_subgraph(name: str):
    """Every department has the *same* recursive Brain→Execute→QA→Evolve graph."""
    assert name in DEPARTMENTS

    def brain(state: MatrixState) -> dict:
        return {"plan": [
            f"Interpret the request as a {name} assignment",
            f"Work within scopes: {', '.join(DEPARTMENT_TOOL_SCOPES[name])}",
            "Produce auditable deliverables, then test the result",
        ]}

    def execute(state: MatrixState) -> dict:
        attempts = dict(state.get("attempts", {}))
        attempt = attempts.get(name, 0) + 1
        attempts[name] = attempt
        # Intentionally simulated: does NOT claim real marketing, payment,
        # development, publishing or financial actions have been performed.
        artifact = {
            "department": name,
            "attempt": attempt,
            "mode": "simulation",
            "summary": f"Draft {name} work package for: {state['request']}",
            "evidence": ["Generated structured draft; no external side effects"],
            "scopes": DEPARTMENT_TOOL_SCOPES[name],
        }
        return {"attempts": attempts, "artifacts": state.get("artifacts", []) + [artifact]}

    def qa(state: MatrixState) -> dict:
        latest = state["artifacts"][-1]
        forced = bool(state.get("force_fail_first", False) and latest["attempt"] == 1)
        ok = bool(latest.get("summary") and latest.get("evidence")) and not forced
        return {"department_quality": {
            "department": name, "passed": ok, "attempt": latest["attempt"],
            "reason": "Injected first-attempt defect" if forced else
                      ("Artifact has traceable contents" if ok else "Incomplete artifact"),
        }}

    def local_evolution(state: MatrixState) -> dict:
        verdict = state["department_quality"]
        return {"feedback": state.get("feedback", []) + [{
            "source": name, "kind": "department_feedback",
            "passed": verdict["passed"], "attempt": verdict["attempt"],
            "action": "Propose corrective evaluation" if not verdict["passed"]
                      else "Archive candidate training example for human curation",
        }]}

    graph = StateGraph(MatrixState)
    graph.add_node("brain", brain)
    graph.add_node("execute", execute)
    graph.add_node("qa", qa)
    graph.add_node("local_evolution", local_evolution)
    graph.add_edge(START, "brain")
    graph.add_edge("brain", "execute")
    graph.add_edge("execute", "qa")
    graph.add_edge("qa", "local_evolution")
    graph.add_edge("local_evolution", END)
    return graph.compile()


def make_evolution_review_subgraph():
    """Evidence-driven improvement proposals. No autonomous model fine-tuning."""
    graph = StateGraph(MatrixState)

    def observe(state: MatrixState) -> dict:
        passed = [x for x in state.get("feedback", []) if x["passed"]]
        failed = [x for x in state.get("feedback", []) if not x["passed"]]
        return {"evolution": {
            "outcomes_observed": len(state.get("feedback", [])),
            "passed": len(passed), "failed": len(failed),
            "candidate_examples": [x for x in passed if x["kind"] == "department_feedback"],
        }}

    def diagnose(state: MatrixState) -> dict:
        record = dict(state["evolution"])
        record["diagnosis"] = (
            "One or more QA defects require regression coverage"
            if record["failed"] else "No failed checks in this simulated run"
        )
        return {"evolution": record}

    def propose(state: MatrixState) -> dict:
        record = dict(state["evolution"])
        record["proposals"] = [
            "Curate approved outcome examples into a versioned training/evaluation dataset",
            "Evaluate candidate changes in a sandbox against regression tests",
            "Require review before promoting prompts, tools, policies, or model versions",
        ]
        return {"evolution": record}

    def validate(state: MatrixState) -> dict:
        record = dict(state["evolution"])
        record["promotion_status"] = "proposal_only_unapproved"
        record["trained_model"] = False
        record["production_modified"] = False
        return {"evolution": record}

    for name, node in (("observe", observe), ("diagnose", diagnose),
                       ("propose", propose), ("validate", validate)):
        graph.add_node(name, node)
    graph.add_edge(START, "observe")
    graph.add_edge("observe", "diagnose")
    graph.add_edge("diagnose", "propose")
    graph.add_edge("propose", "validate")
    graph.add_edge("validate", END)
    return graph.compile()


def build_matrix(checkpointer=None):
    """Build the Central Brain, nine department subgraphs and Evolution loop.

    For resumable interruptions, provide a real checkpointer and invoke the
    graph with config={"configurable":{"thread_id": "..."}}.
    """
    graph = StateGraph(MatrixState)

    def central_brain(state: MatrixState) -> dict:
        request = state.get("request", "").strip()
        if not request:
            raise ValueError("request cannot be empty")
        order = list(state.get("requested_departments") or proposed_departments(request))
        if not order or any(x not in DEPARTMENTS for x in order):
            raise ValueError("Invalid department in work order")
        # Dedup while keeping intent-preserving sequence.
        order = list(dict.fromkeys(order))
        return {
            "work_order": order, "cursor": 0, "attempts": {}, "artifacts": [],
            "feedback": [], "max_retries": min(3, max(0, int(state.get("max_retries", 2)))),
            "approval_required": any(x in request.lower() for x in SENSITIVE_ACTIONS),
            "status": "planned",
        }

    def approval_gate(state: MatrixState) -> dict:
        if not state.get("approval_required", False):
            return {"approval_decision": {"approved": True, "mode": "not_required"}}
        decision = interrupt({
            "type": "human_approval_required",
            "message": "Approval required before processing a sensitive request",
            "request": state["request"], "work_order": state["work_order"],
            "note": "This starter does not execute external actions even when approved.",
        })
        allowed = isinstance(decision, dict) and decision.get("approved") is True
        return {"approval_decision": {
            "approved": allowed,
            "reviewer": decision.get("reviewer") if isinstance(decision, dict) else None,
        }}

    def approval_route(state: MatrixState) -> str:
        return "dispatch" if state["approval_decision"]["approved"] else "reject"

    def dispatch(state: MatrixState) -> dict:
        return {"department": state["work_order"][state["cursor"]]}

    def choose_department(state: MatrixState) -> str:
        return state["department"]

    def integration_qa(state: MatrixState) -> dict:
        dept_ok = state["department_quality"]["passed"]
        item = state["artifacts"][-1]
        scoped = item["department"] == state["department"]
        return {"integration_quality": {
            "passed": bool(dept_ok and scoped),
            "department": state["department"],
            "reason": "Evidence and department match" if dept_ok and scoped else "QA failed",
        }}

    def quality_route(state: MatrixState) -> str:
        if state["integration_quality"]["passed"]:
            return "advance"
        attempts = state.get("attempts", {}).get(state["department"], 0)
        return "repair" if attempts <= state["max_retries"] else "blocked"

    def repair(state: MatrixState) -> dict:
        # No unauthorized modification: go back through the department's
        # planning/QA graph, never blindly patch a production system.
        return {"status": "correcting"}

    def advance(state: MatrixState) -> dict:
        return {"cursor": state["cursor"] + 1, "status": "in_progress"}

    def next_route(state: MatrixState) -> str:
        return "dispatch" if state["cursor"] < len(state["work_order"]) else "evolution_review"

    def finalize(state: MatrixState) -> dict:
        if state.get("status") == "blocked_by_quality_gate":
            return {"final": {**state["final"],
                    "evolution_status": state["evolution"]["promotion_status"]}}
        return {"status": "completed_simulation", "final": {
            "executed_departments": state["work_order"],
            "artifacts_produced": len(state["artifacts"]),
            "all_quality_checks_passed": True,
            "evolution_status": state["evolution"]["promotion_status"],
            "external_actions_executed": False,
        }}

    def reject(state: MatrixState) -> dict:
        return {"status": "approval_denied", "final": {
            "reason": "Human approval was not granted", "external_actions_executed": False,
        }}

    def blocked(state: MatrixState) -> dict:
        return {"status": "blocked_by_quality_gate", "final": {
            "reason": "QA did not pass within bounded retry budget",
            "department": state["department"], "external_actions_executed": False,
        }}

    graph.add_node("central_brain", central_brain)
    graph.add_node("approval_gate", approval_gate)
    graph.add_node("dispatch", dispatch)
    graph.add_node("integration_qa", integration_qa)
    graph.add_node("repair", repair)
    graph.add_node("advance", advance)
    graph.add_node("evolution_review", make_evolution_review_subgraph())
    graph.add_node("finalize", finalize)
    graph.add_node("reject", reject)
    graph.add_node("blocked", blocked)
    for dept in DEPARTMENTS:
        graph.add_node(f"dept_{dept}", make_department_subgraph(dept))
    graph.add_edge(START, "central_brain")
    graph.add_edge("central_brain", "approval_gate")
    graph.add_conditional_edges("approval_gate", approval_route, {
        "dispatch": "dispatch", "reject": "reject",
    })
    graph.add_conditional_edges("dispatch", choose_department, {
        dept: f"dept_{dept}" for dept in DEPARTMENTS
    })
    for dept in DEPARTMENTS:
        graph.add_edge(f"dept_{dept}", "integration_qa")
    graph.add_conditional_edges("integration_qa", quality_route, {
        "advance": "advance", "repair": "repair", "blocked": "blocked",
    })
    graph.add_edge("repair", "dispatch")
    graph.add_conditional_edges("advance", next_route, {
        "dispatch": "dispatch", "evolution_review": "evolution_review",
    })
    graph.add_edge("evolution_review", "finalize")
    graph.add_edge("blocked", "evolution_review")
    for final_node in ("finalize", "reject"):
        graph.add_edge(final_node, END)
    return graph.compile(checkpointer=checkpointer)
