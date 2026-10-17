"""Example: python -m matrix.demo --request 'Build a website' """
import argparse
import json
from uuid import uuid4
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from .graph import build_matrix


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", default="Build a standalone customer portal")
    parser.add_argument("--departments", nargs="*", help="Optional explicit work order")
    parser.add_argument("--simulate-qa-repair", action="store_true")
    parser.add_argument("--decision", choices=["approve", "deny"],
                        help="In demo only: resume an approval interrupt")
    args = parser.parse_args()
    graph = build_matrix(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": str(uuid4())}}
    state = {"request": args.request, "force_fail_first": args.simulate_qa_repair}
    if args.departments:
        state["requested_departments"] = args.departments
    result = graph.invoke(state, config=config)
    if "__interrupt__" in result:
        if not args.decision:
            print(json.dumps({"status": "paused_for_human_approval",
                              "interrupt": [x.value for x in result["__interrupt__"]]}, indent=2))
            print("No decision provided. End of demo (in-memory checkpoint lost on exit).")
            return
        result = graph.invoke(Command(resume={"approved": args.decision == "approve",
                                               "reviewer": "local-demo"}), config=config)
    print(json.dumps({
        "status": result["status"], "final": result["final"],
        "feedback": result.get("feedback", []),
        "evolution": result.get("evolution", {}),
    }, indent=2))


if __name__ == "__main__":
    main()
