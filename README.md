# 🦾 Bybit Take-Profit Trading Bot (with Streamlit GUI)

This project is a simple **crypto trading bot** for **Bybit** that allows you to **automate buying and selling ETH/USDT** (or any spot pair) with a **defined take-profit strategy**. It includes a **Streamlit-powered GUI** where you can input your config, monitor live prices, and **manually stop the bot** at any time.

> 💡 Built using: `Streamlit`, `pybit` (Bybit SDK), `Docker`, `Python 3.11`

---

## 🚀 Features

- 🧠 **Smart logic**: Buys ETH/USDT at market price, then sells when your target profit % is reached.
- 💻 **Streamlit web app**: Clean UI with start/stop buttons, real-time updates.
- 🛑 **Manual stop**: Instantly stop the bot anytime.
- 🧪 **Testnet ready**: Easily toggle between live trading and Bybit Testnet.
- 🐳 **Docker support**: Run anywhere in an isolated container.

---

## 📸 Preview

<img src="https://i.imgur.com/zn3nxn5.png" width="800" />

---

## ⚙️ Requirements

- Python 3.11+
- Bybit API Key (create at [testnet.bybit.com](https://testnet.bybit.com))
- `pip install -r requirements.txt`

---

## 📂 Setup Instructions

### 1. Clone this repo

```bash
git clone https://github.com/your-username/bybit-streamlit-bot.git
cd bybit-streamlit-bot
