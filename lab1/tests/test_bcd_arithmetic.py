import unittest
from src.bcd_arithmetic import Excess3BCDArithmetic

class TestExcess3BCDArithmetic(unittest.TestCase):
    def setUp(self):
        self.arithmetic = Excess3BCDArithmetic()

    def test_add(self):
        a = self.arithmetic.decimal_to_excess3(48)
        b = self.arithmetic.decimal_to_excess3(71)
        res = self.arithmetic.add(a, b)
        val = self.arithmetic.excess3_to_decimal(res)
        self.assertEqual(val, 119)

    def test_conversion(self):
        res = self.arithmetic.decimal_to_excess3(905)
        val = self.arithmetic.excess3_to_decimal(res)
        self.assertEqual(val, 905)