"""Source-contract regression for owner-scoped Pine beta MCP.

Static only: these checks do not authenticate to Supabase, invoke tools,
compile Pine, or certify the ChatGPT App's registered tool list.
"""
import re
from pathlib import Path

SOURCE = (Path(__file__).resolve().parents[1] /
          "services/pine-chat-mvp-mcp/index.ts").read_text(encoding="utf-8")
EXPECTED = [
    "pine_chat_workspace_info",
    "pine_chat_workflow",
    "pine_chat_preview_info",
    "pine_beta_feature_catalog",
    "pine_beta_native_request",
    "pine_beta_job_status",
    "pine_beta_submit_feedback",
    "pine_beta_paper_order",
    "pine_beta_preview_event",
    "pine_beta_recent_receipts",
]


def test_ten_tool_schema_is_explicit_and_stable():
    registered = re.findall(r'server\.registerTool\("([^"]+)"', SOURCE)
    assert registered == EXPECTED
    assert 'version:"0.2.0"' in SOURCE
    assert "tools:10" in SOURCE


def test_authentication_and_owner_scoping_remain_required():
    assert "const membership=await authorizedOwner(req);" in SOURCE
    assert 'return json({error:"not_enrolled_for_pine_chat"},403);' in SOURCE
    assert '.eq("role","owner").eq("enabled",true)' in SOURCE
    assert SOURCE.count('.eq("owner_id",ownerId)') >= 3
    assert "SUPABASE_SERVICE_ROLE_KEY" in SOURCE


def test_native_jobs_are_only_journaled_pending_enrollment():
    assert 'status:"PENDING_NATIVE_ENROLLMENT"' in SOURCE
    assert "native_executed:false" in SOURCE
    assert "JvxzE0Bg|wHwOPnE1|tUblZ9Ev" in SOURCE
    assert 'idempotency_key_conflict' in SOURCE


def test_paper_and_notification_actions_have_no_live_effect():
    assert 'mode:"PAPER_ONLY"' in SOURCE
    assert "live_broker_order_sent:false" in SOURCE
    assert 'mode:"DRY_RUN"' in SOURCE
    assert "notification_sent:false" in SOURCE
    assert "tradingview_alert_created:false" in SOURCE


def test_no_unrestricted_execution_tool_was_registered():
    assert not any(x in EXPECTED for x in (
        "shell", "ssh_run", "broker_order", "publish_script", "run_python",
        "tradingview_execute", "eval", "arbitrary_http_request"
    ))
