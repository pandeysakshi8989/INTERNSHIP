import matplotlib.pyplot as plt
from collections import defaultdict

# Function to generate a bar graph of expenses by category
def generate_expense_graph():
    expenses = defaultdict(float)

    try:
        with open("expenses.txt", "r") as file:
            for line in file:
                values = line.strip().split(",")
                if len(values) == 5:
                    category = values[1]
                    amount = float(values[2])
                    expenses[category] += amount
    except Exception as e:
        return f"Error generating graph: {e}"

    categories = list(expenses.keys())
    amounts = list(expenses.values())

    plt.bar(categories, amounts, color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.title('Expenses by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
