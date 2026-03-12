import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="BudgetBuddy Pro", layout="wide")

st.title("BudgetBuddy Pro")
st.markdown("### Smart Expense Tracking Dashboard")

file = "data.csv"

# Load or create data
if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=["Date", "Category", "Amount"])
    df.to_csv(file, index=False)

# Sidebar
st.sidebar.header("➕ Add New Expense")

date = st.sidebar.date_input("Date", datetime.today())
category = st.sidebar.selectbox(
    "Category",
    ["Food", "Travel", "Shopping", "Bills", "Health", "Entertainment", "Other"]
)
amount = st.sidebar.number_input("Amount (₹)", min_value=0.0)

if st.sidebar.button("Add Expense"):
    new_entry = pd.DataFrame([[date, category, amount]],
                             columns=["Date", "Category", "Amount"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(file, index=False)
    st.sidebar.success("Expense Added!")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Filter Section
st.sidebar.header("🔍 Filters")
selected_month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + sorted(df["Date"].dt.strftime("%B %Y").dropna().unique())
)

if selected_month != "All":
    df = df[df["Date"].dt.strftime("%B %Y") == selected_month]

# Metrics
total_spending = df["Amount"].sum()
avg_spending = df["Amount"].mean() if not df.empty else 0
max_spending = df["Amount"].max() if not df.empty else 0

col1, col2, col3 = st.columns(3)

col1.metric(" Total Spending", f"₹ {total_spending:,.2f}")
col2.metric("Average Expense", f"₹ {avg_spending:,.2f}")
col3.metric("Highest Expense", f"₹ {max_spending:,.2f}")

st.divider()

# Charts
if not df.empty:
    st.subheader("Category-wise Spending")

    category_summary = df.groupby("Category")["Amount"].sum()

    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(category_summary)

    with col2:
        st.write("### Spending Distribution")
        st.pyplot(category_summary.plot.pie(autopct="%1.1f%%", figsize=(4, 4)).figure)

st.divider()

# Expense Table
st.subheader("Expense History")
st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)

st.markdown("---")
st.markdown("Built with using Streamlit")
