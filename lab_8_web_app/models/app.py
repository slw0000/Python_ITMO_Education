class App():
    """
    Класс, содержащий основную информацию об приложении
    """
    def __init__(self, name: str, version: str, author: str):
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании названия приложения')

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version: str):
        if type(version) is str and len(version) >= 3 and '.' in version:
            self.__version = version
        else:
            raise ValueError('Ошибка при задании версии приложения')


    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author: str):
        if type(author) is str and len(author) >= 2:
            self.__author = author
        else:
            raise ValueError('Ошибка при задании Автора приложения')