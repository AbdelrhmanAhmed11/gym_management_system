from models.db_manager import DBManager

class ClientModel:
    def __init__(self):
        self.db = DBManager()

    def get_all(self):
        return self.db.fetchall("SELECT client_code, name, phone, subscription_type, start_date, end_date FROM clients")

    def search(self, keyword):
        kw = f"%{keyword}%"
        return self.db.fetchall(
            "SELECT client_code, name, phone, subscription_type, start_date, end_date FROM clients WHERE name LIKE ? OR client_code LIKE ? OR phone LIKE ?",
            (kw, kw, kw)
        )

    def add(self, data):
        query = """
        INSERT INTO clients (client_code, name, phone, subscription_type, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.db.execute(query, data)

    def update(self, client_code, data):
        query = """
        UPDATE clients SET name=?, phone=?, subscription_type=?, start_date=?, end_date=? WHERE client_code=?
        """
        return self.db.execute(query, (*data, client_code))

    def delete(self, client_code):
        return self.db.execute("DELETE FROM clients WHERE client_code=?", (client_code,)) 