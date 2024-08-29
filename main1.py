import sqlite3

class Expenses:
    def __init__(self, date, description, amount):
        self.date = date
        self.description = description
        self.amount = amount


class Income:
    def __init__(self, amount):
        self.amount = amount


class ExpenseManagement:
    def __init__(self):
        self.conn = sqlite3.connect("main.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.expenses = []  # Initialize 'expenses' list
        self.income = None  # Initialize income
        self.load_expenses_from_db()  # Load existing expenses from the database

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                description TEXT,
                amount REAL
            )
        ''')
        self.conn.commit()

    def load_expenses_from_db(self):
        self.cursor.execute('SELECT id, date, description, amount FROM expenses')
        rows = self.cursor.fetchall()
        self.expenses = [Expenses(date, description, amount) for _, date, description, amount in rows]

    def add_expenses(self, expense):
        # Add to both the in-memory list and the database
        self.expenses.append(expense)
        self.cursor.execute('INSERT INTO expenses (date, description, amount) VALUES (?, ?, ?)',
                            (expense.date, expense.description, expense.amount))
        self.conn.commit()
        print("Expense added successfully.")

    def remove_expenses(self):
        print("How would you like to delete an expense?")
        print("1. By Date")
        print("2. By Description")
        print("3. By Amount")
        delete_choice = input("Enter your choice (1-3): ")

        if delete_choice == '1':
            date = input("Enter the date of the expense to delete (YYYY-MM-DD): ")
            self.cursor.execute('DELETE FROM expenses WHERE date = ?', (date,))
            self.conn.commit()
            self.expenses = [exp for exp in self.expenses if exp.date != date]
            print("Expenses with the specified date deleted successfully.")

        elif delete_choice == '2':
            description = input("Enter the description of the expense to delete: ")
            self.cursor.execute('DELETE FROM expenses WHERE description = ?', (description,))
            self.conn.commit()
            self.expenses = [exp for exp in self.expenses if exp.description != description]
            print("Expenses with the specified description deleted successfully.")

        elif delete_choice == '3':
            try:
                amount = float(input("Enter the amount of the expense to delete: "))
                self.cursor.execute('DELETE FROM expenses WHERE amount = ?', (amount,))
                self.conn.commit()
                self.expenses = [exp for exp in self.expenses if exp.amount != amount]
                print("Expenses with the specified amount deleted successfully.")
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
        else:
            print("Invalid choice. Please try again.")

    def update_expense(self, index, field, new_value):
        if 0 <= index < len(self.expenses):
            expense = self.expenses[index]
            if field == 'date':
                self.cursor.execute('UPDATE expenses SET date = ? WHERE date = ? AND description = ? AND amount = ?',
                                    (new_value, expense.date, expense.description, expense.amount))
                expense.date = new_value
            elif field == 'description':
                self.cursor.execute('UPDATE expenses SET description = ? WHERE date = ? AND description = ? AND amount = ?',
                                    (new_value, expense.date, expense.description, expense.amount))
                expense.description = new_value
            elif field == 'amount':
                self.cursor.execute('UPDATE expenses SET amount = ? WHERE date = ? AND description = ? AND amount = ?',
                                    (new_value, expense.date, expense.description, expense.amount))
                expense.amount = float(new_value)

            self.conn.commit()
            print(f"Expense {field} updated successfully.")
        else:
            print("Invalid expense index.")

    def view_expenses(self):
        if not self.expenses:
            print("No expenses found.")
        else:
            print("Expense list:")
            for exp in self.expenses:
                print(f"Date: {exp.date}, Description: {exp.description}, Amount: {exp.amount:.2f}")

    def total_expenses(self):
        if not self.expenses:
            print("No expenses to calculate.")
            return 0.0
        total = sum(exp.amount for exp in self.expenses)
        print(f"Total expenses: {total:.2f}")
        return total

    def add_income(self, income):
        # Set income
        self.income = Income(income)
        print("Income added successfully.")

    def final_balance(self):
        if self.income is None:
            print("No income added. Please add your income first.")
        else:
            total_expenses = self.total_expenses()
            balance = self.income.amount - total_expenses
            print(f"Total Income: {self.income.amount:.2f}")
            print(f"Total Expenses: {total_expenses:.2f}")
            print(f"Final Balance: {balance:.2f}")


tracker = ExpenseManagement()

while True:
    print("\nWelcome to the finance expenses management!")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Update Expense")
    print("5. Total Expenses")
    print("6. Add Income")
    print("7. Show Final Balance")
    print("8. Exit")

    choice = input("Enter your choice (1-8): ")

    if choice == '1':
        date = input("Enter the date (YYYY-MM-DD): ")
        description = input("Enter the description: ")
        try:
            amount = float(input("Enter the amount: "))
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            continue
        expense = Expenses(date, description, amount)
        tracker.add_expenses(expense)

    elif choice == '2':
        tracker.view_expenses()

    elif choice == '3':
        tracker.remove_expenses()

    elif choice == '4':
        try:
            index = int(input("Enter the expense index to update: ")) - 1
            print("What would you like to update?")
            print("1. Date")
            print("2. Description")
            print("3. Amount")
            update_choice = input("Enter your choice (1-3): ")

            if update_choice == '1':
                new_date = input("Enter the new date (YYYY-MM-DD): ")
                tracker.update_expense(index, 'date', new_date)
            elif update_choice == '2':
                new_description = input("Enter the new description: ")
                tracker.update_expense(index, 'description', new_description)
            elif update_choice == '3':
                try:
                    new_amount = float(input("Enter the new amount: "))
                    tracker.update_expense(index, 'amount', new_amount)
                except ValueError:
                    print("Invalid amount. Please enter a valid number.")
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")

    elif choice == '5':
        tracker.total_expenses()

    elif choice == '6':
        try:
            income_amount = float(input("Enter your income amount: "))
            tracker.add_income(income_amount)
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    elif choice == '7':
        tracker.final_balance()

    elif choice == '8':
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please try again.")
