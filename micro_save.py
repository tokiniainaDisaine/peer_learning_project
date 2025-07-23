#!/usr/bin/python3
"""
Welcome to MicroSave :)
The app to help you reach your financial goals
"""
import mysql.connector


# Functions

# Database
def setup_db(host="localhost", user="root", password="", database="microsave"):
    """
    Sets up the MySQL database and required tables for MicroSave.
    Creates the database and tables if they do not exist.
    """
    # Connect to MySQL server
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    cursor = conn.cursor()

    # Create database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    conn.database = database

    # Create Income table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Income (
            id INT AUTO_INCREMENT PRIMARY KEY,
            source VARCHAR(255),
            amount DECIMAL(100000000,2),
            date DATE
        )
    """)

    # Create Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(255),
            amount DECIMAL(100000000,2),
            date DATE
        )
    """)

    # Create Savings_goal table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Savings_goal (
            id INT PRIMARY KEY,
            amount DECIMAL(100000000,2)
            description VARCHAR(255),
            target_date DATE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.close()
    conn.close()
    print("Database and tables are set up.")

def show_welcome_screen():
    print(">>> Welcome to MicroSaver!")
    print("Your app to track your finances properly.")
    choice = input("Do you wish to continue? [Y/n]: ").strip().lower()
    if choice != 'y':
        print("Goodbye!")
        exit()

def add_income():
    source = input("Enter income source (e.g., job, hustle): ")
    try:
        amount = float(input("Enter amount (RWF): "))
        date = datetime.date.today().isoformat()

        conn = connect_db()
        c = conn.cursor()
        c.execute("INSERT INTO Income (source, amount, date) VALUES (%s, %s, %s)", (source, amount, date))
        conn.commit()
        conn.close()

        print(f"Income of {amount} RWF from {source} recorded.")
    except ValueError:
        print("Invalid amount.")


def add_expenses(category, amount, date, host="localhost", user="root", password="", database="microsave"):
     # Connect to MySQL server
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Expenses (category, amount, date) VALUES (%s, %s, %s)",
        (category, amount, date)
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("Expense added.")


def set_savings_goal(amount, description, target_date, host="localhost", user="root", password="", database="microsave"):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO Savings_goal (category, amount, date) VALUES (%s, %s, %s)",
        (amount, description, target_date)
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("Saving goal added.")





def visualize_percentage(name, value, total):
    """
    Function that give a visual representation of a percentage,
    Prints the representation as "#"

    Args: 
        name (string):
        value (int):
        total (int)

    Returns: None
        prints the visual of the percentage
    """
    
    percentage = (value/total) * 100
    item = "{}: {}%".format(name, percentage)

    print(item.ljust(25), end=" ")

    for i in range(int(percentage/2)):
        print("#", end="")
    print("")



def main():
    setup_db()
    show_welcome_screen()

    while True:
        print("\n-----Main Menu-----")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Set Savings Goal")
        print("4. View Summary")
        print("5. Export Report")
        print("6. Exit")

        choice = input("Choose an option [1-6]: ").strip()

        if choice == '1':
            add_income()
        elif choice == '2':
            add_expenses()
        elif choice == '3':
            set_savings_goal()
        elif choice == '4':
            view_summary()
        elif choice == '5':
            export_report()
        elif choice == '6':
            print("Thank you for using MicroSaver. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
