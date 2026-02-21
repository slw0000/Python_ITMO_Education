from controllers.databasecontroller import SubscriptionCRUD

class SubscriptionController:
    def __init__(self, db_controller: SubscriptionCRUD):
        self.db = db_controller

    def create_sub(self, us_id, cur_id):
        self.db._create(us_id, cur_id)

    def all_subs(self):
        return self.db.read_all()

    def vals_by_us(self, us_id):
        return self.db.read_by_user_id(us_id)

    def user_by_val(self, cur_id):
        return self.db.read_by_currency_id(cur_id)

    def del_by_id(self, id):
        return self.db.delete_by_id(id)

    def del_by_us(self, us_id):
        return self.db.delete_all_by_user_id(us_id)

    def del_by_val(self, cur_id):
        return self.db.delete_all_by_currency_id(cur_id)

    def delete_table(self):
        self.db.__del__()