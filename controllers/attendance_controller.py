from models.attendance_model import AttendanceModel

class AttendanceController:
    def __init__(self):
        self.model = AttendanceModel()

    def log_checkin(self, client_id, user_id):
        return self.model.log_checkin(client_id, user_id)

    def get_by_date(self, date):
        return self.model.get_by_date(date)

    def get_by_client(self, client_id):
        return self.model.get_by_client(client_id) 