# app.py — Bybit Take-Profit Bot (Spot, Unified API v5)

import streamlit as st
import time
from pybit.unified_trading import HTTP

st.set_page_config(page_title="Bybit Take-Profit Bot", layout="centered")
st.title("🦾 Bybit Take-Profit Bot")

if "running" not in st.session_state:
    st.session_state.running = False

# Sidebar: user inputs
st.sidebar.header("Bot Configuration")
api_key = st.sidebar.text_input("API Key", type="password")
api_secret = st.sidebar.text_input("API Secret", type="password")
symbol = st.sidebar.text_input("Symbol", value="ETHUSDT")
usdt_to_spend = st.sidebar.number_input("USDT to Spend", value=50.0, step=1.0)
take_profit_percent = st.sidebar.number_input("Take-Profit %", value=5.0, step=0.5)
testnet_mode = st.sidebar.checkbox("Use Testnet", value=True)

start = st.sidebar.button("🚀 Start Bot")
stop = st.sidebar.button("🛑 Stop Bot")
log_area = st.empty()

def run_bot():
    try:
        session = HTTP(api_key=api_key, api_secret=api_secret, testnet=testnet_mode)
        # initial price fetch
        price_data = session.get_tickers(category="spot", symbol=symbol)
        buy_price = float(price_data['result']['list'][0]['lastPrice'])
        quantity = round(usdt_to_spend / buy_price, 6)

        if quantity * buy_price < 1.0:
            st.error("❌ Order value too low — must be ≥ $1 USDT")
            return

        st.session_state.running = True
        log_area.markdown(f"✅ Price: **${buy_price:.2f}** → Buying **{quantity}**")

        target_price = buy_price * (1 + take_profit_percent / 100)
        log_area.markdown(f"🎯 Target price: **${target_price:.2f}**")

        session.place_order(
            category="spot",
            symbol=symbol,
            side="Buy",
            order_type="Market",
            qty=str(quantity)
        )
        log_area.markdown("📥 Buy order placed.")

        while st.session_state.running:
            price_data = session.get_tickers(category="spot", symbol=symbol)
            current_price = float(price_data['result']['list'][0]['lastPrice'])
            log_area.markdown(f"📈 Market: **${current_price:.2f}**")

            if current_price >= target_price:
                session.place_order(
                    category="spot",
                    symbol=symbol,
                    side="Sell",
                    order_type="Market",
                    qty=str(quantity)
                )
                log_area.markdown(f"💰 Sold at: **${current_price:.2f}**")
                st.session_state.running = False
                break

            time.sleep(5)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.session_state.running = False

if start and not st.session_state.running:
    run_bot()

if stop:
    st.session_state.running = False
    st.warning("🛑 Bot manually stopped!")
