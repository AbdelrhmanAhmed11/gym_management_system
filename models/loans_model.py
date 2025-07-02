from models.db_manager import DBManager

class LoansModel:
    def __init__(self):
        self.db = DBManager()

    def add_loan(self, client_id, amount, description):
        return self.db.execute(
            "INSERT INTO loans (client_id, amount, description) VALUES (?, ?, ?)",
            (client_id, amount, description)
        )

    def get_by_client(self, client_id):
        return self.db.fetchall(
            "SELECT * FROM loans WHERE client_id = ?",
            (client_id,)
        )

    def get_all(self):
        return self.db.fetchall("SELECT * FROM loans")

    def get_running_balance(self, client_id):
        result = self.db.fetchone(
            "SELECT SUM(amount) FROM loans WHERE client_id = ?",
            (client_id,)
        )
        return result[0] if result else 0 