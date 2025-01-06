from db_operations import create_tables, add_admin
from gui import login_ui

def main():
    create_tables()
    add_admin()  # Add admin user if it doesn't exist
    login_ui()  # Start the application with the login UI

if __name__ == "__main__":
    main()
