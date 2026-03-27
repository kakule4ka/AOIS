import unittest
from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable

EXPR_OR = "a | b"
EXPECTED_VARIABLES = ['a', 'b']
EXPECTED_RESULTS = [0, 1, 1, 1]
EXPECTED_INDEX_FORM = "0111"

class TestTruthTable(unittest.TestCase):
    def setUp(self):
        self.table = TruthTable(ExpressionParser().parse(EXPR_OR))

    def test_variables_extracted_correctly(self):
        self.assertEqual(self.table.variables, EXPECTED_VARIABLES)

    def test_results_generation(self):
        self.assertEqual(self.table.results, EXPECTED_RESULTS)

    def test_index_form_generation(self):
        self.assertEqual(self.table.get_index_form(), EXPECTED_INDEX_FORM)

    def test_on_set_generation(self):
        self.assertEqual(len(self.table.get_on_set()), 3)

    def test_off_set_generation(self):
        self.assertEqual(len(self.table.get_off_set()), 1)

    def test_get_table(self):
        vars_list, rows, results = self.table.get_table()
        self.assertEqual(len(vars_list), 2)
        self.assertEqual(len(rows), 4)
        self.assertEqual(len(results), 4)

if __name__ == '__main__':
    unittest.main()