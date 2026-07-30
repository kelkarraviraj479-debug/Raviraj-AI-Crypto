import pandas as pd
import requests
from ta.momentum import RSIIndicator


def analyze_crypto(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
    data = requests.get(url).json()

    df = pd.DataFrame(data)
    df["close"] = df[4].astype(float)

    rsi_calc = RSIIndicator(close=df["close"], window=14)
    df["RSI"] = rsi_calc.rsi()

    price = df["close"].iloc[-1]
    rsi = df["RSI"].iloc[-1]

    print(f"--- {symbol} Analysis ---")
    print(f"Price: ${price}")
    print(f"RSI: {rsi:.2f}")

    if rsi < 30:
        print("Signal: 🟢 BUY (खरेदी करा)")
    elif rsi > 70:
        print("Signal: 🔴 SELL (विक्री करा)")
    else:
        print("Signal: 🟡 HOLD (थांबा)")


if __name__ == "__main__":
    analyze_crypto("BTCUSDT")
    analyze_crypto("ETHUSDT")
  
