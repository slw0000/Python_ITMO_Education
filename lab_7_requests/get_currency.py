import requests
from logger.logger import logger
import logging
import io


# Инициализация логгера
logging.basicConfig(
    filename="logger/get_currencies.log",
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s",
    filemode='w'
)
log = logging.getLogger('currency')

# Инициализация нестаднартного потока вывода (в моём случае StringIO)
nonStandartStream = io.StringIO()


# @logger(handle=nonStandartStream)
#@logger
@logger(handle=log)
def get_currencies(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js")->dict:
    """
    Получает курсы валют с API Центробанка России.
    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).
        url (str): Get запрос для получения курса валют (по умол. https://www.cbr-xml-daily.ru/daily_json.js).
    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    currencies = {}

    if "Valute" in data:
        for code in currency_codes:
            if code in data["Valute"]:
                currencies[code] = data["Valute"][code]["Value"]
                if not isinstance(currencies[code], (int, float)):
                    raise TypeError("Курс валюты имеет неверный тип")
            else:
                currencies[code] = f"Код валюты '{code}' не найден."

    return currencies


