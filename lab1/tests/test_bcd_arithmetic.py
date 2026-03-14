import unittest
from src.bcd_arithmetic import Excess3BCDArithmetic

class TestBCDArithmetic(unittest.TestCase):
    def setUp(self):
        self.arithmetic = Excess3BCDArithmetic()

    def test_conversions(self):
        b1 = self.arithmetic.decimal_to_excess3(142)
        b2 = self.arithmetic.decimal_to_excess3(-357)
        self.assertEqual(self.arithmetic.excess3_to_decimal(b1), 142)
        self.assertEqual(self.arithmetic.excess3_to_decimal(b2), -357)

    def test_add(self):
        a = self.arithmetic.decimal_to_excess3(142)
        b = self.arithmetic.decimal_to_excess3(357)
        res = self.arithmetic.add(a, b)
        self.assertEqual(self.arithmetic.excess3_to_decimal(res), 499)

        a2 = self.arithmetic.decimal_to_excess3(85)
        b2 = self.arithmetic.decimal_to_excess3(27)
        res2 = self.arithmetic.add(a2, b2)
        self.assertEqual(self.arithmetic.excess3_to_decimal(res2), 112)
