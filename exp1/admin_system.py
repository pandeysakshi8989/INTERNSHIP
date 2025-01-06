import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from db_connection import get_db_connection

class AdminSystem:
    def __init__(self, root, user, logout_callback):
        self.root = root
        self.user = user
        self.logout_callback = logout_callback
        self.setup_admin_screen()

    def setup_admin_screen(self):
        """Sets up the admin system screen."""
        label = tk.Label(self.root, text=f"Welcome, Admin {self.user[1]}", font=("Arial", 18))
        label.pack(pady=20)

        view_button = tk.Button(self.root, text="View All Users", command=self.view_all_users)
        view_button.pack(pady=10)

        compare_button = tk.Button(self.root, text="Compare Expenses", command=lambda: self.compare_expenses(1, 2, "Food"))
        compare_button.pack(pady=10)

        self.users_tree = ttk.Treeview(self.root, columns=("User ID", "Username"), show="headings")
        self.users_tree.heading("User ID", text="User ID")
        self.users_tree.heading("Username", text="Username")
        self.users_tree.pack(pady=10)

        global compare_label
        compare_label = tk.Label(self.root, text="", font=("Arial", 12))
        compare_label.pack(pady=10)

        logout_button = tk.Button(self.root, text="Logout", command=self.logout_callback)
        logout_button.pack(pady=10)

    def view_all_users(self):
        """Displays all users in the treeview."""
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        conn.close()

        for user in users:
            self.users_tree.insert("", tk.END, values=(user[0], user[1]))

    def compare_expenses(self, user1_id, user2_id, category):
        """Compares expenses of two users and displays the result."""
        conn = get_db_connection()
        c = conn.cursor()

        c.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ? AND category = ?", (user1_id, category))
        user1_expenses = c.fetchone()[0] or 0

        c.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ? AND category = ?", (user2_id, category))
        user2_expenses = c.fetchone()[0] or 0

        conn.close()

        compare_label.config(text=f"User 1 Expenses: {user1_expenses}\nUser 2 Expenses: {user2_expenses}")
        self.generate_comparison_graph(user1_expenses, user2_expenses)

    def generate_comparison_graph(self, user1_expenses, user2_expenses):
        """Generates the comparison graph."""
        users = ['User 1', 'User 2']
        expenses = [user1_expenses, user2_expenses]

        plt.bar(users, expenses, color=['blue', 'orange'])
        plt.title("Comparison of Expenses")
        plt.xlabel("Users")
        plt.ylabel("Expenses")
        plt.tight_layout()
        plt.show()
