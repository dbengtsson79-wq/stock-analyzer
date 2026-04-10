from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
from app.scheduler import start_scheduler
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()  # Starta bakgrundsprocessen
    yield

app = FastAPI(title="Stock Analyzer", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)