import io
import requests
import unittest
import logging

from get_currency import get_currencies
from logger.logger import logger


class TestGetCurrencies(unittest.TestCase):
    """
    Тестирование функции get_currencies()
    """

    def test_currency(self):
        """
        Проверяет наличие ключа в словаре и значения этого ключа
        """

        MAX_R_VALUE = 1000
        currency_list = ['USD', 'EUR']

        currency_data = get_currencies(currency_list)
        self.assertIn(currency_list[0], currency_data)
        self.assertIsInstance(currency_data['USD'], float)
        self.assertGreaterEqual(currency_data['USD'], 0)
        self.assertLessEqual(currency_data['USD'], MAX_R_VALUE)

    def test_wrong_valute(self):
        """
        Проверяет поведение функции при несуществующей валюте
        """

        currency_list = ['USD', 'EUR', 'GBR']

        self.assertIn("Код валюты", get_currencies(currency_list)['GBR'])
        self.assertIn("не найден", get_currencies(currency_list)['GBR'])

    def test_connection_error(self):
        """
        Проверяет правильность вызова ConnectionError
        """

        currency_list = ['USD', 'EUR']

        with self.assertRaises(requests.exceptions.ConnectionError):
            get_currencies(currency_list, url='https://www.notcorrectapi.ru')

    def test_value_error(self):
        """
            Проверяет правильность вызова ValueError
        """

        currency_list = ['USD', 'EUR']

        with self.assertRaises(ValueError):
            get_currencies(currency_list, url='https://google.com')



class TestIOStreamWrite(unittest.TestCase):
    """
    Тестирование логирования работы функции и вывода ошибок через IOStream
    """

    def setUp(self):
        """
        Настройка функции для тестирования
        """

        self.stream = io.StringIO()
        self.decorated_func = logger(handle=self.stream)(get_currencies)

    def test_logging_error(self):
        """
        Проверка логов при ошибках и правильность выбросов ошибок
        """

        with self.assertRaises(requests.exceptions.ConnectionError):
            self.decorated_func(['USD'], url="https://www.notcorrectapi.ru")

        logs = self.stream.getvalue()
        self.assertRegex(logs, "ERROR")
        self.assertIn("ConnectionError", logs)


    def test_logging_correct_work(self):
        """
        Проверка логов при успешной работе функции
        """

        self.decorated_func(['USD', 'EUR'])

        logs = self.stream.getvalue()
        self.assertIn("INFO", logs)
        self.assertIn("Вызов функции", logs)
        self.assertIn("['USD', 'EUR']", logs)

        self.assertIn("INFO", logs)
        self.assertIn("отработала успешно", logs)
        self.assertRegex(logs, r"\{'USD':\s*\d+\.?\d*,\s*'EUR':\s*\d+\.?\d*\}")


    def tearDown(self):
        del self.stream



class TestLogWrite(unittest.TestCase):
    """
    Тестирование логирования работы функции и вывода ошибок в логгер
    """

    def setUp(self):
        """
        Настройка функции для тестирования
        """

        logging.basicConfig(
            filename="logger/get_currencies.log",
            level=logging.DEBUG,
            format="%(levelname)s: %(message)s",
            filemode='w'
        )
        log = logging.getLogger('currency')

        self.decorated_func = logger(handle=log)(get_currencies)

    def test_logging_error(self):
        """
        Проверка логов при ошибках и правильность выбросов ошибок
        """

        with self.assertRaises(requests.exceptions.ConnectionError):
            self.decorated_func(['USD'], url="https://www.notcorrectapi.ru")

        self.logger = open("logger/get_currencies.log")
        log = self.logger.read()

        self.assertRegex(log, "ERROR")
        self.assertIn("ConnectionError", log)


    def test_logging_correct_work(self):
        """
        Проверка логов при успешной работе функции
        """

        self.decorated_func(['USD', 'EUR'])

        self.logger = open("logger/get_currencies.log")
        log = self.logger.read()

        self.assertIn("INFO", log)
        self.assertIn("Вызов функции", log)
        self.assertIn("['USD', 'EUR']", log)

        self.assertIn("INFO", log)
        self.assertIn("отработала успешно", log)
        self.assertRegex(log, r"\{'USD':\s*\d+\.?\d*,\s*'EUR':\s*\d+\.?\d*\}")



if __name__ == '__main__':
  unittest.main()