from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from models import Author, User, Currency, Subscriptions, App
from controllers.databasecontroller import CurrencyRatesCRUD, UserCRUD, SubscriptionCRUD
from controllers.currencycontroller import CurrencyController
from controllers.usercontroller import UserController
from controllers.subscriptioncontroller import SubscriptionController
from controllers.pages import PageController


# Инициализация объектов класса
main_author = Author('Artem Golubev', 'P3124')
app_info = App('CurrenciesListApp', 'v0.1', main_author.name)

user_1 = User(1, 'Ivan Ivanov')
user_2 = User(2, 'Vladimir Putin')
user_3 = User(3, 'Cristiano Ronaldo')
cur_1 = Currency('USD')
cur_2 = Currency('EUR')
cur_3 = Currency('GBP')
sub_1 = Subscriptions(1, 1, [1, 2])
sub_2 = Subscriptions(2, 2, [2, 3])

# Подключение бд и контроллеров
db_cur = CurrencyRatesCRUD()
db_user = UserCRUD()
db_sub = SubscriptionCRUD()

cr_controller = CurrencyController(db_cur)
us_controller = UserController(db_user)
sub_controller = SubscriptionController(db_sub)

for i in (cur_1, cur_2, cur_3):
    cr_controller.create_currency(i)
for i in (user_1, user_2, user_3):
    us_controller.create_user(i)
for i in (sub_1, sub_2):
    us_id = i.user_id
    for j in i.currency_id:
        sub_controller.create_sub(us_id, j)

# Инициализация окружения
env = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape())

page_controller = PageController(
    env=env,
    author=main_author,
    app=app_info,
    currency_controller=cr_controller,
    user_controller=us_controller,
    subscription_controller=sub_controller
)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обрабатывает GET-запросы, обрабатывает маршрутизацию веб-приложения"""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == '/':
            content = page_controller.render_main()
            self.send_html(content)
        elif path == '/author':
            content = page_controller.render_author()
            self.send_html(content)
        elif path == '/users':
            content = page_controller.render_users()
            self.send_html(content)
        elif path == '/user':
            content, code = page_controller.render_user_info(query)
            self.send_html(content)
        elif path == '/currencies':
            content = page_controller.render_currencies()
            self.send_html(content)
        elif path == '/currency/delete':
            content, code = page_controller.handle_currency_delete(query)
            self.send_html(content, code)
        elif path == '/currency/update':
            content, code = page_controller.handle_currency_update(query)
            self.send_html(content, code)
        elif path == '/currency/show':
            content, code = page_controller.handle_currency_show()
            self.send_html(content, code)
        else:
            self.send_html("""<h2>Страница не найдена! 404</h2>
                           <p><a href="/">Вернуться на главную</a></p>""", 404)


    def send_html(self, result: str, code: int = 200):
        """Отображает страницу приложения и отправляет код запроса"""
        self.send_response(code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(result, "utf-8"))


if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('server is running')
    httpd.serve_forever()