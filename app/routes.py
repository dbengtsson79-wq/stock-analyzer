from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.analysis import get_stock_data

router = APIRouter()

# Visa startsidan
@router.get("/")
def index():
    return FileResponse("static/index.html")

# API-endpoint som returnerar aktiedata
@router.get("/api/stock/{ticker}")
def stock_data(ticker: str):
    data = get_stock_data(ticker)
    return data
@router.get("/api/test-email")
def test_email():
    from app.notifier import send_signal_email
    send_signal_email("TEST", "buy", 123.45)
    return {"status": "Testmail skickat – kolla din inkorg!"}