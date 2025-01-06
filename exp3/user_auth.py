import os
from tkinter import messagebox

# Global dictionary to store users
registered_users = {}

# Load users from the file (username: password)
def load_users():
    global registered_users
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            for line in file:
                username, password = line.strip().split(":")
                registered_users[username] = password

# Save new users to the file with password (username:password)
def save_user(username, password):
    with open("users.txt", "a") as file:
        file.write(f"{username}:{password}\n")
    registered_users[username] = password

# Register a new user with password
def register(username, password):
    global registered_users
    if username in registered_users:
        return "Username already exists."
    
    save_user(username, password)
    load_users()  # Reload users
    return "User registered successfully!"

# Authenticate a user by checking username and password
def login(username, password):
    global registered_users
    if username in registered_users and registered_users[username] == password:
        return "Login successful!"
    else:
        return "Invalid username or password."
