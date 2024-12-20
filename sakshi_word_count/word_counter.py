import sqlite3

def create_database():
    """
    This function creates the SQLite database and the necessary table to store the user's input and word count.
    """
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('word_counter.db')
    c = conn.cursor()
    
    # Create a table for storing user details, inputs, and word count results
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        input_text TEXT NOT NULL,
        word_count INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    # Create a table for storing user registration details
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def store_user_data(user_id, name, input_text, word_count):
    """
    This function stores the user data (name, input text, word count) in the database.
    """
    conn = sqlite3.connect('word_counter.db')
    c = conn.cursor()
    
    # Insert user data into the table (now allowing multiple entries per user)
    c.execute('''
    INSERT INTO user_data (user_id, name, input_text, word_count)
    VALUES (?, ?, ?, ?)
    ''', (user_id, name, input_text, word_count))
    
    conn.commit()
    conn.close()

def store_new_user(user_id, name):
    """
    This function registers a new user by storing their details in the users table.
    """
    conn = sqlite3.connect('word_counter.db')
    c = conn.cursor()

    # Insert new user data into the users table
    c.execute('''
    INSERT INTO users (user_id, name)
    VALUES (?, ?)
    ''', (user_id, name))
    
    conn.commit()
    conn.close()

def get_past_data(user_id):
    """
    This function retrieves past word count data for a given user ID from the database.
    """
    conn = sqlite3.connect('word_counter.db')
    c = conn.cursor()
    
    # Query past data for the given user ID
    c.execute('''
    SELECT input_text, word_count FROM user_data WHERE user_id = ?
    ''', (user_id,))
    
    rows = c.fetchall()
    conn.close()
    
    return rows

def count_words(text):
    """
    This function takes a string as input and returns the number of words.
    It splits the text by spaces and counts the words.
    """
    if not text.strip():
        return 0
    words = text.split()
    return len(words)

def check_existing_user(user_id):
    """
    This function checks if a user ID already exists in the database.
    """
    conn = sqlite3.connect('word_counter.db')
    c = conn.cursor()
    
    # Query the users table to check if the user ID exists
    c.execute('''
    SELECT * FROM users WHERE user_id = ?
    ''', (user_id,))
    
    user = c.fetchone()
    conn.close()
    
    return user

def main():
    """
    The main function that handles user input, stores the data in the database,
    and retrieves past data if needed.
    """
    create_database()

    print("Welcome to the Word Counter Program!")
    
    # Ask if the user is a new user or returning user
    user_choice = input("Are you a new user? (yes/no): ").strip().lower()
    
    user = None  # Initialize the user variable

    if user_choice == 'yes':
        # Register new user
        while True:
            try:
                name = input("Please enter your name: ").strip()
                user_id = int(input("Please enter a unique user ID (numeric only): ").strip())
                
                # Check if user ID already exists
                if check_existing_user(user_id):
                    print("Error: User ID already exists. Please choose a different ID.")
                    continue
                
                # Register the new user
                store_new_user(user_id, name)
                print(f"User {name} successfully registered with ID {user_id}!")
                
                # Set user details
                user = (user_id, name)
                break  # Break out of the loop after successful registration
                
            except ValueError:
                print("Invalid input. Please enter a valid numeric user ID.")
    
    else:
        # Ask for existing user ID if not a new user
        while True:
            try:
                user_id = int(input("Please enter your user ID: ").strip())
                
                if not check_existing_user(user_id):
                    print("Error: User ID not found. Please register first.")
                    continue
                
                user = check_existing_user(user_id)
                print(f"Welcome back, {user[1]}!")

                break  # Proceed after confirming user exists

            except ValueError:
                print("Invalid input. Please enter a valid numeric user ID.")

    # Ask if the user wants to retrieve past data
    user_choice = input("Do you want to view your previous word count data? (yes/no): ").strip().lower()
    
    if user_choice == 'yes':
        # Retrieve and display the past data
        past_data = get_past_data(user[0])  # Use user[0] (user_id) to retrieve data
        if not past_data:
            print(f"No previous data found for user ID {user[0]}.")
        else:
            print(f"\nPrevious Word Count Data for User ID {user[0]}:")
            for entry in past_data:
                print(f"Text: {entry[0]} | Word Count: {entry[1]}")
    else:
        # Start counting words if the user doesn't want to retrieve data
        while True:
            user_input = input("\nEnter your text (or type 'exit' to stop): ")
            
            if user_input.lower() == 'exit':
                print("Thank you for using the Word Counter. Goodbye!")
                break
            
            word_count = count_words(user_input)
            print(f"\nWord Count: {word_count}")
            
            # Store the input and the word count in the database
            store_user_data(user[0], user[1], user_input, word_count)  # Pass user[0] (user_id) and user[1] (name)
            
            continue_input = input("Do you want to enter another text? (yes/no): ").strip().lower()
            if continue_input != 'yes':
                print("Thank you for using the Word Counter. Goodbye!")
                break

# Run the program
if __name__ == "__main__":
    main()
