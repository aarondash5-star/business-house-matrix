import unittest
from certify import certify


class MockFanSMM:
    def __init__(self, services=None, balance=None, raises=False):
        self.calls = []
        self.services = services if services is not None else [{"service": 1, "min": "10", "max": "100"}]
        self.balance = balance if balance is not None else {"balance": "24.50", "currency": "USD"}
        self.raises = raises

    def call(self, action):
        self.calls.append(action)
        if self.raises:
            raise RuntimeError("a sensitive test secret")
        if action == "services":
            return self.services
        if action == "balance":
            return self.balance
        raise AssertionError("unexpected operation")


class TestCertification(unittest.TestCase):
    def test_no_key_blocks_without_calls(self):
        api = MockFanSMM()
        self.assertEqual(certify(api=api, key="")["reason"], "FANSMM_API_KEY_missing")
        self.assertEqual(api.calls, [])

    def test_valid_connectivity(self):
        api = MockFanSMM()
        self.assertEqual(certify(api=api, key="fake")["result"], "passed")
        self.assertEqual(api.calls, ["services", "balance"])

    def test_invalid_balance(self):
        api = MockFanSMM(balance={"balance": "-2", "currency": "USD"})
        self.assertEqual(certify(api=api, key="fake")["reason"], "balance_invalid_number")

    def test_invalid_services(self):
        api = MockFanSMM(services={"items": []})
        self.assertEqual(certify(api=api, key="fake")["reason"], "services_invalid_shape")

    def test_safe_error_reporting(self):
        api = MockFanSMM(raises=True)
        self.assertEqual(certify(api=api, key="fake"), {"result": "failed", "reason": "provider_request_failed"})


if __name__ == "__main__":
    unittest.main()
