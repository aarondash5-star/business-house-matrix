import pytest
pytest.importorskip("langgraph")
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from matrix.graph import build_matrix


def test_recursive_graph_dispatch_and_evolution():
    result = build_matrix().invoke({"request": "Build an app"})
    assert result["status"] == "completed_simulation"
    assert result["final"]["executed_departments"] == ["concept", "design", "development", "qa_qc"]
    assert result["final"]["external_actions_executed"] is False
    assert result["evolution"]["promotion_status"] == "proposal_only_unapproved"


def test_repair_retry_stays_bounded():
    result = build_matrix().invoke({"request": "A concept", "force_fail_first": True})
    assert result["status"] == "completed_simulation"
    assert result["attempts"]["concept"] == 2
    assert any(not x["passed"] for x in result["feedback"])


def test_qa_blocked_with_zero_retry():
    result = build_matrix().invoke({"request": "A concept", "force_fail_first": True,
                                    "max_retries": 0})
    assert result["status"] == "blocked_by_quality_gate"
    assert result["final"]["external_actions_executed"] is False
    assert result["evolution"]["failed"] >= 1


def test_sensitive_work_requires_approval():
    graph = build_matrix(checkpointer=MemorySaver())
    cfg = {"configurable": {"thread_id": "approval-test"}}
    result = graph.invoke({"request": "Deploy new code to production"}, config=cfg)
    assert result.get("__interrupt__")
    result = graph.invoke(Command(resume={"approved": False, "reviewer": "test"}), config=cfg)
    assert result["status"] == "approval_denied"
