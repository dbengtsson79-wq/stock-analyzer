import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.analysis import get_stock_data
from app.notifier import send_signal_email

# Håller koll på senaste signalen per aktie så vi inte skickar samma två gånger
last_signals = {}

def check_tickers():
    tickers = os.getenv("WATCH_TICKERS", "")
    if not tickers:
        return

    for ticker in tickers.split(","):
        ticker = ticker.strip().upper()
        try:
            data = get_stock_data(ticker)
            if not data["data"]:
                continue

            latest = data["data"][-1]
            signal = latest["signal"]
            price = latest["close"]

            # Skicka bara om det är en ny signal sedan sist
            if signal in ["buy", "sell"] and last_signals.get(ticker) != signal:
                send_signal_email(ticker, signal, price)
                last_signals[ticker] = signal
                print(f"Signal skickad: {ticker} - {signal}")
            else:
                print(f"Ingen ny signal för {ticker} (senaste: {signal})")

        except Exception as e:
            print(f"Fel vid kontroll av {ticker}: {e}")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_tickers, "interval", minutes=15)
    scheduler.start()
    print("Schemaläggaren startad – kollar aktier var 15:e minut")
    return scheduler