import unittest
from main import guess_number, list_generator, par_is_corr

class TestGuessNumber(unittest.TestCase):
    """
    Функция TestGuessNumber тестирует основную функцию guess_number и вспомогательные
    для неё list_generator и par_is_cor на правильность вывода функций, правильность вызова ошибок.
    """

    def test_sequential_search(self):
        """Проверяет корректность работы алгоритма последовательного поиска."""
        diap = [1, 2, 3, 4, 5]
        target = 3
        result = guess_number(diap, target, 'seq')
        self.assertEqual(result, (3, 3))

    def test_binary_search(self):
        """Проверяет корректность работы бинарного поиска."""
        diap = [1, 2, 3, 4, 5]
        target = 4
        result = guess_number(diap, target, 'bin')
        self.assertEqual(result[0], 4)
        self.assertTrue(result[1] <= 3)

    def test_unsorted_input_list(self):
        """Проверяет, что поиск работает и при несортированном списке."""
        diap = [5, -1, 3, 4, 2]
        target = 4
        result = guess_number(diap, target, 'seq')
        self.assertEqual(result[0], 4)

        result = guess_number(diap, target, 'bin')
        self.assertEqual(result[0], 4)

    def test_value_not_in_range(self):
        """Проверяет, что при поиске числа вне диапазона вызывается ошибка."""
        with self.assertRaises(ValueError):
            guess_number([1, 2, 3, 4, 5], 10, 'seq')

    def test_invalid_algorithm_type(self):
        """Проверяет обработку неверного значения типа алгоритма."""
        with self.assertRaises(ValueError):
            guess_number([1, 2, 3], 2, 'wrong_type')

    def test_empty_list(self):
        """Проверяет, что при пустом списке вызывается ошибка."""
        with self.assertRaises(ValueError):
            guess_number([], 1, 'seq')

    def test_invalid_list_type(self):
        """Проверяет, что при передаче не списка вызывается ошибка."""
        with self.assertRaises(TypeError):
            guess_number('12345', 1, 'seq')

    def test_non_integer_in_list(self):
        """Проверяет, что при передаче списка с неверным параметром вызывается ошибка."""
        diap = [1, 2.5, 3]
        with self.assertRaises(TypeError):
            guess_number(diap, 3, 'seq')

    def test_single_element_list(self):
        """Проверяет, что поиск работает при диапазоне из одного числа"""
        diap = [42]
        result = guess_number(diap, 42, 'seq')
        self.assertEqual(result, (42, 1))




    def test_par_is_corr_with_int_str_float(self):
        """Проверяет корректную работу функции преобразования типов."""
        self.assertEqual(par_is_corr(10), 10)
        self.assertEqual(par_is_corr("10"), 10)
        self.assertEqual(par_is_corr("+5"), 5)
        self.assertEqual(par_is_corr("-7.0"), -7)
        with self.assertRaises(TypeError):
            par_is_corr("abc")




    def test_list_generator(self):
        """Проверяет правильность формирования диапазона."""
        self.assertEqual(list_generator(1, 3), [1, 2, 3])
        self.assertEqual(list_generator(3, 1), [1, 2, 3])
        with self.assertRaises(TypeError):
            list_generator("a", 5)


if __name__ == '__main__':
    unittest.main()
