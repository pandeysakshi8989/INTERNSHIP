import tkinter as tk
from tkinter import messagebox
from db_operations import register_user, get_user_by_email_and_password, add_admin, create_tables

def register_user_action(email, username, password, confirm_password):
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return False
    if register_user(email, username, password):
        messagebox.showinfo("Success", "Registration successful! Please login.")
        return True
    else:
        messagebox.showerror("Error", "Email already exists. Please login.")
        return False

def authenticate_user_action(email, password):
    user = get_user_by_email_and_password(email, password)
    return user
