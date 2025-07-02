from models.reports_model import ReportsModel

class ReportsController:
    def __init__(self):
        self.model = ReportsModel()

    def get_registered_today(self):
        return self.model.get_registered_today()

    def get_paid_today(self):
        return self.model.get_paid_today()

    def get_attended_today(self):
        return self.model.get_attended_today()

    def get_monthly_financials(self, month):
        return self.model.get_monthly_financials(month)

    def get_missing_payments(self):
        return self.model.get_missing_payments()

    def export_to_pdf(self, data, filename):
        return self.model.export_to_pdf(data, filename)

    def export_to_excel(self, data, filename):
        return self.model.export_to_excel(data, filename) 