import re
from datetime import datetime

class FinanceLogic:
    ## A constructor method that Initialises with database instance
    def __init__(self, db):
        self.db = db

    ## A method that validates form inputs
    def validate_inputs(self, date, description, amount, category):
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(date_pattern, date):
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date.")
        if not description.strip():
            raise ValueError("Description cannot be empty.")
        try:
            amount_val = float(amount)
            if amount_val <= 0:
                raise ValueError("Amount must be positive.")
        except ValueError:
            raise ValueError("Invalid amount. Enter a positive number.")
        if not category:
            raise ValueError("Please select a category.")
        return True

    ## A method that adds a transaction
    def add_transaction(self, date, description, amount, category):
        try:
            if self.validate_inputs(date, description, amount, category):
                self.db.add_transaction(date, description, float(amount), category)
                print(f"Logic: Added transaction: {date}, {description}, {amount}, {category}")  ## Debug
                return True, "Transaction added successfully!"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Failed to add transaction: {e}"

    ## A method that updates a transaction
    def update_transaction(self, trans_id, date, description, amount, category):
        if not trans_id:
            return False, "Please select a transaction to update."
        try:
            if self.validate_inputs(date, description, amount, category):
                self.db.update_transaction(trans_id, date, description, float(amount), category)
                print(f"Logic: Updated transaction ID {trans_id}: {date}, {description}, {amount}, {category}")  ## Debug
                return True, "Transaction updated successfully!"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Failed to update transaction: {e}"

    ## A method that deletes a transaction
    def delete_transaction(self, trans_id):
        if not trans_id:
            return False, "Please select a transaction to delete."
        try:
            self.db.delete_transaction(trans_id)
            print(f"Logic: Deleted transaction ID {trans_id}")  ## Debug
            return True, "Transaction deleted successfully!"
        except Exception as e:
            return False, f"Failed to delete transaction: {e}"

    ## A method that loads all transactions
    def load_transactions(self):
        try:
            transactions = self.db.get_all_transactions()
            print("Logic: Loaded transactions:", transactions)  ## Debug
            return transactions
        except Exception as e:
            raise Exception(f"Failed to load transactions: {e}")