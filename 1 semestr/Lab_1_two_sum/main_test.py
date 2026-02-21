import unittest
from main import two_sum


# Тесты
class TestTwoSum(unittest.TestCase):
    def exmaple_test(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])
        self.assertEqual(two_sum([3, 2, 4], 6), [1, 2])
        self.assertEqual(two_sum([3, 3], 6), [0, 1])

    def test_add_simple_case(self):
        self.assertEqual(two_sum([1, 4, 6, 2, 6, 9, 3, 7, 5], 13), [1, 5])

    def test_add_negative(self):
        self.assertEqual(two_sum([1, 4, 6, 2, -6, 9, 3, -7, 5], -13), [4, 7])

    def test_target_is_integer_float(self):
      self.assertEqual(two_sum([1, 2, 3, 4, 5], 8.0), [2, 4])

    def test_target_is_list(self):
      self.assertIsNone(two_sum([1, 2.0, 3, 4, 5.0], [8.0]))

    def test_elem_is_string(self):
      self.assertIsNone(two_sum([1, 2.0, '3', 4, 5.0], 8.0))

    def test_elem_is_float(self):
      self.assertIsNone(two_sum([1, 2.0, 3, 4, 5.1], 8.0))

    def test_wrong_input(self):
      self.assertIsNone(two_sum('1231', [12, 3, 4]))


# Запуск тестов
if __name__ == '__main__':
    unittest.main()
