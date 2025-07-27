import streamlit as st
import time
from pybit.unified_trading import HTTP

st.set_page_config(page_title="Bybit Take‑Profit Bot", layout="centered")
st.title("🦾 Bybit Take‑Profit Bot")

if "running" not in st.session_state:
    st.session_state.running = False

# Sidebar inputs
api_key = st.sidebar.text_input("API Key", type="password")
api_secret = st.sidebar.text_input("API Secret", type="password")
symbol = st.sidebar.text_input("Symbol", value="ETHUSDT")
usdt_to_spend = st.sidebar.number_input("USDT to Spend", value=50.0, step=1.0)
take_profit_percent = st.sidebar.number_input("Take-Profit %", value=5.0, step=0.5)
testnet = st.sidebar.checkbox("Use Testnet", value=True)
start = st.sidebar.button("🚀 Start Bot")
stop = st.sidebar.button("🛑 Stop Bot")
log = st.empty()

def run_bot():
    try:
        session = HTTP(api_key=api_key, api_secret=api_secret, testnet=testnet)

        # Fetch instrument info
        info = session.get_instruments_info(category="spot", symbol=symbol)['result']['list'][0]
        min_notional_value = float(info['minNotionalValue'])
        min_qty = float(info['minSize'])
        lot_size = float(info['lotSize'])


        # Fetch current price
        price = float(session.get_tickers(category="spot", symbol=symbol)['result']['list'][0]['lastPrice'])

        # Calculate qty with correct precision
        precision = int(abs(len(str(lot_size).split('.')[-1])))
        qty = round(usdt_to_spend / price, precision)

        # Validate against constraints
        if qty < min_qty or qty * price < min_notional_value:
            st.error(f"Min qty: {min_qty}, Min notional: ${min_notional_value}")
            return

        st.session_state.running = True
        log.markdown(f"✅ Price: **${price:.2f}**, Buying **{qty} {symbol[:-4]}**")

        target = price * (1 + take_profit_percent / 100)
        log.markdown(f"🎯 Target: **${target:.2f}**")

        session.place_order(category="spot", symbol=symbol,
                            side="Buy", order_type="Market", qty=str(qty))
        log.markdown("📥 Buy order placed.")

        # Monitor until target reached
        while st.session_state.running:
            current = float(session.get_tickers(category="spot", symbol=symbol)['result']['list'][0]['lastPrice'])
            log.markdown(f"📈 Market: **${current:.2f}**")

            if current >= target:
                session.place_order(category="spot", symbol=symbol,
                                    side="Sell", order_type="Market", qty=str(qty))
                log.markdown(f"💰 Sold at **${current:.2f}**")
                st.session_state.running = False
            else:
                time.sleep(5)

    except Exception as e:
        st.error(f"❌ {e}")
        st.session_state.running = False

if start and not st.session_state.running:
    run_bot()
if stop:
    st.session_state.running = False
    st.warning("🛑 Bot manually stopped.")
