"""
Personal Finance Tracker

This script provides a command-line interface for managing personal finances.
Users can add transactions, view summaries, filter transactions by category, 
and save their data.
"""

from finance import (
    load_transactions,
	add_transaction,
	view_summary,
	view_monthly_summary,
	filter_by_category,
	save_transactions
)


def main():
    """
    Main function to run the Personal Finance Tracker application.

    It loads transactions and provides a menu for the user to interact with 
    the application. The user can add transactions, view summaries, filter 
    transactions, and save their data before exiting.
    """
    # Load existing transactions from storage
    load_transactions()

    while True:
        # Display the main menu
        print("\n=== Personal Finance Tracker ===")
        print("""
            \r1. Add Transaction
			\r2. View Summary
			\r3. View Monthly Summary
			\r4. Filter by Category
			\r5. Save and Exit
   		""")

        # Get user choice
        choice = input("Choose an option (1-5): ")

        match choice:
            case "1":
                # Prompt user for transaction details
                trans_type: str = input("Enter the type of transaction " +
                                        "(income / outcome): ").lower()
                amount: float = input("Enter the transaction amount: ")
                category: str = input("Enter the transaction category: ").lower()
                dt_str: str = input("Enter the date (dd-mm-yyyy): ")

                # Add the transaction
                add_transaction(trans_type, amount, category, dt_str)
            case "2":
                # View summary of all transactions
                view_summary()
            case "3":
                # View summary grouped by month
                view_monthly_summary()
            case "4":
                # Filter transactions by category
                filter_by_category()
            case "5":
                # Save transactions and exit the application
                save_transactions()
                print("Goodbye!")
                break
            case _:
                # Handle invalid menu choices
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
