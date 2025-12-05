import unittest
from models import Author, App, User, Currency, Subscriptions
from utilites.get_currency import get_currencies, get_value_info


class TestAuthor(unittest.TestCase):
    def test_valid_author(self):
        """Тест корректного создания объекта класса Автор"""
        author = Author("Иван Иванов", "P3141")
        self.assertEqual(author.name, "Иван Иванов")
        self.assertEqual(author.group, "P3141")

    def test_invalid_name_short(self):
        """Тест ошибки при неверных параметрах класса Автор"""
        with self.assertRaises(ValueError):
            Author("А", "P3141")

        with self.assertRaises(ValueError):
            Author(123, "P3141")

        with self.assertRaises(ValueError):
            Author("Иван Иванов", "P31")

        with self.assertRaises(ValueError):
            Author("Иван Иванов", 123)


class TestApp(unittest.TestCase):
    def setUp(self):
        self.author = Author("Тест", "P3141")

    def test_valid_app(self):
        """Тест успешной инициализации объекта класса App"""
        app = App("MyApp", "v1.0", self.author.name)
        self.assertEqual(app.name, "MyApp")
        self.assertEqual(app.version, "v1.0")
        self.assertEqual(app.author, "Тест")

    def test_invalid_name_not_str(self):
        """Тест ошибки при неверных параметрах у объекта класса App"""
        with self.assertRaises(ValueError):
            App(123, "v1.0", self.author)

        with self.assertRaises(ValueError):
            App("", "v1.0", self.author)

        with self.assertRaises(ValueError):
            App("MyApp", 1.0, self.author)

        with self.assertRaises(ValueError):
            App("MyApp", "", self.author)


class TestUser(unittest.TestCase):
    def test_valid_user(self):
        """Тест успешной инициализации объекта класса User"""
        user = User(1, "Алиса Смирнова")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Алиса Смирнова")

    def test_invalid_id_not_int(self):
        """Тест ошибки при неверных параметрах у объектов класса User"""
        with self.assertRaises(ValueError):
            User("1", "Алиса")

        with self.assertRaises(ValueError):
            User(-1, "Алиса")

        with self.assertRaises(ValueError):
            User(0, "Алиса")

        with self.assertRaises(ValueError):
            User(1, "А")

        with self.assertRaises(ValueError):
            User(1, 123)


class TestCurrency(unittest.TestCase):
    def test_valid_currency(self):
        """Тест успешной инициализации объекта класа Currency"""
        cur = Currency("USD")
        info = get_value_info("USD")
        self.assertEqual(cur.id, info['ID'])
        self.assertEqual(cur.num_code, info['NumCode'])
        self.assertEqual(cur.char_code, "USD")
        self.assertEqual(cur.name, info['Name'])
        self.assertEqual(cur.value, info['Value'])
        self.assertEqual(cur.nominal, info['Nominal'])

    def test_invalid_char_code_not_str(self):
        eur = Currency("EUR")
        with self.assertRaises(ValueError):
            Currency(123)

        with self.assertRaises(ValueError):
            Currency("US")

        with self.assertRaises(ValueError):
            eur.name = 'E'

        with self.assertRaises(ValueError):
            eur.value = -10.0

        with self.assertRaises(ValueError):
            eur.value = 0

        with self.assertRaises(ValueError):
            eur.nominal = '1'

        with self.assertRaises(ValueError):
            eur.nominal = -1

        with self.assertRaises(ValueError):
            eur.id = 1234


class TestSubscriptions(unittest.TestCase):

    def test_valid_subscription(self):
        sub = Subscriptions(1, 1, ["USD", "EUR"])
        self.assertEqual(sub.id, 1)
        self.assertEqual(sub.user_id, 1)
        self.assertEqual(sub.currency_id, ["USD", "EUR"])

    def test_invalid_currency_id_not_list(self):
        with self.assertRaises(ValueError):
            Subscriptions(1, 1, "USD")

        with self.assertRaises(ValueError):
            Subscriptions(1, 1, [])

        with self.assertRaises(ValueError):
            Subscriptions(1, 1, ["USD", 123])

        with self.assertRaises(ValueError):
            Subscriptions(1, "1", ["USD"])

        with self.assertRaises(ValueError):
            Subscriptions(1, -1, ["USD"])

        with self.assertRaises(ValueError):
            Subscriptions("1", 1, ["USD"])


if __name__ == '__main__':
    unittest.main()