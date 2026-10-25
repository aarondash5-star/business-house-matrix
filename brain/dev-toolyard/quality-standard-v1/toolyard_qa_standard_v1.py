"""Universal Dell Dev Tool Yard quality receipt; not an authorization source.

Every controller action has a declared quality profile. No automated technical
result, external model, or developer self-review is a human brand signoff or a
release approval. Existing project gates remain the sole owner-authorized source.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

VERSION = "toolyard-qa-v1.0.0-20261025"
ACTION_PROFILES = {
    "research_search": "retrieval",
    "dev_docs_fetch": "retrieval",
    "dev_proposal": "documentation",
    "dev_scoped_build": "functional_app",
    "dev_general_build": "functional_app",
    "dev_project_build": "functional_app",
    "game_toolkit": "interactive_media",
    "website_stage": "creative_web",
    "pine_chat_stage": "functional_app",
    "sandbox_qa": "verification",
    "repair_known_issue": "automation",
    "marketing_draft": "marketing",
    "video_preview": "media",
}
REQUIREMENTS = {
    "retrieval": ("source_provenance", "bounded_scope", "no_mutation"),
    "documentation": ("frozen_source", "requirement_trace", "source_checks", "independent_review"),
    "functional_app": ("frozen_brief", "scope_binding", "unit_tests", "negative_security_tests", "mobile_if_ui", "independent_review", "recovery"),
    "interactive_media": ("frozen_brief", "source_fidelity", "frame_or_pixel_visibility", "interaction", "mobile", "reduced_motion", "independent_review", "recovery"),
    "creative_web": ("frozen_brief", "source_fidelity", "rendered_pixel_visibility", "desktop_mobile", "keyboard_accessibility", "reduced_motion", "webgl_failure_fallback", "lighthouse", "marketing_truth", "independent_review", "recovery"),
    "verification": ("scope_binding", "negative_controls", "reproducible_receipt", "isolated_execution"),
    "automation": ("frozen_brief", "scope_binding", "negative_security_tests", "recovery", "independent_review"),
    "marketing": ("source_claim_checks", "nonfabrication", "owner_review", "spend_authorization"),
    "media": ("frozen_brief", "asset_fidelity", "sampled_frames", "mobile", "independent_review", "publication_authorization"),
}

class QualityStandardError(ValueError):
    pass

def verify_coverage(actions: dict) -> dict:
    present = set(actions)
    missing = sorted(present-set(ACTION_PROFILES))
    stale = sorted(set(ACTION_PROFILES)-present)
    return {"policy_version": VERSION, "complete": not missing and not stale,
            "missing": missing, "stale": stale, "mapped_actions": len(ACTION_PROFILES)}

def receipt(project: str, action: str, manifest: str, output: dict) -> dict:
    """Attach conservative, cross-project QA requirements without granting rights."""
    if action not in ACTION_PROFILES:
        raise QualityStandardError("unknown_tool_action_denied")
    if not isinstance(output, dict) or not isinstance(project, str) or not project:
        raise QualityStandardError("invalid_result_or_project")
    if output.get("published") is True or output.get("release_authorized") is True or output.get("design_complete") is True:
        raise QualityStandardError("unverified_release_or_design_claim_denied")
    profile = ACTION_PROFILES[action]
    requirements = REQUIREMENTS[profile]
    report = dict(output)
    # Fail-closed accounting of the result, never pretend tests or human review ran.
    current_gate = output.get("quality_gate") if isinstance(output.get("quality_gate"), dict) else {}
    report["universal_quality_standard"] = {
        "version": VERSION, "project": project, "action": action,
        "manifest": manifest, "profile": profile,
        "mandatory_checks": list(requirements),
        "quality_contract_status": current_gate.get("status", "not_assessed"),
        "technical_execution_only": True,
        "independent_human_accepted": False,
        "production_release_authorized": False,
        "score_10_of_10_certified": False,
        "evidence_standard": "sha_pinned_and_independently_reviewed",
        "cross_tool_yard_applicability": True,
    }
    return report

def inspect_quality_receipt(path: Path, expected_project: str, required_checks: tuple[str,...]) -> dict:
    """Machine-check evidence inventory; never self-certify human acceptance."""
    path=Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 250000:
        raise QualityStandardError("unsafe_or_missing_evidence_receipt")
    data=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data,dict) or data.get("project") != expected_project:
        raise QualityStandardError("foreign_project_evidence_denied")
    events=data.get("checks")
    if not isinstance(events,list):
        raise QualityStandardError("invalid_evidence_events")
    by_id={}
    for event in events:
        if not isinstance(event,dict) or set(event)!={"id","status","artifact_sha256","method"}:
            raise QualityStandardError("invalid_evidence_event")
        key=event["id"]
        if not isinstance(key,str) or key in by_id:
            raise QualityStandardError("duplicate_evidence_event")
        by_id[key]=event
    missing=[]
    for key in required_checks:
        e=by_id.get(key)
        if (not e or e["status"]!="passed" or e["method"] not in ("automated","manual_observed")
            or not isinstance(e["artifact_sha256"],str) or len(e["artifact_sha256"])!=64
            or any(ch not in "0123456789abcdef" for ch in e["artifact_sha256"])):
            missing.append(key)
    return {"project": expected_project, "required": len(required_checks),
            "reported_passing": len(required_checks)-len(missing),
            "missing": missing, "status": "technical_evidence_reported" if not missing else "evidence_incomplete",
            "independent_human_accepted": False, "release_authorized": False}
