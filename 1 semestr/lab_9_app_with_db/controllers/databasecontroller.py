import sqlite3
from utilites.get_currency import get_currencies


class CurrencyRatesCRUD():
    def __init__(self):
        self.__con = sqlite3.connect(':memory:')
        self.__cursor = self.__con.cursor()
        self.__createtable()

    def __createtable(self) -> None:
        self.__con.execute("""
            CREATE TABLE IF NOT EXISTS currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code INTEGER NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER
            )
        """)
        self.__con.commit()

    def _create(self, currency_rates_obj) -> None:
        """Добавление новой валюты"""
        __params = currency_rates_obj.get_full_info()[1:]
        __sqlquery = "INSERT INTO currency(num_code, char_code, name, value, nominal) VALUES (?, ?, ?, ?, ?)"

        self.__cursor.execute(__sqlquery, __params)
        self.__con.commit()

    def _read(self, char_code: str) -> dict:
        """Вывод ифнормации о валюте"""
        self.__cursor.execute(
            "SELECT id, num_code, char_code, name, value, nominal FROM currency WHERE char_code = ?",
            (char_code.upper(),)
        )
        _row = self.__cursor.fetchone()
        result_data = {}
        if _row:
            result_data = {'id': int(_row[0]), 'cur': _row[1], 'date': _row[2], 'value': float(_row[3])}

        return result_data

    def _read_by_id(self, id: int) -> dict:
        """Вывод информации о валюте через id"""
        self.__cursor.execute(
            "SELECT id, num_code, char_code, name, value, nominal FROM currency WHERE id = ?",
            (id,)
        )
        _row = self.__cursor.fetchone()
        result_data = {}
        if _row:
            result_data = {'id': int(_row[0]), 'num_code': _row[1], 'char_code': _row[2], 'name': _row[3], 'value': float(_row[4]), 'nominal': int(_row[5])}

        return result_data

    def _read_all(self) -> list:
        """Возвращает все валюты"""
        self.__cursor.execute("SELECT id, num_code, char_code, name, value, nominal FROM currency")
        rows = self.__cursor.fetchall()
        return [
            {
                "id": row[0],
                "num_code": row[1],
                "char_code": row[2],
                "name": row[3],
                "value": float(row[4]),
                "nominal": row[5],
            } for row in rows
        ]

    def _update(self, char_code: str) -> None:
        """Обновляет курс валюты на актуальное"""
        fresh_rates = get_currencies([char_code])
        new_value = fresh_rates[char_code]

        self.__cursor.execute(
            "UPDATE currency SET value = ? WHERE char_code = ?",
            (new_value, char_code.upper())
        )
        self.__con.commit()

    def _update_by_char_code(self, char_code: str, value: float) -> None:
        """Обновляет курс валюты на заданное число"""
        self.__cursor.execute(
            "UPDATE currency SET value = ? WHERE char_code = ?",
            (value, char_code.upper())
        )
        self.__con.commit()

    def _delete(self, currency_id: int) -> None:
        """Удаляет валюту"""
        self.__cursor.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self.__con.commit()

    def __del__(self) -> None:
        self.__cursor = None
        self.__con.close()

class UserCRUD():
    def __init__(self):
        self.__con = sqlite3.connect(':memory:')
        self.__cursor = self.__con.cursor()
        self.__createtable()

    def __createtable(self) -> None:
        self.__con.execute("""
            CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
        )
        """)
        self.__con.commit()

    def _create(self, user_obj) -> None:
        """Добавление нового пользователя"""
        __params = (user_obj.name,)
        __sqlquery = "INSERT INTO user(name) VALUES (?)"

        self.__cursor.execute(__sqlquery, __params)
        self.__con.commit()

    def _read(self, id: int) -> dict:
        """Вывод информации о пользователе"""
        self.__cursor.execute(
            "SELECT id, name FROM user WHERE id = ?",
            (id,)
        )
        _row = self.__cursor.fetchone()
        result_data = {}
        if _row:
            result_data = {'id': int(_row[0]), 'name': _row[1]}

        return result_data

    def _read_all(self) -> list:
        """Вывод информации о всех пользователях"""
        self.__cursor.execute("SELECT id, name FROM user")
        rows = self.__cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
            } for row in rows
        ]

    def _update(self, id: int, name: str) -> None:
        """Замена имени пользователя"""
        self.__cursor.execute(
            "UPDATE user SET name = ? WHERE id = ?",
            (name, id)
        )
        self.__con.commit()

    def _delete(self, id: int) -> None:
        """Удаление пользователя"""
        self.__cursor.execute("DELETE FROM currency WHERE id = ?", (id,))
        self.__con.commit()

    def __del__(self) -> None:
        self.__cursor = None
        self.__con.close()

class SubscriptionCRUD():
    def __init__(self):
        self.__con = sqlite3.connect(':memory:')
        self.__cursor = self.__con.cursor()
        self.__createtable()

    def __createtable(self):
        self.__con.execute("""
            CREATE TABLE user_currency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            currency_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES user(id),
            FOREIGN KEY(currency_id) REFERENCES currency(id)
            )
        """)
        self.__con.commit()

    def _create(self, user_id: int, currency_id: int) -> None:
        """Добавление новой подписки"""
        self.__cursor.execute(
            "INSERT INTO user_currency (user_id, currency_id) VALUES (?, ?)",
            (user_id, currency_id)
        )
        self.__con.commit()
        return self.__cursor.lastrowid

    def read_all(self) -> list:
        """Вывод всех подписок"""
        self.__cursor.execute("SELECT id, user_id, currency_id FROM user_currency")
        rows = self.__cursor.fetchall()
        return [
            {
                "id": row[0],
                "user_id": row[1],
                "currency_id": row[2]
            }
            for row in rows
        ]

    def read_by_user_id(self, user_id: int) -> list:
        """Вывод подписки пользователя"""
        self.__cursor.execute(
            "SELECT id, user_id, currency_id FROM user_currency WHERE user_id = ?",
            (user_id,)
        )
        rows = self.__cursor.fetchall()
        return [
            {"id": row[0], "user_id": row[1], "currency_id": row[2]}
            for row in rows
        ]

    def read_by_currency_id(self, currency_id: int) -> list:
        """Вывод пользователей, подписанных на валюту"""
        self.__cursor.execute(
            "SELECT id, user_id, currency_id FROM user_currency WHERE currency_id = ?",
            (currency_id,)
        )
        rows = self.__cursor.fetchall()
        return [
            {"id": row[0], "user_id": row[1], "currency_id": row[2]}
            for row in rows
        ]

    def delete_by_id(self, link_id: int) -> None:
        """Удаляет подписку по её id"""
        self.__cursor.execute("DELETE FROM user_currency WHERE id = ?", (link_id,))
        self.__con.commit()

    def delete_all_by_user_id(self, user_id: int) -> None:
        """Удаляет подписку по id пользователя"""
        self.__cursor.execute("DELETE FROM user_currency WHERE user_id = ?", (user_id,))
        self.__con.commit()

    def delete_all_by_currency_id(self, currency_id: int) -> None:
        """Удаляет все подписки на данную валюту"""
        self.__cursor.execute("DELETE FROM user_currency WHERE currency_id = ?", (currency_id,))
        self.__con.commit()

    def __del__(self) -> None:
        if hasattr(self, '_UserCurrencyCRUD__cursor'):
            self.__cursor.close()