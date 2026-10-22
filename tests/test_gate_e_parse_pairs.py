import unittest
from pathlib import Path

# This repository deliberately does not commit a generated solution.
# When the Gate E workcell seeds its immutable pinned tests AND the proposed
# source file, the same six assertions execute normally; no skip is possible.
_has_generated_source = (Path(__file__).resolve().parents[1] /
                         "benchmarks/gate_e/parse_pairs.py").is_file()
if _has_generated_source:
    from benchmarks.gate_e.parse_pairs import parse_pairs
else:
    parse_pairs = None

@unittest.skipUnless(_has_generated_source, "Offline model output is evaluated inside the enrolled workcell, not in the CI checkout")
class ParsePairsIndependentTests(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(parse_pairs("name=Arambol\ncount=10"), {"name":"Arambol","count":"10"})
    def test_comments_blank_and_whitespace(self):
        self.assertEqual(parse_pairs(" # skip\n\n city = Goa  \n"), {"city":"Goa"})
    def test_first_equals_and_duplicates(self):
        self.assertEqual(parse_pairs("token=a=b\ntoken=x=y"), {"token":"x=y"})
    def test_empty(self):
        self.assertEqual(parse_pairs(""), {})
    def test_missing_separator(self):
        with self.assertRaises(ValueError):parse_pairs("broken line")
    def test_empty_key(self):
        with self.assertRaises(ValueError):parse_pairs("   =value")
