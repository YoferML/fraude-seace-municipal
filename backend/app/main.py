# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles # <- Agregar importación
from backend.app.api.endpoints import router as api_router
from backend.app.core.config import settings
import os

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

# Montar los archivos estáticos del frontend para que Render los muestre en la raíz
frontend_path = os.path.join(settings.ROOT_DIR, "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/status")
def status():
    return {"status": "online"}
