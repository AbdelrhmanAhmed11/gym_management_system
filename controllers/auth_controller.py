from models.db_manager import DBManager
import hashlib

class AuthController:
    def __init__(self):
        self.db = DBManager()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password, role):
        hashed = self.hash_password(password)
        user = self.db.fetchone(
            "SELECT id, username, role FROM users WHERE username=? AND password_hash=? AND role=?",
            (username, hashed, role)
        )
        return user 