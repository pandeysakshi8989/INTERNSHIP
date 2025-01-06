import sqlite3

def connect_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    return conn, cursor

def create_tables():
    conn, cursor = connect_db()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        email TEXT UNIQUE,
                        username TEXT,
                        password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        date TEXT,
                        category TEXT,
                        amount REAL,
                        mode_of_payment TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

def add_admin():
    conn, cursor = connect_db()
    cursor.execute('''INSERT OR IGNORE INTO users (email, username, password)
                        VALUES ('admin123@gmail.com', 'admin', 'ad123')''')
    conn.commit()
    conn.close()

def get_user_by_email_and_password(email, password):
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def register_user(email, username, password):
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    if user:
        conn.close()
        return False
    cursor.execute('INSERT INTO users (email, username, password) VALUES (?, ?, ?)', (email, username, password))
    conn.commit()
    conn.close()
    return True

def get_expenses_by_user_id(user_id):
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM expenses WHERE user_id = ?', (user_id,))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def add_expense(user_id, date, category, amount, mode_of_payment):
    conn, cursor = connect_db()
    cursor.execute('INSERT INTO expenses (user_id, date, category, amount, mode_of_payment) VALUES (?, ?, ?, ?, ?)',
                   (user_id, date, category, amount, mode_of_payment))
    conn.commit()
    conn.close()
