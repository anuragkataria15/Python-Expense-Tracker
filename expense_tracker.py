import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---------- File Setup ----------
FILE = "expenses.csv"
if not os.path.exists(FILE):
    pd.DataFrame(columns=["Date", "Category", "Amount", "Description"]).to_csv(FILE, index=False)

# ---------- Page Config ----------
st.set_page_config(page_title="Expense Tracker", page_icon="💸", layout="centered")

st.title("💸 Expense Tracker Dashboard")
st.caption("A modern, minimal expense tracker built with Python & Streamlit")

# ---------- Load Data ----------
def load_data():
    return pd.read_csv(FILE)

# ---------- Add Expense ----------
with st.expander("➕ Add New Expense", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        category = st.text_input("Category (e.g., Food, Travel, Bills)")
        amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
    with col2:
        desc = st.text_input("Description (optional)")
        date = st.date_input("Date", datetime.now())
    
    if st.button("Add Expense", use_container_width=True):
        new_row = pd.DataFrame([[date, category, amount, desc]], 
                               columns=["Date", "Category", "Amount", "Description"])
        df = load_data()
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("Expense added successfully! ✅")

# ---------- View / Analyze ----------
st.subheader("📊 Expense Summary")

df = load_data()
if df.empty:
    st.info("No expenses added yet. Add your first record above!")
else:
    st.dataframe(df, use_container_width=True)

    total = df["Amount"].sum()
    st.metric("Total Spent", f"₹{total:,.2f}")

    # Category-wise chart
    st.bar_chart(df.groupby("Category")["Amount"].sum(), use_container_width=True)

# ---------- Footer ----------
st.markdown("---")
st.caption("Built by **Anurag Kataria** | CT University | Python • Streamlit • Data Handling")
