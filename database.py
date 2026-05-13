import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Create chatbot responses table
cursor.execute('''
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    response TEXT
)
''')

# Create users table (no UNIQUE constraint on username)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    username TEXT,
    password TEXT
)
''')

# Save changes and close connection
conn.commit()
conn.close()

print("Database and tables created successfully!")