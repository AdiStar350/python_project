"""
Finance Module

This module provides functionality for managing personal finance transactions.
It includes functions to load, add, save, and view transactions, as well as 
filter transactions by category or summarize them by month.
"""

import re # Regex Module
from datetime import date, datetime # Date and Time Module
from typing import List, Dict, Any # Type Annotation Module

# List to store all transactions
transactions: List[Dict[str, Any]] = []

# File path for storing transactions
FILE_PATH: str = "transactions.csv"


def load_transactions() -> None:
    """
    Load transactions from a CSV file into the transactions list.
    """
    # Opening the csv file in reading mode
    with open(FILE_PATH, "r", encoding="UTF-8") as file:
        # Iterating over each row in the file
        for row in file:
            row = row.strip()

            # If there is data in the row, set it in the matching variables
            # and add the transaction to the list
            if row:
                trans_type, amount, category, dt_str = [
                    element.strip() for element in row.split(",")
                ]
                add_transaction(trans_type, amount, category, dt_str)


def add_transaction(
    trans_type: str,
    amount: float,
    category: str,
    dt_str: str
) -> None:
    """
    Add a new transaction to the transactions list.

    Args:
        trans_type (str): Type of transaction ('income' or 'outcome').
        amount (float): Amount of the transaction.
        category (str): Category of the transaction.
        dt_str (str): Date of the transaction in 'dd-mm-yyyy' format.

    Raises:
        ValueError: If the transaction type, amount, or date format is invalid.
    """
    # Removing unnecessary whitespace
    trans_type = trans_type.strip()
    category = category.strip()

    # Validating transaction type input
    if trans_type not in ("income", "outcome"):
        raise ValueError("Transaction type is invalid")

    # Validating transaction category input
    if not category:
        raise ValueError("Category cannot be empty")

    # Validating transaction amount input
    try:
        amount = float(amount.strip())

        if amount < 0:
            raise ValueError
    except ValueError as err:
        raise ValueError("Invalid input.\nEnter only a positive number.") from err

    # Validating transaction date input
    try:
        dt: date = datetime.strptime(dt_str, "%d-%m-%Y").date()

        if dt > datetime.now().date():
            raise ValueError("Date cant be in the future.")
    except ValueError as err:
        raise ValueError("Invalid date input. Enter: (Day-Month-Year).") from err

    # Adding the transaction details to the list in the form of a dictionary
    transactions.append({
		"type": trans_type,
		"amount": amount,
		"category": category,
		"date": dt
	})

    # Sorting transactions by date in descending order (most recent date at the end)
    transactions.sort(key=lambda trans: trans["date"])


def save_transactions() -> None:
    """
    Save all transactions to a CSV file.
    """

    # Opening the csv file in writing mode
    with open(FILE_PATH, "w", encoding="UTF-8") as file:
        # Iterating over each transaction in the transactions list
        # and adding the it as a row to the csv file
        for trans in transactions:
            file.write(f"{trans["type"]},{trans["amount"]},{trans["category"]},\
                {trans["date"].strftime("%d-%m-%Y").strip()}\n")


def view_summary() -> None:
    """
    Display a summary of all transactions, including total income, outcome, 
    and balance.
    """
    # Get the total amount of all incomes
    total_income: float = sum(
		trans["amount"] for trans in transactions
		if trans["type"] == "income"
	)

    # Get the total amount of all outcomes
    total_outcome: float = sum(
		trans["amount"] for trans in transactions
		if trans["type"] == "outcome"
	)

    # Getting the difference as the current balance
    total_balance: float = total_income - total_outcome

    # Printing all transactions
    if transactions:
        print("\n--- Overall Summary ---")

        for trans in transactions:
            print(f"Type: {trans["type"].upper()}, Amount: {trans["amount"]:10.2f}, "
                  f"Date: {trans["date"].strftime("%d-%m-%Y")}\n")

        print(f"Total Income : {total_income:10.2f}")
        print(f"Total Outcome: {total_outcome:10.2f}")
        print(f"Total Balance: {total_balance:10.2f}")
    else:
        print("No transactions found.")


def view_monthly_summary() -> None:
    """
    Display a summary of transactions for a specific month and year.

    Prompts the user to enter the month and year, and filters transactions 
    accordingly.
    """
    # Get user input
    month: str = input("Enter month: ").strip()
    year: str = input("Enter Year: ").strip()
    # A regex pattern to look for a certain month and year.
    reg: str = rf"^\d{{2}}-{month.zfill(2)}-{year.zfill(4)}$"

    # Validate the input and converting the them to integers
    try:
        month = int(month)
        year = int(year)

        if month > 12 or month < 1 or year > datetime.now().year:
            raise ValueError
    except ValueError as err:
        raise ValueError("Invalid date values.\nEnter a valid month and year.") from err

    # Creating a new list with only the transactions matching the regex
    monthly_transactions: List[Dict[str, Any]] = [
        trans for trans in transactions
        if re.match(reg, trans["date"].strftime("%d-%m-%Y")) is not None
    ]

    # Get the total amount of matching incomes
    month_income: float = sum(
		trans["amount"] for trans in monthly_transactions
		if trans["type"] == "income"
	)

    # Get the total amount of matching outcomes
    month_outcome: float = sum(
		trans["amount"] for trans in monthly_transactions
		if trans["type"] == "outcome"
	)

    # Printing all the matching transactions and the totals
    if monthly_transactions:
        print(f"\n--- Summary for {year}-{month:02d} ---\n")

        for trans in monthly_transactions:
            print(f"Type: {trans["type"].upper()}, Amount: {trans["amount"]:10.2f}, "
                  f"Category: {trans["category"]}, Date: {trans["date"].strftime("%d-%m-%Y")}\n")

        print(f"Total Monthly Income : {month_income:10.2f}")
        print(f"Total Monthly Outcome: {month_outcome:10.2f}")
    else:
        print("No transactions found for this month.")


def filter_by_category() -> None:
    """
    Filter transactions by a specific category and display a summary.

    Prompts the user to enter a category and filters transactions accordingly.
    """
    # Getting input
    category: str = input("Enter category: ").lower().strip()

    # Creating a new list with only the transactions matching the category input
    category_transactions: List[Dict[str, Any]] = [
        trans for trans in transactions
        if trans['category'] == category
    ]

    # Get the total amount of matching incomes
    category_income: float = sum(
		trans["amount"] for trans in category_transactions
		if trans["type"] == "income"
	)

    # Get the total amount of matching outcomes
    category_outcome: float = sum(
		trans["amount"] for trans in category_transactions
		if trans["type"] == "outcome"
	)

    # Printing all the matching transactions and the totals
    if category_transactions:
        print(f"\n--- Summary for {category} transaction ---\n")

        for trans in category_transactions:
            print(f"Type: {trans["type"].upper()}, Amount: {trans["amount"]:10.2f}, "
                  f"Date: {trans["date"].strftime("%d-%m-%Y")}\n")

            category = category.title()

            print(f"Total Income of {category} : {category_income:10.2f}")
            print(f"Total Outcome of {category}: {category_outcome:10.2f}")
    else:
        print("No transactions found for this category.")
