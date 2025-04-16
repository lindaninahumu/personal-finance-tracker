import tkinter as tk
from database import FinanceDatabase
from gui import FinanceGUI
from application_logic import FinanceLogic

class FinanceTrackerApp:
    ## Initialize app components
    def __init__(self, root):
        self.db = FinanceDatabase()
        self.logic = FinanceLogic(self.db)
        self.gui = FinanceGUI(
            root,
            self.add_transaction,
            self.update_transaction,
            self.delete_transaction,
            self.clear_form
        )
        self.load_transactions()

    ## A method that handles add transaction
    def add_transaction(self):
        date, description, amount, category = self.gui.get_form_data()
        success, message = self.logic.add_transaction(date, description, amount, category)
        if success:
            self.gui.show_info("Success", message)
            self.gui.clear_form()
            self.load_transactions()
        else:
            self.gui.show_error("Input Error", message)

    ## A method that handles update transaction
    def update_transaction(self):
        trans_id = self.gui.get_selected_transaction_id()
        print("Update attempted, trans_id:", trans_id)  ## Debug
        if trans_id is None:
            self.gui.show_warning("Selection Error", "Please select a transaction to update.")
            return
        date, description, amount, category = self.gui.get_form_data()
        success, message = self.logic.update_transaction(trans_id, date, description, amount, category)
        if success:
            self.gui.show_info("Success", message)
            self.gui.clear_form()
            self.load_transactions()
        else:
            self.gui.show_error("Input Error", message)

    ## A method that handles delete transaction
    def delete_transaction(self):
        trans_id = self.gui.get_selected_transaction_id()
        print("Delete attempted, trans_id:", trans_id)  ## Debug
        if trans_id is None:
            self.gui.show_warning("Selection Error", "Please select a transaction to delete.")
            return
        if self.gui.confirm_delete():
            success, message = self.logic.delete_transaction(trans_id)
            if success:
                self.gui.show_info("Success", message)
                self.gui.clear_form()
                self.load_transactions()
            else:
                self.gui.show_error("Error", message)

    ## A method that clears form
    def clear_form(self):
        self.gui.clear_form()

    ## A method that loads transactions into GUI
    def load_transactions(self):
        try:
            transactions = self.logic.load_transactions()
            self.gui.load_transactions(transactions)
        except Exception as e:
            self.gui.show_error("Error", f"Failed to load transactions: {e}")

    ## A method that cleans up on exit
    def __del__(self):
        self.db.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()