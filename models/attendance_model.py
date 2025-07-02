from models.db_manager import DBManager

class AttendanceModel:
    def __init__(self):
        self.db = DBManager()

    def log_checkin(self, client_id, user_id):
        return self.db.execute(
            "INSERT INTO attendance (client_id, checked_in_by) VALUES (?, ?)",
            (client_id, user_id)
        )

    def get_by_date(self, date):
        return self.db.fetchall(
            "SELECT a.id, c.client_code, c.name, a.checkin_time FROM attendance a JOIN clients c ON a.client_id = c.id WHERE DATE(a.checkin_time) = ?",
            (date,)
        )

    def get_by_client(self, client_id):
        return self.db.fetchall(
            "SELECT id, checkin_time FROM attendance WHERE client_id = ?",
            (client_id,)
        ) 