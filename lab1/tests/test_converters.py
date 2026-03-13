import unittest
from src.converters import NumberConverter

class TestNumberConverter(unittest.TestCase):
    def setUp(self):
        self.converter = NumberConverter()

    def test_decimal_to_direct_positive(self):
        res = self.converter.decimal_to_direct(83)
        self.assertEqual(res.bits[0], 0)
        self.assertEqual(res.bits[31], 1)
        self.assertEqual(res.bits[30], 1)
        self.assertEqual(res.bits[29], 0)
        self.assertEqual(res.bits[28], 0)
        self.assertEqual(res.bits[27], 1)
        self.assertEqual(res.bits[26], 0)
        self.assertEqual(res.bits[25], 1)

    def test_decimal_to_additional_negative(self):
        res = self.converter.decimal_to_additional(-117)
        self.assertEqual(res.bits[0], 1)
        val = self.converter.additional_to_decimal(res)
        self.assertEqual(val, -117)

    def test_additional_to_decimal_positive(self):
        res = self.converter.decimal_to_additional(402)
        val = self.converter.additional_to_decimal(res)
        self.assertEqual(val, 402)