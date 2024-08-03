# Personal Finance Tracker

## Overview

Personal Finance Tracker is a desktop application developed using Python and PyQt5. It allows users to track their income and expenses, view transaction summaries, and analyze financial data through charts. The application supports category-based tracking for both income and expenses and persists data using CSV files.

## Features

- **Add/Edit Transactions**: Add or edit income and expense transactions with details including amount, description, and category.
- **View Transactions**: Display a list of all transactions with the option to delete or edit individual entries.
- **View Totals**: See total income, total expenses, and net balance.
- **View Charts**: Visualize income and expense distributions by category using pie charts.
- **Persist Data**: Save and load transactions from a CSV file.

## Requirements

- Python 3.x
- PyQt5
- Matplotlib

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ABDESSAMED-tech/Personal-Finance-Tracker
    cd personal-finance-tracker
    ```

2. **Install the required packages:**

    You can install the required Python packages using pip:

    ```bash
    pip install PyQt5 matplotlib
    ```

3. **Optional - Add custom stylesheet:**

    If you have a custom stylesheet (`MacOS.qss`), place it in the same directory as the Python script.

## Usage

1. **Run the application:**

    Navigate to the directory containing the `main.py` file and execute:

    ```bash
    python main.py
    ```

2. **Add/Edit Transactions:**

    - Click on "Add Income" or "Add Expense" to open a dialog for adding a new transaction.
    - You can also edit or delete existing transactions through the "View Transactions" button.

3. **View Totals:**

    - Click "View Totals" to see a summary of total income, total expenses, and net balance.

4. **View Charts:**

    - Click "View Chart" to visualize income and expense data by category using pie charts.

## File Structure

- `main.py`: Main application script.
- `transactions.csv`: CSV file for storing transactions (automatically created if it doesn’t exist).
- `MacOS.qss`: Custom stylesheet for application styling (optional).

## Customization

You can modify the `MacOS.qss` file to change the appearance of the application. The stylesheet should be applied in the `main.py` file using `app.setStyleSheet(load_stylesheet("MacOS.qss"))`.

## Contributing

If you'd like to contribute to the project, please fork the repository, create a feature branch, and submit a pull request with your changes. 

## License

This project is licensed under the MIT License.
## Contact

For any questions or feedback, please contact [abdessamed.boulariache@gmail.com](mailto:abdessamed.boulariache@gmail.com).



