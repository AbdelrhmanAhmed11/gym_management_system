from models.user_model import UserModel

class UserController:
    def __init__(self):
        self.model = UserModel()

    def get_all(self):
        return self.model.get_all()

    def add_user(self, username, password, role, full_name):
        return self.model.add_user(username, password, role, full_name)

    def remove_user(self, user_id):
        return self.model.remove_user(user_id)

    def change_password(self, user_id, new_password):
        return self.model.change_password(user_id, new_password)

    def get_by_username(self, username):
        return self.model.get_by_username(username)

    def get_by_id(self, user_id):
        return self.model.get_by_id(user_id) 