
# ==================================================
# FINMEE — FINANCIAL ENGINE
# ==================================================

from datetime import date, timedelta
import calendar

# --------------------------------------------------
# CURRENCY CONFIGURATION
# --------------------------------------------------

CURRENCIES = {
    "INR": "Indian Rupee",
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "AED": "UAE Dirham",
    "CAD": "Canadian Dollar",
    "AUD": "Australian Dollar",
    "JPY": "Japanese Yen",
    "SGD": "Singapore Dollar",
    "CHF": "Swiss Franc",
}

CURRENCY_SYMBOLS = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "AED": "د.إ",
    "CAD": "C$",
    "AUD": "A$",
    "JPY": "¥",
    "SGD": "S$",
    "CHF": "CHF",
}

# Indicative conversion rates relative to INR.
# These are sample rates, NOT live market rates.
TO_INR = {
    "INR": 1.0,
    "USD": 83.5,
    "EUR": 90.5,
    "GBP": 105.5,
    "AED": 22.7,
    "CAD": 61.2,
    "AUD": 54.5,
    "JPY": 0.56,
    "SGD": 62.2,
    "CHF": 94.0,
}

# --------------------------------------------------
# EXPENSE CATEGORIES WITH ICONS
# --------------------------------------------------

CATEGORY_ICONS = {
    "Food": "🍕",
    "Shopping": "🛍️",
    "Travel": "✈️",
    "Transport": "🚗",
    "Housing": "🏠",
    "Bills": "📄",
    "Healthcare": "💊",
    "Education": "📚",
    "Entertainment": "🎬",
    "Salary": "💰",
    "Freelance": "💻",
    "Investment": "📈",
    "Subscriptions": "🔄",
    "Personal Care": "💆",
    "Gifts": "🎁",
    "Other": "📌",
}

CATEGORIES = [
    "Food",
    "Shopping",
    "Travel",
    "Transport",
    "Housing",
    "Bills",
    "Healthcare",
    "Education",
    "Entertainment",
    "Salary",
    "Freelance",
    "Investment",
    "Subscriptions",
    "Personal Care",
    "Gifts",
    "Other",
]

INCOME_CATEGORIES = [
    "Salary",
    "Freelance",
    "Business",
    "Investment",
    "Gift",
    "Other",
]

EXPENSE_CATEGORIES = [
    category for category in CATEGORIES
    if category not in INCOME_CATEGORIES
]

ACCOUNT_TYPES = [
    "Bank",
    "Cash",
    "Savings",
    "Credit card",
    "Wallet",
    "Investment",
]

ACCOUNT_ICONS = {
    "Bank": "🏦",
    "Cash": "💵",
    "Savings": "🐖",
    "Credit card": "💳",
    "Wallet": "👛",
    "Investment": "📊",
}

# --------------------------------------------------
# CURRENCY CONVERSION
# --------------------------------------------------

def convert_currency(amount, exchange_rate):
    """Convert using a manually supplied exchange rate."""
    return float(amount) * float(exchange_rate)


def convert_to_base(amount, source_currency, target_currency="INR"):
    """Convert an amount between supported currencies."""

    if source_currency not in TO_INR:
        raise ValueError(f"Unsupported currency: {source_currency}")

    if target_currency not in TO_INR:
        raise ValueError(f"Unsupported currency: {target_currency}")

    amount_in_inr = float(amount) * TO_INR[source_currency]

    return amount_in_inr / TO_INR[target_currency]


# --------------------------------------------------
# MONEY FORMATTING
# --------------------------------------------------

def format_money(amount, currency="INR"):
    symbol = CURRENCY_SYMBOLS.get(currency, currency)

    if currency == "JPY":
        return f"{symbol}{float(amount):,.0f}"

    return f"{symbol}{float(amount):,.2f}"


def money(amount, currency="INR"):
    return format_money(amount, currency)


def compact_money(amount, currency="INR"):
    """Format large numbers compactly (e.g. ₹1.2L, ₹3.4Cr)."""
    symbol = CURRENCY_SYMBOLS.get(currency, currency)
    amount = float(amount)

    if currency == "INR":
        if abs(amount) >= 1_00_00_000:
            return f"{symbol}{amount / 1_00_00_000:.1f}Cr"
        elif abs(amount) >= 1_00_000:
            return f"{symbol}{amount / 1_00_000:.1f}L"
        elif abs(amount) >= 1_000:
            return f"{symbol}{amount / 1_000:.1f}K"
    else:
        if abs(amount) >= 1_000_000:
            return f"{symbol}{amount / 1_000_000:.1f}M"
        elif abs(amount) >= 1_000:
            return f"{symbol}{amount / 1_000:.1f}K"

    return format_money(amount, currency)


# --------------------------------------------------
# SAVINGS CALCULATIONS
# --------------------------------------------------

def calculate_savings(income, expenses):
    return float(income) - float(expenses)


def calculate_savings_rate(income, expenses):

    income = float(income)
    expenses = float(expenses)

    if income <= 0:
        return 0.0

    return ((income - expenses) / income) * 100


# --------------------------------------------------
# BUDGET CALCULATIONS
# --------------------------------------------------

def calculate_budget_usage(spent, budget):
    if budget <= 0:
        return 0.0

    return (float(spent) / float(budget)) * 100


def calculate_remaining_budget(spent, budget):
    return float(budget) - float(spent)


def get_budget_status(spent, budget):

    percentage = calculate_budget_usage(spent, budget)

    if percentage >= 100:
        return "Over budget", "🔴"

    if percentage >= 80:
        return "Almost reached", "🟡"

    if percentage >= 50:
        return "Halfway", "🟠"

    return "On track", "🟢"


# --------------------------------------------------
# FINANCIAL HEALTH
# --------------------------------------------------

def calculate_financial_health(income, expenses, savings_goal=20):

    income = float(income)
    expenses = float(expenses)

    if income <= 0:
        return {
            "score": 0,
            "status": "Insufficient data",
            "emoji": "⚪",
            "savings_rate": 0,
            "color": "#858BA3"
        }

    savings_rate = calculate_savings_rate(income, expenses)

    score = min(max((savings_rate / savings_goal) * 100, 0), 100)

    if savings_rate >= 30:
        status = "Excellent"
        emoji = "🌟"
        color = "#00B894"

    elif savings_rate >= 20:
        status = "Healthy"
        emoji = "💚"
        color = "#19A879"

    elif savings_rate >= 10:
        status = "Fair"
        emoji = "💛"
        color = "#FDCB6E"

    elif savings_rate >= 0:
        status = "Needs improvement"
        emoji = "🟠"
        color = "#F2A65A"

    else:
        status = "Overspending"
        emoji = "🔴"
        color = "#E46D78"

    return {
        "score": round(score),
        "status": status,
        "emoji": emoji,
        "savings_rate": round(savings_rate, 2),
        "color": color
    }


# --------------------------------------------------
# DATE HELPERS
# --------------------------------------------------

def current_month():
    return date.today().strftime("%Y-%m")


def current_year():
    return date.today().year


def current_month_name():
    return date.today().strftime("%B %Y")


def is_valid_amount(amount):
    try:
        return float(amount) > 0
    except (TypeError, ValueError):
        return False


def days_until(target_date_str):
    """Calculate days remaining until a target date."""
    try:
        target = date.fromisoformat(target_date_str)
        delta = target - date.today()
        return max(delta.days, 0)
    except (ValueError, TypeError):
        return 0


def get_greeting():
    """Return a time-appropriate greeting."""
    from datetime import datetime
    hour = datetime.now().hour

    if hour < 12:
        return "Good morning"
    elif hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"
