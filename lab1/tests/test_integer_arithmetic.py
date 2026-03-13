import unittest
from src.converters import NumberConverter
from src.integer_arithmetic import IntegerArithmetic

class TestIntegerArithmetic(unittest.TestCase):
    def setUp(self):
        self.converter = NumberConverter()
        self.arithmetic = IntegerArithmetic()

    def test_add_additional(self):
        a = self.converter.decimal_to_additional(156)
        b = self.converter.decimal_to_additional(-42)
        res = self.arithmetic.add_additional(a, b)
        val = self.converter.additional_to_decimal(res)
        self.assertEqual(val, 114)

    def test_subtract_additional(self):
        a = self.converter.decimal_to_additional(89)
        b = self.converter.decimal_to_additional(214)
        res = self.arithmetic.subtract_additional(a, b)
        val = self.converter.additional_to_decimal(res)
        self.assertEqual(val, -125)

    def test_multiply_direct(self):
        a = self.converter.decimal_to_direct(13)
        b = self.converter.decimal_to_direct(17)
        res = self.arithmetic.multiply_direct(a, b)
        self.assertEqual(res.bits[0], 0)

    def test_divide_direct(self):
        a = self.converter.decimal_to_direct(1024)
        b = self.converter.decimal_to_direct(7)
        res = self.arithmetic.divide_direct(a, b)
        self.assertEqual(res.bits[0], 0)