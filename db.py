import sqlite3

def connect():
    return sqlite3.connect("database.db")

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        points INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_user(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (telegram_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def add_points(user_id, points):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET points = points + ? WHERE telegram_id = ?", (points, user_id))
    conn.commit()
    conn.close()

def get_points(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT points FROM users WHERE telegram_id=?", (user_id,))
    data = cur.fetchone()
    conn.close()
    return data[0] if data else 0

def add_material(title, content):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO materials (title, content) VALUES (?,?)", (title, content))
    conn.commit()
    conn.close()

def get_materials():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT title, content FROM materials")
    data = cur.fetchall()
    conn.close()
    return data
