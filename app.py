
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime, timedelta

from database import (
    init_db,
    get_transactions,
    add_transaction,
    delete_transaction,
    get_accounts,
    add_account,
    delete_account,
    get_account_balances,
    get_budgets,
    add_budget,
    delete_budget,
    get_goals,
    add_goal,
    update_goal,
    delete_goal,
    get_monthly_totals,
    get_category_totals,
    get_transaction_summary,
    get_recurring_transactions,
    add_recurring_transaction,
    delete_recurring_transaction,
)

from finance import (
    CURRENCIES,
    CURRENCY_SYMBOLS,
    CATEGORIES,
    INCOME_CATEGORIES,
    EXPENSE_CATEGORIES,
    ACCOUNT_TYPES,
    CATEGORY_ICONS,
    ACCOUNT_ICONS,
    money,
    compact_money,
    convert_to_base,
    calculate_budget_usage,
    calculate_financial_health,
    get_budget_status,
    calculate_remaining_budget,
    days_until,
    get_greeting,
    current_month,
    current_month_name,
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="FinMee | Smart Finance Tracker",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()


# ==========================================================
# FINMEE PREMIUM DESIGN SYSTEM
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── CSS Variables ── */
:root {
    --primary: #6C5CE7;
    --primary-light: #A29BFE;
    --primary-dark: #5A4BD1;
    --primary-bg: rgba(108,92,231,.06);
    --background: #F8F9FD;
    --surface: #FFFFFF;
    --surface-hover: #FAFBFF;
    --text: #1A1D2E;
    --text-secondary: #6B7294;
    --muted: #9CA3C4;
    --border: #ECEEF5;
    --border-hover: #D4D8E8;
    --green: #00B894;
    --green-bg: rgba(0,184,148,.08);
    --red: #E17055;
    --red-bg: rgba(225,112,85,.08);
    --amber: #FDCB6E;
    --amber-bg: rgba(253,203,110,.1);
    --blue: #74B9FF;
    --blue-bg: rgba(116,185,255,.08);
    --shadow-sm: 0 1px 3px rgba(26,29,46,.04);
    --shadow-md: 0 4px 16px rgba(26,29,46,.06);
    --shadow-lg: 0 12px 40px rgba(108,92,231,.12);
    --radius-sm: 10px;
    --radius-md: 14px;
    --radius-lg: 20px;
    --radius-xl: 24px;
}

/* ── Typography ── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* ── Page background ── */
.stApp {
    background: var(--background);
}

.block-container {
    max-width: 1440px;
    padding: 1.5rem 2rem 4rem;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #FAFBFF 100%);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

[data-testid="stSidebar"] .stRadio > div {
    gap: 2px;
}

[data-testid="stSidebar"] .stRadio > div > label {
    padding: 8px 16px;
    border-radius: var(--radius-sm);
    transition: all .15s ease;
    font-weight: 500;
    color: var(--text-secondary);
}

[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: var(--primary-bg);
    color: var(--primary);
}

[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
    background: var(--primary-bg);
    color: var(--primary);
    font-weight: 600;
}

/* ── Logo + Branding ── */
.finmee-logo {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1.2px;
    background: linear-gradient(135deg, #6C5CE7 0%, #A29BFE 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
}

.finmee-tagline {
    color: var(--muted);
    font-size: 12px;
    font-weight: 500;
    letter-spacing: .3px;
    margin-top: 2px;
}

/* ── Page Headers ── */
.page-heading {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.8px;
    color: var(--text);
    line-height: 1.2;
    margin-bottom: 2px;
}

.page-description {
    font-size: 14px;
    color: var(--text-secondary);
    margin-top: 0;
    margin-bottom: 28px;
    font-weight: 400;
}

/* ── Hero Card ── */
.hero-card {
    background: linear-gradient(135deg, #6C5CE7 0%, #A29BFE 50%, #6C5CE7 100%);
    background-size: 200% 200%;
    animation: gradientShift 8s ease infinite;
    color: white;
    padding: 32px 36px;
    border-radius: var(--radius-xl);
    min-height: 180px;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}

.hero-card::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(255,255,255,.08) 0%, transparent 70%);
    border-radius: 50%;
}

.hero-card::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(255,255,255,.05) 0%, transparent 70%);
    border-radius: 50%;
}

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero-label {
    font-size: 11px;
    font-weight: 700;
    opacity: .85;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.hero-amount {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -2px;
    margin: 10px 0 6px;
    position: relative;
    z-index: 1;
}

.hero-caption {
    font-size: 13px;
    opacity: .75;
    font-weight: 400;
}

.hero-pill {
    display: inline-block;
    background: rgba(255,255,255,.15);
    backdrop-filter: blur(10px);
    padding: 7px 16px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 600;
    margin-top: 12px;
    position: relative;
    z-index: 1;
}

/* ── Section Headers ── */
.section-heading {
    font-size: 17px;
    font-weight: 700;
    color: var(--text);
    margin: 28px 0 14px;
    letter-spacing: -0.3px;
}

/* ── Stat Cards ── */
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 22px 24px;
    box-shadow: var(--shadow-sm);
    transition: all .2s ease;
}

.stat-card:hover {
    border-color: var(--border-hover);
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}

.stat-icon {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 14px;
}

.stat-label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
    letter-spacing: .3px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.stat-value {
    font-size: 24px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.8px;
}

.stat-delta {
    font-size: 12px;
    font-weight: 600;
    margin-top: 6px;
}

.delta-positive { color: var(--green); }
.delta-negative { color: var(--red); }

/* ── Streamlit Metric Override ── */
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 20px 22px;
    box-shadow: var(--shadow-sm);
    transition: all .2s ease;
}

div[data-testid="stMetric"]:hover {
    border-color: var(--border-hover);
    box-shadow: var(--shadow-md);
}

div[data-testid="stMetricLabel"] {
    color: var(--text-secondary);
    font-weight: 600;
    font-size: 12px;
    letter-spacing: .3px;
    text-transform: uppercase;
}

div[data-testid="stMetricValue"] {
    color: var(--text);
    font-weight: 800;
    letter-spacing: -0.5px;
}

/* ── Buttons ── */
div.stButton > button,
div.stDownloadButton > button {
    border-radius: var(--radius-sm);
    min-height: 44px;
    font-weight: 600;
    border: 1px solid var(--border);
    transition: all .15s ease;
    letter-spacing: -0.2px;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    border-color: var(--border-hover);
    box-shadow: var(--shadow-sm);
}

div.stButton > button[kind="primary"],
div.stDownloadButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    border-color: var(--primary);
    color: white;
    box-shadow: 0 4px 14px rgba(108,92,231,.25);
}

div.stButton > button[kind="primary"]:hover,
div.stDownloadButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, var(--primary-dark) 0%, #4A3BC1 100%);
    border-color: var(--primary-dark);
    box-shadow: 0 6px 20px rgba(108,92,231,.3);
    transform: translateY(-1px);
}

/* ── Form Inputs ── */
.stTextInput input,
.stNumberInput input {
    border-radius: var(--radius-sm) !important;
    border-color: var(--border) !important;
    transition: all .15s ease;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px var(--primary-bg) !important;
}

.stSelectbox div[data-baseweb="select"] {
    border-radius: var(--radius-sm);
}

/* ── Data Table ── */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

/* ── Containers ── */
div[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
}

/* ── Progress Bars ── */
.stProgress > div > div {
    border-radius: 20px;
    height: 8px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 2px solid var(--border);
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm) var(--radius-sm) 0 0;
    font-weight: 600;
    padding: 10px 20px;
}

/* ── Horizontal Rule ── */
hr {
    border-color: var(--border);
}

/* ── Toast ── */
div[data-testid="stToast"] {
    border-radius: var(--radius-md);
}

/* ── Account Card ── */
.account-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: var(--shadow-sm);
    transition: all .2s ease;
}

.account-card:hover {
    border-color: var(--primary-light);
    box-shadow: var(--shadow-md);
}

.account-icon {
    font-size: 28px;
    margin-bottom: 10px;
}

.account-name {
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
}

.account-type {
    font-size: 12px;
    color: var(--text-secondary);
    font-weight: 500;
}

.account-balance {
    font-size: 22px;
    font-weight: 800;
    color: var(--text);
    margin-top: 12px;
    letter-spacing: -0.6px;
}

/* ── Budget Card ── */
.budget-status-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 50px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .3px;
}

.status-on-track {
    background: var(--green-bg);
    color: var(--green);
}

.status-warning {
    background: var(--amber-bg);
    color: #E17055;
}

.status-danger {
    background: var(--red-bg);
    color: var(--red);
}

/* ── Goal Card ── */
.goal-progress-ring {
    font-size: 32px;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -1px;
}

/* ── Transaction Badge ── */
.txn-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 50px;
    font-size: 11px;
    font-weight: 600;
}

.txn-income {
    background: var(--green-bg);
    color: var(--green);
}

.txn-expense {
    background: var(--red-bg);
    color: var(--red);
}

.txn-transfer {
    background: var(--blue-bg);
    color: #0984E3;
}

/* ── Empty States ── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-secondary);
}

.empty-state-icon {
    font-size: 48px;
    margin-bottom: 16px;
    opacity: .6;
}

.empty-state-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 8px;
}

.empty-state-text {
    font-size: 14px;
    color: var(--text-secondary);
}

/* ── Health Score ── */
.health-score-circle {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto 12px;
    font-weight: 800;
    font-size: 28px;
    color: white;
    box-shadow: var(--shadow-md);
}

/* ── Footer ── */
.finmee-footer {
    text-align: center;
    color: var(--muted);
    font-size: 12px;
    padding: 20px 0;
    font-weight: 500;
}

.finmee-footer a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 600;
}

/* ── Smooth scrolling ── */
html {
    scroll-behavior: smooth;
}

/* ── Selection color ── */
::selection {
    background: var(--primary-light);
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def heading(title, subtitle):
    st.markdown(
        f'<div class="page-heading">{title}</div>'
        f'<div class="page-description">{subtitle}</div>',
        unsafe_allow_html=True
    )


def section(title):
    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True
    )


def stat_card(icon, bg_color, label, value, delta=None, delta_type="positive"):
    delta_html = ""
    if delta:
        cls = "delta-positive" if delta_type == "positive" else "delta-negative"
        delta_html = f'<div class="stat-delta {cls}">{delta}</div>'

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-icon" style="background:{bg_color};">{icon}</div>
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def empty_state(icon, title, text):
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-state-icon">{icon}</div>
        <div class="empty-state-title">{title}</div>
        <div class="empty-state-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)


def chart_layout(fig, height=None):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, -apple-system, sans-serif",
            color="#6B7294",
            size=12
        ),
        margin=dict(l=10, r=10, t=25, b=10),
        legend_title_text="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=11)
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#F0F1F6",
            zeroline=False,
        ),
    )
    if height:
        fig.update_layout(height=height)
    return fig


def base_amount(transaction, currency):
    return convert_to_base(
        transaction["amount"],
        transaction["currency"],
        currency
    )


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        '<div class="finmee-logo">◈ FinMee</div>'
        '<div class="finmee-tagline">Smart Personal Finance</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.divider()

    st.caption("NAVIGATE")

    page = st.radio(
        "Navigation",
        [
            "📊  Overview",
            "💸  Transactions",
            "🏦  Accounts",
            "📋  Budgets",
            "🎯  Goals",
            "📈  Analytics",
            "🔄  Recurring",
            "📑  Reports",
        ],
        label_visibility="collapsed",
    )

    # Strip emoji prefix for page matching
    page = page.split("  ", 1)[-1].strip()

    st.divider()

    st.caption("SETTINGS")

    currency = st.selectbox(
        "Base currency",
        list(CURRENCIES.keys()),
        index=list(CURRENCIES.keys()).index("INR"),
        format_func=lambda c: f"{CURRENCY_SYMBOLS.get(c, c)}  {c} · {CURRENCIES[c]}",
    )

    st.divider()

    st.markdown(
        '<div style="text-align:center;">'
        '<div class="finmee-logo" style="font-size:18px;">◈ FinMee</div>'
        '<div style="color:var(--muted);font-size:11px;margin-top:2px;">'
        'Version 2.0 · Made with 💜'
        '</div></div>',
        unsafe_allow_html=True
    )


# ==========================================================
# LOAD APPLICATION DATA
# ==========================================================

transactions = get_transactions()
accounts = get_accounts()
account_balances = get_account_balances(currency)

summary = get_transaction_summary(currency)

total_income = summary["income"]
total_expenses = summary["expense"]
net_savings = summary["net_savings"]
savings_rate = summary["savings_rate"]

total_balance = sum(
    account["balance_base"]
    for account in account_balances
)

health = calculate_financial_health(total_income, total_expenses)


# ==========================================================
# OVERVIEW DASHBOARD
# ==========================================================

if page == "Overview":

    greeting = get_greeting()

    heading(
        f"{greeting} 👋",
        f"Here's your financial snapshot for {current_month_name()}."
    )

    # Hero balance card
    account_text = f"{len(accounts)} account" if len(accounts) == 1 else f"{len(accounts)} accounts"

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-label">TOTAL BALANCE</div>
            <div class="hero-amount">{money(total_balance, currency)}</div>
            <div class="hero-caption">
                Across {account_text} · {health['emoji']} Financial health: {health['status']}
            </div>
            <div class="hero-pill">
                ◈ {current_month_name()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # KPI stat cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        stat_card(
            "💰", "var(--green-bg)",
            "Total Income", money(total_income, currency),
        )

    with c2:
        stat_card(
            "🛍️", "var(--red-bg)",
            "Total Expenses", money(total_expenses, currency),
        )

    with c3:
        delta_text = f"↑ {savings_rate:.1f}% savings rate" if savings_rate >= 0 else f"↓ {abs(savings_rate):.1f}%"
        delta_type = "positive" if net_savings >= 0 else "negative"
        stat_card(
            "🐖", "var(--primary-bg)",
            "Net Savings", money(net_savings, currency),
            delta=delta_text, delta_type=delta_type
        )

    with c4:
        stat_card(
            "🏦", "var(--blue-bg)",
            "Accounts", str(len(accounts)),
        )

    st.write("")

    # Charts row
    left, right = st.columns([1.5, 1])

    with left:
        section("Cash flow overview")

        monthly = get_monthly_totals(currency)

        if not monthly.empty:
            fig = px.bar(
                monthly,
                x="month",
                y=["income", "expense"],
                barmode="group",
                color_discrete_sequence=["#6C5CE7", "#FDCB6E"],
                labels={
                    "month": "",
                    "value": "Amount",
                    "variable": ""
                }
            )
            fig.update_traces(
                marker_line_width=0,
                marker_cornerradius=6,
            )
            fig = chart_layout(fig, height=340)
            st.plotly_chart(fig, use_container_width=True)
        else:
            empty_state("📊", "No data yet", "Add transactions to see your cash flow trends.")

    with right:
        section("Spending breakdown")

        categories = get_category_totals(currency)

        if not categories.empty:
            colors = [
                "#6C5CE7", "#A29BFE", "#00B894", "#FDCB6E",
                "#E17055", "#74B9FF", "#FF7675", "#55EFC4",
                "#FD79A8", "#636E72", "#DFE6E9", "#B2BEC3"
            ]

            fig = px.pie(
                categories,
                names="category",
                values="amount",
                hole=.72,
                color_discrete_sequence=colors,
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent",
                textfont_size=11,
                marker_line_width=2,
                marker_line_color="white",
            )

            fig = chart_layout(fig, height=340)
            st.plotly_chart(fig, use_container_width=True)
        else:
            empty_state("🍩", "No expenses yet", "Your spending breakdown will appear here.")

    # Recent transactions
    section("Recent transactions")

    if transactions:
        recent = transactions[:7]

        for t in recent:
            icon = CATEGORY_ICONS.get(t["category"], "📌")
            badge_class = f"txn-{t['kind'].lower()}"
            sign = "+" if t["kind"] == "Income" else "-" if t["kind"] == "Expense" else "⇄"
            amount_color = "var(--green)" if t["kind"] == "Income" else "var(--red)" if t["kind"] == "Expense" else "var(--primary)"

            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                        background:white;border:1px solid var(--border);border-radius:var(--radius-md);
                        padding:14px 20px;margin-bottom:6px;transition:all .15s ease;">
                <div style="display:flex;align-items:center;gap:14px;">
                    <span style="font-size:22px;">{icon}</span>
                    <div>
                        <div style="font-weight:600;color:var(--text);font-size:14px;">
                            {t['description'] or t['category']}
                        </div>
                        <div style="font-size:12px;color:var(--text-secondary);">
                            {t['transaction_date']} · {t['account'] or ''}
                            <span class="txn-badge {badge_class}" style="margin-left:8px;">{t['kind']}</span>
                        </div>
                    </div>
                </div>
                <div style="font-weight:700;color:{amount_color};font-size:16px;letter-spacing:-0.3px;">
                    {sign}{money(t['amount'], t['currency'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        empty_state("📝", "No transactions yet", "Add your first transaction to get started.")

    # Account cards
    if account_balances:
        section("Your accounts")

        cols = st.columns(min(3, len(account_balances)))

        for i, acc in enumerate(account_balances):
            with cols[i % len(cols)]:
                icon = ACCOUNT_ICONS.get(acc["type"], "💼")
                st.markdown(f"""
                <div class="account-card">
                    <div class="account-icon">{icon}</div>
                    <div class="account-name">{acc['name']}</div>
                    <div class="account-type">{acc['type']} · {acc['currency']}</div>
                    <div class="account-balance">{money(acc['balance_base'], currency)}</div>
                </div>
                """, unsafe_allow_html=True)


# ==========================================================
# TRANSACTIONS
# ==========================================================

elif page == "Transactions":

    heading(
        "Transactions",
        "Every transaction, organized in one place."
    )

    # Add transaction in expander
    with st.expander("➕ Add a new transaction", expanded=False):

        with st.form("transaction_form", clear_on_submit=True):

            col1, col2, col3 = st.columns(3)

            kind = col1.selectbox(
                "Type",
                ["Expense", "Income", "Transfer"],
                help="Select the transaction type"
            )

            amount = col2.number_input(
                "Amount",
                min_value=0.01,
                max_value=1_000_000_000_000.0,
                value=100.0,
                step=100.0,
                format="%.2f",
                help="Enter any transaction amount."
            )

            transaction_currency = col3.selectbox(
                "Currency",
                list(CURRENCIES.keys()),
                format_func=lambda c: f"{CURRENCY_SYMBOLS.get(c, c)} {c}",
            )

            col4, col5, col6 = st.columns(3)

            # Show relevant categories based on type
            category_options = INCOME_CATEGORIES if kind == "Income" else EXPENSE_CATEGORIES if kind == "Expense" else CATEGORIES
            category = col4.selectbox("Category", category_options)

            account_names = [a["name"] for a in accounts]

            account_sel = col5.selectbox(
                "From account",
                account_names if account_names else ["Create an account first"]
            )

            destination = col6.selectbox(
                "To account",
                account_names if account_names else ["Create an account first"],
                disabled=(kind != "Transfer")
            )

            col7, col8 = st.columns(2)

            transaction_date = col7.date_input("Date", value=date.today())

            description = col8.text_input(
                "Description",
                placeholder="e.g. Grocery shopping at BigBasket"
            )

            submitted = st.form_submit_button(
                "💾  Save transaction",
                type="primary",
                use_container_width=True
            )

            if submitted:
                if not accounts:
                    st.error("Please create an account first.")
                elif kind == "Transfer" and account_sel == destination:
                    st.error("Please choose two different accounts for a transfer.")
                else:
                    add_transaction(
                        kind=kind,
                        amount=amount,
                        currency=transaction_currency,
                        category=category,
                        account=account_sel,
                        transaction_date=str(transaction_date),
                        description=description,
                        destination_account=(
                            destination if kind == "Transfer" else None
                        ),
                        exchange_rate=convert_to_base(
                            1.0, transaction_currency, "INR"
                        )
                    )
                    st.toast("✅ Transaction saved!", icon="💸")
                    st.rerun()

    # Filters
    section("Transaction history")

    if transactions:
        # Filter bar
        filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])

        search = filter_col1.text_input(
            "🔍 Search",
            placeholder="Search by description, category, or account...",
            label_visibility="collapsed"
        )

        kind_filter = filter_col2.selectbox(
            "Type",
            ["All", "Income", "Expense", "Transfer"],
            label_visibility="collapsed"
        )

        date_range = filter_col3.selectbox(
            "Period",
            ["All time", "This month", "Last 30 days", "Last 90 days", "This year"],
            label_visibility="collapsed"
        )

        df = pd.DataFrame(transactions)

        # Apply filters
        if search:
            mask = df.astype(str).apply(
                lambda column: column.str.contains(search, case=False, na=False)
            ).any(axis=1)
            df = df[mask]

        if kind_filter != "All":
            df = df[df["kind"] == kind_filter]

        if date_range != "All time":
            today = date.today()
            if date_range == "This month":
                start = today.replace(day=1)
            elif date_range == "Last 30 days":
                start = today - timedelta(days=30)
            elif date_range == "Last 90 days":
                start = today - timedelta(days=90)
            elif date_range == "This year":
                start = today.replace(month=1, day=1)
            df = df[df["transaction_date"] >= str(start)]

        # Display columns
        display_columns = [
            "transaction_date", "kind", "description",
            "category", "account", "amount", "currency"
        ]
        display_columns = [c for c in display_columns if c in df.columns]

        st.dataframe(
            df[display_columns],
            use_container_width=True,
            hide_index=True,
            column_config={
                "transaction_date": st.column_config.DateColumn("Date", format="DD MMM YYYY"),
                "kind": "Type",
                "description": "Description",
                "category": "Category",
                "account": "Account",
                "amount": st.column_config.NumberColumn("Amount", format="%.2f"),
                "currency": "Currency"
            }
        )

        # Actions row
        action_col1, action_col2 = st.columns(2)

        with action_col1:
            st.download_button(
                "📥  Download CSV",
                df[display_columns].to_csv(index=False).encode("utf-8"),
                "finmee-transactions.csv",
                "text/csv"
            )

        with action_col2:
            st.caption(f"Showing {len(df)} of {len(transactions)} transactions")

        # Delete section
        with st.expander("🗑️ Delete a transaction"):
            transaction_options = {
                f'{t["transaction_date"]} · {t["description"] or t["category"]} · {money(t["amount"], t["currency"])}': t["id"]
                for t in transactions
            }

            selected = st.selectbox(
                "Select transaction to delete",
                [""] + list(transaction_options.keys()),
                label_visibility="collapsed"
            )

            if selected and st.button("Delete selected transaction", type="primary"):
                delete_transaction(transaction_options[selected])
                st.toast("🗑️ Transaction deleted.", icon="✅")
                st.rerun()

    else:
        empty_state("📝", "No transactions yet", "Click 'Add a new transaction' above to get started.")


# ==========================================================
# ACCOUNTS
# ==========================================================

elif page == "Accounts":

    heading(
        "Accounts & wallets",
        "Manage your money across different accounts."
    )

    with st.expander("➕ Add a new account", expanded=not bool(accounts)):

        with st.form("account_form", clear_on_submit=True):

            col1, col2 = st.columns(2)

            name = col1.text_input(
                "Account name",
                placeholder="e.g. HDFC Savings"
            )

            account_type = col2.selectbox(
                "Account type",
                ACCOUNT_TYPES,
                format_func=lambda t: f"{ACCOUNT_ICONS.get(t, '💼')} {t}"
            )

            col3, col4 = st.columns(2)

            account_currency = col3.selectbox(
                "Currency",
                list(CURRENCIES.keys()),
                format_func=lambda c: f"{CURRENCY_SYMBOLS.get(c, c)} {c}",
            )

            opening_balance = col4.number_input(
                "Opening balance",
                min_value=0.0,
                value=0.0
            )

            submitted = st.form_submit_button(
                "🏦  Create account",
                type="primary"
            )

            if submitted:
                if not name.strip():
                    st.error("Please enter an account name.")
                else:
                    try:
                        add_account(
                            name.strip(),
                            account_type,
                            account_currency,
                            opening_balance
                        )
                        st.toast("🏦 Account created!", icon="✅")
                        st.rerun()
                    except Exception:
                        st.error("An account with this name may already exist.")

    section("Your accounts")

    if account_balances:

        # Total balance summary
        st.markdown(f"""
        <div style="background:var(--primary-bg);border-radius:var(--radius-lg);
                    padding:20px 24px;margin-bottom:20px;border:1px solid rgba(108,92,231,.1);">
            <div style="font-size:12px;font-weight:600;color:var(--primary);
                        letter-spacing:.5px;text-transform:uppercase;">Combined Balance</div>
            <div style="font-size:28px;font-weight:800;color:var(--primary);
                        letter-spacing:-1px;margin-top:4px;">{money(total_balance, currency)}</div>
            <div style="font-size:12px;color:var(--text-secondary);margin-top:4px;">
                Across {len(account_balances)} account(s) in {currency}
            </div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(min(3, len(account_balances)))

        for i, acc in enumerate(account_balances):
            with cols[i % len(cols)]:
                icon = ACCOUNT_ICONS.get(acc["type"], "💼")
                balance_color = "var(--green)" if acc["balance_base"] >= 0 else "var(--red)"

                st.markdown(f"""
                <div class="account-card">
                    <div class="account-icon">{icon}</div>
                    <div class="account-name">{acc['name']}</div>
                    <div class="account-type">{acc['type']} · {acc['currency']}</div>
                    <div class="account-balance" style="color:{balance_color};">
                        {money(acc['balance_base'], currency)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.write("")

        # Delete account
        with st.expander("🗑️ Delete an account"):
            account_options = {
                f"{ACCOUNT_ICONS.get(a['type'], '💼')} {a['name']} ({a['type']})": a["id"]
                for a in accounts
            }

            selected_account = st.selectbox(
                "Select account to delete",
                [""] + list(account_options.keys()),
                label_visibility="collapsed"
            )

            if selected_account:
                st.warning("⚠️ Deleting an account does NOT delete its transactions.")
                if st.button("Delete account", type="primary"):
                    delete_account(account_options[selected_account])
                    st.toast("🗑️ Account deleted.", icon="✅")
                    st.rerun()

    else:
        empty_state("🏦", "No accounts yet", "Create your first account to start tracking your money.")


# ==========================================================
# BUDGETS
# ==========================================================

elif page == "Budgets":

    heading(
        "Budgets",
        "Set spending limits and stay in control."
    )

    with st.expander("➕ Create a monthly budget", expanded=False):

        with st.form("budget_form", clear_on_submit=True):

            col1, col2, col3 = st.columns(3)

            category = col1.selectbox(
                "Category",
                EXPENSE_CATEGORIES,
                format_func=lambda c: f"{CATEGORY_ICONS.get(c, '📌')} {c}"
            )

            limit_amount = col2.number_input(
                "Monthly limit",
                min_value=1.0,
                value=5000.0,
                step=500.0
            )

            month = col3.date_input(
                "Budget month",
                value=date.today().replace(day=1)
            )

            submitted = st.form_submit_button(
                "📋  Create budget",
                type="primary",
                use_container_width=True
            )

            if submitted:
                add_budget(
                    category,
                    limit_amount,
                    currency,
                    month.strftime("%Y-%m")
                )
                st.toast("📋 Budget created!", icon="✅")
                st.rerun()

    section("Budget performance")

    budgets = get_budgets()

    if budgets:

        for budget in budgets:

            spent = sum(
                base_amount(t, currency)
                for t in transactions
                if t["kind"] == "Expense"
                and t["category"] == budget["category"]
                and t["transaction_date"].startswith(budget["month"])
            )

            budget_limit = convert_to_base(
                budget["limit_amount"],
                budget["currency"],
                currency
            )

            percentage = calculate_budget_usage(spent, budget_limit)
            remaining = calculate_remaining_budget(spent, budget_limit)
            status_text, status_emoji = get_budget_status(spent, budget_limit)

            # Status styling
            if percentage >= 100:
                status_class = "status-danger"
                bar_color = "var(--red)"
            elif percentage >= 80:
                status_class = "status-warning"
                bar_color = "var(--amber)"
            else:
                status_class = "status-on-track"
                bar_color = "var(--green)"

            icon = CATEGORY_ICONS.get(budget["category"], "📌")

            with st.container(border=True):

                top1, top2 = st.columns([3, 1])

                with top1:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:10px;">
                        <span style="font-size:24px;">{icon}</span>
                        <div>
                            <div style="font-weight:700;font-size:15px;color:var(--text);">
                                {budget['category']}
                            </div>
                            <div style="font-size:12px;color:var(--text-secondary);">
                                {budget['month']}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with top2:
                    st.markdown(f"""
                    <div style="text-align:right;">
                        <span class="budget-status-pill {status_class}">
                            {status_emoji} {status_text}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

                st.progress(min(percentage / 100, 1.0))

                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-top:-8px;">
                    <span style="color:var(--text-secondary);">
                        {money(spent, currency)} of {money(budget_limit, currency)}
                    </span>
                    <span style="font-weight:600;color:{'var(--green)' if remaining >= 0 else 'var(--red)'};">
                        {money(abs(remaining), currency)} {'remaining' if remaining >= 0 else 'over'}
                    </span>
                </div>
                """, unsafe_allow_html=True)

                if st.button(
                    "🗑️ Delete",
                    key=f'delete_budget_{budget["id"]}',
                ):
                    delete_budget(budget["id"])
                    st.toast("🗑️ Budget deleted.", icon="✅")
                    st.rerun()

    else:
        empty_state("📋", "No budgets yet", "Create a monthly budget to track your spending limits.")


# ==========================================================
# FINANCIAL GOALS
# ==========================================================

elif page == "Goals":

    heading(
        "Financial goals",
        "Turn your savings plans into achievements."
    )

    with st.expander("➕ Create a savings goal", expanded=False):

        with st.form("goal_form", clear_on_submit=True):

            name = st.text_input(
                "Goal name",
                placeholder="e.g. New MacBook, Emergency Fund, Vacation"
            )

            col1, col2, col3 = st.columns(3)

            target = col1.number_input(
                "Target amount",
                min_value=1.0,
                value=50000.0,
                step=1000.0
            )

            saved = col2.number_input(
                "Already saved",
                min_value=0.0,
                value=0.0
            )

            goal_currency = col3.selectbox(
                "Currency",
                list(CURRENCIES.keys()),
                format_func=lambda c: f"{CURRENCY_SYMBOLS.get(c, c)} {c}",
            )

            due_date = st.date_input(
                "Target date",
                date.today() + timedelta(days=180)
            )

            submitted = st.form_submit_button(
                "🎯  Create goal",
                type="primary",
                use_container_width=True
            )

            if submitted:
                if name.strip():
                    add_goal(
                        name.strip(),
                        target,
                        saved,
                        goal_currency,
                        str(due_date)
                    )
                    st.toast("🎯 Goal created!", icon="✅")
                    st.rerun()
                else:
                    st.error("Please enter a goal name.")

    section("Your savings goals")

    goals = get_goals()

    if goals:

        for goal in goals:

            with st.container(border=True):

                target_amount = goal["target_amount"]
                saved_amount = goal["saved_amount"]
                remaining = max(target_amount - saved_amount, 0)

                percentage = (
                    saved_amount / target_amount * 100
                    if target_amount > 0 else 0
                )

                days_left = days_until(goal["due_date"])

                # Color based on progress
                if percentage >= 100:
                    color = "var(--green)"
                    status = "🎉 Completed!"
                elif percentage >= 50:
                    color = "var(--primary)"
                    status = f"📅 {days_left} days left"
                else:
                    color = "var(--amber)"
                    status = f"📅 {days_left} days left"

                top1, top2 = st.columns([3, 1])

                with top1:
                    st.markdown(f"""
                    <div>
                        <div style="font-size:18px;font-weight:700;color:var(--text);">
                            🎯 {goal['name']}
                        </div>
                        <div style="font-size:12px;color:var(--text-secondary);margin-top:2px;">
                            {status} · Due {goal['due_date']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with top2:
                    st.markdown(f"""
                    <div class="goal-progress-ring" style="text-align:right;color:{color};">
                        {min(percentage, 100):.0f}%
                    </div>
                    """, unsafe_allow_html=True)

                st.progress(min(percentage / 100, 1.0))

                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-top:-8px;">
                    <span style="color:var(--text-secondary);">
                        {money(saved_amount, goal['currency'])} saved
                    </span>
                    <span style="font-weight:600;color:var(--text);">
                        {money(remaining, goal['currency'])} to go
                    </span>
                </div>
                """, unsafe_allow_html=True)

                st.write("")

                uc1, uc2, uc3 = st.columns([2, 1, 1])

                new_saved = uc1.number_input(
                    "Update saved",
                    min_value=0.0,
                    value=float(saved_amount),
                    key=f'goal_saved_{goal["id"]}',
                    label_visibility="collapsed"
                )

                with uc2:
                    if st.button(
                        "💾 Update",
                        key=f'update_goal_{goal["id"]}',
                        use_container_width=True
                    ):
                        update_goal(goal["id"], new_saved)
                        st.toast("✅ Goal updated!", icon="🎯")
                        st.rerun()

                with uc3:
                    if st.button(
                        "🗑️ Delete",
                        key=f'delete_goal_{goal["id"]}',
                        use_container_width=True
                    ):
                        delete_goal(goal["id"])
                        st.toast("🗑️ Goal deleted.", icon="✅")
                        st.rerun()

    else:
        empty_state("🎯", "No goals yet", "Create a savings goal to start tracking your progress.")


# ==========================================================
# ANALYTICS
# ==========================================================

elif page == "Analytics":

    heading(
        "Financial analytics",
        "Understand your financial habits through data."
    )

    # Financial Health Score
    st.markdown(f"""
    <div style="background:white;border:1px solid var(--border);border-radius:var(--radius-xl);
                padding:28px;text-align:center;box-shadow:var(--shadow-sm);margin-bottom:24px;">
        <div class="health-score-circle" style="background:{health['color']};">
            {health['score']}
        </div>
        <div style="font-size:18px;font-weight:700;color:var(--text);margin-bottom:4px;">
            {health['emoji']} {health['status']}
        </div>
        <div style="font-size:13px;color:var(--text-secondary);">
            Financial Health Score · {health['savings_rate']}% savings rate
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Income", money(total_income, currency))
    c2.metric("Expenses", money(total_expenses, currency))
    c3.metric("Net Savings", money(net_savings, currency))
    c4.metric("Savings Rate", f"{savings_rate:.1f}%")

    # Charts
    tab1, tab2, tab3 = st.tabs(["📊 Cash Flow", "🍩 Categories", "📈 Trends"])

    with tab1:
        monthly = get_monthly_totals(currency)

        if not monthly.empty:
            # Bar chart
            fig = px.bar(
                monthly,
                x="month",
                y=["income", "expense"],
                barmode="group",
                color_discrete_sequence=["#6C5CE7", "#FDCB6E"],
                labels={"month": "", "value": "Amount", "variable": ""}
            )
            fig.update_traces(marker_cornerradius=6)
            fig = chart_layout(fig, height=400)
            st.plotly_chart(fig, use_container_width=True)

            # Net savings line
            monthly["net"] = monthly["income"] - monthly["expense"]
            fig2 = px.area(
                monthly,
                x="month",
                y="net",
                color_discrete_sequence=["#6C5CE7"],
                labels={"month": "", "net": "Net Savings"}
            )
            fig2.update_traces(
                fill="tozeroy",
                fillcolor="rgba(108,92,231,.08)",
                line_width=2.5,
            )
            fig2 = chart_layout(fig2, height=250)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            empty_state("📊", "No data yet", "Add transactions to generate analytics.")

    with tab2:
        categories = get_category_totals(currency)

        if not categories.empty:
            left, right = st.columns([1, 1])

            with left:
                colors = [
                    "#6C5CE7", "#A29BFE", "#00B894", "#FDCB6E",
                    "#E17055", "#74B9FF", "#FF7675", "#55EFC4",
                    "#FD79A8", "#636E72"
                ]
                fig = px.pie(
                    categories,
                    names="category",
                    values="amount",
                    hole=.72,
                    color_discrete_sequence=colors,
                )
                fig.update_traces(
                    textposition="inside",
                    textinfo="percent",
                    marker_line_width=2,
                    marker_line_color="white",
                )
                fig = chart_layout(fig, height=380)
                st.plotly_chart(fig, use_container_width=True)

            with right:
                fig = px.bar(
                    categories,
                    x="amount",
                    y="category",
                    orientation="h",
                    color="amount",
                    color_continuous_scale=[[0, "#A29BFE"], [1, "#6C5CE7"]],
                    labels={"amount": "Amount", "category": ""}
                )
                fig.update_traces(marker_cornerradius=6)
                fig.update_coloraxes(showscale=False)
                fig = chart_layout(fig, height=380)
                st.plotly_chart(fig, use_container_width=True)

                # Top 3 categories
                st.markdown("**Top spending categories:**")
                for _, row in categories.head(3).iterrows():
                    icon = CATEGORY_ICONS.get(row["category"], "📌")
                    st.markdown(f"{icon} **{row['category']}** — {money(row['amount'], currency)}")

        else:
            empty_state("🍩", "No data yet", "Add expenses to see category breakdown.")

    with tab3:
        monthly = get_monthly_totals(currency)

        if not monthly.empty:
            fig = px.line(
                monthly,
                x="month",
                y=["income", "expense"],
                markers=True,
                color_discrete_sequence=["#6C5CE7", "#E17055"],
                labels={"month": "", "value": "Amount", "variable": ""}
            )
            fig.update_traces(line_width=2.5)
            fig = chart_layout(fig, height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            empty_state("📈", "No trends yet", "Add transactions across multiple months to see trends.")


# ==========================================================
# RECURRING TRANSACTIONS
# ==========================================================

elif page == "Recurring":

    heading(
        "Recurring transactions",
        "Manage your subscriptions, EMIs, and regular payments."
    )

    with st.expander("➕ Add a recurring transaction", expanded=False):

        with st.form("recurring_form", clear_on_submit=True):

            col1, col2, col3 = st.columns(3)

            kind = col1.selectbox("Type", ["Expense", "Income"])
            amount = col2.number_input("Amount", min_value=0.01, value=500.0, step=100.0)
            rec_currency = col3.selectbox(
                "Currency",
                list(CURRENCIES.keys()),
                format_func=lambda c: f"{CURRENCY_SYMBOLS.get(c, c)} {c}",
            )

            col4, col5, col6 = st.columns(3)

            category = col4.selectbox("Category", CATEGORIES,
                                      format_func=lambda c: f"{CATEGORY_ICONS.get(c, '📌')} {c}")

            account_names = [a["name"] for a in accounts]
            account_sel = col5.selectbox(
                "Account",
                account_names if account_names else ["Create an account first"]
            )

            frequency = col6.selectbox("Frequency", ["Monthly", "Weekly", "Yearly"])

            col7, col8 = st.columns(2)
            next_date = col7.date_input("Next due date", value=date.today())
            description = col8.text_input("Description", placeholder="e.g. Netflix subscription")

            submitted = st.form_submit_button(
                "🔄  Add recurring",
                type="primary",
                use_container_width=True
            )

            if submitted:
                if not accounts:
                    st.error("Please create an account first.")
                else:
                    add_recurring_transaction(
                        kind=kind,
                        amount=amount,
                        currency=rec_currency,
                        category=category,
                        account=account_sel,
                        description=description,
                        frequency=frequency,
                        next_date=str(next_date)
                    )
                    st.toast("🔄 Recurring transaction added!", icon="✅")
                    st.rerun()

    section("Active recurring transactions")

    recurring = get_recurring_transactions()

    if recurring:
        for rec in recurring:
            icon = CATEGORY_ICONS.get(rec["category"], "📌")
            days = days_until(rec["next_date"]) if rec.get("next_date") else None

            with st.container(border=True):
                left, right = st.columns([3, 1])

                with left:
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;">
                        <span style="font-size:24px;">{icon}</span>
                        <div>
                            <div style="font-weight:700;color:var(--text);">
                                {rec['description'] or rec['category']}
                            </div>
                            <div style="font-size:12px;color:var(--text-secondary);">
                                {rec['frequency']} · {rec['account'] or ''}
                                {f' · Next: {rec["next_date"]}' if rec.get('next_date') else ''}
                                {f' ({days}d away)' if days is not None else ''}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with right:
                    amount_color = "var(--red)" if rec["kind"] == "Expense" else "var(--green)"
                    st.markdown(f"""
                    <div style="text-align:right;">
                        <div style="font-size:18px;font-weight:700;color:{amount_color};">
                            {money(rec['amount'], rec['currency'])}
                        </div>
                        <div style="font-size:11px;color:var(--text-secondary);">/{rec['frequency'].lower()}</div>
                    </div>
                    """, unsafe_allow_html=True)

                if st.button("🗑️ Remove", key=f'del_rec_{rec["id"]}'):
                    delete_recurring_transaction(rec["id"])
                    st.toast("🗑️ Recurring transaction removed.", icon="✅")
                    st.rerun()
    else:
        empty_state("🔄", "No recurring transactions", "Add subscriptions, EMIs, or regular payments to track them.")


# ==========================================================
# REPORTS
# ==========================================================

elif page == "Reports":

    heading(
        "Reports & exports",
        "Your financial records, organized and ready to export."
    )

    section("Financial summary")

    # Summary cards
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Income", money(total_income, currency))
    c2.metric("Total Expenses", money(total_expenses, currency))
    c3.metric("Net Savings", money(net_savings, currency))
    c4.metric("Savings Rate", f"{savings_rate:.1f}%")

    # Financial health
    section("Financial health")

    st.markdown(f"""
    <div style="background:white;border:1px solid var(--border);border-radius:var(--radius-lg);
                padding:24px;display:flex;align-items:center;gap:24px;box-shadow:var(--shadow-sm);">
        <div class="health-score-circle" style="background:{health['color']};
                    width:80px;height:80px;font-size:22px;flex-shrink:0;">
            {health['score']}
        </div>
        <div>
            <div style="font-size:16px;font-weight:700;color:var(--text);">
                {health['emoji']} {health['status']}
            </div>
            <div style="font-size:13px;color:var(--text-secondary);margin-top:4px;">
                Your savings rate is {health['savings_rate']}%.
                {'Great job! Keep it up.' if health['savings_rate'] >= 20 else 'Try to save at least 20% of your income.'}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Reports
    section("Transaction report")

    if transactions:
        df = pd.DataFrame(transactions)

        display_columns = [
            "transaction_date", "kind", "description",
            "category", "account", "amount", "currency"
        ]
        display_columns = [c for c in display_columns if c in df.columns]

        st.dataframe(
            df[display_columns],
            use_container_width=True,
            hide_index=True,
            column_config={
                "transaction_date": st.column_config.DateColumn("Date", format="DD MMM YYYY"),
                "kind": "Type",
                "amount": st.column_config.NumberColumn("Amount", format="%.2f"),
            }
        )

        # Export buttons
        exp1, exp2 = st.columns(2)

        with exp1:
            st.download_button(
                "📥  Download full report (CSV)",
                df[display_columns].to_csv(index=False).encode("utf-8"),
                "finmee-full-report.csv",
                "text/csv",
                type="primary",
                use_container_width=True
            )

        with exp2:
            # Category summary export
            cat_data = get_category_totals(currency)
            if not cat_data.empty:
                st.download_button(
                    "📊  Download category summary (CSV)",
                    cat_data.to_csv(index=False).encode("utf-8"),
                    "finmee-category-summary.csv",
                    "text/csv",
                    use_container_width=True
                )

    else:
        empty_state("📑", "No data yet", "Add transactions to generate reports.")


# ==========================================================
# FOOTER
# ==========================================================

st.write("")
st.divider()

st.markdown(
    """
    <div class="finmee-footer">
        ◈ <b>FinMee</b> · Your money. Your control.<br>
        Smart Personal Finance Management · Made with 💜 by Rachit
    </div>
    """,
    unsafe_allow_html=True
)
