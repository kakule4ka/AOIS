import unittest
import io
import sys
from src.bit_array import BitArray
from src.formatters import ResultFormatter

class TestResultFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = ResultFormatter()
        self.arr = BitArray()
        self.arr.bits[31] = 1

    def test_print_binary(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.formatter.print_binary(self.arr)
        sys.stdout = sys.__stdout__
        expected_full = "00000000000000000000000000000001"
        self.assertIn(f"01 ({expected_full})", captured_output.getvalue())