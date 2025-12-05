from decimal import Decimal
from utilites.get_currency import get_currencies, get_value_info

class Currency():
    """
    Класс для хранения данных и вылютах
    """
    def __init__(self, char_code: str):
        self.char_code: str = char_code

        info = get_value_info(self.char_code)
        self.__id = info['ID']
        self.__num_code = info['NumCode']
        self.__name = info['Name']
        self.__value = Decimal(str(info['Value']))
        self.__nominal = info['Nominal']



    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: str):
        if type(id) is str and len(id) > 0:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании ID валюты')


    @property
    def num_code(self):
        return self.__num_code

    @num_code.setter
    def num_code(self, num_code: int):
        if type(num_code) is int and num_code > 0:
            self.__num_code = num_code
        else:
            raise ValueError('Ошибка при задании цифрового кода валюты')


    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, char_code: str):
        if type(char_code) is str and len(char_code) == 3:
            self.__char_code = char_code.upper()
        else:
            raise ValueError('Ошибка при задании ID валюты')


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени пользователя')


    @property
    def value(self):
        return float(str(self.__value))

    @value.setter
    def value(self, value):
        if type(value) in (float, int) and Decimal(str(value)) > Decimal('0'):
            self.__value = float(str(value))
        else:
            raise ValueError('Ошибка при задании значения курса валюты')


    @property
    def nominal(self):
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: int):
        if type(nominal) is int and nominal > 0:
            self.__nominal = nominal
        else:
            raise ValueError('Ошибка при задании значения номинала валюты')


    def update_value(self):
        """
        Обновляет значение курса валюты
        """
        self.__value = Decimal(str(get_currencies([self.char_code])[self.char_code]))


    def get_full_info(self):
        """
        Возвращает список с полной информацией о валюте
        """
        return self.__id, self.__num_code, self.__char_code, self.__name, float(str(self.__value)), self.__nominal


