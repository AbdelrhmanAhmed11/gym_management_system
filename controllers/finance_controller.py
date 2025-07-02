from models.finance_model import FinanceModel

class FinanceController:
    def __init__(self):
        self.model = FinanceModel()

    def add_payment(self, client_id, amount, description, user_id):
        return self.model.add_payment(client_id, amount, description, user_id)

    def add_expense(self, category, amount, description, user_id):
        return self.model.add_expense(category, amount, description, user_id)

    def get_payments_by_date(self, date):
        return self.model.get_payments_by_date(date)

    def get_expenses_by_date(self, date):
        return self.model.get_expenses_by_date(date)

    def get_unmatched_payments(self):
        return self.model.get_unmatched_payments()

    def get_daily_payments_by_user(self, user_id, date):
        return self.model.get_daily_payments_by_user(user_id, date)

    def get_all(self):
        return self.model.get_all() 