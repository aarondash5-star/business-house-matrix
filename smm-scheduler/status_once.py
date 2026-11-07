"""Read-only status lookup for a previously authorized FanSMM order."""
from __future__ import annotations
import argparse
import json
import re
import sys
from providers.fansmm import FanSMM

ORDER_ID = re.compile(r"^[0-9]{1,20}$")
KNOWN_STATES = {
    "Pending", "In progress", "Processing", "Partial", "Completed",
    "Canceled", "Cancelled", "Refunded", "Failed"
}


def check_status(order_id: str, client=None):
    if not isinstance(order_id, str) or not ORDER_ID.fullmatch(order_id):
        return {"result": "blocked", "reason": "invalid_existing_order_id"}
    try:
        api = client if client is not None else FanSMM.from_environment()
        response = api.call("status", {"order": order_id})
        if not isinstance(response, dict) or not isinstance(response.get("status"), str):
            return {"result": "failed", "reason": "invalid_provider_response"}
        state = response["status"].strip()
        safe_state = state if state in KNOWN_STATES else "Unrecognized"
        result = {"result": "passed", "order_status": safe_state}
        remains = response.get("remains")
        if remains is not None and str(remains).isdigit():
            result["remaining_quantity"] = int(remains)
        return result
    except Exception:
        return {"result": "failed", "reason": "provider_request_failed"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", required=True, help="Existing order ID. No new orders created.")
    args = parser.parse_args()
    result = check_status(args.order)
    print(json.dumps(result, sort_keys=True))
    sys.exit(0 if result["result"] == "passed" else 1)
