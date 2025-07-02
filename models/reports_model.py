from models.db_manager import DBManager

class ReportsModel:
    def __init__(self):
        self.db = DBManager()

    def get_registered_today(self):
        return self.db.fetchall("SELECT * FROM clients WHERE DATE(created_at) = DATE('now')")

    def get_paid_today(self):
        return self.db.fetchall("SELECT * FROM finances WHERE category = 'payment' AND DATE(created_at) = DATE('now')")

    def get_attended_today(self):
        return self.db.fetchall("SELECT * FROM attendance WHERE DATE(checkin_time) = DATE('now')")

    def get_monthly_financials(self, month):
        return self.db.fetchall("SELECT * FROM finances WHERE strftime('%Y-%m', created_at) = ?", (month,))

    def get_missing_payments(self):
        return self.db.fetchall("SELECT * FROM clients WHERE amount_remaining > 0 AND end_date >= DATE('now')")

    def export_to_pdf(self, data, filename):
        # Stub for PDF export
        pass

    def export_to_excel(self, data, filename):
        # Stub for Excel export
        pass 