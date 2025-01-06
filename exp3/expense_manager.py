import os

# Function to add an expense
def add_expense(date, category, amount, payment_mode, user):
    if not date or not category or not amount or not payment_mode:
        return "Please fill all fields!"

    # Validate amount: Check if it's a valid number
    try:
        amount = float(amount)
    except ValueError:
        return "Please enter a valid amount!"

    # Add expense to the file
    try:
        with open("expenses.txt", "a") as file:
            file.write(f"{date},{category},{amount},{payment_mode},{user}\n")
        return "Expense added successfully!"
    except Exception as e:
        return f"Error saving expense: {e}"

# Function to delete an expense
def delete_expense(date, category, amount, payment_mode, user):
    try:
        with open("expenses.txt", "r") as file:
            lines = file.readlines()
        
        with open("expenses.txt", "w") as file:
            for line in lines:
                if line.strip() != f"{date},{category},{amount},{payment_mode},{user}":
                    file.write(line)
        return "Expense deleted successfully!"
    except Exception as e:
        return f"Error deleting expense: {e}"

# Function to show all expenses
def get_all_expenses():
    expenses = []
    if os.path.exists("expenses.txt"):
        try:
            with open("expenses.txt", "r") as file:
                for line in file:
                    values = line.strip().split(",")
                    if len(values) == 5:
                        expenses.append(tuple(values))
        except Exception as e:
            return f"Error reading expenses: {e}"
    return expenses
