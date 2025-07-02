import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'gym_management.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

SAMPLE_USERS = [
    ("admin", "admin123", "admin", "Gym Owner"),
    ("reception", "recept123", "receptionist", "Front Desk")
]

def hash_password(password):
    # Simple hash for demo; use bcrypt in production
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        # Insert sample users
        for username, password, role, full_name in SAMPLE_USERS:
            conn.execute(
                "INSERT OR IGNORE INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
                (username, hash_password(password), role, full_name)
            )
        conn.commit()
    print('Database initialized and sample users added.')

if __name__ == '__main__':
    main() 