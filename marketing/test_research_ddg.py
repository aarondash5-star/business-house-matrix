#!/usr/bin/env python3
"""DuckDuckGo zero-CAPTCHA-bypass provider-switch regression tests."""
import io,json,unittest
from unittest import mock
import research_ddg as m

class DDGTests(unittest.TestCase):
    def test_sensitive_queries_denied(self):
        for q in ("password 123","bob@example.com","x","api key secret"):
            with self.assertRaises(ValueError):m.check_query(q)
    def test_result_engine_strict(self):
        r=m.interpret({"results":[
            {"url":"https://thehiddenoak.space/","title":"Hidden Oak","engine":"duckduckgo"},
            {"url":"https://attacker.test/","engine":"google cse"}
        ]},"Arambol wellness")
        self.assertEqual(len(r["results"]),1)
        self.assertEqual(r["results"][0]["engine"],"duckduckgo")
        self.assertFalse(r["results"][0]["facts_verified"])
    def test_captcha_fail_closed(self):
        r=m.interpret({"results":[],"unresponsive_engines":[["duckduckgo","CAPTCHA"]]},"Goa sauna")
        self.assertEqual(r["status"],"blocked_captcha")
    @mock.patch.object(m,"opera_fallback")
    @mock.patch.object(m,"urlopen")
    def test_opera_called_once_only_if_captcha(self,opener,fallback):
        class Resp:
            def __enter__(self):return self
            def __exit__(self,*args):return False
            def read(self,limit=0):
                return json.dumps({"results":[],"unresponsive_engines":[["duckduckgo","CAPTCHA"]]}).encode()
        opener.return_value=Resp()
        fallback.return_value={"provider":"duckduckgo_via_isolated_opera","status":"observed",
                               "results":[],"fallback_used":True}
        r=m.search("Hidden Oak sauna")
        fallback.assert_called_once_with("Hidden Oak sauna")
        self.assertEqual(r["primary_status"],"blocked_captcha")
        self.assertTrue(r["fallback_used"])
    @mock.patch.object(m,"opera_fallback")
    @mock.patch.object(m,"urlopen")
    def test_no_fallback_for_successful_searxng_ddg(self,opener,fallback):
        class Resp:
            def __enter__(self):return self
            def __exit__(self,*args):return False
            def read(self,limit=0):
                return json.dumps({"results":[{"engine":"duckduckgo","url":"https://thehiddenoak.space/","title":"Hidden Oak"}]}).encode()
        opener.return_value=Resp()
        r=m.search("Hidden Oak sauna")
        self.assertEqual(r["status"],"observed")
        fallback.assert_not_called()
    def test_opera_adapter_invalid_response_fails_closed(self):
        with mock.patch.object(m.subprocess,"run") as run:
            run.return_value=mock.Mock(stdout='{"provider":"duckduckgo_via_isolated_opera","status":"observed","existing_session_touched":true,"results":[]}')
            r=m.opera_fallback("Hidden Oak sauna")
        self.assertEqual(r["status"],"unavailable")

if __name__=="__main__":unittest.main()
