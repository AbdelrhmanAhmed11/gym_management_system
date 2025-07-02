import sqlite3
import os

class DBManager:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), '../db/gym_management.db')
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    def fetchone(self, query, params=()):
        with self.connect() as conn:
            cur = conn.execute(query, params)
            return cur.fetchone()

    def fetchall(self, query, params=()):
        with self.connect() as conn:
            cur = conn.execute(query, params)
            return cur.fetchall()

    def execute(self, query, params=()):
        with self.connect() as conn:
            cur = conn.execute(query, params)
            conn.commit()
            return cur.lastrowid 