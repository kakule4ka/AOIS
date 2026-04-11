# test_expr_parser.py
import unittest
from src.expr_parser import ExpressionParser

class TestExpressionParser(unittest.TestCase):
    def setUp(self):
        self.parser = ExpressionParser()

    def test_parse_simple_expression_variables(self):
        evaluator = self.parser.parse("a & b")
        self.assertEqual(evaluator.variables, ['a', 'b'])

    def test_evaluate_simple_expression_true(self):
        evaluator = self.parser.parse("a & b")
        result = evaluator.evaluate({'a': 1, 'b': 1})
        self.assertEqual(result, 1)

    def test_evaluate_simple_expression_false(self):
        evaluator = self.parser.parse("a & b")
        result = evaluator.evaluate({'a': 1, 'b': 0})
        self.assertEqual(result, 0)

    def test_evaluate_complex_expression(self):
        evaluator = self.parser.parse("!(a -> b) | c")
        result = evaluator.evaluate({'a': 1, 'b': 0, 'c': 0})
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()