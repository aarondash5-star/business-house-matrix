"""Canonical, project-local department definitions: independent of other masters."""
from __future__ import annotations

DEPARTMENTS = (
    "concept", "design", "development", "qa_qc", "marketing",
    "sales", "accounts", "support", "evolution",
)

# Permissions are examples of least-privilege intended exposure, NOT an auth boundary.
DEPARTMENT_TOOL_SCOPES = {
    "concept": ["research.read", "briefs.write_draft"],
    "design": ["assets.read", "designs.write_draft"],
    "development": ["code.read", "code.write_branch", "tests.run"],
    "qa_qc": ["code.read", "tests.run", "reports.write_draft"],
    "marketing": ["analytics.read", "campaigns.write_draft"],
    "sales": ["crm.read", "offers.write_draft"],
    "accounts": ["ledger.read", "reports.write_draft"],
    "support": ["tickets.read", "replies.write_draft"],
    "evolution": ["outcomes.read", "evaluations.run", "proposals.write_draft"],
}

SENSITIVE_ACTIONS = (
    "publish", "send", "delete", "deploy", "payment", "transfer",
    "grant access", "revoke", "change permissions", "production", "purchase",
    "post live", "merge", "refund",
)


def proposed_departments(request: str) -> list[str]:
    q = request.lower()
    if any(x in q for x in ("learn", "evolve", "retrain", "training", "train ", "correct the agent")):
        return ["evolution"]
    if any(x in q for x in ("launch", "go to market", "campaign")):
        return ["concept", "design", "marketing", "sales"]
    if any(x in q for x in ("build", "develop", "software", "app ", "website")):
        return ["concept", "design", "development", "qa_qc"]
    if any(x in q for x in ("invoice", "budget", "expense", "accounts")):
        return ["accounts", "qa_qc"]
    if any(x in q for x in ("customer", "support", "ticket")):
        return ["support"]
    return ["concept"]
