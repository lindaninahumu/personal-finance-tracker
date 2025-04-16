import tkinter as tk
from tkinter import ttk, messagebox

class FinanceGUI:
    ## A constructor method that initialises GUI with root window
    def __init__(self, root, add_callback, update_callback, delete_callback, clear_callback):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("800x600")
        ## Setting bluish background theme
        ##self.root.configure(bg="#ADD8E6")  ## Light blue color
        self.add_callback = add_callback
        self.update_callback = update_callback
        self.delete_callback = delete_callback
        self.clear_callback = clear_callback
        self.create_widgets()

    ## A method that creates all GUI elements
    def create_widgets(self):
        ## A code responsible for creating a Form Frame
        form_frame = ttk.LabelFrame(self.root, text="Add/Edit Transaction", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)
        form_frame.configure(style="Blue.TLabelframe")
        
        ## A code responsible for creating Date textfield
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, tk.StringVar(value="2025-04-15").get())

        ## A code responsible for creating Description textfield
        ttk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        ## A code responsible for creating Amount textfield
        ttk.Label(form_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        ## A code responsible for creating a combo box (Category)
        ttk.Label(form_frame, text="Category:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.category_combo = ttk.Combobox(form_frame, values=["Income", "Expense", "Savings"])
        self.category_combo.grid(row=3, column=1, padx=5, pady=5)
        self.category_combo.set("Expense")

        ## A code responsible for creating all the Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Add Transaction", command=self.add_callback).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Transaction", command=self.update_callback).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Transaction", command=self.delete_callback).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_callback).pack(side="left", padx=5)

        ## A code responsible for creating Transactions table
        table_frame = ttk.LabelFrame(self.root, text="Transactions", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        table_frame.configure(style="Blue.TLabelframe")

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Date", "Description", "Amount", "Category"),
            show="headings",
            selectmode="browse"  ## Ensure single selection
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        ## Set column widths for better visibility
        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Description", width=200)
        self.tree.column("Amount", width=100)
        self.tree.column("Category", width=100)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        ## Ensure Treeview has focus
        self.tree.focus_set()

        ## Configure style for bluish theme and Treeview selection
        style = ttk.Style()
        style.theme_use("vista")  ## Use Windows default theme
        ##style.configure("Blue.TLabelframe", background="#ADD8E6")
        ##style.configure("Blue.TLabelframe.Label", background="#ADD8E6")
        style.configure("Treeview", background="#F0F8FF", fieldbackground="#F0F8FF", foreground="black")
        style.map("Treeview",
                  background=[("selected", "#4682B4")],
                  foreground=[("selected", "white")])  ## Highlight with contrast
        print("Treeview style applied")  ## Debug

    ## A method that populates form when a transaction is selected
    def on_tree_select(self, event):
        selected = self.tree.selection()
        print("Selected row:", selected)  ## Debug
        if selected:
            item = self.tree.item(selected[0])
            values = item["values"]
            print("Selected values:", values)  ## Debug
            if values:
                ## Populate form without clearing selection
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, str(values[1]))
                self.desc_entry.delete(0, tk.END)
                self.desc_entry.insert(0, str(values[2]))
                self.amount_entry.delete(0, tk.END)
                self.amount_entry.insert(0, str(values[3]))
                self.category_combo.set(str(values[4]))
        else:
            self.clear_form()

    ## A method that clears form fields
    def clear_form(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, tk.StringVar(value="2025-04-15").get())
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_combo.set("Expense")
        ## Avoid clearing Treeview selection
        # self.tree.selection_remove(self.tree.selection())

    ## A method that loads transactions into table
    def load_transactions(self, transactions):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in transactions:
            self.tree.insert("", "end", values=row)
        print("Transactions loaded:", transactions)  ## Debug

    ## A method that gets form data
    def get_form_data(self):
        return (
            self.date_entry.get(),
            self.desc_entry.get().strip(),
            self.amount_entry.get(),
            self.category_combo.get()
        )

    ## A method that gets selected transaction ID
    def get_selected_transaction_id(self):
        selected = self.tree.selection()
        print("Getting selected ID, selection:", selected)  ## Debug
        if selected:
            item = self.tree.item(selected[0])
            values = item["values"]
            if values:
                print("Selected ID:", values[0])  ## Debug
                return values[0]
        return None

    ## A method that shows error message
    def show_error(self, title, message):
        messagebox.showerror(title, message)

    ## A method that shows info message
    def show_info(self, title, message):
        messagebox.showinfo(title, message)

    ## A method that shows warning message
    def show_warning(self, title, message):
        messagebox.showwarning(title, message)

    ## A method that shows confirmation dialog
    def confirm_delete(self):
        return messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction?")