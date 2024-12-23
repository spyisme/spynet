import sqlite3
import json

# Paths
json_file_path = 'ECU24~23.json'
sqlite_db_path = 'students.db'

# Connect to SQLite
conn = sqlite3.connect(sqlite_db_path)
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT,
        faculty TEXT
    )
''')

# Load JSON data and insert into the database
with open(json_file_path, 'r') as file:
    data = json.load(file)
    for entry in data:
        cursor.execute('''
            INSERT OR IGNORE INTO students (id, name, email, phone, faculty)
            VALUES (?, ?, ?, ?, ?)
        ''', (entry['id'], entry['Name'], entry['Email'], entry['Phone'], entry['Faculty']))

conn.commit()
conn.close()

print("Database setup complete!")
