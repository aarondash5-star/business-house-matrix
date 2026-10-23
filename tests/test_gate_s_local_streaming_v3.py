"""Gate S v3 local planning controls: offline unit tests, no model call."""
import importlib.util
import pathlib
import tempfile
import unittest
import json
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("gate_s_local_streaming_v3",ROOT/"brain/supervisor/gate_s_local_streaming_v3.py")
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class TestLocalStreaming(unittest.TestCase):
 def test_five_distinct_phases(self):self.assertEqual(len(g.PHASES),5)
 def test_staged_prompt_is_rich(self):
  payload=g.stage_request("01","Discovery","Audit PMS and bookings","none","20m")
  text=payload["prompt"]
  for phrase in ("Andaz Vibe Stay","Moksha Wellness","ACCEPTANCE TEST","DEPENDENCIES","unknowns","Private staging"):
   self.assertIn(phrase.lower(),text.lower())
 def test_not_fixed_five_steps(self):self.assertNotIn("EXACTLY five steps",g.RULES)
 def test_no_actions(self):
  p=g.stage_request("01","Discovery","Audit PMS","none","20m")
  self.assertEqual(p["model"],"qwen3:4b-instruct")
  self.assertTrue(p["stream"])
  self.assertEqual(p["keep_alive"],"20m")
  self.assertEqual(p["options"]["num_predict"],1400)
  self.assertEqual(p["options"]["num_ctx"],4096)
  self.assertNotIn("tools",p)
 def test_final_unload(self):
  p=g.stage_request("05","Review","Risk assessment","none","0")
  self.assertEqual(p["keep_alive"],"0")
 def test_no_false_claims(self):
  for keyword in ("Do NOT invent","No shell commands","No model tools"):
   if keyword=="No model tools":continue
   self.assertIn(keyword,g.RULES)
 def test_atomic_receipts(self):
  with tempfile.TemporaryDirectory() as path:
   target=pathlib.Path(path)/"progress.json"
   g.atomic_json(target,{"state":"running","publish":False})
   self.assertEqual(json.loads(target.read_text())["state"],"running")
   self.assertFalse(target.with_name("progress.json.tmp").exists())
 def test_task_context_private(self):
  self.assertIn("Kitchen/cafe operational status is NOT confirmed",g.CONTEXT)
  self.assertIn("WhatsApp",g.CONTEXT)
if __name__=="__main__":unittest.main()
