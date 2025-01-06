import tkinter as tk
from tkinter import messagebox
from login_register import LoginRegister
from admin_system import AdminSystem
from expense_system import ExpenseSystem

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker System")
        self.current_screen = None
        
        self.open_login_register()

    def open_login_register(self):
        """Open the login/register screen."""
        self.clear_screen()
        self.current_screen = LoginRegister(self.root, self.login_success)

    def login_success(self, user, is_admin):
        """Handles successful login and redirects based on user role."""
        if is_admin:
            self.open_admin_system(user)
        else:
            self.open_expense_system(user)

    def open_admin_system(self, user):
        """Opens the admin system after login."""
        self.clear_screen()
        self.current_screen = AdminSystem(self.root, user, self.logout)

    def open_expense_system(self, user):
        """Opens the expense system after login."""
        self.clear_screen()
        self.current_screen = ExpenseSystem(self.root, user, self.logout)

    def logout(self):
        """Logs out and goes back to the login screen."""
        self.open_login_register()

    def clear_screen(self):
        """Clears the current screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
