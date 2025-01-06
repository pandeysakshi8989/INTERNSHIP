import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# Function to add an expense
def add_expense():
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
            file.write(f"{date},{category},{amount},{payment_mode}\n")
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
        date, category, amount, payment_mode = item_text

        # Remove the selected expense from the file
        try:
            with open("expenses.txt", "r") as file:
                lines = file.readlines()
            
            with open("expenses.txt", "w") as file:
                for line in lines:
                    if line.strip() != f"{date},{category},{amount},{payment_mode}":
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
                    # Ensure there are exactly 4 values
                    values = line.strip().split(",")
                    if len(values) != 4:  # Skip invalid lines
                        continue
                    
                    date, category, amount, payment_mode = values
                    expenses_tree.insert("", tk.END, values=(date, category, amount, payment_mode))
                    total_expense += float(amount)
            total_label.config(text=f"Total Expense: {total_expense:.2f}")
        except Exception as e:
            total_label.config(text="Error reading expenses file.")
            print(f"Error: {e}")
    else:
        total_label.config(text="No expenses recorded.")

# Function to show expenses grouped by category
def show_category_expenses():
    expenses_tree.delete(*expenses_tree.get_children())
    category_totals = {}

    if os.path.exists("expenses.txt"):
        try:
            with open("expenses.txt", "r") as file:
                for line in file:
                    # Ensure there are exactly 4 values
                    values = line.strip().split(",")
                    if len(values) != 4:  # Skip invalid lines
                        continue
                    
                    date, category, amount, payment_mode = values
                    amount = float(amount)

                    if category not in category_totals:
                        category_totals[category] = 0
                    category_totals[category] += amount

            for category, total in category_totals.items():
                expenses_tree.insert("", tk.END, values=(category, f"{total:.2f}"))
            total_label.config(text="Category-wise Expenses")
        except Exception as e:
            total_label.config(text="Error reading expenses file.")
            print(f"Error: {e}")
    else:
        total_label.config(text="No expenses recorded.")

# Function to show expenses grouped by month
def show_monthly_expenses():
    expenses_tree.delete(*expenses_tree.get_children())
    monthly_totals = {}

    if os.path.exists("expenses.txt"):
        try:
            with open("expenses.txt", "r") as file:
                for line in file:
                    # Ensure there are exactly 4 values
                    values = line.strip().split(",")
                    if len(values) != 4:  # Skip invalid lines
                        continue
                    
                    date, category, amount, payment_mode = values
                    amount = float(amount)
                    expense_date = datetime.strptime(date, "%d-%m-%Y")  # Change date format to DD-MM-YYYY
                    month_year = expense_date.strftime("%B %Y")  # Group by month (e.g., January 2025)

                    if month_year not in monthly_totals:
                        monthly_totals[month_year] = 0
                    monthly_totals[month_year] += amount

            for month_year, total in monthly_totals.items():
                expenses_tree.insert("", tk.END, values=(month_year, f"{total:.2f}"))
            total_label.config(text="Monthly Expenses")
        except Exception as e:
            total_label.config(text="Error reading expenses file.")
            print(f"Error: {e}")
    else:
        total_label.config(text="No expenses recorded.")

# Function to change the view to show all expenses
def change_to_all_expenses_view():
    show_all_expenses()

# Function to change the view to show category-wise expenses
def change_to_category_expenses_view():
    show_category_expenses()

# Function to change the view to show monthly expenses
def change_to_monthly_expenses_view():
    show_monthly_expenses()

# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")

# Create labels and entries for adding expenses
date_label = tk.Label(root, text="Date (DD-MM-YYYY):")
date_label.grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

category_label = tk.Label(root, text="Category:")
category_label.grid(row=1, column=0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=2, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

# Adding payment mode options using combobox
payment_mode_label = tk.Label(root, text="Payment Mode:")
payment_mode_label.grid(row=3, column=0, padx=5, pady=5)
payment_mode_combobox = ttk.Combobox(root, values=["Cash", "Credit Card", "Debit Card", "Online", "UPI"])
payment_mode_combobox.grid(row=3, column=1, padx=5, pady=5)
payment_mode_combobox.set('')

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

# Create a treeview to display expenses
columns = ("Date", "Category", "Amount", "Payment Mode")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.heading("Payment Mode", text="Payment Mode")
expenses_tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# Create a label to display the total expense
total_label = tk.Label(root, text="")
total_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Create a label to show the status of expense addition and deletion
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

# Create buttons to view different types of expenses
view_all_button = tk.Button(root, text="View All Expenses", command=change_to_all_expenses_view)
view_all_button.grid(row=8, column=0, padx=5, pady=10)

view_category_button = tk.Button(root, text="View Category Expenses", command=change_to_category_expenses_view)
view_category_button.grid(row=8, column=1, padx=5, pady=10)

view_monthly_button = tk.Button(root, text="View Monthly Expenses", command=change_to_monthly_expenses_view)
view_monthly_button.grid(row=8, column=2, padx=5, pady=10)

delete_button = tk.Button(root, text="Delete Expense", command=delete_expense)
delete_button.grid(row=9, column=0, columnspan=3, padx=5, pady=10)

# Check if the 'expenses.txt' file exists; create it if it doesn't
if not os.path.exists("expenses.txt"):
    try:
        with open("expenses.txt", "w"):
            pass
    except Exception as e:
        messagebox.showerror("Error", f"Could not create file: {e}")

# Display all expenses on application start
show_all_expenses()

root.mainloop()
