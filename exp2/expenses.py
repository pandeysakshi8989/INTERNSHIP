import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

# Global variable for logged-in user
logged_in_user = None
registered_users = set()

# Load registered users from the file
def load_users():
    global registered_users
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            registered_users = set(file.read().splitlines())

# Save new users to the file
def save_user(username):
    with open("users.txt", "a") as file:
        file.write(f"{username}\n")
    registered_users.add(username)

# Function to log out
def logout():
    global logged_in_user
    logged_in_user = None
    status_label.config(text="Logged out successfully.", fg="green")
    user_label.config(text="User: Not logged in")
    login_button.config(state=tk.NORMAL)

# Function to log in
def login():
    global logged_in_user
    username = username_entry.get()
    if username in registered_users:
        logged_in_user = username
        user_label.config(text=f"User: {logged_in_user}")
        status_label.config(text="Logged in successfully.", fg="green")
        login_button.config(state=tk.DISABLED)
    else:
        messagebox.showwarning("Login Error", "User not registered! Please register first.")

# Function to register a new user
def register():
    username = username_entry.get()
    if username:
        if username in registered_users:
            messagebox.showwarning("Registration Error", "Username already exists.")
        else:
            save_user(username)
            messagebox.showinfo("Registration", "User registered successfully!")
            load_users()  # Reload users
            login()  # Automatically log in after registration
    else:
        messagebox.showwarning("Input Error", "Please enter a username to register.")

# Function to add an expense
def add_expense():
    if not logged_in_user:
        messagebox.showwarning("Login Required", "Please log in first!")
        return

    # Get user inputs
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    payment_mode = payment_mode_combobox.get()

    # Validate inputs
    if not date or not category or not amount or not payment_mode:
        status_label.config(text="Please fill all the fields!", fg="red")
        return

    # Validate date format (DD-MM-YYYY)
    try:
        datetime.strptime(date, "%d-%m-%Y")  # Check if the date is valid
    except ValueError:
        status_label.config(text="Please enter a valid date (DD-MM-YYYY)!", fg="red")
        return

    # Validate amount: check if it's a valid number
    try:
        amount = float(amount)  # Convert amount to float to check if it's a valid number
    except ValueError:
        status_label.config(text="Please enter a valid amount!", fg="red")
        return

    # Add expense to the file
    try:
        with open("expenses.txt", "a") as file:
            file.write(f"{date},{category},{amount},{payment_mode},{logged_in_user}\n")
        status_label.config(text="Expense added successfully!", fg="green")
    except Exception as e:
        status_label.config(text="Error saving expense!", fg="red")
        print(f"Error: {e}")

    # Clear input fields
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    payment_mode_combobox.set('')

    # Refresh the expense list view
    show_all_expenses()

# Function to delete an expense
def delete_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, amount, payment_mode, user = item_text

        # Remove the selected expense from the file
        try:
            with open("expenses.txt", "r") as file:
                lines = file.readlines()
            
            with open("expenses.txt", "w") as file:
                for line in lines:
                    if line.strip() != f"{date},{category},{amount},{payment_mode},{user}":
                        file.write(line)
            
            status_label.config(text="Expense deleted successfully!", fg="green")
            show_all_expenses()
        except Exception as e:
            status_label.config(text="Error deleting expense!", fg="red")
            print(f"Error: {e}")
    else:
        status_label.config(text="Please select an expense to delete!", fg="red")

# Function to show all expenses
def show_all_expenses():
    expenses_tree.delete(*expenses_tree.get_children())
    total_expense = 0

    if os.path.exists("expenses.txt"):
        try:
            with open("expenses.txt", "r") as file:
                for line in file:
                    # Ensure there are exactly 5 values (date, category, amount, payment mode, user)
                    values = line.strip().split(",")
                    if len(values) != 5:  # Skip invalid lines
                        continue
                    
                    date, category, amount, payment_mode, user = values
                    expenses_tree.insert("", tk.END, values=(date, category, amount, payment_mode, user))
                    total_expense += float(amount)
            total_label.config(text=f"Total Expense: {total_expense:.2f}")
        except Exception as e:
            total_label.config(text="Error reading expenses file.")
            print(f"Error: {e}")
    else:
        total_label.config(text="No expenses recorded.")

# Function to search expenses by category
def search_category_expenses():
    category = category_search_entry.get()
    if not category:
        messagebox.showwarning("Input Error", "Please enter a category to search.")
        return
    
    expenses_tree.delete(*expenses_tree.get_children())
    category_totals = {}

    if os.path.exists("expenses.txt"):
        try:
            with open("expenses.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) != 5:  # Skip invalid lines
                        continue
                    
                    date, exp_category, amount, payment_mode, user = values
                    if category.lower() in exp_category.lower():  # Case-insensitive search
                        amount = float(amount)
                        if exp_category not in category_totals:
                            category_totals[exp_category] = 0
                        category_totals[exp_category] += amount

            for exp_category, total in category_totals.items():
                expenses_tree.insert("", tk.END, values=(exp_category, f"{total:.2f}"))
            total_label.config(text=f"Expenses for Category: {category}")
            generate_category_graph(category_totals)
        except Exception as e:
            total_label.config(text="Error reading expenses file.")
            print(f"Error: {e}")
    else:
        total_label.config(text="No expenses recorded.")

# Function to generate a category-wise graph
def generate_category_graph(category_totals):
    categories = list(category_totals.keys())
    expenses = list(category_totals.values())

    plt.figure(figsize=(10, 6))
    plt.bar(categories, expenses)
    plt.title("Category-wise Expenses")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to search expenses by month
def search_monthly_expenses():
    month_year = month_search_entry.get()
    if not month_year:
        messagebox.showwarning("Input Error", "Please enter a month and year to search (e.g., January 2025).")
        return

    expenses_tree.delete(*expenses_tree.get_children())
    monthly_totals = {}

    if os.path.exists("expenses.txt"):
        try:
            with open("expenses.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) != 5:  # Skip invalid lines
                        continue
                    
                    date, category, amount, payment_mode, user = values
                    amount = float(amount)
                    expense_date = datetime.strptime(date, "%d-%m-%Y")  # Change date format to DD-MM-YYYY
                    expense_month_year = expense_date.strftime("%B %Y")

                    if expense_month_year == month_year:
                        if expense_month_year not in monthly_totals:
                            monthly_totals[expense_month_year] = 0
                        monthly_totals[expense_month_year] += amount

            for month, total in monthly_totals.items():
                expenses_tree.insert("", tk.END, values=(month, f"{total:.2f}"))
            total_label.config(text=f"Expenses for {month_year}")
            generate_month_graph(monthly_totals)
        except Exception as e:
            total_label.config(text="Error reading expenses file.")
            print(f"Error: {e}")
    else:
        total_label.config(text="No expenses recorded.")

# Function to generate a monthly graph
def generate_month_graph(monthly_totals):
    months = list(monthly_totals.keys())
    expenses = list(monthly_totals.values())

    plt.figure(figsize=(10, 6))
    plt.bar(months, expenses)
    plt.title("Monthly Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to compare two users' expenses by month
def compare_users_expenses_month():
    user1 = user1_compare_entry.get()
    user2 = user2_compare_entry.get()
    month_year = compare_month_entry.get()

    if not user1 or not user2 or not month_year:
        messagebox.showwarning("Input Error", "Please enter both users and a month/year to compare.")
        return

    user1_total, user2_total = 0, 0
    if os.path.exists("expenses.txt"):
        try:
            with open("expenses.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) != 5:
                        continue

                    date, category, amount, payment_mode, user = values
                    if user == user1 or user == user2:
                        expense_date = datetime.strptime(date, "%d-%m-%Y")
                        expense_month_year = expense_date.strftime("%B %Y")
                        if expense_month_year == month_year:
                            if user == user1:
                                user1_total += float(amount)
                            elif user == user2:
                                user2_total += float(amount)

            # Display comparison results
            comparison_label.config(text=f"{user1} spent: {user1_total:.2f}\n{user2} spent: {user2_total:.2f}")
            generate_comparison_graph(user1, user2, user1_total, user2_total)
        except Exception as e:
            comparison_label.config(text="Error comparing expenses.")
            print(f"Error: {e}")
    else:
        comparison_label.config(text="No expenses recorded.")

# Function to generate a comparison graph for two users
def generate_comparison_graph(user1, user2, user1_total, user2_total):
    users = [user1, user2]
    expenses = [user1_total, user2_total]

    plt.figure(figsize=(8, 5))
    plt.bar(users, expenses, color=['blue', 'orange'])
    plt.title(f"Expense Comparison between {user1} and {user2}")
    plt.xlabel("Users")
    plt.ylabel("Amount Spent")
    plt.tight_layout()
    plt.show()

# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")

# Load the registered users
load_users()

# User registration and login
user_label = tk.Label(root, text="User: Not logged in")
user_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

username_label = tk.Label(root, text="Enter Username:")
username_label.grid(row=1, column=0, padx=5, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1, padx=5, pady=5)

register_button = tk.Button(root, text="Register", command=register)
register_button.grid(row=1, column=2, padx=5, pady=5)

login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=0, padx=5, pady=5)

logout_button = tk.Button(root, text="Logout", command=logout)
logout_button.grid(row=2, column=2, padx=5, pady=5)

# Expense input
date_label = tk.Label(root, text="Date (DD-MM-YYYY):")
date_label.grid(row=3, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=3, column=1, padx=5, pady=5)

category_label = tk.Label(root, text="Category:")
category_label.grid(row=4, column=0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=4, column=1, padx=5, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=5, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=5, column=1, padx=5, pady=5)

payment_mode_label = tk.Label(root, text="Payment Mode:")
payment_mode_label.grid(row=6, column=0, padx=5, pady=5)
payment_mode_combobox = ttk.Combobox(root, values=["Cash", "Credit Card", "Debit Card", "Online", "UPI"])
payment_mode_combobox.grid(row=6, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10)

# Treeview for displaying expenses
columns = ("Date", "Category", "Amount", "Payment Mode", "User")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.heading("Payment Mode", text="Payment Mode")
expenses_tree.heading("User", text="User")
expenses_tree.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

# Label to display total expenses
total_label = tk.Label(root, text="")
total_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Label to show status messages
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# Category search
category_search_label = tk.Label(root, text="Search by Category:")
category_search_label.grid(row=11, column=0, padx=5, pady=5)
category_search_entry = tk.Entry(root)
category_search_entry.grid(row=11, column=1, padx=5, pady=5)

search_category_button = tk.Button(root, text="Search", command=search_category_expenses)
search_category_button.grid(row=11, column=2, padx=5, pady=5)

# Monthly search
month_search_label = tk.Label(root, text="Search by Month (e.g., January 2025):")
month_search_label.grid(row=12, column=0, padx=5, pady=5)
month_search_entry = tk.Entry(root)
month_search_entry.grid(row=12, column=1, padx=5, pady=5)

search_month_button = tk.Button(root, text="Search", command=search_monthly_expenses)
search_month_button.grid(row=12, column=2, padx=5, pady=5)

# Compare Users' Expenses
compare_label = tk.Label(root, text="Compare Users' Expenses")
compare_label.grid(row=13, column=0, columnspan=2, padx=5, pady=5)

user1_label = tk.Label(root, text="User 1:")
user1_label.grid(row=14, column=0, padx=5, pady=5)
user1_compare_entry = tk.Entry(root)
user1_compare_entry.grid(row=14, column=1, padx=5, pady=5)

user2_label = tk.Label(root, text="User 2:")
user2_label.grid(row=15, column=0, padx=5, pady=5)
user2_compare_entry = tk.Entry(root)
user2_compare_entry.grid(row=15, column=1, padx=5, pady=5)

compare_month_label = tk.Label(root, text="Month (e.g., January 2025):")
compare_month_label.grid(row=16, column=0, padx=5, pady=5)
compare_month_entry = tk.Entry(root)
compare_month_entry.grid(row=16, column=1, padx=5, pady=5)

compare_button = tk.Button(root, text="Compare", command=compare_users_expenses_month)
compare_button.grid(row=16, column=2, padx=5, pady=5)

# Label for comparison results
comparison_label = tk.Label(root, text="")
comparison_label.grid(row=17, column=0, columnspan=3, padx=5, pady=5)

# Load existing users
load_users()

root.mainloop()
