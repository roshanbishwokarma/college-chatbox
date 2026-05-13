import sqlite3

# Connect to database
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Create chatbot responses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT,
    response TEXT
)
""")

# Create users table (duplicates allowed)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    username TEXT,
    password TEXT
)
""")

# Create chat history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    bot_response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Save and close
conn.commit()
conn.close()

print("Database and all tables created successfully!")