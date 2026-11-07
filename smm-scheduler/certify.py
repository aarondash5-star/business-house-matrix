"""One-shot FanSMM read-only connectivity certification. Never logs credentials or balances."""
from __future__ import annotations
import datetime as dt
import json
import os
import sys
from decimal import Decimal, InvalidOperation
from providers.fansmm import FanSMM


def certify(api=None, key=None):
    key = os.environ.get("FANSMM_API_KEY") if key is None else key
    if not key:
        return {"result": "blocked", "reason": "FANSMM_API_KEY_missing"}
    try:
        client = api if api is not None else FanSMM(key)
        services = client.call("services")
        if not isinstance(services, list):
            return {"result": "failed", "reason": "services_invalid_shape"}
        balance = client.call("balance")
        if not isinstance(balance, dict) or "currency" not in balance or "balance" not in balance:
            return {"result": "failed", "reason": "balance_invalid_shape"}
        try:
            value = Decimal(str(balance["balance"]))
            if not value.is_finite() or value < 0:
                raise InvalidOperation()
        except (InvalidOperation, ValueError):
            return {"result": "failed", "reason": "balance_invalid_number"}
        if not isinstance(balance["currency"], str) or len(balance["currency"]) != 3:
            return {"result": "failed", "reason": "currency_invalid"}
        return {"result": "passed", "stage": "read_only_api_connectivity", "services_count": len(services)}
    except Exception:
        return {"result": "failed", "reason": "provider_request_failed"}


if __name__ == "__main__":
    result = certify()
    result["checked_at"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    print(json.dumps(result, sort_keys=True))
    sys.exit(0 if result["result"] == "passed" else 1)
