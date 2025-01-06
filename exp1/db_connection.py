import sqlite3

def create_db():
    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('expense_tracker.db')
    c = conn.cursor()

    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    confirm_password TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date TEXT,
                    category TEXT,
                    amount REAL,
                    payment_mode TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS admin (
                    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL)''')

    # Insert default admin (you can modify this part as needed)
    c.execute("SELECT * FROM admin WHERE admin_id = 1")
    if not c.fetchone():
        c.execute("INSERT INTO admin (username, password) VALUES ('admin', 'admin123')")

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('expense_tracker.db')
    return conn
