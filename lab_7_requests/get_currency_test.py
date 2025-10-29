import unittest
import requests
import io
import sys
from get_currency import get_currencies


MAX_R_VALUE = 1000
currency_list = ['USD', 'EUR']


class TestGetCurrencies(unittest.TestCase):

  def test_currency_usd(self):
    """
      Проверяет наличие ключа в словаре и значения этого ключа
    """

    currency_data = get_currencies(currency_list)

    self.assertIn(currency_list[0], currency_data)
    self.assertIsInstance(currency_data['USD'], float)
    self.assertGreaterEqual(currency_data['USD'], 0)
    self.assertLessEqual(currency_data['USD'], MAX_R_VALUE)

  def test_nonexist_code(self):
    self.assertIn("Код валюты", get_currencies(['XYZ'])['XYZ'])
    self.assertIn("XYZ", get_currencies(['XYZ'])['XYZ'])
    self.assertIn("не найден", get_currencies(['XYZ'])['XYZ'])

  def test_get_currency_error(self):
    with self.assertRaises(requests.exceptions.RequestException):
      get_currencies(currency_list, url="https://")




class TestStreamWrite(unittest.TestCase):

  def setUp(self):
    self.nonstandardstream = io.StringIO()


    try:
      self.get_currencies = get_currencies(['USD'],
                                         url="https://",
                                         handle=self.nonstandardstream)
    except:
      pass
      # self.trace = trace(get_currencies, handle=self.nonstandardstream)


  def test_writing_stream(self):
    error_phrase_regex = "Ошибка при запросе к API"
    logger = open('logger/errors.log', 'r')
    log_line = logger.readline()

    error_text_io = self.nonstandardstream.getvalue()

    self.assertIn(error_phrase_regex, error_text_io)
    self.assertIn(log_line, error_text_io)

    # with self.assertRaises(requests.exceptions.RequestException):
    # self.trace(['USD'], url="https://")


  def tearDown(self):
    del self.nonstandardstream


if __name__ == '__main__':
  unittest.main()