import pandas as pd
import requests
from ta.momentum import RSIIndicator

# Telegram चे डिटेल्स
TELEGRAM_TOKEN = "8656577007:AAG-88xWvn-3kXwk8cTeoHHWC7WtJ_eDAys"
TELEGRAM_CHAT_ID = "8678438898"


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")


def analyze_crypto(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    df["close"] = df[4].astype(float)

    rsi_calc = RSIIndicator(close=df["close"], window=14)
    df["RSI"] = rsi_calc.rsi()

    price = df["close"].iloc[-1]
    rsi = df["RSI"].iloc[-1]

    signal = "🟡 HOLD (थांबा)"
    if rsi < 30:
        signal = "🟢 BUY (खरेदी करा - Market Oversold)"
    elif rsi > 70:
        signal = "🔴 SELL (विक्री करा - Market Overbought)"

    msg = f"🤖 *Crypto Bot Alert*\n\n🪙 *Pair:* {symbol}\n💵 *Price:* ${price:.2f}\n📊 *RSI:* {rsi:.2f}\n\n🎯 *Signal:* {signal}"

    print(msg)
    send_telegram_message(msg)


if __name__ == "__main__":
    analyze_crypto("BTCUSDT")
    analyze_crypto("ETHUSDT")
    
  
