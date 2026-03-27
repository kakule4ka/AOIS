import unittest
from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable
from src.zhegalkin import ZhegalkinPolynomial

EXPR_AND = "a & b"
EXPR_FALSE = "a & !a"
EXPECTED_POLYNOMIAL = "ab"
RESULT_ZERO = "0"

class TestZhegalkinPolynomial(unittest.TestCase):
    def test_get_polynomial_string(self):
        table = TruthTable(ExpressionParser().parse(EXPR_AND))
        zh = ZhegalkinPolynomial(table.results, table.variables)
        self.assertEqual(zh.get_polynomial(), EXPECTED_POLYNOMIAL)

    def test_get_polynomial_zero(self):
        table = TruthTable(ExpressionParser().parse(EXPR_FALSE))
        zh = ZhegalkinPolynomial(table.results, table.variables)
        self.assertEqual(zh.get_polynomial(), RESULT_ZERO)

    def test_is_linear_false(self):
        table = TruthTable(ExpressionParser().parse(EXPR_AND))
        zh = ZhegalkinPolynomial(table.results, table.variables)
        self.assertFalse(zh.is_linear())

if __name__ == '__main__':
    unittest.main()