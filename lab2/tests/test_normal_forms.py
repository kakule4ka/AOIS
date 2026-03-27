import unittest
from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable
from src.normal_forms import NormalForms

EXPR_XOR = "a ~ b"
EXPR_TRUE = "a | !a"
EXPR_FALSE = "a & !a"
EXPECTED_SDNF = "(!a&!b) | (a&b)"
EXPECTED_SKNF = "(a|!b) & (!a|b)"
EXPECTED_SDNF_NUMBERS = [0, 3]
EXPECTED_SKNF_NUMBERS = [1, 2]
RESULT_ZERO = "0"
RESULT_ONE = "1"

class TestNormalForms(unittest.TestCase):
    def setUp(self):
        parser = ExpressionParser()
        evaluator = parser.parse(EXPR_XOR)
        table = TruthTable(evaluator)
        self.nf = NormalForms(table)

    def test_get_sdnf_string(self):
        self.assertEqual(self.nf.get_sdnf(), EXPECTED_SDNF)

    def test_get_sknf_string(self):
        self.assertEqual(self.nf.get_sknf(), EXPECTED_SKNF)

    def test_get_sdnf_numeric_format(self):
        self.assertEqual(self.nf.get_sdnf_numeric(), EXPECTED_SDNF_NUMBERS)

    def test_get_sknf_numeric_format(self):
        self.assertEqual(self.nf.get_sknf_numeric(), EXPECTED_SKNF_NUMBERS)

    def test_sdnf_empty(self):
        parser = ExpressionParser()
        table = TruthTable(parser.parse(EXPR_FALSE))
        nf = NormalForms(table)
        self.assertEqual(nf.get_sdnf(), RESULT_ZERO)

    def test_sknf_empty(self):
        parser = ExpressionParser()
        table = TruthTable(parser.parse(EXPR_TRUE))
        nf = NormalForms(table)
        self.assertEqual(nf.get_sknf(), RESULT_ONE)

if __name__ == '__main__':
    unittest.main()