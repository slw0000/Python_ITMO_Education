class Subscriptions():
    """
    Класс для хранения информации о подписках пользователей на валюты
    """
    def __init__(self, id: int, user_id: int, currency_id: list):
        self.id: int = id
        self.user_id: int = user_id
        self.currency_id: list = currency_id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        if type(id) is int and id > 0:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании ID подписки')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int):
        if type(user_id) is int and user_id > 0:
            self.__user_id = user_id
        else:
            raise ValueError('Ошибка при задании ID пользователя')

    @property
    def currency_id(self):
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, currency_id: list):
        if (type(currency_id) is list and len(currency_id) > 0
                and all(isinstance(x, str) for x in currency_id)):
            self.__currency_id = currency_id
        else:
            raise ValueError('Ошибка при задании внешнего ключа к Currency')


