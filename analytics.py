import pandas as pd


def prepare_data(transactions):
    if not transactions:
        return pd.DataFrame()

    df = pd.DataFrame([dict(row) for row in transactions])

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["month"] = df["date"].dt.to_period("M").astype(str)

    return df


def get_summary(df):
    if df.empty:
        return {
            "income": 0,
            "expenses": 0,
            "balance": 0,
            "savings": 0
        }

    income = df.loc[
        df["transaction_type"] == "Income", "base_amount"
    ].sum()

    expenses = df.loc[
        df["transaction_type"] == "Expense", "base_amount"
    ].sum()

    return {
        "income": float(income),
        "expenses": float(expenses),
        "balance": float(income - expenses),
        "savings": float(income - expenses)
    }


def category_summary(df):
    if df.empty:
        return pd.DataFrame()

    expenses = df[df["transaction_type"] == "Expense"]

    if expenses.empty:
        return pd.DataFrame()

    return (
        expenses.groupby("category")["base_amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def monthly_summary(df):
    if df.empty:
        return pd.DataFrame()

    result = (
        df.pivot_table(
            index="month",
            columns="transaction_type",
            values="base_amount",
            aggfunc="sum",
            fill_value=0
        )
        .reset_index()
    )

    return result