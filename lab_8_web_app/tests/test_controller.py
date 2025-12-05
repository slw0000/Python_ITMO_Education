import unittest
import threading
import urllib.request
import urllib.error
from http.server import HTTPServer

from myapp import SimpleHTTPRequestHandler


class TestController(unittest.TestCase):
    SERVER = None
    THREAD = None
    PORT = 8080

    @classmethod
    def setUpClass(cls):
        """Запускаем сервер перед тестами"""
        cls.SERVER = HTTPServer(('localhost', cls.PORT), SimpleHTTPRequestHandler)
        cls.THREAD = threading.Thread(target=cls.SERVER.serve_forever)
        cls.THREAD.daemon = True
        cls.THREAD.start()

    @classmethod
    def tearDownClass(cls):
        """Останавливаем сервер после тестов"""
        cls.SERVER.shutdown()
        cls.THREAD.join()

    def make_request(self, path):
        """Вспомогательная функция для выполнения GET-запроса"""
        url = f"http://localhost:{self.PORT}{path}"
        try:
            with urllib.request.urlopen(url) as response:
                return response.read().decode('utf-8'), response.getcode()
        except urllib.error.HTTPError as e:
            return e.read().decode('utf-8'), e.code

    def test_root_page(self):
        """Тест главной страницы"""
        content, code = self.make_request('/')
        self.assertEqual(code, 200)
        self.assertIn('Главная страница', content)
        self.assertIn('CurrenciesListApp', content)

    def test_author_page(self):
        """Тест страницы об авторе"""
        content, code = self.make_request('/author')
        self.assertEqual(code, 200)
        self.assertIn('Об авторе', content)
        self.assertIn('P3124', content)  # группа автора

    def test_users_page(self):
        """Тест страницы со всеми пользователями"""
        content, code = self.make_request('/users')
        self.assertEqual(code, 200)
        self.assertIn('Список пользователей', content)
        self.assertIn('Ivan Ivanov', content)

    def test_currencies_page(self):
        """ТЕст страницы со списком доступных валют"""
        content, code = self.make_request('/currencies')
        self.assertEqual(code, 200)
        self.assertIn('Список валют', content)
        self.assertIn('USD', content)
        self.assertIn('EUR', content)
        self.assertIn('GBP', content)

    def test_user_page_valid_id_1(self):
        """Тест страницы с информацией о пользователе"""
        content, code = self.make_request('/user?id=1')
        self.assertEqual(code, 200)
        self.assertIn('Информация о пользователе', content)
        self.assertIn('Ivan Ivanov', content)
        self.assertIn('USD', content)
        self.assertIn('EUR', content)

        content, code = self.make_request('/user?id=2')
        self.assertEqual(code, 200)
        self.assertIn('Vladimir Putin', content)
        self.assertIn('EUR', content)
        self.assertIn('GBP', content)

    def test_user_page_missing_id(self):
        """Тест ошибки при неверном маршруте формата /user?..."""
        content, code = self.make_request('/user')
        self.assertEqual(code, 404)
        self.assertIn('ошибк', content.lower())

        content, code = self.make_request('/user?id=abc')
        self.assertEqual(code, 404)

    def test_user_page_nonexistent_id(self):
        """Тест ошибки при несуществующем id"""
        content, code = self.make_request('/user?id=999')
        self.assertIn(code, [404, 400])
        self.assertIn('не найден', content.lower())

    def test_404_page(self):
        """Тест ошибки при несуществуещем маршруте"""
        content, code = self.make_request('/nonexistent')
        self.assertEqual(code, 404)
        self.assertIn('не найдена', content.lower())


if __name__ == '__main__':
    unittest.main(argv=[''], exit=False, verbosity=2)