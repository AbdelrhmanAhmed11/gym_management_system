from models.session_model import SessionModel

class SessionController:
    def __init__(self):
        self.model = SessionModel()

    def add_session(self, client_id, trainer_name, session_date, session_type, is_group):
        return self.model.add_session(client_id, trainer_name, session_date, session_type, is_group)

    def get_by_trainer(self, trainer_name):
        return self.model.get_by_trainer(trainer_name)

    def get_by_client(self, client_id):
        return self.model.get_by_client(client_id)

    def get_all(self):
        return self.model.get_all() 