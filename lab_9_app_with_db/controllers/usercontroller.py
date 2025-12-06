from controllers.databasecontroller import UserCRUD

class UserController:
    def __init__(self, db_controller: UserCRUD):
        self.db = db_controller

    def create_user(self, user_obj):
        self.db._create(user_obj)

    def user_info(self, id: int):
        return self.db._read(id)

    def user_info_all(self):
        return self.db._read_all()

    def update_user_info(self, id: int, name: str):
        self.db._update(id, name)

    def delete_user(self, id: int):
        self.db._delete(id)

    def delete_table(self):
        self.db.__del__()


