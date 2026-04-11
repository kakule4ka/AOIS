import unittest
from src.hash_table import HashTable

class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(size=20)

    def test_get_v_calculation(self):
        self.assertEqual(self.ht._get_v("аб"), 1)
        self.assertEqual(self.ht._get_v("Вя"), 98)
        self.assertEqual(self.ht._get_v("Тр"), 644)
        self.assertEqual(self.ht._get_v("А"), 0)

    def test_hash_calculation(self):
        v = 98
        expected_hash = 98 % 20
        self.assertEqual(self.ht._hash(v), expected_hash)

    def test_create_and_read_single(self):
        self.assertTrue(self.ht.create("Абаев", "Сергей"))
        self.assertEqual(self.ht.read("Абаев"), "Сергей")
        self.assertIsNone(self.ht.read("Неизвестный"))

    def test_create_duplicate_key(self):
        self.ht.create("Бобков", "Тимур")
        self.assertFalse(self.ht.create("Бобков", "Другой"))

    def test_collision_chaining_creation(self):
        self.assertTrue(self.ht.create("Ковалев", "Игорь"))
        self.assertTrue(self.ht.create("Кожевников", "Максим"))
        self.assertTrue(self.ht.create("Козлов", "Петр"))

        self.assertEqual(self.ht.read("Ковалев"), "Игорь")
        self.assertEqual(self.ht.read("Кожевников"), "Максим")
        self.assertEqual(self.ht.read("Козлов"), "Петр")

    def test_collision_chaining_flags(self):
        self.ht.create("Давыденко", "Александр")
        self.ht.create("Данилов", "Павел")

        v = self.ht._get_v("Давыденко")
        h = self.ht._hash(v)
        head_node = self.ht.table[h]

        self.assertIsNotNone(head_node)
        self.assertEqual(head_node.id_key, "Давыденко")
        self.assertEqual(head_node.c_flag, 1)
        self.assertEqual(head_node.t_flag, 0)

        second_node = head_node.p0_next
        self.assertIsNotNone(second_node)
        self.assertEqual(second_node.id_key, "Данилов")
        self.assertEqual(second_node.c_flag, 0)
        self.assertEqual(second_node.t_flag, 1)

    def test_update_data(self):
        self.ht.create("Видерт", "Евгений")
        self.assertTrue(self.ht.update("Видерт", "Евгений Обновленный"))
        self.assertEqual(self.ht.read("Видерт"), "Евгений Обновленный")
        self.assertFalse(self.ht.update("Отсутствующий", "Данные"))

    def test_update_in_chain(self):
        self.ht.create("Ковалев", "Игорь")
        self.ht.create("Кожевников", "Максим")
        self.assertTrue(self.ht.update("Кожевников", "Максим Новый"))
        self.assertEqual(self.ht.read("Кожевников"), "Максим Новый")

    def test_delete_single_node(self):
        self.ht.create("Кот", "Василий")
        self.assertTrue(self.ht.delete("Кот"))
        self.assertIsNone(self.ht.read("Кот"))
        self.assertFalse(self.ht.delete("Кот"))

    def test_delete_head_of_chain(self):
        self.ht.create("Ковалев", "Игорь")
        self.ht.create("Кожевников", "Максим")
        
        self.assertTrue(self.ht.delete("Ковалев"))
        self.assertIsNone(self.ht.read("Ковалев"))
        self.assertEqual(self.ht.read("Кожевников"), "Максим")

    def test_delete_middle_of_chain(self):
        self.ht.create("Ковалев", "Игорь")
        self.ht.create("Кожевников", "Максим")
        self.ht.create("Козлов", "Петр")

        self.assertTrue(self.ht.delete("Кожевников"))
        self.assertIsNone(self.ht.read("Кожевников"))
        self.assertEqual(self.ht.read("Ковалев"), "Игорь")
        self.assertEqual(self.ht.read("Козлов"), "Петр")

    def test_deleted_flags(self):
        self.ht.create("Гракова", "Иван")
        v = self.ht._get_v("Гракова")
        h = self.ht._hash(v)
        
        node = self.ht.table[h]
        self.assertEqual(node.d_flag, 0)
        self.assertEqual(node.u_flag, 1)

        self.ht.delete("Гракова")
        self.assertEqual(node.d_flag, 1)
        self.assertEqual(node.u_flag, 0)

    def test_load_factor(self):
        self.assertEqual(self.ht.load_factor(), 0.0)
        self.ht.create("Абаев", "Сергей")
        self.ht.create("Бобков", "Тимур")
        self.assertEqual(self.ht.load_factor(), 2 / 20)

if __name__ == '__main__':
    unittest.main()