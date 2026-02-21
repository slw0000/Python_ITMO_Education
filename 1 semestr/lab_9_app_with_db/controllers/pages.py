from jinja2 import Environment
from models import Author, App
from controllers.currencycontroller import CurrencyController
from controllers.usercontroller import UserController
from controllers.subscriptioncontroller import SubscriptionController


class PageController:
    def __init__(
        self,
        env: Environment,
        author: Author,
        app: App,
        currency_controller: CurrencyController,
        user_controller: UserController,
        subscription_controller: SubscriptionController
    ):
        self.env = env
        self.author = author
        self.app = app
        self.cr_controller = currency_controller
        self.us_controller = user_controller
        self.sub_controller = subscription_controller

        # Предзагрузка шаблонов
        self.main_page = self.env.get_template("main.html")
        self.users_page = self.env.get_template("users.html")
        self.user_info_page = self.env.get_template("user_info.html")
        self.currencies_page = self.env.get_template("currencies.html")
        self.author_page = self.env.get_template("author.html")

        # Рендер главной и авторской страниц
        self.main_html = self.main_page.render(
            title='Главная страница',
            myapp=self.app.name,
            version=self.app.version,
            author=self.app.author,
            navigation=[
                {'name': 'Список пользователей', 'link': '/users'},
                {'name': 'Списки валют', 'link': '/currencies'},
                {'name': 'Об авторе', 'link': '/author'}
            ]
        )
        self.author_html = self.author_page.render(
            title='Об авторе',
            version=self.app.version,
            author=self.app.author,
            group=self.author.group
        )

    def render_main(self):
        """Отрисовка главной страницы"""
        return self.main_html

    def render_author(self):
        """Отрисовка страницы автора"""
        return self.author_html

    def render_users(self):
        """Отрисовка страницы пользователей"""
        return self.users_page.render(
            title='Список пользователей',
            author=self.author.name,
            version=self.app.version,
            navigation=self.us_controller.user_info_all()
        )

    def render_currencies(self):
        """Отрисовка страницы со всеми валютами"""
        return self.currencies_page.render(
            title='Список валют',
            author=self.author.name,
            version=self.app.version,
            all_vals=self.cr_controller.cur_info_all()
        )

    def render_user_info(self, query: dict):
        """Отрисовка и обработка маршрута для персональной страницы пользователя"""
        user_id = query.get('id', [None])[0]
        # Проверяем корректность id
        if not user_id or user_id == '':
            return """<h2>Ошибка: укажите id</h2>
            <p><a href="/">Вернуться на главную</a></p>""", 400
        try:
            user_id = int(user_id)
        except ValueError:
            return """<h2>ID должен быть числом</h2>
            <p><a href="/">Вернуться на главную</a></p>""", 400

        cur_user = self.us_controller.user_info(user_id)
        sub = self.sub_controller.vals_by_us(user_id)
        cur_sub = [self.cr_controller.cur_info_by_id(id['currency_id'])['name'] for id in sub]
        vals = [self.cr_controller.cur_info_by_id(id['currency_id']) for id in sub]

        if cur_sub == []:
            cur_sub = 'Подписки отсутвуют.'
        if cur_user == {}:
            return f"""<h2>Пользователь с ID={user_id} не найден</h2>
            <p><a href="/">Вернуться на главную</a></p>""", 404

        user_info = self.user_info_page.render(title='Информация о пользователе',
                                          author=self.author.name,
                                          version=self.app.version,
                                          user_id=user_id,
                                          user_name=cur_user['name'],
                                          sub_vals=cur_sub,
                                          all_vals=vals
                                          )
        return user_info, 200


    def handle_currency_delete(self, query: dict):
        """Обработка маршрута для удаления валюты по id"""
        id_str = query.get('id', [None])[0]
        if not id_str:
            return """<h2>Ошибка: укажите параметр id
            <p><a href="/">Вернуться на главную</a></p>""", 400

        try:
            currency_id = int(id_str)
            success = self.cr_controller.delete_currency(currency_id)
            if success:
                return f"""<h2>Валюта с ID={currency_id} успешно удалена</h2>
                <p><a href="/">Вернуться на главную</a></p>""", 200
            else:
                return f"""<h2>Валюта с ID={currency_id} не найдена</h2>
                <p><a href="/">Вернуться на главную</a></p>""", 404
        except ValueError:
            return """<h2>Ошибка: id должен быть целым числом</h2>
            <p><a href="/">Вернуться на главную</a></p>""", 400

    def handle_currency_update(self, query: dict):
        """Обработка маршрута для обновления курса валюты"""
        param_name = None
        new_value = None

        for key in query:
            if key != 'id':
                param_name = key.upper()
                try:
                    new_value = query[key][0]
                    break
                except ValueError:
                    continue

        if not param_name:
            return """<h2>Ошибка: укажите код валюты (три латинские буквы)</h2>
            <p><a href="/">Вернуться на главную</a></p>""", 400

        try:
            if param_name != 'VAL':
                try:
                    new_value = float(new_value)
                except ValueError:
                    return """<h2>Неверное значение курса валюты</h2>
                    <p><a href="/">Вернуться на главную</a></p>""", 400
                self.cr_controller.update_currency_value(param_name, new_value)
                return f"""<h2>Курс {param_name} обновлён на {new_value}</h2>
                <p><a href="/">Вернуться на главную</a></p>""", 200

            elif param_name == 'VAL':
                self.cr_controller.update_currency(new_value)
                return f"""<h2>Курс {new_value} обновлён на актуальный</h2>
                <p><a href="/">Вернуться на главную</a></p>""", 200
        except ValueError as e:
            return f"""<h2>Ошибка: {e}</h2>
            <p><a href="/">Вернуться на главную</a></p>""", 400

    def handle_currency_show(self):
        """Обработка маршрута для вывода курсов всех валют в консоль"""
        currencies = self.cr_controller.cur_info_all()
        output = ""
        for cur in currencies:
            output += f"ID={cur['id']}, Code={cur['char_code']}, Name={cur['name']}, Value={cur['value']}, Nominal={cur['nominal']}\n"
        print("Все валюты в базе данных:\n")
        print(output)
        return f"Валюты успешно выведены в консоль", 200