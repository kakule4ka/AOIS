# test_normal_forms.py
import unittest
from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable
from src.normal_forms import NormalForms

class TestNormalForms(unittest.TestCase):
    def setUp(self):
        parser = ExpressionParser()
        evaluator = parser.parse("a ~ b")
        table = TruthTable(evaluator)
        self.nf = NormalForms(table)

    def test_get_sdnf_string(self):
        self.assertEqual(self.nf.get_sdnf(), "(!a & !b) | (a & b)")

    def test_get_sknf_string(self):
        self.assertEqual(self.nf.get_sknf(), "(a | !b) & (!a | b)")

    def test_get_sdnf_numeric_format(self):
        self.assertEqual(self.nf.get_sdnf_numeric(), "[0, 3]")

    def test_get_sknf_numeric_format(self):
        self.assertEqual(self.nf.get_sknf_numeric(), "[1, 2]")

    def test_sdnf_empty(self):
        parser = ExpressionParser()
        table = TruthTable(parser.parse("a & !a"))
        nf = NormalForms(table)
        self.assertEqual(nf.get_sdnf(), "0")

    def test_sknf_empty(self):
        parser = ExpressionParser()
        table = TruthTable(parser.parse("a | !a"))
        nf = NormalForms(table)
        self.assertEqual(nf.get_sknf(), "1")

if __name__ == '__main__':
    unittest.main()