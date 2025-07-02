from models.client_model import ClientModel

class ClientsController:
    def __init__(self):
        self.model = ClientModel()

    def load_all(self):
        return self.model.get_all()

    def search(self, keyword):
        return self.model.search(keyword)

    def add(self, data):
        return self.model.add(data)

    def update(self, client_code, data):
        return self.model.update(client_code, data)

    def delete(self, client_code):
        return self.model.delete(client_code) 