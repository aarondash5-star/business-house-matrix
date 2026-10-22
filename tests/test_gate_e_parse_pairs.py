import unittest
from benchmarks.gate_e.parse_pairs import parse_pairs

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
