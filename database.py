import sqlite3

class FinanceDatabase:
    ## A constructor method that initialises database (finance_tracker.db) connection
    def __init__(self, db_name="finance_tracker.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.setup_database()

    ## A method that Sets up (create) the transactions table
    def setup_database(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL
                )
            """)
            self.conn.commit()
            print("Database initialized")  ## Debug
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to initialize database: {e}")

    ## A method that inserts a new transaction in the transactions table
    def add_transaction(self, date, description, amount, category):
        try:
            self.cursor.execute(
                "INSERT INTO transactions (date, description, amount, category) VALUES (?, ?, ?, ?)",
                (date, description, amount, category)
            )
            self.conn.commit()
            print(f"Added transaction: {date}, {description}, {amount}, {category}")  ## Debug
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to add transaction: {e}")

    ## A method that fetches all transactions from the transactions table
    def get_all_transactions(self):
        try:
            self.cursor.execute("SELECT * FROM transactions")
            transactions = self.cursor.fetchall()
            print("Fetched transactions:", transactions)  ## Debug
            return transactions
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to load transactions: {e}")

    ## A method that updates an existing transaction in the transactions table
    def update_transaction(self, trans_id, date, description, amount, category):
        try:
            self.cursor.execute(
                "UPDATE transactions SET date = ?, description = ?, amount = ?, category = ? WHERE id = ?",
                (date, description, amount, category, trans_id)
            )
            self.conn.commit()
            print(f"Updated transaction ID {trans_id}: {date}, {description}, {amount}, {category}")  ## Debug
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to update transaction: {e}")

    ## A method that deletes a transaction from the transactions table
    def delete_transaction(self, trans_id):
        try:
            self.cursor.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
            self.conn.commit()
            print(f"Deleted transaction ID {trans_id}")  ## Debug
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to delete transaction: {e}")

    ## A method that closes database connection
    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")  ## Debug