from models.db_manager import DBManager

class InvitationModel:
    def __init__(self):
        self.db = DBManager()

    def add_invitation(self, client_id, friend_name, friend_phone):
        return self.db.execute(
            "INSERT INTO invitations (client_id, friend_name, friend_phone) VALUES (?, ?, ?)",
            (client_id, friend_name, friend_phone)
        )

    def get_by_client(self, client_id):
        return self.db.fetchall(
            "SELECT * FROM invitations WHERE client_id = ?",
            (client_id,)
        )

    def get_all(self):
        return self.db.fetchall("SELECT * FROM invitations")

    def tag_invitation(self, invitation_id, tagged):
        return self.db.execute(
            "UPDATE invitations SET tagged = ? WHERE id = ?",
            (tagged, invitation_id)
        ) 