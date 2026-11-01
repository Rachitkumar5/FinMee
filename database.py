
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "finance.db"


# ==================================================
# DATABASE CONNECTION
# ==================================================

@contextmanager
def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def fetch_all(query, params=()):
    with connect() as db:
        return [dict(row) for row in db.execute(query, params).fetchall()]


def fetch_one(query, params=()):
    with connect() as db:
        row = db.execute(query, params).fetchone()
        return dict(row) if row else None


# ==================================================
# DATABASE INITIALIZATION AND MIGRATION
# ==================================================

def init_db():

    with connect() as db:

        # Create tables without indexes first.
        db.executescript("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT DEFAULT 'Bank',
            currency TEXT DEFAULT 'INR',
            opening_balance REAL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT DEFAULT 'Expense',
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'INR',
            category TEXT DEFAULT 'Other',
            account TEXT,
            destination_account TEXT,
            date TEXT,
            transaction_date TEXT,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            limit_amount REAL NOT NULL,
            currency TEXT DEFAULT 'INR',
            month TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            saved_amount REAL DEFAULT 0,
            currency TEXT DEFAULT 'INR',
            due_date TEXT
        );

        CREATE TABLE IF NOT EXISTS recurring_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'INR',
            category TEXT DEFAULT 'Other',
            account TEXT,
            description TEXT,
            frequency TEXT DEFAULT 'Monthly',
            next_date TEXT,
            active INTEGER DEFAULT 1
        );
        """)

        # Check existing table structures.
        migrations = {
            "accounts": {
                "type": "TEXT DEFAULT 'Bank'",
                "currency": "TEXT DEFAULT 'INR'",
                "opening_balance": "REAL DEFAULT 0",
                "created_at": "TEXT"
            },

            "transactions": {
                "kind": "TEXT DEFAULT 'Expense'",
                "currency": "TEXT DEFAULT 'INR'",
                "category": "TEXT DEFAULT 'Other'",
                "account": "TEXT",
                "destination_account": "TEXT",
                "date": "TEXT",
                "transaction_date": "TEXT",
                "description": "TEXT",
                "exchange_rate": "REAL NOT NULL DEFAULT 1.0",
                "created_at": "TEXT"
            },

            "budgets": {
                "category": "TEXT DEFAULT 'Other'",
                "limit_amount": "REAL DEFAULT 0",
                "currency": "TEXT DEFAULT 'INR'",
                "month": "TEXT"
            }
        }

        # Add missing columns safely.
        for table, columns in migrations.items():

            existing = {
                row["name"]
                for row in db.execute(f"PRAGMA table_info({table})")
            }

            for column, definition in columns.items():

                if column not in existing:
                    db.execute(
                        f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
                    )

        # Copy old date values into the new date column.
        db.execute("""
            UPDATE transactions
            SET transaction_date = date
            WHERE (transaction_date IS NULL OR transaction_date = '')
            AND date IS NOT NULL
        """)

        # Ensure missing dates have a valid value.
        db.execute("""
            UPDATE transactions
            SET transaction_date = ?
            WHERE transaction_date IS NULL OR transaction_date = ''
        """, (datetime.today().strftime("%Y-%m-%d"),))

        # Create indexes AFTER migration.
        db.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_date
            ON transactions(transaction_date)
        """)

        db.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_category
            ON transactions(category)
        """)


# ==================================================
# ACCOUNT MANAGEMENT
# ==================================================

def add_account(name, account_type="Bank",
                currency="INR", opening_balance=0):

    with connect() as db:
        db.execute("""
            INSERT INTO accounts (name, type, currency, opening_balance)
            VALUES (?, ?, ?, ?)
        """, (name, account_type, currency, opening_balance))


def get_accounts():
    return fetch_all("SELECT * FROM accounts ORDER BY id DESC")


def get_account(account_id):
    return fetch_one(
        "SELECT * FROM accounts WHERE id = ?",
        (account_id,)
    )


def delete_account(account_id):
    with connect() as db:
        db.execute("DELETE FROM accounts WHERE id = ?", (account_id,))


# ==================================================
# TRANSACTION MANAGEMENT
# ==================================================

def add_transaction(kind, amount, currency="INR",
                    category="Other", account=None,
                    transaction_date=None, description="",
                    destination_account=None, exchange_rate=1.0):

    transaction_date = transaction_date or datetime.today().strftime("%Y-%m-%d")
    amount = float(amount)
    exchange_rate = float(exchange_rate)

    if amount <= 0 or exchange_rate <= 0:
        raise ValueError("Amount and exchange rate must be greater than zero.")

    with connect() as db:
        cursor = db.execute("""
            INSERT INTO transactions (
                kind, amount, currency, category,
                account, destination_account,
                date, transaction_date, description, exchange_rate
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            kind, amount, currency, category,
            account, destination_account,
            transaction_date, transaction_date, description,
            exchange_rate
        ))

        return cursor.lastrowid

def get_transactions():
    return fetch_all("""
        SELECT * FROM transactions
        ORDER BY transaction_date DESC, id DESC
    """)


def get_transaction(transaction_id):
    return fetch_one(
        "SELECT * FROM transactions WHERE id = ?",
        (transaction_id,)
    )


def update_transaction(transaction_id, kind, amount,
                       currency="INR", category="Other",
                       account=None, transaction_date=None,
                       description="", destination_account=None,
                       exchange_rate=1.0):

    transaction_date = transaction_date or datetime.today().strftime("%Y-%m-%d")
    amount = float(amount)
    exchange_rate = float(exchange_rate)

    if amount <= 0 or exchange_rate <= 0:
        raise ValueError("Amount and exchange rate must be greater than zero.")

    with connect() as db:
        db.execute("""
            UPDATE transactions
            SET kind = ?,
                amount = ?,
                currency = ?,
                category = ?,
                account = ?,
                destination_account = ?,
                date = ?,
                transaction_date = ?,
                description = ?,
                exchange_rate = ?
            WHERE id = ?
        """, (
            kind, amount, currency, category,
            account, destination_account,
            transaction_date, transaction_date,
            description, exchange_rate, transaction_id
        ))

def delete_transaction(transaction_id):
    with connect() as db:
        db.execute(
            "DELETE FROM transactions WHERE id = ?",
            (transaction_id,)
        )


# ==================================================
# ACCOUNT BALANCES
# ==================================================

def get_account_balances(base_currency="INR"):
    from finance import convert_to_base

    accounts = get_accounts()
    transactions = get_transactions()

    results = []

    for account in accounts:

        balance = convert_to_base(
            account["opening_balance"] or 0,
            account["currency"],
            base_currency
        )

        for transaction in transactions:

            amount = convert_to_base(
                transaction["amount"],
                transaction["currency"],
                base_currency
            )

            if transaction["kind"] == "Income":
                if transaction["account"] == account["name"]:
                    balance += amount

            elif transaction["kind"] == "Expense":
                if transaction["account"] == account["name"]:
                    balance -= amount

            elif transaction["kind"] == "Transfer":

                if transaction["account"] == account["name"]:
                    balance -= amount

                if transaction["destination_account"] == account["name"]:
                    balance += amount

        results.append({
            **account,
            "balance_base": balance
        })

    return results


# ==================================================
# BUDGET MANAGEMENT
# ==================================================

def add_budget(category, limit_amount,
               currency="INR", month=None):

    month = month or datetime.today().strftime("%Y-%m")

    with connect() as db:
        db.execute("""
            INSERT INTO budgets (category, limit_amount, currency, month)
            VALUES (?, ?, ?, ?)
        """, (category, limit_amount, currency, month))


def get_budgets(month=None):

    if month:
        return fetch_all(
            "SELECT * FROM budgets WHERE month = ? ORDER BY id DESC",
            (month,)
        )

    return fetch_all("SELECT * FROM budgets ORDER BY month DESC, id DESC")


def delete_budget(budget_id):
    with connect() as db:
        db.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))


# ==================================================
# FINANCIAL GOALS
# ==================================================

def add_goal(name, target_amount, saved_amount=0,
             currency="INR", due_date=None):

    with connect() as db:
        cursor = db.execute("""
            INSERT INTO goals
            (name, target_amount, saved_amount, currency, due_date)
            VALUES (?, ?, ?, ?, ?)
        """, (name, target_amount, saved_amount, currency, due_date))

        return cursor.lastrowid


def get_goals():
    return fetch_all("SELECT * FROM goals ORDER BY id DESC")


def update_goal(goal_id, saved_amount):
    with connect() as db:
        db.execute(
            "UPDATE goals SET saved_amount = ? WHERE id = ?",
            (saved_amount, goal_id)
        )


def delete_goal(goal_id):
    with connect() as db:
        db.execute("DELETE FROM goals WHERE id = ?", (goal_id,))


# ==================================================
# RECURRING TRANSACTIONS
# ==================================================

def add_recurring_transaction(kind, amount,
                              currency="INR", category="Other",
                              account=None, description="",
                              frequency="Monthly", next_date=None):

    with connect() as db:
        cursor = db.execute("""
            INSERT INTO recurring_transactions (
                kind, amount, currency, category,
                account, description, frequency, next_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            kind, amount, currency, category,
            account, description, frequency, next_date
        ))

        return cursor.lastrowid


def get_recurring_transactions():
    return fetch_all("""
        SELECT * FROM recurring_transactions
        ORDER BY next_date ASC
    """)


def delete_recurring_transaction(recurring_id):
    with connect() as db:
        db.execute(
            "DELETE FROM recurring_transactions WHERE id = ?",
            (recurring_id,)
        )


# ==================================================
# ANALYTICS
# ==================================================

def get_monthly_totals(base_currency="INR"):
    import pandas as pd
    from finance import convert_to_base

    data = {}

    for transaction in get_transactions():

        month = (transaction["transaction_date"] or "")[:7]

        if not month:
            continue

        data.setdefault(month, {
            "month": month,
            "income": 0.0,
            "expense": 0.0
        })

        kind = transaction["kind"]

        if kind in ("Income", "Expense"):
            data[month][kind.lower()] += convert_to_base(
                transaction["amount"],
                transaction["currency"],
                base_currency
            )

    return pd.DataFrame(
        sorted(data.values(), key=lambda item: item["month"])
    )


def get_category_totals(base_currency="INR"):
    import pandas as pd
    from finance import convert_to_base

    totals = {}

    for transaction in get_transactions():

        if transaction["kind"] == "Expense":

            category = transaction["category"] or "Other"

            totals[category] = totals.get(category, 0) + convert_to_base(
                transaction["amount"],
                transaction["currency"],
                base_currency
            )

    return pd.DataFrame([
        {"category": category, "amount": amount}
        for category, amount in sorted(
            totals.items(),
            key=lambda item: item[1],
            reverse=True
        )
    ])


def get_transaction_summary(base_currency="INR"):
    from finance import convert_to_base

    income = 0.0
    expense = 0.0

    for transaction in get_transactions():

        amount = convert_to_base(
            transaction["amount"],
            transaction["currency"],
            base_currency
        )

        if transaction["kind"] == "Income":
            income += amount

        elif transaction["kind"] == "Expense":
            expense += amount

    return {
        "income": income,
        "expense": expense,
        "net_savings": income - expense,
        "savings_rate": (
            (income - expense) / income * 100
            if income else 0
        )
    }
