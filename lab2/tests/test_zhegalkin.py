# test_zhegalkin.py
import unittest
from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable
from src.zhegalkin import ZhegalkinPolynomial

class TestZhegalkinPolynomial(unittest.TestCase):
    def test_get_polynomial_string(self):
        table = TruthTable(ExpressionParser().parse("a & b"))
        zh = ZhegalkinPolynomial(table.get_index_form(), table.variables)
        self.assertEqual(zh.get_polynomial(), "ab")

    def test_get_polynomial_zero(self):
        table = TruthTable(ExpressionParser().parse("a & !a"))
        zh = ZhegalkinPolynomial(table.get_index_form(), table.variables)
        self.assertEqual(zh.get_polynomial(), "0")

    def test_is_linear_false(self):
        table = TruthTable(ExpressionParser().parse("a & b"))
        zh = ZhegalkinPolynomial(table.get_index_form(), table.variables)
        self.assertFalse(zh.is_linear())

if __name__ == '__main__':
    unittest.main()