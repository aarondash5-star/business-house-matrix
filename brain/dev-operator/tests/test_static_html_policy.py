import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(name):
    p=ROOT/(name+".py")
    spec=importlib.util.spec_from_file_location("dev_"+name,p)
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module

policy=load("static_html_policy")
agent=load("agent_loop")
cell=load("workcell_runner")

GOOD='''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Demo</title><style>body{margin:0;font-family:sans-serif}
@media(max-width:600px){main{padding:12px}}</style></head>
<body><main class="panel"><h1 id="heading">Safe</h1><p aria-label="information">Ready</p></main></body></html>'''

def variant(value):
    return GOOD.replace('<main class="panel">','<main class="panel">'+value,1)

class StaticPolicyTests(unittest.TestCase):
    def test_valid_semantic_css(self):
        self.assertTrue(policy.validate_static_html(GOOD))
    def test_agent_agrees_with_policy(self):
        out=agent.parse_single_html(GOOD,"frontend/test.html")
        self.assertEqual(out["files"][0]["content"],GOOD)
    def test_reject_active_tags(self):
        for code in ('<script>alert(1)</script>','<iframe src="data:text/html,hi"></iframe>',
                     '<object data="data:text/html,hi"></object>',
                     '<embed src="data:text/html,hi">',
                     '<svg><script>bad</script></svg>',
                     '<form><input autofocus></form>',
                     '<a href="javascript:alert(1)">Launch</a>'):
            with self.subTest(code=code),self.assertRaises(policy.StaticHTMLViolation):
                policy.validate_static_html(variant(code))
    def test_reject_active_attribute(self):
        for attack in ('<p onclick="doThing()">click</p>',
                       '<div onpointerenter="doThing()">x</div>',
                       '<p style="background:url(//cdn.test/x)">x</p>',
                       '<p style="width:expression(alert(1))">x</p>'):
            with self.subTest(attack=attack),self.assertRaises(policy.StaticHTMLViolation):
                policy.validate_static_html(variant(attack))
    def test_reject_css_loading(self):
        for css in ('@import "https://cdn.test/x.css";',
                    'body{background:url(//cdn.test/p)}',
                    'body{background:image-set("https://cdn.test/x" 1x)}',
                    'body{behavior:url(foo.htc)}',
                    'body{background:\\75rl(//cdn.test/x)}',
                    '@font-face{src:url("//cdn.test/font")}'):
            with self.subTest(css=css),self.assertRaises(policy.StaticHTMLViolation):
                policy.validate_static_html(GOOD.replace('</style>',css+'</style>'))
    def test_reject_meta_redirect_and_charset(self):
        for meta in ('<meta http-equiv="refresh" content="0;url=javascript:alert(1)">',
                     '<meta name="referrer" content="unsafe-url">',
                     '<meta charset="utf-16">'):
            with self.subTest(meta=meta),self.assertRaises(policy.StaticHTMLViolation):
                policy.validate_static_html(GOOD.replace('</head>',meta+'</head>'))
    def test_reject_incomplete_structure(self):
        for bad in (GOOD.replace('<body>',''),GOOD.replace('</body>',''),
                    GOOD.replace('<main class="panel">','<div>'),
                    GOOD.replace('<head>',''),GOOD.replace('<!doctype html>',''),
                    GOOD.replace('</html>','')):
            with self.subTest(test=bad[-30:]),self.assertRaises(policy.StaticHTMLViolation):
                policy.validate_static_html(bad)
    def test_reject_duplicate_attr_and_comments(self):
        for bad in (GOOD.replace('lang="en"','lang="en" onclick="x"'),
                    GOOD.replace('lang="en"','lang="en" lang="de"'),
                    GOOD.replace('<main class="panel">','<!-- active --> <main class="panel">')):
            with self.subTest(test=bad[:50]),self.assertRaises(policy.StaticHTMLViolation):
                policy.validate_static_html(bad)
    def test_sandbox_rejects_external_active_content(self):
        # Independent QA re-parses content even if a caller skips model validation.
        with tempfile.TemporaryDirectory(prefix="release-hardening-") as root:
            root=Path(root)
            for i,html in enumerate((GOOD,variant('<p onclick="act()">x</p>'),
                                     GOOD.replace('</style>','@import "https://remote/x.css";</style>'))):
                cell.isolated(root,"apply",{"paths":["frontend/demo.html"],
                    "files":[{"path":"frontend/demo.html","content":html}]})
                outcome=cell.isolated(root,"qa",{"paths":["frontend/demo.html"],
                                              "test_profile":"static-html"})
                self.assertEqual(outcome["qa_passed"],i==0)
                self.assertTrue(outcome["tests_executed"])
    def test_sandbox_fails_closed_on_missing_policy(self):
        self.assertTrue(cell.STATIC_POLICY.exists())
        self.assertTrue(cell.doctor(Path(tempfile.mkdtemp(prefix="release-doctor-")))["passed"])

if __name__=="__main__":
    unittest.main()
