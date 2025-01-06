from db_operations import add_expense, get_expenses_by_user_id

def add_expense_action(user_id, date, category, amount, mode_of_payment):
    add_expense(user_id, date, category, amount, mode_of_payment)

def get_user_expenses(user_id):
    return get_expenses_by_user_id(user_id)
