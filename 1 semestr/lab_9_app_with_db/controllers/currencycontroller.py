from controllers.databasecontroller import CurrencyRatesCRUD

class CurrencyController:
    def __init__(self, db_controller: CurrencyRatesCRUD):
        self.db = db_controller

    def create_currency(self, valute_obj):
        self.db._create(valute_obj)

    def cur_info(self, char_code: str):
        return self.db._read(char_code)

    def cur_info_by_id(self, id: int):
        return self.db._read_by_id(id)

    def cur_info_all(self):
        return self.db._read_all()

    def update_currency(self, char_code: str):
        self.db._update(char_code)

    def update_currency_value(self, char_code: str, new_value: float):
        self.db._update_by_char_code(char_code, new_value)

    def update_all(self):
        for i in self.db._read_all():
            self.update_currency(i['char_code'])

    def delete_currency(self, currency_id: int):
        self.db._delete(currency_id)

    def delete_table(self):
        self.db.__del__()