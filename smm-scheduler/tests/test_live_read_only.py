import json
from pathlib import Path
import unittest
from scheduler import validate_jobs
from status_once import check_status


class ReadOnlyProductionTests(unittest.TestCase):
    def test_production_jobs_enabled_and_read_only(self):
        jobs = json.loads((Path(__file__).resolve().parents[1] / "jobs.json").read_text())
        parsed = validate_jobs(jobs)
        self.assertEqual(len(parsed), 2)
        self.assertTrue(all(j["enabled"] for j in parsed))
        self.assertEqual({x["action"] for x in parsed}, {"services", "balance"})

    def test_invalid_order_id_no_network(self):
        class Mock:
            def call(self, action, params):
                raise AssertionError("Unexpected network access")
        self.assertEqual(check_status("abc", Mock())["result"], "blocked")
        self.assertEqual(check_status("123\n", Mock())["result"], "blocked")

    def test_existing_order_status(self):
        class Mock:
            def call(self, action, params):
                assert action == "status"
                assert params == {"order": "23501"}
                return {"status": "Partial", "remains": "157", "charge": "SECRET"}
        self.assertEqual(check_status("23501", Mock()), {
            "result": "passed", "order_status": "Partial", "remaining_quantity": 157})

    def test_provider_error_sanitized(self):
        class Mock:
            def call(self, action, params):
                raise RuntimeError("secret password")
        result = check_status("23501", Mock())
        self.assertEqual(result, {"result": "failed", "reason": "provider_request_failed"})

    def test_untrusted_status_sanitized(self):
        class Mock:
            def call(self, action, params):
                return {"status": "<script>secret</script>"}
        self.assertEqual(check_status("23501", Mock())["order_status"], "Unrecognized")


if __name__ == "__main__":
    unittest.main()
