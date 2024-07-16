import sqlite3
import os

# delete existing database if exists

if os.path.exists('database.db'):
    os.remove('database.db')

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    password TEXT
                )''')

# Create files table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    filename TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created successfully")