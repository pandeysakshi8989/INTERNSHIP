import sqlite3

# Connect to the SQLite database (this will create the database if it doesn't exist)
conn = sqlite3.connect('expense_tracker.db')
cursor = conn.cursor()

# Create the 'users' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL
);
''')

# Create the 'expenses' table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    payment_mode TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

# Insert Users
users_data = [
    ('alice', 'alice123'),
    ('bob', 'bob456'),
    ('charlie', 'charlie789'),
    ('diana', 'diana101'),
    ('emma', 'emma202')
]

cursor.executemany('INSERT OR IGNORE INTO users (username) VALUES (?)', [(user[0],) for user in users_data])

# Get user IDs
cursor.execute('SELECT id, username FROM users')
users = {user[1]: user[0] for user in cursor.fetchall()}

# Insert Expenses for Alice
expenses_data = [
    ('01-01-2025', 'Food', 20.5, 'Cash', 'alice'),
    ('02-01-2025', 'Transport', 15.0, 'Credit Card', 'alice'),
    ('03-01-2025', 'Shopping', 50.0, 'Debit Card', 'alice'),
    ('04-01-2025', 'Entertainment', 30.0, 'Online', 'alice'),

    ('01-01-2025', 'Food', 25.0, 'Debit Card', 'bob'),
    ('02-01-2025', 'Transport', 10.0, 'Cash', 'bob'),
    ('03-01-2025', 'Shopping', 60.0, 'Credit Card', 'bob'),
    ('04-01-2025', 'Utilities', 40.0, 'UPI', 'bob'),

    ('01-01-2025', 'Food', 35.0, 'Cash', 'charlie'),
    ('02-01-2025', 'Transport', 20.0, 'Debit Card', 'charlie'),
    ('03-01-2025', 'Shopping', 45.0, 'Credit Card', 'charlie'),
    ('04-01-2025', 'Entertainment', 25.0, 'Online', 'charlie'),

    ('01-01-2025', 'Food', 15.0, 'UPI', 'diana'),
    ('02-01-2025', 'Transport', 30.0, 'Debit Card', 'diana'),
    ('03-01-2025', 'Shopping', 40.0, 'Credit Card', 'diana'),
    ('04-01-2025', 'Entertainment', 20.0, 'Cash', 'diana'),

    ('01-01-2025', 'Food', 18.0, 'Credit Card', 'emma'),
    ('02-01-2025', 'Transport', 12.0, 'UPI', 'emma'),
    ('03-01-2025', 'Shopping', 30.0, 'Debit Card', 'emma'),
    ('04-01-2025', 'Utilities', 35.0, 'Cash', 'emma')
]

# Map user names to user_ids and prepare data
expenses_with_user_ids = [(date, category, amount, payment_mode, users[user]) for (date, category, amount, payment_mode, user) in expenses_data]

# Insert Expenses for all users
cursor.executemany('''
INSERT INTO expenses (date, category, amount, payment_mode, user_id) 
VALUES (?, ?, ?, ?, ?)
''', expenses_with_user_ids)

# Commit the changes and close the connection
conn.commit()

# Print confirmation
print("Users and expenses data have been inserted successfully.")

# Close the connection
conn.close()
