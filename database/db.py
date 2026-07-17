import sqlite3

# Create DB and table
def init_db():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT
        )
    """)

    conn.commit()
    conn.close()


# Save chat
def save_chat(user_message, bot_response):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chats (user_message, bot_response)
        VALUES (?, ?)
    """, (user_message, bot_response))

    conn.commit()
    conn.close()


# Get all chats
def get_chats():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chats")
    rows = cursor.fetchall()

    conn.close()
    return rows