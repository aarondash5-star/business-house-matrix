"""Tool-free, network-free unit tests for the self-contained governed pilot."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"strict_content_agent_v3.py"
spec=importlib.util.spec_from_file_location("strict_content_v3",SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
GOOD='<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width"></head><body><main><h1>Pine Chat</h1><p>Sample chat transcript and message here.</p></main></body></html>'

class PilotTest(unittest.TestCase):
    def test_valid_proposal_scoped_review_only(self):
        result=mod.payload(GOOD)
        self.assertEqual(result["status"],"needs_independent_review")
        self.assertEqual(set(v["path"] for v in result["payload"]["files"]),{mod.APP,mod.TEST})
        self.assertFalse(result["executed"])
        self.assertFalse(result["approved"])

    def test_repair_missing_main(self):
        html=GOOD.replace("<main>","").replace("</main>","")
        result=mod.payload(html)
        contents=next(v["content"] for v in result["payload"]["files"] if v["path"]==mod.APP)
        self.assertIn("<main>",contents)

    def test_missing_main_without_body_denied(self):
        with self.assertRaises(ValueError):
            mod.payload(GOOD.replace("<body>","").replace("</body>","").replace("<main>","").replace("</main>",""))

    def test_deny_network_scripts_secrets_and_events(self):
        for value in ("<script>alert(1)</script>","https://example.com","api_key","onerror=alert(1)","javascript:alert(1)","<iframe>"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    mod.payload(GOOD.replace("</main>",value+"</main>"))

    def test_deny_incomplete_output(self):
        with self.assertRaises(ValueError):
            mod.unpack('{"file":"arbitrary path"}')
        with self.assertRaises(ValueError):
            mod.unpack("not json")

    def test_deny_extra_model_schema(self):
        with self.assertRaises(ValueError):
            mod.unpack('{"html":"x","shell":"rm -rf /"}')

    def test_bounded_source_and_one_manifest(self):
        self.assertEqual(mod.MAX_ATTEMPTS,2)
        self.assertEqual(mod.TASK,"pine_chat_b1_synthetic_review_v1")
        self.assertEqual(mod.PROJECT,"pine_mcp_chat")
        with self.assertRaises(ValueError):mod.repair_known_markup("x"*7000)

if __name__=="__main__":unittest.main()
