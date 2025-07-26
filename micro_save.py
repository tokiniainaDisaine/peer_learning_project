#!/usr/bin/python3
"""
Welcome to MicroSave :)
The app to help you reach your financial goals
"""
import mysql.connector
import datetime
from getpass import getpass

# Functions

# Database
def setup_db(host="localhost", user="root", password="", database="microsave"):
    """
    Sets up the MySQL database and required tables for MicroSave.
    Creates the database and tables if they do not exist.
    """
    # Connect to MySQL server
    try:
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
                amount INT,
                date DATE
            )
        """)

        # Create Expenses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(255),
                amount INT,
                date DATE
            )
        """)

        # Create Savings_goal table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Savings_goal (
                id INT PRIMARY KEY,
                amount INT,
                description VARCHAR(255),
                target_date DATE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.close()
        conn.close()
        print("Database and tables are set up.")

    except mysql.connector.Error as e:
        print(f"Error setting up database: {e}")


#  DATABASE CONNECTION
def get_connection(password=""):
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="microsave"
        )
    except mysql.connector.Error as e:
        print(f"DB Connection Failed: {e}")
        return None


def show_welcome_screen():
    print(">>> Welcome to MicroSaver!")
    print("Your app to track your finances properly.")
    choice = input("Do you wish to continue? [Y/n]: ").strip().lower()
    if choice != 'y':
        print("Goodbye!")
        exit()
        

def add_income(password=""):
    source = input("Enter income source (e.g., job, hustle): ")
    try:
        amount = float(input("Enter amount (RWF): "))
        if amount < 0:
            print("Amount cannot be negative.")
            return
        date = datetime.date.today().isoformat()

        conn = get_connection(password)
        if not conn: return
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Income (source, amount, date) VALUES (%s, %s, %s)", (source, amount, date))
        conn.commit()
        conn.close()

        print(f"Income of {amount} RWF from {source} recorded.")
    except ValueError:
        print("Invalid amount.")


def add_expenses(password=""):
    try:
        category = input("Enter expense category (e.g., food, transport): ")
        amount = float(input("Enter amount (RWF): "))
        if amount < 0:
            print("Amount cannot be negative.")
            return
        date_today = datetime.date.today().isoformat()

        conn = get_connection(password)
        if not conn: return
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Expenses (category, amount, date) VALUES (%s, %s, %s)", (category, amount, date_today))
        conn.commit()
        cursor.close()
        conn.close()

        print(f"Expense of {amount} RWF for {category} recorded.")

    except ValueError:
        print("Invalid amount.")

    except Exception as e:
        print(f"Error storing expense: {e}")


def set_savings_goal(password=""):
    try:
        amount = float(input("Enter your savings goal amount (RWF): "))

        if amount < 0:
            print("Amount cannot be negative.")
            return

        description = input("Short description for this goal: ")
        target_date = input("Enter Target Date (YYYY-MM-DD): ")

        conn = get_connection(password)
        if not conn: return
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO Savings_goal (id, amount, description, target_date) VALUES (%s, %s, %s, %s)",
            (1, amount, description, target_date)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Saving goal added.\n")
    except ValueError:
        print("Invalid input. Amount should be a number.")
    except mysql.connector.errors.DataError:
        print("Invalid input. The target date should be in a date format.")
    except Exception as e:
        print(f" Error: {e}")


def view_summary(password=""):
    try:
        conn = get_connection(password)
        if not conn: return
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(amount) FROM Income")
        income = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(amount) FROM Expenses")
        expenses = cursor.fetchone()[0] or 0

        cursor.execute("SELECT amount FROM Savings_goal WHERE id = 1")
        result = cursor.fetchone()
        goal = result[0] if result else 0

        cursor.close()
        conn.close()

        balance = income - expenses
        print("\n Financial Summary")
        print(f"Total Income: RWF {income}")
        print(f"Total Expenses: RWF {expenses}")
        print(f"Current Balance: RWF {balance}")
        print(f"Savings Goal: RWF {goal}")
        visualize_percentage("Goal Achieved", balance, goal)
    except Exception as e:
        print(f" Error generating summary: {e}")


# ===== EXPORT REPORT =====
def export_report(password=""):
    try:
        conn = get_connection(password)
        if not conn: return
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(amount) FROM Income")
        income = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(amount) FROM Expenses")
        expenses = cursor.fetchone()[0] or 0

        cursor.execute("SELECT amount FROM Savings_goal WHERE id = 1")
        result = cursor.fetchone()
        goal = result[0] if result else 0
        date_today = datetime.date.today().isoformat()

        balance = income - expenses

        filename = "report.txt"
        if not filename.endswith(".txt"):
            filename += ".txt"

        with open(filename, "a") as f:
            f.write("MicroSaver Financial Report\n")
            f.write(f"Total Income: RWF {income}\n")
            f.write(f"Total Expenses: RWF {expenses}\n")
            f.write(f"Current Balance: RWF {balance}\n")
            f.write(f"Savings Goal: RWF {goal}\n")

            if goal > 0:
                progress = (balance / goal) * 100
                f.write(f"Goal Achievement: {progress:.2f}%\n")
            else:
                f.write("Goal Achievement: No goal set.\n")

            f.write(f"Summary done on {date_today}\n")
            f.write("-----------------------------------------\n")

        print(f"Report exported successfully to {filename}.\n")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f" Export failed: {e}")


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
    try:
        percentage = (value / total) * 100 if total else 0
        item = f"{name}: {percentage:.2f}%"
        print(item.ljust(25), end=" ")
        print("\n")
    except Exception as e:
        print(f"Visualization error: {e}")


def main():
    password = getpass("Enter your MySQL root password: ")

    setup_db(password=password)
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
            add_income(password=password)
        elif choice == '2':
            add_expenses(password=password)
        elif choice == '3':
            set_savings_goal(password=password)
        elif choice == '4':
            view_summary(password=password)
        elif choice == '5':
            export_report(password=password)
        elif choice == '6':
            print("Thank you for using MicroSaver. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
