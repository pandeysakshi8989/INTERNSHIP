import tkinter as tk
from tkinter import messagebox
import hashlib
from db_connection import get_db_connection

class LoginRegister:
    def __init__(self, root, login_success_callback):
        self.root = root
        self.login_success_callback = login_success_callback
        self.create_login_screen()

    def create_login_screen(self):
        """Creates the login screen."""
        login_label = tk.Label(self.root, text="Login", font=("Arial", 24))
        login_label.pack(pady=10)

        username_label = tk.Label(self.root, text="Username:")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self.root, text="Password:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.root, text="Login", command=self.verify_login)
        login_button.pack(pady=10)

        self.register_button = tk.Button(self.root, text="Register", command=self.create_registration_screen)
        self.register_button.pack(pady=10)

    def verify_login(self):
        """Verifies the login credentials and calls the callback."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        # Check the database for user credentials
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user:
            stored_password_hash = user[1]  # Assuming password is stored in user[1]
            if self.verify_password(password, stored_password_hash):
                self.login_success_callback(user)
            else:
                messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.create_registration_screen()  # Show registration option if login fails

    def verify_password(self, input_password, stored_password_hash):
        """Verifies if the provided password matches the stored hashed password."""
        # Hash the input password and compare it with the stored hash
        hashed_input_password = hashlib.sha256(input_password.encode()).hexdigest()
        return hashed_input_password == stored_password_hash

    def create_registration_screen(self):
        """Creates the registration screen."""
        self.clear_screen()

        registration_label = tk.Label(self.root, text="Register", font=("Arial", 24))
        registration_label.pack(pady=10)

        username_label = tk.Label(self.root, text="Username:")
        username_label.pack(pady=5)
        self.register_username_entry = tk.Entry(self.root)
        self.register_username_entry.pack(pady=5)

        password_label = tk.Label(self.root, text="Password:")
        password_label.pack(pady=5)
        self.register_password_entry = tk.Entry(self.root, show="*")
        self.register_password_entry.pack(pady=5)

        confirm_password_label = tk.Label(self.root, text="Confirm Password:")
        confirm_password_label.pack(pady=5)
        self.confirm_password_entry = tk.Entry(self.root, show="*")
        self.confirm_password_entry.pack(pady=5)

        register_button = tk.Button(self.root, text="Register", command=self.register_user)
        register_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back to Login", command=self.create_login_screen)
        back_button.pack(pady=10)

    def register_user(self):
        """Registers a new user in the database."""
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Hash the password before saving it
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Insert the new user into the database
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Registration successful! You can now login.")
        self.create_login_screen()

    def clear_screen(self):
        """Clears the screen by destroying all widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()
