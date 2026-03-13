import unittest
from src.float_arithmetic import IEEE754Arithmetic

class TestIEEE754Arithmetic(unittest.TestCase):
    def setUp(self):
        self.arithmetic = IEEE754Arithmetic()

    def test_add(self):
        a = self.arithmetic.float_to_bits(5.75)
        b = self.arithmetic.float_to_bits(-3.25)
        res = self.arithmetic.add(a, b)
        val = self.arithmetic.bits_to_float(res)
        self.assertEqual(val, 2.5)

    def test_subtract(self):
        a = self.arithmetic.float_to_bits(14.125)
        b = self.arithmetic.float_to_bits(6.5)
        res = self.arithmetic.subtract(a, b)
        val = self.arithmetic.bits_to_float(res)
        self.assertEqual(val, 7.625)

    def test_multiply(self):
        a = self.arithmetic.float_to_bits(2.5)
        b = self.arithmetic.float_to_bits(-4.0)
        res = self.arithmetic.multiply(a, b)
        val = self.arithmetic.bits_to_float(res)
        self.assertEqual(val, -10.0)

    def test_divide(self):
        a = self.arithmetic.float_to_bits(15.5)
        b = self.arithmetic.float_to_bits(2.0)
        res = self.arithmetic.divide(a, b)
        val = self.arithmetic.bits_to_float(res)
        self.assertEqual(val, 7.75)