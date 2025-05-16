import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

st.set_page_config(page_title="MSTY Monitoring Tool", layout="wide")
st.title("📊 MSTY Stock Monitoring & Simulation Suite")

tabs = st.tabs([
    "📊 Compounding Simulator",
    "📈 Market Monitoring",
    "📐 Cost Basis Tools",
    "🛡️ Hedging Tools",
    "📤 Export Center"
])

# Tab 4: Hedging Tools
with tabs[3]:
    st.header("🛡️ Hedging Tools with Live Options Data")

    shares_to_hedge = st.number_input("Shares to Hedge", min_value=0, value=10000)
    current_price = st.number_input("Current Share Price ($)", min_value=0.0, value=1250.0)
    expected_exit_price = st.number_input("Expected Exit Price ($)", min_value=0.0, value=1000.0)

    ticker = "MSTR"
    try:
        stock = yf.Ticker(ticker)
        expirations = stock.options
        selected_expiry = st.selectbox("Select Expiration Date", expirations)

        option_chain = stock.option_chain(selected_expiry)
        puts = option_chain.puts
        puts = puts.sort_values("strike")

        # Suggest a strike price close to current price
        closest_strike = puts.iloc[(puts["strike"] - current_price).abs().argsort()[:1]]
        suggested_strike = closest_strike["strike"].values[0]
        est_price = closest_strike["lastPrice"].values[0]

        st.success(f"Suggested Strike: ${suggested_strike}, Estimated Option Cost: ${est_price:.2f}")

        total_contracts = shares_to_hedge / 100
        total_hedge_cost = est_price * total_contracts * 100
        total_cashout = shares_to_hedge * expected_exit_price
        payout = (suggested_strike - expected_exit_price) * shares_to_hedge
        net = payout - total_hedge_cost

        st.metric("📉 Total Hedge Cost", f"${total_hedge_cost:,.2f}")
        st.metric("💵 Exit Cashout", f"${total_cashout:,.2f}")
        st.metric("📈 Net Hedge Benefit", f"${net:,.2f}")
    except Exception as e:
        st.error("Unable to fetch live option data. Please check connection or try later.")