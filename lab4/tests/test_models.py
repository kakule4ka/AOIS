import unittest
from src.models import HashNode

class TestHashNode(unittest.TestCase):
    def test_node_initialization(self):
        node = HashNode("Иванов", "Данные")
        
        self.assertEqual(node.id_key, "Иванов")
        self.assertEqual(node.pi_data, "Данные")
        self.assertEqual(node.c_flag, 0)
        self.assertEqual(node.u_flag, 1)
        self.assertEqual(node.t_flag, 1)
        self.assertEqual(node.l_flag, 0)
        self.assertEqual(node.d_flag, 0)
        self.assertIsNone(node.p0_next)