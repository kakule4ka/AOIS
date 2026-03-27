import unittest
from src.expr_parser import ExpressionParser
from src.truth_table import TruthTable
from src.zhegalkin import ZhegalkinPolynomial
from src.post_classes import PostClasses

EXPR_CONST_ZERO = "a & !a"
EXPR_AND = "a & b"
EXPR_IMPL = "a -> b"
CLASS_T0 = "T0"
CLASS_T1 = "T1"

class TestPostClasses(unittest.TestCase):
    def test_t0_class_membership(self):
        parser = ExpressionParser()
        table = TruthTable(parser.parse(EXPR_CONST_ZERO))
        zh = ZhegalkinPolynomial(table.results, table.variables)
        post = PostClasses(table, zh)
        self.assertTrue(post.is_T0())
        self.assertFalse(post.is_T1())

    def test_get_all_classes_dictionary(self):
        parser = ExpressionParser()
        table = TruthTable(parser.parse(EXPR_CONST_ZERO))
        zh = ZhegalkinPolynomial(table.results, table.variables)
        post = PostClasses(table, zh)
        classes = post.get_all_classes()
        self.assertIn(CLASS_T0, classes)
        self.assertTrue(classes[CLASS_T0])

    def test_is_s_false(self):
        table = TruthTable(ExpressionParser().parse(EXPR_AND))
        zh = ZhegalkinPolynomial(table.results, table.variables)
        post = PostClasses(table, zh)
        self.assertFalse(post.is_S())

    def test_is_m_false(self):
        table = TruthTable(ExpressionParser().parse(EXPR_IMPL))
        zh = ZhegalkinPolynomial(table.results, table.variables)
        post = PostClasses(table, zh)
        self.assertFalse(post.is_M())

if __name__ == '__main__':
    unittest.main()