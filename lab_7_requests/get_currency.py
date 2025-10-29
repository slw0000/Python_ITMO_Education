import requests
import sys

def get_currencies(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js", handle=sys.stdout)->dict:
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).
        url (str): Get запрос для получения курса валют (по умол. https://www.cbr-xml-daily.ru/daily_json.js).
        handle: Определеят поток для вывода ошибки.


    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.
              Возвращает None в случае ошибки запроса.
    """

    try:

        response = requests.get(url)

        response.raise_for_status()
        data = response.json()
        currencies = {}

        if "Valute" in data:
            for code in currency_codes:
                if code in data["Valute"]:
                    currencies[code] = data["Valute"][code]["Value"]
                else:
                    currencies[code] = f"Код валюты '{code}' не найден."
        return currencies

    except requests.exceptions.RequestException as e:
        f = open('logger/errors.log', 'w')
        f.write(str(e))
        f.close()


        handle.write(f"Ошибка при запросе к API: {e}")
        raise requests.exceptions.RequestException('Упали с исключением')


# Пример использования функции:
# currency_list = ['USD', 'EUR', 'GBP', 'NNZ']

# currency_data = get_currencies(currency_list)
# if currency_data:
     # print(currency_data)