from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from models import Author, User, Currency, Subscriptions, App


# Инициализация объектов класса
main_author = Author('Artem Golubev', 'P3124')
app_info = App('CurrenciesListApp', 'v0.1', main_author.name)
user_1 = User(1, 'Ivan Ivanov')
user_2 = User(2, 'Vladimir Putin')
user_3 = User(3, 'Cristiano Ronaldo')
cur_1 = Currency('USD')
cur_2 = Currency('EUR')
cur_3 = Currency('GBP')
sub_1 = Subscriptions(1, 1, ['USD', 'EUR'])
sub_2 = Subscriptions(2, 2, ['EUR', 'GBP'])

all_users = [user_1, user_2, user_3]
all_cur = [cur_1, cur_2, cur_3]
all_sub = [sub_1, sub_2]



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Обрабатывает GET-запросы, обрабатывает маршрутизацию веб-приложения
        """
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == '/':
            global main
            self.send_html(main)
        elif path == '/users':
            users = users_page.render(title='Список пользователей', author=main_author.name,
                                      version=app_info.version, navigation=all_users)
            self.send_html(users)
        elif path == '/user':
            self.send_user_html(query)
        elif path == '/currencies':
            for i in all_cur:
                i.update_value()
            currencies = currencies_page.render(title='Список валют', author=main_author.name,
                                      version=app_info.version, all_vals=all_cur)
            self.send_html(currencies)
        elif path == '/author':
            global author
            self.send_html(author)
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.send_html("Страница не найдена! 404", 404)


    def send_user_html(self, query: dict):
        global user_info_page
        try:
            if 'id' not in query:
                raise ValueError('Ошибка! Неверное указано значение id')
            id = int(query['id'][0])
            if id == '':
                raise ValueError('Ошибка! Неверное указано значение id')
        except:
            self.send_html('Ошибка! Неверное указано значение id!', 404)
            return

        cur_user = None
        cur_sub = None
        vals = []
        for i in all_users:
            if i.id == id: cur_user = i
        if cur_user is None:
            self.send_html(f'Ошибка! Пользователь не найден при id={id}!', 404)
            return

        for i in all_sub:
            if i.id == id: cur_sub = i
        if cur_sub is None:
            self.send_html(f'Ошибка! '
                           f''
                           f''
                           f'Подписки не найдены при id={id}!', 404)
            return

        for i in all_cur:
            if i.char_code in cur_sub.currency_id:
                vals.append(i.get_full_info())
        if vals == []:
            self.send_html(f'Отсутствуют валюты из подписки при id={id}!', 404)
            return

        user_info = user_info_page.render(title='Информация о пользователе',
                                          author=main_author.name,
                                          version=app_info.version,
                                          user_id=id,
                                          user_name=cur_user.name,
                                          sub_id=cur_sub.id,
                                          sub_vals=cur_sub.currency_id,
                                          all_vals=vals
                                          )
        self.send_html(user_info)


    def send_html(self, result: str, code: int = 200):
        """
        Отображает страницу приложения и отправляет код запроса
        """
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(result, "utf-8"))


# Инициализация окружения
env = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape())

# Инициализация шаблонов
main_page = env.get_template("main.html")
users_page = env.get_template("users.html")
user_info_page = env.get_template("user_info.html")
currencies_page = env.get_template("currencies.html")
author_page = env.get_template("author.html")



main = main_page.render(title='Главная страница', myapp=app_info.name,
                        version=app_info.version, author=app_info.author,
                        navigation=[{'name': 'Список пользователей', 'link': '/users'},
                                    {'name': 'Список валют', 'link': '/currencies'},
                                    {'name': 'Об авторе', 'link': '/author'}])

author = author_page.render(title='Об авторе', version=app_info.version,
                            author=app_info.author, group=main_author.group)


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('server is running')
    httpd.serve_forever()