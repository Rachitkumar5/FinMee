# ◈ FinMee — Smart Personal Finance Tracker

A premium personal finance management dashboard built with Python and Streamlit.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

## ✨ Features

- 📊 **Beautiful Dashboard** — Real-time financial overview with animated hero cards and interactive charts
- 💸 **Transaction Management** — Add, search, filter, and export income/expense/transfer transactions
- 🏦 **Multi-Account Tracking** — Bank, cash, savings, credit card, wallet, and investment accounts
- 📋 **Budget Management** — Set monthly spending limits per category with visual progress tracking
- 🎯 **Financial Goals** — Create savings goals with progress tracking and due dates
- 📈 **Rich Analytics** — Cash flow trends, category breakdowns, financial health scoring
- 🔄 **Recurring Transactions** — Track subscriptions, EMIs, and regular payments
- 📑 **Reports & Exports** — Download CSV reports of transactions and category summaries
- 💱 **Multi-Currency** — 10 currencies with automatic conversion (INR, USD, EUR, GBP, etc.)
- 🎨 **Premium UI/UX** — Inter font, gradient cards, smooth animations, responsive design

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.9+ | Core language |
| Streamlit | Web framework |
| SQLite | Local database |
| Pandas | Data processing |
| Plotly | Interactive charts |

## 🚀 Quick Start

```bash
# Clone the repository
git clone YOUR_REPOSITORY_URL
cd smart-expense-tracker

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
smart-expense-tracker/
├── app.py              # Main Streamlit application
├── database.py         # SQLite database layer
├── finance.py          # Financial engine & calculations
├── analytics.py        # Data analysis helpers
├── insights.py         # AI insights (coming soon)
├── finance.db          # SQLite database file
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── config.toml     # Streamlit theme configuration
└── README.md
```

## 💱 Supported Currencies

INR (₹), USD ($), EUR (€), GBP (£), AED (د.إ), CAD (C$), AUD (A$), JPY (¥), SGD (S$), CHF

> **Note:** Exchange rates are indicative sample rates for demonstration purposes.

## 👨‍💻 Author

**Rachit Kumar**

---

*Made with 💜 using Streamlit*
