import sqlite3
def init_db():
conn = sqlite3.connect("bot_data.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
user_id INTEGER PRIMARY KEY,
slept BOOLEAN DEFAULT 0,
last_alarm TEXT DEFAULT '06:00'
)
''')
conn.commit()
conn.close()
if __name__ == "__main__":
init_db()