import tkinter as tk
from tkinter import messagebox
from user_operations import register_user_action, authenticate_user_action
from expense_operations import add_expense_action, get_user_expenses
from graph_operations import generate_expense_graph
from db_operations import add_admin, create_tables

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
        user = authenticate_user_action(email, password)
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
        
        if register_user_action(email, username, password, confirm_password):
            root.destroy()
            login_ui()

    tk.Button(root, text="Register", command=register_action).grid(row=4, column=0, columnspan=2)
    
    root.mainloop()

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
        add_expense_action(user_id, date, category, amount, mode_of_payment)
        messagebox.showinfo("Success", "Expense added successfully!")

    tk.Button(root, text="Add Expense", command=add_expense_action).grid(row=5, column=0)

    root.mainloop()

def admin_dashboard():
    root = tk.Tk()
    root.title("Admin Dashboard - Expense Tracker")

    tk.Label(root, text="Admin Dashboard").grid(row=0, column=0)
    
    # Code for admin-specific actions
    
    root.mainloop()
