import sys
import csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QDialog, QTextEdit, QMessageBox, QFormLayout, QGroupBox, QInputDialog, QComboBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt

TRANSACTIONS_FILE = 'transactions.csv'
transactions = []

# Define categories
income_categories = [
    "Salary/Wages", "Freelance/Consulting", "Business Income", "Investment Income",
    "Rental Income", "Interest Income", "Dividends", "Bonuses", "Gifts",
    "Government Benefits", "Scholarships/Grants", "Royalties", "Alimony/Child Support",
    "Other Income"
]

expense_categories = [
    "Housing/Rent/Mortgage", "Utilities (Electricity, Water, Gas)", "Groceries/Food",
    "Transportation (Fuel, Public Transit)", "Insurance (Health, Auto, Home)",
    "Healthcare (Medical Bills, Prescriptions)", "Education (Tuition, Books)",
    "Entertainment (Movies, Events)", "Dining Out (Restaurants, Cafes)", "Clothing/Apparel",
    "Personal Care (Haircuts, Toiletries)", "Childcare/Schooling", "Savings/Investments",
    "Debt Repayment (Loans, Credit Cards)", "Travel/Vacation", "Home Maintenance/Repairs",
    "Gifts/Donations", "Subscriptions (Magazines, Streaming Services)",
    "Office Supplies/Business Expenses", "Other Expenses"
]

def load_transactions():
    global transactions
    transactions = []
    try:
        with open(TRANSACTIONS_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append({
                    'amount': float(row['amount']),
                    'type': row['type'],
                    'description': row['description'],
                    'category': row['category']
                })
    except FileNotFoundError:
        transactions = []

def save_transactions():
    with open(TRANSACTIONS_FILE, mode='w', newline='') as file:
        fieldnames = ['amount', 'type', 'description', 'category']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction)

def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()

class AddTransactionDialog(QDialog):
    def __init__(self, t_type, transaction=None, index=None):
        super().__init__()
        self.t_type = t_type
        self.transaction = transaction
        self.index = index
        self.setWindowTitle(f"Add {t_type.capitalize()}" if not transaction else f"Edit {t_type.capitalize()}")
        self.setStyleSheet(load_stylesheet("MacOS.qss"))
        self.init_ui()
        
    def init_ui(self):
        layout = QFormLayout()
        
        self.amount_input = QLineEdit()
        self.description_input = QTextEdit()
        self.category_input = QComboBox()
        
        # Set categories based on transaction type
        if self.t_type == 'income':
            self.category_input.addItems(income_categories)
        else:
            self.category_input.addItems(expense_categories)
        
        if self.transaction:
            self.amount_input.setText(str(self.transaction['amount']))
            self.description_input.setText(self.transaction['description'])
            self.category_input.setCurrentText(self.transaction['category'])
        
        self.add_button = QPushButton("Add" if not self.transaction else "Update")
        self.add_button.clicked.connect(self.add_transaction)
        
        layout.addRow("Amount:", self.amount_input)
        layout.addRow("Description:", self.description_input)
        layout.addRow("Category:", self.category_input)
        layout.addRow(self.add_button)
        
        self.setLayout(layout)
        
    def add_transaction(self):
        try:
            amount = float(self.amount_input.text())
            description = self.description_input.toPlainText()
            category = self.category_input.currentText()
            if not description:
                raise ValueError("Description cannot be empty.")
            transaction = {
                'amount': amount,
                'type': self.t_type,
                'description': description,
                'category': category
            }
            if self.transaction:
                transactions[self.index] = transaction
            else:
                transactions.append(transaction)
            save_transactions()  # Save to CSV
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))

class FinanceTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Finance Tracker")
        self.setGeometry(100, 100, 800, 600)
        load_transactions()  # Load transactions from CSV
        self.init_ui()
        
    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.summary_label = QLabel()
        self.summary_label.setFont(QFont('Arial', 18))
        self.summary_label.setAlignment(Qt.AlignCenter)
        self.update_summary()
        
        self.buttons_layout = QHBoxLayout()
        self.income_group = QGroupBox("Income")
        self.expense_group = QGroupBox("Expenses")
        
        self.income_layout = QVBoxLayout()
        self.add_income_button = QPushButton("Add Income")
        self.add_income_button.clicked.connect(lambda: self.open_add_transaction_dialog('income'))
        self.income_layout.addWidget(self.add_income_button)
        self.income_group.setLayout(self.income_layout)
        
        self.expense_layout = QVBoxLayout()
        self.add_expense_button = QPushButton("Add Expense")
        self.add_expense_button.clicked.connect(lambda: self.open_add_transaction_dialog('expense'))
        self.expense_layout.addWidget(self.add_expense_button)
        self.expense_group.setLayout(self.expense_layout)
        
        self.buttons_layout.addWidget(self.income_group)
        self.buttons_layout.addWidget(self.expense_group)
        
        self.view_transactions_button = QPushButton("View Transactions")
        self.view_transactions_button.clicked.connect(self.view_transactions)
        
        self.view_totals_button = QPushButton("View Totals")
        self.view_totals_button.clicked.connect(self.view_totals)
        
        self.view_chart_button = QPushButton("View Chart")
        self.view_chart_button.clicked.connect(self.view_chart)
        
        self.layout.addWidget(self.summary_label)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addWidget(self.view_transactions_button)
        self.layout.addWidget(self.view_totals_button)
        self.layout.addWidget(self.view_chart_button)
        
        self.setStyleSheet(load_stylesheet("MacOS.qss"))

    def open_add_transaction_dialog(self, t_type, transaction=None, index=None):
        dialog = AddTransactionDialog(t_type, transaction, index)
        if dialog.exec() == QDialog.Accepted:
            self.update_summary()
            QMessageBox.information(self, "Success", f"{t_type.capitalize()} {'added' if not transaction else 'updated'} successfully!")
        
    def view_transactions(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Transactions")
        dialog.setStyleSheet(load_stylesheet("MacOS.qss"))
        
        layout = QVBoxLayout()
        transactions_text = QTextEdit()
        transactions_text.setReadOnly(True)
        transactions_text.setStyleSheet("background-color: #fff; border: 1px solid #ddd; border-radius: 5px; padding: 10px;")
        
        if not transactions:
            transactions_text.setText("No transactions found.")
        else:
            for i, transaction in enumerate(transactions):
                transactions_text.append(f"{i+1}. {transaction['type'].capitalize()} of ${transaction['amount']} - {transaction['description']} ({transaction['category']})")
        
        delete_button = QPushButton("Delete Transaction")
        delete_button.clicked.connect(lambda: self.delete_transaction(dialog, transactions_text))
        
        edit_button = QPushButton("Edit Transaction")
        edit_button.clicked.connect(lambda: self.edit_transaction(dialog, transactions_text))
        
        delete_button.setStyleSheet("background-color: #F44336; color: white; padding: 10px; border: none; border-radius: 5px;")
        edit_button.setStyleSheet("background-color: #FFC107; color: black; padding: 10px; border: none; border-radius: 5px;")
        
        layout.addWidget(transactions_text)
        layout.addWidget(delete_button)
        layout.addWidget(edit_button)
        dialog.setLayout(layout)
        dialog.exec()
        
    def delete_transaction(self, dialog, transactions_text):
        index, ok = QInputDialog.getInt(dialog, "Delete Transaction", "Enter transaction number to delete:", 1, 1, len(transactions))
        if ok:
            transactions.pop(index - 1)
            save_transactions()  # Save to CSV
            self.update_summary()
            self.view_transactions()
            QMessageBox.information(self, "Success", "Transaction deleted successfully!")
        
    def edit_transaction(self, dialog, transactions_text):
        index, ok = QInputDialog.getInt(dialog, "Edit Transaction", "Enter transaction number to edit:", 1, 1, len(transactions))
        if ok:
            transaction = transactions[index - 1]
            self.open_add_transaction_dialog(transaction['type'], transaction, index - 1)
            self.view_transactions()
        
    def view_totals(self):
        total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
        total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
        net_balance = total_income - total_expenses
        
        totals_message = (
            f"Total Income: ${total_income}\n"
            f"Total Expenses: ${total_expenses}\n"
            f"Net Balance: ${net_balance}"
        )
        
        QMessageBox.information(self, "Totals", totals_message)
    
    def view_chart(self):
        def func(pct, allvals):
            total = sum(allvals)
            value = pct / 100 * total
            return f"${value:.2f} ({pct:.1f}%)"
        
        # Aggregate income data by category
        income_data = {}
        expense_data = {}
        
        for transaction in transactions:
            if transaction['type'] == 'income':
                category = transaction['category']
                income_data[category] = income_data.get(category, 0) + transaction['amount']
            elif transaction['type'] == 'expense':
                category = transaction['category']
                expense_data[category] = expense_data.get(category, 0) + transaction['amount']
        
        if not income_data and not expense_data:
            QMessageBox.warning(self, "No Data", "No data available to plot.")
            return
        
        # Plot income chart
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))
        
        if income_data:
            labels = list(income_data.keys())
            sizes = list(income_data.values())
            axs[0].pie(sizes, labels=labels, autopct=lambda pct: func(pct, sizes), startangle=140)
            axs[0].axis('equal')  # Equal aspect ratio ensures the pie chart is circular
            axs[0].set_title('Income by Category')
        
        # Plot expenses chart
        if expense_data:
            labels = list(expense_data.keys())
            sizes = list(expense_data.values())
            axs[1].pie(sizes, labels=labels, autopct=lambda pct: func(pct, sizes), startangle=140)
            axs[1].axis('equal')  # Equal aspect ratio ensures the pie chart is circular
            axs[1].set_title('Expenses by Category')
        
        plt.tight_layout()
        plt.show()



    def update_summary(self):
        total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
        total_expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
        net_balance = total_income - total_expenses
        
        self.summary_label.setText(
            f"Total Income: ${total_income}   |   Total Expenses: ${total_expenses}   |   Net Balance: ${net_balance}"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Load and apply the stylesheet
    stylesheet = load_stylesheet("MacOS.qss")
    app.setStyleSheet(stylesheet)
    
    window = FinanceTracker()
    window.show()
    sys.exit(app.exec())
