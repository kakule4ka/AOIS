# test_truth_table.py
import unittest
from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable

class TestTruthTable(unittest.TestCase):
    def setUp(self):
        self.table = TruthTable(ExpressionParser().parse("a | b"))

    def test_variables_extracted_correctly(self):
        self.assertEqual(self.table.variables, ['a', 'b'])

    def test_results_generation(self):
        results = [row[1] for row in self.table.table]
        self.assertEqual(results, [0, 1, 1, 1])

    def test_index_form_generation(self):
        self.assertEqual(self.table.get_index_form(), "0111")

    def test_on_set_generation(self):
        self.assertEqual(len(self.table.get_on_set()), 3)

    def test_off_set_generation(self):
        self.assertEqual(len(self.table.get_off_set()), 1)

    def test_get_table(self):
        vars_list = self.table.variables
        rows = [row[0] for row in self.table.table]
        results = [row[1] for row in self.table.table]
        
        self.assertEqual(len(vars_list), 2)
        self.assertEqual(len(rows), 4)
        self.assertEqual(len(results), 4)

if __name__ == '__main__':
    unittest.main()