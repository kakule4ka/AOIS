import unittest
from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable
from src.analyzer import BooleanAnalyzer

EXPR_WITH_DUMMY = "a | (b & !b)"
DUMMY_VARIABLE = 'b'
VAR_A = 'a'
VAR_NOT_EXIST = 'z'

class TestBooleanAnalyzer(unittest.TestCase):
    def setUp(self):
        parser = ExpressionParser()
        evaluator = parser.parse(EXPR_WITH_DUMMY)
        table = TruthTable(evaluator)
        self.analyzer = BooleanAnalyzer(table)

    def test_find_dummy_variables(self):
        dummies = self.analyzer.find_dummy_variables()
        self.assertIn(DUMMY_VARIABLE, dummies)

    def test_get_partial_derivative_existing(self):
        deriv = self.analyzer.get_partial_derivative(VAR_A)
        self.assertTrue(any(v == 1 for v in deriv))

    def test_get_partial_derivative_missing(self):
        deriv = self.analyzer.get_partial_derivative(VAR_NOT_EXIST)
        self.assertEqual(deriv, [])

    def test_get_mixed_derivative_existing(self):
        deriv = self.analyzer.get_mixed_derivative([VAR_A, DUMMY_VARIABLE])
        self.assertTrue(all(v == 0 for v in deriv))

    def test_get_mixed_derivative_missing(self):
        deriv = self.analyzer.get_mixed_derivative([VAR_NOT_EXIST])
        self.assertEqual(len(deriv), len(self.analyzer.results))

if __name__ == '__main__':
    unittest.main()