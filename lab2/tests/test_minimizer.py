# test_minimizer.py
import unittest
from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable
from src.minimizer import Minimizer

class TestMinimizer(unittest.TestCase):
    def setUp(self):
        parser = ExpressionParser()
        evaluator = parser.parse("a | (a & b)")
        table = TruthTable(evaluator)
        self.minimizer = Minimizer(table)

    def test_get_calculation_method(self):
        calc_data = self.minimizer.get_calculation_method(for_sdnf=True)
        
        self.assertIn("stages", calc_data)
        self.assertIn("prime_implicants", calc_data)
        self.assertIn("minimal_form", calc_data)
        
        self.assertCountEqual(calc_data["stages"][0], ['10', '11'])
        self.assertCountEqual(calc_data["stages"][1], ['1-'])
        
        self.assertCountEqual(calc_data["prime_implicants"], ['1-'])
        self.assertEqual(calc_data["minimal_form"], "a")

    def test_get_tabular_method(self):
        tab_data = self.minimizer.get_tabular_method(for_sdnf=True)
        
        self.assertIn("stages", tab_data)
        self.assertIn("table", tab_data)
        
        self.assertIn('1-', tab_data["table"])
        self.assertCountEqual(tab_data["table"]['1-'], ['10', '11'])

    def test_get_karnaugh_map(self):
        k_map = self.minimizer.get_karnaugh_map()
        
        self.assertEqual(k_map['rows_vars'], 'a')
        self.assertEqual(k_map['cols_vars'], 'b')
        
        expected_map = [
            ["", "0", "1"],
            ["0", "0", "0"],
            ["1", "1", "1"]
        ]
        self.assertEqual(k_map['map'], expected_map)

if __name__ == '__main__':
    unittest.main()