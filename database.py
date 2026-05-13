import sqlite3

conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Chatbot responses table
cursor.execute('''
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    response TEXT
)
''')
#user table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    username TEXT UNIQUE,
    password TEXT
)
''')

conn.commit()
conn.close()

print("Database and tables created successfully!")