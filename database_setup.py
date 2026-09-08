import sqlite3
from werkzeug.security import generate_password_hash
import os

def setup_db():
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # Default users from original app
    default_users = {
        "AnkithaRashmiReddy": "Reddy@123",
        "PawanSimhaR": "Simha@123",
        "AsraFathima": "Asra@123"
    }

    for username, password in default_users.items():
        hashed_pw = generate_password_hash(password)
        try:
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_pw))
            print(f"User '{username}' created successfully.")
        except sqlite3.IntegrityError:
            print(f"User '{username}' already exists.")

    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == '__main__':
    setup_db()
