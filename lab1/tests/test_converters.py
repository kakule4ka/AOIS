import unittest
from src.converters import NumberConverter

class TestNumberConverter(unittest.TestCase):
    def setUp(self):
        self.converter = NumberConverter()

    def test_direct_conversion(self):
        b1 = self.converter.decimal_to_direct(42)
        b2 = self.converter.decimal_to_direct(-73)
        self.assertEqual(self.converter.direct_to_decimal(b1), 42)
        self.assertEqual(self.converter.direct_to_decimal(b2), -73)

    def test_additional_conversion(self):
        b1 = self.converter.decimal_to_additional(115)
        b2 = self.converter.decimal_to_additional(-89)
        self.assertEqual(self.converter.additional_to_decimal(b1), 115)
        self.assertEqual(self.converter.additional_to_decimal(b2), -89)

    def test_additional_conversion_edge_cases(self):
        b_min = self.converter.decimal_to_additional(-2147483648)
        self.assertEqual(self.converter.additional_to_decimal(b_min), -2147483648)

    def test_fixed_conversion(self):
        b1 = self.converter.decimal_to_fixed(13.625)
        b2 = self.converter.decimal_to_fixed(-5.125)
        self.assertEqual(self.converter.fixed_to_decimal(b1), 13.625)
        self.assertEqual(self.converter.fixed_to_decimal(b2), -5.125)

if __name__ == '__main__':
    unittest.main()