import unittest
from src.converters import NumberConverter
from src.integer_arithmetic import IntegerArithmetic

class TestIntegerArithmetic(unittest.TestCase):
    def setUp(self):
        self.converter = NumberConverter()
        self.arithmetic = IntegerArithmetic()

    def test_add_additional(self):
        a = self.converter.decimal_to_additional(45)
        b = self.converter.decimal_to_additional(-12)
        res = self.arithmetic.add_additional(a, b)
        self.assertEqual(self.converter.additional_to_decimal(res), 33)

    def test_subtract_additional(self):
        a = self.converter.decimal_to_additional(88)
        b = self.converter.decimal_to_additional(33)
        res = self.arithmetic.subtract_additional(a, b)
        self.assertEqual(self.converter.additional_to_decimal(res), 55)

    def test_multiply_direct(self):
        a = self.converter.decimal_to_direct(11)
        b = self.converter.decimal_to_direct(-7)
        res = self.arithmetic.multiply_direct(a, b)
        self.assertEqual(self.converter.direct_to_decimal(res), -77)

    def test_divide_fixed(self):
        a = self.converter.decimal_to_fixed(22.5)
        b = self.converter.decimal_to_fixed(1.5)
        res = self.arithmetic.divide_fixed(a, b)
        self.assertEqual(self.converter.fixed_to_decimal(res), 15.0)

        a2 = self.converter.decimal_to_fixed(-35.0)
        b2 = self.converter.decimal_to_fixed(8.0)
        res2 = self.arithmetic.divide_fixed(a2, b2)
        self.assertEqual(self.converter.fixed_to_decimal(res2), -4.375)
