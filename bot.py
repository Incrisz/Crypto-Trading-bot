import streamlit as st
import time
from pybit.unified_trading import HTTP

st.set_page_config(page_title="Bybit Take-Profit Bot", layout="centered")

st.title("🦾 Bybit Take-Profit Bot")

# Initialize session state
if "running" not in st.session_state:
    st.session_state.running = False

# Sidebar config
st.sidebar.header("Bot Configuration")
api_key = st.sidebar.text_input("API Key", type="password")
api_secret = st.sidebar.text_input("API Secret", type="password")
symbol = st.sidebar.text_input("Symbol", value="ETHUSDT")
usdt_to_spend = st.sidebar.number_input("USDT to Spend (quoteQty)", value=50.0, step=1.0)
take_profit_percent = st.sidebar.number_input("Take-Profit %", value=5.0, step=0.5)
testnet_mode = st.sidebar.checkbox("Use Testnet", value=True)

# Buttons
start = st.sidebar.button("🚀 Start Bot")
stop = st.sidebar.button("🛑 Stop Bot")

log_area = st.empty()

def run_bot():
    try:
        session = HTTP(api_key=api_key, api_secret=api_secret, testnet=testnet_mode)

        # Step 1: Get current price
        price_data = session.get_tickers(category="spot", symbol=symbol)
        buy_price = float(price_data['result']['list'][0]['lastPrice'])

        st.session_state.running = True
        log_area.markdown(f"✅ Current market price: **${buy_price:.2f}**")

        # Step 2: Calculate target price
        target_price = buy_price * (1 + take_profit_percent / 100)
        log_area.markdown(f"🎯 Target price: **${target_price:.2f}**")

        # Step 3: Place market BUY order using quoteQty
        session.place_order(
            category="spot",
            symbol=symbol,
            side="Buy",
            order_type="Market",
            quoteQty=str(usdt_to_spend)
        )
        log_area.markdown(f"📥 Buy order placed using **${usdt_to_spend:.2f}** USDT")

        # Step 4: Monitor market price until target hit
        while st.session_state.running:
            price_data = session.get_tickers(category="spot", symbol=symbol)
            current_price = float(price_data['result']['list'][0]['lastPrice'])

            log_area.markdown(f"📈 Current price: **${current_price:.2f}**")

            if current_price >= target_price:
                session.place_order(
                    category="spot",
                    symbol=symbol,
                    side="Sell",
                    order_type="Market",
                    quoteQty=str(usdt_to_spend)
                )
                log_area.markdown(f"💰 Sold at: **${current_price:.2f}**")
                st.session_state.running = False
                break

            time.sleep(5)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.session_state.running = False

# Button logic
if start and not st.session_state.running:
    run_bot()

if stop:
    st.session_state.running = False
    st.warning("🛑 Bot manually stopped!")
