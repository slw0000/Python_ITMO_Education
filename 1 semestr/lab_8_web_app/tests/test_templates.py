import unittest
from jinja2 import Environment, FileSystemLoader
import os
from models import Author, App, User, Currency, Subscriptions
from utilites.get_currency import get_currencies


class TestTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        cls.env = Environment(loader=FileSystemLoader(template_dir))

    def test_main_template_renders(self):
        """Тест рендера главной страницы"""
        template = self.env.get_template('main.html')
        app = App("CurrenciesListApp", "v0.1", "Artem Golubev")

        result = template.render(
            title='Главная страница',
            myapp=app.name,
            version=app.version,
            author=app.author
        )

        self.assertIn('Главная страница', result)
        self.assertIn('CurrenciesListApp', result)
        self.assertIn('v0.1', result)
        self.assertIn('Artem Golubev', result)

    def test_author_template_renders(self):
        """Тест рендера страницы автора"""
        template = self.env.get_template('author.html')
        author = Author("Artem Golubev", "P3124")
        app = App("CurrenciesListApp", "v0.1", author.name)

        result = template.render(
            title='Об авторе',
            version=app.version,
            author=app.author,
            group=author.group
        )

        self.assertIn('Об авторе', result)
        self.assertIn('v0.1', result)
        self.assertIn('Artem Golubev', result)
        self.assertIn('P3124', result)

    def test_users_template_renders(self):
        """тест рендера станицы с пользователями"""
        template = self.env.get_template('users.html')
        users = [
            User(1, 'Ivan Ivanov'),
            User(2, 'Artem Artemov')
        ]
        author = Author("Artem Golubev", "P3124")
        app = App("CurrenciesListApp", "v0.1", author.name)

        result = template.render(
            title='Список пользователей',
            author=app.author,
            version=app.version,
            navigation=users
        )

        self.assertIn('Список пользователей', result)
        self.assertIn('Ivan Ivanov', result)
        self.assertIn('Artem Artemov', result)
        self.assertGreater(result.count('<li>'), 0)

    def test_currencies_template_renders(self):
        """Тест рендера страницы с валютами"""
        template = self.env.get_template('currencies.html')
        currencies = [
            Currency('USD'),
            Currency('EUR'),
            Currency('GBP')
        ]
        author = Author("Artem Golubev", "P3124")
        app = App("CurrenciesListApp", "v0.1", author.name)

        result = template.render(
            title='Список валют',
            author=app.author,
            version=app.version,
            all_vals=currencies
        )

        self.assertIn('Список валют', result)
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertIn('GBP', result)
        self.assertIn('Доллар', result)
        self.assertIn(str(get_currencies(['USD'])['USD']), result)

    def test_user_info_template_renders(self):
        """Тест рендера страницы с информацией о пользователе"""
        template = self.env.get_template('user_info.html')
        user = User(1, 'Ivan Ivanov')
        subscription = Subscriptions(1, 1, ['USD', 'EUR'])
        currencies = [
            Currency('USD'),
            Currency('EUR')
        ]
        author = Author("Artem Golubev", "P3124")
        app = App("CurrenciesListApp", "v0.1", author.name)

        vals = []
        for cur in currencies:
            if cur.char_code in subscription.currency_id:
                vals.append(cur.get_full_info())

        result = template.render(title='Информация о пользователе',
                                          author=author.name,
                                          version=app.version,
                                          user_id=user.id,
                                          user_name=user.name,
                                          sub_id=subscription.id,
                                          sub_vals=subscription.currency_id,
                                          all_vals=vals
                                          )

        self.assertIn('Информация о пользователе', result)
        self.assertIn('Ivan Ivanov', result)
        self.assertIn('USD', result)
        self.assertIn('EUR', result)
        self.assertIn(str(get_currencies(['USD'])['USD']), result)



if __name__ == '__main__':
    unittest.main()