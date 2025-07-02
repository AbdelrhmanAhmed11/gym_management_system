from models.db_manager import DBManager
import hashlib

class UserModel:
    def __init__(self):
        self.db = DBManager()

    def get_all(self):
        return self.db.fetchall("SELECT id, username, role, full_name FROM users")

    def add_user(self, username, password, role, full_name):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.db.execute(
            "INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
            (username, password_hash, role, full_name)
        )

    def remove_user(self, user_id):
        return self.db.execute("DELETE FROM users WHERE id=?", (user_id,))

    def change_password(self, user_id, new_password):
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        return self.db.execute("UPDATE users SET password_hash=? WHERE id=?", (password_hash, user_id))

    def get_by_username(self, username):
        return self.db.fetchone("SELECT id, username, role, full_name FROM users WHERE username=?", (username,))

    def get_by_id(self, user_id):
        return self.db.fetchone("SELECT id, username, role, full_name FROM users WHERE id=?", (user_id,)) 