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
            amount DECIMAL(10,2),
            date DATE
        )
    """)

    # Create Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(255),
            amount DECIMAL(10,2),
            date DATE
        )
    """)

    # Create Savings_goal table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Savings_goal (
            id INT PRIMARY KEY,
            amount DECIMAL(10,2)
        )
    """)

    cursor.close()
    conn.close()
    print("Database and tables are set up.")


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



# User input 
"""
For the user input,

We'll need to get those variables:

Main expenses:
-income
-food_expense
-rent_expense
-transportation

Optional:
Asks the user for the expense name
Then asks how much does it cost
Store in dictionary:
other_expenses = {
    "expense_name": value
}
"""

# Calculate the present income/expense


# Calculate the target income/expense
# f(x) = 100 / x
