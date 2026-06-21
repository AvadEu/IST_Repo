import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import settings
from web.routers.api import router as api_router
from web.routers.pages import router as pages_router

app = FastAPI(title="Discord Secretary")

app.include_router(pages_router)
app.include_router(api_router, prefix="/api")

os.makedirs(settings.audio_dir, exist_ok=True)
app.mount("/audio", StaticFiles(directory=settings.audio_dir), name="audio")
