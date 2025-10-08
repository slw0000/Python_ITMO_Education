import unittest
from main import gen_bin_tree, left_branch, right_branch


class TestBinTree(unittest.TestCase):
    """
    Класс TestBinTree тестирует функции gen_bin_tree, left_branch и
    right_branch на правильность вывода функций, правильность вызова ошибок.
    """

    def test_left_branch(self):
        """Проверяет корректность формирования левой ветки."""
        self.assertEqual(left_branch(2), 8)
        self.assertEqual(left_branch(3, lambda x: x + 14), 17)

    def test_right_branch(self):
        """Проверяет корректность формирования правой ветки."""
        self.assertEqual(right_branch(1), 2)
        self.assertEqual(right_branch(7, lambda x: x - 2), 5)

    def test_gen_bin_tree(self):
        """Проверка корректности формирования бинарного дерева и своевременности вывода ошибок."""
        self.assertEqual(gen_bin_tree(height=2, root=5, l_b=lambda x: x + 1, r_b=lambda x: x ** 2),
                         {"5": [{"6": [{"7": []}, {"36": []}]}, {"25":[{"26":[]}, {"625": []}]}]})
        self.assertEqual(gen_bin_tree(height=2, root=10, l_b=lambda x: x ** 2, r_b=lambda x: 2 * (x + 4)),
                         {"10": [{"100": [{"10000": []}, {"208": []}]}, {"28": [{"784": []}, {"64": []}]}]})

        self.assertEqual(gen_bin_tree(height=0, root=13), {'13': []})

        self.assertEqual(gen_bin_tree(),
                         {'4': [{'16': [
                             {'64': [{'256': [{'1024': []}, {'257': []}]}, {'65': [{'260': []}, {'66': []}]}]},
                             {'17': [{'68': [{'272': []}, {'69': []}]}, {'18': [{'72': []}, {'19': []}]}]}]}, {
                                    '5': [{'20': [{'80': [{'320': []}, {'81': []}]}, {'21': [{'84': []}, {'22': []}]}]},
                                          {'6': [{'24': [{'96': []}, {'25': []}]}, {'7': [{'28': []}, {'8': []}]}]}]}]}
                         )

        with self.assertRaises(ValueError):
            gen_bin_tree(height=-1, root=10)

        with self.assertRaises(ValueError):
            gen_bin_tree(height=1, root=0, h=3)

        with self.assertRaises(TypeError):
            gen_bin_tree(height=1.2, root=0, l_b=lambda x: x + 1)



if __name__ == '__main__':
    unittest.main()
