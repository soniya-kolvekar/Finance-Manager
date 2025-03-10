import datetime
import json
import os
import math
from auth import register, authenticate, load_data, save_data  # Importing the functions from auth.py

# Add Expense
def add_expense(username):
    """Add an expense for the logged-in user."""
    category = input("Enter the expense category (e.g., Rent, Utilities, etc.): ")
    amount = float(input("Enter expense amount: "))
    description = input("Enter expense description (optional): ")

    # Get the current date automatically
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    data = load_data()
    user_data = data["users"][username]

    # Add the expense to the user data
    user_data["expenses"].append({"category": category, "amount": amount, "description": description, "date": date})

    # Check if the category exists in the budget and deduct the expense amount
    if category in user_data["budget"]:
        if user_data["budget"][category] >= amount:
            user_data["budget"][category] -= amount
            print(f"Expense added successfully! Remaining budget for {category}: ₹{user_data['budget'][category]}")
        else:
            print("Warning: Insufficient budget for this category!")
    else:
        print(f"No budget allocated for the category '{category}'. Expense added without budget adjustment.")

    save_data(data)

# View Expenses
def view_expenses(username):
    """View all expenses for the logged-in user."""
    data = load_data()
    user_data = data["users"][username]

    if not user_data["expenses"]:
        print("No expense records found!")
        return

    print("\n--- Expense Records ---")
    for i, expense in enumerate(user_data["expenses"], 1):
        print(f"{i}. ₹{expense['amount']} - {expense['category']} - {expense['description']} ({expense['date']})")

    total_expenses = sum(expense["amount"] for expense in user_data["expenses"])
    print(f"\nTotal Expenses: ₹{total_expenses}")

# Add Income
def add_income(username):
    """Add income for the logged-in user."""
    amount = float(input("Enter income amount: "))
    source = input("Enter income source: ")

    # Get the current date automatically
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    data = load_data()
    user_data = data["users"][username]
    user_data["income"].append({"amount": amount, "source": source, "date": date})
    user_data["balance"] += amount

    save_data(data)
    print("Income added successfully!")

# View Income
def view_income(username):
    """View all income records for the logged-in user."""
    data = load_data()
    user_data = data["users"][username]

    if not user_data["income"]:
        print("No income records found!")
        return

    print("\n--- Income Records ---")
    for i, income in enumerate(user_data["income"], 1):
        print(f"{i}. ₹{income['amount']} - {income['source']} ({income['date']})")

    total_income = sum(i["amount"] for i in user_data["income"])
    print(f"\nTotal Income: ₹{total_income}")

# Add Budget
def add_budget(username):
    """Add a budget for a specific category."""
    category = input("Enter the budget category (e.g., Rent, Utilities, etc.): ")
    amount = float(input("Enter budget amount: "))

    data = load_data()
    user_data = data["users"][username]
    user_data["budget"][category] = amount

    save_data(data)
    print(f"Budget for '{category}' set to ₹{amount}.")

# View Budget
def view_budget(username):
    """View all budget categories for the logged-in user."""
    data = load_data()
    user_data = data["users"][username]

    if not user_data["budget"]:
        print("No budgets set!")
        return

    print("\n--- Budget Allocation ---")
    for category, amount in user_data["budget"].items():
        print(f"{category}: ₹{amount}")
     
goals = {}
           
# Set a savings goal
def set_savings_goal(username):
    """Set a savings goal for the logged-in user."""
    goal_name = input("Enter the goal name (e.g., Vacation, Emergency Fund): ")
    target_amount = float(input("Enter the target amount for this goal (₹): "))

    data = load_data()
    user_data = data["users"][username]

    # Check if goal already exists
    if goal_name in user_data["goals"]:
        print(f"Goal '{goal_name}' already exists. Updating the target amount.")
    else:
        print(f"Setting a new savings goal '{goal_name}'.")

    # Set the goal with initial savings as 0
    user_data["goals"][goal_name] = {
        "target_amount": target_amount,
        "current_savings": 0
    }

    save_data(data)
    print(f"Goal '{goal_name}' set with a target amount of ₹{target_amount}.")

# Add savings to a goal
def add_savings(username):
    """Add savings towards a specific goal."""
    goal_name = input("Enter the goal name you want to add savings to: ")
    amount = float(input("Enter the amount to add towards the goal: "))

    data = load_data()
    user_data = data["users"][username]

    if goal_name not in user_data["goals"]:
        print(f"Goal '{goal_name}' not found. Please set the goal first.")
        return

    # Add the savings to the goal
    user_data["goals"][goal_name]["current_savings"] += amount

    save_data(data)
    print(f"₹{amount} added to your goal '{goal_name}'. Current savings: ₹{user_data['goals'][goal_name]['current_savings']}")

# View savings goals
def view_savings_goals(username):
    """View all savings goals and their progress."""
    data = load_data()
    user_data = data["users"][username]

    if not user_data["goals"]:
        print("No savings goals set!")
        return

    print("\n--- Savings Goals ---")
    for goal_name, goal_data in user_data["goals"].items():
        progress = goal_data["current_savings"]
        target = goal_data["target_amount"]
        remaining = target - progress
        print(f"Goal: {goal_name}")
        print(f"Target Amount: ₹{target}")
        print(f"Current Savings: ₹{progress}")
        print(f"Remaining Amount: ₹{remaining}")
        print("------------------------")

# Add Investment
def add_investment(username):
    """Add an investment for the logged-in user."""
    investment_type = input("Enter the investment type (e.g., Stocks, Mutual Funds, etc.): ")
    amount = float(input("Enter the amount invested: ₹"))
    start_date = input("Enter the investment start date (YYYY-MM-DD): ")

    data = load_data()
    user_data = data["users"][username]
    
    # Add investment to the user's investments list
    user_data["investments"].append({
        "type": investment_type,
        "amount": amount,
        "start_date": start_date,
        "current_value": amount  # Assuming the current value is the same initially
    })

    save_data(data)
    print(f"Investment in {investment_type} added successfully!")

# View Investments
def view_investments(username):
    """View all investments for the logged-in user."""
    data = load_data()
    user_data = data["users"][username]

    if not user_data["investments"]:
        print("No investments found!")
        return

    print("\n--- Investments ---")
    for i, investment in enumerate(user_data["investments"], 1):
        print(f"{i}. Type: {investment['type']}, Amount: ₹{investment['amount']}, "
              f"Start Date: {investment['start_date']}, Current Value: ₹{investment['current_value']}")

# Update Investment
def update_investment(username):
    """Update the current value of an investment."""
    data = load_data()
    user_data = data["users"][username]

    if not user_data["investments"]:
        print("No investments found!")
        return

    print("\n--- Investments ---")
    for i, investment in enumerate(user_data["investments"], 1):
        print(f"{i}. Type: {investment['type']}, Amount: ₹{investment['amount']}, "
              f"Start Date: {investment['start_date']}, Current Value: ₹{investment['current_value']}")

    # Choose an investment to update
    investment_index = int(input("Enter the number of the investment to update: ")) - 1
    if investment_index < 0 or investment_index >= len(user_data["investments"]):
        print("Invalid investment selection.")
        return

    # Update the current value
    new_value = float(input("Enter the new current value of the investment: ₹"))
    user_data["investments"][investment_index]["current_value"] = new_value

    save_data(data)
    print(f"Investment updated successfully! New current value: ₹{new_value}")


# Add Loan
def add_loan(username):
    """Add a loan for the logged-in user."""
    loan_name = input("Enter the loan name (e.g., Home Loan, Personal Loan): ")
    loan_amount = float(input("Enter the loan amount: ₹"))
    interest_rate = float(input("Enter the interest rate (annual, in percentage): "))
    tenure = int(input("Enter the loan tenure (in years): "))

    data = load_data()
    user_data = data["users"][username]

    # Add loan to the user's loans list
    user_data["loans"].append({
        "loan_name": loan_name,
        "loan_amount": loan_amount,
        "interest_rate": interest_rate,
        "tenure": tenure,
        "emi": calculate_emi(loan_amount, interest_rate, tenure),
        "remaining_amount": loan_amount  # Initially, the remaining amount is the loan amount
    })

    save_data(data)
    print(f"Loan '{loan_name}' added successfully!")

# View Loans
def view_loans(username):
    """View all loans for the logged-in user."""
    data = load_data()
    user_data = data["users"][username]

    if not user_data["loans"]:
        print("No loans found!")
        return

    print("\n--- Loans ---")
    for i, loan in enumerate(user_data["loans"], 1):
        print(f"{i}. Loan Name: {loan['loan_name']}, Amount: ₹{loan['loan_amount']}, "
              f"Interest Rate: {loan['interest_rate']}%, Tenure: {loan['tenure']} years, "
              f"EMI: ₹{loan['emi']}, Remaining Amount: ₹{loan['remaining_amount']}")

# Loan EMI Calculator
def calculate_emi(loan_amount, interest_rate, tenure):
    """Calculate the EMI for a loan."""
    monthly_interest_rate = interest_rate / 12 / 100  # Monthly interest rate
    months = tenure * 12  # Total number of months
    emi = loan_amount * monthly_interest_rate * math.pow(1 + monthly_interest_rate, months) / (math.pow(1 + monthly_interest_rate, months) - 1)
    return round(emi, 2)

# Add Debt
def add_debt(username):
    """Add a debt for the logged-in user."""
    debt_name = input("Enter the debt name (e.g., Credit Card, Personal Borrowing): ")
    debt_amount = float(input("Enter the debt amount: ₹"))
    due_date = input("Enter the debt due date (YYYY-MM-DD): ")

    data = load_data()
    user_data = data["users"][username]

    # Add debt to the user's debt list
    user_data["debts"].append({
        "debt_name": debt_name,
        "debt_amount": debt_amount,
        "due_date": due_date,
        "paid_amount": 0  # Initially, no amount is paid
    })

    save_data(data)
    print(f"Debt '{debt_name}' added successfully!")

# View Debts
def view_debts(username):
    """View all debts for the logged-in user."""
    data = load_data()
    user_data = data["users"][username]

    if not user_data["debts"]:
        print("No debts found!")
        return

    print("\n--- Debts ---")
    for i, debt in enumerate(user_data["debts"], 1):
        print(f"{i}. Debt Name: {debt['debt_name']}, Amount: ₹{debt['debt_amount']}, "
              f"Due Date: {debt['due_date']}, Paid Amount: ₹{debt['paid_amount']}, "
              f"Remaining Amount: ₹{debt['debt_amount'] - debt['paid_amount']}")

# Pay Loan
def pay_loan(username):
    """Make a payment towards a loan."""
    data = load_data()
    user_data = data["users"][username]

    if not user_data["loans"]:
        print("No loans to pay!")
        return

    print("\n--- Loans ---")
    for i, loan in enumerate(user_data["loans"], 1):
        print(f"{i}. Loan Name: {loan['loan_name']}, Remaining Amount: ₹{loan['remaining_amount']}")

    loan_index = int(input("Enter the number of the loan to pay: ")) - 1
    if loan_index < 0 or loan_index >= len(user_data["loans"]):
        print("Invalid loan selection.")
        return

    payment_amount = float(input("Enter the amount to pay towards the loan: ₹"))
    if payment_amount > user_data["loans"][loan_index]["remaining_amount"]:
        print("Payment exceeds remaining loan amount!")
        return

    # Update the remaining loan amount
    user_data["loans"][loan_index]["remaining_amount"] -= payment_amount
    save_data(data)
    print(f"₹{payment_amount} paid towards the loan. Remaining Amount: ₹{user_data['loans'][loan_index]['remaining_amount']}")

# Pay Debt
def pay_debt(username):
    """Make a payment towards a debt."""
    data = load_data()
    user_data = data["users"][username]

    if not user_data["debts"]:
        print("No debts to pay!")
        return

    print("\n--- Debts ---")
    for i, debt in enumerate(user_data["debts"], 1):
        print(f"{i}. Debt Name: {debt['debt_name']}, Remaining Amount: ₹{debt['debt_amount'] - debt['paid_amount']}")

    debt_index = int(input("Enter the number of the debt to pay: ")) - 1
    if debt_index < 0 or debt_index >= len(user_data["debts"]):
        print("Invalid debt selection.")
        return

    payment_amount = float(input("Enter the amount to pay towards the debt: ₹"))
    if payment_amount > (user_data["debts"][debt_index]["debt_amount"] - user_data["debts"][debt_index]["paid_amount"]):
        print("Payment exceeds remaining debt amount!")
        return

    # Update the paid amount
    user_data["debts"][debt_index]["paid_amount"] += payment_amount
    save_data(data)
    print(f"₹{payment_amount} paid towards the debt. Remaining Debt: ₹{user_data['debts'][debt_index]['debt_amount'] - user_data['debts'][debt_index]['paid_amount']}")

# Main Menu Update (Add Loan, View Loan, Pay Loan, Add Debt, View Debt, Pay Debt options)
def main_menu(username):
    """Display the main menu after successful login."""
    while True:
        print("\nFinance Manager")
        print("1. Add Income")
        print("2. View Income")
        print("3. Add Budget")
        print("4. View Budget")
        print("5. Add Expense")
        print("6. View Expenses")
        print("7. Set Savings Goal")
        print("8. Add Savings to Goal")
        print("9. View Savings Goals")
        print("10. Add Investment")
        print("11. View Investments")
        print("12. Update Investment")
        print("13. Add Loan")
        print("14. View Loans")
        print("15. Pay Loan")
        print("16. Add Debt")
        print("17. View Debts")
        print("18. Pay Debt")
        print("19. Logout")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            add_income(username)
        elif choice == "2":
            view_income(username)
        elif choice == "3":
            add_budget(username)
        elif choice == "4":
            view_budget(username)
        elif choice == "5":
            add_expense(username)
        elif choice == "6":
            view_expenses(username)
        elif choice == "7":
            set_savings_goal(username)
        elif choice == "8":
            add_savings(username)
        elif choice == "9":
            view_savings_goals(username)
        elif choice == "10":
            add_investment(username)
        elif choice == "11":
            view_investments(username)
        elif choice == "12":
            update_investment(username)
        elif choice == "13":
            add_loan(username)
        elif choice == "14":
            view_loans(username)
        elif choice == "15":
            pay_loan(username)
        elif choice == "16":
            add_debt(username)
        elif choice == "17":
            view_debts(username)
        elif choice == "18":
            pay_debt(username)
        elif choice == "19":
            print(f"Logging out {username}...")
            break
        else:
            print("Invalid choice! Please try again.")

# Main function
def main():
    """Main function to run the Finance Manager."""
    print("Welcome to Finance Manager!")
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            username = input("Enter a new username: ")
            password = input("Enter a new password: ")
            if register(username, password):  # Register function from auth.py
                print("Thank You For Registering")
        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if authenticate(username, password):  # Authenticate function from auth.py
                print(f"Login successful! Welcome, {username}.")
                main_menu(username)
            else:
                print("Invalid username or password.")
        elif choice == "3":
            print("Exiting Finance Manager...")
            print("Thank You")
            break
        else:
            print("Invalid option! Try again.")

if __name__ == "__main__":
    main()