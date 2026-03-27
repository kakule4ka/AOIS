import unittest
from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable
from src.minimizer import Minimizer

EXPR_FOR_MINIMIZATION = "a | (a & b)"
KEY_STAGES = "stages"
KEY_PRIME_IMPLICANTS = "prime_implicants"
KEY_TABLE = "table"

class TestMinimizer(unittest.TestCase):
    def setUp(self):
        parser = ExpressionParser()
        evaluator = parser.parse(EXPR_FOR_MINIMIZATION)
        table = TruthTable(evaluator)
        self.minimizer = Minimizer(table)

    def test_get_calculation_method_structure(self):
        calc_data = self.minimizer.get_calculation_method()
        self.assertIn(KEY_STAGES, calc_data)
        self.assertIn(KEY_PRIME_IMPLICANTS, calc_data)

    def test_get_calculation_tabular_method(self):
        tab_data = self.minimizer.get_calculation_tabular_method()
        self.assertIn(KEY_STAGES, tab_data)
        self.assertIn(KEY_TABLE, tab_data)
        self.assertTrue(isinstance(tab_data[KEY_TABLE], dict))

if __name__ == '__main__':
    unittest.main()