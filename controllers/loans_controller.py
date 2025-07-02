from models.loans_model import LoansModel

class LoansController:
    def __init__(self):
        self.model = LoansModel()

    def add_loan(self, client_id, amount, description):
        return self.model.add_loan(client_id, amount, description)

    def get_by_client(self, client_id):
        return self.model.get_by_client(client_id)

    def get_all(self):
        return self.model.get_all()

    def get_running_balance(self, client_id):
        return self.model.get_running_balance(client_id) 