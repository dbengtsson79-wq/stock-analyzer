import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_signal_email(ticker: str, signal: str, price: float):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not all([sender, password, receiver]):
        print("E-postinställningar saknas i .env")
        return

    emoji = "🟢" if signal == "buy" else "🔴"
    subject = f"{emoji} {signal.upper()}-signal för {ticker}"
    body = f"""
    Hej!

    Din Stock Analyzer har upptäckt en signal för {ticker}:

    Signal:  {signal.upper()} {emoji}
    Pris:    {price} USD
    Orsak:   MA20 korsade MA50

    Logga in på din Stock Analyzer för att se grafen.

    /Stock Analyzer
    """

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, msg.as_string())
            print(f"E-post skickad för {ticker} - {signal}")
    except Exception as e:
        print(f"Kunde inte skicka e-post: {e}")