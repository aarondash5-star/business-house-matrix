"""Immutable RC1 independent Python two-file benchmark tests.

Absent generated sources in ordinary source checkout -> skip; in the enrolled
capsule both files must exist and all assertions run against model output.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
READY = all((ROOT / path).is_file() for path in
            ("benchmarks/gate_e/money.py","benchmarks/gate_e/invoice.py"))

@unittest.skipUnless(READY,"model-created benchmark files absent in Git checkout")
class InvoiceModelBenchmark(unittest.TestCase):
    def test_zero_and_integer(self):
        from benchmarks.gate_e.money import parse_cents
        self.assertEqual(parse_cents("0"),0)
        self.assertEqual(parse_cents("12"),1200)
        self.assertEqual(parse_cents("$4"),400)

    def test_decimal_padding(self):
        from benchmarks.gate_e.money import parse_cents
        self.assertEqual(parse_cents("3.1"),310)
        self.assertEqual(parse_cents("$2.35"),235)
        self.assertEqual(parse_cents("0.01"),1)

    def test_validation_fail_closed(self):
        from benchmarks.gate_e.money import parse_cents
        for invalid in ["-1"," 1","1 ","1.234","1.","","$","1e2","a",None,12]:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    parse_cents(invalid)

    def test_empty_and_sum(self):
        from benchmarks.gate_e.invoice import invoice_total
        self.assertEqual(invoice_total([]),0)
        self.assertEqual(invoice_total(["$1.50","2","0.5"]),400)

    def test_repeated_and_large_numbers(self):
        from benchmarks.gate_e.invoice import invoice_total
        self.assertEqual(invoice_total(["100","100","0.01"]),20001)

    def test_invalid_invoice_inputs(self):
        from benchmarks.gate_e.invoice import invoice_total
        for invalid in [None,"12",12,{"x":"3"}]:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    invoice_total(invalid)
        with self.assertRaises(ValueError):
            invoice_total(["1.00","wrong"])

if __name__=="__main__":
    unittest.main()
