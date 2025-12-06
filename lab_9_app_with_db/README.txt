Лабораторная работа №9. CRUD для приложения отслеживания курсов валют c SQLite базой данных

Выполнил: Голубев Артём Дмитриевич
ИСУ: 502712
Группа: Р3124


ДЛЯ ЗАПУСКА ПРИЛОЖЕНИЯ ЗАПУСТИТЬ myapp.py и перейти в http://localhost:8080
ДЛЯ ЗАПУСКА ТЕСТОВ ЗАПУСТИТЬ main_test.py


Задание:
Цель работы
Реализовать CRUD (Create, Read, Update, Delete) для сущностей бизнес-логики приложения.
Освоить работу с SQLite в памяти (:memory:) через модуль sqlite3.
Понять принципы первичных и внешних ключей и их роль в связях между таблицами.
Выделить контроллеры для работы с БД и для рендеринга страниц в отдельные модули.
Использовать архитектуру MVC и соблюдать разделение ответственности.
Отображать пользователям таблицу с валютами, на которые они подписаны.
Реализовать полноценный роутер, который обрабатывает GET-запросы и выполняет сохранение/обновление данных и рендеринг страниц.
Научиться тестировать функционал на примере сущностей currency и user с использованием unittest.mock.
1. Основные задачи
CRUD для Currency
Create — добавление новых валют в базу данных.
Read — вывод валют из базы данных.
Update — обновление значения курса валюты.
Delete — удаление валюты по id.
Все действия должны использовать параметризованные запросы для защиты от SQL-инъекций.
Работа с SQLite
Использовать базу в памяти (sqlite3.connect(':memory:')).
Объяснить, для чего нужны первичные ключи (PRIMARY KEY) и внешние ключи (FOREIGN KEY).
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_code TEXT NOT NULL,
    char_code TEXT NOT NULL,
    name TEXT NOT NULL,
    value FLOAT,
    nominal INTEGER
);

CREATE TABLE user_currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    currency_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(currency_id) REFERENCES currency(id)
);
2. Контроллеры и MVC
Пример разбиения для Currency

Model (models/currency.py)

class Currency:
    def __init__(self, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.__num_code = num_code
        self.__char_code = char_code
        self.__name = name
        self.__value = value
        self.__nominal = nominal

    @property
    def num_code(self):
        return self.__num_code

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, val: str):
        if len(val) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self.__char_code = val.upper()

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val: float):
        if val < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        self.__value = val

    @property
    def nominal(self):
        return self.__nominal
Controller (controllers/currencycontroller.py)

from controllers.databasecontroller import CurrencyRatesCRUD
from models.currency import Currency

class CurrencyController:
    def __init__(self, db_controller: CurrencyRatesCRUD):
        self.db = db_controller

    def list_currencies(self):
        return self.db._read()

    def update_currency(self, char_code: str, value: float):
        self.db._update({char_code: value})

    def delete_currency(self, currency_id: int):
        self.db._delete(currency_id)
View (Jinja2, templates/currencies.html)

<h2>Валюты</h2>
<table id="currencies" class="table table-striped">
<tr>
<th>ID</th><th>NumCode</th><th>CharCode</th><th>Name</th><th>Value</th><th>Nominal</th><th>Действия</th>
</tr>
{% for item in currencies %}
  <tr>
    <td>{{ item.id }}</td>
    <td>{{ item.num_code }}</td>
    <td>{{ item.char_code }}</td>
    <td>{{ item.name }}</td>
    <td>{{ item.value }}</td>
    <td>{{ item.nominal }}</td>
    <td><a href="/currency/delete?id={{item.id}}">Удалить</a></td>
  </tr>
{% endfor %}
</table>
3. Маршруты приложения и шаблоны
Маршрут	Описание	Шаблон
/	Главная страница, вывод информации об авторе и список валют	index.html
/author	Информация об авторе	author.html
/users	Список пользователей	users.html
/user?id=...	Просмотр одного пользователя	user.html
/currencies	Список всех валют	currencies.html
/currency/delete?id=...	Удаление валюты	—
/currency/update?USD=...	Обновление курса валюты	—
/currency/show	Вывод валют в консоль (для отладки)	—
4. Пример работы с БД
Создание записей с именованными параметрами

data = [
    {"num_code": "840", "char_code": "USD", "name": "Доллар США", "value": 90.0, "nominal": 1},
    {"num_code": "978", "char_code": "EUR", "name": "Евро", "value": 91.0, "nominal": 1}
]

sql = "INSERT INTO currency(num_code, char_code, name, value, nominal) VALUES(:num_code, :char_code, :name, :value, :nominal)"
cursor.executemany(sql, data)
conn.commit()
Параметризованный SELECT

char_code = "USD"
sql = "SELECT * FROM currency WHERE char_code = ?"
cursor.execute(sql, (char_code,))
result = cursor.fetchall()
5. Пример тестирования с unittest.mock
import unittest
from unittest.mock import MagicMock
from controllers.currencycontroller import CurrencyController

class TestCurrencyController(unittest.TestCase):
    def test_list_currencies(self):
        mock_db = MagicMock()
        mock_db._read.return_value = [{"id":1, "char_code":"USD", "value":90}]
        controller = CurrencyController(mock_db)
        result = controller.list_currencies()
        self.assertEqual(result[0]['char_code'], "USD")
        mock_db._read.assert_called_once()
6. Рекомендации по MVC и разделению кода
Models — только свойства сущностей, геттеры и сеттеры.
Controllers — отдельные модули:
databasecontroller.py — работа с SQLite
currencycontroller.py — бизнес-логика
pages.py — рендеринг страниц через Jinja2
Views — HTML-шаблоны в папке templates/.
Главный файл (myapp.py) — инициализация сервера, создание контроллеров, маршрутизация через do_GET.
Для Jinja2 объект Environment создаётся в главном файле приложения для повторного использования всеми контроллерами и рендерингом страниц.
7. Требования к отчету
Цель работы.
Описание моделей, их свойств и связей.
Структура проекта с назначением файлов.
Реализацию CRUD с примерами SQL-запросов.
Скриншоты работы приложения (главная страница, таблица валют, обновление и удаление).
Примеры тестов с unittest.mock и результаты их выполнения.
Выводы о применении MVC, работе с SQLite, обработке маршрутов и рендеринге шаблонов.


