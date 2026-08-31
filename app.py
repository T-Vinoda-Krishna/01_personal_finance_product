import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="SpendWise", layout="wide")
st.title("SpendWise — Personal Finance Product Prototype")
st.caption("Self-directed product MVP using synthetic demo data.")

@st.cache_data
def sample_data():
    rng = np.random.default_rng(42)
    dates = pd.date_range("2026-01-01", "2026-06-30", freq="D")
    categories = ["Rent", "Food", "Transport", "Shopping", "Entertainment", "Utilities", "Health"]
    rows = []
    for i in range(700):
        d = dates[rng.integers(0, len(dates))]
        c = rng.choice(categories, p=[0.10,0.25,0.14,0.18,0.10,0.12,0.11])
        base = {"Rent":18000,"Food":650,"Transport":420,"Shopping":1500,"Entertainment":500,"Utilities":1200,"Health":900}[c]
        amount = max(50, rng.lognormal(np.log(base), 0.45))
        rows.append([d, f"{c} merchant", round(amount,2), c])
    return pd.DataFrame(rows, columns=["date","description","amount","category"]).sort_values("date")

df = sample_data()
uploaded = st.file_uploader("Upload transactions CSV (date, description, amount, category)", type="csv")
if uploaded:
    try:
        df = pd.read_csv(uploaded, parse_dates=["date"])
    except Exception as e:
        st.error(f"Could not read file: {e}")

df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
month = st.selectbox("Month", sorted(df["month"].unique(), reverse=True))
m = df[df["month"] == month].copy()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total spend", f"₹{m.amount.sum():,.0f}")
col2.metric("Transactions", f"{len(m):,}")
col3.metric("Avg transaction", f"₹{m.amount.mean():,.0f}")
col4.metric("Top category", m.groupby("category").amount.sum().idxmax())

st.subheader("Spend by category")
cat = m.groupby("category", as_index=False).amount.sum().sort_values("amount", ascending=False)
st.plotly_chart(px.bar(cat, x="category", y="amount", title="Monthly spending"), use_container_width=True)

st.subheader("Budget tracker")
budgets = {}
for c in cat["category"]:
    budgets[c] = st.number_input(f"{c} budget", min_value=0.0, value=float(max(5000, cat.loc[cat.category==c,"amount"].iloc[0]*1.15)), step=500.0)
budget_df = cat.copy()
budget_df["budget"] = budget_df["category"].map(budgets)
budget_df["utilization_pct"] = 100*budget_df["amount"]/budget_df["budget"]
st.dataframe(budget_df.style.format({"amount":"₹{:,.0f}","budget":"₹{:,.0f}","utilization_pct":"{:.1f}%"}), use_container_width=True)

st.subheader("Unusual spending alerts")
q90 = df.amount.quantile(0.90)
alerts = m[m.amount >= q90][["date","description","amount","category"]].sort_values("amount", ascending=False)
st.dataframe(alerts.head(15), use_container_width=True)
