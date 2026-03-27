import unittest
from src.bit_array import BitArray

class TestBitArray(unittest.TestCase):
    def test_initialization(self):
        arr = BitArray()
        self.assertEqual(len(arr.bits), 32)
        self.assertEqual(sum(arr.bits), 0)