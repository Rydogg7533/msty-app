
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import matplotlib.pyplot as plt
from fpdf import FPDF
import yagmail
from io import BytesIO

st.set_page_config(page_title="MSTY Stock Monitoring & Simulation Suite", layout="wide")
st.title("📊 MSTY Stock Monitoring & Simulation Suite")

tabs = st.tabs([
    "📈 Compounding Simulator",
    "📉 Market Monitoring",
    "📐 Cost Basis Tools",
    "🛡️ Hedging Tools",
    "📤 Export Center"
])

# --- Tab 1: Compounding Simulator ---
with tabs[0]:
    st.header("📈 Compounding Simulator")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        shares = st.number_input("Total Share Count", min_value=0, value=10000)
    with col2:
        dividend = st.number_input("Average Monthly Dividend per Share ($)", min_value=0.0, value=2.0)
    with col3:
        reinvest_price = st.number_input("Average Reinvestment Price ($)", min_value=0.01, value=25.0)
    with col4:
        months = st.number_input("Simulation Period (Months)", min_value=1, value=48)

    with st.expander("📌 Advanced Options"):
        drip_percent = st.slider("Percentage DRIP (Dividend Reinvestment %)", min_value=0, max_value=100, value=100)
        monthly_withdrawal = st.number_input("Fixed Monthly Withdrawal ($)", min_value=0, value=0)
        tax_rate = st.slider("Tax Rate on Dividends (%)", min_value=0, max_value=50, value=0)

    result = []
    current_shares = shares

    for month in range(1, months + 1):
        gross_dividends = current_shares * dividend
        after_tax = gross_dividends * (1 - tax_rate / 100)
        reinvest_amount = (after_tax - monthly_withdrawal) * (drip_percent / 100)
        new_shares = reinvest_amount / reinvest_price if reinvest_price else 0
        current_shares += new_shares
        result.append((month, current_shares, new_shares, gross_dividends, reinvest_amount))

    df_view = pd.DataFrame(result, columns=["Month", "Total Shares", "Shares Bought", "Dividends", "Reinvested"])

    st.dataframe(df_view)
    st.download_button("📊 Download Projection CSV", df_view.to_csv(index=False), "projection.csv")

# --- Tab 2: Market Monitoring ---
with tabs[1]:
    st.header("📉 Market Monitoring")
    st.info("Live options, covered call, and IV tracking will be shown here.")
    st.markdown("This section will be developed next.")

# --- Tab 3: Cost Basis Tools ---
with tabs[2]:
    st.header("📐 Cost Basis Calculator")
    st.info("Track multiple buy blocks and calculate weighted average price.")
    editor = st.data_editor(pd.DataFrame({
        "Shares": [0],
        "Price Per Share": [0.0]
    }), num_rows="dynamic", key="cost_basis")

    if not editor.empty:
        total_cost = (editor["Shares"] * editor["Price Per Share"]).sum()
        total_shares = editor["Shares"].sum()
        weighted_avg = total_cost / total_shares if total_shares else 0
        st.metric("Weighted Avg Cost", f"${weighted_avg:.2f}")

# --- Tab 4: Hedging Tools ---
with tabs[3]:
    st.header("🛡️ Hedge Estimator with Multi-Expiration Comparison")
    col1, col2, col3 = st.columns(3)
    with col1:
        hedge_shares = st.number_input("Shares to Hedge", value=10000)
    with col2:
        current_price = st.number_input("Current MSTR Price ($)", value=25.0)
    with col3:
        expected_exit = st.number_input("Expected Exit Price ($)", value=10.0)

    min_strike = round(expected_exit, 2)
    hedge_cost_est = (current_price - expected_exit) * 0.1  # Simulated premium
    est_cash_out = hedge_shares * expected_exit

    st.markdown(f"### 📌 Prefilled Strike Price: **${min_strike}**")
    st.markdown(f"### 💸 Estimated Option Premium per Share: **${hedge_cost_est:.2f}**")
    st.metric("Total Estimated Cash Out at Exit", f"${est_cash_out:,.2f}")

# --- Tab 5: Export Center ---
with tabs[4]:
    st.header("📤 Export Center")
    st.info("Export simulation, hedge, and tax reports as CSV or PDF.")

    if "df_view" in locals():
        st.download_button("📈 Download Projection CSV", df_view.to_csv(index=False), "projection.csv")

    if st.button("📨 Email PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="MSTY Stock Report", ln=1)
        pdf.cell(200, 10, txt=f"Final Shares: {int(current_shares)}", ln=2)
        pdf_output = BytesIO()
        pdf.output(pdf_output)
        yag = yagmail.SMTP("your@gmail.com", oauth2_file="credentials.json")
        yag.send(to="your@gmail.com", subject="MSTY Report", contents="Attached", attachments=pdf_output)
        st.success("Report emailed!")
import subprocess
st.subheader("🔍 Installed Packages (for debugging only)")
st.text(subprocess.getoutput('pip freeze'))
