from models.db_manager import DBManager

class SessionModel:
    def __init__(self):
        self.db = DBManager()

    def add_session(self, client_id, trainer_name, session_date, session_type, is_group):
        return self.db.execute(
            "INSERT INTO private_sessions (client_id, trainer_name, session_date, session_type, is_group) VALUES (?, ?, ?, ?, ?)",
            (client_id, trainer_name, session_date, session_type, is_group)
        )

    def get_by_trainer(self, trainer_name):
        return self.db.fetchall(
            "SELECT * FROM private_sessions WHERE trainer_name = ?",
            (trainer_name,)
        )

    def get_by_client(self, client_id):
        return self.db.fetchall(
            "SELECT * FROM private_sessions WHERE client_id = ?",
            (client_id,)
        )

    def get_all(self):
        return self.db.fetchall("SELECT * FROM private_sessions") 