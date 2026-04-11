import unittest
from src.expr_parser import ExpressionParser

EXPR_SIMPLE_AND = "a & b"
EXPR_COMPLEX = "!(a -> b) | c"
VAR_A = 'a'
VAR_B = 'b'
VAR_C = 'c'

class TestExpressionParser(unittest.TestCase):
    def setUp(self):
        self.parser = ExpressionParser()

    def test_parse_simple_expression_variables(self):
        evaluator = self.parser.parse(EXPR_SIMPLE_AND)
        self.assertEqual(evaluator.variables, [VAR_A, VAR_B])

    def test_evaluate_simple_expression_true(self):
        evaluator = self.parser.parse(EXPR_SIMPLE_AND)
        result = evaluator.evaluate({VAR_A: 1, VAR_B: 1})
        self.assertEqual(result, 1)

    def test_evaluate_simple_expression_false(self):
        evaluator = self.parser.parse(EXPR_SIMPLE_AND)
        result = evaluator.evaluate({VAR_A: 1, VAR_B: 0})
        self.assertEqual(result, 0)

    def test_evaluate_complex_expression(self):
        evaluator = self.parser.parse(EXPR_COMPLEX)
        result = evaluator.evaluate({VAR_A: 1, VAR_B: 0, VAR_C: 0})
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()