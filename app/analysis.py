import yfinance as yf
import ta

def get_stock_data(ticker: str):
    df = yf.download(ticker, period="6mo", interval="1d", auto_adjust=True)

    if hasattr(df.columns, 'levels'):
        df.columns = df.columns.get_level_values(0)

    df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()
    df["MA20"] = ta.trend.SMAIndicator(df["Close"], window=20).sma_indicator()
    df["MA50"] = ta.trend.SMAIndicator(df["Close"], window=50).sma_indicator()

    df = df.dropna()

# Räkna ut signaler – enbart baserat på MA-korsning
    df["signal"] = "neutral"
    for i in range(1, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        ma_cross_up = prev["MA20"] < prev["MA50"] and curr["MA20"] >= curr["MA50"]
        ma_cross_down = prev["MA20"] > prev["MA50"] and curr["MA20"] <= curr["MA50"]

        if ma_cross_up:
            df.iloc[i, df.columns.get_loc("signal")] = "buy"
        elif ma_cross_down:
            df.iloc[i, df.columns.get_loc("signal")] = "sell"
            
    result = []
    for date, row in df.iterrows():
        result.append({
            "date": str(date.date()),
            "close": round(float(row["Close"]), 2),
            "rsi": round(float(row["RSI"]), 2),
            "ma20": round(float(row["MA20"]), 2),
            "ma50": round(float(row["MA50"]), 2),
            "signal": row["signal"],
        })

    return {"ticker": ticker.upper(), "data": result}