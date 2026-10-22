"""Pure offline policy tests for the fixed-loopback RC1 structured proposer."""
from pathlib import Path
import sys
import json
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import gate_e_rc1_ollama as model

class ModelTransportPolicy(unittest.TestCase):
    def test_fixed_loopback_and_model_caps(self):
        obj=model.request_payload("Build an enrolled public benchmark")
        self.assertEqual(model.URL,"http://127.0.0.1:11434/api/generate")
        self.assertFalse(obj["stream"])
        self.assertEqual(obj["model"],"granite4:3b")
        self.assertLessEqual(obj["options"]["num_predict"],750)
        self.assertEqual(obj["keep_alive"],"0")

    def test_large_untrusted_prompt_denied(self):
        with self.assertRaises(ValueError):
            model.request_payload("x"*23000)

    def test_redirect_denied(self):
        self.assertIsNone(model.NoRedirect().redirect_request(
            None,None,302,"move",{},"https://example.net/"))

    def test_schema_limits_and_no_unknown_fields(self):
        schema=model.request_payload("Return two enrolled files")["format"]
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["files"]["maxItems"],8)
        self.assertFalse(schema["properties"]["files"]["items"]["additionalProperties"])

if __name__=="__main__":unittest.main()
