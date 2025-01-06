import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import get_db_connection
import matplotlib.pyplot as plt

# Functions for managing expenses
def add_expense(user_id, date, category, amount, payment_mode):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("INSERT INTO expenses (user_id, date, category, amount, payment_mode) VALUES (?, ?, ?, ?, ?)",
              (user_id, date, category, amount, payment_mode))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Expense added successfully!")

def delete_expense(expense_id):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Expense deleted successfully!")

def show_expenses(user_id):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM expenses WHERE user_id = ?", (user_id,))
    expenses = c.fetchall()
    conn.close()

    # Clear the previous entries in the treeview
    for item in expenses_tree.get_children():
        expenses_tree.delete(item)

    # Insert expenses into the treeview
    for expense in expenses:
        expenses_tree.insert("", tk.END, values=(expense[0], expense[2], expense[3], expense[4], expense[5]))

class ExpenseSystem:
    def __init__(self, root, user, logout_callback):
        self.root = root
        self.user = user
        self.logout_callback = logout_callback
        self.setup_expense_system()

    def setup_expense_system(self):
        """Sets up the expense system screen for regular users."""
        label = tk.Label(self.root, text=f"Welcome, {self.user[1]}", font=("Arial", 18))
        label.pack(pady=20)

        # Add Expense Button
        add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        add_button.pack(pady=10)

        # Show Expenses Button
        show_button = tk.Button(self.root, text="Show Expenses", command=self.show_expenses)
        show_button.pack(pady=10)

        # Treeview for showing expenses
        columns = ("Expense ID", "Date", "Category", "Amount", "Payment Mode")
        global expenses_tree
        expenses_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        expenses_tree.heading("Expense ID", text="Expense ID")
        expenses_tree.heading("Date", text="Date")
        expenses_tree.heading("Category", text="Category")
        expenses_tree.heading("Amount", text="Amount")
        expenses_tree.heading("Payment Mode", text="Payment Mode")
        expenses_tree.pack(pady=10)

        # Logout Button
        logout_button = tk.Button(self.root, text="Logout", command=self.logout_callback)
        logout_button.pack(pady=10)

    def add_expense(self):
        """Add a new expense."""
        # For demonstration purposes, we add a hardcoded expense (you can later modify it with input dialogs)
        add_expense(self.user[0], "2025-01-06", "Food", 20.5, "Cash")

    def show_expenses(self):
        """Show expenses from the database."""
        show_expenses(self.user[0])

    def delete_expense(self, expense_id):
        """Delete an expense based on its ID."""
        delete_expense(expense_id)
