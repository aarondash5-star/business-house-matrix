import datetime as dt
import json
import pathlib
import tempfile
import unittest
from scheduler import run_due, validate_jobs, iso, write_json_atomic, load_json
from providers.fansmm import FanSMM, ProviderError

UTC = dt.timezone.utc
T0 = dt.datetime(2026, 11, 7, 5, 0, tzinfo=UTC)


def sample(action="balance", interval=10):
    return {"id": "demo", "provider": "fansmm", "action": action, "interval_minutes": interval, "enabled": True}


class TestScheduler(unittest.TestCase):
    def test_accepts_read_only_jobs(self):
        self.assertEqual(len(validate_jobs({"jobs": [sample()]})), 1)

    def test_rejects_paid_order_action(self):
        item = sample("add")
        with self.assertRaises(ValueError):
            validate_jobs({"jobs": [item]})

    def test_rejects_duplicate_ids(self):
        with self.assertRaises(ValueError):
            validate_jobs({"jobs": [sample(), sample()]})

    def test_rejects_sub_five_minute_interval(self):
        with self.assertRaises(ValueError):
            validate_jobs({"jobs": [sample(interval=1)]})

    def test_due_executes_once(self):
        called = []
        def handler(p, a, x):
            called.append(a)
            return {"balance": "10", "currency": "USD"}
        state, report = run_due([sample()], {"jobs": {}}, handler, T0, dry_run=False)
        self.assertEqual(report[0]["result"], "success")
        self.assertEqual(called, ["balance"])
        state, report = run_due([sample()], state, handler, T0 + dt.timedelta(minutes=9), dry_run=False)
        self.assertEqual(report[0]["result"], "not_due")
        self.assertEqual(len(called), 1)
        _, report = run_due([sample()], state, handler, T0 + dt.timedelta(minutes=10), dry_run=False)
        self.assertEqual(report[0]["result"], "success")
        self.assertEqual(len(called), 2)

    def test_dry_run_has_zero_side_effects(self):
        def fail(*args):
            raise AssertionError("No calls during preview")
        original = {"jobs": {}}
        next_state, report = run_due([sample()], original, fail, T0, dry_run=True)
        self.assertEqual(next_state, original)
        self.assertEqual(report[0]["result"], "dry_run_due")

    def test_disabled_does_not_execute(self):
        j = sample()
        j["enabled"] = False
        _, report = run_due([j], {"jobs": {}}, lambda *a: self.fail("called"), T0, dry_run=False)
        self.assertEqual(report[0]["result"], "disabled")

    def test_error_backoff_and_redaction(self):
        def error(*args):
            raise RuntimeError("secret-token-should-not-appear")
        state, report = run_due([sample()], {"jobs": {}}, error, T0, dry_run=False)
        self.assertEqual(report[0]["error_type"], "RuntimeError")
        self.assertNotIn("secret-token", json.dumps(state) + json.dumps(report))
        self.assertEqual(state["jobs"]["demo"]["next_run_at"], iso(T0 + dt.timedelta(minutes=10)))

    def test_atomic_persistence(self):
        with tempfile.TemporaryDirectory() as directory:
            p = pathlib.Path(directory) / "state.json"
            write_json_atomic(p, {"jobs": {"demo": {"result": "success"}}})
            self.assertEqual(load_json(p, {})["jobs"]["demo"]["result"], "success")

    def test_status_requires_order(self):
        with self.assertRaises(ValueError):
            validate_jobs({"jobs": [sample("status")]})
        j = sample("status")
        j["params"] = {"order": 123}
        self.assertEqual(validate_jobs({"jobs": [j]})[0]["params"]["order"], 123)


class TestProvider(unittest.TestCase):
    def test_balance_and_service_mapping(self):
        calls = []
        api = FanSMM("synthetic-key", transport=lambda fields: calls.append(fields) or {"balance": "12"})
        self.assertEqual(api.call("balance")["balance"], "12")
        self.assertEqual(calls[0]["action"], "balance")

    def test_billable_operation_blocked_before_network(self):
        api = FanSMM("synthetic-key", transport=lambda fields: self.fail("network"))
        with self.assertRaises(ValueError):
            api.call("add", {"service": 1, "quantity": 50})

    def test_status_payload(self):
        calls = []
        api = FanSMM("synthetic-key", transport=lambda fields: calls.append(fields) or {"status": "Completed"})
        result = api.call("status", {"order": "23501"})
        self.assertEqual(result["status"], "Completed")
        self.assertEqual(calls[0]["order"], "23501")

    def test_provider_error_is_redacted(self):
        api = FanSMM("synthetic-key", transport=lambda fields: {"error": "secret"})
        with self.assertRaisesRegex(ProviderError, "Provider reported an error"):
            api.call("services")


if __name__ == "__main__":
    unittest.main()
