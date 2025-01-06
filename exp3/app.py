import tkinter as tk
from tkinter import ttk, messagebox
from user_auth import login, register
from expense_manager import add_expense, delete_expense, get_all_expenses
from utils import generate_expense_graph
from data_storage import check_files

# GUI Setup
root = tk.Tk()
root.title("Expense Tracker")

# Initialize global variables
logged_in_user = None

# Ensure required files exist
check_files()

# Function to handle user login
def handle_login():
    global logged_in_user
    username = username_entry.get()
    password = password_entry.get()
    response = login(username, password)
    
    if response == "Login successful!":
        logged_in_user = username
        user_label.config(text=f"User: {logged_in_user}")
        status_label.config(text="Logged in successfully.", fg="green")
        login_button.config(state=tk.DISABLED)
    else:
        messagebox.showwarning("Login Error", response)

# Function to handle user registration
def handle_register():
    username = username_entry.get()
    password = password_entry.get()
    response = register(username, password)
    
    if response == "User registered successfully!":
        messagebox.showinfo("Registration", response)
        handle_login()  # Automatically log in after registration
    else:
        messagebox.showwarning("Registration Error", response)

# Function to add an expense
def handle_add_expense():
    if not logged_in_user:
        messagebox.showwarning("Login Required", "Please log in first!")
        return

    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    payment_mode = payment_mode_combobox.get()

    response = add_expense(date, category, amount, payment_mode, logged_in_user)
    status_label.config(text=response, fg="green" if "successfully" in response else "red")
    show_expenses()

# Function to delete an expense
def handle_delete_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, amount, payment_mode, user = item_text

        response = delete_expense(date, category, amount, payment_mode, user)
        status_label.config(text=response, fg="green" if "successfully" in response else "red")
        show_expenses()
    else:
        status_label.config(text="Please select an expense to delete!", fg="red")

# Function to show all expenses
def show_expenses():
    expenses = get_all_expenses()
    expenses_tree.delete(*expenses_tree.get_children())
    for expense in expenses:
        expenses_tree.insert("", tk.END, values=expense)

# Function to display the expense graph
def show_graph():
    generate_expense_graph()

# GUI Widgets
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=5, pady=5)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = tk.Button(root, text="Login", command=handle_login)
login_button.grid(row=2, column=0, padx=5, pady=5)

register_button = tk.Button(root, text="Register", command=handle_register)
register_button.grid(row=2, column=1, padx=5, pady=5)

user_label = tk.Label(root, text="User: Not logged in")
user_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

status_label = tk.Label(root, text="Please log in to continue.")
status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Expense Form
date_label = tk.Label(root, text="Date (DD-MM-YYYY):")
date_label.grid(row=5, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=5, column=1, padx=5, pady=5)

category_label = tk.Label(root, text="Category:")
category_label.grid(row=6, column=0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=6, column=1, padx=5, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=7, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=7, column=1, padx=5, pady=5)

payment_mode_label = tk.Label(root, text="Payment Mode:")
payment_mode_label.grid(row=8, column=0, padx=5, pady=5)
payment_mode_combobox = ttk.Combobox(root, values=["Cash", "Debit Card", "Credit Card", "UPI", "Online"])
payment_mode_combobox.grid(row=8, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Expense", command=handle_add_expense)
add_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

delete_button = tk.Button(root, text="Delete Expense", command=handle_delete_expense)
delete_button.grid(row=9, column=2, padx=5, pady=5)

# Show Expense List
expenses_tree = ttk.Treeview(root, columns=("Date", "Category", "Amount", "Payment Mode", "User"), show="headings")
expenses_tree.grid(row=10, column=0, columnspan=3, padx=5, pady=5)

expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.heading("Payment Mode", text="Payment Mode")
expenses_tree.heading("User", text="User")

# Expense Graph Button
graph_button = tk.Button(root, text="Show Expense Graph", command=show_graph)
graph_button.grid(row=11, column=0, columnspan=3, padx=5, pady=5)

# Start the application
show_expenses()
root.mainloop()
