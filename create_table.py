import sqlite3

conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT,
    bot_response TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("chat_history table created successfully!")