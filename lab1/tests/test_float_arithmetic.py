import unittest
from src.float_arithmetic import IEEE754Arithmetic
from src.bit_array import BitArray

class TestFloatArithmetic(unittest.TestCase):
    def setUp(self):
        self.arithmetic = IEEE754Arithmetic()

    def test_edge_cases_conversions(self):
        z_bits = self.arithmetic.float_to_bits(0.0)
        self.assertEqual(sum(z_bits.bits), 0)
        self.assertEqual(self.arithmetic.bits_to_float(z_bits), 0.0)
        
        frac_bits = self.arithmetic.float_to_bits(0.125)
        self.assertEqual(self.arithmetic.bits_to_float(frac_bits), 0.125)
        
        empty_bits = BitArray()
        self.assertEqual(self.arithmetic.bits_to_float(empty_bits), 0.0)

    def test_add(self):
        a = self.arithmetic.float_to_bits(1.5)
        b = self.arithmetic.float_to_bits(1.5)
        res1 = self.arithmetic.add(a, b)
        self.assertEqual(self.arithmetic.bits_to_float(res1), 3.0)

        z = self.arithmetic.float_to_bits(0.0)
        res2 = self.arithmetic.add(a, z)
        self.assertEqual(self.arithmetic.bits_to_float(res2), 1.5)

        res3 = self.arithmetic.add(z, a)
        self.assertEqual(self.arithmetic.bits_to_float(res3), 1.5)

    def test_subtract(self):
        a = self.arithmetic.float_to_bits(10.5)
        b = self.arithmetic.float_to_bits(10.5)
        res1 = self.arithmetic.subtract(a, b)
        self.assertEqual(self.arithmetic.bits_to_float(res1), 0.0)

        c = self.arithmetic.float_to_bits(5.0)
        d = self.arithmetic.float_to_bits(15.0)
        res2 = self.arithmetic.subtract(c, d)
        self.assertEqual(self.arithmetic.bits_to_float(res2), -10.0)

    def test_multiply(self):
        a = self.arithmetic.float_to_bits(3.0)
        b = self.arithmetic.float_to_bits(1.5)
        res1 = self.arithmetic.multiply(a, b)
        self.assertEqual(self.arithmetic.bits_to_float(res1), 4.5)

        z = self.arithmetic.float_to_bits(0.0)
        res2 = self.arithmetic.multiply(a, z)
        self.assertEqual(self.arithmetic.bits_to_float(res2), 0.0)

        res3 = self.arithmetic.multiply(z, a)
        self.assertEqual(self.arithmetic.bits_to_float(res3), 0.0)

    def test_divide(self):
        a = self.arithmetic.float_to_bits(15.0)
        b = self.arithmetic.float_to_bits(3.0)
        res1 = self.arithmetic.divide(a, b)
        self.assertEqual(self.arithmetic.bits_to_float(res1), 5.0)

        z = self.arithmetic.float_to_bits(0.0)
        res2 = self.arithmetic.divide(z, a)
        self.assertEqual(self.arithmetic.bits_to_float(res2), 0.0)

        res3 = self.arithmetic.divide(a, z)
        self.assertEqual(sum(res3.bits), 0)
