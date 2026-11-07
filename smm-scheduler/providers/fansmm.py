"""FanSMM API v2 read-only adapter. Excludes paid engagement orders."""
import json
import os
import urllib.error
import urllib.parse
import urllib.request


class ProviderError(Exception):
    pass


class FanSMM:
    ENDPOINT = "https://fansmm.in/api/v2"
    ALLOWED = {"services", "balance", "status"}

    def __init__(self, key, transport=None):
        if not key or not isinstance(key, str):
            raise ValueError("Missing FanSMM API key")
        self._key = key
        self._transport = transport or self._post

    @classmethod
    def from_environment(cls):
        return cls(os.environ.get("FANSMM_API_KEY"))

    def _post(self, fields):
        data = urllib.parse.urlencode(fields).encode("utf-8")
        req = urllib.request.Request(
            self.ENDPOINT, data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                if response.status != 200:
                    raise ProviderError("Provider returned a non-200 HTTP status")
                payload = response.read(524289)
        except urllib.error.URLError:
            raise ProviderError("Provider HTTP transport failed") from None
        if len(payload) > 524288:
            raise ProviderError("Provider response exceeds maximum length")
        try:
            return json.loads(payload)
        except (ValueError, UnicodeError):
            raise ProviderError("Invalid provider JSON response") from None

    def call(self, action, params=None):
        params = params or {}
        if action not in self.ALLOWED:
            raise ValueError("Unsupported or billable operation blocked")
        if not isinstance(params, dict):
            raise ValueError("params must be an object")
        fields = {"key": self._key, "action": action}
        if action == "status":
            order = params.get("order")
            if not isinstance(order, (str, int)) or not str(order).isdigit():
                raise ValueError("status requires numeric order")
            if set(params) != {"order"}:
                raise ValueError("status accepts only order")
            fields["order"] = str(order)
        elif params:
            raise ValueError("action does not accept parameters")
        result = self._transport(fields)
        if not isinstance(result, (dict, list)) or (isinstance(result, dict) and "error" in result):
            raise ProviderError("Provider reported an error or unexpected response")
        return result
