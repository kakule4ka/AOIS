import unittest
import io
import sys
from src.bit_array import BitArray
from src.formatters import ResultFormatter

class TestResultFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = ResultFormatter()
        self.b = BitArray()
        self.b.bits[-1] = 1

    def test_print_binary(self):
        captured = io.StringIO()
        sys.stdout = captured
        self.formatter.print_binary(self.b)
        sys.stdout = sys.__stdout__
        self.assertIn("00000000000000000000000000000001", captured.getvalue())

    def test_print_decimal(self):
        captured = io.StringIO()
        sys.stdout = captured
        self.formatter.print_decimal(42.5)
        sys.stdout = sys.__stdout__
        self.assertIn("42.5", captured.getvalue())

    def test_print_both(self):
        captured = io.StringIO()
        sys.stdout = captured
        self.formatter.print_both(self.b, 42.5, "Op")
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        
    
        self.assertIn("--- Op ---", output)
        self.assertIn("00000000000000000000000000000001", output)
        self.assertIn("Decimal: 42.5", output)