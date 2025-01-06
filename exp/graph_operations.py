import pandas as pd
import matplotlib.pyplot as plt
from db_operations import get_expenses_by_user_id

def generate_expense_graph(user_id):
    expenses = get_expenses_by_user_id(user_id)
    df = pd.DataFrame(expenses, columns=['ID', 'User_ID', 'Date', 'Category', 'Amount', 'Mode_of_Payment'])
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Monthly expenses graph
    monthly_expenses = df.groupby(df['Date'].dt.to_period('M'))['Amount'].sum()
    fig, ax = plt.subplots(figsize=(5, 5))
    monthly_expenses.plot(kind='bar', ax=ax)
    ax.set_title('Monthly Expenses')
    ax.set_ylabel('Amount')
    
    # Category-wise expenses graph
    category_expenses = df.groupby('Category')['Amount'].sum()
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    category_expenses.plot(kind='pie', ax=ax2, autopct='%1.1f%%')
    ax2.set_title('Category-wise Expenses')

    return fig, fig2
