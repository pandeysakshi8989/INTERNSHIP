import sqlite3
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Connect to SQLite database
def connect_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    return conn, cursor

# Create tables if they do not exist
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

# Predefined admin credentials
def add_admin():
    conn, cursor = connect_db()
    cursor.execute('''INSERT OR IGNORE INTO users (email, username, password)
                        VALUES ('admin123@gmail.com', 'admin', 'ad123')''')
    conn.commit()
    conn.close()

# Register a new user
def register_user(email, username, password):
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    if user:
        messagebox.showerror("Error", "Email already exists. Please login.")
        return False
    else:
        cursor.execute('INSERT INTO users (email, username, password) VALUES (?, ?, ?)',
                       (email, username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Registration successful! Please login.")
        return True

# Authenticate user login
def authenticate_user(email, password):
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Add expense
def add_expense(user_id, date, category, amount, mode_of_payment):
    conn, cursor = connect_db()
    cursor.execute('INSERT INTO expenses (user_id, date, category, amount, mode_of_payment) VALUES (?, ?, ?, ?, ?)',
                   (user_id, date, category, amount, mode_of_payment))
    conn.commit()
    conn.close()

# Get expenses of the user
def get_expenses(user_id):
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM expenses WHERE user_id = ?', (user_id,))
    expenses = cursor.fetchall()
    conn.close()
    return expenses

# Generate graph for expenses (monthly and category-wise)
def generate_expense_graph(user_id):
    expenses = get_expenses(user_id)
    df = pd.DataFrame(expenses, columns=['ID', 'User_ID', 'Date', 'Category', 'Amount', 'Mode_of_Payment'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Monthly expenses graph
    monthly_expenses = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()
    fig, ax = plt.subplots(figsize=(5, 5))
    monthly_expenses.plot(kind='bar', ax=ax)
    ax.set_title('Monthly Expenses')
    ax.set_ylabel('Amount')
    
    # Category-wise expenses graph
    category_expenses = df.groupby('Category')['Amount'].sum()
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    category_expenses.plot(kind='pie', ax=ax2, autopct='%1.1f%%')
    ax2.set_title('Category-wise Expenses')

    return fig, fig2

# Tkinter UI for login
def login_ui():
    root = tk.Tk()
    root.title("Expense Tracker - Login")
    
    tk.Label(root, text="Email").grid(row=0, column=0)
    tk.Label(root, text="Password").grid(row=1, column=0)
    
    email_entry = tk.Entry(root)
    password_entry = tk.Entry(root, show="*")
    
    email_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)
    
    def login_action():
        email = email_entry.get()
        password = password_entry.get()
        user = authenticate_user(email, password)
        if user:
            if email == 'admin123@gmail.com':
                admin_dashboard()
            else:
                user_dashboard(user[0], user[1])  # user[0] = user_id, user[1] = username
        else:
            messagebox.showerror("Error", "Invalid credentials")
    
    tk.Button(root, text="Login", command=login_action).grid(row=2, column=0, columnspan=2)
    tk.Button(root, text="Register", command=register_ui).grid(row=3, column=0, columnspan=2)
    
    root.mainloop()

# Tkinter UI for registration
def register_ui():
    root = tk.Tk()
    root.title("Expense Tracker - Register")
    
    tk.Label(root, text="Email").grid(row=0, column=0)
    tk.Label(root, text="Username").grid(row=1, column=0)
    tk.Label(root, text="Password").grid(row=2, column=0)
    tk.Label(root, text="Confirm Password").grid(row=3, column=0)
    
    email_entry = tk.Entry(root)
    username_entry = tk.Entry(root)
    password_entry = tk.Entry(root, show="*")
    confirm_password_entry = tk.Entry(root, show="*")
    
    email_entry.grid(row=0, column=1)
    username_entry.grid(row=1, column=1)
    password_entry.grid(row=2, column=1)
    confirm_password_entry.grid(row=3, column=1)
    
    def register_action():
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
        elif register_user(email, username, password):
            root.destroy()
            login_ui()

    tk.Button(root, text="Register", command=register_action).grid(row=4, column=0, columnspan=2)
    
    root.mainloop()

# User Dashboard
def user_dashboard(user_id, username):
    root = tk.Tk()
    root.title(f"Welcome {username} - Expense Tracker")

    tk.Label(root, text=f"Hello, {username}").grid(row=0, column=0)

    # Expense form
    tk.Label(root, text="Date").grid(row=1, column=0)
    tk.Label(root, text="Category").grid(row=2, column=0)
    tk.Label(root, text="Amount").grid(row=3, column=0)
    tk.Label(root, text="Mode of Payment").grid(row=4, column=0)
    
    date_entry = tk.Entry(root)
    category_entry = tk.Entry(root)
    amount_entry = tk.Entry(root)
    mode_of_payment_entry = tk.Entry(root)
    
    date_entry.grid(row=1, column=1)
    category_entry.grid(row=2, column=1)
    amount_entry.grid(row=3, column=1)
    mode_of_payment_entry.grid(row=4, column=1)
    
    def add_expense_action():
        date = date_entry.get()
        category = category_entry.get()
        amount = float(amount_entry.get())
        mode_of_payment = mode_of_payment_entry.get()
        add_expense(user_id, date, category, amount, mode_of_payment)
        messagebox.showinfo("Success", "Expense added successfully!")

    tk.Button(root, text="Add Expense", command=add_expense_action).grid(row=5, column=0)
    
    root.mainloop()

# Admin Dashboard
def admin_dashboard():
    root = tk.Tk()
    root.title("Admin Dashboard - Expense Tracker")

    tk.Label(root, text="Admin Dashboard").grid(row=0, column=0)
    # More code for admin-specific tasks like viewing all users and expenses

    root.mainloop()

# Create tables and add admin on first run
create_tables()
add_admin()

# Start the application with login UI
login_ui()
