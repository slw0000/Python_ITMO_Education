import unittest
from unittest.mock import MagicMock
from controllers.currencycontroller import CurrencyController
from controllers.usercontroller import UserController


class TestCurrencyController(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.controller = CurrencyController(self.mock_db)

    def test_create_currency(self):
        """Тест создание валюты."""
        mock_currency = MagicMock()
        self.controller.create_currency(mock_currency)
        self.mock_db._create.assert_called_once_with(mock_currency)

    def test_cur_info(self):
        """Тест получение валюты по символьному коду."""
        fake_data = {"id": 1, "char_code": "USD", "value": 90.5}
        self.mock_db._read.return_value = fake_data

        result = self.controller.cur_info("USD")

        self.assertEqual(result, fake_data)
        self.mock_db._read.assert_called_once_with("USD")

    def test_cur_info_by_id(self):
        """Тест получение валюты по ID."""
        fake_data = {"id": 2, "char_code": "EUR", "value": 92.1}
        self.mock_db._read_by_id.return_value = fake_data

        result = self.controller.cur_info_by_id(2)

        self.assertEqual(result, fake_data)
        self.mock_db._read_by_id.assert_called_once_with(2)

    def test_cur_info_all(self):
        """Тест получение всех валют."""
        fake_list = [
            {"id": 1, "char_code": "USD"},
            {"id": 2, "char_code": "EUR"}
        ]
        self.mock_db._read_all.return_value = fake_list

        result = self.controller.cur_info_all()

        self.assertEqual(result, fake_list)
        self.mock_db._read_all.assert_called_once()

    def test_update_currency(self):
        """Тест обновление курса через внешний API."""
        self.controller.update_currency("GBP")
        self.mock_db._update.assert_called_once_with("GBP")

    def test_update_currency_value(self):
        """Тест обновление курса с явным значением."""
        self.controller.update_currency_value("USD", 100.5)
        self.mock_db._update_by_char_code.assert_called_once_with("USD", 100.5)

    def test_update_all(self):
        """Тест обновление всех валют."""
        fake_currencies = [
            {"id": 1, "char_code": "USD"},
            {"id": 2, "char_code": "EUR"}
        ]
        self.mock_db._read_all.return_value = fake_currencies

        self.controller.update_all()

        self.mock_db._read_all.assert_called_once()
        self.mock_db._update.assert_any_call("USD")
        self.mock_db._update.assert_any_call("EUR")
        self.assertEqual(self.mock_db._update.call_count, 2)

    def test_delete_currency(self):
        """Тест удаление валюты по ID."""
        self.controller.delete_currency(5)
        self.mock_db._delete.assert_called_once_with(5)


class TestUserController(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.controller = UserController(self.mock_db)

    def test_create_user(self):
        """Тест создание пользователя."""
        mock_user = MagicMock()
        self.controller.create_user(mock_user)
        self.mock_db._create.assert_called_once_with(mock_user)

    def test_user_info(self):
        """Тест получение пользователя по ID."""
        fake_user = {"id": 3, "name": "Иван"}
        self.mock_db._read.return_value = fake_user

        result = self.controller.user_info(3)

        self.assertEqual(result, fake_user)
        self.mock_db._read.assert_called_once_with(3)

    def test_user_info_all(self):
        """Тест получение всех пользователей."""
        fake_users = [{"id": 1, "name": "Иван"}, {"id": 2, "name": "Артём"}]
        self.mock_db._read_all.return_value = fake_users

        result = self.controller.user_info_all()

        self.assertEqual(result, fake_users)
        self.mock_db._read_all.assert_called_once()

    def test_update_user_info(self):
        """Тест обновление имени пользователя."""
        self.controller.update_user_info(10, "Новое Имя")
        self.mock_db._update.assert_called_once_with(10, "Новое Имя")

    def test_delete_user(self):
        """Тест удаление пользователя."""
        self.controller.delete_user(7)
        self.mock_db._delete.assert_called_once_with(7)


if __name__ == '__main__':
    unittest.main()