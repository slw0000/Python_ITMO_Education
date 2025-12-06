import unittest
from unittest.mock import MagicMock
from jinja2 import Environment, DictLoader
from models import Author, App
from controllers.pages import PageController


class TestPageRender(unittest.TestCase):

    def setUp(self):
        templates = {
            "main.html": "<title>{{ title }}</title><h1>{{ myapp }}</h1>",
            "author.html": "<h2>{{ title }}</h2><p>Группа: {{ group }}</p>",
            "users.html": "<h2>{{ title }}</h2>{% for user in navigation %}<p>{{ user.name }}</p>{% endfor %}",
            "currencies.html": "<h2>{{ title }}</h2>{% for item in all_vals %}<p>{{ item.char_code }}: {{ item.value }}</p>{% endfor %}",
            "user_info.html": "<h2>{{ title }}</h2><p>{{ user_name }}</p><p>Подписки: {{ sub_vals }}</p>"
        }
        self.env = Environment(loader=DictLoader(templates))

        self.mock_currency_ctrl = MagicMock()
        self.mock_user_ctrl = MagicMock()
        self.mock_sub_ctrl = MagicMock()

        self.author = Author('Artem Golubev', 'P3124')
        self.app = App('CurrenciesListApp', 'v0.1', 'Artem Golubev')

        self.page_ctrl = PageController(
            env=self.env,
            author=self.author,
            app=self.app,
            currency_controller=self.mock_currency_ctrl,
            user_controller=self.mock_user_ctrl,
            subscription_controller=self.mock_sub_ctrl
        )

    def test_render_main(self):
        """Тест рендер главной страницы."""
        html = self.page_ctrl.render_main()
        self.assertIn("<title>Главная страница</title>", html)
        self.assertIn("<h1>CurrenciesListApp</h1>", html)

    def test_render_author(self):
        """Тест рендер страницы об авторе."""
        html = self.page_ctrl.render_author()
        self.assertIn("<h2>Об авторе</h2>", html)
        self.assertIn("Группа: P3124", html)

    def test_render_users(self):
        """Тест рендер списка пользователей."""
        fake_users = [{"id": 1, "name": "Ivan"}, {"id": 2, "name": "Artem"}]
        self.mock_user_ctrl.user_info_all.return_value = fake_users

        html = self.page_ctrl.render_users()

        self.assertIn("<h2>Список пользователей</h2>", html)
        self.assertIn("<p>Ivan</p>", html)
        self.assertIn("<p>Artem</p>", html)
        self.mock_user_ctrl.user_info_all.assert_called_once()

    def test_render_currencies(self):
        """Тест рендер списка валют."""
        fake_currencies = [
            {"id": 1, "char_code": "USD", "value": 90.5, "name": "Доллар", "nominal": 1},
            {"id": 2, "char_code": "EUR", "value": 92.0, "name": "Евро", "nominal": 1}
        ]
        self.mock_currency_ctrl.cur_info_all.return_value = fake_currencies

        html = self.page_ctrl.render_currencies()

        self.assertIn("<h2>Список валют</h2>", html)
        self.assertIn("<p>USD: 90.5</p>", html)
        self.assertIn("<p>EUR: 92.0</p>", html)
        self.mock_currency_ctrl.cur_info_all.assert_called_once()

    def test_render_user_info_success(self):
        """Тест успешный рендер информации о пользователе."""
        self.mock_user_ctrl.user_info.return_value = {"id": 1, "name": "Ivan"}
        self.mock_sub_ctrl.vals_by_us.return_value = [{"currency_id": 1}, {"currency_id": 2}]

        def mock_cur_info_by_id(cid):
            data = {
                1: {"id": 1, "name": "USD", "char_code": "USD", "value": 90.5, "nominal": 1},
                2: {"id": 2, "name": "EUR", "char_code": "EUR", "value": 92.0, "nominal": 1}
            }
            return data.get(cid, {})

        self.mock_currency_ctrl.cur_info_by_id.side_effect = mock_cur_info_by_id

        html, code = self.page_ctrl.render_user_info({"id": ["1"]})

        self.assertEqual(code, 200)
        self.assertIn("<h2>Информация о пользователе</h2>", html)
        self.assertIn("<p>Ivan</p>", html)
        self.assertIn("USD", html)
        self.assertIn("EUR", html)

    def test_render_user_info_no_id(self):
        """Тест отсутствует id в запросе."""
        html, code = self.page_ctrl.render_user_info({})
        self.assertEqual(code, 400)
        self.assertIn("укажите id", html)

    def test_render_user_info_invalid_id(self):
        """Тест id не является числом."""
        html, code = self.page_ctrl.render_user_info({"id": ["abc"]})
        self.assertEqual(code, 400)
        self.assertIn("ID должен быть числом", html)

    def test_render_user_info_not_found(self):
        """Тест пользователь не найден."""
        self.mock_user_ctrl.user_info.return_value = {}
        html, code = self.page_ctrl.render_user_info({"id": ["999"]})
        self.assertEqual(code, 404)
        self.assertIn("не найден", html)

    def test_handle_currency_delete_success(self):
        """Тест успешное удаление валюты."""
        self.mock_currency_ctrl.delete_currency.return_value = True
        html, code = self.page_ctrl.handle_currency_delete({"id": ["5"]})
        self.assertEqual(code, 200)
        self.assertIn("успешно удалена", html)

    def test_handle_currency_delete_not_found(self):
        """Тест валюта не найдена при удалении."""
        self.mock_currency_ctrl.delete_currency.return_value = False
        html, code = self.page_ctrl.handle_currency_delete({"id": ["999"]})
        self.assertEqual(code, 404)
        self.assertIn("не найдена", html)

    def test_handle_currency_update_with_value(self):
        """Тест обновление курса с явным значением."""
        html, code = self.page_ctrl.handle_currency_update({"USD": ["100.5"]})
        self.assertEqual(code, 200)
        self.assertIn("Курс USD обновлён на 100.5", html)
        self.mock_currency_ctrl.update_currency_value.assert_called_with("USD", 100.5)

    def test_handle_currency_update_invalid_value(self):
        """Тест недопустимое значение курса."""
        html, code = self.page_ctrl.handle_currency_update({"USD": ["abc"]})
        self.assertEqual(code, 400)
        self.assertIn("Неверное значение курса", html)

    def test_handle_currency_show(self):
        """Тест вывод валют в консоль."""
        fake_currencies = [{"id": 1, "char_code": "USD", "name": "Доллар", "value": 90.5, "nominal": 1}]
        self.mock_currency_ctrl.cur_info_all.return_value = fake_currencies

        message, code = self.page_ctrl.handle_currency_show()

        self.assertEqual(code, 200)
        self.assertEqual(message, "Валюты успешно выведены в консоль")
        self.mock_currency_ctrl.cur_info_all.assert_called_once()


if __name__ == '__main__':
    unittest.main()