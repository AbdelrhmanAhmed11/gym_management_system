from models.db_manager import DBManager

class FinanceModel:
    def __init__(self):
        self.db = DBManager()

    def add_payment(self, client_id, amount, description, user_id):
        return self.db.execute(
            "INSERT INTO finances (client_id, category, amount, description, recorded_by) VALUES (?, 'payment', ?, ?, ?)",
            (client_id, amount, description, user_id)
        )

    def add_expense(self, category, amount, description, user_id):
        return self.db.execute(
            "INSERT INTO finances (category, amount, description, recorded_by) VALUES (?, ?, ?, ?)",
            (category, amount, description, user_id)
        )

    def get_payments_by_date(self, date):
        return self.db.fetchall(
            "SELECT f.id, c.client_code, c.name, f.amount, f.description FROM finances f LEFT JOIN clients c ON f.client_id = c.id WHERE f.category = 'payment' AND DATE(f.created_at) = ?",
            (date,)
        )

    def get_expenses_by_date(self, date):
        return self.db.fetchall(
            "SELECT id, category, amount, description FROM finances WHERE category != 'payment' AND DATE(created_at) = ?",
            (date,)
        )

    def get_unmatched_payments(self):
        return self.db.fetchall(
            "SELECT f.id, c.client_code, c.name, f.amount FROM finances f LEFT JOIN clients c ON f.client_id = c.id WHERE f.category = 'payment' AND (f.client_id IS NULL OR f.amount <= 0)")

    def get_daily_payments_by_user(self, user_id, date):
        return self.db.fetchall(
            "SELECT id, amount, description FROM finances WHERE category = 'payment' AND recorded_by = ? AND DATE(created_at) = ?",
            (user_id, date)
        )

    def get_all(self):
        return self.db.fetchall("SELECT * FROM finances") 