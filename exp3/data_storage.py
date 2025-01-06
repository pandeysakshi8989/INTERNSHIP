import os

# Ensure the file paths exist
def check_files():
    if not os.path.exists("users.txt"):
        open("users.txt", "w").close()
    if not os.path.exists("expenses.txt"):
        open("expenses.txt", "w").close()
