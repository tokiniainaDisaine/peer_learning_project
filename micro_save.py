#!/usr/bin/python3
"""
MicroSave - Personal Finance Tracker

This application helps users track their income, expenses, and savings goals.
It uses a MySQL database to store financial records and provides summary reports.

Features:
- Add income and expenses
- Set and track savings goals
- View financial summaries
- Export reports to text files

Author: Group Coding Lab 4
Date: 2025-07-28
"""


import mysql.connector
import datetime
from getpass import getpass

# =========================
# Database Setup Functions
# =========================

def setup_db(host="localhost", user="root", password="", database="microsave"):
    """
    Sets up the MySQL database and required tables for MicroSave.
    Creates the database and tables if they do not exist.

    Args:
        host (str): MySQL server host
        user (str): MySQL username
        password (str): MySQL password
        database (str): Database name

    Returns:
        None
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


# =========================
# Database Connection
# =========================

def get_connection(password=""):
    """
    Establishes a connection to the MicroSave MySQL database.

    Args:
        password (str): MySQL password

    Returns:
        mysql.connector.connection.MySQLConnection or None
    """
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


# =========================
# User Interface Functions
# =========================

def show_welcome_screen():
    """
    Displays the welcome screen and prompts the user to continue.

    Returns:
        None
    """
    print(">>> Welcome to MicroSaver!")
    print("Your app to track your finances properly.")
    choice = input("Do you wish to continue? [Y/n]: ").strip().lower()
    if choice != 'y':
        print("Goodbye!")
        exit()
        

# =========================
# Income Functions
# =========================

def add_income(password=""):
    """
    Prompts the user to add an income record to the database.

    Args:
        password (str): MySQL password

    Returns:
        None
    """
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


# =========================
# Expense Functions
# =========================

def add_expenses(password=""):
    """
    Prompts the user to add an expense record to the database.

    Args:
        password (str): MySQL password

    Returns:
        None
    """

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


# =========================
# Savings Goal Functions
# =========================

def set_savings_goal(password=""):
    """
    Prompts the user to set or update a savings goal.

    Args:
        password (str): MySQL password

    Returns:
        None
    """
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


# =========================
# Summary Functions
# =========================

def view_summary(password=""):
    """
    Displays a summary of total income, expenses, balance, and savings goal.

    Args:
        password (str): MySQL password

    Returns:
        None
    """
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


def view_long_summary(password=""):
    """
    Displays a detailed summary including all expense records.

    Args:
        password (str): MySQL password

    Returns:
        None
    """
    try:
        conn = get_connection(password)
        if not conn: return
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(amount) FROM Income")
        income = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(amount) FROM Expenses")
        expenses = cursor.fetchone()[0] or 0

        cursor.execute("SELECT * FROM Expenses")
        expenses_list = cursor.fetchall() or 0

        cursor.execute("SELECT amount FROM Savings_goal WHERE id = 1")
        result = cursor.fetchone()
        goal = result[0] if result else 0

        cursor.close()
        conn.close()

        balance = income - expenses
        print("\n Financial Summary")
        print(f"Total Income: RWF {income}")
        print("Expenses list:")
        for expense in expenses_list:
            print(f"    {expense[1]}: RWF {expense[2]} on {expense[3]}")
        print(f"Total Expenses: RWF {expenses}")
        print(f"Current Balance: RWF {balance}")
        print(f"Savings Goal: RWF {goal}")
        visualize_percentage("Goal Achieved", balance, goal)
    except Exception as e:
        print(f" Error generating summary: {e}")


# =========================
# Report Export Function
# =========================

def export_report(password=""):
    """
    Exports a financial summary report to a text file.

    Args:
        password (str): MySQL password

    Returns:
        None
    """
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


# =========================
# Visualization Function
# =========================

def visualize_percentage(name, value, total):
    """
    Prints a visual representation of the percentage achieved towards a goal.

    Args:
        name (str): Name of the metric
        value (int): Current value
        total (int): Goal value

    Returns:
        None
    """
    try:
        percentage = (value / total) * 100 if total else 0
        if percentage > 100:
            print("Your goal has been reached")
        item = f"{name}: {percentage:.2f}%"
        print(item.ljust(25), end=" ")
    except Exception as e:
        print(f"Visualization error: {e}")


# =========================
# Main Application Loop
# =========================

def main():
    """
    Main function to run the MicroSave application.
    Handles user interaction and menu navigation.

    Returns:
        None
    """
    password = getpass("Enter your MySQL root password: ")

    setup_db(password=password)
    show_welcome_screen()

    while True:
        print("\n-----Main Menu-----")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Set Savings Goal")
        print("4. View Summary")
        print("5. View Long Summary")
        print("6. Export Report")
        print("7. Exit")

        choice = input("Choose an option [1-7]: ").strip()

        if choice == '1':
            add_income(password=password)
        elif choice == '2':
            add_expenses(password=password)
        elif choice == '3':
            set_savings_goal(password=password)
        elif choice == '4':
            view_summary(password=password)
        elif choice == '5':
            view_long_summary(password=password)
        elif choice == '6':
            export_report(password=password)
        elif choice == '7':
            print("Thank you for using MicroSaver. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
