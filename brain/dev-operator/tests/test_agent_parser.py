import importlib.util
from pathlib import Path
import sys
import unittest

p=Path(__file__).resolve().parents[1]/"agent_loop.py"
spec=importlib.util.spec_from_file_location("dev_agent_loop",p)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)

GOOD='<!doctype html><html lang="en"><head><meta name="viewport" content="width=device-width"></head><body><main>Demo</main></body></html>'
class AgentParserTests(unittest.TestCase):
    def test_raw_html_to_scoped_source(self):
        d=m.parse_single_html(GOOD,"frontend/sample.html")
        self.assertEqual(d["files"][0]["path"],"frontend/sample.html")
        self.assertEqual(d["files"][0]["content"],GOOD)
    def test_mixed_preamble_exact_extract(self):
        d=m.parse_single_html("Here is the UI: "+GOOD+" End.","frontend/sample.html")
        self.assertEqual(d["files"][0]["content"],GOOD)
    def test_legacy_json_html_wrapper(self):
        import json
        d=m.parse_single_html(json.dumps({"html":GOOD}),"frontend/sample.html")
        self.assertEqual(d["files"][0]["content"],GOOD)
    def test_legacy_files_wrapper_ignores_untrusted_path(self):
        import json
        x=json.dumps({"files":[{"path":"other/foreign.html","content":GOOD}]})
        d=m.parse_single_html(x,"frontend/sample.html")
        self.assertEqual(d["files"][0]["path"],"frontend/sample.html")
    def test_reject_non_html(self):
        with self.assertRaises(ValueError):m.parse_single_html('{"files":[]}',"frontend/sample.html")
    def test_reject_model_suggested_wrong_file_type(self):
        with self.assertRaises(ValueError):m.parse_single_html(GOOD,"src/main.py")
    def test_reject_script_network(self):
        for injected in ("<script>console.log(1)</script>","https://external.example","<iframe></iframe>"):
            with self.subTest(injected=injected),self.assertRaises(ValueError):
                m.parse_single_html(GOOD.replace("</main>",injected+"</main>"),"frontend/sample.html")

if __name__=="__main__":unittest.main()
