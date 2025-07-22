#!/usr/bin/python3
"""
Welcome to MicroSave :)

The app to help you reach your financial goals
"""

# Functions

def visualize_percentage(name, value, total):
    """
    Function that give a visual representation of a percentage,
    Prints the representation as "#"

    Args: 
        name (string):
        value (int):

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
"""

# Calculate the present income/expense

income = 500_000
food = 100_000
rent = 150_000
transportation = 30_000

print("According to our calculactions")
print("Here is a visual representation of your income/exepnses")

visualize_percentage("Income", income, income)
visualize_percentage("Food", food, income)
visualize_percentage("Rent", rent, income)
visualize_percentage("Transportation", transportation, income)

# Calculate the target income/expense
# f(x) = 100 / x 
