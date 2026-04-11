# test_post_classes.py
import unittest
from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable
from src.zhegalkin import ZhegalkinPolynomial
from src.post_classes import PostClasses

class TestPostClasses(unittest.TestCase):
    def test_t0_class_membership(self):
        parser = ExpressionParser()
        table = TruthTable(parser.parse("a & !a"))
        zh = ZhegalkinPolynomial(table.get_index_form(), table.variables)
        post = PostClasses(table, zh)
        self.assertTrue(post.is_T0())
        self.assertFalse(post.is_T1())

    def test_get_all_classes_dictionary(self):
        parser = ExpressionParser()
        table = TruthTable(parser.parse("a & !a"))
        zh = ZhegalkinPolynomial(table.get_index_form(), table.variables)
        post = PostClasses(table, zh)
        classes = post.get_all_classes()
        self.assertIn("T0", classes)
        self.assertTrue(classes["T0"])

    def test_is_s_false(self):
        table = TruthTable(ExpressionParser().parse("a & b"))
        zh = ZhegalkinPolynomial(table.get_index_form(), table.variables)
        post = PostClasses(table, zh)
        self.assertFalse(post.is_S())

    def test_is_m_false(self):
        table = TruthTable(ExpressionParser().parse("a -> b"))
        zh = ZhegalkinPolynomial(table.get_index_form(), table.variables)
        post = PostClasses(table, zh)
        self.assertFalse(post.is_M())

if __name__ == '__main__':
    unittest.main()